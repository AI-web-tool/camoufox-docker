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

Each time the container starts, it generates a random token for the WebSocket endpoint.

**Option 1: Query the API** (recommended for programmatic access)

```bash
curl -s http://localhost:9222/json
# {"wsEndpointPath":"/9fdb26279ee5d7d04595337a5acec1c7"}
```

**Option 2: Check the logs**

```bash
docker logs camoufox
# Websocket endpoint: ws://localhost:9222/9fdb26279ee5d7d04595337a5acec1c7
```

**Option 3: Set a fixed token** (no need to discover)

Set the `CAMOUFOX_WS_PATH` environment variable to use a predictable token that persists across restarts:

```yaml
environment:
  CAMOUFOX_PORT: 9222
  CAMOUFOX_WS_PATH: my-secret-token
# Endpoint will always be: ws://localhost:9222/my-secret-token
```

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `CAMOUFOX_PORT` | `9222` | Port for the Playwright WebSocket server |
| `CAMOUFOX_WS_PATH` | *(random)* | Fixed WebSocket path/token. If unset, a random token is generated on each start. |

## Usage with n8n

This container pairs with the [n8n-nodes-camoufox](https://github.com/LPilic/n8n-nodes-camoufox) community node. Configure the credential with:

- **WebSocket Endpoint**: `ws://camoufox:9222` (the node auto-discovers the token via the `/json` API), or `ws://camoufox:9222/<token>` with the full token

## License

MIT
