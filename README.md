# devops-ai-toolkit

A practical toolkit for DevOps engineers who want AI that actually knows their infrastructure — not a generic assistant that starts from zero every session.

## The idea

Most AI tools are built for software developers. They live in IDEs, autocomplete code, and suggest functions. That's useful for developers, but DevOps engineers work differently.

A DevOps engineer's day is spent in the terminal: checking pod status, reading logs, debugging deployments, managing Helm releases, chasing down flaky CI pipelines. The tools are all command-line first — `kubectl`, `helm`, `ssh`, `git`.

Terminal-native AI agents with full system access map naturally to how infrastructure engineers already work. Instead of switching context to a chat window, you stay in the terminal and let the agent work alongside you — with live access to your cluster, full knowledge of your project, and memory that persists across sessions.

This repo is a practical toolkit built around that idea.

---

## What's inside

### 📖 Knowledge System

The centrepiece of the toolkit. A system for building persistent AI memory — turning a stateless assistant into one that knows your project deeply.

**[→ Read the full guide](docs/knowledge-system.md)**

Key concepts:
- `product.md` — the brain file that auto-loads every session
- A knowledge lookup order that eliminates back-and-forth
- Reusable prompt templates for repeated workflows
- Specialist agents with baked-in domain expertise
- A self-improving loop that gets better every session

### 🔌 MCP Servers

Model Context Protocol servers give your AI agent direct access to your infrastructure — no copy-pasting, no context switching.

| Server | What it does |
|--------|-------------|
| [kubernetes](mcp-servers/kubernetes/) | SSH-based access to a Kubernetes cluster — get pods, read logs, describe resources, check Helm releases |

### 🧠 Skills

Reusable instruction sets that teach the agent how to work with specific tools and workflows. Load a skill and the agent immediately understands the conventions, commands, and best practices.

| Skill | What it covers |
|-------|---------------|
| [kubernetes](skills/kubernetes/) | Navigating clusters, debugging pods, reading logs, working with Helm |

---

## How it fits together

```
Your terminal (Kiro CLI or Claude Code)
        │
        ├── Knowledge System → persistent project memory
        │       ├── product.md     → architecture, rules, tickets
        │       ├── prompts/       → reusable workflow templates
        │       ├── agents/        → specialist domain experts
        │       └── docs/          → deep documentation per topic
        │
        ├── MCP Servers → direct infrastructure access
        │       └── kubernetes MCP → kubectl/helm over SSH
        │
        └── Skills → tool-specific expertise
                └── kubernetes skill → conventions, debugging patterns
```

A typical session: `product.md` loads automatically — the agent already knows your architecture, active tickets, and working rules. The MCP server gives it live access to your cluster. You describe a problem and the agent reads the logs, checks events, and helps you find the root cause — without you copy-pasting anything.

---

## Getting started

### Prerequisites

- [Kiro CLI](https://kiro.dev) or [Claude Code](https://claude.ai/code)
- Python 3.11+ (for MCP server)
- SSH access to a Kubernetes cluster

### 1. Set up the knowledge system

Start with `product.md`. This is the highest-leverage thing you can do:

```bash
mkdir -p ~/.kiro/prompts
cp examples/product.md.template ~/.kiro/product.md
# Edit it to match your project
```

Read the [full knowledge system guide](docs/knowledge-system.md) to understand how to build it out properly.

### 2. Install a skill

```bash
cp -r skills/kubernetes ~/.kiro/skills/
```

### 3. Run the MCP server

```bash
pip install mcp fastmcp
python3 mcp-servers/kubernetes/k8s_mcp_server.py
```

Configure it in `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "k8s-cluster": {
      "command": "python3",
      "args": ["/path/to/k8s_mcp_server.py"],
      "disabled": false
    }
  }
}
```

---

## Contributing

Contributions welcome — especially:
- New MCP servers for common DevOps tools (ArgoCD, Terraform, Grafana, Vault)
- New skills for tools like GitHub Actions, GitLab CI, Datadog
- Improvements to the knowledge system guide based on real usage

## License

MIT
