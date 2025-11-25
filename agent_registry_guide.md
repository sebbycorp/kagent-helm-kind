# Adding DateTime MCP Server to Agent Registry

## Overview

Agent Registry (localhost:12121) is a centralized registry for MCP servers and agents, similar to Docker Hub for containers. It allows you to:

- **Publish** MCP servers and agents
- **Share** them with others
- **Version** your releases
- **Discover** available MCP servers

This is **different from your Kubernetes deployment**, which is the runtime environment where your agents actually run.

```
┌─────────────────────────────────────┐
│   Agent Registry (localhost:12121)  │
│   - Discovery & Distribution        │
│   - Version Management               │
│   - Metadata Storage                 │
└─────────────────────────────────────┘
                  │
                  │ arctl pull/deploy
                  ▼
┌─────────────────────────────────────┐
│   Kubernetes Cluster                 │
│   - Runtime Environment              │
│   - datetime-agent (running)         │
│   - datetime-agent-mcp (running)     │
└─────────────────────────────────────┘
```

## Prerequisites

✅ You already have:
- Agent Registry running at `http://localhost:12121`
- `arctl` CLI installed
- datetime-server MCP project in `mcp-servers/datetime-server/`
- Docker image `datetime-server:latest` built

## Step 1: Understanding arctl Commands

```bash
# List what's currently in the registry
arctl mcp list        # List MCP servers
arctl agent list      # List agents
arctl skill list      # List skills

# Publish to registry
arctl mcp publish ./path/to/mcp-server
arctl agent publish ./path/to/agent

# Show details
arctl mcp show <name>
arctl agent show <name>
```

## Step 2: Create mcp.yaml (if needed)

arctl looks for` mcp.yaml` in your project. You have `kmcp.yaml`, which might work. If not, create `mcp.yaml`:

```bash
cd mcp-servers/datetime-server
```

Create **`mcp.yaml`** (if `kmcp.yaml` doesn't work):

```yaml
name: datetime-server
version: 0.1.0
description: A simple MCP server that provides date and time tools
author: sebbycorp
framework: fastmcp-python

# MCP server configuration
server:
  port: 3000
  transport: stdio
  
# Tools provided by this MCP server
tools:
  - name: get_date
    description: Get current date in various formats (ISO, US, EU, long, short)
  - name: get_time
    description: Get current time in 24-hour or 12-hour format
  - name: get_datetime
    description: Get current date and time together (ISO, timestamp, human-readable)

# Docker configuration
docker:
  image: datetime-server
  tag: latest
  cmd: python
  args:
    - src/main.py
```

## Step 3: Publish MCP Server to Registry

### Option 1: Publish Without Pushing to Docker Registry

```bash
cd mcp-servers/datetime-server

# Publish to Agent Registry (local only)
arctl mcp publish .
```

This will:
- Read your `mcp.yaml` (or `kmcp.yaml`)
- Register the MCP server in the Agent Registry
- Make it discoverable at `http://localhost:12121`

### Option 2: Publish WITH Docker Registry Push

If you want to push to Docker Hub or another registry:

```bash
# Build and publish with push
arctl mcp publish . \
  --docker-url docker.io/sebbycorp \
  --tag v0.1.0 \
  --push
```

This will:
- Build the Docker image
- Tag it as `docker.io/sebbycorp/datetime-server:v0.1.0`
- Push to Docker registry
- Publish to Agent Registry

## Step 4: Verify in Agent Registry

### Via CLI

```bash
# List MCP servers in registry
arctl mcp list

# Show details
arctl mcp show datetime-server
```

### Via Web UI

1. Open `http://localhost:12121` in your browser
2. Navigate to "MCP Servers" section
3. You should see **datetime-server** listed

## Step 5: Publish an Agent (Optional)

If you want to publish a complete agent that uses your MCP server:

### Create Agent Project

```bash
# Initialize a new agent project
arctl agent init my-datetime-agent
cd my-datetime-agent
```

### Edit `agent.yaml`

```yaml
name: datetime-agent
version: 0.1.0
description: AI agent that provides date and time information
author: sebbycorp

# MCP servers this agent uses
mcp_servers:
  - name: datetime-server
    version: 0.1.0

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
```

### Publish Agent

```bash
arctl agent publish .
```

### Verify Agent

```bash
# List agents
arctl agent list

# Show details
arctl agent show datetime-agent
```

## Step 6: Deploy from Registry

Once published to the registry, you or others can deploy it:

```bash
# Deploy MCP server from registry
arctl mcp deploy datetime-server

# Deploy agent from registry
arctl agent deploy datetime-agent
```

## Comparison: Registry vs Kubernetes

| Aspect | Agent Registry | Kubernetes (kagent) |
|--------|---------------|---------------------|
| **Purpose** | Discovery & distribution | Runtime execution |
| **Location** | `localhost:12121` | K8s cluster |
| **Add Method** | `arctl mcp publish` | `kubectl apply` |
| **Resources** | Metadata & images | Running pods |
| **View** | Web UI / CLI | `kubectl get` |
| **Usage** | Share & discover | Deploy & run |

## Troubleshooting

### Issue: "mcp.yaml not found"

**Solution:** Create `mcp.yaml` as shown in Step 2, or check if arctl accepts `kmcp.yaml`.

### Issue: "Docker image not found"

**Solution:** Make sure you've built the image:

```bash
cd mcp-servers/datetime-server
kmcp build --project-dir . -t datetime-server:latest
```

### Issue: "Registry not responding"

**Solution:** Start the registry:

```bash
arctl mcp list -A   # This starts the daemon if not running
```

Then check: `http://localhost:12121`

### Issue: "Cannot push to Docker registry"

**Solution:** Login to Docker first:

```bash
docker login
```

Then use `--push` flag with `arctl mcp publish`.

## Quick Reference

```bash
# 📋 List everything in registry
arctl mcp list
arctl agent list
arctl skill list

# 📤 Publish to registry
arctl mcp publish ./mcp-servers/datetime-server
arctl agent publish ./my-agent

# 👀 View details
arctl mcp show datetime-server
arctl agent show datetime-agent

# 🚀 Deploy from registry
arctl mcp deploy datetime-server
arctl agent deploy datetime-agent

# 🗑️ Remove from registry
arctl mcp remove datetime-server
arctl agent remove datetime-agent

# 🌐 Access Web UI
open http://localhost:12121
```

## Next Steps

1. **Publish your datetime-server** to the registry
2. **View it in the Web UI** at localhost:12121
3. **Create an agent wrapper** if you want a complete agent package
4. **Share your MCP server** with others by pushing to a public Docker registry

The Agent Registry provides a centralized way to manage and discover AI capabilities, while Kubernetes provides the production runtime environment!
