<!-- AgentWeave AI Context v0.1.2 â€” run `agentweave update-template` to update -->
# AI Workflow Context

> This file is deployed by `agentweave init` and versioned with the package.
> Run `agentweave update-template --agent claude` to generate a prompt that
> keeps this file current with new AI capabilities and best practices.

---

## Project Overview

[Replace with: what this project does, who uses it, key workflows, scale expectations]

## Tech Stack

[Replace with: exact versions, package manager, runtime version]

## Essential Commands

[Replace with: dev, test, build, lint â€” all copy-pasteable]

## Architecture

[Replace with: key directories and what belongs in each one]

---

## Code Standards

### Quality
- Never skip tests or disable linting to make the build pass
- Write tests alongside implementation, not as an afterthought
- Keep functions under 50 lines â€” extract helpers when needed
- No `TODO` comments in committed code â€” implement or open a tracked issue

### Security
- NEVER commit `.env` files, API keys, or credentials
- Validate ALL user input at API/system boundaries â€” never trust client data
- Use parameterized queries â€” no string interpolation in SQL
- Sanitize before rendering any user-generated content

### Workflow
- Prefer editing existing files over creating new ones
- Never create new abstractions for single-use operations
- No feature flags, backwards-compat shims, or speculative future-proofing
- Match the style and patterns already established in the codebase

### Token Efficiency
- Use a sub-agent for high-volume operations (test runs, log analysis, doc fetching)
- Summarize command output â€” do NOT dump raw stdout into context
- When context is near full: `/compact` with current phase, modified files, failing tests
- After 2+ failed correction attempts on the same issue: `/clear` and rewrite the prompt

---

## Sub-Agent Setup

Create these in `.claude/agents/` based on project type. Each agent outputs findings
with severity: CRITICAL / HIGH / MEDIUM / INFO.

### Always Create
- `security-reviewer` â€” OWASP Top 10, auth flows, secrets exposure, injection risks
- `qa-engineer` â€” edge case tests, acceptance criteria validation
- `code-reviewer` â€” maintainability, complexity, naming, style (read-only tools)

### Create If the Project Has a UI
- `ux-reviewer` â€” WCAG 2.1 AA, UX copy clarity, flow logic

### Create If the Project Has a Database
- `db-specialist` â€” schema design, indexes, migration safety, query efficiency

### Create If the Project Has a Public API
- `api-designer` â€” REST/GraphQL conventions, versioning, error responses

### Create If the Project Will Be Deployed
- `devops-reviewer` â€” CI/CD config, Dockerfile, env var handling, secrets management

### Always Use Your Agents

Creating agents is only step one. **Invoke them every time their scope applies — never create and forget:**
- `security-reviewer` — run before every commit or PR, and after any auth/input-handling change
- `qa-engineer` — run after implementing any feature or fixing any bug
- `code-reviewer` — run on every non-trivial change before marking a task complete
- Specialty agents (`ux-reviewer`, `db-specialist`, etc.) — run whenever their domain is touched

If an agent exists and is relevant, using it is not optional.

---

## Multi-Agent Workflow (AgentWeave)

If `.agentweave/session.json` exists, you are in multi-agent mode.

**On every session start:**
1. Read `.agentweave/AGENTS.md` â€” collaboration guide and full command reference
2. Read `.agentweave/shared/context.md` â€” current project state and your task
3. Run `agentweave status` to see pending work (via Bash â€” do not ask user to run it)

**Rule: run all `agentweave` CLI commands via Bash automatically.**
Never ask the user to run CLI commands. They only paste relay prompts.

### When You Are Principal

**ALWAYS enter plan mode before any non-trivial implementation task:**
- Use `EnterPlanMode` to design your approach before writing or delegating
- Present the plan for user approval, then implement or delegate to other agents
- No exceptions: plan first, code second — even for tasks that seem straightforward

### Delegating to Kimi

```bash
agentweave quick --to kimi "[task description]"
agentweave relay --agent kimi
```

Show the relay prompt output to the user to paste into Kimi Code.

### When User Says "Kimi Is Done"

```bash
agentweave inbox --agent claude
agentweave summary
```

Review Kimi's work and continue without user input.

### Cross-Agent Sub-Agent Requests

Write `.agentweave/shared/agent-request-[topic].md`, then tell user:
"Tell Kimi to check `.agentweave/shared/` for a new request from Claude"

---

## When Compacting

[Replace with: current phase, modified files, failing tests, active AgentWeave task IDs]
