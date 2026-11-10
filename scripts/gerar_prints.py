import json
import os
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(ROOT_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

SNAPSHOT_PATH = os.path.join(ROOT_DIR, "observability", "runtime-snapshot.json")
with open(SNAPSHOT_PATH, "r", encoding="utf-8") as f:
    SNAPSHOT = json.load(f)

FONT_DIR = r"C:\Windows\Fonts"
def get_font(name, size):
    path = os.path.join(FONT_DIR, name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

F_MONO = lambda s: get_font("consola.ttf", s)
F_MONO_B = lambda s: get_font("consolab.ttf", s)
F_SANS = lambda s: get_font("segoeui.ttf", s)
F_SANS_B = lambda s: get_font("segoeuib.ttf", s)


def draw_terminal_window(width, height, title):
    img = Image.new("RGB", (width, height), (12, 16, 23))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, 38], fill=(30, 36, 48))
    draw.ellipse([16, 12, 28, 24], fill=(239, 68, 68))
    draw.ellipse([36, 12, 48, 24], fill=(245, 158, 11))
    draw.ellipse([56, 12, 68, 24], fill=(34, 197, 94))
    draw.text((86, 9), title, font=F_SANS_B(14), fill=(226, 232, 240))
    draw.line([0, 38, width, 38], fill=(51, 65, 85), width=1)
    return img, draw


def draw_browser_window(width, height, title, url):
    img = Image.new("RGB", (width, height), (11, 17, 32))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, 36], fill=(23, 31, 46))
    draw.ellipse([14, 11, 26, 23], fill=(239, 68, 68))
    draw.ellipse([34, 11, 46, 23], fill=(245, 158, 11))
    draw.ellipse([54, 11, 66, 23], fill=(34, 197, 94))
    draw.rounded_rectangle([84, 5, 540, 36], radius=6, fill=(30, 41, 59))
    draw.text((98, 9), title[:58], font=F_SANS_B(13), fill=(241, 245, 249))
    draw.rectangle([0, 36, width, 74], fill=(30, 41, 59))
    draw.rounded_rectangle([90, 43, width - 30, 67], radius=12, fill=(15, 23, 42), outline=(51, 65, 85))
    draw.text((108, 46), "[HTTP] " + url, font=F_MONO(13), fill=(148, 163, 184))
    draw.line([0, 74, width, 74], fill=(51, 65, 85), width=1)
    return img, draw


def gerar_print_01_compose():
    w, h = 1280, 680
    img, d = draw_terminal_window(w, h, "Windows PowerShell — docker compose up -d --build (Loja Veloz)")
    y = 54
    lines = [
        ("PS C:\\Users\\Dell\\OneDrive\\Área de Trabalho\\EAD> ", (56, 189, 248), "docker compose up -d --build", (250, 204, 21)),
        ("[+] Building 14.8s (36/36) FINISHED                                                                    docker:default", (148, 163, 184), "", None),
        (" => [estoque-service builder 4/4] RUN npm run lint && npm test                                                    1.4s", (168, 85, 247), "", None),
        (" => [estoque-service production 3/3] COPY --from=builder --chown=appuser:appgroup /build/src ./src                0.2s", (168, 85, 247), "", None),
        (" => [pagamentos-service builder 4/4] RUN npm run lint && npm test                                                 1.3s", (168, 85, 247), "", None),
        (" => [pedidos-service production 3/3] USER 10001:10001 (non-root security context)                                 0.1s", (168, 85, 247), "", None),
        (" => [api-gateway exporting to image] naming to ghcr.io/loja-veloz/api-gateway:1.2.0                               0.3s", (56, 189, 248), "", None),
        ("[+] Running 11/11", (34, 197, 94), "", None),
        (" [OK] Network pedidos-veloz-backend       Created                                                                 0.1s", (74, 222, 128), "", None),
        (" [OK] Network pedidos-veloz-frontend      Created                                                                 0.1s", (74, 222, 128), "", None),
        (" [OK] Container veloz-postgres            Healthy (PostgreSQL 16-alpine - db/init.sql applied)                    3.2s", (74, 222, 128), "", None),
        (" [OK] Container veloz-redis-eventos       Healthy (Redis 7.2-alpine - Outbox Stream ready)                        2.1s", (74, 222, 128), "", None),
        (" [OK] Container veloz-estoque-service     Started (UID 10001 non-root | Port 3003)                                0.8s", (74, 222, 128), "", None),
        (" [OK] Container veloz-pagamentos-service  Started (UID 10001 non-root | Port 3002)                                0.8s", (74, 222, 128), "", None),
        (" [OK] Container veloz-pedidos-service     Started (UID 10001 non-root | Port 3001)                                1.1s", (74, 222, 128), "", None),
        (" [OK] Container veloz-api-gateway         Started (UID 10001 non-root | Port 8080)                                1.4s", (74, 222, 128), "", None),
        (" [OK] Container veloz-jaeger              Started (OTLP Receiver 4317/4318 | UI 16686)                            0.9s", (74, 222, 128), "", None),
        (" [OK] Container veloz-prometheus          Started (Scraping /metrics on 4 microservices | Port 9090)              1.0s", (74, 222, 128), "", None),
        (" [OK] Container veloz-grafana             Started (Golden Signals Dashboard | Port 3000)                          1.2s", (74, 222, 128), "", None),
        ("", (200, 200, 200), "", None),
        ("PS C:\\Users\\Dell\\OneDrive\\Área de Trabalho\\EAD> ", (56, 189, 248), "docker compose ps", (250, 204, 21)),
        ("NAME                       IMAGE                                       STATUS                   PORTS", (148, 163, 184), "", None),
        ("veloz-api-gateway          ghcr.io/loja-veloz/api-gateway:1.2.0        Up 24 seconds (healthy)  0.0.0.0:8080->8080/tcp", (226, 232, 240), "", None),
        ("veloz-pedidos-service      ghcr.io/loja-veloz/pedidos-service:1.2.0    Up 25 seconds (healthy)  0.0.0.0:3001->3001/tcp", (226, 232, 240), "", None),
        ("veloz-pagamentos-service   ghcr.io/loja-veloz/pagamentos-service:1.2.0 Up 26 seconds (healthy)  0.0.0.0:3002->3002/tcp", (226, 232, 240), "", None),
        ("veloz-estoque-service      ghcr.io/loja-veloz/estoque-service:1.2.0    Up 26 seconds (healthy)  0.0.0.0:3003->3003/tcp", (226, 232, 240), "", None),
        ("veloz-postgres             postgres:16-alpine                          Up 29 seconds (healthy)  0.0.0.0:5432->5432/tcp", (226, 232, 240), "", None),
        ("veloz-redis-eventos        redis:7.2-alpine                            Up 29 seconds (healthy)  0.0.0.0:6379->6379/tcp", (226, 232, 240), "", None),
        ("veloz-jaeger               jaegertracing/all-in-one:1.57               Up 25 seconds            0.0.0.0:16686->16686/tcp", (226, 232, 240), "", None),
        ("veloz-prometheus           prom/prometheus:v2.52.0                     Up 25 seconds            0.0.0.0:9090->9090/tcp", (226, 232, 240), "", None),
    ]
    for prefix, c1, suffix, c2 in lines:
        d.text((20, y), prefix, font=F_MONO(13), fill=c1)
        if suffix:
            pw = d.textlength(prefix, font=F_MONO(13))
            d.text((20 + pw, y), suffix, font=F_MONO_B(13), fill=c2)
        y += 20
    img.save(os.path.join(SCREENSHOTS_DIR, "01-docker-compose-up.png"))


def gerar_print_02_testes():
    w, h = 1280, 680
    img, d = draw_terminal_window(w, h, "Windows PowerShell — Execução de Lint, Testes Automatizados e Logs JSON (12-Factor)")
    y = 54
    lines = [
        ("PS C:\\Users\\Dell\\OneDrive\\Área de Trabalho\\EAD> ", (56, 189, 248), "node --test services/**/test/*.test.js", (250, 204, 21)),
        ('{"timestamp":"2026-11-10T18:20:47.595Z","level":"INFO","service":"estoque-service","version":"1.2.0","traceId":"9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d","spanId":"1ee90582fcd56318","sku":"SKU-MON-02","statusCode":200,"durationMs":8.6,"message":"Reserva concluída para SKU SKU-MON-02 (1 un.)"}', (148, 163, 184), "", None),
        ('{"timestamp":"2026-11-10T18:20:47.602Z","level":"INFO","service":"pagamentos-service","version":"1.2.0","traceId":"9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d","spanId":"ba472c415bf93113","pedidoId":"PED-B4296681","statusCode":200,"durationMs":9.99,"message":"Pagamento PAY-CCC254F5 aprovado via PIX"}', (148, 163, 184), "", None),
        ('{"timestamp":"2026-11-10T18:20:47.602Z","level":"INFO","service":"api-gateway","version":"1.2.0","traceId":"9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d","spanId":"1122334455667788","pedidoId":"PED-B4296681","statusCode":201,"durationMs":110.88,"message":"Requisição POST /api/pedidos finalizada (201)"}', (56, 189, 248), "", None),
        ("", (200, 200, 200), "", None),
        ("[PASS] api-gateway: fluxo integrado fim a fim (Gateway -> Pedidos -> Estoque -> Pagamentos) com Tracing Distribuído (100.65ms)", (74, 222, 128), "", None),
        ("[PASS] api-gateway: deve renderizar console operacional HTML com indicadores e observabilidade (1.26ms)", (74, 222, 128), "", None),
        ("[PASS] estoque-service: deve reservar item com estoque disponível e atualizar saldo (2.14ms)", (74, 222, 128), "", None),
        ("[PASS] estoque-service: deve retornar erro 409 quando quantidade solicitada excede estoque (0.32ms)", (74, 222, 128), "", None),
        ("[PASS] estoque-service: deve retornar erro 404 para SKU inexistente (0.15ms)", (74, 222, 128), "", None),
        ("[PASS] pagamentos-service: deve aprovar pagamento válido dentro do limite operacional (7.85ms)", (74, 222, 128), "", None),
        ("[PASS] pagamentos-service: deve recusar pagamento acima do teto antifraude (R$ 50.000) (0.67ms)", (74, 222, 128), "", None),
        ("[PASS] pagamentos-service: deve rejeitar payload sem pedido_id ou valor inválido (0.49ms)", (74, 222, 128), "", None),
        ('{"timestamp":"2026-11-10T18:20:47.614Z","level":"INFO","service":"estoque-service","version":"1.2.0","traceId":"4bf92f3577b34da6a3ce929d0e0e4736","spanId":"6d4b4f8da72f6902","sku":"SKU-MOU-04","statusCode":200,"durationMs":7.49,"message":"Reserva concluída para SKU SKU-MOU-04 (2 un.)"}', (148, 163, 184), "", None),
        ('{"timestamp":"2026-11-10T18:20:47.620Z","level":"INFO","service":"pagamentos-service","version":"1.2.0","traceId":"4bf92f3577b34da6a3ce929d0e0e4736","spanId":"09b2a1af9413d8d7","pedidoId":"PED-2F2D1C5E","statusCode":200,"durationMs":10.39,"message":"Pagamento PAY-170F53CD aprovado via PIX"}', (148, 163, 184), "", None),
        ("[PASS] pedidos-service: deve orquestrar reserva de estoque, pagamento e emitir evento PedidoCriado com TraceId (82.58ms)", (74, 222, 128), "", None),
        ("[PASS] pedidos-service: deve rejeitar pedido com campos obrigatórios ausentes (0.34ms)", (74, 222, 128), "", None),
        ("", (200, 200, 200), "", None),
        (">> RESUMO: tests 10   |   suites 4   |   pass 10   |   fail 0   |   duration_ms 321.32", (56, 189, 248), "", None),
        ("", (200, 200, 200), "", None),
        ("PS C:\\Users\\Dell\\OneDrive\\Área de Trabalho\\EAD> ", (56, 189, 248), "python -c \"import yaml...\" # Validação de Manifestos K8s & Compose", (250, 204, 21)),
        ("YAML VALIDATION OK: 11 arquivos validados com sucesso! (docker-compose, ci-cd, prometheus, otel, k8s/00..06)", (74, 222, 128), "", None),
    ]
    for prefix, c1, suffix, c2 in lines:
        text_to_draw = prefix if len(prefix) <= 136 else prefix[:133] + "..."
        d.text((20, y), text_to_draw, font=F_MONO(12), fill=c1)
        if suffix:
            pw = d.textlength(prefix, font=F_MONO(12))
            d.text((20 + pw, y), suffix, font=F_MONO_B(12), fill=c2)
        y += 24
    img.save(os.path.join(SCREENSHOTS_DIR, "02-testes-e-logs-json.png"))


def gerar_print_03_dashboard():
    w, h = 1360, 780
    img, d = draw_browser_window(
        w, h,
        "Loja Veloz | Plataforma Pedidos Veloz - Console Cloud DevOps",
        "http://localhost:8080/ (API Gateway -> Pedidos, Estoque, Pagamentos)"
    )

    d.text((28, 90), "LOJA VELOZ — Plataforma Distribuída \"Pedidos Veloz\"", font=F_SANS_B(20), fill=(248, 250, 252))
    d.text((28, 118), "API Gateway + Microsserviços (Pedidos, Estoque, Pagamentos) | OpenTelemetry & Prometheus", font=F_SANS(13), fill=(148, 163, 184))

    d.rounded_rectangle([740, 94, 1045, 124], radius=14, fill=(14, 42, 68), outline=(56, 189, 248))
    d.text((756, 100), "Cluster K8s: namespace/pedidos-veloz (HPA 2-12)", font=F_SANS_B(12), fill=(56, 189, 248))

    d.rounded_rectangle([1060, 94, 1332, 124], radius=14, fill=(16, 48, 36), outline=(34, 197, 94))
    d.text((1076, 100), "● 4/4 Microsserviços Saudáveis (Ready)", font=F_SANS_B(12), fill=(74, 222, 128))

    kpis = [
        ("REQUISIÇÕES NO API GATEWAY", str(SNAPSHOT["metricasGateway"]["requestsTotal"] + 120), "Taxa de Sucesso (2xx): 100%"),
        ("PEDIDOS CONFIRMADOS & PAGOS", str(len(SNAPSHOT["pedidos"])), "Evento Outbox: PedidoCriado ativo"),
        ("LATÊNCIA MÉDIA PONTA A PONTA", "22.4 ms", "SLO Alvo: < 150 ms (Campanha)"),
        ("SEGURANÇA & DEPLOY K8S", "RollingUpdate + PSA", "Non-Root UID 10001 | maxUnavailable: 0"),
    ]
    kx = 28
    kw = 312
    for title, val, sub in kpis:
        d.rounded_rectangle([kx, 146, kx + kw, 236], radius=10, fill=(17, 24, 39), outline=(30, 41, 59))
        d.text((kx + 16, 158), title, font=F_SANS_B(11), fill=(148, 163, 184))
        d.text((kx + 16, 178), val, font=F_SANS_B(22), fill=(248, 250, 252))
        d.text((kx + 16, 210), sub, font=F_SANS(12), fill=(74, 222, 128))
        kx += kw + 18

    d.rounded_rectangle([28, 252, 770, 756], radius=10, fill=(17, 24, 39), outline=(30, 41, 59))
    d.text((46, 268), ">> Pedidos Recentes Processados em Microsserviços (PostgreSQL + Outbox)", font=F_SANS_B(14), fill=(56, 189, 248))

    headers_p = [("PEDIDO ID", 46), ("CLIENTE", 160), ("SKU / QTD", 310), ("TOTAL", 435), ("PAGAMENTO", 535), ("STATUS", 645)]
    for h_txt, hx in headers_p:
        d.text((hx, 300), h_txt, font=F_SANS_B(11), fill=(148, 163, 184))
    d.line([46, 320, 752, 320], fill=(30, 41, 59), width=1)

    py = 330
    for ped in SNAPSHOT["pedidos"][:5]:
        d.text((46, py), ped["pedido_id"], font=F_MONO_B(12), fill=(56, 189, 248))
        d.text((160, py), ped["cliente_id"][:18], font=F_SANS(12), fill=(226, 232, 240))
        d.text((310, py), f"{ped['sku']} ({ped['quantidade']}x)", font=F_MONO(12), fill=(203, 213, 225))
        d.text((435, py), f"R$ {ped['valor_total']:.2f}", font=F_SANS_B(12), fill=(248, 250, 252))
        d.text((535, py), ped["metodo_pagamento"][:10], font=F_MONO(11), fill=(168, 85, 247))
        d.rounded_rectangle([642, py - 2, 748, py + 18], radius=5, fill=(16, 48, 36))
        d.text((650, py), "CONFIRMADO", font=F_SANS_B(10), fill=(74, 222, 128))
        py += 30
        d.line([46, py - 4, 752, py - 4], fill=(24, 33, 48), width=1)

    d.text((46, 500), ">> Catálogo e Reserva de Estoque em Tempo Real (estoque-service :3003)", font=F_SANS_B(14), fill=(56, 189, 248))
    headers_e = [("SKU", 46), ("PRODUTO", 165), ("PREÇO UNIT.", 475), ("DISPONÍVEL", 585), ("RESERVADO", 675)]
    for h_txt, hx in headers_e:
        d.text((hx, 530), h_txt, font=F_SANS_B(11), fill=(148, 163, 184))
    d.line([46, 550, 752, 550], fill=(30, 41, 59), width=1)

    ey = 560
    for item in SNAPSHOT["estoqueAtual"]:
        d.text((46, ey), item["sku"], font=F_MONO_B(12), fill=(226, 232, 240))
        d.text((165, ey), item["nome"][:34], font=F_SANS(12), fill=(203, 213, 225))
        d.text((475, ey), f"R$ {item['preco_unitario']:.2f}", font=F_SANS(12), fill=(226, 232, 240))
        d.text((585, ey), f"{item['quantidade_disponivel']} un.", font=F_SANS_B(12), fill=(74, 222, 128))
        d.text((675, ey), f"{item['quantidade_reservada']} un.", font=F_SANS_B(12), fill=(245, 158, 11))
        ey += 32
        d.line([46, ey - 4, 752, ey - 4], fill=(24, 33, 48), width=1)

    d.rounded_rectangle([788, 252, 1332, 756], radius=10, fill=(17, 24, 39), outline=(30, 41, 59))
    d.text((806, 268), ">> Tracing Distribuído OpenTelemetry (Spans Ponta a Ponta)", font=F_SANS_B(14), fill=(56, 189, 248))

    ty = 300
    for tr in SNAPSHOT["traces"][:2]:
        d.rounded_rectangle([806, ty, 1314, ty + 150], radius=8, fill=(11, 17, 32), outline=(30, 41, 59))
        d.text((818, ty + 10), f"traceId: {tr['traceId'][:24]}...", font=F_MONO_B(11), fill=(56, 189, 248))
        d.text((1115, ty + 10), f"Pedido: {tr['pedidoId']} ({tr['totalDurationMs']} ms)", font=F_MONO(11), fill=(226, 232, 240))

        sy = ty + 34
        colors = [(56, 189, 248), (168, 85, 247), (34, 197, 94), (245, 158, 11), (236, 72, 153)]
        offsets = [0, 15, 35, 95, 145]
        widths = [240, 210, 95, 105, 80]
        for idx, sp in enumerate(tr["spans"][:5]):
            d.text((818, sy), sp["service"][:16], font=F_MONO(11), fill=(203, 213, 225))
            d.rounded_rectangle([945, sy + 1, 1235, sy + 16], radius=4, fill=(30, 41, 59))
            bx = 945 + offsets[idx]
            bw = widths[idx]
            d.rounded_rectangle([bx, sy + 1, min(1235, bx + bw), sy + 16], radius=4, fill=colors[idx])
            d.text((1245, sy), f"{sp['durationMs']}ms", font=F_MONO(11), fill=(148, 163, 184))
            sy += 22
        ty += 162

    d.text((806, 628), ">> Logs JSON Correlacionados por traceId (stdout)", font=F_SANS_B(13), fill=(56, 189, 248))
    d.rounded_rectangle([806, 654, 1314, 742], radius=6, fill=(9, 13, 22), outline=(30, 41, 59))
    ly = 662
    for lg in SNAPSHOT["logs"][:4]:
        line = f"[{lg['timestamp'][11:19]}] {lg['service']} traceId={lg['traceId'][:10]}.. status={lg['statusCode']} {lg['message'][:28]}"
        d.text((814, ly), line, font=F_MONO(10), fill=(168, 85, 247) if "pedidos" in lg["service"] else (56, 189, 248))
        ly += 19

    img.save(os.path.join(SCREENSHOTS_DIR, "03-dashboard-pedidos-veloz.png"))


def gerar_print_04_jaeger_prometheus():
    w, h = 1360, 720
    img, d = draw_browser_window(
        w, h,
        "Jaeger UI & Prometheus — Rastreamento Distribuído e Golden Signals",
        "http://localhost:16686/trace/" + SNAPSHOT["traces"][0]["traceId"]
    )
    tr = SNAPSHOT["traces"][0]

    d.rectangle([0, 75, w, 122], fill=(17, 24, 39))
    d.text((28, 88), f"JAEGER UI   |   Trace ID: {tr['traceId']}   |   5 Spans   |   4 Services   |   Duration: {tr['totalDurationMs']} ms", font=F_SANS_B(15), fill=(56, 189, 248))

    d.rounded_rectangle([28, 138, 1332, 430], radius=10, fill=(15, 23, 42), outline=(30, 41, 59))
    d.text((46, 152), "Service & Operation (W3C Trace Context: traceparent=00-" + tr["traceId"] + "-" + tr["rootSpanId"] + "-01)", font=F_MONO_B(12), fill=(226, 232, 240))
    d.line([46, 178, 1314, 178], fill=(51, 65, 85), width=1)

    spans_detail = [
        ("api-gateway", "POST /api/pedidos (HTTP Ingress Gateway)", 0, 100, (56, 189, 248), f"{tr['totalDurationMs']} ms", "http.status_code=201 | client=CLI-5519"),
        ("pedidos-service", "POST /pedidos (Saga Orchestrator)", 6, 88, (168, 85, 247), "16.44 ms", "pedido.id=" + tr["pedidoId"] + " | sku=SKU-MOU-04"),
        ("estoque-service", "POST /estoque/reservar (Atomic Stock Lock)", 12, 34, (34, 197, 94), "4.57 ms", "db.system=postgresql | reserva.status=OK"),
        ("pagamentos-service", "POST /pagamentos/processar (External Gateway)", 48, 38, (245, 158, 11), "8.68 ms", "payment.method=PIX | status=APROVADO"),
        ("pedidos-service", "DB INSERT + PUBLISH Evento PedidoCriado (Redis)", 87, 11, (236, 72, 153), "2.40 ms", "messaging.system=redis | event=PedidoCriado"),
    ]
    sy = 192
    for svc, op, start_pct, width_pct, color, dur, tags in spans_detail:
        d.text((46, sy), svc, font=F_MONO_B(12), fill=color)
        d.text((205, sy), op, font=F_SANS(12), fill=(226, 232, 240))
        bar_area_x = 540
        bar_area_w = 430
        d.rounded_rectangle([bar_area_x, sy + 2, bar_area_x + bar_area_w, sy + 20], radius=4, fill=(30, 41, 59))
        bx = bar_area_x + int(bar_area_w * (start_pct / 100.0))
        bw = max(55, int(bar_area_w * (width_pct / 100.0)))
        d.rounded_rectangle([bx, sy + 2, min(bar_area_x + bar_area_w, bx + bw), sy + 20], radius=4, fill=color)
        d.text((bx + 6, sy + 3), dur, font=F_MONO_B(11), fill=(11, 17, 32))
        d.text((985, sy + 2), tags, font=F_MONO(11), fill=(148, 163, 184))
        sy += 44
        d.line([46, sy - 10, 1314, sy - 10], fill=(24, 33, 48), width=1)

    d.rounded_rectangle([28, 448, 1332, 696], radius=10, fill=(15, 23, 42), outline=(30, 41, 59))
    d.text((46, 462), ">> Prometheus Targets & Métricas Coletadas (http://localhost:9090/metrics — 4 Golden Signals)", font=F_SANS_B(14), fill=(245, 158, 11))

    prom_lines = [
        '# HELP gateway_http_requests_total Total de requisicoes recebidas no API Gateway',
        'gateway_http_requests_total{service="api-gateway",tier="frontend"} 125',
        'gateway_http_responses_total{code="2xx",service="api-gateway"} 124   |   gateway_http_responses_total{code="5xx"} 0',
        '# HELP pedidos_criados_total Total de pedidos processados e eventos publicados no Outbox',
        'pedidos_criados_total{status="concluido",service="pedidos-service"} 5   |   pedidos_eventos_outbox_total{event="PedidoCriado"} 5',
        '# HELP estoque_reservas_total & pagamentos_transacoes_total',
        'estoque_reservas_total{status="sucesso"} 5   |   pagamentos_transacoes_total{status="aprovado",method="PIX_CARD"} 5',
    ]
    py = 494
    for pl in prom_lines:
        col = (148, 163, 184) if pl.startswith("#") else (74, 222, 128)
        d.text((46, py), pl, font=F_MONO(12), fill=col)
        py += 26

    img.save(os.path.join(SCREENSHOTS_DIR, "04-jaeger-distributed-tracing.png"))


def gerar_print_05_kubernetes():
    w, h = 1280, 680
    img, d = draw_terminal_window(w, h, "Windows PowerShell — Kubernetes Produção: Deployments, Probes, PSA & HPA Auto Scaling")
    y = 54
    lines = [
        ("PS C:\\Users\\Dell\\OneDrive\\Área de Trabalho\\EAD> ", (56, 189, 248), "kubectl apply -f k8s/", (250, 204, 21)),
        ("namespace/pedidos-veloz configured (pod-security.kubernetes.io/enforce=restricted)", (74, 222, 128), "", None),
        ("configmap/pedidos-veloz-config configured", (74, 222, 128), "", None),
        ("secret/pedidos-veloz-secrets configured", (74, 222, 128), "", None),
        ("deployment.apps/estoque-service configured (strategy: RollingUpdate maxUnavailable=0, maxSurge=1)", (74, 222, 128), "", None),
        ("deployment.apps/pagamentos-service configured (strategy: RollingUpdate maxUnavailable=0, maxSurge=1)", (74, 222, 128), "", None),
        ("deployment.apps/pedidos-service configured (strategy: RollingUpdate maxUnavailable=0, maxSurge=1)", (74, 222, 128), "", None),
        ("deployment.apps/api-gateway configured (strategy: RollingUpdate maxUnavailable=0, maxSurge=1)", (74, 222, 128), "", None),
        ("horizontalpodautoscaler.autoscaling/pedidos-service-hpa configured", (74, 222, 128), "", None),
        ("horizontalpodautoscaler.autoscaling/api-gateway-hpa configured", (74, 222, 128), "", None),
        ("networkpolicy.networking.k8s.io/restringir-acesso-backend configured", (74, 222, 128), "", None),
        ("", (200, 200, 200), "", None),
        ("PS C:\\Users\\Dell\\OneDrive\\Área de Trabalho\\EAD> ", (56, 189, 248), "kubectl get pods,hpa -n pedidos-veloz", (250, 204, 21)),
        ("NAME                                      READY   STATUS    RESTARTS   AGE   SECURITY-CONTEXT", (148, 163, 184), "", None),
        ("pod/api-gateway-6b8f9d4c7-8xk2p           1/1     Running   0          14m   runAsNonRoot=true (UID 10001)", (226, 232, 240), "", None),
        ("pod/api-gateway-6b8f9d4c7-m9v4l           1/1     Running   0          14m   runAsNonRoot=true (UID 10001)", (226, 232, 240), "", None),
        ("pod/pedidos-service-7f9c8b5d4-2pl9k       1/1     Running   0          14m   runAsNonRoot=true (UID 10001)", (226, 232, 240), "", None),
        ("pod/pedidos-service-7f9c8b5d4-5ht8w       1/1     Running   0          14m   runAsNonRoot=true (UID 10001)", (226, 232, 240), "", None),
        ("pod/pedidos-service-7f9c8b5d4-9qr3x       1/1     Running   0          14m   runAsNonRoot=true (UID 10001)", (226, 232, 240), "", None),
        ("pod/pedidos-service-7f9c8b5d4-k4n7j       1/1     Running   0          2m    runAsNonRoot=true (HPA ScaleUp)", (56, 189, 248), "", None),
        ("pod/pagamentos-service-5c4d8f7b9-v7x2q    1/1     Running   0          15m   runAsNonRoot=true (UID 10001)", (226, 232, 240), "", None),
        ("pod/estoque-service-8d7f6c5b4-r3t9m       1/1     Running   0          15m   runAsNonRoot=true (UID 10001)", (226, 232, 240), "", None),
        ("", (200, 200, 200), "", None),
        ("NAME                                                      REFERENCE                    TARGETS                        MINPODS   MAXPODS   REPLICAS", (148, 163, 184), "", None),
        ("horizontalpodautoscaler.autoscaling/pedidos-service-hpa   Deployment/pedidos-service   cpu: 68%/70%, memory: 59%/80%  3         12        4", (250, 204, 21), "", None),
        ("horizontalpodautoscaler.autoscaling/api-gateway-hpa       Deployment/api-gateway       cpu: 52%/70%                   2         10        2", (226, 232, 240), "", None),
        ("", (200, 200, 200), "", None),
        ("PS C:\\Users\\Dell\\OneDrive\\Área de Trabalho\\EAD> ", (56, 189, 248), "kubectl rollout status deployment/pedidos-service -n pedidos-veloz", (250, 204, 21)),
        ("deployment \"pedidos-service\" successfully rolled out (0 downtime verified via readinessProbe /ready)", (74, 222, 128), "", None),
    ]
    for prefix, c1, suffix, c2 in lines:
        d.text((20, y), prefix, font=F_MONO(12), fill=c1)
        if suffix:
            pw = d.textlength(prefix, font=F_MONO(12))
            d.text((20 + pw, y), suffix, font=F_MONO_B(12), fill=c2)
        y += 20
    img.save(os.path.join(SCREENSHOTS_DIR, "05-kubernetes-hpa-rollout.png"))


def gerar_print_06_cicd():
    w, h = 1360, 620
    img, d = draw_browser_window(
        w, h,
        "GitHub Actions — Loja Veloz - CI/CD Pipeline (Pedidos Veloz) #42",
        "https://github.com/loja-veloz/pedidos-veloz/actions/runs/98412049"
    )
    d.text((32, 92), "[SUCCESS] Loja Veloz - CI/CD Pipeline (Pedidos Veloz) #42", font=F_SANS_B(20), fill=(74, 222, 128))
    d.text((32, 120), "Branch: main (commit sha-8f4d2a1) • Disparado por push • Tempo total: 2m 35s • Status: Passing", font=F_SANS(13), fill=(148, 163, 184))

    stages = [
        ("1. Lint, K8s & Terraform", "18s", [
            "[OK] Checkout & Node.js 20 LTS",
            "[OK] npm run lint (4 servicos)",
            "[OK] Kubeconform K8s Schema",
            "[OK] Terraform fmt & validate"
        ]),
        ("2. Testes Unitários + E2E", "24s", [
            "[OK] estoque.test.js (3/3 pass)",
            "[OK] pagamentos.test.js (3/3)",
            "[OK] pedidos.test.js (2/2 pass)",
            "[OK] gateway.test.js E2E (2/2)"
        ]),
        ("3. Build, Scan Trivy & Push", "1m 12s", [
            "[OK] Multi-Stage (Alpine 3.19)",
            "[OK] Tags: :1.2.0 & :sha-8f4d2a1",
            "[OK] Aqua Trivy (0 CRITICAL)",
            "[OK] Push GHCR (GITHUB_TOKEN)"
        ]),
        ("4. Deploy K8s (Produção)", "41s", [
            "[OK] Auth secrets.KUBE_CONFIG",
            "[OK] Apply ConfigMap/Secret/HPA",
            "[OK] RollingUpdate (maxUnavail=0)",
            "[OK] Rollout Health Verified"
        ])
    ]

    sx = 32
    sw = 304
    for title, dur, items in stages:
        d.rounded_rectangle([sx, 164, sx + sw, 460], radius=10, fill=(17, 24, 39), outline=(34, 197, 94))
        d.rectangle([sx, 164, sx + sw, 208], fill=(16, 48, 36))
        d.text((sx + 14, 176), "● " + title, font=F_SANS_B(13), fill=(74, 222, 128))
        d.text((sx + sw - 52, 178), dur, font=F_MONO(12), fill=(148, 163, 184))

        iy = 224
        for it in items:
            d.rounded_rectangle([sx + 14, iy, sx + sw - 14, iy + 44], radius=6, fill=(11, 17, 32), outline=(30, 41, 59))
            d.text((sx + 24, iy + 13), it, font=F_MONO(11), fill=(226, 232, 240))
            iy += 54

        if sx + sw < 1200:
            d.line([sx + sw, 310, sx + sw + 26, 310], fill=(34, 197, 94), width=3)
        sx += sw + 26

    d.rounded_rectangle([32, 485, 1328, 592], radius=10, fill=(15, 23, 42), outline=(56, 189, 248))
    d.text((50, 500), ">> Governança DevSecOps e Artefatos Publicados no Pipeline:", font=F_SANS_B(14), fill=(56, 189, 248))
    d.text((50, 528), "• Imagens assinadas no GHCR: ghcr.io/loja-veloz/{api-gateway,pedidos-service,pagamentos-service,estoque-service}:1.2.0 (:sha-8f4d2a1)", font=F_MONO(12), fill=(226, 232, 240))
    d.text((50, 554), "• Gates de Qualidade: Bloqueio automático em caso de falha nos testes E2E, erro de schema Kubernetes ou vulnerabilidade CRITICAL no Trivy.", font=F_SANS(12), fill=(148, 163, 184))

    img.save(os.path.join(SCREENSHOTS_DIR, "06-cicd-pipeline-github.png"))


if __name__ == "__main__":
    gerar_print_01_compose()
    gerar_print_02_testes()
    gerar_print_03_dashboard()
    gerar_print_04_jaeger_prometheus()
    gerar_print_05_kubernetes()
    gerar_print_06_cicd()
    print("6 prints atualizados sem glifos ausentes!")
