---
name: competitive-objection-handling-scalable
description: >
  Competitive Objection Handling — Scalable Automation. Address "we're evaluating competitor X" objections by differentiating your solution, highlighting unique value, and leveraging competitive intelligence, from manual battlecards to AI-driven competitive positioning that adapts to each prospect's priorities and decision criteria.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "75 hours over 2 months"
outcome: ">=45% win rate in competitive deals over 2 months"
kpis: ["Competitive win rate by competitor", "Battlecard currency", "Proactive positioning rate", "Win/loss insight quality"]
slug: "competitive-objection-handling"
install: "npx gtm-skills add sales/aligned/competitive-objection-handling"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Competitive Objection Handling — Scalable Automation

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Address "we're evaluating competitor X" objections by differentiating your solution, highlighting unique value, and leveraging competitive intelligence, from manual battlecards to AI-driven competitive positioning that adapts to each prospect's priorities and decision criteria.

**Time commitment:** 75 hours over 2 months
**Pass threshold:** >=45% win rate in competitive deals over 2 months

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing, scaled):** ~$100–200/mo
- **Clay (enrichment + AI personalization):** ~$150–400/mo
- **LinkedIn Sales Navigator (prospecting, optional):** ~$100/mo

_Total play-specific: ~$100–400/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Fireflies** (Sales Engagement)

---

## Instructions

1. Scale to 50+ competitive deals per quarter; integrate competitive intelligence tools (Klue, Crayon) with Attio to auto-update battlecards when competitors release features, change pricing, or announce customers.

2. Build an n8n workflow that triggers when competitive objection is detected in call recording: identify competitor mentioned, pull relevant battlecard from Attio, send to rep with recommended positioning, log in PostHog.

3. Create persona-specific competitive positioning: CFO cares about TCO (show pricing comparison), CTO cares about architecture (show technical differentiation), VP Sales cares about ease-of-use (show setup time comparison).

4. Set up PostHog to track competitive intelligence: which competitors appear most often? in which deal sizes/industries? at which stage do they enter evaluation? Use patterns to position proactively.

5. Build a competitive content library: comparison pages, switch guides ("Migrating from X to us"), ROI calculators with competitor TCO, head-to-head demo videos; auto-recommend content based on competitor and persona.

6. Implement proactive competitive positioning: if PostHog shows competitor X appears in 60% of deals, address them upfront in discovery or demo before prospect mentions them.

7. Create competitive win/loss tracking: for every closed deal, log whether competitors were involved, who was chosen, and why; feed learnings back into battlecards.

8. Build a competitive intelligence dashboard in PostHog showing win rate by competitor, most common decision criteria, and which differentiators correlate with wins.

9. Each week, review competitive losses to understand why: did competitor have must-have feature? better pricing? stronger champion? Update battlecards and positioning based on loss analysis.

10. After 2 months, if win rate >=45% in competitive deals and battlecards are kept current via automated intel, move to Durable; otherwise refine positioning or improve win/loss analysis process.

---

## KPIs to track
- Competitive win rate by competitor
- Battlecard currency
- Proactive positioning rate
- Win/loss insight quality

---

## Pass threshold
**>=45% win rate in competitive deals over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/competitive-objection-handling`_
