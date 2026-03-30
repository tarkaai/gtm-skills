---
name: success-criteria-definition-smoke
description: >
  Success Criteria Definition — Smoke Test. Co-create specific, measurable success criteria with prospects to align expectations and provide clear evaluation framework for purchase decision.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Success criteria defined with ≥8 opportunities in 1 week"
kpis: ["Success criteria definition rate", "Quantifiable metric percentage", "Mutual agreement rate", "Close rate correlation"]
slug: "success-criteria-definition"
install: "npx gtm-skills add sales/connected/success-criteria-definition"
---
# Success Criteria Definition — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Co-create specific, measurable success criteria with prospects to align expectations and provide clear evaluation framework for purchase decision.

**Time commitment:** 5 hours over 1 week
**Pass threshold:** Success criteria defined with ≥8 opportunities in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. On first 8-10 opportunities past discovery, ask: 'How will you know this purchase was successful 90 days after going live?'.

2. Guide prospects to define 3-5 specific, measurable success criteria (e.g., 'Reduce manual work by 10 hours/week', 'Increase conversion rate by 15%', 'Achieve ROI within 6 months').

3. Probe for quantifiable metrics: 'What specific number would you need to see to consider this a success?'.

4. Document success criteria in Attio with specific metrics, timelines, and stakeholders responsible for measuring success.

5. Validate achievability: confirm your product can deliver on these criteria; flag any stretch goals that need careful expectation setting.

6. Track PostHog events: success_criteria_defined, quantifiable_metric_established, achievability_validated, mutual_agreement_reached.

7. Use success criteria to structure POC or trial: 'Let's set up a 2-week test specifically measuring [criterion]'.

8. Set pass threshold: Define success criteria with ≥8 opportunities in 1 week with ≥80% having quantifiable metrics.

9. Measure correlation: track whether deals with defined success criteria close at higher rates and have better retention.

10. Document which success criteria definition approaches work best; proceed to Baseline if threshold met.

---

## KPIs to track
- Success criteria definition rate
- Quantifiable metric percentage
- Mutual agreement rate
- Close rate correlation

---

## Pass threshold
**Success criteria defined with ≥8 opportunities in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/success-criteria-definition`_
