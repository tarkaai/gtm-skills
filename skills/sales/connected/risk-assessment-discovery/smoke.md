---
name: risk-assessment-discovery-smoke
description: >
  Risk & Concern Discovery — Smoke Test. Surface concerns, risks, and objections early in the sales cycle to address them proactively rather than encountering surprises at decision time.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Risks identified and addressed with ≥8 opportunities in 1 week"
kpis: ["Risk discovery completion rate", "High-severity risk identification", "Mitigation plan creation rate", "Late-stage objection reduction"]
slug: "risk-assessment-discovery"
install: "npx gtm-skills add sales/connected/risk-assessment-discovery"
---
# Risk & Concern Discovery — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Surface concerns, risks, and objections early in the sales cycle to address them proactively rather than encountering surprises at decision time.

**Time commitment:** 5 hours over 1 week
**Pass threshold:** Risks identified and addressed with ≥8 opportunities in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. On first 8-10 discovery calls, explicitly ask: 'What concerns do you have about making this change?' and 'What could prevent this from being successful?'.

2. Create risk categories: Financial (budget, ROI, cost), Technical (integration, security, complexity), Organizational (change management, adoption, training), Timeline (urgency, competing priorities), Vendor (company stability, support, roadmap).

3. Use follow-up probes: 'What's the worst that could happen if this doesn't work?' and 'What would your CEO/board say if this failed?'.

4. Log all identified risks in Attio with severity rating (High/Medium/Low) and category; create mitigation plan for each high-severity risk.

5. Track PostHog events: risk_identified, high_severity_risk, mitigation_plan_created, risk_addressed.

6. Address risks immediately: provide proof points, case studies, guarantees, or commitments that mitigate specific concerns.

7. Create risk mitigation document: written plan showing how each identified risk will be addressed with specific actions and timelines.

8. Set pass threshold: Identify risks with ≥8 opportunities in 1 week with ≥70% having documented mitigation plans.

9. Measure impact: track how early risk discovery affects close rates, deal velocity, and objection frequency at proposal stage.

10. Document which risk discovery questions uncover most critical concerns; proceed to Baseline if threshold met.

---

## KPIs to track
- Risk discovery completion rate
- High-severity risk identification
- Mitigation plan creation rate
- Late-stage objection reduction

---

## Pass threshold
**Risks identified and addressed with ≥8 opportunities in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/risk-assessment-discovery`_
