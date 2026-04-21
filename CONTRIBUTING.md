# Contributing

Contributions are welcome — especially new skills and MCP servers for common DevOps tools.

## What to contribute

**New skills** — instruction sets for tools that DevOps engineers use daily:
- CI/CD: GitHub Actions, GitLab CI, ArgoCD, FluxCD
- Infrastructure: Terraform, Ansible, Vault
- Monitoring: Grafana, Datadog, Prometheus
- Code review: GitHub PRs, GitLab MRs

**New MCP servers** — direct AI access to infrastructure tools:
- ArgoCD
- Terraform
- Grafana

**Improvements to existing content** — fixes, additions, better examples

## Guidelines

**For skills:**
- Follow the existing structure — `SKILL.md` and `skill.json` in a named folder under `skills/`
- `SKILL.md` should cover: overview, common commands, debugging patterns, working rules
- Write for LLM consumption — tables and explicit rules work better than prose
- Keep it generic — no company-specific tools or internal URLs
- Test it with a real AI agent before submitting

**For MCP servers:**
- Follow the existing pattern — read-only tools run automatically, write tools require confirmation
- Include a namespace or resource validation check
- Add clear docstrings explaining what each tool does and when to use it
- Keep configuration at the top of the file so it's easy to find

**General:**
- One skill or MCP server per pull request
- Update the README table if you add a new skill or MCP server
- Keep things practical — if you built it for real work, it belongs here

## Structure

```
skills/
└── your-tool/
    ├── SKILL.md      ← Instructions and knowledge
    └── skill.json    ← Metadata (name, description, tags)

mcp-servers/
└── your-tool/
    ├── your_tool_mcp_server.py   ← MCP server
    └── requirements.txt          ← Python dependencies
```
