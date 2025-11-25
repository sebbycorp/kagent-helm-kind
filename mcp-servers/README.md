# MCP Servers Development

This directory contains Model Context Protocol (MCP) servers and guides for developing your own MCP servers for use with Kagent agents.

## 📋 Table of Contents

- [Overview](#overview)
- [What is MCP?](#what-is-mcp)
- [Getting Started](#getting-started)
- [Example: DateTime Server](#example-datetime-server)
- [Building Your Own MCP Server](#building-your-own-mcp-server)
- [Deployment to Kubernetes](#deployment-to-kubernetes)
- [Testing and Debugging](#testing-and-debugging)
- [Best Practices](#best-practices)

## Overview

MCP (Model Context Protocol) servers extend the capabilities of AI agents by providing them with tools and resources they can use to accomplish tasks. This directory contains:

- **Example MCP servers** demonstrating common patterns
- **Development guides** for creating your own servers
- **Deployment manifests** for Kubernetes
- **Testing utilities** to validate your servers

## What is MCP?

The Model Context Protocol (MCP) is an open protocol that allows AI agents to:

📦 **Access Tools** - Execute functions like getting the current time, making API calls, or querying databases

📚 **Read Resources** - Access files, documentation, or other data sources

💬 **Provide Prompts** - Offer pre-configured prompts or templates

### MCP Architecture

```
┌─────────────────┐
│   AI Agent      │ ← Kagent running in Kubernetes
│  (Claude, etc)  │
└────────┬────────┘
         │ MCP Protocol (stdio/SSE)
         ▼
┌─────────────────┐
│   MCP Server    │ ← Your custom server
│                 │
│  • Tools        │ ← Functions the agent can call
│  • Resources    │ ← Data the agent can access
│  • Prompts      │ ← Templates for the agent
└─────────────────┘
```

## Getting Started

### Prerequisites

```bash
# Python 3.12 or higher
python --version

# uv - Modern Python package manager (recommended)
pip install uv

# kmcp - Kagent MCP CLI tool
# Installation: https://docs.kagent.dev/mcp/kmcp
```

### Quick Start with DateTime Server

The fastest way to understand MCP servers is to explore the datetime example:

```bash
cd datetime-server

# 1. Read the quick start guide
cat QUICKSTART.md

# 2. Install dependencies
uv sync

# 3. Run locally for testing
uv run python src/main.py

# 4. Test with the MCP Inspector
npx @modelcontextprotocol/inspector uv run python src/main.py
```

## Example: DateTime Server

The `datetime-server/` is a complete, production-ready example that provides date and time tools to agents.

### Directory Structure

```
datetime-server/
├── README.md                      # Complete documentation
├── QUICKSTART.md                  # 5-minute getting started guide
├── DEPLOYMENT.md                  # Kubernetes deployment guide
├── Dockerfile                     # Container image definition
├── kmcp.yaml                      # MCP server configuration
├── pyproject.toml                 # Python dependencies
├── src/
│   ├── __init__.py
│   └── main.py                   # MCP server implementation
├── tests/
│   ├── __init__.py
│   └── test_datetime_server.py   # Unit tests
└── datetime-agent-deployment.yaml # Kubernetes manifests
```

### What It Provides

The datetime server offers these tools to agents:

#### 1. `get_date`
Returns the current date in various formats:

```python
# Formats available:
- ISO: 2024-11-25
- US: 11/25/2024
- EU: 25/11/2024
- long: Monday, November 25, 2024
- short: Nov 25, 2024
```

#### 2. `get_time`
Returns the current time:

```python
# Formats available:
- 24-hour: 14:30:00
- 12-hour: 2:30 PM
```

#### 3. `get_datetime`
Returns date and time together:

```python
# Formats available:
- ISO: 2024-11-25T14:30:00
- timestamp: 1732556400
- human: Monday, November 25, 2024 at 2:30 PM
```

### Documentation Quick Links

- **[datetime-server/README.md](./datetime-server/README.md)** - Complete server documentation
- **[datetime-server/QUICKSTART.md](./datetime-server/QUICKSTART.md)** - Get started in 5 minutes
- **[datetime-server/DEPLOYMENT.md](./datetime-server/DEPLOYMENT.md)** - Deploy to Kubernetes

## Building Your Own MCP Server

### Step 1: Initialize Project

```bash
# Create a new directory
mkdir my-mcp-server
cd my-mcp-server

# Initialize Python project with uv
uv init

# Add FastMCP dependency
uv add "fastmcp[all]"
```

### Step 2: Create Server Code

Create `src/main.py`:

```python
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("my-server")

@mcp.tool()
def greet(name: str) -> str:
    """
    Greet someone by name.
    
    Args:
        name: The name of the person to greet
        
    Returns:
        A greeting message
    """
    return f"Hello, {name}! Welcome to MCP."

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b

# Run the server
if __name__ == "__main__":
    mcp.run()
```

### Step 3: Create Configuration

Create `kmcp.yaml`:

```yaml
name: my-server
version: 0.1.0
description: My custom MCP server
author: your-name

server:
  port: 3000
  transport: stdio

tools:
  - name: greet
    description: Greet someone by name
  - name: add_numbers
    description: Add two numbers together

docker:
  image: my-server
  tag: latest
  cmd: python
  args:
    - src/main.py
```

### Step 4: Create Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml ./
COPY src/ ./src/

# Install dependencies
RUN uv sync

# Run the server
CMD ["uv", "run", "python", "src/main.py"]
```

### Step 5: Test Locally

```bash
# Run the server
uv run python src/main.py

# In another terminal, test with MCP Inspector
npx @modelcontextprotocol/inspector uv run python src/main.py
```

### Step 6: Build Docker Image

```bash
# Using kmcp (recommended)
kmcp build --project-dir . -t my-server:latest

# Or using docker directly
docker build -t my-server:latest .
```

## Deployment to Kubernetes

### Step 1: Create MCP Server Manifest

Create `my-server-deployment.yaml`:

```yaml
apiVersion: kagent.dev/v1alpha2
kind: MCPServer
metadata:
  name: my-server-mcp
  namespace: kagent
spec:
  image: localhost:5001/my-server:latest
  env:
    - name: LOG_LEVEL
      value: "INFO"
```

### Step 2: Create Agent Manifest

Create `my-agent-deployment.yaml`:

```yaml
apiVersion: kagent.dev/v1alpha2
kind: Agent
metadata:
  name: my-agent
  namespace: kagent
spec:
  modelConfigName: default
  mcpServers:
    - my-server-mcp
  systemMessage: |
    You are a helpful assistant with access to custom tools.
    
    Available tools:
    - greet: Greet someone by name
    - add_numbers: Add two numbers together
    
    Use these tools to help users with their requests.
```

### Step 3: Push to Local Registry

```bash
# Tag for local registry
docker tag my-server:latest localhost:5001/my-server:latest

# Push to Kind's local registry
docker push localhost:5001/my-server:latest
```

### Step 4: Deploy to Kubernetes

```bash
# Deploy MCP server
kubectl apply -f my-server-deployment.yaml

# Deploy agent
kubectl apply -f my-agent-deployment.yaml

# Verify deployment
kubectl get mcpservers -n kagent
kubectl get agents -n kagent
```

## Testing and Debugging

### Local Testing with MCP Inspector

The MCP Inspector is a web-based tool for testing MCP servers:

```bash
# Install and run
npx @modelcontextprotocol/inspector uv run python src/main.py
```

This opens a web interface where you can:
- View available tools
- Test tool calls with different parameters
- See request/response data
- Debug issues

### Unit Testing

Create tests in `tests/test_my_server.py`:

```python
import pytest
from src.main import greet, add_numbers

def test_greet():
    result = greet("Alice")
    assert result == "Hello, Alice! Welcome to MCP."

def test_add_numbers():
    result = add_numbers(5, 3)
    assert result == 8
    
def test_add_numbers_negative():
    result = add_numbers(-5, 10)
    assert result == 5
```

Run tests:

```bash
uv run pytest tests/
```

### Debugging in Kubernetes

```bash
# View MCP server logs
kubectl logs -n kagent -l kagent.dev/mcp-server=my-server-mcp

# View agent logs
kubectl logs -n kagent -l kagent.dev/agent=my-agent

# Describe resources for events
kubectl describe mcpserver my-server-mcp -n kagent
kubectl describe agent my-agent -n kagent

# Check if MCP server is registered with the agent
kubectl get agent my-agent -n kagent -o yaml
```

### Common Issues

#### MCP Server Not Starting

```bash
# Check pod status
kubectl get pods -n kagent | grep my-server

# View detailed events
kubectl describe pod <pod-name> -n kagent

# Common causes:
# - Image pull errors (check image name and registry)
# - Python syntax errors (check logs)
# - Missing dependencies (verify pyproject.toml)
```

#### Agent Can't Connect to MCP Server

```bash
# Verify MCP server is running
kubectl get mcpserver my-server-mcp -n kagent

# Check agent configuration
kubectl get agent my-agent -n kagent -o yaml

# Look for connection errors in agent logs
kubectl logs -n kagent -l kagent.dev/agent=my-agent | grep -i error
```

## Best Practices

### 1. Tool Design

✅ **DO:**
- Write clear, descriptive docstrings
- Use type hints for all parameters
- Validate input parameters
- Return structured data
- Handle errors gracefully

❌ **DON'T:**
- Use vague or ambiguous tool names
- Ignore error cases
- Return unstructured output
- Perform side effects without documentation

### 2. Error Handling

```python
@mcp.tool()
def divide(a: float, b: float) -> float:
    """
    Divide two numbers.
    
    Args:
        a: Numerator
        b: Denominator (must not be zero)
        
    Returns:
        Result of a / b
        
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### 3. Configuration Management

Use environment variables for configuration:

```python
import os

API_KEY = os.getenv("API_KEY", "")
BASE_URL = os.getenv("BASE_URL", "https://api.example.com")
```

In Kubernetes manifests:

```yaml
spec:
  env:
    - name: API_KEY
      valueFrom:
        secretKeyRef:
          name: my-secret
          key: api-key
    - name: BASE_URL
      value: "https://api.example.com"
```

### 4. Logging

```python
import logging

logger = logging.getLogger(__name__)

@mcp.tool()
def fetch_data(query: str) -> dict:
    """Fetch data from external API."""
    logger.info(f"Fetching data for query: {query}")
    
    try:
        # ... fetch logic ...
        logger.info("Data fetched successfully")
        return result
    except Exception as e:
        logger.error(f"Failed to fetch data: {e}")
        raise
```

### 5. Security

- **Never hardcode secrets** - Use Kubernetes secrets
- **Validate all inputs** - Don't trust agent inputs blindly
- **Limit permissions** - Use least-privilege principle
- **Sanitize outputs** - Remove sensitive data before returning

### 6. Performance

- **Cache when possible** - Avoid repeated API calls
- **Set timeouts** - Don't let requests hang indefinitely
- **Use async** - For I/O-bound operations
- **Monitor resource usage** - Set appropriate resource limits in Kubernetes

## Additional Resources

### Official Documentation

- **[MCP Specification](https://modelcontextprotocol.io)** - Protocol details
- **[FastMCP Documentation](https://github.com/jlowin/fastmcp)** - Python framework
- **[Kagent MCP Docs](https://docs.kagent.dev/mcp)** - Kagent-specific guides

### Example MCP Servers

- **[Anthropic Examples](https://github.com/anthropics/anthropic-mcp-examples)** - Official examples
- **[Community Servers](https://github.com/modelcontextprotocol/servers)** - Community-maintained

### Tools

- **[MCP Inspector](https://github.com/modelcontextprotocol/inspector)** - Testing UI
- **[kmcp CLI](https://docs.kagent.dev/mcp/kmcp)** - Build and deploy tools

## Next Steps

1. **Explore the datetime-server example** - See [datetime-server/QUICKSTART.md](./datetime-server/QUICKSTART.md)
2. **Build your own MCP server** - Follow the guide above
3. **Deploy to Kubernetes** - Use the manifests as templates
4. **Publish to Agent Registry** - See [../registry/README.md](../registry/README.md)

---

**Happy Building! 🚀**

Need help? Check out:
- [GitHub Issues](https://github.com/sebbycorp/kagent-helm-kind/issues)
- [GitHub Discussions](https://github.com/sebbycorp/kagent-helm-kind/discussions)
- [MCP Community Discord](https://discord.gg/modelcontextprotocol)
