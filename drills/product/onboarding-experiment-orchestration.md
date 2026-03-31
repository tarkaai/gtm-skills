---
name: onboarding-experiment-orchestration
description: Design, instrument, run, and evaluate A/B tests on onboarding flows — tours, emails, checklists, and empty states — to maximize activation rate
category: Product
tools:
  - PostHog
  - Intercom
  - Loops
  - n8n
fundamentals:
  - posthog-experiments
  - posthog-feature-flags
  - posthog-funnels
  - posthog-custom-events
  - intercom-product-tours
  - intercom-in-app-messages
  - loops-sequences
  - n8n-workflow-basics
---

# Onboarding Experiment Orchestration

This drill runs A/B tests specifically on onboarding surfaces: product tours, welcome emails, setup wizards, empty states, and activation nudges. It goes beyond generic experimentation by handling the unique constraints of onboarding — small cohort windows, one-shot exposure (each user onboards once), and the need to test across multiple channels simultaneously.

## Prerequisites

- PostHog with experiments, feature flags, and funnel tracking configured
- Intercom with product tours enabled
- Loops with transactional and sequence emails configured
- A defined activation metric (run `activation-optimization` drill first if undefined)
- At least 50 signups per week (below this, experiments take too long to reach significance)

## Input

- The onboarding surface to test (tour, email, checklist, empty state, or combination)
- Current activation rate (baseline)
- A specific hypothesis about what to change and why

## Steps

### 1. Identify the highest-leverage test surface

Query PostHog for your onboarding funnel drop-offs using `posthog-funnels`:

```
signup_completed → tour_started → tour_completed → activation_reached
```

Find the step with the largest absolute drop-off. This is where a test has the most potential impact. Rank test surfaces:

- **Tour content/flow** if tour_started → tour_completed drop-off > 40%
- **Tour trigger timing** if signup_completed → tour_started drop-off > 30%
- **Email sequence** if email_opened but activation_reached is low (users read but don't act)
- **Empty state design** if first_page_viewed → first_action_taken drop-off > 60%
- **Checklist/progress bar** if users complete steps 1-2 but abandon before activation

### 2. Structure the hypothesis

Format: "If we [specific change to onboarding surface], then [activation rate / tour completion / email CTR] will [increase by X%], because [reasoning from data]."

Examples of strong onboarding hypotheses:
- "If we reduce the product tour from 7 steps to 3 steps focused only on [core action], tour completion will increase by 20pp, because session recordings show users dismissing after step 4"
- "If we change the Day 1 email CTA from 'Explore your dashboard' to 'Create your first [object]', email-to-activation rate will increase by 5pp, because the current CTA leads to an empty dashboard with no clear next step"
- "If we add sample data to the empty state, first_action_taken within 10 minutes will increase by 15pp, because new users currently see a blank screen with no model for what 'good' looks like"

### 3. Set up the experiment in PostHog

Using `posthog-feature-flags`, create a feature flag for the experiment:
- Flag name: `onboarding-exp-{surface}-{date}` (e.g., `onboarding-exp-tour-length-2026-04`)
- Variants: `control` (current onboarding) and `treatment` (the change)
- Allocation: 50/50 split
- Filter: Only new users (`signup_date >= experiment_start_date`)
- Stickiness: Per-user (ensure each user always sees the same variant)

Using `posthog-experiments`, configure the experiment:
- Primary metric: activation_reached (within 14 days of signup)
- Secondary metrics: tour_completed, time_to_activation, day_7_retention
- Guardrail metrics: support_ticket_created (should not spike), signup_abandoned (should not spike)

### 4. Implement the variant

Depending on the test surface:

**Product tour test:** Using `intercom-product-tours`, create a second tour variant. Use the PostHog feature flag value (passed to Intercom via user properties or n8n webhook) to trigger the correct tour. Do not run both tours — the control group sees Tour A, treatment sees Tour B.

**Email sequence test:** Using `loops-sequences`, create a second email sequence variant. Using `n8n-workflow-basics`, build a workflow that reads the user's PostHog feature flag value and enrolls them in the matching Loops sequence.

**In-app message test:** Using `intercom-in-app-messages`, create parallel message variants targeted to users based on a custom attribute synced from the PostHog flag.

**Empty state test:** Implement via PostHog feature flag in your product code. Control sees current empty state; treatment sees the variant.

### 5. Instrument tracking

Using `posthog-custom-events`, ensure both variants emit identical events with a `variant` property:
- `onboarding_experiment_enrolled` with `{experiment_id, variant, persona_type}`
- All standard onboarding events (`tour_started`, `tour_step_completed`, `tour_completed`, `activation_reached`) should carry the `experiment_variant` property
- `onboarding_experiment_exposure` fires on first meaningful exposure to the variant (not just flag evaluation)

### 6. Run the experiment — do not peek

Set a calendar reminder for the planned end date. The minimum experiment duration:
- If >=50 signups/week: 14 days (to reach ~100 per variant)
- If 25-50 signups/week: 21 days
- If <25 signups/week: 28 days (and consider testing a bolder change)

Only check early if a guardrail metric fires (support ticket spike, error rate increase). Peeking at results mid-experiment and calling winners early leads to false positives.

### 7. Evaluate results

When the experiment reaches its planned sample size:

1. Pull results from PostHog: primary metric (activation rate) for control vs treatment
2. Check statistical significance (95% confidence minimum)
3. Check practical significance: is the lift large enough to justify permanent implementation?
4. Review secondary metrics: did the treatment improve activation without hurting retention or increasing support load?
5. Review session recordings for 5-10 users in each variant to understand the qualitative difference

Decision:
- **Winner clear (>=95% confidence, positive lift on primary, no secondary degradation):** Implement the winning variant permanently. Disable the feature flag. Log the result.
- **Inconclusive (< 95% confidence):** The variants perform similarly. Keep whichever is simpler. Log the learning.
- **Treatment worse:** Revert. Investigate why the hypothesis was wrong — the learning is more valuable than the result.
- **Mixed (primary improved, secondary degraded):** Do not implement. Redesign the variant to capture the primary win without the secondary cost.

Log the full result in Attio and PostHog (`experiment_completed` event with all metrics).

## Output

- A fully instrumented onboarding A/B test with clear hypothesis, tracking, and evaluation criteria
- Statistically rigorous result with documented decision
- Learnings logged for future hypothesis generation

## Triggers

Run this drill:
- After `experiment-hypothesis-design` selects an onboarding hypothesis as "next"
- When activation rate drops and investigation points to an onboarding surface
- On a regular cadence (e.g., one new onboarding experiment every 2-4 weeks at Scalable level)
