---
name: demo-storytelling-framework-smoke
description: >
  Demo Storytelling Framework — Smoke Test. Transform product demos from feature walkthroughs into compelling narratives using customer stories and prospect-specific scenarios to drive emotional engagement and conviction.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "Storytelling demos delivered to ≥5 opportunities in 1 week"
kpis: ["Storytelling adoption rate", "Prospect engagement signals", "Demo-to-proposal conversion", "Close rate improvement"]
slug: "demo-storytelling-framework"
install: "npx gtm-skills add sales/connected/demo-storytelling-framework"
drills:
  - icp-definition
  - threshold-engine
---
# Demo Storytelling Framework — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Overview
Transform product demos from feature walkthroughs into compelling narratives using customer stories and prospect-specific scenarios to drive emotional engagement and conviction.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** Storytelling demos delivered to ≥5 opportunities in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. Restructure next 5-8 demos using story framework: Start with customer challenge similar to prospect's, show how they approached solution, demonstrate product solving that specific problem, end with results achieved.

2. Gather customer stories from case studies and interviews: 3-5 compelling stories covering different use cases, ICPs, and outcomes.

3. Create demo story structure: Problem (customer faced this challenge), Impact (here's what it cost them), Solution (here's how they used our product), Outcome (here's what they achieved).

4. Personalize story selection: choose customer story that matches prospect's industry, company size, use case, and pain points discussed in discovery.

5. Weave product demonstration through story: instead of 'Let me show you this feature', say 'Here's how [Customer] uses this capability to [achieve outcome]'.

6. Track PostHog events: storytelling_demo_delivered, customer_story_referenced, prospect_engagement_signals, emotional_connection_observed.

7. Measure engagement cues during demo: note when prospects lean in, ask questions, take notes, express excitement or relate to story.

8. Set pass threshold: Deliver storytelling demos to ≥5 opportunities in 1 week with ≥70% showing strong engagement signals.

9. Compare storytelling vs. feature-walkthrough demos: measure difference in engagement, demo-to-proposal rates, close rates.

10. Document which stories and narrative structures drive strongest response; proceed to Baseline if threshold met.

---

## KPIs to track
- Storytelling adoption rate
- Prospect engagement signals
- Demo-to-proposal conversion
- Close rate improvement

---

## Pass threshold
**Storytelling demos delivered to ≥5 opportunities in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/demo-storytelling-framework`_
