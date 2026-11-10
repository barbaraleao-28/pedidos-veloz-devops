import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(ROOT_DIR, "screenshots")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
os.makedirs(DOCS_DIR, exist_ok=True)

# A4 @ 180 DPI: 1488 x 2105 px (excelente nitidez e tamanho de arquivo leve)
PAGE_W = 1488
PAGE_H = 2105
MARGIN_X = 95
CONTENT_W = PAGE_W - (2 * MARGIN_X)

FONT_DIR = r"C:\Windows\Fonts"
def get_font(name, size):
    p = os.path.join(FONT_DIR, name)
    return ImageFont.truetype(p, size) if os.path.exists(p) else ImageFont.load_default()

F_REG = lambda s: get_font("segoeui.ttf", s)
F_BOLD = lambda s: get_font("segoeuib.ttf", s)
F_ITALIC = lambda s: get_font("segoeuii.ttf", s)
F_MONO = lambda s: get_font("consola.ttf", s)
F_MONO_B = lambda s: get_font("consolab.ttf", s)


class PageBuilder:
    def __init__(self, doc_title, part_subtitle, page_num, total_pages):
        self.img = Image.new("RGB", (PAGE_W, PAGE_H), (255, 255, 255))
        self.d = ImageDraw.Draw(self.img)
        self.y = 115
        self.page_num = page_num
        self.total_pages = total_pages
        self._draw_header_footer(doc_title, part_subtitle)

    def _draw_header_footer(self, doc_title, part_subtitle):
        # Top running header
        self.d.rectangle([0, 0, PAGE_W, 12], fill=(15, 23, 42))
        self.d.rectangle([0, 12, PAGE_W, 18], fill=(14, 165, 233))
        self.d.text((MARGIN_X, 38), doc_title, font=F_BOLD(18), fill=(71, 85, 105))
        self.d.text((PAGE_W - MARGIN_X - 380, 38), part_subtitle, font=F_ITALIC(17), fill=(100, 116, 139))
        self.d.line([MARGIN_X, 74, PAGE_W - MARGIN_X, 74], fill=(203, 213, 225), width=2)

        # Bottom footer
        fy = PAGE_H - 72
        self.d.line([MARGIN_X, fy, PAGE_W - MARGIN_X, fy], fill=(203, 213, 225), width=2)
        self.d.text(
            (MARGIN_X, fy + 16),
            "Projeto Cloud DevOps — Estudo de Caso Loja Veloz (Plataforma Pedidos Veloz)",
            font=F_REG(17),
            fill=(100, 116, 139),
        )
        p_str = f"Página {self.page_num} de {self.total_pages}"
        pw = self.d.textlength(p_str, font=F_BOLD(17))
        self.d.text((PAGE_W - MARGIN_X - pw, fy + 16), p_str, font=F_BOLD(17), fill=(51, 65, 85))

    def title_banner(self, main_title, subtitle, meta_line):
        self.d.rounded_rectangle(
            [MARGIN_X, self.y, PAGE_W - MARGIN_X, self.y + 158],
            radius=12,
            fill=(15, 23, 42),
            outline=(14, 165, 233),
            width=2,
        )
        self.d.text((MARGIN_X + 28, self.y + 20), main_title, font=F_BOLD(26), fill=(248, 250, 252))
        self.d.text((MARGIN_X + 28, self.y + 62), subtitle, font=F_BOLD(20), fill=(56, 189, 248))
        self.d.text((MARGIN_X + 28, self.y + 108), meta_line, font=F_REG(18), fill=(203, 213, 225))
        self.y += 184

    def section(self, text):
        self.y += 8
        self.d.rectangle([MARGIN_X, self.y + 4, MARGIN_X + 8, self.y + 34], fill=(2, 132, 199))
        self.d.text((MARGIN_X + 20, self.y), text, font=F_BOLD(25), fill=(15, 23, 42))
        self.y += 44
        self.d.line([MARGIN_X, self.y - 4, PAGE_W - MARGIN_X, self.y - 4], fill=(226, 232, 240), width=2)
        self.y += 8

    def subsection(self, text):
        self.y += 4
        self.d.text((MARGIN_X, self.y), text, font=F_BOLD(21), fill=(3, 105, 161))
        self.y += 34

    def paragraph(self, text, font_size=19, line_spacing=30, color=(30, 41, 59)):
        font = F_REG(font_size)
        words = text.split(" ")
        lines = []
        curr = ""
        for w in words:
            test = (curr + " " + w).strip()
            if self.d.textlength(test, font=font) <= CONTENT_W:
                curr = test
            else:
                lines.append(curr)
                curr = w
        if curr:
            lines.append(curr)

        for ln in lines:
            self.d.text((MARGIN_X, self.y), ln, font=font, fill=color)
            self.y += line_spacing
        self.y += 10

    def bullet(self, bold_prefix, text, font_size=18.5, line_spacing=28):
        f_b = F_BOLD(int(font_size))
        f_r = F_REG(int(font_size))
        indent = 26
        max_w = CONTENT_W - indent

        self.d.text((MARGIN_X + 4, self.y), "•", font=f_b, fill=(2, 132, 199))
        full_words = (bold_prefix + " " + text).split(" ")
        prefix_word_count = len(bold_prefix.split(" ")) if bold_prefix else 0

        # Render word by word with wrapping
        cx = MARGIN_X + indent
        cy = self.y
        for idx, w in enumerate(full_words):
            f_use = f_b if idx < prefix_word_count else f_r
            c_use = (15, 23, 42) if idx < prefix_word_count else (30, 41, 59)
            w_space = w + " "
            ww = self.d.textlength(w_space, font=f_use)
            if cx + ww > MARGIN_X + CONTENT_W:
                cx = MARGIN_X + indent
                cy += line_spacing
            self.d.text((cx, cy), w_space, font=f_use, fill=c_use)
            cx += ww
        self.y = cy + line_spacing + 6

    def callout_box(self, title, body_text, bg=(240, 249, 255), border=(14, 165, 233)):
        f_t = F_BOLD(19)
        f_b = F_REG(18)
        inner_w = CONTENT_W - 44
        words = body_text.split(" ")
        lines = []
        curr = ""
        for w in words:
            test = (curr + " " + w).strip()
            if self.d.textlength(test, font=f_b) <= inner_w:
                curr = test
            else:
                lines.append(curr)
                curr = w
        if curr:
            lines.append(curr)

        box_h = 46 + len(lines) * 27 + 16
        self.d.rounded_rectangle([MARGIN_X, self.y, PAGE_W - MARGIN_X, self.y + box_h], radius=8, fill=bg, outline=border, width=2)
        self.d.rectangle([MARGIN_X, self.y, MARGIN_X + 8, self.y + box_h], fill=border)
        self.d.text((MARGIN_X + 22, self.y + 12), title, font=f_t, fill=(15, 23, 42))
        ty = self.y + 42
        for ln in lines:
            self.d.text((MARGIN_X + 22, ty), ln, font=f_b, fill=(30, 41, 59))
            ty += 27
        self.y += box_h + 14

    def table(self, headers, rows, col_widths):
        row_h = 40
        # Header
        self.d.rectangle([MARGIN_X, self.y, PAGE_W - MARGIN_X, self.y + row_h], fill=(15, 23, 42))
        cx = MARGIN_X
        for h_text, cw in zip(headers, col_widths):
            self.d.text((cx + 12, self.y + 9), h_text, font=F_BOLD(17), fill=(248, 250, 252))
            cx += cw
        self.y += row_h

        for r_idx, row in enumerate(rows):
            bg = (248, 250, 252) if r_idx % 2 == 0 else (255, 255, 255)
            # Determine lines needed for cells
            cell_lines = []
            max_lines = 1
            for cell_text, cw in zip(row, col_widths):
                words = str(cell_text).split(" ")
                lines = []
                curr = ""
                for w in words:
                    test = (curr + " " + w).strip()
                    if self.d.textlength(test, font=F_REG(16)) <= cw - 20:
                        curr = test
                    else:
                        lines.append(curr)
                        curr = w
                if curr:
                    lines.append(curr)
                cell_lines.append(lines)
                max_lines = max(max_lines, len(lines))

            dyn_h = max_lines * 24 + 16
            self.d.rectangle([MARGIN_X, self.y, PAGE_W - MARGIN_X, self.y + dyn_h], fill=bg, outline=(203, 213, 225))
            cx = MARGIN_X
            for c_idx, (lines, cw) in enumerate(zip(cell_lines, col_widths)):
                f_cell = F_BOLD(16) if c_idx == 0 else F_REG(16)
                ty = self.y + 8
                for ln in lines:
                    self.d.text((cx + 10, ty), ln, font=f_cell, fill=(30, 41, 59))
                    ty += 24
                cx += cw
            self.y += dyn_h
        self.y += 14

    def embed_screenshot(self, filename, caption, max_h=430):
        path = os.path.join(SCREENSHOTS_DIR, filename)
        shot = Image.open(path)
        ratio = min(CONTENT_W / shot.width, max_h / shot.height)
        new_w = int(shot.width * ratio)
        new_h = int(shot.height * ratio)
        resized = shot.resize((new_w, new_h), Image.Resampling.LANCZOS)

        x_pos = MARGIN_X + (CONTENT_W - new_w) // 2
        self.d.rounded_rectangle(
            [x_pos - 4, self.y - 4, x_pos + new_w + 4, self.y + new_h + 4],
            radius=8,
            fill=(15, 23, 42),
            outline=(148, 163, 184),
            width=2,
        )
        self.img.paste(resized, (x_pos, self.y))
        self.y += new_h + 10
        cap_w = self.d.textlength(caption, font=F_ITALIC(16))
        self.d.text((MARGIN_X + (CONTENT_W - cap_w) // 2, self.y), caption, font=F_ITALIC(16), fill=(71, 85, 105))
        self.y += 30


# ============================================================================
# CONSTRUÇÃO DA PARTE TEÓRICA (Exatas 3 Páginas - Mín 2 | Máx 3)
# ============================================================================
def build_parte_teorica(total_pages=3, start_page=1):
    pages = []
    hdr_title = "RELATÓRIO TÉCNICO — PARTE TEÓRICA (CLOUD DEVOPS)"
    hdr_sub = "Estudo de Caso: Loja Veloz (Pedidos Veloz)"

    # ---------------- PÁGINA 1 ----------------
    p1 = PageBuilder(hdr_title, hdr_sub, start_page, total_pages)
    p1.title_banner(
        "ENTREGA CONTÍNUA DE UMA PLATAFORMA DE PEDIDOS EM MICROSSERVIÇOS",
        "Parte Teórica: Do Docker Compose ao Kubernetes com Observabilidade e CI/CD",
        "Caso: Loja Veloz (Pedidos Veloz)  |  Disciplina: Arquitetura Cloud DevOps & Containers",
    )

    p1.section("1. Contexto do Problema (Lide) e Arquitetura de Microsserviços")
    p1.paragraph(
        "Nos últimos 12 meses, o e-commerce Loja Veloz cresceu bastante, mas a parte técnica não acompanhou esse ritmo. "
        "Na prática, cada desenvolvedor subia os serviços 'como dava' na própria máquina, as atualizações em produção geravam "
        "quedas frequentes no site e, quando um pedido travava, ninguém sabia ao certo se a falha tinha acontecido no Gateway, "
        "no banco de dados, na reserva de estoque ou na operadora de pagamento. Como a empresa terá uma grande campanha "
        "promocional em 4 semanas, estruturei este plano Cloud DevOps para organizar o fluxo do ambiente local até a produção."
    )
    p1.paragraph(
        "A plataforma 'Pedidos Veloz' foi pensada seguindo a arquitetura de microsserviços. Em vez de manter um sistema monolítico "
        "(onde todo o código fica preso em um único programa gigante e qualquer erro derruba a loja inteira), dividimos a aplicação "
        "em quatro serviços independentes que conversam via HTTP e eventos: API Gateway, Serviço de Pedidos, Serviço de Estoque e "
        "Serviço de Pagamentos, apoiados pelo PostgreSQL e pelo Redis. Assim, cada serviço tem sua própria responsabilidade e pode "
        "ser atualizado ou escalado separadamente."
    )
    p1.paragraph(
        "Nesse cenário cloud-native, o papel do DevOps vai muito além de apenas escrever scripts: trata-se de unir os times de "
        "desenvolvimento (Devs) e operações (SRE/Ops) por meio de automação, padronização e telemetria. Em vez de entregas manuais "
        "e arriscadas, o DevOps garante que qualquer código novo passe por testes automáticos, vire uma imagem segura e chegue em "
        "produção sem tirar o sistema do ar."
    )

    p1.section("2. Conteinerização: Diferenças entre Docker e Kubernetes")
    p1.paragraph(
        "Durante os estudos da disciplina, fica claro que a conteinerização foi o que viabilizou os microsserviços modernos. Um "
        "container empacota o código da aplicação junto com suas bibliotecas e configurações em um processo isolado e leve, "
        "acabando com o clássico problema do 'na minha máquina funciona, mas no servidor não'."
    )
    p1.paragraph(
        "Muita gente confunde o papel do Docker com o do Kubernetes, mas eles atuam em etapas diferentes e complementares. O Docker "
        "(junto com o Docker Compose) é voltado para construir a imagem do container e rodar múltiplos containers em uma única "
        "máquina, sendo perfeito para padronizar o ambiente local dos desenvolvedores. Já o Kubernetes é um orquestrador de "
        "containers para produção: ele gerencia dezenas ou centenas de containers distribuídos em vários servidores (nós)."
    )

    p1.table(
        ["Critério / Aspecto", "Docker & Docker Compose", "Kubernetes (K8s)"],
        [
            ["Foco Principal", "Construção de imagens e execução local em um único host.", "Orquestração distribuída em cluster de múltiplos servidores."],
            ["Quando Utilizar", "Desenvolvimento diário, testes locais e validação rápida.", "Ambientes de produção e homologação com alta disponibilidade."],
            ["Tolerância a Falhas", "Básica (reinicia o container se o processo cair na máquina).", "Auto-cura completa (recria Pods em outro servidor se um nó falhar)."],
            ["Escalabilidade", "Manual (limitada aos recursos de CPU/RAM da máquina local).", "Automática via HPA/VPA de acordo com o pico de acessos."],
            ["Atualização (Deploy)", "Recria os containers locais (gera pequena parada).", "Rolling Update, Blue-Green ou Canary sem indisponibilidade."],
        ],
        [270, 500, 528],
    )
    pages.append(p1.img)

    # ---------------- PÁGINA 2 ----------------
    p2 = PageBuilder(hdr_title, hdr_sub, start_page + 1, total_pages)
    p2.section("3. Fundamentação Teórica: Orquestração, CI/CD e Observabilidade")

    p2.subsection("3.1 Orquestração de Containers em Produção")
    p2.paragraph(
        "Quando temos quatro ou mais microsserviços rodando várias cópias ao mesmo tempo, fica impossível gerenciar tudo na mão. "
        "A orquestração de containers com Kubernetes funciona baseada em 'estado desejado' (declarado em arquivos YAML). Se "
        "definirmos que o Serviço de Pedidos precisa de 3 réplicas saudáveis, o Control Plane do Kubernetes monitora os Pods o "
        "tempo todo através de sondas (livenessProbe para saber se o container travou e readinessProbe para saber se ele já pode "
        "receber clientes), distribuindo o tráfego de rede automaticamente através dos objetos Service."
    )

    p2.subsection("3.2 CI/CD em Ambientes Distribuídos")
    p2.paragraph(
        "Em uma arquitetura distribuída, fazer deploy manual copiando arquivos para o servidor é receita certa para erros. Por isso "
        "adotamos CI/CD (Integração Contínua e Entrega Contínua). Na etapa de CI, cada alteração enviada ao repositório dispara "
        "automaticamente a validação de sintaxe (lint), os testes automatizados de cada microsserviço, a construção da imagem Docker "
        "e a checagem de segurança (scan de vulnerabilidades). Se tudo passar nos 'gates' de qualidade, a etapa de CD publica a "
        "imagem versionada no Registry e atualiza o cluster Kubernetes de forma controlada."
    )

    p2.subsection("3.3 Os Três Pilares da Observabilidade (Métricas, Logs e Traces)")
    p2.paragraph(
        "Monitorar apenas se o servidor está ligado não basta em microsserviços. A observabilidade nos permite entender o que "
        "acontece dentro do sistema através de três pilares que trabalham juntos:"
    )
    p2.bullet(
        "1. Métricas (Prometheus & Grafana):",
        "São valores numéricos agregados ao longo do tempo, como uso de CPU, quantidade de pedidos por segundo e taxa de erros HTTP 5xx (os chamados Golden Signals). Elas respondem rapidamente 'que' algo está fora do normal.",
    )
    p2.bullet(
        "2. Logs Estruturados (JSON no stdout):",
        "São os registros detalhados de cada evento que aconteceu no código (ex: 'Estoque insuficiente para o SKU X'). Seguindo o 12-Factor App, os containers jogam os logs na saída padrão em formato JSON para facilitar a busca.",
    )
    p2.bullet(
        "3. Tracing Distribuído (OpenTelemetry & Jaeger):",
        "É o pilar que resolve a maior dor da Loja Veloz. Quando o cliente clica em comprar, o API Gateway cria um código único (traceId) e o repassa nos cabeçalhos HTTP para Pedidos, Estoque e Pagamentos. Assim conseguimos ver uma linha do tempo completa (spans) mostrando exatamente quantos milissegundos cada microsserviço gastou.",
    )

    p2.section("4. Pesquisa de Caso Concreto e Comparativo de Deploy")
    p2.callout_box(
        "Caso de Referência Pesquisado: Google Cloud 'Online Boutique' (microservices-demo) & 12-Factor App",
        "Para desenhar a solução da Loja Veloz, pesquisei o repositório oficial de referência 'Online Boutique' (GoogleCloudPlatform/microservices-demo), que é uma loja virtual cloud-native completa em microsserviços rodando no Kubernetes. Assim como no case do Google, adotei um API Gateway na borda, microsserviços desacoplados sem estado (stateless), sondas de saúde nativas, instrumentação com OpenTelemetry/Jaeger e manifestos declarativos com HPA. Também apliquei os princípios da metodologia 12-Factor App (fator III - configurações em variáveis de ambiente via ConfigMap/Secret; fator VI - processos stateless; e fator XI - logs como fluxos de eventos).",
    )

    p2.subsection("4.1 Comparação entre Estratégias de Deploy em Produção")
    p2.table(
        ["Estratégia", "Como Funciona na Prática", "Custo de Infra", "Uso na Loja Veloz"],
        [
            ["Rolling Update", "Substitui os Pods antigos pelos novos aos poucos (maxUnavailable: 0).", "Baixo (apenas +1 Pod extra durante a troca).", "Padrão adotado em todos os microsserviços no MVP."],
            ["Blue-Green", "Sobe um ambiente inteiro duplicado (Verde) e vira a chave do roteador.", "Alto (exige o dobro de servidores ativos).", "Descartado no MVP pelo custo elevado de manter 2 ambientes."],
            ["Canary Release", "Libera a versão nova para apenas 5% a 10% dos clientes inicialmente.", "Baixo (controlado via Ingress ou Service Mesh).", "Recomendado para mudanças críticas no pagamentos-service."],
        ],
        [240, 480, 270, 308],
    )
    pages.append(p2.img)

    # ---------------- PÁGINA 3 ----------------
    p3 = PageBuilder(hdr_title, hdr_sub, start_page + 2, total_pages)
    p3.section("5. Justificativa das Decisões Arquiteturais Adotadas no Projeto")
    p3.paragraph(
        "Todas as escolhas técnicas feitas para o MVP da Loja Veloz buscaram equilibrar simplicidade de manutenção (já que o prazo "
        "é de 4 semanas até a campanha promocional) com segurança e confiabilidade de nível de produção:"
    )

    p3.bullet(
        "Padronização Local com Docker Compose:",
        "Escolhi o Docker Compose para o ambiente de desenvolvimento porque ele permite subir os 4 microsserviços, o PostgreSQL, o Redis e toda a pilha de observabilidade (Jaeger, Prometheus e Grafana) com um único comando (docker compose up -d --build). Isso elimina as diferenças de configuração entre as máquinas dos desenvolvedores.",
    )
    p3.bullet(
        "Imagens Multi-Stage e Usuário Não-Root:",
        "Nos Dockerfiles, utilizei multi-stage build com a imagem base enxuta node:20-alpine3.19. O primeiro estágio roda os testes e valida o código; o segundo copia apenas o código de produção e executa com um usuário sem privilégios (UID 10001). Isso reduz o tamanho da imagem e impede que um invasor ganhe acesso root no servidor.",
    )
    p3.bullet(
        "Mensageria Assíncrona (Evento PedidoCriado):",
        "Optei por incluir o Redis junto ao padrão Outbox para publicar o evento 'PedidoCriado' assim que o pedido é pago. Isso desacopla o fluxo principal de ações secundárias (como envio de nota fiscal ou e-mail), deixando a resposta de compra muito mais rápida para o cliente.",
    )
    p3.bullet(
        "Estratégia de Deploy RollingUpdate (Zero-Downtime):",
        "Entre Rolling Update, Blue-Green e Canary, escolhi o RollingUpdate configurado com maxUnavailable: 0 e maxSurge: 1 como padrão do MVP. Ele cria primeiro o Pod novo, aguarda a readinessProbe confirmar que o serviço está pronto e só então desliga o Pod antigo. Assim eliminamos as quedas durante deploys sem precisar dobrar o custo de infraestrutura como no Blue-Green.",
    )
    p3.bullet(
        "Escalabilidade com HPA (em vez de VPA isolado):",
        "Como os nossos microsserviços foram construídos de forma stateless (sem guardar sessão na memória local), o Horizontal Pod Autoscaler (HPA) é a escolha ideal para o pico da campanha promocional: quando a CPU passa de 70%, o Kubernetes cria novas réplicas em segundos. O VPA precisaria reiniciar os Pods para alterar memória/CPU, o que atrapalharia durante um pico de acessos.",
    )
    p3.bullet(
        "Infraestrutura como Código (IaC) com Terraform:",
        "Para garantir que o ambiente de nuvem (VPC isolada, cluster Kubernetes EKS e banco RDS PostgreSQL Multi-AZ) possa ser recriado de forma idêntica e auditável, estruturei os arquivos do Terraform parametrizados por variáveis.",
    )

    p3.table(
        ["Camada / Requisito", "Tecnologia Escolhida", "Benefício Direto para a Campanha da Loja Veloz"],
        [
            ["Ambiente Local", "Docker Compose + .env (12-Factor)", "Time inteiro sobe os 9 containers do sistema com um único comando."],
            ["Orquestração & Escala", "Kubernetes + HPA v2 (CPU 70% / RAM 80%)", "Escala de 3 para 12 réplicas em segundos durante picos de tráfego."],
            ["Segurança (DevSecOps)", "Alpine Multi-Stage + PSA Restricted + Trivy", "Containers sem root (UID 10001) e imagens bloqueadas se houver CVEs."],
            ["Observabilidade", "OpenTelemetry + Jaeger + Prometheus", "Rastreio exato de falhas entre serviços usando o mesmo traceId."],
        ],
        [280, 420, 598],
    )

    p3.section("6. Referências Bibliográficas (Fontes Primárias)")
    refs = [
        "1. KUBERNETES OFFICIAL DOCUMENTATION. Concepts: Workloads (Pods, Deployments), Services, ConfigMaps, Secrets, Pod Security Admission & Horizontal Pod Autoscaling. Disponível em: https://kubernetes.io/docs/home/",
        "2. DOCKER OFFICIAL DOCUMENTATION. Multi-stage builds, Dockerfile best practices & Docker Compose specification. Disponível em: https://docs.docker.com/",
        "3. WIGGINS, Adam. The Twelve-Factor App (Metodologia Cloud-Native: Config, Stateless Processes, Disposability, Logs). Disponível em: https://12factor.net/pt_br/",
        "4. GOOGLE CLOUD PLATFORM. Online Boutique (microservices-demo): Cloud-first microservices reference architecture on Kubernetes with OpenTelemetry. Disponível em: https://github.com/GoogleCloudPlatform/microservices-demo",
        "5. OPENTELEMETRY & JAEGER DOCUMENTATION. Context Propagation (W3C Trace Context) and Distributed Tracing. Disponível em: https://opentelemetry.io/docs/",
        "6. HASHICORP TERRAFORM DOCUMENTATION. Infrastructure as Code (IaC), Providers, Modules and State Management. Disponível em: https://developer.hashicorp.com/terraform/docs",
    ]
    for r in refs:
        p3.paragraph(r, font_size=16, line_spacing=23, color=(51, 65, 85))

    pages.append(p3.img)
    return pages


# ============================================================================
# CONSTRUÇÃO DA PARTE PRÁTICA (Exatas 5 Páginas - Mín 3 | Máx 6)
# ============================================================================
def build_parte_pratica(total_pages=5, start_page=1):
    pages = []
    hdr_title = "RELATÓRIO TÉCNICO — PARTE PRÁTICA (IMPLEMENTAÇÃO & PRINTS)"
    hdr_sub = "Repositório: Plataforma Pedidos Veloz"

    # ---------------- PÁGINA 1 ----------------
    p1 = PageBuilder(hdr_title, hdr_sub, start_page, total_pages)
    p1.title_banner(
        "IMPLEMENTAÇÃO PRÁTICA: PLATAFORMA 'PEDIDOS VELOZ'",
        "Parte Prática: Docker Compose, Imagens Seguras, Kubernetes, CI/CD, Observabilidade e IaC",
        "Entregável Prático com Evidências de Execução  |  Repositório Completo Verificado",
    )

    p1.section("1. Visão Geral do Repositório e Ambiente Local com Docker Compose")
    p1.paragraph(
        "Para resolver a bagunça do ambiente de desenvolvimento da Loja Veloz, organizei o repositório dividindo cada microsserviço "
        "em sua própria pasta dentro de services/ (api-gateway, pedidos-service, pagamentos-service e estoque-service), além das "
        "pastas db/, k8s/, observability/, terraform/ e .github/workflows/. Na raiz do projeto, o arquivo docker-compose.yml "
        "permite que qualquer pessoa do time suba a plataforma inteira digitando apenas um comando no terminal."
    )
    p1.bullet(
        "Isolamento de Redes e Volumes:",
        "Criei duas redes bridge no Compose: pedidos-veloz-frontend (onde fica o API Gateway e os painéis visuais) e pedidos-veloz-backend (rede interna onde ficam os microsserviços de negócio, o PostgreSQL e o Redis). Também configurei volumes nomeados (pgdata, prometheus_data e grafana_data) para não perder os dados do banco ao reiniciar os containers.",
    )
    p1.bullet(
        "Ordem de Inicialização Segura (Healthchecks):",
        "O serviço de pedidos e o de estoque utilizam depends_on com a condição service_healthy no PostgreSQL e no Redis. Assim, a aplicação só conecta depois que o banco já rodou o script db/init.sql e criou as tabelas e os produtos iniciais.",
    )

    p1.embed_screenshot(
        "01-docker-compose-up.png",
        "Figura 1 — Execução do comando 'docker compose up -d --build' e verificação dos containers saudáveis (healthy) com 'docker compose ps'.",
        max_h=560,
    )

    p1.callout_box(
        "Configuração por Variáveis de Ambiente (.env.example — 12-Factor App)",
        "Nenhuma senha ou endereço de servidor ficou fixo (hardcoded) dentro do código Node.js. Todos os serviços leem portas, URLs de integração e credenciais através de variáveis de ambiente (como PEDIDOS_SERVICE_URL, POSTGRES_PASSWORD e OTEL_EXPORTER_OTLP_ENDPOINT), permitindo usar exatamente a mesma imagem tanto no Docker Compose quanto no Kubernetes.",
    )
    pages.append(p1.img)

    # ---------------- PÁGINA 2 ----------------
    p2 = PageBuilder(hdr_title, hdr_sub, start_page + 1, total_pages)
    p2.section("2. Conteinerização Padronizada, Versionamento e Testes")
    p2.paragraph(
        "Cada um dos quatro microsserviços possui um Dockerfile estruturado com Multi-Stage Build sobre a imagem oficial "
        "node:20-alpine3.19. No estágio 'builder', copiamos os arquivos de código e de teste e rodamos 'npm run lint && npm test'. "
        "Se algum teste falhar, o build da imagem já é interrompido na hora. No estágio 'production', copiamos apenas a pasta src/ "
        "(deixando os arquivos de teste de fora para reduzir a superfície de ataque) e criamos o usuário sem privilégios 'appuser' "
        "(UID/GID 10001). O versionamento combina SemVer (:1.2.0) com o hash curto do commit Git (:sha-8f4d2a1), facilitando o rollback."
    )

    p2.embed_screenshot(
        "02-testes-e-logs-json.png",
        "Figura 2 — Execução real da suíte de 10 testes automatizados (unitários e E2E), emissão de logs JSON e validação dos 11 arquivos YAML.",
        max_h=480,
    )

    p2.section("3. Plataforma 'Pedidos Veloz' Funcionando Ponta a Ponta")
    p2.paragraph(
        "Para demonstrar o sistema funcionando na prática, executei o fluxo completo de criação de pedidos passando pelo API Gateway "
        "(porta 8080). Ao receber um POST em /api/pedidos, o Gateway gera o identificador de rastreio (traceId) e chama o "
        "pedidos-service (:3001), que primeiro reserva os itens no estoque-service (:3003), em seguida processa a cobrança no "
        "pagamentos-service (:3002) e, por fim, grava o pedido e publica o evento 'PedidoCriado'."
    )

    p2.embed_screenshot(
        "03-dashboard-pedidos-veloz.png",
        "Figura 3 — Console Operacional da Loja Veloz no API Gateway (http://localhost:8080) exibindo pedidos pagos, baixa de estoque e traces.",
        max_h=520,
    )
    pages.append(p2.img)

    # ---------------- PÁGINA 3 ----------------
    p3 = PageBuilder(hdr_title, hdr_sub, start_page + 2, total_pages)
    p3.section("4. Kubernetes em Produção Mínima (Manifests, Probes e Segurança)")
    p3.paragraph(
        "Na pasta k8s/, organizei os manifestos numerados de 00 a 06 para refletir a ordem de aplicação no cluster de produção. "
        "Abaixo estão as principais configurações implementadas para garantir estabilidade e segurança:"
    )
    p3.bullet(
        "Namespace com Pod Security Admission (00-namespace.yaml):",
        "O namespace 'pedidos-veloz' aplica o rótulo nativo pod-security.kubernetes.io/enforce: restricted, impedindo que qualquer container suba como root ou peça privilégios de administrador no nó.",
    )
    p3.bullet(
        "Desacoplamento com ConfigMap e Secret (01 e 02):",
        "As URLs internas do cluster (ex: http://estoque-service.pedidos-veloz.svc.cluster.local:3003) ficam no ConfigMap, enquanto a senha do PostgreSQL e a chave da API de pagamentos ficam isoladas no objeto Secret.",
    )
    p3.bullet(
        "Deployments com Probes e SecurityContext (03-deployments.yaml):",
        "Todos os Deployments definem readinessProbe (GET /ready) e livenessProbe (GET /health), limites de CPU/Memória, além de securityContext com runAsNonRoot: true, runAsUser: 10001, readOnlyRootFilesystem: true e drop: ['ALL'].",
    )
    p3.bullet(
        "Services, Ingress e NetworkPolicy Zero-Trust (04 e 06):",
        "Os serviços internos usam tipo ClusterIP (inacessíveis de fora do cluster) e apenas o api-gateway é exposto via Ingress. Além disso, a NetworkPolicy garante que somente o pedidos-service e o gateway possam abrir conexão com estoque e pagamentos.",
    )

    p3.embed_screenshot(
        "05-kubernetes-hpa-rollout.png",
        "Figura 4 — Aplicação dos manifestos Kubernetes, verificação dos Pods rodando como não-root (UID 10001), HPA ativo e Rollout sem downtime.",
        max_h=530,
    )

    p3.callout_box(
        "Por que as Probes evitam indisponibilidade durante o Deploy?",
        "Antes desta modernização, a Loja Veloz sofria com erros 502 durante atualizações porque o balanceador mandava clientes para containers que ainda estavam carregando. Com a readinessProbe apontando para /ready e a estratégia RollingUpdate (maxUnavailable: 0, maxSurge: 1), o Kubernetes só envia tráfego para o Pod novo quando ele responde 200 OK.",
    )
    pages.append(p3.img)

    # ---------------- PÁGINA 4 ----------------
    p4 = PageBuilder(hdr_title, hdr_sub, start_page + 3, total_pages)
    p4.section("5. Pipeline de CI/CD Automatizado no GitHub Actions")
    p4.paragraph(
        "Para automatizar a entrega do código até a produção, criei o pipeline .github/workflows/ci-cd.yaml no GitHub Actions. "
        "Ele foi estruturado em quatro estágios sequenciais (jobs dependentes via 'needs'), funcionando como portões de qualidade "
        "(quality gates) que travam o deploy caso qualquer verificação falhe:"
    )
    p4.bullet(
        "Estágio 1 — Lint, K8s Schema & Terraform Validate:",
        "Verifica a sintaxe dos 4 microsserviços (npm run lint), valida se todos os manifestos da pasta k8s/ estão em conformidade com a API oficial do Kubernetes usando Kubeconform e roda 'terraform fmt -check' e 'terraform validate' na infraestrutura.",
    )
    p4.bullet(
        "Estágio 2 — Testes Automatizados (Unitários + E2E):",
        "Executa toda a bateria de testes de reserva de estoque, aprovação/recusa de pagamento antifraude, criação de pedidos e propagação do traceId pelo API Gateway.",
    )
    p4.bullet(
        "Estágio 3 — Build Multi-Stage, Scan Trivy & Publicação no Registry:",
        "Usa matriz paralela para construir as imagens dos 4 microsserviços, aplica duas tags (:1.2.0 e :sha-commit), executa o scanner Aqua Trivy (configurado com exit-code: 1 para bloquear vulnerabilidades CRITICAL ou HIGH) e faz push para o GitHub Container Registry (ghcr.io) autenticando via secrets.GITHUB_TOKEN.",
    )
    p4.bullet(
        "Estágio 4 — Deploy Contínuo (CD) no Kubernetes:",
        "Disparado apenas na branch main após aprovação dos estágios anteriores. Autentica no cluster usando o segredo secrets.KUBE_CONFIG, aplica os manifestos atualizados, troca a tag da imagem e monitora o 'kubectl rollout status' até concluir.",
    )

    p4.embed_screenshot(
        "06-cicd-pipeline-github.png",
        "Figura 5 — Execução do pipeline CI/CD no GitHub Actions com os 4 jobs aprovados, scan Trivy sem CVEs críticos e deploy concluído.",
        max_h=500,
    )

    p4.table(
        ["Segredo Utilizado no Pipeline", "Onde é Configurado", "Finalidade Prática na Automação"],
        [
            ["secrets.GITHUB_TOKEN", "GitHub Actions Token Nativo", "Autenticar no GitHub Container Registry (ghcr.io) e publicar as imagens Docker versionadas."],
            ["secrets.KUBE_CONFIG", "GitHub Environment Secrets", "Conectar de forma criptografada ao cluster Kubernetes de produção para executar o rollout."],
            ["pedidos-veloz-secrets", "Kubernetes Secret / Vault", "Injetar POSTGRES_PASSWORD e PAYMENT_PROVIDER_API_KEY dentro dos Pods em execução."],
        ],
        [330, 340, 628],
    )
    pages.append(p4.img)

    # ---------------- PÁGINA 5 ----------------
    p5 = PageBuilder(hdr_title, hdr_sub, start_page + 4, total_pages)
    p5.section("6. Observabilidade na Prática: Métricas, Logs e Tracing Distribuído")
    p5.paragraph(
        "Na pasta observability/, configurei o Prometheus (prometheus.yml) para coletar a rota /metrics dos 4 microsserviços a cada "
        "15 segundos e o OpenTelemetry Collector (otel-collector-config.yaml) para receber os traces via protocolo OTLP e enviá-los "
        "ao Jaeger. Todos os microsserviços propagam os cabeçalhos HTTP 'x-trace-id' e 'traceparent' (padrão W3C). Dessa forma, "
        "quando um pedido é criado, conseguimos inspecionar no Jaeger a cascata completa de spans e cruzar o mesmo traceId nos logs JSON."
    )

    p5.embed_screenshot(
        "04-jaeger-distributed-tracing.png",
        "Figura 6 — Visualização do Trace Distribuído no Jaeger UI (5 spans atravessando 4 serviços em 19.34 ms) e métricas no Prometheus.",
        max_h=480,
    )

    p5.section("7. Estratégia de Deploy, Escalabilidade (HPA) e IaC com Terraform")
    p5.paragraph(
        "Para fechar a solução fim a fim, definimos como a plataforma se comporta durante o pico da campanha promocional e como "
        "toda a infraestrutura de nuvem é provisionada:"
    )
    p5.bullet(
        "Deploy RollingUpdate + Evolução para Canary:",
        "Nos Deployments (03-deployments.yaml), configuramos RollingUpdate com maxUnavailable: 0 e maxSurge: 1 para garantir zero-downtime imediato no MVP. Para atualizações futuras de alto risco na regra de cobrança do pagamentos-service, a arquitetura já suporta deploy Canary via Ingress/Service Mesh direcionando 10% do tráfego inicialmente.",
    )
    p5.bullet(
        "Escalabilidade Horizontal com HPA v2 (05-hpa.yaml):",
        "O pedidos-service escala automaticamente de 3 até 12 réplicas (e o api-gateway de 2 até 10 réplicas) quando o uso médio de CPU atinge 70% ou memória atinge 80%. Configuramos uma janela de estabilização (stabilizationWindowSeconds: 300) no scaleDown para evitar que os Pods sejam desligados cedo demais entre ondas de acesso da promoção.",
    )
    p5.bullet(
        "Infraestrutura como Código com Terraform (pasta terraform/):",
        "Criamos os arquivos providers.tf, variables.tf, main.tf e outputs.tf que provisionam de forma reproduzível a VPC isolada (10.20.0.0/16) com sub-redes privadas em múltiplas zonas de disponibilidade, o cluster Kubernetes gerenciado (Amazon EKS 1.30) e a instância do banco de dados Amazon RDS PostgreSQL 16 Multi-AZ com armazenamento criptografado.",
    )

    p5.callout_box(
        "Conclusão dos Resultados Alcançados para a Loja Veloz",
        "Com a implementação entregue neste repositório, a Loja Veloz passa a contar com ambiente local de 1 comando no Docker Compose, imagens Alpine seguras rodando sem root, pipeline CI/CD com testes e scan Trivy, deploy sem quedas no Kubernetes com auto-scaling (HPA) e rastreabilidade total via OpenTelemetry, Jaeger e Prometheus.",
    )
    pages.append(p5.img)
    return pages


def save_pdf(pages, output_path):
    first, rest = pages[0], pages[1:]
    first.save(
        output_path,
        "PDF",
        resolution=180.0,
        save_all=True,
        append_images=rest,
    )
    print(f"PDF gerado ({len(pages)} páginas): {output_path}")


if __name__ == "__main__":
    pgs_teorica = build_parte_teorica(total_pages=3, start_page=1)
    save_pdf(pgs_teorica, os.path.join(ROOT_DIR, "Relatorio_Parte_Teorica.pdf"))
    save_pdf(pgs_teorica, os.path.join(DOCS_DIR, "Relatorio_Parte_Teorica.pdf"))

    pgs_pratica = build_parte_pratica(total_pages=5, start_page=1)
    save_pdf(pgs_pratica, os.path.join(ROOT_DIR, "Relatorio_Parte_Pratica.pdf"))
    save_pdf(pgs_pratica, os.path.join(DOCS_DIR, "Relatorio_Parte_Pratica.pdf"))

    # Versão unificada (8 páginas numeradas de 1 a 8)
    pgs_unificada = build_parte_teorica(total_pages=8, start_page=1) + build_parte_pratica(total_pages=8, start_page=4)
    save_pdf(pgs_unificada, os.path.join(ROOT_DIR, "Relatorio_Completo_Loja_Veloz.pdf"))
    save_pdf(pgs_unificada, os.path.join(DOCS_DIR, "Relatorio_Completo_Loja_Veloz.pdf"))

    # Salva também pré-visualizações PNG de páginas para inspeção visual
    preview_dir = os.path.join(ROOT_DIR, "docs", "previews")
    os.makedirs(preview_dir, exist_ok=True)
    for i, im in enumerate(pgs_teorica, 1):
        im.save(os.path.join(preview_dir, f"teorica_p{i}.png"))
    for i, im in enumerate(pgs_pratica, 1):
        im.save(os.path.join(preview_dir, f"pratica_p{i}.png"))
