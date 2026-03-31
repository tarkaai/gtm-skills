---
name: sandbox-environment-demo-scalable
description: >
  Sandbox Environment Demo — Scalable Automation. Provide hands-on sandbox environment during sales process so prospects can test product with their own data and use cases to validate fit and build confidence.
stage: "Sales > Connected"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Scalable Automation"
time: "65 hours over 2 months"
outcome: "Automated sandboxes on ≥75% of qualified opportunities at scale over 2 months"
kpis: ["Sandbox provisioning automation", "Active usage rate", "Engagement score", "Sandbox-to-close conversion", "Deal velocity improvement"]
slug: "sandbox-environment-demo"
install: "npx gtm-skills add sales/connected/sandbox-environment-demo"
drills:
  - onboarding-flow
  - posthog-gtm-events
  - crm-pipeline-setup
  - activation-optimization
  - feature-announcement
  - upgrade-prompt
---
# Sandbox Environment Demo — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Overview
Provide hands-on sandbox environment during sales process so prospects can test product with their own data and use cases to validate fit and build confidence.

**Time commitment:** 65 hours over 2 months
**Pass threshold:** Automated sandboxes on ≥75% of qualified opportunities at scale over 2 months

---

## Budget

**Play-specific tools & costs**
- **Intercom (in-app messaging + email sequences):** ~$75–300/mo
- **Loom or Descript (video content at scale):** ~$15–30/mo
- **Typeform (in-app surveys + NPS):** ~$25/mo

_Total play-specific: ~$15–300/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)

---

## Instructions

1. Build n8n workflow that auto-provisions sandbox environments when deal reaches connected stage; sends personalized kickoff email with relevant resources.

2. Create intelligent sandbox configuration: n8n analyzes prospect's industry, use case, and requirements; auto-configures sandbox with most relevant sample data and integrations.

3. Implement automated usage monitoring: n8n tracks PostHog sandbox events; triggers interventions based on usage patterns (low activity, error encounters, milestone achievements).

4. Set up sandbox health scoring: n8n calculates engagement score based on login frequency, feature usage, workflow completion, time invested.

5. Connect PostHog to n8n: when sandbox shows high engagement, trigger accelerated follow-up; when usage stalls, send re-engagement content; when milestone reached, congratulate and propose next step.

6. Build sandbox intelligence dashboard: track provisioning velocity, usage patterns, completion rates, correlation with deal outcomes.

7. Create A/B testing for sandbox onboarding: test different kickoff materials, tutorial formats, success checklists; optimize for engagement and conversion.

8. Set guardrails: active usage rate must stay ≥60% of Baseline level; sandbox-to-close conversion must remain ≥45%.

9. Implement predictive sandbox analytics: identify usage patterns that predict deal success; prioritize high-scoring sandboxes for sales attention.

10. After 2 months, evaluate sandbox program impact on close rates and deal velocity; if metrics hold, proceed to Durable AI-driven sandbox intelligence.

---

## KPIs to track
- Sandbox provisioning automation
- Active usage rate
- Engagement score
- Sandbox-to-close conversion
- Deal velocity improvement

---

## Pass threshold
**Automated sandboxes on ≥75% of qualified opportunities at scale over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/sandbox-environment-demo`_
