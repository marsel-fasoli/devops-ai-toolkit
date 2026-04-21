# Building a Persistent AI Knowledge System for DevOps

## The Problem

AI assistants are stateless. Every new conversation starts from zero — they don't know your project, your architecture, your team's conventions, or what you tried last week. This means:

- You waste time re-explaining context every session
- The AI gives generic advice instead of project-specific help
- Mistakes get repeated because there's no memory of past investigations
- The AI can't build on previous work

## The Solution

A hand-curated knowledge base — a folder of structured markdown files that gets loaded as context every session. This turns a generic AI into one that knows your project deeply.

The system has five components that work together: a brain file, detailed documentation, reusable prompts, ticket investigation folders, and specialist agents. Each one solves a different part of the problem.

---

## Architecture

```
~/.ai-knowledge/
├── .kiro/
│   ├── product.md              ← THE BRAIN — auto-loaded every session
│   ├── prompts/                ← Reusable workflow templates
│   │   ├── find-doc.md         ← Topic → file index
│   │   ├── update-docs.md      ← End-of-session doc refresh
│   │   ├── tickets.md          ← Active tickets grouped by status
│   │   ├── ticket-refresher.md ← Deep dive on a specific ticket
│   │   ├── analyze-logs.md     ← Log analysis with error categorization
│   │   └── new-deployment.md   ← Deploy a new environment from zero
│   ├── agents/
│   │   └── log-analyst.json    ← Specialist agent with domain expertise
│   └── settings/
├── docs/                       ← Detailed documentation files
├── PROJ-XXXX/                  ← Per-ticket investigation history
├── logs/                       ← Log files for analysis
├── screenshots/                ← Visual evidence
└── scripts/                    ← Helper scripts
```

---

## Component 1: product.md — The Brain

The single most important file. Auto-loaded every session. Everything else is secondary.

### What it contains

**Knowledge lookup order** — the most critical section. Defines the exact steps the AI follows before asking you anything:

```markdown
## Knowledge Lookup Order (CRITICAL — NEVER REMOVE FROM CONTEXT)

When you don't know something or aren't sure:

1. Check this file (product.md) — covers architecture, locations, workflows, rules
2. Run @find-doc to locate the relevant documentation file
3. Read the detailed documentation file in full
4. Check actual source code or config files on disk
5. Only then ask the user — never guess or make assumptions

After getting the answer: update product.md so it's available next session.
Every time you have to ask something you should have known, that's a signal to add it here.
```

This single rule eliminates most of the back-and-forth that makes AI assistants frustrating.

**Architecture overview** — components, ports, namespaces, storage, execution flow. Written as a reference table, not prose.

**Deployment locations** — exact paths for everything. Where charts live, where configs go, what scripts exist and how to run them.

**Working style rules** — hard constraints the AI must never violate:

```markdown
## Working Style Rules

- NEVER commit or push — user handles all git operations
- NEVER run destructive commands without showing the command first and waiting for approval
- NEVER deploy to production without explicit confirmation
- ALWAYS show proposed changes before applying them
- Read-only operations (get, describe, logs, cat, grep) are fine without asking
- When stuck: ask, never guess
- Complete logs only — save full log files, analyze entirely, never work from snippets
- Update documentation as we work — capture new knowledge immediately
- For every new ticket or issue — create a folder immediately when work begins, not after it's resolved. An empty folder with just an investigation file started is better than no folder at all
- For every new topic that grows too large for product.md — create a dedicated file in docs/
```

**Active tickets** — current status of every open issue:

```markdown
## Active Tickets

| Ticket   | Description                    | Status      | Blocked on         |
|----------|--------------------------------|-------------|--------------------|
| PROJ-101 | Memory leak in service A       | In progress | —                  |
| PROJ-102 | Database version upgrade       | Blocked     | Maintenance window |
| PROJ-103 | CI pipeline flaky test         | ✅ Closed   | —                  |
```

**Prompt auto-suggest rules** — tells the AI when to suggest each prompt:

```markdown
## Prompt Auto-Suggest Rules

When I recognize a situation that matches a prompt, suggest it:
"💡 This looks like a good time to run @analyze-logs."
Don't run it automatically — just suggest it.

| Prompt              | Suggest when...                                    |
|---------------------|----------------------------------------------------|
| @analyze-logs       | User shares logs or mentions an error              |
| @tickets            | User asks "what are we working on"                 |
| @ticket-refresher   | User mentions a specific ticket number             |
| @update-docs        | Session is ending or significant new info learned  |
| @new-deployment     | User wants to set up a new environment             |
```

**System improvement rule** — the AI flags workflow improvements during normal work without interrupting:

```markdown
## System Improvement Rule

During normal work, if you notice:
- Information you had to ask the user that should have been in product.md
- A manual step repeated more than twice that could become a prompt
- A doc that has grown too large and should be split
- Stale information that no longer matches reality

Flag it with: "💡 System improvement idea: [description]"
Don't interrupt the current task — just note it so we can decide later.
```

**The golden rule:** if the AI had to ask about something it should have known, add it to `product.md`.

---

## Component 2: Detailed Documentation

Each file covers one domain in depth. One topic per file. Written for LLM consumption — tables and explicit rules, not prose.

**Create a new file immediately when a topic grows too large for product.md or when a new domain is first investigated — don't wait until the end. A short file with just the basics is better than no file at all.**

| Domain | What to document |
|--------|-----------------|
| Architecture | System components, data flow, integration points |
| Infrastructure | Cluster setup, networking, storage layout |
| Deployment | How to deploy, rollback, and verify each service |
| Monitoring | Dashboards, alerts, how to read metrics |
| Troubleshooting | Known failure patterns, fixes that worked, what to check first |
| Investigations | Completed bug investigations with full context and root cause |

The `@find-doc` prompt acts as an index — it maps topic keywords to the right file so the AI knows where to look without grepping everything.

---

## Component 3: Prompts — Reusable Workflows

Instead of explaining the same task every time, prompt templates give the AI a structured procedure. Anything you explain more than twice should become a prompt.

| Prompt | What it does | Auto-suggested when... |
|--------|-------------|----------------------|
| `@analyze-logs` | Parses log files, categorizes failures, identifies root cause | User shares logs or mentions an error |
| `@tickets` | Shows open tickets grouped by blocked vs actionable | User asks "what are we working on" |
| `@ticket-refresher` | Deep dive on a specific ticket with full investigation context | User mentions a ticket number |
| `@update-docs` | End-of-session cleanup — fix stale info, propose new prompts | Session is ending |
| `@find-doc` | Maps a topic keyword to the right documentation file | AI needs to look something up |
| `@new-deployment` | Full deployment from zero with verification steps | User wants to set up a new environment |

### Example prompt file

```markdown
# @analyze-logs

When triggered:

1. Ask the user for the log file path or paste
2. Scan the ENTIRE file — never just the last 50 lines
3. Identify all error types and categorize them
4. Find the FIRST occurrence of each error — root cause is usually early, not late
5. Build a timeline of key events with timestamps
6. Compare with any previous investigation in the relevant ticket folder
7. Provide: root cause hypothesis, affected components, recommended next step
8. Save the analysis to the relevant ticket folder as investigation notes
```

---

## Component 4: Ticket Folders — Investigation History

Each issue gets its own folder. **Create it immediately when work begins — not after the issue is resolved.** An empty folder with just an investigation file started is better than no folder at all.

When a ticket comes back up weeks later, the AI picks up exactly where you left off — no re-explaining.

```
PROJ-101/
├── PROJ-101_investigation.md   ← Notes, root cause hypothesis, timeline
├── logs.tar.gz                 ← Captured log files
├── screenshot_error.png        ← Visual evidence
└── draft_response.txt          ← Communication draft for stakeholders
```

The investigation file should include:
- When the issue was first reported
- What was tried and what didn't work
- The root cause once identified
- The fix applied and how it was verified
- Who was involved (as roles, not names)

---

## Component 5: Specialist Agents

Agents go beyond prompts — they are persistent specialist personas with deep domain knowledge baked in. Where a prompt gives the AI a procedure, an agent gives it expertise.

A well-designed agent includes:

- **Domain context** — what system it's analyzing, what the components are, how they interact
- **Log formats** — exact patterns to look for in each log type
- **Known issues** — current open bugs and their symptoms
- **Analysis approach** — the exact reasoning chain to follow
- **Working style** — how to present findings (timelines, tables, evidence with line numbers)

### Example agent definition

```json
{
  "name": "log-analyst",
  "description": "Infrastructure log analysis specialist",
  "prompt": "You are a log analysis specialist for a microservices platform running on Kubernetes.\n\n## Log Formats\n- Service A: `YYYY-MM-DD HH:mm:ss,SSS LEVEL thread class : message`\n- Service B: `YYYY-MM-DD HH:mm:ss,SSS LEVEL class [thread] message`\n\n## Key Patterns\n- Operation IDs (UUID format) — track a single operation across all logs\n- Status transitions: PENDING → RUNNING → SUCCESS/FAILED\n- Connection refused — which service, which port, how many retries\n- Timeout patterns — distinguish client timeout from server timeout\n\n## Known Issues\n- PROJ-101 (OPEN): Memory leak in service A under high load\n- PROJ-102 (OPEN): Flaky connection between service B and database\n\n## Analysis Approach\n1. Identify the operation ID(s) involved\n2. Trace the operation across all available logs\n3. Build a timeline with exact timestamps\n4. Find the FIRST error — root cause is usually early\n5. Distinguish expected behavior from actual bugs\n6. Always show evidence with timestamps and line numbers\n\n## Working Style\n- Never assume — verify from log data\n- Use tables for comparisons\n- Show exact log excerpts as evidence",
  "tools": ["fs_read", "grep", "glob"],
  "keyboardShortcut": "ctrl+shift+l",
  "welcomeMessage": "Log analyst ready. Share the log files and describe what you're investigating."
}
```

The key difference from a prompt: the agent carries this expertise into every interaction automatically. Activate it when doing a focused investigation session.

---

## How It Works In Practice

### Session start
1. `product.md` auto-loads — AI immediately knows the project, the rules, the current tickets
2. User asks a question or gives a task
3. AI follows the lookup order: `product.md` → `@find-doc` → detailed docs → source code → ask

### During work
- AI follows working style rules without being reminded
- AI uses skills to interact with Jira, CI/CD, and code review tools directly
- AI suggests relevant prompts when it recognizes the situation
- AI flags system improvement opportunities without interrupting

### Session end
- Run `@update-docs` — captures new knowledge, fixes stale info, proposes new prompts
- Next session starts with updated knowledge

---

## The Self-Improving Loop

```
Session work
    │
    ├── AI notices something to improve → "💡 System improvement idea: ..."
    │
    └── Session ends → @update-docs
            │
            ├── Fix stale information
            ├── Add new knowledge to product.md
            ├── Propose new prompts for repeated workflows
            └── Next session is better than the last
```

This is what separates a knowledge base that stays useful from one that goes stale.

---

## Backup Strategy

The knowledge base IS the value. Back it up to at least two independent locations.

```bash
# Add to crontab (crontab -e)
# Every Sunday at 2 AM
0 2 * * 0 tar -czf ~/ai-knowledge-backup.tar.gz ~/.ai-knowledge/ && \
          scp ~/ai-knowledge-backup.tar.gz user@remote-server:~/ai-knowledge-backup.tar.gz

# Restore
cd ~ && tar xzf ~/ai-knowledge-backup.tar.gz
```

---

## The Difference

| Without the system | With the system |
|---|---|
| "What namespace should I use?" | AI already knows |
| 5 minutes explaining the architecture | AI already knows the full stack |
| "We tried this last week and it failed" | AI reads the investigation doc |
| "Can you check the CI pipeline?" | AI has the skill, checks directly |
| "Don't push to master!" | Rule is in product.md, AI never does it |
| Generic advice | Knows your specific setup and conventions |
| Forgets everything next session | Picks up exactly where you left off |
| Same manual steps every time | `@prompt-name` and it's done |
| AI never improves | AI suggests system improvements as it works |

---

## How To Build This For Your Project

Start small. Don't try to document everything upfront — the system grows organically.

**Day 1:**
1. Create `.kiro/product.md` with architecture, key paths, and working style rules
2. Add the knowledge lookup order — this is the single most important thing
3. Add the system improvement rule
4. Copy `examples/prompts/update-docs.md` into your `.kiro/prompts/` folder and run it at the end of this first session — this is not optional, it is the habit that makes everything else work

**Week 1-2:**
5. Create a `@find-doc` prompt as your documentation grows
6. Add a prompt for your most common repeated workflow
7. Let ticket folders grow naturally as you work on issues

**Ongoing:**
8. Every time the AI asks something it should have known — add it to `product.md`
9. Every workflow you explain twice — turn it into a prompt
10. Every investigation you complete — document it in the ticket folder
11. Every single session — run `@update-docs`

The investment is small — maybe 10 minutes per session. The payoff compounds: after a couple of months, the AI knows your project better than a new team member would after weeks of onboarding.

**The key insight:** the AI is only as good as the context you give it. Make that context persistent.
