---
name: free-to-paid-conversion-funnel-smoke
description: >
  Free to Paid Funnel — Smoke Test. Map the free-to-paid conversion path, instrument
  tracking on the core upgrade surface, and run a manual test with 10-50 free users
  to confirm conversion signal exists before automating.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥6% free-to-paid conversion rate from test cohort"
kpis: ["Free-to-paid conversion rate", "Time from signup to upgrade", "Activation-to-upgrade rate"]
slug: "free-to-paid-conversion-funnel"
install: "npx gtm-skills add product/upsell/free-to-paid-conversion-funnel"
drills:
  - lead-capture-surface-setup
  - posthog-gtm-events
  - threshold-engine
---

# Free to Paid Funnel — Smoke Test

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes
Prove that a deliberate upgrade surface (in-app prompt, feature gate, or pricing page CTA) can convert free users to paid at ≥6%. One surface, one cohort, manual observation. No automation, no always-on infrastructure.

## Leading Indicators
- Free users reach the upgrade surface (impression count > 0)
- At least 1 user clicks the upgrade CTA within 3 days
- Time from signup to first upgrade surface impression is < 7 days
- No user reports confusion about pricing or plan differences

## Instructions

### 1. Instrument the free-to-paid funnel events
Run the `posthog-gtm-events` drill to configure the core event taxonomy for this play. Define and implement these events in PostHog:

| Event | When it fires | Key properties |
|-------|--------------|----------------|
| `signup_completed` | User finishes free signup | `signup_source`, `plan: free` |
| `activation_milestone_reached` | User completes the first value action | `milestone_name`, `days_since_signup` |
| `upgrade_surface_impression` | Upgrade CTA enters viewport | `surface_type` (modal/gate/banner/pricing_page), `page` |
| `upgrade_surface_clicked` | User clicks the upgrade CTA | `surface_type`, `page`, `plan_shown` |
| `upgrade_started` | User enters checkout flow | `plan_selected`, `billing_period` |
| `upgrade_completed` | Stripe confirms subscription creation | `plan_selected`, `mrr`, `days_since_signup` |

Verify each event fires correctly by performing the action yourself and checking PostHog Live Events.

### 2. Deploy one upgrade surface
Run the `lead-capture-surface-setup` drill to build a single upgrade surface on the highest-intent page in your product. Choose one:

- **Feature gate**: Block access to a premium feature the user has tried to use. Show what they get and the price. One-click upgrade path.
- **Limit alert**: When the user hits 80%+ of a free plan limit, show a contextual message with the upgrade option.
- **Pricing page CTA**: Improve the in-product pricing page with clear plan comparison and a prominent upgrade button.

Deploy to a test group of 10-50 free users. Use a PostHog feature flag to control exposure so you can measure precisely who saw the surface.

**Human action required:** Review the upgrade surface copy and CTA before launching. Verify the checkout flow works end-to-end (click upgrade CTA -> see pricing -> enter payment -> subscription created). Test this yourself first.

### 3. Observe behavior for 7 days
Monitor PostHog Live Events daily for the test cohort. Log:
- How many users saw the upgrade surface (`upgrade_surface_impression` count)
- How many clicked (`upgrade_surface_clicked` count)
- How many started checkout (`upgrade_started` count)
- How many completed (`upgrade_completed` count)
- Any qualitative feedback from users (support tickets, chat messages about pricing)

Do not intervene during the observation period. Let the surface perform as deployed.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against the pass threshold: ≥6% free-to-paid conversion rate from the test cohort (users who saw the upgrade surface and completed upgrade within 7 days).

- **Pass → proceed to Baseline.** Document which surface type worked, the conversion rate, and the most common upgrade path.
- **Fail → iterate.** Diagnose: Did users see the surface but not click? (Copy/positioning problem.) Did they click but not complete checkout? (Pricing/friction problem.) Did they never reach the surface? (Activation/timing problem.) Fix the specific failure point and re-run.

## Time Estimate
- 2 hours: Event instrumentation and verification
- 1 hour: Upgrade surface build and deployment
- 1 hour: Daily monitoring over 7 days (10 min/day)
- 1 hour: Threshold evaluation and documentation

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, feature flags | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Stripe | Payment processing, subscription management | 2.9% + $0.30 per transaction — [stripe.com/pricing](https://stripe.com/pricing) |

**Play-specific cost:** Free (standard stack only)

## Drills Referenced
- `lead-capture-surface-setup` — build and deploy the upgrade surface with full tracking and CRM routing
- `posthog-gtm-events` — define and implement the free-to-paid event taxonomy in PostHog
- `threshold-engine` — evaluate conversion rate against ≥6% pass threshold
