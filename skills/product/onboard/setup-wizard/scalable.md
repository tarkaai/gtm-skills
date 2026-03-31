---
name: setup-wizard-scalable
description: >
  Guided Setup Wizard — Scalable. Build persona-specific wizard variants for 3+
  personas, run systematic A/B tests on step copy, ordering, and UX, and
  maintain >=70% completion at 500+ users/month.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable"
time: "60 hours over 2 months"
outcome: ">=70% wizard completion sustained at 500+ new users per month"
kpis: ["Wizard completion rate (overall)", "Wizard completion rate (per persona)", "Median time to complete", "Config success rate", "Experiment win rate", "Step-level dropoff by persona"]
slug: "setup-wizard"
install: "npx gtm-skills add product/onboard/setup-wizard"
drills:
  - onboarding-persona-scaling
  - ab-test-orchestrator
  - dashboard-builder
---

# Guided Setup Wizard — Scalable

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

>=70% wizard completion rate sustained across 500+ new users per month. Per-persona completion rates are all >=60% (no persona left behind). At least 3 persona-specific wizard variants running simultaneously. At least 4 A/B tests completed with 2+ producing statistically significant improvements.

## Leading Indicators

- Automated persona classification assigns >=90% of new signups to a specific persona (not "default")
- Per-persona completion rates are converging (gap between best and worst persona is <15pp)
- A/B test pipeline has 1 active experiment running at all times
- Stall rate is <10% per step across all personas
- Config success rate is >=90% across all variants

## Instructions

### 1. Build persona-specific wizard variants

Run the `onboarding-persona-scaling` drill to:

1. Analyze Baseline data to identify 3+ distinct personas based on role, company size, signup source, and first actions taken. Each persona must have >=50 historical wizard completions for statistical validity.

2. Build automated persona classification: an n8n workflow triggered on `signup_completed` that assigns `persona_type` based on user properties. Classification rules are if/else chains based on role, email domain, company size, and signup source UTMs.

3. Create a wizard variant for each persona. Differences between variants:
   - **Steps included**: Some personas skip certain steps (solo users skip team invite; technical users skip the guided tour and go straight to API setup)
   - **Step ordering**: Lead with the step that delivers the most value for this persona
   - **Step content**: Different Intercom Checklist descriptions, different Product Tour copy, different inline help text
   - **Email sequence**: Per-persona nudge emails referencing their specific use case

4. Use PostHog multi-variant feature flag `setup-wizard-variant` to route each persona to their wizard. Flag assignment is based on the `persona_type` property set by the classification workflow.

5. Build per-persona funnels in PostHog (from `dashboard-builder`) so each variant's performance is tracked independently.

### 2. Run systematic A/B tests

Run the `ab-test-orchestrator` drill to test wizard improvements. Test queue (prioritize by expected impact):

**Test 1: Step ordering.** For the worst-performing persona, test whether reordering steps improves completion. Hypothesis: "If we lead with the highest-value step instead of the current first step, completion rate will increase by 5pp because users see value before effort."

**Test 2: Wizard length.** Test a 4-step "express" wizard variant vs the full 6-step version for one persona. Hypothesis: "If we reduce the wizard to 4 essential steps, completion rate will increase by 8pp because shorter wizards have less dropoff."

**Test 3: Product Tour depth.** For the step with the highest dropoff, test a 4-stop guided tour vs a 2-stop minimal tour. Hypothesis: "A shorter tour will increase step completion by 5pp because long tours get dismissed."

**Test 4: Nudge timing.** Test stall nudge at 2 hours vs 6 hours vs 24 hours. Hypothesis: "Earlier nudges (2h) will reduce stall rate by 10pp because users are still in the setup mindset."

Rules:
- One test active per persona at a time
- Minimum 200 users per variant before evaluating
- 95% statistical significance required to declare a winner
- Log all test results (win, lose, inconclusive) in Attio

### 3. Scale monitoring to per-persona

Run the `dashboard-builder` drill to expand monitoring:
- Per-persona dashboards showing each variant's health independently
- Persona-level anomaly detection: alert if any persona's completion drops >15% from its rolling average
- Weekly report now includes per-persona breakdown and experiment results
- Cohort comparison across signup weeks to detect regression from deploys or persona mix shifts

### 4. Evaluate against threshold

After 2 months with 500+ users:

- **Primary:** >=70% overall wizard completion rate
- **Per-persona:** Every persona >=60% completion
- **Scale proof:** Completion rate did not degrade as volume increased from Baseline levels
- **Experiments:** >=4 tests completed, >=2 winners implemented

If PASS: Document the winning wizard variants, persona classification accuracy, and experiment learnings. Proceed to Durable.

If FAIL: If overall rate is below 70% but trending up, extend Scalable for 2 more weeks. If a specific persona is dragging the average down, focus all testing on that persona's variant. If experiments are inconclusive, test bigger changes (remove steps, change the wizard modality entirely).

## Time Estimate

- 15 hours: Persona analysis, classification workflow, variant creation
- 12 hours: Build 3 wizard variants with per-persona checklists, tours, and emails
- 15 hours: Run 4 A/B tests (setup, monitoring, analysis per test)
- 8 hours: Expand monitoring dashboard and reporting
- 10 hours: Analyze results, iterate on failing variants, document

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Events, funnels, experiments, feature flags, session recordings | Free up to 1M events; ~$50-200/mo at 500+ users depending on event volume ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Multiple checklists, Product Tours, persona-targeted messages | $85/seat/mo Advanced plan (needed for multiple tours and advanced targeting) ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Per-persona email sequences | $49/mo for up to 5K contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Persona classification, stall detection, monitoring workflows | $60/mo Pro plan for 10K executions ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated play-specific cost at Scalable:** $194-394/mo depending on Intercom seats and PostHog volume

## Drills Referenced

- `onboarding-persona-scaling` -- builds persona classification, per-persona wizard variants, and per-persona tracking
- `ab-test-orchestrator` -- runs systematic A/B tests on wizard steps, ordering, tours, and nudge timing
- `dashboard-builder` -- per-persona monitoring, anomaly detection, and weekly reports
