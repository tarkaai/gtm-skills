---
name: twitter-x-ads-scalable
description: >
    Twitter/X Ads — Scalable Automation. Run promoted tweets and accounts targeting specific
  audiences, keywords, and interests to build awareness and drive traffic from solution-aware users.
stage: "Marketing > Solution Aware"
motion: "Lightweight Paid"
channels: "Paid, Social"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥750,000 impressions and ≥65 qualified leads from $8,000/month over 4 months"
kpis: ["Weekly volume", "Conversion rate", "Cost per result", "Automation efficiency", "Quality score"]
slug: "twitter-x-ads"
install: "npx gtm-skills add marketing/solution-aware/twitter-x-ads"
drills:
  - ab-test-orchestrator
  - tool-sync-workflow
---
# Twitter/X Ads — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Lightweight Paid | **Channels:** Paid, Social

## Overview
Twitter/X Ads — Scalable Automation. Run promoted tweets and accounts targeting specific audiences, keywords, and interests to build awareness and drive traffic from solution-aware users.

**Time commitment:** 75 hours over 3 months
**Pass threshold:** ≥750,000 impressions and ≥65 qualified leads from $8,000/month over 4 months

---

## Budget

**Play-specific tools & costs**
- **Tool and automation costs:** ~$100-500/mo at scale

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Automate campaign management
Run the `ab-test-orchestrator` drill to set up systematic creative testing: test 3-5 ad variants per audience, automatically pause underperformers, promote winners, and launch new variants weekly.

### 2. Build tool sync workflows
Run the `tool-sync-workflow` drill to connect: ad platform conversions to Attio deals, PostHog events to ad platform audiences (for lookalike targeting), and CRM data back to ad platforms for exclusion lists (don't target existing customers).

### 3. Scale budget with guardrails
Increase budget 20-30% monthly as long as CPA stays within target. Set automated alerts for CPA increases above 20%. Build n8n workflows to pause campaigns automatically if daily spend exceeds budget by 10%.

### 4. Evaluate against threshold
Measure against: ≥750,000 impressions and ≥65 qualified leads from $8,000/month over 4 months. If PASS, proceed to Durable. If FAIL, consolidate to best-performing audiences and creatives before scaling further.

---

## KPIs to track
- Weekly volume
- Conversion rate
- Cost per result
- Automation efficiency
- Quality score

---

## Pass threshold
**≥750,000 impressions and ≥65 qualified leads from $8,000/month over 4 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/twitter-x-ads`_
