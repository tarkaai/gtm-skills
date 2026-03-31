# GTM Skills — Claude Code Configuration

## What this repo is

This is a collection of GTM (go-to-market) play skills for B2B startups. Each skill guides you through a specific play at a specific maturity level (Smoke → Baseline → Scalable → Durable).

## Reading the user's stack config

Before running any skill, read `.gtm-config.json` in the project root (or `~/.gtm-config.json` globally). This file defines the user's default tools:

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

Throughout skill instructions, replace references to tool categories with the user's configured tool. For example, if `crm` is `salesforce`, every CRM step should reference Salesforce fields, objects, and workflows — not generic CRM language.

If no config exists, prompt the user: "It looks like you haven't configured your GTM stack yet. Run `npx gtm-skills init` or tell me your CRM and automation platform and I'll proceed with those."

## Skill structure — Plays, Drills & Fundamentals

Skills are organized in three layers:

- **Plays** (240) at `skills/{stage}/{sub-stage}/{play-slug}/{level}.md` — what to run. Each play references drills and fundamentals instead of giving vague instructions.
- **Drills** (~196) at `drills/{category}/{drill-name}.md` — practiced routines that combine multiple tools into reusable workflows (e.g., `/build-prospect-list`, `/cold-email-sequence`). Organized into 12 categories: prospecting, outreach, content, events, paid, partnerships, measurement, activation, engagement, monetization, sales-process, advocacy.
- **Fundamentals** (~25) at `skills/fundamentals/{category}/{tool}/SKILL.md` — tool-specific core skills the agent must master (e.g., Clay enrichment, Attio pipeline management).

Each play file contains:
- Frontmatter: name, description, stage, motion, level, time, outcome, kpis
- Play-specific tool costs (not CRM/automation — those are standard)
- Step-by-step instructions referencing drills and fundamentals
- Pass/fail threshold
- KPIs to track

## How to run a skill

When a skill is invoked:
1. Read the user's `.gtm-config.json`
2. Substitute tool names throughout the instructions
3. Where instructions say "in your CRM", use the user's configured CRM
4. Where instructions say "set up automation", use the user's automation platform
5. Execute each step, checking in with the user at decision points
6. Track KPIs in PostHog (or the user's analytics tool)
7. At the end, evaluate against the pass threshold and recommend next steps

## Meta-skills (legacy) and Fundamentals

`tools/crm/` and `tools/automation/` contain legacy meta-skills. These are being migrated to `skills/fundamentals/`. When a skill requires CRM work, check for a matching fundamental first, then fall back to the tools/ meta-skills:
- Attio: read `tools/crm/attio.md`
- Salesforce: read `tools/crm/salesforce.md`
- HubSpot: read `tools/crm/hubspot.md`
- Pipedrive: read `tools/crm/pipedrive.md`
- Clarify: read `tools/crm/clarify.md`

## Level progression

Never skip levels. If a user asks to run a Scalable skill but hasn't run Baseline, remind them: "Scalable assumes you've proven the play at Baseline. Do you have Baseline results to reference? If so, share them and we'll proceed. If not, start with the Baseline skill first."

## Budget guidance

Play-specific budgets shown in skills are estimates for the unique tools that play requires. They do not include:
- CRM cost (standard stack)
- Automation platform cost (standard stack)
- PostHog cost (free tier covers most use cases)

Smoke levels should cost nothing or close to it. Push back if the user wants to spend heavily before validating.
