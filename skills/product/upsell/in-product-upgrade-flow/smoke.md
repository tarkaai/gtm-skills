---
name: in-product-upgrade-flow-smoke
description: >
  Self-Serve Upgrade UX — Smoke Test. Build a single in-product upgrade surface
  (pricing modal, inline checkout, or upgrade banner) on one high-intent trigger
  point and measure whether users complete self-serve upgrades without sales
  involvement.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥5% of upgrade-surface-exposed users complete a self-serve upgrade within 7 days"
kpis: ["Self-serve upgrade completion rate", "Surface impression-to-click rate", "Time from surface view to upgrade completion", "Checkout abandonment rate"]
slug: "in-product-upgrade-flow"
install: "npx gtm-skills add product/upsell/in-product-upgrade-flow"
drills:
  - upgrade-prompt
  - posthog-gtm-events
---

# Self-Serve Upgrade UX — Smoke Test

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

5% or more of users who see the in-product upgrade surface complete a self-serve plan upgrade within 7 days without any sales involvement. "Upgrade-surface-exposed users" means users who triggered an `upgrade_surface_shown` event. This proves that an in-product upgrade path can convert users when presented at the right moment with the right context.

## Leading Indicators

- Upgrade surface impressions per day (users are reaching the trigger point organically)
- Surface click-through rate: percentage of users who see the upgrade surface and interact with it (click "Upgrade," expand plan details, or open the checkout modal)
- Checkout start rate: percentage of clickers who reach the payment step
- Time from first surface impression to upgrade completion (shorter means lower friction)
- Users who view the surface multiple times before upgrading (high revisit count suggests the surface is memorable but the conversion barrier needs reduction)

## Instructions

### 1. Identify the highest-intent upgrade trigger point

Run the `upgrade-prompt` drill to determine where in the product users are most likely to upgrade. Pick ONE trigger point for the Smoke test:

| Trigger Type | Example | Signal Strength |
|-------------|---------|----------------|
| **Usage limit hit** | User attempts to create a 6th project on a 5-project free plan | Highest — user is blocked and has immediate need |
| **Feature gate encounter** | User clicks a Pro-only feature and sees a locked state | High — user discovered a capability they want |
| **Growth signal** | User invites their 4th team member and approaches the seat limit | Medium — user is investing in the product |
| **Milestone reached** | User completes their 100th action or hits 30 days of active usage | Medium — user has proven engagement |

Select the trigger with the highest daily occurrence rate among free or lower-tier users. The Smoke test needs enough volume to measure within 7 days (minimum 50 trigger events expected).

### 2. Build the upgrade surface

Design and implement the upgrade surface that appears at the trigger point. The surface must include:

1. **Context**: Why the surface appeared. Tie it directly to what the user just did. "You have used 5 of 5 projects" or "This feature is available on Pro."
2. **Value framing**: What upgrading unlocks. One sentence, specific to the trigger. "Upgrade to Pro for unlimited projects" not "Upgrade to unlock more features."
3. **Price clarity**: Show the exact price difference. "$29/mo — $20 more than your current plan" or "Start Pro for $49/mo."
4. **One-click action**: A single primary CTA that takes the user directly to checkout with the target plan pre-selected. No intermediate steps, no "learn more" detour.
5. **Dismissal option**: A clear close button. Never trap users. Track the dismissal in PostHog.

**Surface format options (choose one):**
- **Inline modal**: Appears centered on screen at the trigger moment. Best for limit-hit and feature-gate triggers where the user is blocked.
- **Slide-in panel**: Appears from the right side with plan comparison. Best for growth-signal triggers where the user is not blocked.
- **Contextual banner**: Appears at the top of the current page with a persistent CTA. Best for milestone triggers where the user should not be interrupted.

**Human action required:** Implement the upgrade surface component in the product. Wire the primary CTA to your Stripe checkout or billing settings page with the target plan pre-selected. Deploy behind a PostHog feature flag so you can control rollout.

### 3. Instrument event tracking

Run the `posthog-gtm-events` drill to set up tracking for the upgrade flow:

| Event | When Fired | Properties |
|-------|-----------|-----------|
| `upgrade_surface_shown` | Upgrade surface enters viewport | `trigger_type`, `user_plan`, `target_plan`, `page`, `surface_format` |
| `upgrade_surface_clicked` | User clicks the upgrade CTA | `trigger_type`, `user_plan`, `target_plan`, `surface_format` |
| `upgrade_surface_dismissed` | User closes the surface | `trigger_type`, `time_on_surface_seconds`, `surface_format` |
| `upgrade_checkout_started` | User reaches the payment page | `trigger_type`, `user_plan`, `target_plan`, `price_monthly` |
| `upgrade_checkout_completed` | Stripe confirms the subscription change | `trigger_type`, `previous_plan`, `new_plan`, `mrr_delta` |

Build a PostHog funnel:
```
upgrade_surface_shown
  -> upgrade_surface_clicked
    -> upgrade_checkout_started
      -> upgrade_checkout_completed
```

Enable PostHog session recordings for users who see the upgrade surface to diagnose friction in the checkout flow.

### 4. Launch to a test group and evaluate

Enable the PostHog feature flag for 10-50 active free or lower-tier users. Monitor for 7 days.

**Primary metric:** `upgrade_checkout_completed` / `upgrade_surface_shown`. Target: >=5%.

**Secondary metric:** `upgrade_surface_clicked` / `upgrade_surface_shown`. Target: >=15%. If surface CTR is above 15% but checkout completion is below 5%, the checkout flow has friction. If surface CTR is below 15%, the surface itself needs improvement.

**Pass (>=5% self-serve upgrade rate):** The in-product upgrade surface converts. Proceed to Baseline to automate and run always-on with a control group.

**Fail:** Diagnose the funnel:
- Low impressions: The trigger point is too rare. Switch to a higher-frequency trigger.
- Low CTR (<15%): The surface does not communicate value. Test a different value framing or surface format.
- High CTR but low checkout completion: The checkout flow has friction. Check if the target plan is pre-selected, if pricing is clear, if payment entry requires too many fields. Watch session recordings.
- Users dismiss quickly (<3 seconds on surface): The surface feels interruptive. Switch to a less intrusive format (banner instead of modal) or change timing (show after the user completes the action, not during it).

## Time Estimate

- 1 hour: Trigger point analysis, surface format selection
- 2 hours: Upgrade surface implementation and PostHog event instrumentation (human)
- 1 hour: Feature flag configuration, test group selection, funnel setup
- 1 hour: 7-day monitoring, session recording review, threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, event tracking, funnels, session recordings | Free up to 1M events/mo — https://posthog.com/pricing |
| Stripe | Payment processing for upgrade checkout | 2.9% + $0.30 per transaction — https://stripe.com/pricing |

**Play-specific cost:** Free (uses existing stack)

## Drills Referenced

- `upgrade-prompt` — identify the highest-intent trigger point and design the contextual upgrade surface with value framing and one-click action
- `posthog-gtm-events` — instrument the full upgrade flow event taxonomy from surface impression through checkout completion
