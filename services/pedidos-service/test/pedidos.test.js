const test = require('node:test');
const assert = require('node:assert/strict');
const { orquestrarCriacaoPedido } = require('../src/index');

test('pedidos-service: deve orquestrar reserva de estoque, pagamento e emitir evento PedidoCriado com TraceId', async () => {
  const resultado = await orquestrarCriacaoPedido(
    { cliente_id: 'CLI-TESTE-10', sku: 'SKU-MOU-04', quantidade: 2, metodo_pagamento: 'PIX' },
    { traceId: '4bf92f3577b34da6a3ce929d0e0e4736', spanId: '00f067aa0ba902b7', parentSpanId: null }
  );

  assert.equal(resultado.ok, true);
  assert.equal(resultado.codigo, 201);
  assert.equal(resultado.pedido.status, 'PAGO_E_CONFIRMADO');
  assert.equal(resultado.evento_publicado, 'PedidoCriado');
  assert.equal(resultado.pedido.trace_id, '4bf92f3577b34da6a3ce929d0e0e4736');
  assert.equal(resultado.spans.length, 3);
});

test('pedidos-service: deve rejeitar pedido com campos obrigatórios ausentes', async () => {
  const resultado = await orquestrarCriacaoPedido(
    { cliente_id: '', sku: '' },
    { traceId: '4bf92f3577b34da6a3ce929d0e0e4736', spanId: '00f067aa0ba902b7', parentSpanId: null }
  );

  assert.equal(resultado.ok, false);
  assert.equal(resultado.codigo, 400);
});
