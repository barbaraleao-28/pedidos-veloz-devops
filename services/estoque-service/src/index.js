const http = require('node:http');
const crypto = require('node:crypto');

const PORT = Number(process.env.ESTOQUE_PORT || process.env.PORT || 3003);
const SERVICE_NAME = 'estoque-service';
const APP_VERSION = process.env.APP_VERSION || '1.2.0';

// Catálogo inicial em memória (sincronizado com db/init.sql para execução resiliente)
const catalogoEstoque = new Map([
  ['SKU-NOTE-01', { sku: 'SKU-NOTE-01', nome: 'Notebook Gamer Veloz Pro 16GB', preco_unitario: 4899.90, quantidade_disponivel: 45, quantidade_reservada: 2 }],
  ['SKU-MON-02',  { sku: 'SKU-MON-02',  nome: 'Monitor Ultrawide 34" 144Hz', preco_unitario: 2199.00, quantidade_disponivel: 80, quantidade_reservada: 5 }],
  ['SKU-TEC-03',  { sku: 'SKU-TEC-03',  nome: 'Teclado Mecânico RGB Switch Blue', preco_unitario: 349.90, quantidade_disponivel: 150, quantidade_reservada: 12 }],
  ['SKU-MOU-04',  { sku: 'SKU-MOU-04',  nome: 'Mouse Wireless UltraLeve 26000 DPI', preco_unitario: 289.50, quantidade_disponivel: 200, quantidade_reservada: 8 }],
  ['SKU-HEAD-05', { sku: 'SKU-HEAD-05', nome: 'Headset Surround 7.1 Cancelamento Ruído', preco_unitario: 499.00, quantidade_disponivel: 65, quantidade_reservada: 3 }]
]);

const metricas = {
  requestsTotal: 0,
  reservasSucesso: 0,
  reservasFalha: 0,
  latenciaSomaMs: 0
};

function logEstruturado(level, msg, meta = {}) {
  const entry = {
    timestamp: new Date().toISOString(),
    level,
    service: SERVICE_NAME,
    version: APP_VERSION,
    ...meta,
    message: msg
  };
  console.log(JSON.stringify(entry));
}

function extrairTraceContext(req) {
  const traceId = req.headers['x-trace-id'] || crypto.randomBytes(16).toString('hex');
  const parentSpanId = req.headers['x-span-id'] || null;
  const spanId = crypto.randomBytes(8).toString('hex');
  return { traceId, parentSpanId, spanId };
}

function lerJsonBody(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', chunk => { raw += chunk; });
    req.on('end', () => {
      if (!raw) return resolve({});
      try {
        resolve(JSON.parse(raw));
      } catch (err) {
        reject(new Error('JSON inválido'));
      }
    });
    req.on('error', reject);
  });
}

function reservarItem(sku, quantidade) {
  const item = catalogoEstoque.get(sku);
  if (!item) {
    return { ok: false, codigo: 404, erro: `SKU '${sku}' não encontrado no catálogo.` };
  }
  if (!Number.isInteger(quantidade) || quantidade <= 0) {
    return { ok: false, codigo: 400, erro: 'A quantidade solicitada deve ser um inteiro positivo.' };
  }
  if (item.quantidade_disponivel < quantidade) {
    return {
      ok: false,
      codigo: 409,
      erro: `Estoque insuficiente para ${sku}. Disponível: ${item.quantidade_disponivel}, Solicitado: ${quantidade}`
    };
  }

  item.quantidade_disponivel -= quantidade;
  item.quantidade_reservada += quantidade;

  return {
    ok: true,
    codigo: 200,
    reserva: {
      reserva_id: 'RES-' + crypto.randomBytes(4).toString('hex').toUpperCase(),
      sku: item.sku,
      nome: item.nome,
      quantidade_reservada: quantidade,
      preco_unitario: item.preco_unitario,
      valor_total: Number((item.preco_unitario * quantidade).toFixed(2)),
      saldo_restante: item.quantidade_disponivel
    }
  };
}

function criarServidorEstoque() {
  return http.createServer(async (req, res) => {
    const inicio = performance.now();
    const { traceId, parentSpanId, spanId } = extrairTraceContext(req);
    metricas.requestsTotal++;

    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('x-trace-id', traceId);
    res.setHeader('x-span-id', spanId);

    const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);

    // Probes Kubernetes
    if (req.method === 'GET' && url.pathname === '/health') {
      res.writeHead(200);
      return res.end(JSON.stringify({ status: 'UP', service: SERVICE_NAME, version: APP_VERSION }));
    }

    if (req.method === 'GET' && url.pathname === '/ready') {
      res.writeHead(200);
      return res.end(JSON.stringify({ ready: true, catalog_size: catalogoEstoque.size }));
    }

    // Endpoint Prometheus Metrics
    if (req.method === 'GET' && url.pathname === '/metrics') {
      res.setHeader('Content-Type', 'text/plain; version=0.0.4; charset=utf-8');
      res.writeHead(200);
      return res.end([
        '# HELP estoque_http_requests_total Total de requisicoes HTTP no servico de estoque',
        '# TYPE estoque_http_requests_total counter',
        `estoque_http_requests_total{service="${SERVICE_NAME}"} ${metricas.requestsTotal}`,
        '# HELP estoque_reservas_total Total de reservas de estoque por status',
        '# TYPE estoque_reservas_total counter',
        `estoque_reservas_total{status="sucesso"} ${metricas.reservasSucesso}`,
        `estoque_reservas_total{status="falha"} ${metricas.reservasFalha}`,
        '# HELP estoque_latency_ms_sum Soma da latencia em milissegundos',
        '# TYPE estoque_latency_ms_sum counter',
        `estoque_latency_ms_sum ${metricas.latenciaSomaMs.toFixed(2)}`
      ].join('\n') + '\n');
    }

    // Listagem de estoque
    if (req.method === 'GET' && url.pathname === '/estoque') {
      const itens = Array.from(catalogoEstoque.values());
      const duracao = Number((performance.now() - inicio).toFixed(2));
      metricas.latenciaSomaMs += duracao;
      logEstruturado('INFO', 'Consulta de catálogo de estoque realizada', {
        traceId, spanId, parentSpanId, httpMethod: 'GET', path: '/estoque', statusCode: 200, durationMs: duracao
      });
      res.writeHead(200);
      return res.end(JSON.stringify({ service: SERVICE_NAME, total_skus: itens.length, itens }));
    }

    // Reserva e baixa de estoque
    if (req.method === 'POST' && url.pathname === '/estoque/reservar') {
      try {
        const body = await lerJsonBody(req);
        const resultado = reservarItem(body.sku, Number(body.quantidade));
        const duracao = Number((performance.now() - inicio).toFixed(2));
        metricas.latenciaSomaMs += duracao;

        if (!resultado.ok) {
          metricas.reservasFalha++;
          logEstruturado('WARN', `Falha na reserva de estoque: ${resultado.erro}`, {
            traceId, spanId, parentSpanId, sku: body.sku, quantidade: body.quantidade, statusCode: resultado.codigo, durationMs: duracao
          });
          res.writeHead(resultado.codigo);
          return res.end(JSON.stringify({ erro: resultado.erro, traceId, spanId }));
        }

        metricas.reservasSucesso++;
        logEstruturado('INFO', `Reserva concluída para SKU ${body.sku} (${body.quantidade} un.)`, {
          traceId, spanId, parentSpanId, reservaId: resultado.reserva.reserva_id, sku: body.sku, saldoRestante: resultado.reserva.saldo_restante, statusCode: 200, durationMs: duracao
        });
        res.writeHead(200);
        return res.end(JSON.stringify({ ...resultado.reserva, traceId, spanId, durationMs: duracao }));
      } catch (err) {
        res.writeHead(400);
        return res.end(JSON.stringify({ erro: err.message, traceId }));
      }
    }

    res.writeHead(404);
    res.end(JSON.stringify({ erro: 'Rota não encontrada no estoque-service' }));
  });
}

if (require.main === module) {
  const server = criarServidorEstoque();
  server.listen(PORT, () => {
    logEstruturado('INFO', `Microsserviço ${SERVICE_NAME} iniciado na porta ${PORT}`, { port: PORT });
  });
}

module.exports = { criarServidorEstoque, reservarItem, catalogoEstoque };
