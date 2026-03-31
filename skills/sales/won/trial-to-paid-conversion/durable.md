---
name: trial-to-paid-conversion-durable
description: >
  Trial-to-Paid Conversion — Durable Intelligence. Convert free trial users to paying customers by driving activation, demonstrating value, and creating urgency, from manual trial follow-ups to AI-driven trial orchestration that personalizes interventions and maximizes conversion rates.
stage: "Sales > Won"
motion: "Outbound Founder-Led"
channels: "Email, Product, Direct"
level: "Durable Intelligence"
time: "135 hours over 6 months"
outcome: "Sustained or improving trial conversion rate (>=50%) over 6 months via continuous agent-driven onboarding optimization, intervention personalization, and churn prevention"
kpis: ["Trial conversion rate trend", "Agent experiment win rate", "Churn prediction accuracy", "Personalization impact"]
slug: "trial-to-paid-conversion"
install: "npx gtm-skills add sales/won/trial-to-paid-conversion"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - multi-channel-cadence
  - dashboard-builder
  - ab-test-orchestrator
---
# Trial-to-Paid Conversion — Durable Intelligence

> **Stage:** Sales → Won | **Motion:** Outbound Founder-Led | **Channels:** Email, Product, Direct

## Overview
Convert free trial users to paying customers by driving activation, demonstrating value, and creating urgency, from manual trial follow-ups to AI-driven trial orchestration that personalizes interventions and maximizes conversion rates.

**Time commitment:** 135 hours over 6 months
**Pass threshold:** Sustained or improving trial conversion rate (>=50%) over 6 months via continuous agent-driven onboarding optimization, intervention personalization, and churn prevention

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
- **PostHog** (CDP)
- **Attio** (CRM)
- **n8n** (Automation)
- **OpenAI** (AI/LLM)

---

## Instructions

1. Deploy an AI agent in n8n that continuously analyzes trial user behavior patterns to predict conversion probability; auto-prioritizes high-probability users for sales intervention and low-probability users for automated re-engagement.

2. Set up the agent to run experiments on trial experience: test different onboarding flows, activation milestone sequences, and intervention timing; promote approaches with highest conversion rates.

3. Build a feedback loop where every trial conversion triggers the agent to analyze that user's activation path; identify successful patterns and strengthen those pathways for future trials.

4. Deploy AI-driven personalization: agent analyzes user's role, company, and early behaviors to customize onboarding content, feature recommendations, and success metrics shown during trial.

5. Implement real-time trial health monitoring: agent detects when trial users are at risk of churning (low engagement, stuck on setup) and triggers personalized interventions (email, in-app message, call booking).

6. Build predictive upgrade timing: agent predicts optimal moment to present upgrade offer based on user's value realization signals (completed key workflow, achieved outcome, invited team).

7. Create market adaptation logic: if trial conversion rates drop, agent investigates (longer sales cycles? new competitor? product friction?) and suggests onboarding or pricing adjustments.

8. Agent continuously refines activation milestones: tests which behaviors most strongly predict conversion; adds new milestones that emerge as predictive and retires weak signals.

9. Implement dynamic trial length: agent recommends optimal trial length for each user based on their onboarding speed, complexity of use case, and engagement trajectory.

10. Establish monthly review cycles: agent generates trial intelligence reports showing conversion trends, activation patterns, intervention effectiveness, and recommended onboarding updates; team reviews and approves changes or rolls back underperforming experiments.

---

## KPIs to track
- Trial conversion rate trend
- Agent experiment win rate
- Churn prediction accuracy
- Personalization impact

---

## Pass threshold
**Sustained or improving trial conversion rate (>=50%) over 6 months via continuous agent-driven onboarding optimization, intervention personalization, and churn prevention**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/won/trial-to-paid-conversion`_
