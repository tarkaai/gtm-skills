---
name: demo-storytelling-framework-scalable
description: >
  Demo Storytelling Framework — Scalable Automation. Transform product demos from feature walkthroughs into compelling narratives using customer stories and prospect-specific scenarios to drive emotional engagement and conviction.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Scalable Automation"
time: "58 hours over 2 months"
outcome: "Storytelling demos on ≥75% of opportunities at scale over 2 months with maintained conversion improvement"
kpis: ["Storytelling adoption rate", "Demo-to-proposal conversion", "Engagement score", "Story matching accuracy", "Close rate improvement"]
slug: "demo-storytelling-framework"
install: "npx gtm-skills add sales/connected/demo-storytelling-framework"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Demo Storytelling Framework — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Overview
Transform product demos from feature walkthroughs into compelling narratives using customer stories and prospect-specific scenarios to drive emotional engagement and conviction.

**Time commitment:** 58 hours over 2 months
**Pass threshold:** Storytelling demos on ≥75% of opportunities at scale over 2 months with maintained conversion improvement

---

## Budget

**Play-specific tools & costs**
- **Apollo or Aircall (calling at volume):** ~$100–200/mo
- **Intercom or Loops (automated sequences):** ~$100–300/mo

_Total play-specific: ~$100–300/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Gong** (Sales Engagement)

---

## Instructions

1. Build n8n workflow that recommends optimal customer story for each demo based on prospect's industry, use case, company size, and pain points from discovery.

2. Create story intelligence: n8n analyzes which stories resonate best with which prospect segments; surfaces most relevant narratives for each demo.

3. Implement automated story preparation: n8n generates demo prep doc with recommended story, key narrative points, feature mapping, expected outcomes to emphasize.

4. Set up engagement tracking: use Gong to analyze demo recordings for engagement signals (prospect questions, excitement indicators, story connection moments).

5. Connect PostHog to n8n: track which stories are used most frequently, which drive highest engagement, which correlate with proposal acceptance.

6. Build storytelling intelligence dashboard: measure story usage, engagement scores by story, conversion rates by narrative approach, effectiveness by rep.

7. Create story asset library: maintain video customer testimonials, written case studies, data visualizations, quote cards organized by story for easy reference during demos.

8. Set guardrails: storytelling adoption must stay ≥75% of Baseline level; demo-to-proposal improvement must remain ≥12%.

9. Implement story refresh process: regularly update story library with new customer successes, retire outdated stories, A/B test new narrative structures.

10. After 2 months, evaluate storytelling impact on deal quality and close rates; if metrics hold, proceed to Durable AI-driven story intelligence.

---

## KPIs to track
- Storytelling adoption rate
- Demo-to-proposal conversion
- Engagement score
- Story matching accuracy
- Close rate improvement

---

## Pass threshold
**Storytelling demos on ≥75% of opportunities at scale over 2 months with maintained conversion improvement**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/demo-storytelling-framework`_
