# DateTime MCP Server - Quick Deployment Guide

## TL;DR - Deploy in 3 Steps

```bash
# 1. Navigate to the project
cd "mcp-servers/datetime-server"

# 2. Build and load to kind cluster
kmcp build --project-dir . -t datetime-server:latest --kind-load-cluster kind

# 3. Deploy to Kubernetes
kmcp deploy --file kmcp.yaml --image datetime-server:latest
```

## Alternative: Using kubectl

```bash
# 1. Navigate to the project
cd "mcp-servers/datetime-server"

# 2. Build and load to kind cluster
kmcp build --project-dir . -t datetime-server:latest --kind-load-cluster kind

# 3. Apply the deployment manifest
kubectl apply -f datetime-server-deployment.yaml

# 4. Check status
kubectl get pods
kubectl get mcpserver datetime-server
```

## Available Tools

| Tool | Description | Example Usage |
|------|-------------|---------------|
| `get_date` | Get current date in various formats | `get_date(format="long")` |
| `get_time` | Get current time in 24h or 12h format | `get_time(format="12h")` |
| `get_datetime` | Get current date and time together | `get_datetime(format="human")` |

## Verify Deployment

```bash
# Check if pod is running
kubectl get pods | grep datetime-server

# Check MCP server status
kubectl get mcpserver datetime-server

# View pod logs
kubectl logs -l app=datetime-server

# Test with MCP inspector (if deployed via kmcp deploy)
# Inspector should open automatically
```

## Test Locally First (Optional)

```bash
# Run with MCP inspector
kmcp run --project-dir .

# Or run directly with uv
uv run python src/main.py
```
