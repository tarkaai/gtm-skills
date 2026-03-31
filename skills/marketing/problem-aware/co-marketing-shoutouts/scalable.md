---
name: co-marketing-shoutouts-scalable
description: >
  Partner Newsletter Shoutout — Scalable Automation. Automate a portfolio of 20+
  newsletter partners with scheduled placements, blurb delivery, lead routing,
  and performance tracking — all running without manual coordination.
stage: "Marketing > Problem Aware"
motion: "Partnerships & Warm Intros"
channels: "Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 200 clicks and ≥ 15 leads over 2 months"
kpis: ["Impressions", "Click-through rate"]
slug: "co-marketing-shoutouts"
install: "npx gtm-skills add marketing/problem-aware/co-marketing-shoutouts"
drills:
  - partner-pipeline-automation
  - follow-up-automation
  - tool-sync-workflow
---

# Partner Newsletter Shoutout — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Email

## Outcomes

A portfolio of 20+ active newsletter partners with automated placement scheduling, blurb delivery, lead routing, and performance tracking. At least 200 clicks and 15 leads over 2 months. The 10x multiplier at this level comes from: (a) managing more partners simultaneously without proportional effort, (b) reusing proven blurb templates across similar partners, and (c) automating the coordination that was manual at Baseline.

## Leading Indicators

- Partner pipeline converts at ≥30% (prospects contacted → active partners)
- Placement cadence is ≥8 placements/month across the portfolio
- Lead routing from PostHog to Attio happens automatically within 5 minutes of a click
- Per-partner cost per lead remains below $20 (or free if no partner fees)
- Partner retention: ≥70% of partners agree to a second placement
- Time spent on partner coordination drops below 2 hours/week (down from 6+ at Baseline)

## Instructions

### 1. Build the partner pipeline automation

Run the `partner-pipeline-automation` drill to create n8n workflows that automate the full partner lifecycle:

**Partner outreach workflow:**
- Trigger: New partner added to "Newsletter Partners" list in Attio with status "Prospect"
- Automatically send personalized outreach via Instantly using a template that references Baseline results
- Follow up once after 5 days if no response
- Update Attio status on reply detection

**Placement scheduling workflow:**
- Weekly cron checks Attio for partners with upcoming placement dates
- Alerts you if a blurb has not been approved yet
- Auto-sends approved blurbs to partner contacts with the tracked CTA link
- Logs placement confirmations in Attio

**Lead routing workflow:**
- PostHog webhook fires on `co_marketing_click` events
- n8n creates a lead in Attio linked to the specific partner
- Tags the lead with partner source, blurb variant, and placement date

### 2. Scale the partner portfolio

Using the partner research from Baseline, expand to 20+ active partners. Prioritize:
- Partners in the same vertical as your top Baseline performers
- Partners with newsletter audiences >5,000 subscribers
- Partners where Crossbeam shows high account overlap

Use the `follow-up-automation` drill to build automated follow-up sequences for partner prospects who don't respond to initial outreach. Keep the follow-up to 2 touches maximum — partners are collaborators, not cold prospects.

### 3. Templatize blurb production

Create a blurb template library based on Baseline winners:
- Organize templates by angle: curiosity, data-driven, story-driven
- Organize templates by partner audience type: technical, executive, marketing
- Each template has fill-in variables: `{partner_audience_pain_point}`, `{your_specific_benefit}`, `{social_proof_stat}`
- An agent can generate a new blurb from a template in under 2 minutes per partner

Store the template library in Attio or a shared document linked from each partner record.

### 4. Connect all tools

Run the `tool-sync-workflow` drill to ensure data flows bidirectionally:
- PostHog co-marketing events → Attio partner records (clicks, leads, conversion rates)
- Attio partner status changes → n8n workflows (trigger next automation step)
- Instantly outreach events → Attio partner pipeline (track outreach status)
- Loops sequences → partner nurture (keep active partners engaged between placements)

Verify the sync by checking: when a click arrives in PostHog, does the Attio partner record update within 5 minutes?

### 5. Run the scaled program

Execute 8+ placements per month across the portfolio:
- Stagger placements across the month (avoid clustering all placements in one week)
- Rotate blurb variants so the same partner's audience sees different angles
- Track which partners have the best click-to-lead conversion (not just click volume)
- Identify "anchor partners" — the 3-5 partners that consistently generate the most leads

### 6. Evaluate against threshold

After 2 months, measure aggregate results:

**Pass threshold: ≥ 200 clicks AND ≥ 15 leads over 2 months**

- **Pass**: Document the partner portfolio, automation workflows, and per-partner economics. Proceed to Durable.
- **Marginal**: 150-199 clicks or 10-14 leads. Scale is working but conversion needs optimization. Test different landing pages or blurb angles before Durable.
- **Fail**: <150 clicks. Diagnose: Is the partner pipeline too small? Are placements actually running on schedule? Is the blurb quality declining as you scale? Fix the bottleneck and run one more month.

## Time Estimate

- Automation setup (n8n workflows, tool sync): 15 hours
- Partner pipeline expansion (research + outreach): 15 hours
- Blurb template library creation: 5 hours
- Ongoing management (8 weeks × 2 hours/week): 16 hours
- Analysis and optimization: 9 hours

Total: ~60 hours over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| n8n | Workflow automation (partner pipeline, lead routing) | Cloud Starter: ~$24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Partner CRM, lead tracking, pipeline management | Plus: $34/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Event tracking, attribution, analytics | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Instantly | Partner outreach email sequences | Growth: $30/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Loops | Partner nurture sequences | Starter: free up to 1K contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Crossbeam | Partner account overlap mapping | Free tier: 3 seats ([crossbeam.com](https://www.crossbeam.com)) |
| Clay | Partner enrichment (if expanding research) | Launch: $185/mo ([clay.com](https://www.clay.com)) |

**Estimated cost for this level: ~$90-270/mo** (n8n + Attio required; Clay and Instantly optional depending on existing tools)

## Drills Referenced

- `partner-pipeline-automation` — automate partner outreach, scheduling, blurb delivery, and lead routing
- `follow-up-automation` — automated follow-up for unresponsive partner prospects
- `tool-sync-workflow` — connect PostHog, Attio, Instantly, and Loops for bidirectional data flow
