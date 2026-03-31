---
name: freemium-model-smoke
description: >
  Freemium Tier Strategy — Smoke Test. Define the free tier boundary, deploy one lead capture
  surface with a self-serve signup flow, onboard a small batch of free users, and validate that
  at least 5% convert to paid within 14 days.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=5% free-to-paid conversion within 14 days of signup"
kpis: ["Free signups", "Free-to-paid rate", "Median days to upgrade"]
slug: "freemium-model"
install: "npx gtm-skills add product/onboard/freemium-model"
drills:
  - lead-capture-surface-setup
  - onboarding-flow
  - threshold-engine
---

# Freemium Tier Strategy — Smoke Test

> **Stage:** Product -> Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Prove the concept: a free tier with clear limits drives signups, and a meaningful percentage of those free users self-serve upgrade to paid. No automation, no always-on. Run one manual cycle with a small cohort (10-50 free signups) and measure how many convert. The pass threshold is 5%+ free-to-paid conversion within 14 days of signup.

## Leading Indicators

- Signup form or landing page produces 10+ free signups within the test window
- At least 60% of free signups complete the first value action (project created, workflow run, data imported) within 48 hours
- At least 3 free users encounter a plan limit or feature gate during normal usage
- At least 1 free user self-serve upgrades to paid without human outreach

## Instructions

### 1. Define the free tier boundary

Before building anything, document the exact line between free and paid. The free tier must be useful enough to demonstrate value but limited enough to create natural upgrade pressure. Define:

- **Free limits**: which resources are capped (projects, seats, API calls, storage) and at what number
- **Free features**: which features are available vs. gated behind paid (list every feature and its tier)
- **Upgrade triggers**: which specific moments will a free user hit the wall and want more (creating their 6th project when the limit is 5, inviting a 4th teammate when the limit is 3, trying to use an advanced feature)

**Human action required:** Review the free tier definition with the product team. The most common mistake is making the free tier too generous (no upgrade pressure) or too restrictive (users never reach the value moment). The free tier should let users experience the core workflow completely, then limit scale or advanced capabilities.

### 2. Deploy the signup surface

Run the `lead-capture-surface-setup` drill to build the self-serve signup flow. For this play, use the short form variant:

- Fields: name, work email, company name (optional)
- Submit button: "Start free" or "Get started for free"
- Post-signup redirect: directly into the product (not to a "check your email" page)
- PostHog tracking: `cta_impression`, `cta_clicked`, `lead_captured` events firing on the signup page

Wire the n8n webhook: signup -> create Attio contact record with `plan_tier: free` and `signup_source` property -> enroll in Loops onboarding sequence.

### 3. Build the free-user onboarding experience

Run the `onboarding-flow` drill configured for the free tier:

- Map 4 onboarding milestones: account created -> profile completed -> first value action taken -> value moment reached (first result, completed workflow, or shared output)
- Build an Intercom product tour (3-4 steps) that guides new free users to the first value action
- Create a 5-email Loops sequence: welcome (immediate), quick-start guide (Day 1), social proof (Day 3), feature discovery (Day 5), check-in (Day 7)
- Each email skips if the user already completed the relevant milestone
- Instrument the onboarding funnel in PostHog: `signup_completed` -> `profile_completed` -> `first_value_action` -> `value_moment_reached`

Focus the entire onboarding experience on reaching the value moment. Do not mention paid features or upgrades during onboarding. Let the user experience the free tier fully before encountering any limit.

### 4. Observe limit encounters and upgrade behavior

Once 10+ free users have been onboarded, monitor their usage manually:

- Check PostHog for users approaching plan limits (80%+ of any capped resource)
- Check for users who attempted a gated feature (PostHog event: `feature_gate_hit`)
- Note which limits users hit first, how they react, and whether they attempt to upgrade

For the Smoke test, do not build automated upgrade prompts. Observe the natural behavior: do free users who hit a limit attempt to upgrade on their own? This validates that the free tier boundary is in the right place.

### 5. Evaluate against threshold

Run the `threshold-engine` drill. After 14 days from the first batch of signups:

- Free-to-paid rate = (users who upgraded to paid) / (total free signups)
- Median days to upgrade = median time from signup to upgrade for those who converted
- Pass threshold: >=5% free-to-paid conversion

If PASS: the free tier boundary creates natural upgrade pressure and the value moment is compelling enough. Proceed to Baseline.

If FAIL, diagnose:
- Did users complete onboarding? (If <60% reached value moment: onboarding friction, simplify the first-run experience)
- Did users hit plan limits? (If <30% encountered a limit: free tier is too generous, tighten limits)
- Did users who hit limits attempt to upgrade? (If not: the upgrade path is not visible or the paid tier value proposition is unclear)
- Did users who started checkout complete it? (If not: pricing page or checkout UX problem)

## Time Estimate

- 1 hour: define the free tier boundary (features, limits, gated capabilities)
- 1.5 hours: deploy signup surface and wire PostHog + CRM routing
- 1.5 hours: build onboarding flow (Intercom tour + Loops sequence + PostHog funnel)
- 0.5 hours/day for 7 days observation: monitor usage, check limit encounters (3.5 hours total, ~30 min active/day)
- 0.5 hours: compute results and evaluate threshold

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnel analysis, session recordings | Free up to 1M events/mo -- [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | Product tours for free-user onboarding | Essential $29/seat/mo -- [intercom.com/pricing](https://intercom.com/pricing) |
| Loops | Onboarding email sequence | Free up to 1,000 contacts -- [loops.so/pricing](https://loops.so/pricing) |
| Attio | CRM contact records with plan tier tracking | Free up to 3 seats -- [attio.com/pricing](https://attio.com/pricing) |
| n8n | Webhook routing from signup to CRM and email | Free self-hosted; cloud from $24/mo -- [n8n.io/pricing](https://n8n.io/pricing) |

**Estimated play-specific cost: Free** (all tools have free tiers sufficient for Smoke-level volume)

## Drills Referenced

- `lead-capture-surface-setup` -- builds the self-serve signup page with tracking, CRM routing, and email enrollment
- `onboarding-flow` -- creates the multi-channel onboarding experience that guides free users to the value moment
- `threshold-engine` -- evaluates free-to-paid conversion rate against the 5% pass threshold
