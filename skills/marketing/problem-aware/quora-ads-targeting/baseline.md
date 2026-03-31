---
name: quora-ads-targeting-baseline
description: >
    Quora Ads — Baseline Run. Run answer-based ads on Quora targeting specific questions and topics
  to reach problem-aware and solution-aware audiences actively seeking solutions.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid, Communities"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥100,000 impressions and ≥18 qualified leads from $1,500 budget over 3 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "quora-ads-targeting"
install: "npx gtm-skills add marketing/problem-aware/quora-ads-targeting"
drills:
  - budget-allocation
  - posthog-gtm-events
  - retargeting-setup
---
# Quora Ads — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid, Communities

## Overview
Quora Ads — Baseline Run. Run answer-based ads on Quora targeting specific questions and topics to reach problem-aware and solution-aware audiences actively seeking solutions.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥100,000 impressions and ≥18 qualified leads from $1,500 budget over 3 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Optimize budget allocation
Run the `budget-allocation` drill to analyze your Smoke test data and allocate budget across ad sets, audiences, and platforms. Shift budget toward the highest-performing segments. Set daily budget caps to prevent overspend.

### 2. Set up retargeting
Run the `retargeting-setup` drill to configure retargeting audiences: website visitors who didn't convert, landing page visitors, and engaged social followers. Create retargeting ad variants with stronger CTAs.

### 3. Configure tracking pipeline
Run the `posthog-gtm-events` drill to set up end-to-end tracking: `quora-ads-targeting_ad_click`, `quora-ads-targeting_landing_page_view`, `quora-ads-targeting_form_submit`, `quora-ads-targeting_lead_qualified`. Connect ad platform data to PostHog via webhooks for unified reporting.

### 4. Run for 2 weeks at increased budget
Scale budget to $1,000-3,000 for the test period. Monitor daily: CPA trends, quality of leads entering CRM, ad fatigue indicators (declining CTR). Make weekly adjustments to targeting and creative.

### 5. Evaluate against threshold
Measure against: ≥100,000 impressions and ≥18 qualified leads from $1,500 budget over 3 weeks. If PASS, proceed to Scalable. If FAIL, test different audiences, creatives, or platforms.

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥100,000 impressions and ≥18 qualified leads from $1,500 budget over 3 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/quora-ads-targeting`_
