---
name: referral-program-scalable
description: >
  Incentivized Referral Program — Scalable Automation. Expand referral surfaces across
  every high-intent product moment, systematically A/B test incentives and messaging,
  and build always-on funnel monitoring to sustain >=8% referral rate at scale.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "40 hours over 6 weeks"
outcome: ">=8% referral rate sustained across 500+ prompted users AND referral CAC < 50% of paid acquisition CAC"
kpis: ["Referral rate at scale", "Referee activation rate", "Referral CAC vs paid CAC", "Viral coefficient", "Referral surfaces active", "A/B test win rate"]
slug: "referral-program"
install: "npx gtm-skills add product/referrals/referral-program"
drills:
  - ab-test-orchestrator
  - referral-channel-scaling
  - dashboard-builder
---

# Incentivized Referral Program — Scalable Automation

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Referral rate sustains >=8% across 500+ prompted users (not just power users, the broad eligible base). Referral CAC is less than 50% of paid acquisition CAC. Multiple referral surfaces are active and instrumented. The funnel is monitored with automated alerts for degradation.

## Leading Indicators

- 3+ referral surfaces active with independent tracking (in-app, email, social share)
- At least 2 A/B tests completed with statistical significance
- Referral funnel daily health checks returning "healthy" status
- Viral coefficient >0.15 (each referrer produces fractional additional referrals)
- Referee quality holding: referred user 30-day retention >= organic user 30-day retention

## Instructions

### 1. Expand referral surfaces across the product

Run the `referral-channel-scaling` drill. Deploy referral prompts at every high-intent moment:

- **Post-milestone in-app prompt** via Intercom: after first major workflow completion, after plan upgrade, after usage milestones (100th action, etc.)
- **Lifecycle email CTAs** via Loops: inject referral sections into the Day 7 email, monthly usage summary, and plan renewal confirmation
- **Post-action social sharing**: when users generate shareable outputs (reports, dashboards, exports), offer a share mechanic where the link requires signup to view, carrying the referrer's code

Use PostHog feature flags to roll out each new surface to 50% of eligible users first. Measure share rate per surface. Keep surfaces with >3% share rate; retire those below 1% after 4 weeks. Tag every referral event with a `surface` property so you can attribute conversions per channel.

### 2. Run systematic A/B tests on referral variables

Run the `ab-test-orchestrator` drill. Test these variables in priority order (one at a time, minimum 200 samples per variant):

**Test 1 -- Incentive structure:**
- Control: current two-sided reward (e.g., both get 1 month free)
- Variant: tiered reward (1 referral = sticker, 3 = free month, 5 = free year)
- Primary metric: referral links shared per prompted user
- Secondary metric: referrals per referrer (do tiered rewards motivate repeat referrals?)

**Test 2 -- Prompt timing:**
- Control: prompt at current trigger moment
- Variant: prompt 2 seconds after the user completes a success action (celebratory moment)
- Primary metric: share rate (prompt shown -> link shared)

**Test 3 -- Share copy:**
- Control: generic share text ("Check out [product]")
- Variant: personalized share text ("I use [product] for [user's top feature]. You'd like it.")
- Primary metric: referral link click-through rate (shared -> clicked)

**Test 4 -- Referee landing page:**
- Control: standard signup page with referral badge
- Variant: personalized page showing the referrer's name and usage context
- Primary metric: signup conversion (clicked -> signup completed)

Log every test result in PostHog and Attio. After each test concludes, implement the winner permanently before starting the next test.

### 3. Build always-on funnel monitoring

Run the `dashboard-builder` drill. Set up:

- Daily automated health check via n8n that calculates 7-day rolling conversion rates at each funnel stage
- Healthy/warning/critical classification for each stage transition (benchmarks defined in the drill)
- Slack alerts for any stage entering "critical" status
- Weekly referral report: volume, conversion rates, top referrers, referral CAC vs paid CAC, viral coefficient

The monitor should also track:
- Referral rate by user segment (power users, standard users, new users)
- Referral quality: compare 30-day retention and LTV of referred users vs organic users
- Channel attribution: which referral surface produces the highest-converting referees

### 4. Optimize the referrer retention loop

Identify referrers who shared once but never again. Using n8n, build a 30-day re-engagement cadence:

- Day 30 after last share: Loops email with their referral stats ("You've helped [count] people discover [product]. Ready to help another?")
- Day 45: Intercom in-app message with progress toward next reward tier
- Day 60: Final nudge with a time-limited bonus incentive ("Refer someone this week and both of you get [extra reward]")

Rate limit: maximum 1 re-engagement touch per 15 days. Do not pester.

### 5. Evaluate against threshold

Measure after 6 weeks:
- Referral rate across 500+ prompted users: target >=8%
- Referral CAC vs paid CAC: target <50%
- Viral coefficient: target >0.15
- Referral funnel health: no stages in "critical" for more than 48 hours

- **Pass:** Proceed to Durable. Document the winning test results, the top-performing surfaces, and the referral CAC calculation.
- **Fail on rate at scale:** Referral rate held with power users but dropped with the broader base. Segment analysis: which user cohort refers least? Create a targeted referral program variant for that cohort.
- **Fail on CAC:** Rewards are too expensive relative to referee value. Reduce the reward or shift to non-monetary incentives (early access, badges, recognition).

## Time Estimate

- 8 hours: deploy 3+ new referral surfaces with PostHog tracking and feature flag rollout
- 12 hours: design, run, and evaluate 4 A/B tests over 6 weeks (3 hours per test cycle)
- 8 hours: build referral funnel monitoring, daily health checks, and weekly reports
- 6 hours: build referrer retention loop, configure re-engagement automation
- 6 hours: ongoing monitoring, analysis, and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags for surface rollout, experiments for A/B tests, funnel analysis, cohorts | Free up to 1M events/mo and 1M feature flag requests; $0.00005/event after ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app referral prompts at multiple surfaces, re-engagement messages | From $29/seat/mo; Proactive Support $349/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Lifecycle email referral CTAs, referrer re-engagement sequences, reward notifications | From $49/mo for 5,000 contacts; $149/mo for 50,000 ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Funnel monitoring workflows, referrer re-engagement automation, reward pipeline | From EUR 24/mo Starter; EUR 60/mo Pro for 10K executions ([n8n.io/pricing](https://n8n.io/pricing/)) |
| Attio | Referrer records, test results, referral program performance tracking | $29/user/mo Plus ([attio.com](https://attio.com)) |

**Estimated play-specific cost at this level:** $100-250/mo (Loops paid plan + n8n Pro + incremental Intercom/PostHog usage)

## Drills Referenced

- `ab-test-orchestrator` -- designs, runs, and evaluates A/B tests on incentive structure, prompt timing, share copy, and landing page
- `referral-channel-scaling` -- deploys referral surfaces across in-app prompts, lifecycle emails, and post-action social sharing
- `dashboard-builder` -- builds always-on funnel monitoring with daily health checks, alerts, and weekly reports
