const test = require('node:test');
const assert = require('node:assert/strict');
const { reservarItem, catalogoEstoque } = require('../src/index');

test('estoque-service: deve reservar item com estoque disponível e atualizar saldo', () => {
  const saldoInicial = catalogoEstoque.get('SKU-TEC-03').quantidade_disponivel;
  const resultado = reservarItem('SKU-TEC-03', 2);

  assert.equal(resultado.ok, true);
  assert.equal(resultado.codigo, 200);
  assert.equal(resultado.reserva.sku, 'SKU-TEC-03');
  assert.equal(resultado.reserva.quantidade_reservada, 2);
  assert.equal(resultado.reserva.saldo_restante, saldoInicial - 2);
});

test('estoque-service: deve retornar erro 409 quando quantidade solicitada excede estoque', () => {
  const resultado = reservarItem('SKU-NOTE-01', 9999);
  assert.equal(resultado.ok, false);
  assert.equal(resultado.codigo, 409);
  assert.match(resultado.erro, /Estoque insuficiente/);
});

test('estoque-service: deve retornar erro 404 para SKU inexistente', () => {
  const resultado = reservarItem('SKU-INEXISTENTE-99', 1);
  assert.equal(resultado.ok, false);
  assert.equal(resultado.codigo, 404);
});
