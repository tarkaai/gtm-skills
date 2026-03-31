---
name: free-to-paid-conversion-funnel-baseline
description: >
  Free to Paid Funnel — Baseline Run. Deploy the upgrade surface to all free users
  with always-on tracking, lifecycle email sequences, and automated funnel dashboards.
  First continuous automation proving the conversion rate holds at scale.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥10% free-to-paid conversion rate across all free users over 2 weeks"
kpis: ["Free-to-paid conversion rate", "Time from signup to upgrade", "Activation rate", "Upgrade surface CTR"]
slug: "free-to-paid-conversion-funnel"
install: "npx gtm-skills add product/upsell/free-to-paid-conversion-funnel"
drills:
  - activation-optimization
  - feature-announcement
  - onboarding-flow
---

# Free to Paid Funnel — Baseline Run

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes
The upgrade surface from Smoke is now live for all free users. Lifecycle emails guide free users toward activation and upgrade. PostHog dashboards track the full funnel continuously. Conversion rate holds at ≥10% over 2 weeks with no manual intervention in the conversion path.

## Leading Indicators
- Activation rate (signup to first value action) is ≥40% within 7 days
- Upgrade surface CTR (impression to click) is ≥8%
- Lifecycle email open rate is ≥30%
- Median time from signup to upgrade impression is decreasing week-over-week
- No checkout abandonment spike (abandonment rate stays below 60%)

## Instructions

### 1. Optimize activation to feed the funnel
Run the `activation-optimization` drill to identify and improve the key activation metric. The free-to-paid funnel depends on free users reaching the activation milestone — unactivated users almost never upgrade. Analyze PostHog funnels from Smoke data to find the biggest drop-off between signup and activation. Implement fixes:

- If users stall at signup completion: simplify the signup flow, reduce required fields
- If users sign up but never take the first action: add an onboarding checklist via Intercom, pre-populate sample data
- If users take the first action but do not form a habit: add a progress indicator, send day-3 email highlighting what they accomplished

Target: ≥40% of signups reach the activation milestone within 7 days.

### 2. Build the onboarding-to-upgrade email sequence
Run the `onboarding-flow` drill to create a lifecycle email sequence via Loops that guides free users from signup through activation toward the upgrade surface:

| Email | Timing | Content | Skip condition |
|-------|--------|---------|----------------|
| Welcome | Immediate | One clear next step to reach the first value action. Link directly to the action, not the dashboard. | — |
| Quick start | Day 1 | Show the fastest path to the activation milestone with a short tutorial or video. | Already activated |
| Social proof | Day 3 | How similar users got value. Include a specific metric or outcome. | Already activated |
| Upgrade preview | Day 5 | Show what the paid plan unlocks. Tie it to the user's specific usage. Include a direct upgrade link. | Already upgraded |
| Personal check-in | Day 7 | From a real person (founder or CS). Ask if they need help. Include a Cal.com booking link. | Already upgraded |
| Limit nudge | Triggered | When user hits 70% of a free plan limit. Show what they lose vs. what they get on paid. | Already upgraded |

Configure each email to skip if the user has already completed the relevant action. Never send an upgrade email to a user who has not yet activated.

### 3. Announce the upgrade path to existing free users
Run the `feature-announcement` drill to inform existing free users about the upgrade surface. Create:

- An Intercom in-app message for activated free users showing what paid unlocks, with a direct upgrade CTA
- A Loops broadcast email to habitual free users (3+ sessions in 7 days) highlighting the specific features they would gain

**Human action required:** Review the announcement copy. Ensure it feels helpful ("unlock more of what you already use") rather than pushy ("upgrade now"). Launch to all free users.

### 4. Build the continuous funnel dashboard
Configure a PostHog dashboard to monitor the full funnel in real time:

| Panel | Metric |
|-------|--------|
| Signup → Activation funnel | `signup_completed` -> `activation_milestone_reached` (7-day window) |
| Activation → Upgrade funnel | `activation_milestone_reached` -> `upgrade_surface_impression` -> `upgrade_surface_clicked` -> `upgrade_started` -> `upgrade_completed` |
| Conversion rate trend | Daily free-to-paid conversion rate, 7-day rolling average |
| Email sequence performance | Open rate, click rate, and skip rate per email in the lifecycle sequence |
| Checkout abandonment | `upgrade_started` events without a corresponding `upgrade_completed` within 24 hours |

Review this dashboard twice per week. Fix any step where conversion drops below 50% of the previous step.

### 5. Evaluate against threshold
After 2 weeks of continuous operation, measure: ≥10% of free users who saw the upgrade surface completed an upgrade.

- **Pass → proceed to Scalable.** Document the full funnel conversion rates, the winning upgrade surface, and the email sequence performance.
- **Fail → diagnose and iterate.** Check: Is activation the bottleneck? (Fix onboarding.) Is the surface seen but not clicked? (Fix copy/placement.) Is checkout abandoned? (Fix pricing page/payment flow.) Re-run Baseline after fixing the specific failure point.

## Time Estimate
- 4 hours: Activation analysis and optimization
- 4 hours: Email sequence build and configuration
- 3 hours: Announcement creation and deployment
- 2 hours: Dashboard setup
- 3 hours: Monitoring, iteration, and threshold evaluation over 2 weeks

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnels, cohorts, dashboards, feature flags | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Loops | Lifecycle email sequences and broadcasts | Free up to 1,000 contacts; from $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app messages and product tours | From $29/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |
| Stripe | Subscription management | 2.9% + $0.30/txn — [stripe.com/pricing](https://stripe.com/pricing) |

**Play-specific cost:** Loops ~$49/mo + Intercom ~$29/mo = ~$78-130/mo depending on seat count and contacts

## Drills Referenced
- `activation-optimization` — find and improve the activation metric that predicts conversion
- `onboarding-flow` — build the multi-channel onboarding and lifecycle email sequence
- `feature-announcement` — announce the upgrade path to existing free users via in-app and email
