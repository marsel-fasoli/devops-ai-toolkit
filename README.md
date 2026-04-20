devops-ai-toolkit
A collection of MCP servers, Kiro skills, and AI-assisted workflows built for DevOps engineers who live in the terminal.
Philosophy
Most AI coding tools are built for software developers — they autocomplete code, suggest functions, and live inside an IDE. That works well for developers, but DevOps engineers work differently.
A DevOps engineer's day is spent in the terminal: checking pod status, reading logs, debugging deployments, managing Helm releases, navigating CI/CD pipelines. The tools we use — kubectl, helm, ssh, git — are all command-line first.
Terminal-native AI agents with full system access map naturally to how infrastructure engineers already work. Instead of switching context to a chat window, you stay in the terminal and let the AI work alongside you — reading your cluster state, understanding your codebase, and helping you move faster without losing context.
This repo is a practical toolkit built around that idea.
What's inside
MCP Servers
Model Context Protocol (MCP) servers extend AI agents with real tool access. Instead of describing your infrastructure to an AI, you give it direct read access to query it.
ServerWhat it doeskubernetesSSH-based access to a Kubernetes cluster — get pods, read logs, describe resources, check Helm releases
Skills
Skills are reusable instruction sets that teach an AI agent how to work effectively with a specific tool or workflow. Load a skill at the start of a session and the agent immediately understands the tool's conventions, common commands, and best practices.
SkillWhat it coverskubernetesNavigating clusters, debugging pods, reading logs, working with namespaces and Helm
How it fits together
Your terminal (Kiro CLI or Claude Code)
        │
        ├── MCP Servers → direct access to your infrastructure
        │       └── kubernetes MCP → kubectl/helm over SSH
        │
        └── Skills → context about how to work with each tool
                └── kubernetes skill → conventions, commands, debugging patterns
A typical session: you load the Kubernetes skill so the agent understands your environment, and the MCP server gives it live access to query your cluster. You describe a problem — "this pod keeps crashing" — and the agent reads the logs, checks events, and helps you find the root cause without you having to copy-paste anything.
Getting started
Prerequisites

Kiro CLI or Claude Code
Python 3.11+
SSH access to a Kubernetes cluster (for the MCP server)

Using a skill
Copy the skill folder into your .kiro/skills/ directory:
bashcp -r skills/kubernetes ~/.kiro/skills/
Then reference it in your Kiro session or add it to your agent configuration.
Running the MCP server
bashpip install mcp fastmcp
python3 mcp-servers/kubernetes/k8s_mcp_server.py
Configure it in your .kiro/settings/mcp.json:
json{
  "mcpServers": {
    "k8s-cluster": {
      "command": "python3",
      "args": ["/path/to/k8s_mcp_server.py"],
      "disabled": false
    }
  }
}
Contributing
Contributions welcome — especially new skills and MCP servers for common DevOps tools (ArgoCD, Terraform, Grafana, etc.).
License
MIT
