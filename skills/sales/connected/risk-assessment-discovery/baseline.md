---
name: risk-assessment-discovery-baseline
description: >
  Risk & Concern Discovery — Baseline Run. Surface concerns, risks, and objections early in the sales cycle to address them proactively rather than encountering surprises at decision time.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "14 hours over 2 weeks"
outcome: "Risks identified and mitigated on ≥80% of opportunities over 2 weeks"
kpis: ["Risk discovery rate", "Risk mitigation success rate", "Close rate impact", "Late-stage surprise reduction"]
slug: "risk-assessment-discovery"
install: "npx gtm-skills add sales/connected/risk-assessment-discovery"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Risk & Concern Discovery — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Surface concerns, risks, and objections early in the sales cycle to address them proactively rather than encountering surprises at decision time.

**Time commitment:** 14 hours over 2 weeks
**Pass threshold:** Risks identified and mitigated on ≥80% of opportunities over 2 weeks

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

---

## Instructions

1. Expand risk discovery to 35-50 opportunities over 2 weeks.

2. Build comprehensive risk assessment framework covering all five risk categories with specific probe questions for each.

3. Create risk severity scoring rubric: assess likelihood (High/Medium/Low) and impact (High/Medium/Low) for each identified risk.

4. Set up PostHog event tracking: risk_category_identified, severity_scored, mitigation_delivered, risk_resolved, deal_progression_post_risk.

5. Develop risk mitigation playbooks: standard responses and proof points for common risks in each category.

6. Track risk-to-outcome correlation: measure how identified risks affect close rate, deal velocity, discount requests, and contract terms.

7. Build risk escalation process: route high-severity risks to appropriate stakeholders (CFO for financial, CTO for technical, CEO for strategic).

8. Set pass threshold: Risks identified and documented on ≥80% of opportunities over 2 weeks with ≥60% having all high-severity risks mitigated before proposal.

9. Analyze risk patterns: which risks appear most frequently, which predict deal losses, which are easiest to mitigate.

10. If threshold met, document risk discovery playbook and proceed to Scalable; if not, refine risk assessment framework.

---

## KPIs to track
- Risk discovery rate
- Risk mitigation success rate
- Close rate impact
- Late-stage surprise reduction

---

## Pass threshold
**Risks identified and mitigated on ≥80% of opportunities over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/risk-assessment-discovery`_
