---
name: linkedin-founder-threads-scalable
description: >
  Founder LinkedIn content — Scalable Automation. Founder-led LinkedIn posts and short video with clear CTAs to build awareness and inbound leads, from a one-week smoke test through scaled content and agent-driven optimization that sustains or improves lead volume over time.
stage: "Marketing > Unaware"
motion: "Founder Social Content"
channels: "Social"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 20 inbound leads over 2 months"
kpis: ["Impressions", "Engagement rate", "Profile visits", "CTA clicks"]
slug: "linkedin-founder-threads"
install: "npx gtm-skills add marketing/unaware/linkedin-founder-threads"
drills:
  - social-content-pipeline
  - blog-seo-pipeline
  - content-repurposing
  - newsletter-pipeline
  - posthog-gtm-events
---
# Founder LinkedIn content — Scalable Automation

> **Stage:** Marketing → Unaware | **Motion:** Founder Social Content | **Channels:** Social

## Overview
Founder-led LinkedIn posts and short video with clear CTAs to build awareness and inbound leads, from a one-week smoke test through scaled content and agent-driven optimization that sustains or improves lead volume over time.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** ≥ 20 inbound leads over 2 months

---

## Budget

**Play-specific tools & costs**
- **Taplio (LinkedIn scheduling + AI assist):** ~$50/mo
- **Buffer or Typefully (cross-platform scheduling):** ~$10–20/mo

_Total play-specific: ~$10–50/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **LinkedIn** (Channel)
- **Taplio** (Analytics)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Typefully** (Channel)
- **Buffer** (Channel)
- **Loom** (Video)
- **Descript** (Video)
- **LinkedIn Sales Navigator** (Channel)

---

## Instructions

1. Set volume target: 5–10x Baseline post output (e.g. 15–20 posts over 2 months) and aim for ≥ 20 inbound leads over 2 months; keep content format and CTA consistent with Baseline.

2. Create a content calendar in a spreadsheet or tool (e.g. Taplio, Notion) with topics, hooks, and publish dates; batch-write posts where possible to save time.

3. Connect LinkedIn (via Taplio or native export) and your landing page or CRM to PostHog so every lead (DM, form fill) is logged with source "LinkedIn" and timestamp.

4. In n8n, build a workflow triggered by PostHog when a lead event fires: e.g. send a Slack notification, add lead to CRM, or trigger a follow-up email so no lead sits more than 24 hours.

5. Publish on schedule; use scheduling in LinkedIn or a tool to maintain consistency without daily manual posting.

6. Each week, record impressions, engagement rate, profile visits, and new leads in PostHog; compute running lead count and compare to target (≥ 20 over 2 months).

7. Keep lead rate within 20% of Baseline (e.g. if Baseline was 5 leads per 2 weeks, Scalable should yield at least 4 leads per 2 weeks on average).

8. If lead volume or engagement drops, pause scaling and test one variable (e.g. post length, CTA copy) before adding more volume.

9. At the end of 2 months, confirm total leads ≥ 20 and that follow-up and conversion to meetings are tracked in PostHog and CRM.

10. If metrics hold, document the content system and hand off to Durable for agent-driven optimization; if not, refine content or targeting before Durable.

---

## KPIs to track
- Impressions
- Engagement rate
- Profile visits
- CTA clicks

---

## Pass threshold
**≥ 20 inbound leads over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/unaware/linkedin-founder-threads`_
