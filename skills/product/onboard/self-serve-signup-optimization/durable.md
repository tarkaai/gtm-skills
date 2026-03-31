---
name: self-serve-signup-optimization-durable
description: >
  Signup Funnel Optimization — Durable Intelligence. Reduce friction in signup flow through testing and optimization to increase conversion rate.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Website, Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving CVR ≥35% over 6 months via AI"
kpis: ["Signup conversion", "Form completion", "Drop-off points", "Experiment velocity", "AI lift"]
slug: "self-serve-signup-optimization"
install: "npx gtm-skills add product/onboard/self-serve-signup-optimization"
drills:
  - onboarding-flow
  - posthog-gtm-events
  - crm-pipeline-setup
  - activation-optimization
  - feature-announcement
  - upgrade-prompt
  - churn-prevention
  - dashboard-builder
---
# Signup Funnel Optimization — Durable Intelligence

> **Stage:** Product → Onboard | **Motion:** Lead Capture Surface | **Channels:** Website, Product

## Overview
Reduce friction in signup flow through testing and optimization to increase conversion rate.

**Time commitment:** 150 hours over 6 months
**Pass threshold:** Sustained or improving CVR ≥35% over 6 months via AI

---

## Budget

**Play-specific tools & costs**
- **Intercom (agent-triggered messaging, health-based):** ~$150–500/mo
- **Typeform (automated NPS + CSAT loops):** ~$25/mo
- **Descript (AI-powered video repurposing):** ~$30/mo

_Total play-specific: ~$25–500/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (Product Analytics)
- **n8n** (Automation)
- **Loops** (Email)
- **Intercom** (Communication)
- **OpenAI** (AI/LLM)

---

## Instructions

1. Stream PostHog to n8n; build AI behavior agent.

2. AI runs weekly A/B tests via PostHog flags.

3. AI monitors, compares, rolls out winners.

4. AI personalizes based on properties/patterns.

5. AI identifies at-risk; triggers n8n interventions.

6. Loop: AI proposes → PostHog tracks → AI applies.

7. AI analyzes recordings; suggests UX improvements.

8. Guardrail: >20% drop for 2wks = alert.

9. Monthly: AI report on experiments and wins.

10. Sustain/improve over 6mo via AI optimization.

---

## KPIs to track
- Signup conversion
- Form completion
- Drop-off points
- Experiment velocity
- AI lift

---

## Pass threshold
**Sustained or improving CVR ≥35% over 6 months via AI**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/onboard/self-serve-signup-optimization`_
