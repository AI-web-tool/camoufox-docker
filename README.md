# camoufox-docker

Docker container for [Camoufox](https://camoufox.com) — a stealthy, anti-detect browser built on Firefox that evades bot detection. Exposes a Playwright WebSocket server for remote browser automation.

## Quick Start

### With Docker Compose

Add to your `docker-compose.yaml`:

```yaml
camoufox:
  build: ./camoufox
  container_name: camoufox
  restart: always
  ports:
    - "9222:9222"
  environment:
    CAMOUFOX_PORT: 9222
```

```bash
docker compose build camoufox
docker compose up -d camoufox
```

### With Docker directly

```bash
docker build -t camoufox .
docker run -d --name camoufox -p 9222:9222 -e CAMOUFOX_PORT=9222 --restart always camoufox
```

## Getting the WebSocket Endpoint

Each time the container starts, it generates a random token for the WebSocket endpoint. Get it from the logs:

```bash
docker logs camoufox
# Websocket endpoint: ws://localhost:9222/9fdb26279ee5d7d04595337a5acec1c7
```

Or extract just the endpoint:

```bash
docker logs camoufox 2>&1 | grep "Websocket endpoint" | tail -1
```

The token changes on every container restart.

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `CAMOUFOX_PORT` | `9222` | Port for the Playwright WebSocket server |

## Usage with n8n

This container pairs with the [n8n-nodes-camoufox](https://github.com/LPilic/n8n-nodes-camoufox) community node. Configure the credential with:

- **WebSocket Endpoint**: `ws://camoufox:9222/<token>` (use the container name when both services are on the same Docker network)

## License

MIT
