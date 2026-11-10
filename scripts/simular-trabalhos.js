const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { executarFluxoPedidoGateway, tracesRecentes, logsCorrelacionados, metricas } = require('../services/api-gateway/src/index');
const { repositorioPedidos, filaEventosOutbox } = require('../services/pedidos-service/src/index');
const { catalogoEstoque } = require('../services/estoque-service/src/index');

async function executarSimulacaoReal() {
  const cenarios = [
    { cliente_id: 'CLI-8821 (Ana Clara)', sku: 'SKU-NOTE-01', quantidade: 1, metodo_pagamento: 'PIX' },
    { cliente_id: 'CLI-4092 (Marcos V.)', sku: 'SKU-MON-02', quantidade: 2, metodo_pagamento: 'CARTAO_CREDITO' },
    { cliente_id: 'CLI-1138 (Beatriz S.)', sku: 'SKU-TEC-03', quantidade: 3, metodo_pagamento: 'PIX' },
    { cliente_id: 'CLI-7740 (Lucas M.)', sku: 'SKU-HEAD-05', quantidade: 1, metodo_pagamento: 'CARTAO_CREDITO' },
    { cliente_id: 'CLI-5519 (Fernanda R.)', sku: 'SKU-MOU-04', quantidade: 2, metodo_pagamento: 'PIX' }
  ];

  for (const c of cenarios) {
    const traceId = crypto.randomBytes(16).toString('hex');
    const spanId = crypto.randomBytes(8).toString('hex');
    await executarFluxoPedidoGateway(c, traceId, spanId);
  }

  const snapshot = {
    geradoEm: new Date().toISOString(),
    metricasGateway: metricas,
    pedidos: repositorioPedidos,
    eventosOutbox: filaEventosOutbox,
    estoqueAtual: Array.from(catalogoEstoque.values()),
    traces: tracesRecentes,
    logs: logsCorrelacionados
  };

  const outDir = path.join(__dirname, '..', 'observability');
  fs.writeFileSync(path.join(outDir, 'runtime-snapshot.json'), JSON.stringify(snapshot, null, 2), 'utf-8');
  console.log('Simulação concluída com sucesso. Pedidos gerados:', snapshot.pedidos.length);
}

executarSimulacaoReal();
