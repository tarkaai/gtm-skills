---
name: role-based-onboarding-baseline
description: >
  Persona-Based Onboarding — Baseline Run. Wire persona-specific onboarding to always-on
  automation: behavioral email sequences per persona via Loops, PostHog-triggered n8n workflows,
  and A/B test of personalized vs generic onboarding on 50% of new signups over 2 weeks.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥55% activation rate for personalized cohort AND ≥12pp lift over generic control"
kpis: ["Activation rate by persona", "Activation lift vs control", "Tour completion rate", "Email open rate per persona", "Time to activation"]
slug: "role-based-onboarding"
install: "npx gtm-skills add product/onboard/role-based-onboarding"
drills:
  - onboarding-sequence-design
  - onboarding-sequence-automation
  - posthog-gtm-events
---

# Persona-Based Onboarding — Baseline Run

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Personalized onboarding achieves ≥55% activation rate AND ≥12 percentage point lift over the generic control group, sustained over a 2-week always-on run. Email sequences are fully automated — no manual enrollment or sending.

## Leading Indicators

- Email open rate per persona exceeds 40% (sequences are relevant to the persona)
- Email click-through rate per persona exceeds 8% (CTAs match the persona's next step)
- Tour completion rate per persona exceeds 65% (improved from Smoke with email reinforcement)
- Time to activation for personalized users is 30%+ shorter than control
- Control group activation rate provides a stable baseline for comparison

## Instructions

### 1. Set up the event taxonomy

Run the `posthog-gtm-events` drill. Define a standard event taxonomy for this play:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `onboarding_enrolled` | User classified and enrolled in persona path | `persona_type`, `persona_confidence`, `signup_source` |
| `onboarding_tour_started` | Product tour begins | `persona_type`, `tour_variant` |
| `onboarding_tour_completed` | All tour steps finished | `persona_type`, `duration_seconds` |
| `onboarding_email_sent` | Loops sends an onboarding email | `persona_type`, `email_step`, `subject` |
| `onboarding_email_opened` | User opens onboarding email | `persona_type`, `email_step` |
| `onboarding_email_clicked` | User clicks CTA in onboarding email | `persona_type`, `email_step`, `cta_url` |
| `onboarding_activation_reached` | User completes persona-specific activation action | `persona_type`, `days_since_signup` |

Build PostHog funnels:
- Per-persona: `onboarding_enrolled → onboarding_tour_completed → onboarding_activation_reached`
- Email attribution: `onboarding_email_sent → onboarding_email_opened → onboarding_email_clicked → onboarding_activation_reached`
- Cohort comparison: personalized cohort vs control cohort activation rate

### 2. Design persona-specific email sequences

Run the `onboarding-sequence-design` drill. For each persona, design a 5-7 email sequence where:

- **Email 1 (immediate)**: Welcome email referencing the persona's specific goal. CTA links to the first step of their activation path (not generic dashboard).
- **Email 2 (24h, if milestone 1 not reached)**: "Did you get stuck?" email with a persona-specific tutorial or walkthrough.
- **Email 3 (48h or on milestone completion)**: Use case example matching the persona's role and industry.
- **Email 4 (Day 5, if not activated)**: Social proof from similar users ("Other [persona role] teams activated by doing X").
- **Email 5 (Day 7, if not activated)**: Personal help offer with Cal.com booking link.
- **Email 6 (on activation)**: Celebration email with next recommended action specific to the persona.
- **Email 7 (2 days after activation)**: Bridge to regular usage — advanced feature or integration relevant to the persona.

Each email uses skip logic: exit the non-activated branch when `onboarding_activation_reached` fires for this user.

### 3. Wire the automation pipeline

Run the `onboarding-sequence-automation` drill. Build n8n workflows that connect PostHog events to Loops:

**Enrollment workflow**: `signup_completed` PostHog webhook → n8n extracts user data + `persona_type` → creates Loops contact with persona properties → Loops auto-starts the persona-matched sequence.

**Milestone sync workflow**: Each `milestone_N_completed` PostHog webhook → n8n updates Loops contact properties → Loops sequence branches/skips emails based on milestone status.

**Activation exit workflow**: `onboarding_activation_reached` PostHog webhook → n8n updates Loops contact with `activated: true` → Loops exits the non-activated branch and sends the celebration email.

**Email event tracking**: Loops webhooks for open/click events → n8n routes to PostHog as `onboarding_email_opened` / `onboarding_email_clicked` events.

### 4. Launch the A/B test

Create a PostHog feature flag `onboarding-personalization-baseline` with two variants:
- **Treatment (50%)**: Full persona-specific onboarding (tours + emails)
- **Control (50%)**: Existing generic onboarding (one tour + generic email sequence)

Enable the flag for all new signups. Ensure randomization is user-level (each user always sees the same variant).

**Human action required:** Review the first 10 users through each path. Verify emails arrive on schedule, tours trigger correctly, and the PostHog funnel shows data for both cohorts. Fix any pipeline breaks before the full 2-week run.

### 5. Evaluate against threshold

After 2 weeks, compute:
- **Personalized cohort activation rate**: must be ≥55%
- **Lift over control**: must be ≥12 percentage points
- **Per-persona breakdown**: identify which personas activate best and worst

If PASS: Document the winning configuration. Disable the control branch and roll personalized onboarding to 100%. Proceed to Scalable.

If FAIL but lift is positive (personalized > control but below threshold): Analyze per-persona funnels. Find the persona with the worst activation rate. Check tour completion and email engagement for that persona — the bottleneck is usually in one specific step. Fix that step and re-run for 1 more week.

If FAIL with no lift: The personalization approach may be wrong. Check: Are personas correctly classified? Is the activation metric right for each persona? Are the tours actually different enough to matter? Revisit persona definitions.

## Time Estimate

- 4 hours: Event taxonomy setup and PostHog funnel creation
- 5 hours: Designing 2-3 persona-specific email sequences (content + branching logic)
- 4 hours: n8n workflows (enrollment, milestone sync, activation exit, email tracking)
- 1 hour: Feature flag setup and A/B test launch
- 2 hours: Monitoring, debugging, and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, feature flags, A/B test | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Product tours (from Smoke, maintained) | Essential: $29/seat/mo annual ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Persona-specific email sequences | Free up to 1,000 contacts; $49/mo for up to 5,000 ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Workflow automation (PostHog → Loops bridge) | Standard stack |
| Cal.com | Booking link in help-offer emails | Free tier available ([cal.com/pricing](https://cal.com/pricing)) |

**Estimated play-specific cost at this level:** $0-49/mo (Loops free tier covers up to 1,000 contacts; $49/mo if >1,000 onboarding contacts)

## Drills Referenced

- `onboarding-sequence-design` — design persona-specific email content, triggers, timing, and branching logic
- `onboarding-sequence-automation` — wire PostHog events to Loops sequences via n8n for always-on delivery
- `posthog-gtm-events` — define the standard event taxonomy for all onboarding tracking
