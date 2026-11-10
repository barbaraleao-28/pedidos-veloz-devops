const test = require('node:test');
const assert = require('node:assert/strict');
const { processarTransacao } = require('../src/index');

test('pagamentos-service: deve aprovar pagamento válido dentro do limite operacional', () => {
  const res = processarTransacao({
    pedido_id: 'PED-1001',
    cliente_id: 'CLI-01',
    valor: 2199.00,
    metodo: 'PIX'
  });

  assert.equal(res.ok, true);
  assert.equal(res.codigo, 200);
  assert.equal(res.transacao.status, 'APROVADO');
  assert.match(res.transacao.pagamento_id, /^PAY-/);
  assert.match(res.transacao.autorizacao_externa, /^AUTH-/);
});

test('pagamentos-service: deve recusar pagamento acima do teto antifraude (R$ 50.000)', () => {
  const res = processarTransacao({
    pedido_id: 'PED-9999',
    cliente_id: 'CLI-02',
    valor: 75000.00,
    metodo: 'CARTAO_CREDITO'
  });

  assert.equal(res.ok, false);
  assert.equal(res.codigo, 422);
  assert.equal(res.transacao.status, 'RECUSADO');
});

test('pagamentos-service: deve rejeitar payload sem pedido_id ou valor inválido', () => {
  const res = processarTransacao({ pedido_id: '', valor: -10 });
  assert.equal(res.ok, false);
  assert.equal(res.codigo, 400);
});
