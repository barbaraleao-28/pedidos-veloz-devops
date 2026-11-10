# ============================================================================
# STAGE 1: Validação de Sintaxe e Preparação (Multi-Stage Build)
# ============================================================================
FROM node:20-alpine3.19 AS builder

WORKDIR /build

COPY package.json ./
COPY src/ ./src/

RUN npm run lint

# ============================================================================
# STAGE 2: Imagem Final de Produção (Enxuta, Imutável e Não-Root)
# ============================================================================
FROM node:20-alpine3.19 AS production

ARG APP_VERSION=1.2.0
LABEL org.opencontainers.image.title="pedidos-service" \
      org.opencontainers.image.description="Microsserviço de Pedidos - Loja Veloz" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.vendor="Loja Veloz E-Commerce"

ENV NODE_ENV=production \
    APP_VERSION=${APP_VERSION} \
    PEDIDOS_PORT=3001

WORKDIR /app

RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup && \
    chown -R appuser:appgroup /app

COPY --from=builder --chown=appuser:appgroup /build/package.json ./
COPY --from=builder --chown=appuser:appgroup /build/src ./src

USER 10001:10001

EXPOSE 3001

HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3001/health || exit 1

CMD ["node", "src/index.js"]
