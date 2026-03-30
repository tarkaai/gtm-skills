---
name: roi-calculator-baseline
description: >
  ROI Calculator & Business Case — Baseline Run. Quantify and demonstrate ROI to justify purchase decisions and overcome budget objections, from manual ROI spreadsheets to AI-driven dynamic business case generation that personalizes value narratives and auto-updates based on prospect data and market benchmarks.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email, Website"
level: "Baseline Run"
time: "24 hours over 2 weeks"
outcome: ">=70% of prospects with >=5x ROI and >=40% faster close time for strong-ROI deals over 2 weeks"
kpis: ["ROI distribution", "Deal velocity by ROI tier", "Close rate by ROI tier", "Business case conversion rate"]
slug: "roi-calculator"
install: "npx gtm-skills add sales/proposed/roi-calculator"
---
# ROI Calculator & Business Case — Baseline Run

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email, Website

## Overview
Quantify and demonstrate ROI to justify purchase decisions and overcome budget objections, from manual ROI spreadsheets to AI-driven dynamic business case generation that personalizes value narratives and auto-updates based on prospect data and market benchmarks.

**Time commitment:** 24 hours over 2 weeks
**Pass threshold:** >=70% of prospects with >=5x ROI and >=40% faster close time for strong-ROI deals over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$40–100/mo
- **Clay or Apollo (list building + enrichment):** ~$50–150/mo

_Total play-specific: ~$40–150/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **Loom** (Video)

---

## Instructions

1. Expand ROI calculators to 15-20 prospects over 2 weeks; build a professional ROI calculator tool (web-based or polished spreadsheet) with multiple value drivers (time savings, cost reduction, revenue increase, risk mitigation).

2. Create industry/persona-specific ROI templates: Sales ROI (pipeline increase, deal velocity), Operations ROI (efficiency, cost reduction), Finance ROI (compliance savings, reporting time).

3. Set pass threshold: >=70% of prospects achieve >=5x ROI, and prospects with strong ROI close >=40% faster than prospects with weak ROI (<3x).

4. During discovery and demo, continuously gather ROI inputs; validate numbers with prospect: "You mentioned 40 hours/month—at $100/hour, that's $48K/year. Sound right?"

5. Build comprehensive business cases: combine ROI calculator with qualitative benefits (risk reduction, competitive advantage), customer proof points (case studies), and implementation plan; deliver as polished 1-2 page document.

6. Present ROI early in sales cycle (post-demo) to anchor value: "Before we discuss pricing, let's quantify the value—here's what we're projecting based on your situation." Sets high-value expectation.

7. Sync ROI data from Attio to PostHog; create a funnel showing roi_calculated → roi_presented → roi_validated → proposal_delivered → deal_closed; measure conversion at each stage.

8. For deals with weak ROI (<3x), either find additional value drivers (risk reduction, compliance, revenue impact) or consider disqualifying (low ROI = low close probability + high churn risk).

9. After 2 weeks, compare deal velocity and close rates for strong ROI (>=5x) vs weak ROI (<3x) deals; if strong ROI accelerates closes by >=40%, ROI is highly predictive.

10. If >=70% of deals have strong ROI and strong-ROI deals close >=40% faster, move to Scalable; otherwise improve discovery quality or expand value drivers in calculator.

---

## KPIs to track
- ROI distribution
- Deal velocity by ROI tier
- Close rate by ROI tier
- Business case conversion rate

---

## Pass threshold
**>=70% of prospects with >=5x ROI and >=40% faster close time for strong-ROI deals over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/roi-calculator`_
