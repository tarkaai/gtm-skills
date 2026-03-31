---
name: empty-state-scaling
description: Scale empty state experiences across all product surfaces with persona variants, automated template curation, and multi-surface A/B testing
category: Product
tools:
  - PostHog
  - Intercom
  - n8n
  - Loops
fundamentals:
  - posthog-feature-flags
  - posthog-experiments
  - posthog-cohorts
  - posthog-custom-events
  - intercom-in-app-messages
  - intercom-user-properties
  - n8n-triggers
  - n8n-scheduling
  - loops-sequences
---

# Empty State Scaling

This drill takes validated empty state designs (from the `empty-state-design` drill) and scales them across all product surfaces with persona-based variants, automated template curation, and systematic A/B testing. The goal is to maintain high CTR as user volume grows from dozens to hundreds to thousands.

## Input

- Validated empty state designs for P0 surfaces with baseline CTR data from the Baseline level
- PostHog tracking flowing on all empty state surfaces
- At least 2 user personas defined (from the `onboarding-personalization` drill)
- 500+ monthly active users seeing empty states

## Steps

### 1. Expand empty state coverage to all surfaces

Using the audit from the `empty-state-design` drill, design and implement empty states for all remaining P1 and P2 surfaces. Prioritize by traffic: check PostHog to see which P1/P2 surfaces users actually visit. A P2 surface visited by 80% of users matters more than a P1 surface visited by 5%.

For each new surface, implement the standard tracking events (`empty_state_viewed`, `empty_state_cta_clicked`, `first_item_created`) using the `posthog-custom-events` fundamental. Add the surface to the master empty state dashboard.

### 2. Build persona variants for P0 surfaces

Using the `posthog-feature-flags` fundamental, create feature flags for each P0 empty state that serve different content based on user persona. For each persona variant:

- **Headline:** Frame the value proposition in terms of that persona's goal. A "Team Lead" sees "Organize your team's work" while a "Solo Creator" sees "Track your projects in one place."
- **Templates:** Show templates relevant to the persona's use case. A developer persona sees API integration templates. A marketer persona sees campaign templates.
- **CTA text:** Match the persona's vocabulary. "Create your first project" vs "Set up your workspace" vs "Import your data."
- **Sample data:** If using sample data, tailor the example items to the persona's domain.

Using `intercom-user-properties`, sync the persona classification to drive in-app message variants.

### 3. Build the template recommendation engine

Using `n8n-triggers`, create a workflow that curates template recommendations per user:

1. On `empty_state_viewed` event, n8n receives the webhook
2. Look up the user's persona, industry, and signup source in PostHog
3. Query the template catalog for the top 3 templates matching the user's profile
4. Return the template IDs to the product via API response or feature flag payload
5. Track which templates are shown and selected

Using `n8n-scheduling`, run a weekly job that analyzes template selection data:
- Which templates have the highest `first_item_created` conversion rate?
- Which templates are shown but never selected (remove or redesign)?
- Are there persona/industry combinations with no good template (create one)?

### 4. Run systematic A/B tests across surfaces

Using `posthog-experiments`, set up experiments on each P0 surface. Test one variable at a time:

**Round 1 — CTA copy:** Test 3 headline + CTA combinations per surface. Run each test until 200+ users per variant. Measure `empty_state_cta_clicked` rate.

**Round 2 — Visual treatment:** Test sample data vs template gallery vs static illustration. Measure `first_item_created` rate (not just clicks but actual item creation).

**Round 3 — Template count:** Test showing 3 vs 5 vs 7 templates. More options can cause choice paralysis. Measure `empty_state_template_selected` rate and time-to-selection.

**Round 4 — Timing:** Test whether showing the empty state immediately vs after a 3-second delay with a welcome animation affects CTR.

Log all experiment results in PostHog with `posthog-custom-events` event `experiment_completed` with properties: `surface`, `variable_tested`, `winner`, `lift_percentage`, `confidence`.

### 5. Build the lifecycle email bridge

Using `loops-sequences`, create an email sequence that reinforces empty state CTAs for users who did not convert in-product:

- **Email trigger:** `empty_state_viewed` fired 2+ times for the same P0 surface without `first_item_created`
- **Email 1 (24h after first view):** "We noticed you haven't [created your first X] yet. Here's a 60-second walkthrough." Include a deep link directly to the empty state screen.
- **Email 2 (72h after first view):** "Here's how [similar company] set up their [X] in under 5 minutes." Social proof with a direct link to the template gallery.
- **Skip condition:** If `first_item_created` fires, exit the sequence immediately.

### 6. Monitor aggregate performance at scale

Using `posthog-cohorts`, create a cohort of "users who activated from empty states" — defined as users whose `first_item_created` event occurred within 60 seconds of an `empty_state_cta_clicked` event. Track this cohort's size weekly.

Build a PostHog dashboard showing:
- Overall empty state CTR across all surfaces (aggregated)
- Per-surface CTR trend (weekly)
- Per-persona CTR comparison
- Template selection rates
- Email bridge conversion rate
- Experiment velocity (tests run per month)

Set alerts: if any P0 surface CTR drops below 40% for 7 consecutive days, fire a Slack alert.

## Output

- Empty state experiences on all product surfaces (P0, P1, P2)
- Persona-specific variants on all P0 surfaces
- Template recommendation engine
- Systematic A/B testing pipeline with logged results
- Lifecycle email bridge for non-converting users
- Aggregate performance dashboard with alerts

## Triggers

- Template curation job: weekly via n8n
- Experiment monitoring: continuous via PostHog
- Email bridge: event-triggered via Loops
- Performance alerts: daily via n8n
