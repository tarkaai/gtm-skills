---
name: role-based-onboarding-smoke
description: >
  Persona-Based Onboarding — Smoke Test. Define 2-3 user personas, build persona-specific
  product tours in Intercom, route users via PostHog feature flags, and measure per-persona
  activation rate against a 45% threshold on 20-50 test users.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥45% activation rate for at least one persona in a 20-50 user test"
kpis: ["Activation rate by persona", "Tour completion rate by persona", "Time to activation by persona"]
slug: "role-based-onboarding"
install: "npx gtm-skills add product/onboard/role-based-onboarding"
drills:
  - onboarding-personalization
  - threshold-engine
---

# Persona-Based Onboarding — Smoke Test

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

At least one persona-specific onboarding path achieves ≥45% activation rate in a 20-50 user test group over 1 week. You have validated that role-based routing works and that at least one persona converts better than the generic onboarding baseline.

## Leading Indicators

- Tour completion rate per persona exceeds 60% (users finish the tour they are shown)
- Time to activation for persona-matched users is shorter than for unmatched users
- Tour dismissal rate per persona is below 30% (the content is relevant)
- Per-persona activation rates diverge (proving that different personas need different paths)

## Instructions

### 1. Define 2-3 user personas

Run the `onboarding-personalization` drill, Step 1. Analyze your existing activated users in PostHog to identify 2-3 distinct persona segments based on role, use case, company size, and signup source. Each persona must have a different "aha moment" — the action that correlates with retention for that user type.

Document each persona:
- **Name**: A short label (e.g., "solo_creator", "team_lead", "technical_builder")
- **Detection signal**: How to identify this persona at signup (role field, email domain, referral source)
- **Activation action**: The specific action that means this persona "got it" (created first project, invited teammate, connected integration)
- **Tour focus**: The 3-5 steps that get this persona to their activation action fastest

### 2. Build persona-specific product tours

Run the `onboarding-personalization` drill, Steps 3-5. For each persona, create a product tour in Intercom with 3-5 interactive steps. Each tour guides the user directly to their persona-specific activation action.

Set up a PostHog feature flag `onboarding-tour-persona` with variants matching your personas. Route users to the correct tour based on their `persona_type` property. Users without a detected persona get the existing generic tour as a fallback.

**Human action required:** Review each product tour before launch. Walk through each tour manually in the product to verify: steps render correctly, interactive elements work, the tour leads to the activation action, and the copy is clear and specific to the persona.

### 3. Instrument per-persona tracking

Run the `onboarding-personalization` drill, Step 6. Track these PostHog events with `persona_type` as a property on each:

- `tour_started` — user saw the first step of their persona tour
- `tour_step_completed` — user completed a tour step (include `step_number`, `step_name`)
- `tour_completed` — user finished all tour steps
- `tour_dismissed` — user closed the tour early (include `step_number` where they stopped)
- `activation_reached` — user completed their persona-specific activation action

Build a per-persona activation funnel in PostHog: `tour_started → tour_completed → activation_reached`.

### 4. Launch to test group

Enable the `onboarding-tour-persona` feature flag for 20-50 new signups using PostHog's percentage rollout (or target a specific cohort). Monitor the PostHog Live Events stream to confirm events fire correctly for the first 5 users.

### 5. Evaluate against threshold

Run the `threshold-engine` drill. After 7 days, pull per-persona metrics:

- Activation rate per persona (target: ≥45% for at least one persona)
- Tour completion rate per persona
- Time to activation per persona
- Comparison to generic onboarding baseline

If ≥45% activation for at least one persona: PASS. Document the winning persona path and proceed to Baseline.

If FAIL: Investigate the per-persona funnel. If tour completion is low, simplify the tour. If tour completion is high but activation is low, the tour is not leading to the right action — redefine the activation metric or restructure the tour steps. Iterate and re-run.

## Time Estimate

- 2 hours: Persona definition and activation metric analysis
- 2 hours: Building 2-3 product tours in Intercom + PostHog feature flag setup
- 1 hour: Event instrumentation and funnel creation
- 1 hour: Launch, monitoring, and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, event tracking, funnel analysis | Free tier: 1M events + 1M feature flag requests/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Product tours for persona-specific onboarding | Essential: $29/seat/mo annual ([intercom.com/pricing](https://intercom.com/pricing)) |

**Estimated play-specific cost at this level:** Free (PostHog free tier sufficient for 20-50 users; Intercom assumed as standard stack)

## Drills Referenced

- `onboarding-personalization` — define personas, build tours, set up routing, instrument per-persona tracking
- `threshold-engine` — evaluate activation rate against ≥45% pass threshold
