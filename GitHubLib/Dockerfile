FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* tsconfig.json ./
RUN npm ci --no-audit --no-fund || npm install --no-audit --no-fund
COPY src/ src/
RUN npx tsc

FROM node:22-alpine AS prod
# docker-cli: the Karen fuzz handler shells out to `docker run` against the
# docker-socket-proxy (DOCKER_HOST) to spawn hardened per-world fuzz containers.
RUN apk add --no-cache git ca-certificates docker-cli
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev --no-audit --no-fund || npm install --omit=dev --no-audit --no-fund
COPY --from=build /app/dist ./dist
ENV NODE_ENV=production
ENV PORT=3000
EXPOSE 3000
CMD ["node", "dist/index.js"]
