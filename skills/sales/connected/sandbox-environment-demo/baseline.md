---
name: sandbox-environment-demo-baseline
description: >
  Sandbox Environment Demo — Baseline Run. Provide hands-on sandbox environment during sales process so prospects can test product with their own data and use cases to validate fit and build confidence.
stage: "Sales > Connected"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "Sandboxes on ≥80% of qualified opportunities over 2 weeks"
kpis: ["Sandbox provisioning rate", "Active usage rate", "Success checklist completion", "Sandbox-to-close conversion"]
slug: "sandbox-environment-demo"
install: "npx gtm-skills add sales/connected/sandbox-environment-demo"
drills:
  - onboarding-flow
  - posthog-gtm-events
  - crm-pipeline-setup
  - threshold-engine
---
# Sandbox Environment Demo — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Overview
Provide hands-on sandbox environment during sales process so prospects can test product with their own data and use cases to validate fit and build confidence.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** Sandboxes on ≥80% of qualified opportunities over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Tally or Typeform (surveys + forms):** Free–$25/mo
- **Loom (async video for onboarding/CSM):** Free–$15/mo

_Total play-specific: ~$15–25/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)

---

## Instructions

1. Expand sandbox program to 20-30 opportunities over 2 weeks.

2. Create sandbox environment tiers: Basic (standard sample data), Custom (prospect-specific data), Enterprise (full integration setup for complex evaluation).

3. Build sandbox playbook: qualification criteria for sandbox access, provisioning process, kickoff templates, usage monitoring dashboards, intervention triggers.

4. Set up PostHog event tracking: sandbox_provisioned, first_login, feature_used, workflow_completed, data_uploaded, help_requested, milestone_achieved.

5. Implement usage-based interventions: low usage triggers check-in email, specific feature usage triggers relevant content, completed workflows trigger congratulations and next steps.

6. Track sandbox to outcome metrics: measure usage patterns that predict proposal acceptance and close; identify which workflows drive highest conviction.

7. Create sandbox content library: video tutorials, workflow guides, use case templates, troubleshooting docs organized by persona and use case.

8. Set pass threshold: Sandboxes on ≥80% of qualified opportunities over 2 weeks with ≥65% active usage and ≥50% completing success checklist.

9. Analyze sandbox patterns: which features drive most engagement, which workflows validate fit, which usage levels predict closes.

10. If threshold met, document sandbox program and proceed to Scalable; if not, refine sandbox experience or support model.

---

## KPIs to track
- Sandbox provisioning rate
- Active usage rate
- Success checklist completion
- Sandbox-to-close conversion

---

## Pass threshold
**Sandboxes on ≥80% of qualified opportunities over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/sandbox-environment-demo`_
