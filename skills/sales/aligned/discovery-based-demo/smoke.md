---
name: discovery-based-demo-smoke
description: >
  Discovery-Based Demo — Smoke Test. Tailor product demos to pain points uncovered in discovery to maximize relevance and engagement, from manual demo customization to AI-driven dynamic demos that auto-adapt based on prospect signals and deliver personalized value narratives.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=3 out of 5 demos yield next-step commitment via pain-based customization in 1 week"
kpis: ["Demo-to-nextstep conversion", "Demo engagement score", "Pain coverage rate", "Questions asked per demo"]
slug: "discovery-based-demo"
install: "npx gtm-skills add sales/aligned/discovery-based-demo"
---
# Discovery-Based Demo — Smoke Test

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Overview
Tailor product demos to pain points uncovered in discovery to maximize relevance and engagement, from manual demo customization to AI-driven dynamic demos that auto-adapt based on prospect signals and deliver personalized value narratives.

**Time commitment:** 8 hours over 1 week
**Pass threshold:** >=3 out of 5 demos yield next-step commitment via pain-based customization in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **Loom** (Video)

---

## Instructions

1. Create a demo preparation checklist: review discovery notes, identify top 3 pain points, map each pain to specific product features, prepare custom demo narrative.

2. For 5 upcoming demos, spend 15-20 minutes before each call reviewing discovery notes in Attio and customizing demo flow to address prospect's specific pains.

3. Set pass threshold: >=3 out of 5 demos result in next-step commitment (technical eval, proposal request, stakeholder intro), and customized demos outperform generic demos by >=30% in engagement.

4. Structure demo around prospect's pain journey: start with their current state and pain, show how product solves each pain, quantify value at each step, end with their future state.

5. During demo, explicitly connect features to discovery: "You mentioned spending 10 hours/week on manual reports—this feature automates that, saving your team 8 hours weekly."

6. After each demo, log outcome in Attio (next step committed, needs follow-up, not interested) and track which pain-to-feature mappings resonated most.

7. In PostHog, create events for demo_conducted, demo_customized, and demo_outcome with properties for pains addressed and next-step status.

8. Compare engagement metrics for customized demos vs generic feature walkthroughs: measure questions asked, meeting duration, and next-step conversion rate.

9. After 1 week, analyze: did >=3 out of 5 customized demos yield next steps? Did customization improve engagement or outcomes vs your baseline generic demo approach?

10. If customized demos convert >=60% to next steps (vs ~30% for generic), document pain-to-feature mapping process and proceed to Baseline; otherwise refine demo structure or discovery quality.

---

## KPIs to track
- Demo-to-nextstep conversion
- Demo engagement score
- Pain coverage rate
- Questions asked per demo

---

## Pass threshold
**>=3 out of 5 demos yield next-step commitment via pain-based customization in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/discovery-based-demo`_
