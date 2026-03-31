---
name: onboarding-call-program-scalable
description: >
  High-Touch Onboarding Calls — Scalable Automation. Scale to 50+ calls per month
  with team routing, persona-based call scripts, and systematic A/B testing of
  invitation channels, call structure, and follow-up sequences.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Direct"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "50+ calls/mo with ≥75% post-call activation rate; identify highest-impact call variant via A/B testing"
kpis: ["Calls completed per month", "Post-call 7-day activation rate", "Activation lift vs no-call", "Booking funnel conversion", "Call score by team member"]
slug: "onboarding-call-program"
install: "npx gtm-skills add product/onboard/onboarding-call-program"
drills:
  - ab-test-orchestrator
  - onboarding-call-performance-monitor
---
# High-Touch Onboarding Calls — Scalable Automation

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Direct

## Outcomes

Scale the onboarding call program from a single-person operation to a team-run, systematically tested program doing 50+ calls per month. Use A/B testing to optimize every part of the funnel: invitation copy, call structure, follow-up cadence. Build the performance monitoring system that will feed the Durable level's autonomous optimization.

**Pass threshold:** 50+ calls completed per month with ≥75% post-call 7-day activation rate. At least 2 completed A/B tests with statistically significant results.

## Leading Indicators

- Call volume scaling week-over-week toward 50+/month
- Round-robin routing distributing calls evenly across team members
- A/B tests reaching statistical significance within planned timeframes
- Performance monitoring dashboard operational with daily anomaly checks
- Booking funnel conversion stable or improving as volume grows

## Instructions

### 1. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill to test variations across the onboarding call funnel. Run tests sequentially (one at a time) to isolate variables:

**Test 1 — Invitation channel effectiveness:**
- Control: current multi-channel invitation (in-app + email sequence)
- Variant: email-only invitation (no in-app message)
- Metric: booking rate (invited → booked)
- Hypothesis: "If we simplify to email-only invitations, booking rate will remain within 5pp because most bookings come from email."
- Duration: 2 weeks or 200+ eligible users per variant

**Test 2 — Call structure:**
- Control: current 30-minute call with full discovery + walkthrough
- Variant: 20-minute call that skips discovery and goes straight to the guided walkthrough
- Metric: post-call 7-day activation rate
- Hypothesis: "If we shorten the call to 20 minutes and focus entirely on the walkthrough, activation rate will remain ≥75% because the walkthrough is the high-value block."
- Duration: 4 weeks or 30+ calls per variant

**Test 3 — Follow-up timing:**
- Control: follow-up email within 1 hour of call
- Variant: follow-up email at 24 hours after call
- Metric: post-call 7-day activation rate
- Hypothesis: "If we delay the follow-up to 24 hours, users who activated during the call still activate (no change), but users who did not activate during the call will benefit from a fresh prompt the next day."
- Duration: 4 weeks or 30+ calls per variant

**Test 4 — Qualification criteria expansion:**
- Control: current qualification criteria (paid plan + high signals)
- Variant: expand to include free-plan users with high early engagement
- Metric: post-call 7-day activation rate AND subsequent conversion to paid
- Hypothesis: "If we offer calls to engaged free users, their activation rate will be ≥60% and ≥20% will convert to paid within 30 days."
- Duration: 4 weeks

For each test, use PostHog feature flags to split eligible users. Log experiment setup, duration, and results in Attio.

### 2. Build the performance monitoring system

Run the `onboarding-call-performance-monitor` drill to create always-on monitoring:

- Build the PostHog dashboard with 6 panels: full funnel trend, call quality distribution, activation rate call vs no-call, time to activation distribution, booking source breakdown, no-show/cancellation rate
- Define anomaly thresholds for each metric (booking rate, completion rate, activation rate, call score, activation lift, no-show rate)
- Build the daily monitoring n8n workflow with anomaly alerts
- Build the weekly performance report with funnel data, booking sources, call quality, trends, and recommended actions
- Build the monthly cohort comparison and ROI analysis

### 3. Scale with team routing

Expand from a single person running calls to a team. Configure Cal.com round-robin scheduling:

- Set up a Cal.com team event type with round-robin assignment across onboarding team members
- Configure availability windows per team member
- Optionally route by user attribute: enterprise users to senior team members, specific verticals to product specialists

**Human action required:** Onboard new team members on the call script and scoring rubric. Have them shadow 2-3 calls, then run 2-3 calls with the original caller observing, before running solo.

Track per-team-member metrics in PostHog: call score, activation rate, and call volume. Identify if specific team members consistently outperform and document what they do differently.

### 4. Build persona-based call variants

Create 2-3 call script variants targeting different user personas:

- Pull persona distribution data from PostHog (by plan type, company size, use case, or signup source)
- For each persona, adjust the `onboarding-call-script` drill output:
  - Different discovery questions relevant to their use case
  - A walkthrough that follows their specific critical path to activation
  - Follow-up content tailored to their next valuable feature
- Route users to the appropriate variant based on their PostHog properties or Attio record

### 5. Evaluate against threshold

After 2 months:

1. Confirm call volume: ≥50 completed calls per month
2. Confirm activation rate: ≥75% post-call 7-day activation rate
3. Confirm A/B tests: at least 2 tests completed with statistically significant results
4. Review the performance monitoring system: are dashboards accurate, are anomaly alerts firing correctly, are weekly reports useful?

**Pass:** All thresholds met. Proceed to Durable.
**Fail:** If volume is below 50/month, expand qualification criteria or improve booking rate. If activation rate dropped below 75%, review call scores for quality degradation. If no A/B tests completed, increase test traffic or test larger effect sizes.

Capture the program's ROI: (incremental activations from calls x customer LTV) vs (time spent on calls x cost per hour + tool costs).

## Time Estimate

- 8 hours: A/B test design, setup, and analysis (4 tests)
- 10 hours: Performance monitoring system build (dashboard, anomaly detection, reports)
- 4 hours: Team routing setup and team member onboarding
- 4 hours: Persona-based call variant creation
- 30 hours: Running 100+ calls over 2 months (with team, distributed)
- 4 hours: Monthly evaluation and optimization

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Cal.com | Team scheduling with round-robin | Teams: $15/user/mo ([cal.com/pricing](https://cal.com/pricing)) |
| Fireflies | Call recording and transcript analysis at scale | Pro: $10/user/mo annually ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |
| Intercom | In-app invitation messages + product tours | Essential: $29/seat/mo annually ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Invitation sequences + follow-up emails | $49/mo for 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated play-specific cost:** $90-175/mo (Cal.com Teams for 2-3 users + Fireflies Pro for 2-3 users + Loops starter)

## Drills Referenced

- `ab-test-orchestrator` — designs, runs, and analyzes A/B tests on invitation channels, call structure, follow-up timing, and qualification criteria
- `onboarding-call-performance-monitor` — builds the PostHog dashboard, daily anomaly detection, weekly performance reports, and monthly cohort analysis
