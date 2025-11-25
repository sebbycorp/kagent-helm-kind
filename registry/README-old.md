# Agent Registry

Publish, discover, and deploy MCP servers and agents using the Agent Registry.

## 📋 Table of Contents

- [Overview](#overview)
- [What is Agent Registry?](#what-is-agent-registry)
- [Getting Started](#getting-started)
- [Publishing MCP Servers](#publishing-mcp-servers)
- [Publishing Agents](#publishing-agents)
- [Deploying from Registry](#deploying-from-registry)
- [Common Commands](#common-commands)
- [Troubleshooting](#troubleshooting)

## Overview

The Agent Registry is a centralized platform for managing MCP servers and AI agents, similar to how Docker Hub manages container images. It provides:

- 🔍 **Discovery** - Browse available MCP servers and agents
- 📦 **Publishing** - Share your MCP servers with others
- 🏷️ **Versioning** - Manage multiple versions of your servers
- 🚀 **Deployment** - Deploy agents directly from the registry
- 🌐 **Web UI** - Visual interface at `http://localhost:12121`

## What is Agent Registry?

### Registry vs Kubernetes

It's important to understand the distinction:

```
┌─────────────────────────────────────┐
│   Agent Registry (localhost:12121)  │
│   - Discovery & Distribution        │
│   - Version Management               │
│   - Metadata Storage                 │
│   - Image Repository                 │
└─────────────────────────────────────┘
                  │
                  │ arctl pull/deploy
                  ▼
┌─────────────────────────────────────┐
│   Kubernetes Cluster                 │
│   - Runtime Environment              │
│   - Running Agents                   │
│   - Running MCP Servers              │
└─────────────────────────────────────┘
```

| Aspect | Agent Registry | Kubernetes (kagent) |
|--------|---------------|---------------------|
| **Purpose** | Discovery & distribution | Runtime execution |
| **Location** | `localhost:12121` | K8s cluster |
| **Add Method** | `arctl mcp publish` | `kubectl apply` |
| **Resources** | Metadata & images | Running pods |
| **View** | Web UI / CLI | `kubectl get` |
| **Usage** | Share & discover | Deploy & run |

## Getting Started

### 1. Install arctl

The `arctl` CLI is your main interface to the Agent Registry.

```bash
# Install using the official script
curl -fsSL https://raw.githubusercontent.com/agentregistry-dev/agentregistry/main/scripts/get-arctl | bash

# Verify installation
arctl version
```

### 2. Start Agent Registry

The registry will start automatically when you run your first command:

```bash
# This will start the registry daemon
arctl mcp list

# Verify it's running
curl http://localhost:12121/health
```

The registry runs as a background daemon and includes:
- **API Server** on port 12121
- **Web UI** accessible at `http://localhost:12121`
- **Local storage** for metadata and images

### 3. Configure Your Environment

```bash
# (Optional) Configure Cursor integration
arctl configure cursor

# View current configuration
arctl config show
```

## Publishing MCP Servers

### Quick Publish

Navigate to your MCP server directory and publish:

```bash
cd mcp-servers/datetime-server

# Publish to registry (local only)
arctl mcp publish .
```

This will:
1. Read your `mcp.yaml` or `kmcp.yaml` configuration
2. Register the MCP server metadata in the registry
3. Make it discoverable via CLI and Web UI

### Publish with Docker Registry Push

To share your MCP server publicly, push to Docker Hub or another registry:

```bash
# Build, tag, push, and publish in one command
arctl mcp publish . \
  --docker-url docker.io/sebbycorp/datetime-server \
  --tag v1.0.0 \
  --push
```

This will:
1. Build the Docker image
2. Tag it as `docker.io/sebbycorp/datetime-server:v1.0.0`
3. Push to Docker registry
4. Register in Agent Registry with metadata

### Required Files

Your MCP server directory should contain:

#### mcp.yaml (or kmcp.yaml)

```yaml
name: datetime-server
version: 1.0.0
description: MCP server providing date and time tools
author: sebbycorp
framework: fastmcp-python

server:
  port: 3000
  transport: stdio

tools:
  - name: get_date
    description: Get current date in various formats
  - name: get_time
    description: Get current time
  - name: get_datetime
    description: Get current date and time together

docker:
  image: datetime-server
  tag: latest
  cmd: python
  args:
    - src/main.py
```

#### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml ./
COPY src/ ./src/

RUN uv sync

CMD ["uv", "run", "python", "src/main.py"]
```

### Verify Publication

```bash
# List all MCP servers in registry
arctl mcp list

# Show details of your server
arctl mcp show datetime-server

# View in Web UI
open http://localhost:12121
```

## Publishing Agents

An agent is a complete package that combines MCP servers with configuration and system prompts.

### Step 1: Create Agent Project

```bash
# Initialize a new agent project
arctl agent init my-datetime-agent
cd my-datetime-agent
```

### Step 2: Configure Agent

Edit `agent.yaml`:

```yaml
name: datetime-agent
version: 1.0.0
description: AI agent that provides date and time information
author: sebbycorp

# MCP servers this agent uses
mcp_servers:
  - name: datetime-server
    version: 1.0.0

# Agent configuration
agent:
  model: claude-3-5-sonnet-20241022
  system_message: |
    You are a helpful assistant that provides accurate date and time information.
    
    You have access to the following tools:
    - get_date: Returns the current date in various formats
    - get_time: Returns the current time in 24-hour or 12-hour format
    - get_datetime: Returns date and time together
    
    When users ask about dates or times, use the appropriate tool.
    Be concise and accurate in your responses.

# Skills/capabilities
skills:
  - id: date-time-info
    name: Date & Time Information
    description: Get current date, time, or datetime in various formats
    tags:
      - datetime
      - time
      - date
    examples:
      - "What's today's date?"
      - "What time is it?"
      - "Get me the current datetime in ISO format"
      - "What day of the week is it?"
```

### Step 3: Publish Agent

```bash
# Publish to registry
arctl agent publish .

# Verify publication
arctl agent list
arctl agent show datetime-agent
```

## Deploying from Registry

Once MCP servers and agents are in the registry, you or others can deploy them easily.

### Deploy MCP Server

```bash
# Deploy MCP server from registry to Kubernetes
arctl mcp deploy datetime-server

# Specify version
arctl mcp deploy datetime-server --version 1.0.0

# Deploy to specific namespace
arctl mcp deploy datetime-server --namespace kagent
```

### Deploy Agent

```bash
# Deploy agent from registry
arctl agent deploy datetime-agent

# With options
arctl agent deploy datetime-agent \
  --version 1.0.0 \
  --namespace kagent
```

### Verify Deployment

```bash
# Check MCP server status
kubectl get mcpservers -n kagent

# Check agent status
kubectl get agents -n kagent

# View logs
kubectl logs -n kagent -l kagent.dev/agent=datetime-agent
```

## Common Commands

### MCP Server Commands

```bash
# 📋 List all MCP servers
arctl mcp list

# 📤 Publish MCP server
arctl mcp publish ./path/to/server

# 📤 Publish with Docker push
arctl mcp publish . \
  --docker-url docker.io/username/server \
  --tag v1.0.0 \
  --push

# 👀 View server details
arctl mcp show server-name

# 🚀 Deploy MCP server
arctl mcp deploy server-name

# 🚀 Deploy specific version
arctl mcp deploy server-name --version 1.0.0

# 🗑️ Remove MCP server
arctl mcp remove server-name
```

### Agent Commands

```bash
# 📋 List all agents
arctl agent list

# 🆕 Initialize new agent project
arctl agent init my-agent

# 📤 Publish agent
arctl agent publish ./path/to/agent

# 👀 View agent details
arctl agent show agent-name

# 🚀 Deploy agent
arctl agent deploy agent-name

# 🗑️ Remove agent
arctl agent remove agent-name
```

### Skill Commands

```bash
# 📋 List all skills
arctl skill list

# 👀 View skill details
arctl skill show skill-name

# 🔍 Search skills by tag
arctl skill search --tag datetime
```

### Configuration Commands

```bash
# ⚙️ Configure Cursor integration
arctl configure cursor

# ⚙️ Show configuration
arctl config show

# ⚙️ Set registry URL
arctl config set registry-url http://localhost:12121
```

## Troubleshooting

### Registry Not Responding

**Symptom:** `arctl` commands fail with connection errors

**Solutions:**

```bash
# Check if registry is running
curl http://localhost:12121/health

# Start the registry daemon
arctl mcp list

# Check for port conflicts
lsof -i :12121

# Kill conflicting processes
kill -9 <PID>

# Restart arctl daemon
arctl daemon restart
```

### MCP Server Not Found

**Symptom:** `arctl mcp show server-name` returns "not found"

**Solutions:**

```bash
# Verify publication
arctl mcp list | grep server-name

# Re-publish
cd path/to/server
arctl mcp publish .

# Check mcp.yaml exists and is valid
cat mcp.yaml
```

### Docker Image Push Fails

**Symptom:** `--push` flag results in authentication errors

**Solutions:**

```bash
# Login to Docker Hub
docker login

# Verify credentials
docker info | grep Username

# Try push again
arctl mcp publish . \
  --docker-url docker.io/username/server \
  --tag v1.0.0 \
  --push
```

### Agent Deployment Fails

**Symptom:** `arctl agent deploy` fails or agent doesn't start

**Solutions:**

```bash
# Check if MCP servers are available
arctl mcp list

# Verify agent configuration
arctl agent show agent-name

# Check Kubernetes resources
kubectl get agents -n kagent
kubectl get mcpservers -n kagent

# View agent logs
kubectl logs -n kagent -l kagent.dev/agent=agent-name

# Describe agent for events
kubectl describe agent agent-name -n kagent
```

### Web UI Not Loading

**Symptom:** `http://localhost:12121` doesn't load

**Solutions:**

```bash
# Verify registry is running
curl http://localhost:12121/health

# Check for errors in registry logs
arctl daemon logs

# Restart the daemon
arctl daemon restart

# Access via explicit URL
open http://127.0.0.1:12121
```

## Examples

### Example 1: Complete DateTime Server Workflow

```bash
# 1. Navigate to MCP server
cd mcp-servers/datetime-server

# 2. Publish to registry
arctl mcp publish .

# 3. Verify publication
arctl mcp show datetime-server

# 4. Deploy to Kubernetes
arctl mcp deploy datetime-server --namespace kagent

# 5. Verify deployment
kubectl get mcpservers -n kagent
```

### Example 2: Publish and Share Publicly

```bash
# 1. Build and publish to Docker Hub
cd mcp-servers/datetime-server

arctl mcp publish . \
  --docker-url docker.io/sebbycorp/datetime-server \
  --tag v1.0.0 \
  --push

# 2. Anyone can now deploy it
arctl mcp deploy datetime-server
```

### Example 3: Create Complete Agent

```bash
# 1. Initialize agent project
arctl agent init weather-agent
cd weather-agent

# 2. Edit agent.yaml (configure MCP servers, system message, etc.)
vim agent.yaml

# 3. Publish agent
arctl agent publish .

# 4. Deploy agent
arctl agent deploy weather-agent --namespace kagent

# 5. Verify
kubectl get agents -n kagent
```

## Advanced Usage

### Custom Registry URL

If running a remote registry:

```bash
# Configure custom registry
arctl config set registry-url https://registry.example.com

# Use with commands
arctl mcp publish . --registry https://registry.example.com
```

### Private Registries

For private Docker registries:

```bash
# Login to private registry
docker login registry.example.com

# Publish with private registry
arctl mcp publish . \
  --docker-url registry.example.com/my-org/my-server \
  --tag v1.0.0 \
  --push
```

### Version Management

```bash
# Publish multiple versions
arctl mcp publish . --tag v1.0.0
arctl mcp publish . --tag v1.1.0
arctl mcp publish . --tag latest

# Deploy specific version
arctl mcp deploy my-server --version v1.0.0

# List versions
arctl mcp show my-server --versions
```

## Additional Resources

- **[Agent Registry GitHub](https://github.com/agentregistry-dev/agentregistry)** - Source code and documentation
- **[Detailed Tutorial](../agent_registry_guide.md)** - Step-by-step guide with examples
- **[MCP Server Development](../mcp-servers/README.md)** - Create your own MCP servers
- **[Kagent Documentation](https://docs.kagent.dev)** - Official Kagent docs

## Quick Reference Card

```bash
# 🚀 Getting Started
curl -fsSL https://raw.githubusercontent.com/agentregistry-dev/agentregistry/main/scripts/get-arctl | bash

# 📋 Discovery
arctl mcp list                    # List MCP servers
arctl agent list                  # List agents
arctl skill list                  # List skills

# 📤 Publishing
arctl mcp publish .               # Publish MCP server
arctl agent publish .             # Publish agent

# 👀 Details
arctl mcp show <name>             # View MCP server details
arctl agent show <name>           # View agent details

# 🚀 Deployment
arctl mcp deploy <name>           # Deploy MCP server
arctl agent deploy <name>         # Deploy agent

# 🗑️ Management
arctl mcp remove <name>           # Remove MCP server
arctl agent remove <name>         # Remove agent

# 🌐 Web UI
open http://localhost:12121       # Access registry UI
```

---

**Ready to Publish? 🚀**

Start by publishing the datetime-server example:

```bash
cd mcp-servers/datetime-server
arctl mcp publish .
```

Then view it in the Web UI: `http://localhost:12121`

---

**Need Help?**

- [GitHub Issues](https://github.com/sebbycorp/kagent-helm-kind/issues)
- [Agent Registry Repo](https://github.com/agentregistry-dev/agentregistry)
- [Discussions](https://github.com/sebbycorp/kagent-helm-kind/discussions)