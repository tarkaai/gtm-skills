---
name: risk-assessment-discovery-durable
description: >
  Risk & Concern Discovery — Durable Intelligence. Surface concerns, risks, and objections early in the sales cycle to address them proactively rather than encountering surprises at decision time.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "138 hours over 6 months"
outcome: "Sustained or improving risk mitigation success and deal predictability over 6 months via continuous AI-driven risk intelligence"
kpis: ["Risk prediction accuracy", "Early risk identification rate", "Mitigation success rate", "Late-stage surprise elimination", "Close rate improvement"]
slug: "risk-assessment-discovery"
install: "npx gtm-skills add sales/connected/risk-assessment-discovery"
---
# Risk & Concern Discovery — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Surface concerns, risks, and objections early in the sales cycle to address them proactively rather than encountering surprises at decision time.

**Time commitment:** 138 hours over 6 months
**Pass threshold:** Sustained or improving risk mitigation success and deal predictability over 6 months via continuous AI-driven risk intelligence

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$100–200/mo
- **Clay (enrichment + continuous list refresh):** ~$200–500/mo
- **LinkedIn Sales Navigator:** ~$100/mo

_Total play-specific: ~$100–500/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Anthropic** (AI/LLM)
- **Gong** (Sales Engagement)

---

## Instructions

1. Deploy PostHog event streams triggering n8n AI agents when: new risk is identified, risk severity changes, or historical similar risks caused deal losses.

2. Build n8n AI risk intelligence agent analyzing won/lost deal data: identifies which risks are most frequently fatal, which are most easily mitigated, which predict specific objections.

3. Implement AI-powered risk prediction: AI agent analyzes prospect characteristics and deal context to predict likely risks before discovery calls; prepares mitigation materials proactively.

4. Create learning loop: PostHog tracks which risk discovery questions uncover most critical concerns; AI agent recommends optimal risk assessment sequences by prospect type.

5. Build adaptive risk mitigation: AI agent learns from successful mitigations which strategies work best for specific risk categories and prospect segments; suggests personalized mitigation approaches.

6. Deploy proactive risk monitoring: AI agent scans call transcripts and emails for risk language (concern, worried, hesitant, risky); alerts rep immediately with suggested responses.

7. Implement automatic risk escalation: when AI agent identifies risk pattern that historically requires executive involvement, automatically notifies appropriate stakeholder with briefing.

8. Create predictive risk scoring: AI agent predicts probability of specific risks materializing for each deal; prioritizes mitigation efforts on highest-likelihood concerns.

9. Set guardrails: if late-stage surprise rate increases >10% or risk discovery drops below Scalable benchmark for 2+ weeks, alert team and suggest refinements.

10. Establish monthly review cycle: analyze risk pattern evolution, mitigation effectiveness, prediction accuracy; refine AI agent intelligence based on deal outcomes.

---

## KPIs to track
- Risk prediction accuracy
- Early risk identification rate
- Mitigation success rate
- Late-stage surprise elimination
- Close rate improvement

---

## Pass threshold
**Sustained or improving risk mitigation success and deal predictability over 6 months via continuous AI-driven risk intelligence**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/risk-assessment-discovery`_
