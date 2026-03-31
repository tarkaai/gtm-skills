---
name: award-submissions-program-baseline
description: >
    Industry Award Submissions — Baseline Run. Submit to industry awards for credibility, PR
  opportunities, and social proof to influence solution-aware prospects evaluating vendors.
stage: "Marketing > Solution Aware"
motion: "PR & Earned Mentions"
channels: "Other, Social"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥10 submissions and ≥3 wins with ≥10 qualified leads from award PR"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "award-submissions-program"
install: "npx gtm-skills add marketing/solution-aware/award-submissions-program"
drills:
  - case-study-creation
  - newsletter-pipeline
  - posthog-gtm-events
---
# Industry Award Submissions — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** PR & Earned Mentions | **Channels:** Other, Social

## Overview
Industry Award Submissions — Baseline Run. Submit to industry awards for credibility, PR opportunities, and social proof to influence solution-aware prospects evaluating vendors.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥10 submissions and ≥3 wins with ≥10 qualified leads from award PR

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build a PR content machine
Run the `case-study-creation` drill to create 2-3 customer case studies that serve as PR assets. Run the `newsletter-pipeline` drill to start your own newsletter that establishes thought leadership and gives journalists a reason to follow you.

### 2. Configure PR tracking
Run the `posthog-gtm-events` drill to track: `award-submissions-program_mention_published`, `award-submissions-program_backlink_acquired`, `award-submissions-program_referral_traffic`, `award-submissions-program_lead_from_pr`. Set up Google Alerts or a media monitoring tool for brand mentions.

### 3. Execute a 4-week PR push
Pitch 10-20 publications. Submit 2-3 guest articles. Publish your case studies and promote them. Track all coverage and resulting traffic in PostHog.

### 4. Evaluate against threshold
Measure against: ≥10 submissions and ≥3 wins with ≥10 qualified leads from award PR. If PASS, proceed to Scalable. If FAIL, test different story angles or target tier-2 publications first to build credibility.

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥10 submissions and ≥3 wins with ≥10 qualified leads from award PR**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/award-submissions-program`_
