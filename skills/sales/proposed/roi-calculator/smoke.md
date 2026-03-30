---
name: roi-calculator-smoke
description: >
  ROI Calculator & Business Case — Smoke Test. Quantify and demonstrate ROI to justify purchase decisions and overcome budget objections, from manual ROI spreadsheets to AI-driven dynamic business case generation that personalizes value narratives and auto-updates based on prospect data and market benchmarks.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email, Website"
level: "Smoke Test"
time: "7 hours over 1 week"
outcome: ">=5 prospects with >=5x ROI calculated and >=3 reference ROI in decisions within 1 week"
kpis: ["ROI value distribution", "Payback period", "ROI validation rate", "ROI impact on deal velocity"]
slug: "roi-calculator"
install: "npx gtm-skills add sales/proposed/roi-calculator"
---
# ROI Calculator & Business Case — Smoke Test

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email, Website

## Overview
Quantify and demonstrate ROI to justify purchase decisions and overcome budget objections, from manual ROI spreadsheets to AI-driven dynamic business case generation that personalizes value narratives and auto-updates based on prospect data and market benchmarks.

**Time commitment:** 7 hours over 1 week
**Pass threshold:** >=5 prospects with >=5x ROI calculated and >=3 reference ROI in decisions within 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)

---

## Instructions

1. Create a simple ROI calculator in a spreadsheet with inputs for prospect's current costs (labor hours, tool costs, inefficiency losses) and outputs showing savings, payback period, and 3-year ROI.

2. During discovery, gather ROI inputs: "How many hours per week does your team spend on [task]?" "What's the loaded cost per hour?" "How much are you spending on [current solution]?" "What's the cost of [problem] to your business?"

3. Set pass threshold: build ROI calculators for >=5 prospects showing >=5x ROI within 1 year, and >=3 prospects reference ROI in decision-making conversations.

4. After discovery, fill out calculator with prospect's numbers; calculate total annual savings, payback period (time to recoup investment), and 3-year ROI.

5. Present ROI in follow-up: "Based on our conversation, you're spending $100K/year on this problem. Our solution costs $20K and saves you $80K annually—4x ROI in year 1, payback in 10 weeks."

6. Send calculator spreadsheet to prospect for validation: "Here's the math based on your numbers—do these figures align with your experience? Feel free to adjust inputs if needed."

7. Log ROI metrics in Attio with fields for annual_savings, payback_period, three_year_roi, and roi_validated (yes/no); track which ROI thresholds move deals forward.

8. In PostHog, create events for roi_calculated and roi_presented with properties for ROI value, payback period, and prospect response.

9. After 1 week, analyze: did >=3 prospects reference ROI in decision conversations? Did strong ROI (>=5x) correlate with faster deal progression or higher close rates?

10. If >=5 prospects have strong ROI and >=3 reference it in decisions, ROI is a powerful sales tool; document calculator methodology and proceed to Baseline; otherwise improve discovery to capture better ROI inputs.

---

## KPIs to track
- ROI value distribution
- Payback period
- ROI validation rate
- ROI impact on deal velocity

---

## Pass threshold
**>=5 prospects with >=5x ROI calculated and >=3 reference ROI in decisions within 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/roi-calculator`_
