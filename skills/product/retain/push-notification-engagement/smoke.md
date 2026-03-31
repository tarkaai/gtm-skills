---
name: push-notification-engagement-smoke
description: >
  Push Notification Strategy — Smoke Test. Set up push notification infrastructure,
  send a single targeted campaign to a small user cohort, and measure whether push
  produces any engagement signal (CTR and DAU lift).
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥25% CTR on first push campaign sent to 20-50 users"
kpis: ["Push CTR", "Opt-in rate", "DAU lift"]
slug: "push-notification-engagement"
install: "npx gtm-skills add product/retain/push-notification-engagement"
drills:
  - push-notification-setup
  - threshold-engine
---

# Push Notification Strategy — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes
A single push notification campaign sent to 20-50 real users produces a click-through rate of 25% or higher. At least one push type (habit reinforcement, time-sensitive, or value delivery) generates a measurable DAU lift on the day it is sent. The opt-in prompt converts at least 40% of users who see it.

## Leading Indicators
- Opt-in prompt shown to test users without errors
- Permission grant rate on the soft prompt (target: >40%)
- Push notifications delivered successfully (delivery rate >95%)
- At least 1 user clicks a push within 1 hour of delivery
- PostHog events for the push lifecycle (`push_sent`, `push_delivered`, `push_clicked`) fire correctly

## Instructions

### 1. Set up push infrastructure
Run the `push-notification-setup` drill. For Smoke, use OneSignal's free tier. Configure the SDK on your web or mobile app, build a custom soft opt-in prompt, and instrument PostHog events for the full push lifecycle. Verify the integration by sending a test push to yourself.

**Human action required:** Review the opt-in prompt copy and placement before deploying to real users. The prompt should appear after a meaningful user action (not on page load) and clearly state what notifications the user will receive.

### 2. Select a test cohort
Identify 20-50 active users to test with. Choose users who have been active in the last 7 days and log in at least 2-3 times per week. These users are most likely to grant permission and engage with push, giving you the strongest signal for the Smoke test.

### 3. Send one targeted push campaign
Run the the push notification campaign workflow (see instructions below) drill. Pick one campaign type to test — the strongest candidate is usually **value delivery** (e.g., "Your weekly report is ready") because it provides immediate utility rather than asking the user to do something. Write the push copy following the drill's guidelines: 5-8 word title, 15-25 word body, deep link to the specific content.

Send the push at the user's local timezone peak-activity time (default: 9-10 AM if you lack per-user timing data). Use OneSignal's timezone delivery feature.

### 4. Measure results
Run the `threshold-engine` drill to evaluate against the pass criteria:

- **Push CTR**: `push_clicked / push_delivered` — target ≥25%
- **Opt-in rate**: `push_permission_granted / push_prompt_shown` — target ≥40%
- **DAU lift**: Compare the test cohort's DAU on the push-send day vs their average DAU over the prior week

If CTR is below 25%, diagnose:
- Was the push copy specific and value-driven, or generic?
- Did the deep link go to the right place?
- Was the send time appropriate for the user's timezone?

Iterate on copy and timing, then re-send to the same cohort.

## Time Estimate
- 2 hours: SDK integration, opt-in prompt, PostHog event setup
- 1 hour: Test cohort selection, campaign copy, OneSignal configuration
- 1 hour: Send campaign and wait for results (send in morning, check by evening)
- 1 hour: Analyze results, document findings, decide pass/fail

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| OneSignal | Push notification delivery | Free (unlimited push subscribers) |
| PostHog | Event tracking and CTR measurement | Standard stack — excluded |
| n8n | Subscription sync workflow | Standard stack — excluded |

## Drills Referenced
- `push-notification-setup` — configure push SDK, opt-in prompt, and PostHog event tracking
- the push notification campaign workflow (see instructions below) — design and send the targeted push campaign
- `threshold-engine` — evaluate CTR and DAU lift against pass criteria
