---
name: empty-state-onboarding-scalable
description: >
  Empty State Guidance — Scalable Automation. Personalize empty states by persona, scale
  template curation with automated recommendations, run systematic A/B tests across all
  surfaces, and maintain 45%+ CTR at 500+ monthly users.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=45% aggregate empty state CTR sustained across 500+ monthly users encountering empty states"
kpis: ["Aggregate empty state CTR", "Per-surface CTR", "Per-persona CTR", "Template selection rate", "Experiment velocity (tests/month)", "Activation rate from empty state path"]
slug: "empty-state-onboarding"
install: "npx gtm-skills add product/onboard/empty-state-onboarding"
drills:
  - onboarding-personalization
  - ab-test-orchestrator
  - empty-state-scaling
---

# Empty State Guidance — Scalable Automation

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Empty state experiences cover all product surfaces (P0, P1, P2). P0 surfaces serve persona-specific variants with tailored CTAs, templates, and sample data. A template recommendation engine curates the most relevant templates per user. Systematic A/B testing runs continuously with 2+ experiments per month. Aggregate CTR holds at 45%+ with 500+ monthly users encountering empty states.

## Leading Indicators

- Per-persona CTR variance narrows (all personas within 10pp of each other) within 4 weeks
- Template recommendation engine increases template selection rate by 15%+ over random ordering
- A/B test pipeline runs 2+ experiments per month with clear winners adopted
- P1 and P2 surfaces show meaningful CTR (>25%) as they are treated
- Lifecycle email bridge re-engages 10%+ of users who did not convert in-product

## Instructions

### 1. Build persona-specific empty state variants

Run the `onboarding-personalization` drill to define 2-4 user personas and their detection logic. Then apply persona variants to each P0 empty state:

For each P0 surface, create feature flag variants:
- **Variant per persona:** Different headline, CTA text, and template set tailored to that persona's goal
- **Fallback variant:** For users without a detected persona, use the best-performing generic variant from Baseline

Example for a project management product's dashboard empty state:
- **Solo Creator persona:** "Track your ideas in one place. Start with a template." + creative project templates
- **Team Lead persona:** "Get your team organized. Create a shared project." + team workflow templates
- **Developer persona:** "Import your existing data or connect an integration." + API import CTA

Deploy variants via PostHog feature flags keyed on the user's `persona_type` property.

### 2. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill to set up a testing pipeline for empty state surfaces. Run experiments in this order:

**Month 1:**
- Test CTA copy on the highest-traffic P0 surface (3 variants, 200+ users per variant)
- Test sample data vs template gallery on the second-highest-traffic P0 surface

**Month 2:**
- Test template count (3 vs 5 vs 7) on the surface where templates are most used
- Test the visual treatment of P1 surfaces (contextual CTA vs minimal text link)

For each test, use `posthog-experiments` to create the experiment, set the primary metric (`empty_state_cta_clicked` rate or `first_item_created` rate), and let it run to statistical significance. Document every result — wins AND losses — in PostHog annotations.

### 3. Scale empty state coverage and template engine

Run the `empty-state-scaling` drill to:
1. Design and deploy empty states for all P1 and P2 surfaces
2. Build the n8n template recommendation engine that curates templates per user based on persona, industry, and past behavior
3. Set up the weekly template performance analysis job
4. Build the lifecycle email bridge that targets users who viewed P0 empty states 2+ times without creating an item

Monitor the template recommendation engine weekly. If a template has <5% selection rate over 4 weeks, replace it with a new template and track whether the replacement performs better.

### 4. Build the aggregate performance dashboard

Create a PostHog dashboard with:
- Overall empty state CTR trend (12-week line chart with 45% target line)
- Per-surface CTR table ranked by CTR descending
- Per-persona CTR comparison chart
- Template selection and conversion rates
- Experiment log (active tests, recent results)
- Email bridge performance (open rate, click rate, conversion to `first_item_created`)

Set automated alerts:
- Any P0 surface CTR drops below 40% for 7+ days: Slack alert
- Overall aggregate CTR drops below 45%: Slack alert
- Template recommendation engine produces zero recommendations for >10% of users: Slack alert (data gap)

### 5. Evaluate against threshold

After 2 months, compute:
- **Aggregate empty state CTR:** total `empty_state_cta_clicked` / total `empty_state_viewed` across ALL surfaces
- **User volume:** count of unique users with at least one `empty_state_viewed` event in the last 30 days
- **Threshold:** CTR >= 45% AND user volume >= 500

If PASS: Document per-surface and per-persona CTR. Note which experiments produced the biggest lifts. Prepare for Durable by ensuring 4+ weeks of stable performance data exist. Proceed to Durable.

If FAIL: Identify the drag. If aggregate CTR is <45% but some surfaces are >50%, focus on the underperforming surfaces. If CTR was high at smaller volume but dropped at 500+, investigate whether the new user mix changed (different personas, different acquisition channels) and adjust variants accordingly.

## Time Estimate

- 12 hours: Build persona-specific empty state variants for all P0 surfaces
- 8 hours: Design and deploy P1 and P2 empty state treatments
- 10 hours: Build and configure the template recommendation engine
- 8 hours: Set up and run 4+ A/B experiments
- 6 hours: Build the lifecycle email bridge
- 8 hours: Build the aggregate dashboard and alert system
- 4 hours: Weekly monitoring and optimization (2h/week for 2 months, averaged)
- 4 hours: Final evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Events, feature flags, experiments, session recordings, dashboards | Free tier covers up to 1M events/mo; paid starts at $0.00005/event. [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app messages, persona-targeted banners, stuck-user nudges | Essential: $29/seat/mo (annual). Product Tours add-on may apply. [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Lifecycle email bridge sequence | $49/mo for up to 5,000 contacts. [loops.so/pricing](https://loops.so/pricing) |
| n8n | Template recommendation engine, scheduled jobs, alert workflows | Starter: ~$24/mo (cloud) or free self-hosted. [n8n.io/pricing](https://n8n.io/pricing/) |

**Estimated play-specific cost at this level:** $100-200/mo (Intercom seat + Loops + n8n cloud)

## Drills Referenced

- `onboarding-personalization` — define personas, build detection logic, route users to persona-specific tours
- `ab-test-orchestrator` — design, run, and analyze A/B tests on empty state surfaces
- `empty-state-scaling` — expand coverage to all surfaces, build template engine, run systematic testing at scale
