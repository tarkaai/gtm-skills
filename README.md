# GTM Skills for AI Agents

240 battle-tested GTM plays for B2B startups, packaged as AI agent skills.

Each play covers Marketing, Sales, and Product stages — from a quick **Smoke Test** (validate in a week, free) through **Baseline**, **Scalable**, and **Durable** (agent-driven, continuous improvement). Pick the level that matches where you are.

**Works with:** Claude Code · Cursor · Windsurf · n8n · Any MCP-compatible agent

---

## How it works

**240 plays to run. 40 drills to practice. 25 fundamentals to master.**

The GTM Skills repo is organized in three layers:

- **Plays** (240) — The game plan. Each play tells the agent *what* to do for a specific GTM motion at a specific maturity level (Smoke through Durable). Example: "Cold Email Outreach - Smoke" or "Churn Prevention - Scalable".

- **Drills** (~40) — Practiced routines that make plays work. These are composite workflows that combine multiple tools into a repeatable sequence. Example: `/build-prospect-list` chains Clay enrichment into Attio, `/cold-email-sequence` generates copy and sets up Instantly campaigns.

- **Fundamentals** (~25) — Tool-specific core skills the agent must master. Each one teaches the agent how to use a single tool deeply. Example: Clay enrichment waterfalls, Attio pipeline management, PostHog GTM event schemas.

```
  Plays  →  reference  →  Drills  →  reference  →  Fundamentals
 (240)                    (~40)                      (~25)
  what                  how to                    how to use
  to do                 combine                   each tool
```

When you install a play, the CLI resolves which drills and fundamentals it needs based on your configured stack. Smoke plays pull 2-3 fundamentals. Durable plays pull the full tree.

---

## Install

### Option 1: CLI (Recommended)

```bash
npx gtm-skills install
```

This copies all skills to `~/.claude/skills/` and creates a config file for your stack.

Install selectively:

```bash
# One stage
npx gtm-skills install --stage marketing

# One play (all 4 levels)
npx gtm-skills install --play outbound-founder-email

# One specific level
npx gtm-skills install --play outbound-founder-email --level baseline
```

### Option 2: Claude Code Plugin

Install via Claude Code's built-in plugin system:

```bash
/plugin marketplace add tarkaai/gtm-skills
/plugin install gtm-skills
```

### Option 3: Clone and Copy

Clone the repo and copy the skills folder into your agent's skills directory:

```bash
git clone https://github.com/tarkaai/gtm-skills.git
cp -r gtm-skills/skills/* .agents/skills/
```

### Option 4: Git Submodule

Add as a submodule for easy updates:

```bash
git submodule add https://github.com/tarkaai/gtm-skills.git .agents/gtm-skills
```

Then reference skills from `.agents/gtm-skills/skills/`.

To update later:

```bash
git submodule update --remote .agents/gtm-skills
```

### Option 5: Fork and Customize

1. Fork this repository on GitHub
2. Customize plays for your specific ICP, stack, or motion
3. Clone your fork and point your agent at it

### Option 6: SkillKit (Multi-Agent)

Use [SkillKit](https://github.com/rohitg00/skillkit) to install plays across multiple AI agents (Claude Code, Cursor, Copilot, etc.):

```bash
# Install all plays
npx skillkit install tarkaai/gtm-skills

# Install specific plays
npx skillkit install tarkaai/gtm-skills --skill outbound-founder-email

# List available plays
npx skillkit install tarkaai/gtm-skills --list
```

---

## Configure your stack

On first install you'll be prompted. Or edit `~/.gtm-config.json` directly:

```json
{
  "crm": "attio",
  "automation": "n8n",
  "email_tool": "instantly",
  "enrichment": "clay",
  "linkedin_tool": "dripify",
  "scheduling": "cal.com",
  "analytics": "posthog"
}
```

**CRM options:** `attio` · `salesforce` · `hubspot` · `pipedrive` · `clarify`
**Automation options:** `n8n` · `claude-code` · `make`
**Email options:** `instantly` · `smartlead` · `lemlist` · `loops`
**Enrichment options:** `clay` · `apollo`
**LinkedIn automation:** `dripify` · `expandi` · `waalaxy`

When you run a skill, it references your configured defaults so instructions are specific to your stack, not generic.

---

## How plays are organized

```
skills/
  marketing/
    unaware/          # People who don't know they have a problem
    problem-aware/    # Know the problem, not yet looking for solutions
    solution-aware/   # Comparing options
    product-aware/    # Know your product, evaluating fit
  sales/
    qualified/        # Fits ICP, ready for outreach
    connected/        # Initial contact made
    aligned/          # Fit confirmed, stakeholders engaged
    proposed/         # Proposal delivered, negotiating
    won/              # Closed, transitioning to product
  product/
    onboard/          # New customer getting started
    retain/           # Building habits, preventing churn
    upsell/           # Expansion opportunities
    referrals/        # Turning customers into advocates
    winback/          # Re-engaging churned users
```

Each play folder has four skill files: `smoke.md`, `baseline.md`, `scalable.md`, `durable.md`.

---

## The 4 levels

| Level | Goal | Time | When to use |
|-------|------|------|-------------|
| **Smoke** | Validate the play works | 1 week | Any time you want to test a new play |
| **Baseline** | Prove repeatable results | 2 weeks | After smoke passes |
| **Scalable** | Scale 5–10× with automation | 2 months | After baseline proves out |
| **Durable** | Agent-driven continuous improvement | 6+ months | When you want this play to run itself |

**Rule:** Only move to the next level when the current one passes its threshold. A Smoke that doesn't hit its outcome isn't a failure — it's signal. Iterate the ICP, offer, or channel before spending more.

---

## Budget philosophy

Budgets in these skills show **only play-specific tool costs** — things you buy uniquely for this play. Your CRM and automation platform (n8n, Claude Code) are not included; they're part of your standard stack, paid once.

Most Smoke levels cost nothing. Most Baselines cost under $300/mo. You can run a full outbound engine for under $500/mo.

---

## What's included

- **98 Marketing plays** across Unaware → Product Aware
- **44 Sales plays** across Qualified → Won
- **98 Product plays** across Onboard → Winback
- **Tool meta-skills** in `tools/` for CRM and automation-specific instructions

---

## MCP server

The full playbook is also available as an MCP endpoint for agents that need to discover plays programmatically:

```
https://tarka.ai/api/mcp
```

Tools: `list_plays`, `get_play`, `search_plays`
Resources: `playbook://catalog`, `playbook://play/{slug}`, `playbook://play/{slug}/level/{level}`

---

## Contributing

Skills are generated from the canonical plays data at [tarka.ai/playbook](https://tarka.ai/playbook). To propose a new play or fix, open an issue or PR on this repo.

---

Maintained by [Tarka](https://tarka.ai) · [Browse all plays](https://tarka.ai/playbook) · [MIT License](LICENSE)
