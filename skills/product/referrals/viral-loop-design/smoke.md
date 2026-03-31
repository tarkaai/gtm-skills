---
name: viral-loop-design-smoke
description: >
  Built-In Virality — Smoke Test. Design and manually test one product-native viral mechanic
  (invite, share, or collaborate) with a small user cohort to prove the loop produces any signups.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Viral coefficient ≥0.3 measured across ≥50 active users"
kpis: ["Viral coefficient (K)", "Invites sent per active user", "Invite-to-signup conversion rate"]
slug: "viral-loop-design"
install: "npx gtm-skills add product/referrals/viral-loop-design"
drills:
  - viral-mechanic-design
  - threshold-engine
---

# Built-In Virality — Smoke Test

> **Stage:** Product → Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

One viral mechanic designed, prototyped, and tested with a small user cohort. The mechanic produces measurable signups from non-users who were exposed to the product through existing users' actions. Viral coefficient K >= 0.3.

## Leading Indicators

- Users perform the viral trigger action (invite, share, or collaborate) without being prompted
- Non-users click through shared artifacts or invite links
- At least some non-users who land on the conversion surface sign up
- Signed-up referees activate (reach the product's activation metric)

## Instructions

### 1. Design the viral mechanic

Run the `viral-mechanic-design` drill. The drill analyzes existing PostHog data to identify which product actions naturally expose the product to non-users, selects the highest-potential viral mechanic type (invite-to-collaborate, share-to-show, or use-to-expose), and produces a mechanic specification document.

The specification includes: the trigger action, the shareable artifact, the conversion surface for non-users, the expected viral coefficient, and the PostHog event schema.

### 2. Build a minimal prototype

**Human action required:** Implement the viral mechanic in the product. The mechanic needs three components:

1. A trigger surface — the UI element that lets users perform the viral action (invite button, share link generator, or collaborative feature). Place it at the moment of highest user motivation (immediately after the user creates value).
2. A shareable artifact — what the non-user receives or sees (invite email, shared link with preview, embedded widget). Must carry a referral identifier (unique link or code per user).
3. A conversion surface — the landing page or signup gate the non-user hits. Must show enough product value to motivate signup while requiring an account to interact fully.

Keep the prototype minimal. One sharing channel (email or link copy). One landing page variant. No reward system yet.

### 3. Instrument basic tracking

Add PostHog events manually for the prototype:

- `viral_trigger_action` — user clicks the share/invite button
- `viral_share_initiated` — user actually sends the invite or copies the link (with `share_channel` and `recipients_count` properties)
- `viral_landing_viewed` — non-user lands on the conversion surface (with `referral_code` property)
- `viral_signup_completed` — non-user creates an account via the viral path (with `referral_code` property)

Use `posthog-custom-events` fundamental for implementation details.

### 4. Test with a small cohort

**Human action required:** Select 50-100 active users. Roll out the viral mechanic to this cohort only (use a PostHog feature flag if available, or target by user segment). Let it run for 5-7 days. Do not prompt users to share — the mechanic should work through natural product usage.

### 5. Measure viral coefficient

Run the `threshold-engine` drill to evaluate:

```
K = (total invites sent by cohort / cohort size) * (signups from invites / total invite recipients)
```

Pull from PostHog: count of `viral_share_initiated` (sum of `recipients_count`), count of `viral_signup_completed` where `referral_code` is present.

**Pass threshold:** K >= 0.3.

If K < 0.1, the mechanic type is wrong — the trigger action is too infrequent or the conversion surface is too weak. Return to step 1 and select a different mechanic.

If 0.1 <= K < 0.3, the mechanic has potential but needs friction reduction. Check: Are users finding the share button? Are non-users clicking through? Where in the funnel is the biggest drop-off? Fix the weakest step and re-test for another 5 days.

If K >= 0.3, proceed to Baseline.

## Time Estimate

- 2 hours: viral mechanic design (drill + specification)
- 1 hour: prototype implementation guidance and tracking setup
- 0.5 hours: cohort selection and feature flag configuration
- 1.5 hours: measurement, analysis, and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, feature flags, funnel analysis | Free tier: 1M events/mo, 1M feature flag requests/mo. Paid: usage-based starting at $0.00005/event. https://posthog.com/pricing |

## Drills Referenced

- `viral-mechanic-design` — designs the viral mechanic type, trigger, and loop specification
- `threshold-engine` — evaluates K against the pass threshold and recommends next action
