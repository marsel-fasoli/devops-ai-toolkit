# @find-doc

Use this prompt to quickly locate the right documentation file for a topic,
instead of searching through all files manually.

## How to use

Run this prompt with a topic keyword:
> @find-doc kubernetes
> @find-doc deployment
> @find-doc ticket PROJ-101

## What I will do

1. Check the Documentation Index in product.md for a matching file
2. If found — tell you exactly which file covers that topic and open it
3. If not found — search the docs/ folder for relevant content
4. If still not found — tell you honestly that the documentation doesn't exist yet

## Maintaining this index

The Documentation Index in product.md should be updated every time a new file is created.
Run @update-docs at the end of each session to keep it current.

---

## Documentation Index

> Copy this section into your product.md and update it as you add files.
> This is the master index — keep it accurate.

```markdown
## Documentation Index

| Topic | File | What it covers |
|-------|------|---------------|
| Architecture | docs/architecture.md | System components, data flow, integration points |
| Deployment | docs/deployment.md | How to deploy, rollback, and verify each service |
| Troubleshooting | docs/troubleshooting.md | Known failure patterns and fixes |
| Monitoring | docs/monitoring.md | Dashboards, alerts, how to read metrics |
| [Your topic] | docs/[your-file].md | [What it covers] |
```
