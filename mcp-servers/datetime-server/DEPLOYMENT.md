# DateTime MCP Server

A simple MCP server that provides date and time tools for AI agents.

## About

This MCP server provides three tools for working with dates and times:

1. **get_date** - Get the current date in various formats (ISO, US, EU, long, short)
2. **get_time** - Get the current time in 24-hour or 12-hour format
3. **get_datetime** - Get the current date and time together in various formats

## Tools

### get_date
Returns the current date in the specified format.

**Parameters:**
- `format` (string, optional): Date format. Options:
  - `"iso"` - ISO 8601 format (YYYY-MM-DD) [default]
  - `"us"` - US format (MM/DD/YYYY)
  - `"eu"` - European format (DD/MM/YYYY)
  - `"long"` - Long format (e.g., "January 24, 2025")
  - `"short"` - Short format (e.g., "Jan 24, 2025")

**Example:** `get_date(format="long")` → "November 24, 2025"

### get_time
Returns the current time in the specified format.

**Parameters:**
- `format` (string, optional): Time format. Options:
  - `"24h"` - 24-hour format [default]
  - `"12h"` - 12-hour format with AM/PM
- `include_seconds` (boolean, optional): Whether to include seconds [default: True]

**Example:** `get_time(format="12h", include_seconds=False)` → "03:41 PM"

### get_datetime
Returns the current date and time together.

**Parameters:**
- `format` (string, optional): DateTime format. Options:
  - `"iso"` - ISO 8601 format (YYYY-MM-DD HH:MM:SS) [default]
  - `"timestamp"` - Unix timestamp
  - `"human"` - Human-readable format
- `timezone` (string, optional): Timezone [currently only "local" is supported]

**Example:** `get_datetime(format="human")` → "November 24, 2025 at 03:41 PM"

## Quick Start

### Option 1: Deploy with kmcp CLI (Recommended)

1. **Build the Docker image and load it to your kind cluster:**
   ```bash
   cd /Users/sebbycorp/Library/CloudStorage/GoogleDrive-sebastian.maniak@solo.io/My\ Drive/Projects/kagent-helm-kind/mcp-servers/datetime-server
   kmcp build --project-dir . -t datetime-server:latest --kind-load-cluster kind
   ```

2. **Deploy using kmcp:**
   ```bash
   kmcp deploy --file kmcp.yaml --image datetime-server:latest
   ```

3. **Verify the deployment:**
   ```bash
   kubectl get pods
   kubectl get mcpserver datetime-server
   ```

### Option 2: Deploy with kubectl

1. **Build the Docker image and load it to your kind cluster:**
   ```bash
   cd /Users/sebbycorp/Library/CloudStorage/GoogleDrive-sebastian.maniak@solo.io/My\ Drive/Projects/kagent-helm-kind/mcp-servers/datetime-server
   kmcp build --project-dir . -t datetime-server:latest --kind-load-cluster kind
   ```

2. **Apply the deployment manifest:**
   ```bash
   kubectl apply -f datetime-server-deployment.yaml
   ```

3. **Verify the deployment:**
   ```bash
   kubectl get pods
   kubectl get mcpserver datetime-server
   ```

### Option 3: Test Locally First

Before deploying to Kubernetes, you can test the server locally:

```bash
# Run locally with MCP inspector
kmcp run --project-dir .

# Or run with uv directly
uv run python src/main.py
```

## Deployment Files

- `kmcp.yaml` - MCP server configuration
- `datetime-server-deployment.yaml` - Kubernetes MCPServer resource manifest
- `Dockerfile` - Docker image build configuration

## Testing

Once deployed, you can test the tools using the MCP inspector:

```bash
# If deployed via kmcp deploy, the inspector opens automatically
# Otherwise, you can connect manually using the inspector
```

## Directory Structure

```
datetime-server/
├── src/
│   ├── tools/
│   │   ├── echo.py          # Example echo tool (can be removed)
│   │   ├── get_date.py      # Date tool
│   │   ├── get_time.py      # Time tool
│   │   └── get_datetime.py  # DateTime tool
│   ├── core/
│   │   ├── server.py        # MCP server implementation
│   │   └── utils.py         # Utility functions
│   └── main.py              # Entry point
├── kmcp.yaml                # MCP configuration
├── datetime-server-deployment.yaml  # Kubernetes deployment
├── Dockerfile               # Docker build config
└── README.md               # This file
```

## Use with Kagent/AgentGateway

If you plan to use this MCP server with kagent and agentgateway, add the `kagent.dev/discovery=disabled` label to prevent automatic discovery:

```yaml
apiVersion: kagent.dev/v1alpha1
kind: MCPServer
metadata:
  name: datetime-server
  namespace: default
  labels:
    kagent.dev/discovery: disabled
spec:
  deployment:
    image: "datetime-server:latest"
    port: 3000
    cmd: "python"
    args: ["src/main.py"]
  transportType: "stdio"
```

## Next Steps

- Add timezone support to all tools
- Add tools for date/time manipulation (add days, subtract hours, etc.)
- Add formatting helpers for different locales
- Add natural language parsing (e.g., "tomorrow", "next week")
