---
name: discovery-based-demo-baseline
description: >
  Discovery-Based Demo — Baseline Run. Tailor product demos to pain points uncovered in discovery to maximize relevance and engagement, from manual demo customization to AI-driven dynamic demos that auto-adapt based on prospect signals and deliver personalized value narratives.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Baseline Run"
time: "22 hours over 2 weeks"
outcome: ">=70% demo-to-nextstep conversion and >=40% demo-to-proposal conversion over 2 weeks"
kpis: ["Demo-to-nextstep conversion", "Demo-to-proposal conversion", "Demo engagement score", "Recap video view rate"]
slug: "discovery-based-demo"
install: "npx gtm-skills add sales/aligned/discovery-based-demo"
---
# Discovery-Based Demo — Baseline Run

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Overview
Tailor product demos to pain points uncovered in discovery to maximize relevance and engagement, from manual demo customization to AI-driven dynamic demos that auto-adapt based on prospect signals and deliver personalized value narratives.

**Time commitment:** 22 hours over 2 weeks
**Pass threshold:** >=70% demo-to-nextstep conversion and >=40% demo-to-proposal conversion over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Apollo (includes dialer) or Aircall:** ~$50–100/mo
- **Intercom or Loops (in-app/email triggers):** ~$75–150/mo

_Total play-specific: ~$50–150/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **Loom** (Video)

---

## Instructions

1. Expand to 10-15 demos over 2 weeks; build a demo playbook in Attio with pain-to-feature maps for top 10 pain types your prospects experience.

2. Create demo templates by persona: Sales Leader demo (pipeline visibility, forecasting), Operations demo (workflow automation, reporting), Finance demo (cost savings, ROI tracking).

3. Set pass threshold: >=70% of demos result in next-step commitment, and demo-to-proposal conversion rate is >=40% within 2 weeks.

4. Before each demo, review discovery notes and create a custom demo agenda: list 3-5 pain points to address, features to show for each, and ROI points to emphasize.

5. Send pre-demo email with agenda: "Based on our discovery, I'll show how we solve [pain 1], [pain 2], and [pain 3]—I expect this will save you ~$40K/year." Sets expectations and confirms relevance.

6. During demo, use storytelling: show customer case study with similar pains, walk through their before/after journey, connect to prospect's situation throughout.

7. After demo, send recap video (Loom) highlighting the 3 features that solve their top pains; include ROI summary and next steps; track view rate and engagement in PostHog.

8. Sync demo outcomes from Attio to PostHog; build a funnel showing discovery_completed → demo_scheduled → demo_conducted → next_step_committed → proposal_requested.

9. After 2 weeks, analyze which pain-to-feature mappings drive highest demo-to-nextstep conversion; prioritize showing those features first in future demos.

10. If >=70% of demos yield next steps and demo-to-proposal conversion >=40%, document demo playbook and move to Scalable; otherwise refine pain mapping or demo structure.

---

## KPIs to track
- Demo-to-nextstep conversion
- Demo-to-proposal conversion
- Demo engagement score
- Recap video view rate

---

## Pass threshold
**>=70% demo-to-nextstep conversion and >=40% demo-to-proposal conversion over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/discovery-based-demo`_
