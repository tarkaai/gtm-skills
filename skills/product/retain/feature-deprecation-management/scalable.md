---
name: feature-deprecation-management-scalable
description: >
  Feature Sunset Communication — Scalable Automation. Handle multiple concurrent
  deprecations with dynamic routing that matches each user to the right migration
  path, A/B tested communication, and churn prevention for at-risk users.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥85% migration at 500+ affected users across 2+ concurrent deprecations"
kpis: ["Migration completion rate at scale", "Churn from sunset", "Migration velocity by segment", "Route effectiveness (completion rate per path)", "Cost per migration"]
slug: "feature-deprecation-management"
install: "npx gtm-skills add product/retain/feature-deprecation-management"
drills:
  - ab-test-orchestrator
  - churn-prevention
---

# Feature Sunset Communication — Scalable Automation

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Scale the deprecation system to handle 500+ affected users across multiple concurrent feature sunsets. At Baseline, every user in a tier got the same experience. At Scalable, the system dynamically routes each user to the migration path most likely to succeed for them based on their behavior. Communication is A/B tested to find the highest-converting messages. Churn prevention catches users who fall through the cracks.

## Leading Indicators

- Dynamic routing assigning users to paths within 24 hours of entering the deprecation cohort
- A/B tests running on deprecation messaging with 200+ samples per variant
- Self-serve path completion rate above 70% (these users cost nothing to migrate)
- High-touch path reserved for less than 15% of affected users (keeps cost per migration low)
- Churn prevention catching at-risk deprecation users before they cancel

## Instructions

### 1. A/B test deprecation communication

Run the `ab-test-orchestrator` drill to optimize the deprecation messaging. Test these variables one at a time:

**Test 1: Notice urgency framing**
- Control: "This feature will be retired on {date}. Migrate now."
- Variant: "You have {N} days to migrate. {X}% of users like you have already switched."

**Test 2: Migration CTA placement**
- Control: Banner at top of deprecated feature page
- Variant: Inline prompt within the deprecated feature's workflow, triggered at the moment of use

**Test 3: Email subject line**
- Control: "Important: {Feature} is being retired on {date}"
- Variant: "{Name}, your migration guide for {Feature} is ready"

Use PostHog experiments with a minimum of 200 users per variant. Run each test for 7 days or until statistical significance. Implement winners immediately and feed results into the routing rules.

### 2. Deploy dynamic segment routing

Run the the deprecation segment routing workflow (see instructions below) drill. This builds the system that evaluates each user's behavior and assigns them to the optimal migration path:

- **Self-starter users** (clicked CTA, used replacement within 48h) → Self-serve: Intercom checklist only
- **Needs guidance** (clicked CTA, did NOT use replacement within 7 days) → Guided: product tour + 2-email sequence
- **Workflow-dependent** (critical tier + 3+ workflows using deprecated feature) → High-touch: personal migration plan + 1:1 session booking + workflow-specific email guides
- **Resistant** (regressed after trying replacement OR dismissed all notices) → Rescue: account owner task + personalized feedback request
- **Passive** (low tier + no engagement with notices) → Light touch: single reminder email 14 days before sunset

The routing workflow runs daily in n8n, evaluates each user, sets PostHog feature flags to control which migration experience they see, and re-routes users whose behavior changes (e.g., a self-starter who stalls gets upgraded to guided).

### 3. Activate churn prevention for deprecation users

Run the `churn-prevention` drill with a specific focus on the deprecation cohort. Configure:

- **Churn signal overlay:** Layer standard churn signals (usage decline, billing page visits, team shrinkage) on top of deprecation-specific signals (migration stalled for 14+ days, regression to old feature, multiple notice dismissals)
- **Intervention targeting:** When a deprecation-cohort user triggers churn signals, the intervention should acknowledge the deprecation: "We know the {feature} change is a big adjustment. Can we help you get set up with {replacement}?" — not a generic retention message
- **Escalation path:** If a critical-tier user shows both deprecation stall AND standard churn signals, escalate immediately to account owner with full context: migration status, churn risk score, usage data, and MRR at risk

The churn prevention system runs continuously alongside the migration tracker. A user can be in both the migration pipeline and the churn intervention pipeline simultaneously.

### 4. Scale across multiple deprecations

With the routing and testing infrastructure in place, add new deprecations without rebuilding the system:

1. For each new deprecation, run the `deprecation-impact-assessment` drill (from Smoke)
2. The communication templates are parameterized by `feature_slug` — create new instances, do not rebuild from scratch
3. The routing workflow evaluates all active deprecations in a single daily run
4. The migration dashboard shows all active deprecations side by side
5. A/B test learnings from one deprecation apply to the next (e.g., if social proof framing won for deprecation A, start with it as the default for deprecation B)

### 5. Evaluate against threshold

After 2 months of running with 500+ affected users across 2+ concurrent deprecations:

- **Primary threshold:** ≥85% migration completion rate across all active deprecations
- **Scale test:** The per-migration cost (staff hours + tool costs) should be lower than Baseline. If high-touch paths are consuming more than 15% of migrations, the self-serve and guided paths need improvement.

If PASS: The system scales. Document: which routing paths have the highest completion rates, which A/B test results to carry forward, cost per migration by path. Proceed to Durable.

If FAIL: Identify the bottleneck. If migration rate is high but cost is too high, shift more users to self-serve. If migration rate is low at scale, the routing rules may not cover a new user archetype — analyze stalled users for common patterns and create a new route.

## Time Estimate

- 10 hours: A/B test design, setup, and analysis (3 tests across 2 months)
- 15 hours: Segment routing workflow build and testing
- 10 hours: Churn prevention configuration for deprecation overlay
- 15 hours: Multi-deprecation scaling and template parameterization
- 10 hours: Ongoing monitoring, route optimization, and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, cohorts, funnels, dashboards | Free tier covers most usage; paid at $0.00005/event above 1M ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app messages, checklists, product tours, churn interventions | Advanced $85/seat/mo for workflow routing ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email sequences, transactional emails, broadcasts | $49/mo+ based on contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | Migration scores, routing data, account owner tasks | Standard stack — excluded from play budget |
| n8n | Routing workflow, churn detection, migration scoring | Standard stack — excluded from play budget |

**Estimated play-specific cost:** $134-185/mo (Intercom Advanced for workflow routing + Loops paid plan)

## Drills Referenced

- `ab-test-orchestrator` — designs and runs A/B tests on deprecation messaging, CTA placement, and email copy using PostHog experiments
- the deprecation segment routing workflow (see instructions below) — dynamically routes each user to the optimal migration path (self-serve, guided, high-touch, rescue, light-touch) based on behavior
- `churn-prevention` — overlays deprecation-specific churn signals on standard churn detection and triggers contextual interventions
