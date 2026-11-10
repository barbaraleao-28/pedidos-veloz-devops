# Entrega Contínua de uma Plataforma de Pedidos em Microsserviços: do Docker Compose ao Kubernetes com Observabilidade e CI/CD

**Parte Teórica — Estudo de Caso: Loja Veloz ("Pedidos Veloz")**

---

## 1. Contexto do Problema (Lide) e Arquitetura de Microsserviços

Nos últimos 12 meses, o e-commerce **Loja Veloz** cresceu bastante, mas a parte técnica não acompanhou esse ritmo. Na prática, cada desenvolvedor subia os serviços "como dava" na própria máquina, as atualizações em produção geravam quedas frequentes no site e, quando um pedido travava, ninguém sabia ao certo se a falha tinha acontecido no Gateway, no banco de dados, na reserva de estoque ou na operadora de pagamento. Como a empresa terá uma grande campanha promocional em 4 semanas, estruturei este plano Cloud DevOps para organizar o fluxo do ambiente local até a produção.

A plataforma **Pedidos Veloz** foi pensada seguindo a arquitetura de microsserviços. Em vez de manter um sistema monolítico (onde todo o código fica preso em um único programa gigante e qualquer erro derruba a loja inteira), dividimos a aplicação em quatro serviços independentes que conversam via HTTP e eventos:

- **API Gateway (`api-gateway`)**: Ponto único de entrada HTTP que recebe as requisições dos clientes e encaminha para os serviços internos.
- **Serviço de Pedidos (`pedidos-service`)**: Coordena a criação e consulta de pedidos, integrando estoque, pagamento, persistência e eventos.
- **Serviço de Estoque (`estoque-service`)**: Cuida do catálogo de produtos e faz a reserva e baixa dos itens comprados.
- **Serviço de Pagamentos (`pagamentos-service`)**: Faz a validação antifraude e comunica com o adquirente externo para aprovar a cobrança.

Nesse cenário *cloud-native*, o papel do **DevOps** vai muito além de apenas escrever scripts: trata-se de aproximar os times de desenvolvimento (*Devs*) e operações (*SRE/Ops*) por meio de automação, padronização e telemetria. Em vez de entregas manuais e arriscadas, a cultura DevOps garante que qualquer código novo passe por testes automáticos, vire uma imagem segura e chegue em produção sem tirar o sistema do ar.

---

## 2. Conteinerização: Diferenças entre Docker e Kubernetes

A conteinerização foi o que viabilizou os microsserviços modernos. Um container empacota o código da aplicação junto com suas bibliotecas e configurações em um processo isolado e leve, acabando com o clássico problema do *"na minha máquina funciona, mas no servidor não"*.

Muita gente confunde o papel do **Docker** com o do **Kubernetes**, mas eles atuam em etapas diferentes e complementares:

- **Docker e Docker Compose**: Focados em construir a imagem do container (`Dockerfile`) e rodar múltiplos containers em uma única máquina (`docker-compose.yml`). É a ferramenta ideal para padronizar o ambiente local de desenvolvimento e testes rápidos.
- **Kubernetes (K8s)**: É um orquestrador de containers para produção. Enquanto o Docker cria e roda o container isolado, o Kubernetes atua como o "maestro" que gerencia dezenas ou centenas de containers espalhados em vários servidores (nós), cuidando de auto-recuperação, balanço de carga e escalabilidade.

| Critério / Aspecto | Docker & Docker Compose | Kubernetes (K8s) |
| :--- | :--- | :--- |
| **Foco Principal** | Construção de imagens e execução local em um único host. | Orquestração distribuída em cluster de múltiplos servidores. |
| **Quando Utilizar** | Desenvolvimento diário, testes locais e validação rápida. | Ambientes de produção e homologação com alta disponibilidade. |
| **Tolerância a Falhas** | Básica (reinicia o container se o processo cair na máquina). | Auto-cura completa (recria Pods em outro servidor se um nó falhar). |
| **Escalabilidade** | Manual (limitada aos recursos de CPU/RAM da máquina local). | Automática via HPA/VPA de acordo com o pico de acessos. |
| **Atualização (Deploy)** | Recria os containers locais (gera pequena parada). | *Rolling Update*, *Blue-Green* ou *Canary* sem indisponibilidade. |

---

## 3. Fundamentação Teórica: Orquestração, CI/CD e Observabilidade

### 3.1 Orquestração de Containers em Produção
Quando temos quatro ou mais microsserviços rodando várias cópias ao mesmo tempo, fica impossível gerenciar tudo manualmente. A orquestração com Kubernetes funciona baseada em **estado desejado** (declarado em manifestos YAML). Se definirmos que o Serviço de Pedidos precisa de 3 réplicas saudáveis, o *Control Plane* do Kubernetes monitora os Pods o tempo todo através de sondas (`livenessProbe` para saber se o container travou e `readinessProbe` para saber se ele já pode receber clientes), distribuindo o tráfego de rede automaticamente através dos objetos `Service`.

### 3.2 CI/CD em Ambientes Distribuídos
Em uma arquitetura distribuída, fazer deploy manual copiando arquivos para o servidor é receita certa para erros. Por isso adotamos **CI/CD** (Integração Contínua e Entrega Contínua). Na etapa de **CI**, cada alteração enviada ao Git dispara automaticamente a validação de sintaxe (*lint*), os testes automatizados de cada microsserviço, a construção da imagem Docker e a checagem de segurança (*scan* de vulnerabilidades). Se tudo passar nos *gates* de qualidade, a etapa de **CD** publica a imagem versionada no Registry e atualiza o cluster Kubernetes de forma controlada.

### 3.3 Os Três Pilares da Observabilidade (Métricas, Logs e Traces)
Monitorar apenas se o servidor está ligado não basta em microsserviços. A observabilidade nos permite entender o que acontece dentro do sistema através de três pilares que trabalham juntos:
1. **Métricas (Prometheus & Grafana)**: Valores numéricos agregados ao longo do tempo, como uso de CPU, quantidade de pedidos por segundo e taxa de erros HTTP 5xx (*Golden Signals*). Elas mostram rapidamente *que* algo está fora do normal.
2. **Logs Estruturados (JSON no `stdout`)**: Registros detalhados de cada evento que aconteceu no código (ex: `"Estoque insuficiente para o SKU X"`). Seguindo o *12-Factor App*, os containers jogam os logs na saída padrão em formato JSON.
3. **Tracing Distribuído (OpenTelemetry & Jaeger)**: Resolve a maior dor da Loja Veloz. Quando o cliente clica em comprar, o API Gateway cria um código único (`traceId`) e o repassa nos cabeçalhos HTTP para Pedidos, Estoque e Pagamentos. Assim conseguimos ver uma linha do tempo completa (*spans*) mostrando exatamente quantos milissegundos cada microsserviço gastou.

---

## 4. Pesquisa de Caso Concreto e Comparativo de Deploy

> **Caso de Referência Pesquisado: Google Cloud "Online Boutique" (`microservices-demo`) & 12-Factor App**
> Para desenhar a solução da Loja Veloz, pesquisei o repositório oficial de referência *Online Boutique* (`GoogleCloudPlatform/microservices-demo`), que é uma loja virtual *cloud-native* completa em microsserviços rodando no Kubernetes. Assim como no case do Google, adotei um API Gateway na borda, microsserviços desacoplados sem estado (*stateless*), sondas de saúde nativas, instrumentação com OpenTelemetry/Jaeger e manifestos declarativos com HPA. Também apliquei os princípios da metodologia **12-Factor App** (Fator III - configurações em variáveis de ambiente via `ConfigMap`/`Secret`; Fator VI - processos *stateless*; e Fator XI - logs como fluxos de eventos).

| Estratégia | Como Funciona na Prática | Custo de Infra | Uso na Loja Veloz |
| :--- | :--- | :--- | :--- |
| **Rolling Update** | Substitui os Pods antigos pelos novos aos poucos (`maxUnavailable: 0`). | Baixo (+1 Pod extra durante a troca). | Padrão adotado em todos os microsserviços no MVP. |
| **Blue-Green** | Sobe um ambiente inteiro duplicado (Verde) e vira a chave do roteador. | Alto (dobro de servidores ativos). | Descartado no MVP pelo custo elevado de manter 2 ambientes. |
| **Canary Release** | Libera a versão nova para apenas 5% a 10% dos clientes inicialmente. | Baixo (via Ingress ou Service Mesh). | Recomendado para mudanças críticas no `pagamentos-service`. |

---

## 5. Justificativa das Decisões Arquiteturais Adotadas no Projeto

- **Padronização Local com Docker Compose**: Permite subir os 4 microsserviços, o PostgreSQL, o Redis e toda a pilha de observabilidade (Jaeger, Prometheus e Grafana) com um único comando (`docker compose up -d --build`).
- **Imagens Multi-Stage e Usuário Não-Root**: Nos Dockerfiles, utilizei *multi-stage build* com `node:20-alpine3.19` e usuário sem privilégios (`UID 10001`), reduzindo o tamanho da imagem e impedindo ataques de escalação de privilégio.
- **Mensageria Assíncrona (Evento `PedidoCriado`)**: Incluí o Redis junto ao padrão Outbox para publicar o evento `PedidoCriado` assim que o pedido é pago, desacoplando ações secundárias (como nota fiscal e e-mail).
- **Deploy `RollingUpdate` (`maxUnavailable: 0`) + Escalabilidade com HPA**: Como nossos microsserviços são *stateless*, o HPA escala de 3 para 12 réplicas em segundos quando a CPU passa de 70% na promoção, sem precisar reiniciar Pods como faria o VPA isolado.
- **Infraestrutura como Código (IaC) com Terraform**: Estrutura reproduzível para criar VPC Multi-AZ, cluster EKS e banco RDS PostgreSQL.

---

## 6. Referências Bibliográficas (Fontes Primárias)

1. **KUBERNETES OFFICIAL DOCUMENTATION**. *Concepts: Workloads, Services, ConfigMaps, Secrets, Pod Security Admission & HPA*. Disponível em: https://kubernetes.io/docs/home/
2. **DOCKER OFFICIAL DOCUMENTATION**. *Multi-stage builds, Dockerfile best practices & Docker Compose*. Disponível em: https://docs.docker.com/
3. **WIGGINS, Adam**. *The Twelve-Factor App (Metodologia Cloud-Native)*. Disponível em: https://12factor.net/pt_br/
4. **GOOGLE CLOUD PLATFORM**. *Online Boutique (microservices-demo): Reference Architecture*. Disponível em: https://github.com/GoogleCloudPlatform/microservices-demo
5. **OPENTELEMETRY & JAEGER DOCUMENTATION**. *W3C Trace Context and Distributed Tracing*. Disponível em: https://opentelemetry.io/docs/
6. **HASHICORP TERRAFORM DOCUMENTATION**. *Infrastructure as Code (IaC)*. Disponível em: https://developer.hashicorp.com/terraform/docs
