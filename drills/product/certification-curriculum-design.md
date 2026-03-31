---
name: certification-curriculum-design
description: Design a multi-module certification curriculum with assessments, scoring rubrics, and badge criteria for power users
category: Product
tools:
  - PostHog
  - Intercom
  - Loops
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - intercom-product-tours
  - intercom-in-app-messages
  - loops-sequences
---

# Certification Curriculum Design

This drill produces a complete certification curriculum: the module structure, assessment criteria, scoring rubric, pass/fail thresholds, and badge issuance logic. The output is a specification that the `certification-delivery-automation` drill wires into Intercom, Loops, and PostHog.

## Input

- Product feature inventory: list of all features grouped by complexity (core, intermediate, advanced, power)
- Definition of "power user" for this product: the set of actions and usage patterns that indicate deep product mastery
- Existing onboarding flow or activation metric (from the `onboarding-flow` drill, if run previously)

## Steps

### 1. Define certification tiers

Map your product's feature complexity into certification tiers. Each tier represents a level of product mastery that is independently valuable to the user.

| Tier | Name Pattern | Covers | Prerequisite |
|------|-------------|--------|--------------|
| 1 | Foundations | Core workflows: the actions every user must master to get value | None |
| 2 | Practitioner | Intermediate features: automations, integrations, team collaboration | Tier 1 complete |
| 3 | Expert | Advanced features: custom configurations, API usage, advanced reporting | Tier 2 complete |
| 4 | Power User | Power features: workflow optimization, cross-feature orchestration, performance tuning | Tier 3 complete |

Not every product needs 4 tiers. For Smoke testing, start with 1 tier (Foundations). Expand to 2-3 tiers at Baseline. Add the full 4-tier path at Scalable.

### 2. Design modules within each tier

Each tier contains 3-5 modules. Each module covers a single skill or feature area. Structure every module identically:

```
Module {N}: {Title}
├── Learning objective: "{User} can {specific action} to achieve {measurable result}"
├── Prerequisites: {modules that must be complete first}
├── Content: {what the user reads/watches/interacts with}
│   ├── Concept explanation (200-400 words or 2-3 min video)
│   ├── Guided walkthrough (in-app product tour via Intercom)
│   └── Reference documentation link
├── Practice task: {specific in-product action the user must perform}
└── Assessment: {how completion is verified}
```

The learning objective must be specific and measurable. Bad: "Understand reporting." Good: "Create a custom report filtering by date range and segment, export it as CSV, and schedule it to run weekly."

### 3. Design assessments for each module

Every module ends with an assessment that proves the user can perform the skill in the real product. Types of assessments:

**Action-based (preferred):** The user performs a specific action in the product. PostHog captures the event. If the event fires with the correct properties, the module is marked complete. Example: `posthog.capture('cert_assessment_completed', { module: 'custom-reports', action: 'report_created_with_filter_and_schedule', tier: 'practitioner' })`.

**Quiz-based (fallback):** For conceptual knowledge that cannot be tested via product actions. Use Intercom surveys or inline quizzes. Require 80%+ correct to pass. Track with PostHog: `posthog.capture('cert_quiz_completed', { module: 'data-model', score: 4, total: 5, passed: true })`.

**Multi-step workflow (advanced):** The user must complete a sequence of 3+ connected actions that demonstrate end-to-end mastery. Track the full sequence as a PostHog funnel.

Always prefer action-based assessments. If a skill cannot be assessed by product actions, reconsider whether it belongs in a certification (certifications prove ability, not knowledge).

### 4. Define the scoring rubric

For each tier, define:

- **Pass threshold:** Minimum score to earn the certification. Default: complete all modules + pass all assessments. No partial credit for tiers.
- **Time limit:** How long users have to complete each tier once started. Default: 14 days for Tier 1, 21 days for Tier 2, 30 days for Tier 3-4. After expiry, progress resets for that tier.
- **Attempt limit:** Maximum assessment retakes per module. Default: 3 attempts. If exhausted, require a 48-hour cooldown before retry.
- **Completion order:** Modules within a tier can be completed in any order, but tiers must be completed sequentially.

Track all scoring via PostHog events:

```javascript
posthog.capture('cert_tier_started', {
  tier: 'foundations',
  user_plan: userPlan,
  days_since_signup: daysSinceSignup
});

posthog.capture('cert_module_completed', {
  tier: 'foundations',
  module: 'core-workflows',
  assessment_type: 'action',
  attempts: 1,
  time_spent_minutes: 23
});

posthog.capture('cert_tier_completed', {
  tier: 'foundations',
  total_time_days: 4,
  total_modules: 4,
  assessment_retakes: 1
});
```

### 5. Design badge and credential issuance

When a user completes a tier:

1. Fire PostHog event: `cert_badge_earned` with tier, completion date, and user properties
2. Update Intercom user attribute: `certification_level = "{tier_name}"`
3. Update PostHog person property: `certification_level`, `certification_date_{tier}`
4. Trigger a celebration email via Loops (template per tier)
5. If product supports it, display badge in the user's profile/dashboard

Badge display is optional at Smoke level but required at Baseline and above. The PostHog events and Intercom attributes are required at every level.

### 6. Map the certification funnel

Using the `posthog-funnels` fundamental, define the full certification funnel for tracking:

```
cert_program_viewed (landing page or in-app prompt impression)
  -> cert_tier_started (user begins Tier 1)
    -> cert_module_completed (repeated per module)
      -> cert_assessment_completed (per module)
        -> cert_tier_completed (all modules done)
          -> cert_badge_earned (credential issued)
```

This funnel becomes the primary measurement surface for the certification-program play at all levels.

## Output

- Tier structure document: tier names, module list per tier, learning objectives
- Assessment specification per module: type, PostHog events, pass criteria
- Scoring rubric: pass thresholds, time limits, attempt limits
- PostHog event taxonomy: all certification-specific events and properties
- Badge issuance specification: what happens when each tier is completed
- Certification funnel definition for PostHog

## Triggers

Run once during initial play setup. Re-run when adding new tiers, redesigning assessments, or expanding to new product areas.
