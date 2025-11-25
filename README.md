# Kagent Helm Kind

A comprehensive guide for setting up a local Kagent cluster on Kind (Kubernetes in Docker) with MCP server development and agent registry integration.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
  - [Building a Kind Kagent Cluster](#building-a-kind-kagent-cluster)
  - [Building MCP Servers](#building-mcp-servers)
  - [Using the Agent Registry](#using-the-agent-registry)
- [Project Structure](#project-structure)
- [Additional Resources](#additional-resources)
- [Contributing](#contributing)

## Overview

This repository contains everything you need to:

1. **Build a local Kagent cluster** using Kind with proper networking and registry configuration
2. **Develop and deploy MCP (Model Context Protocol) servers** for extending agent capabilities
3. **Publish and manage agents** using the Agent Registry

Kagent is an AI agent platform that runs on Kubernetes, enabling you to deploy and manage AI agents with enterprise-grade infrastructure.

## Prerequisites

Before getting started, ensure you have the following installed:

- **Docker Desktop** (or equivalent Docker runtime)
- **kubectl** - Kubernetes CLI
- **helm** - Kubernetes package manager
- **kind** - Kubernetes in Docker
- **cloud-provider-kind** - LoadBalancer support for Kind (install with `brew install cloud-provider-kind` and run with `sudo cloud-provider-kind`)
- **arctl** - Agent Registry CLI (installation instructions in [registry documentation](./registry/README.md))
- **Python 3.12+** - For MCP server development
- **uv** - Modern Python package manager (recommended for MCP development)

### Installing Prerequisites with Homebrew

```bash
# Install core tools
brew install kubectl helm kind cloud-provider-kind

# Install Python package manager (optional, for MCP development)
pip install uv
```

### Running cloud-provider-kind

The `cloud-provider-kind` service provides LoadBalancer IP addresses for Kind clusters:

```bash
# Start cloud-provider-kind (requires sudo)
sudo cloud-provider-kind

# This should be running in a separate terminal while using the cluster
# It will automatically assign LoadBalancer IPs to services
```

### Environment Variables

You'll need API keys for your AI providers:

```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export XAI_API_KEY="your-xai-api-key"  # Optional: for xAI/Grok integration
export OPENAI_API_KEY="your-api-key-here" # Optional: for OpenAI integration
```

Add these to your `~/.zshrc` or `~/.bashrc` to persist them.

## Quick Start

### 1. Create the Kind Cluster

```bash
cd build
./setup-kind-cluster.sh
```

This will:
- Create a Kind cluster with the name `kagent-demo`
- Configure a local Docker registry on port 5001
- Set up networking for LoadBalancer services (using MetalLB)

### 2. Install Kagent

```bash
# Install CRDs
helm install kagent-crds oci://ghcr.io/kagent-dev/kagent/helm/kagent-crds \
    --namespace kagent \
    --create-namespace

# Install Kagent with Anthropic provider
helm install kagent oci://ghcr.io/kagent-dev/kagent/helm/kagent \
    --namespace kagent \
    --set providers.default=anthropic \
    --set providers.anthropic.model="claude-3-5-sonnet-20241022" \
    --set providers.anthropic.apiKey=$ANTHROPIC_API_KEY 
```

### 3. Access the Kagent UI

```bash
# Expose UI via LoadBalancer
kubectl patch svc kagent-ui -n kagent -p '{"spec": {"type": "LoadBalancer"}}'

# Get the UI URL
kubectl get svc kagent-ui -n kagent
```

### 4. Build and Deploy Your First MCP Server

```bash
cd mcp-servers/datetime-server

# Build the MCP server Docker image
kmcp build --project-dir . -t datetime-server:latest

# Deploy to Kubernetes
kubectl apply -f datetime-server-deployment.yaml
kubectl apply -f datetime-agent-deployment.yaml
```

## Documentation

### Building a Kind Kagent Cluster

📖 **[Complete Cluster Setup Guide](./build/README.md)**

The `build/` directory contains:
- **[kind-config.yaml](./build/kind-config.yaml)** - Kind cluster configuration with registry and networking
- **[setup-kind-cluster.sh](./build/setup-kind-cluster.sh)** - Automated cluster creation script
- **[README.md](./build/README.md)** - Detailed setup instructions and troubleshooting

**Key Features:**
- Local Docker registry on port 5001
- MetalLB for LoadBalancer support
- Port mappings for HTTP (80), HTTPS (443), and registry (5001)
- Multi-node cluster support

### Building MCP Servers

📖 **[MCP Server Development Guide](./mcp-servers/README.md)**

The `mcp-servers/` directory contains example MCP servers and development documentation:

**Example: DateTime Server**
- **[README.md](./mcp-servers/datetime-server/README.md)** - Complete server documentation
- **[QUICKSTART.md](./mcp-servers/datetime-server/QUICKSTART.md)** - Get started in 5 minutes
- **[DEPLOYMENT.md](./mcp-servers/datetime-server/DEPLOYMENT.md)** - Kubernetes deployment guide

**What You'll Learn:**
- Creating MCP servers with Python and FastMCP
- Implementing tools that agents can use
- Building and testing Docker images locally
- Deploying MCP servers to Kubernetes
- Creating agent manifests that use your MCP servers

### Using the Agent Registry

📖 **[Agent Registry Guide](./registry/README.md)**

The `registry/` directory contains documentation for publishing and managing agents:

**Key Concepts:**
- Publishing MCP servers to the registry
- Creating and publishing complete agents
- Version management and discovery
- Deploying agents from the registry

**Common Commands:**
```bash
# List MCP servers in registry
arctl mcp list

# Publish an MCP server
arctl mcp publish ./mcp-servers/datetime-server

# Deploy an agent from registry
arctl agent deploy datetime-agent
```

## Project Structure

```
kagent-helm-kind/
├── README.md                       # This file - main documentation
├── build/                          # Kind cluster setup
│   ├── README.md                   # Cluster setup guide
│   ├── kind-config.yaml            # Kind cluster configuration
│   └── setup-kind-cluster.sh       # Cluster creation script
├── mcp-servers/                    # MCP server examples and development
│   ├── README.md                   # MCP development guide
│   └── datetime-server/            # Example datetime MCP server
│       ├── README.md               # Server documentation
│       ├── QUICKSTART.md           # Quick start guide
│       ├── DEPLOYMENT.md           # Deployment guide
│       ├── Dockerfile              # Container image
│       ├── kmcp.yaml              # MCP configuration
│       ├── pyproject.toml         # Python dependencies
│       ├── src/                   # Server source code
│       └── tests/                 # Unit tests
├── registry/                       # Agent registry documentation
│   └── README.md                   # Registry usage guide
├── agent_registry_guide.md         # Detailed registry tutorial
└── blog_kubernetes_mcp_agents.md   # Conceptual overview blog post
```

## Additional Resources

### Conceptual Guides

- **[Kubernetes MCP Agents Blog](./blog_kubernetes_mcp_agents.md)** - Deep dive into the architecture and concepts
- **[Agent Registry Tutorial](./agent_registry_guide.md)** - Step-by-step registry usage with examples

### Official Documentation

- [Kagent Documentation](https://docs.kagent.dev)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [Kind Documentation](https://kind.sigs.k8s.io)
- [Agent Registry](https://github.com/agentregistry-dev/agentregistry)

## Contributing

Contributions are welcome! Here's how you can help:

1. **Add new MCP server examples** - Share your custom MCP servers
2. **Improve documentation** - Fix typos, add clarifications, create tutorials
3. **Report issues** - Found a bug? Let us know
4. **Share configurations** - Different Kind setups, Helm values, etc.

### Development Workflow

```bash
# Clone the repository
git clone https://github.com/sebbycorp/kagent-helm-kind.git
cd kagent-helm-kind

# Create a new branch
git checkout -b feature/your-feature-name

# Make your changes

# Test your changes
# (Build cluster, deploy MCP servers, etc.)

# Commit and push
git add .
git commit -m "Description of changes"
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- **Issues**: Please use [GitHub Issues](https://github.com/sebbycorp/kagent-helm-kind/issues)
- **Discussions**: Join the conversation in [GitHub Discussions](https://github.com/sebbycorp/kagent-helm-kind/discussions)
- **Documentation**: Check the individual README files in each directory

---

**Happy Building! 🚀**

Built with ❤️ for the Kagent and MCP community.
