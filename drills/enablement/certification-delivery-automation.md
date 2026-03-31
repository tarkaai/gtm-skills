---
name: certification-delivery-automation
description: Wire certification modules into always-on delivery via Intercom tours, Loops sequences, PostHog tracking, and n8n orchestration
category: Enablement
tools:
  - Intercom
  - Loops
  - PostHog
  - n8n
  - Attio
fundamentals:
  - intercom-product-tours
  - intercom-in-app-messages
  - loops-sequences
  - loops-audience
  - posthog-custom-events
  - posthog-funnels
  - posthog-feature-flags
  - n8n-triggers
  - n8n-workflow-basics
  - n8n-scheduling
  - attio-contacts
  - attio-custom-attributes
---

# Certification Delivery Automation

This drill takes the curriculum specification from `certification-curriculum-design` and wires it into automated delivery. The result is a certification program that runs without manual intervention: users discover the program, enroll, progress through modules, receive assessments, earn badges, and get nudged when they stall.

## Input

- Completed curriculum specification from `certification-curriculum-design` (tier structure, modules, assessments, scoring rubric, event taxonomy)
- Intercom configured with Messenger and Product Tours
- Loops account with sending domain verified
- PostHog tracking installed in the product
- n8n instance running

## Steps

### 1. Build the certification landing surface

The certification program needs a discovery point where eligible users learn about it and enroll. Using `intercom-in-app-messages`, create an in-app banner that appears for users who meet enrollment criteria:

- **Trigger conditions:** User has completed onboarding (activation event fired), has been active for 7+ days, and has NOT started the certification (`cert_tier_started` event absent)
- **Message:** "Become a certified [Product] power user — master advanced features and earn your badge"
- **CTA:** "Start certification" — links to the certification start flow
- **Frequency:** Show once per session, max 3 total impressions. After 3 dismissals, stop showing.

Track impressions and clicks with PostHog:

```javascript
posthog.capture('cert_program_viewed', {
  source: 'intercom_banner',
  user_plan: userPlan,
  days_since_activation: daysSinceActivation
});

posthog.capture('cert_program_enrolled', {
  source: 'intercom_banner',
  tier: 'foundations'
});
```

### 2. Build the enrollment email sequence

Using `loops-sequences`, create a 3-email enrollment nudge sequence for users who qualify but have not enrolled after 14 days:

**Email 1 (Day 14 post-activation, IF cert_program_enrolled is false):**
- Subject: "You're ready for the next level"
- Body: Explain the certification, what they will learn, and the badge they earn. One CTA linking to the certification start page.
- Skip if: User already enrolled

**Email 2 (Day 21, IF still not enrolled):**
- Subject: "X users earned their certification this month"
- Body: Social proof with count of recent certified users. Highlight a specific skill they will gain.
- Skip if: User already enrolled

**Email 3 (Day 28, IF still not enrolled):**
- Subject: "Last reminder: certification closes for this cohort"
- Body: Urgency-driven. If using cohorts, mention the cohort close date. If evergreen, highlight the time investment ("Most users finish in 4 days").
- Skip if: User already enrolled

Using `loops-audience`, segment users: property `certification_enrolled = false`, `activation_date exists`, `days_since_activation >= 14`.

### 3. Build module delivery via Intercom Product Tours

For each module in the curriculum, use `intercom-product-tours` to create a guided walkthrough:

- Each tour covers the module's practice task step by step
- Tour steps should point to real UI elements in the product
- Final step: "Now try it yourself" — dismisses the tour and lets the user perform the assessment action
- Tour completion fires a PostHog event: `cert_tour_completed` with `{module, tier}`

Using `intercom-in-app-messages`, create contextual nudges for each module:

- **Start nudge:** When user opens the product area relevant to the next incomplete module, show a tooltip: "Ready for Module {N}? Start the guided walkthrough."
- **Completion nudge:** After the assessment event fires, show a banner: "Module {N} complete! {X} of {Y} modules done in this tier."

### 4. Wire assessment tracking

Using `posthog-custom-events`, ensure every assessment event captures the full context:

```javascript
// Action-based assessment: fire when the user performs the required action
posthog.capture('cert_assessment_completed', {
  tier: tierName,
  module: moduleName,
  assessment_type: 'action', // or 'quiz' or 'workflow'
  passed: true,
  attempts: attemptCount,
  time_spent_seconds: elapsedTime
});

// Quiz assessment: fire when quiz is submitted
posthog.capture('cert_assessment_completed', {
  tier: tierName,
  module: moduleName,
  assessment_type: 'quiz',
  score: correctAnswers,
  total_questions: totalQuestions,
  passed: correctAnswers >= passingScore,
  attempts: attemptCount
});
```

Using `posthog-feature-flags`, gate assessment availability:

- Flag `cert_tier_{N}_available` controls whether the tier is accessible
- Flag evaluates PostHog person property: all prerequisite tier badges must be earned
- This prevents users from skipping tiers

### 5. Build the progress tracking and stall detection workflow

Using `n8n-scheduling`, create a daily workflow:

1. Query PostHog for users with `cert_tier_started` but NOT `cert_tier_completed` where start date > 7 days ago
2. For each stalled user, calculate: days since last module completion, modules remaining, assessment failures
3. Segment into stall categories:
   - **Mild stall (7-14 days inactive):** Send an Intercom in-app message next time they log in: "You're {X}% through {Tier} — pick up where you left off"
   - **Moderate stall (14-21 days inactive):** Send a Loops email: "Your certification progress is waiting — Module {N} is next"
   - **Hard stall (21+ days):** Send a Loops email from a human (founder or CSM): "Need help finishing your certification? Reply and I'll walk you through it"
4. Log all nudges in PostHog: `cert_stall_nudge_sent` with `{tier, stall_category, nudge_channel}`

### 6. Build badge issuance automation

Using `n8n-triggers`, create a webhook workflow triggered by the `cert_tier_completed` PostHog event:

1. Verify all modules in the tier are complete (prevent false triggers)
2. Using `attio-contacts`, update the person record: set `certification_level` to the completed tier name and `certification_date` to today
3. Using `attio-custom-attributes`, tag the contact with the badge for segmentation
4. Using `loops-sequences`, enroll the user in the badge celebration sequence:
   - Immediate: Congratulations email with badge image, what they mastered, and a CTA to share on LinkedIn
   - Day 2: "Now that you're certified, try {next tier or advanced use case}" — upsell to next tier or deeper engagement
5. Using `intercom-in-app-messages`, show a one-time celebration modal the next time they log in
6. Fire PostHog event: `cert_badge_earned` with full context

### 7. Build the certification dashboard

Using `posthog-funnels`, create the certification funnel:

```
cert_program_viewed -> cert_program_enrolled -> cert_tier_started
  -> cert_module_completed (first) -> cert_tier_completed -> cert_badge_earned
```

Build a PostHog dashboard with:

| Panel | Type | Purpose |
|-------|------|---------|
| Enrollment funnel | Funnel | View-to-enroll-to-start conversion |
| Completion rate by tier | Bar chart | Which tiers have the highest drop-off |
| Time to completion by tier | Line chart | Is certification getting faster over time |
| Stalled users by category | Table | How many users are stuck and where |
| Badge earned trend | Trend line | Certifications issued per week |
| Certified vs non-certified retention | Cohort chart | Does certification actually improve retention |

## Output

- Intercom enrollment banner with targeting rules
- Loops 3-email enrollment nudge sequence
- Intercom Product Tours for each module
- PostHog assessment tracking with feature flag gating
- n8n daily stall detection and nudge workflow
- n8n badge issuance webhook workflow
- PostHog certification dashboard with 6 panels

## Triggers

Run once during Baseline setup. Re-run when adding new tiers (Scalable) or redesigning the enrollment funnel. The stall detection workflow runs daily. Badge issuance runs on every tier completion event.
