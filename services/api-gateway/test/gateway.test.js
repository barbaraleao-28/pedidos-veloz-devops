const test = require('node:test');
const assert = require('node:assert/strict');
const { executarFluxoPedidoGateway, renderDashboardHtml, tracesRecentes } = require('../src/index');

test('api-gateway: fluxo integrado fim a fim (Gateway -> Pedidos -> Estoque -> Pagamentos) com Tracing Distribuído', async () => {
  const traceId = '9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d';
  const gatewaySpanId = '1122334455667788';

  const res = await executarFluxoPedidoGateway(
    {
      cliente_id: 'CLI-E2E-900',
      sku: 'SKU-MON-02',
      quantidade: 1,
      metodo_pagamento: 'PIX'
    },
    traceId,
    gatewaySpanId
  );

  assert.equal(res.status, 201);
  assert.equal(res.body.ok, true);
  assert.equal(res.body.pedido.status, 'PAGO_E_CONFIRMADO');
  assert.equal(res.body.trace.traceId, traceId);
  assert.equal(res.body.trace.spans.length, 5); // Gateway + Pedidos + Estoque + Pagamentos + DB/Outbox
  assert.ok(tracesRecentes.length >= 1);
});

test('api-gateway: deve renderizar console operacional HTML com indicadores e observabilidade', () => {
  const html = renderDashboardHtml();
  assert.match(html, /Loja Veloz/);
  assert.match(html, /Tracing Distribuído OpenTelemetry/);
});
