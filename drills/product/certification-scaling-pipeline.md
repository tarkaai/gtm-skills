---
name: certification-scaling-pipeline
description: Scale the certification program to multiple tiers, personas, and cohorts with automated content generation and persona-based routing
category: Product
tools:
  - PostHog
  - Intercom
  - Loops
  - n8n
  - Attio
fundamentals:
  - posthog-cohorts
  - posthog-feature-flags
  - posthog-experiments
  - posthog-dashboards
  - intercom-in-app-messages
  - intercom-product-tours
  - loops-sequences
  - loops-audience
  - n8n-workflow-basics
  - n8n-scheduling
  - attio-lists
  - attio-custom-attributes
---

# Certification Scaling Pipeline

This drill takes a working 1-2 tier certification program (proven at Baseline) and scales it to serve multiple user personas, all certification tiers, and cohort-based delivery. The goal is to go from dozens of certified users to hundreds per month without proportional manual effort.

## Input

- Certification program running at Baseline with proven enrollment and completion rates
- PostHog data showing certification funnel by segment (plan type, role, use case)
- At least 30 certified users to analyze patterns
- Curriculum spec covering all 4 tiers from `certification-curriculum-design`

## Steps

### 1. Segment users into certification personas

Using `posthog-cohorts`, analyze your certified and non-certified users to identify distinct personas. Segment by:

- **Role:** Admin vs end-user vs manager — each persona needs different modules emphasized
- **Use case:** What primary workflow they use the product for
- **Plan type:** Free vs paid vs enterprise — different feature access affects which modules are relevant
- **Engagement level:** Power users (daily active) vs occasional users (weekly) vs dormant (monthly)

Create 3-5 certification personas. For each persona, document:
- Which modules are most relevant (priority order)
- Which modules can be skipped (not applicable to their use case)
- Recommended pace (aggressive: complete in 1 week vs standard: 2-3 weeks)
- Enrollment trigger (what signals this persona is ready)

### 2. Build persona-based certification paths

Using `posthog-feature-flags`, create flags that control which modules each persona sees:

- Flag `cert_persona` evaluates PostHog person properties (role, plan, primary_use_case) and assigns a persona
- Flag `cert_modules_{persona}` returns the ordered module list for that persona
- Flag `cert_pace_{persona}` returns timing parameters (email frequency, stall thresholds)

Using `intercom-product-tours`, create persona-variant tours. Each module gets 2-3 tour variants showing the same skill applied to different use cases. The flag determines which variant the user sees.

### 3. Launch cohort-based delivery

Instead of evergreen enrollment (anyone starts anytime), introduce cohort-based certification runs:

Using `n8n-scheduling`, create a bi-weekly workflow that:

1. Queries PostHog for all users who qualify for certification but have not enrolled
2. Batches them into a cohort with a shared start date (next Monday)
3. Enrolls the cohort by updating a PostHog person property: `cert_cohort = "{date}"`
4. Triggers the enrollment email via Loops with cohort-specific copy: "You're joining {N} other users starting certification on {date}"
5. Creates an Attio list for the cohort using `attio-lists` for tracking

Cohort benefits:
- Social proof: "23 other users are working on Module 3 this week"
- Accountability: clear start and end dates
- Measurement: compare cohort-over-cohort completion rates

Using `intercom-in-app-messages`, show cohort progress: "Your cohort is {X}% through Tier 1 — you're {ahead/behind} the average"

### 4. Build the multi-tier expansion funnel

Using `loops-sequences`, create tier-transition sequences:

**Tier 1 -> Tier 2 bridge (triggered on Tier 1 badge earned):**
- Day 0: Celebration + "Ready for Practitioner? Here's what you'll master"
- Day 3: "Top Practitioners use {feature} to save {X} hours/week" (social proof + value)
- Day 7: "Your Practitioner certification starts with your cohort on {date}"

**Tier 2 -> Tier 3 bridge (triggered on Tier 2 badge earned):**
- Same pattern, with Expert-tier content

**Tier 3 -> Tier 4 bridge (triggered on Tier 3 badge earned):**
- Personalized: highlight the power user features most relevant to their usage patterns

Using `posthog-experiments`, A/B test bridge sequence variants:
- Variant A: Immediate start (enroll in next tier same day)
- Variant B: Rest period (7-day gap between tiers)
- Variant C: Teaser content (show a preview of Tier 2 skills before enrolling)

Track: Tier 2+ enrollment rate and completion rate per variant.

### 5. Automate certification content refresh

Using `n8n-scheduling`, create a monthly workflow:

1. Query PostHog for module-level completion rates and assessment pass rates
2. Flag modules with <60% first-attempt pass rate — these are too hard or unclear
3. Flag modules with >95% first-attempt pass rate — these may be too easy or not testing real skills
4. Flag modules where median time-to-complete is >2x the expected time — the content or task is confusing
5. Generate a content refresh report with specific modules to update and why
6. Store the report in Attio as a note on the certification campaign record

### 6. Build the scaled certification dashboard

Using `posthog-dashboards`, extend the baseline dashboard with scaling metrics:

| Panel | Type | Purpose |
|-------|------|---------|
| Certifications per month (trend) | Trend line | Are we scaling? |
| Completion rate by persona | Bar chart | Which personas succeed, which struggle |
| Cohort-over-cohort completion | Cohort chart | Is each cohort better than the last |
| Tier transition rate | Funnel | What % of Tier 1 completers start Tier 2, etc. |
| Module difficulty heatmap | Heatmap | First-attempt pass rate by module |
| Stall rate by persona x tier | Table | Where do specific personas get stuck |
| Certified user retention vs non-certified | Line chart | The business case for certification |

Set alerts:
- Monthly certification volume drops below target (100/month at Scalable)
- Any persona's completion rate drops below 50%
- Tier transition rate drops below 40%

## Output

- 3-5 certification persona definitions with personalized module paths
- PostHog feature flags for persona routing
- Persona-variant Intercom Product Tours
- Bi-weekly cohort enrollment automation in n8n
- Tier-transition email sequences in Loops (3 bridges)
- A/B test on tier transition timing
- Monthly content refresh automation
- Scaled certification dashboard with 7 panels

## Triggers

Run once during Scalable setup. The cohort enrollment runs bi-weekly. Content refresh runs monthly. Dashboard is reviewed weekly.
