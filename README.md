# ⚡ Loja Veloz — Plataforma Distribuída "Pedidos Veloz"

> **Entrega Contínua de uma Plataforma de Pedidos em Microsserviços: do Docker Compose ao Kubernetes com Observabilidade e CI/CD**

Este repositório contém a implementação prática completa desenvolvida para modernizar a operação de e-commerce da **Loja Veloz**, preparando a plataforma **Pedidos Veloz** para picos de tráfego em campanhas promocionais com entregas sem indisponibilidade (*zero-downtime*), escalabilidade automática e rastreabilidade ponta a ponta.

---

## 🏗️ 1. Arquitetura do Sistema

A plataforma **Pedidos Veloz** foi desacoplada em **4 microsserviços principais** seguindo a metodologia **12-Factor App**, além de banco de dados relacional, mensageria de eventos e pilha completa de observabilidade:

| Componente | Porta | Responsabilidade Principal |
| :--- | :---: | :--- |
| **`api-gateway`** | `8080` | Ponto único de entrada HTTP, roteamento, injeção de `x-trace-id` / W3C `traceparent` e Console Operacional. |
| **`pedidos-service`** | `3001` | Orquestrador do fluxo de compra: coordena reserva de estoque, cobrança, persistência no PostgreSQL e publicação do evento `PedidoCriado`. |
| **`pagamentos-service`** | `3002` | Processamento de pagamentos (`PIX`, `CARTAO_CREDITO`), validação antifraude e integração com adquirente externo. |
| **`estoque-service`** | `3003` | Catálogo de SKUs, verificação de saldo e reserva atômica de itens. |
| **`postgres`** | `5432` | Banco de dados relacional PostgreSQL 16 com tabelas `produtos_estoque`, `pedidos`, `pagamentos` e `eventos_outbox`. |
| **`redis`** | `6379` | Mensageria leve para publicação/consumo assíncrono do evento `PedidoCriado`. |
| **`jaeger` / `prometheus` / `grafana`** | `16686` / `9090` / `3000` | Rastreamento distribuído OpenTelemetry (OTLP), coleta de métricas (`/metrics`) e visualização dos *Golden Signals*. |

---

## 📂 2. Estrutura do Repositório

```text
├── .github/workflows/
│   └── ci-cd.yaml                 # Pipeline CI/CD (Lint, Testes, Build Multi-Stage, Scan Trivy, Deploy K8s)
├── db/
│   └── init.sql                   # Schema inicial e carga de produtos no PostgreSQL
├── k8s/
│   ├── 00-namespace.yaml          # Namespace com Pod Security Admission (restricted)
│   ├── 01-configmap.yaml          # Configurações de ambiente desacopladas
│   ├── 02-secret.yaml             # Credenciais sensíveis (Banco e API Key)
│   ├── 03-deployments.yaml        # Deployments com RollingUpdate, Probes e SecurityContext não-root
│   ├── 04-services.yaml           # Services ClusterIP e Ingress HTTP
│   ├── 05-hpa.yaml                # HorizontalPodAutoscaler (CPU 70% / Memória 80%, 2 a 12 pods)
│   └── 06-network-policy.yaml     # NetworkPolicy Zero-Trust restringindo tráfego lateral
├── observability/
│   ├── otel-collector-config.yaml # Pipeline OpenTelemetry Collector (OTLP -> Jaeger/Prometheus)
│   └── prometheus.yml             # Scrape de métricas dos 4 microsserviços
├── services/
│   ├── api-gateway/               # Código-fonte, testes automatizados e Dockerfile multi-stage
│   ├── pedidos-service/           # Código-fonte, testes automatizados e Dockerfile multi-stage
│   ├── pagamentos-service/        # Código-fonte, testes automatizados e Dockerfile multi-stage
│   └── estoque-service/           # Código-fonte, testes automatizados e Dockerfile multi-stage
├── terraform/
│   ├── providers.tf               # Providers AWS e Kubernetes + Backend S3/DynamoDB
│   ├── variables.tf               # Variáveis parametrizadas por ambiente
│   ├── main.tf                    # VPC Multi-AZ, Cluster EKS e RDS PostgreSQL 16
│   └── outputs.tf                 # Endpoints exportados pela infraestrutura
├── screenshots/                   # Evidências e prints reais da execução do projeto
├── Relatorio_Parte_Teorica.pdf    # Entregável 1: Fundamentação Teórica (PDF, 2 a 3 páginas)
├── Relatorio_Parte_Pratica.pdf    # Entregável 2: Relatório Técnico Prático com Prints (PDF, 3 a 6 páginas)
├── Relatorio_Completo_Loja_Veloz.pdf # Versão unificada (Teórica + Prática)
├── docker-compose.yml             # Orquestração completa do ambiente local com 1 comando
├── .env.example                   # Modelo de variáveis de ambiente (12-Factor)
└── package.json                   # Scripts globais de lint e testes automatizados
```

---

## 🚀 3. Como Executar Localmente

### Opção A: Ambiente Completo com Docker Compose (Recomendado)

1. Copie o arquivo de variáveis de ambiente de exemplo:
   ```bash
   cp .env.example .env
   ```
2. Suba todos os microsserviços, banco de dados, mensageria e observabilidade com **um único comando**:
   ```bash
   docker compose up -d --build
   ```
3. Acesse os endpoints locais:
   - **Console Operacional & API Gateway**: `http://localhost:8080`
   - **Jaeger UI (Tracing Distribuído)**: `http://localhost:16686`
   - **Prometheus (Métricas)**: `http://localhost:9090`
   - **Grafana (Dashboards)**: `http://localhost:3000`

### Opção B: Execução Direta de Testes e Validação (Node.js >= 20)

Para validar a sintaxe e executar toda a bateria de testes unitários e de integração fim a fim (que sobe os 4 microsserviços em portas locais e valida a criação de pedidos, reserva de estoque, pagamento, métricas e propagação de `traceId`):

```bash
npm run lint
npm test
```

### Exemplo de Requisição de Criação de Pedido via `curl`

```bash
curl -X POST http://localhost:8080/api/pedidos \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "CLI-9042",
    "sku": "SKU-NOTE-01",
    "quantidade": 1,
    "metodo_pagamento": "PIX"
  }'
```

---

## 🛡️ 4. Segurança, Deploy e Escalabilidade

- **Imagens Enxutas e Seguras**: Todos os `Dockerfile` utilizam *multi-stage build* sobre `node:20-alpine3.19`, executando os processos sob o usuário sem privilégios `appuser` (`UID 10001`), sem arquivos de teste na imagem final.
- **Kubernetes Production-Ready**:
  - **Pod Security Admission (PSA)**: Perfil `restricted` habilitado no namespace `pedidos-veloz`.
  - **SecurityContext**: `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false` e remoção de todas as capabilities Linux (`drop: ["ALL"]`).
  - **Zero-Downtime RollingUpdate**: `maxUnavailable: 0` e `maxSurge: 1` combinados com `readinessProbe` (`/ready`) e `livenessProbe` (`/health`).
  - **Auto Scaling (HPA v2)**: Escala horizontalmente `pedidos-service` (3 a 12 réplicas) e `api-gateway` (2 a 10 réplicas) quando CPU atinge 70% ou Memória 80%, com janela de estabilização de 300s no *scaleDown* para evitar *flapping*.
