---
name: in-app-onboarding-tour-scalable
description: >
  Interactive Product Tour — Scalable Automation. Roll out to 100% of users with persona-based
  tour variants, systematic A/B testing, and automated churn prevention to maintain >=45%
  activation at 500+ users per month.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=45% activation rate sustained at 500+ monthly signups"
kpis: ["7-day activation rate", "Tour completion rate", "Median time to activation", "Per-persona activation rate", "Experiment win rate"]
slug: "in-app-onboarding-tour"
install: "npx gtm-skills add product/onboard/in-app-onboarding-tour"
drills:
  - ab-test-orchestrator
  - onboarding-personalization
  - churn-prevention
---

# Interactive Product Tour — Scalable Automation

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Scale the onboarding tour to 100% of users with persona-specific variants that address different user types. Run systematic A/B tests on tour content, timing, and messaging to find the 10x multiplier. Build automated churn prevention that catches stalled users before they abandon the product.

Pass threshold: >=45% activation rate sustained across 500+ monthly signups for at least 2 consecutive months, with no single persona segment below 35%.

## Leading Indicators

- Per-persona activation rates converging within 10 percentage points of each other
- At least 2 A/B tests completed per month with statistically significant results
- Churn prevention interventions re-engaging >=20% of at-risk users
- Tour completion rate >=60% across all persona variants
- Time to activation decreasing month-over-month
- Stalled user count declining as a percentage of signups

## Instructions

### 1. Build persona-specific tours

Run the `onboarding-personalization` drill. Define 2-4 user personas based on PostHog cohort analysis of activated vs churned users. For each persona:

1. Identify the properties available at signup or first session (role, use case, company size, signup source)
2. Map their specific activation path — the fastest route to their "aha moment"
3. Build a dedicated Intercom product tour (3-5 steps) focused on that activation path
4. Set up PostHog feature flag routing: `onboarding-tour-persona` with variants matching persona types

Configure Intercom tour triggers:
- Each tour fires only for its matching persona (`persona_type = X AND onboarding_complete = false`)
- Users without a detected persona get the proven generic tour from Baseline

Instrument per-persona events: `tour_started`, `tour_completed`, `activation_reached` all include `{persona_type}` property.

### 2. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill. Establish a testing cadence of 2 experiments per month. Priority test areas:

**Month 1 experiments:**
- Tour step count: test 3-step vs 5-step tour variants for each persona
- First-step content: test "show me the product" (feature-focused) vs "let me try it" (action-focused) opening steps

**Month 2 experiments:**
- Tour timing: test immediate tour trigger vs 30-second delay after first page load
- Email nudge timing: test 24h vs 48h delay for the first nudge email to stalled users

For each experiment:
1. Form a hypothesis with a predicted outcome and reasoning
2. Calculate required sample size (minimum 200 per variant)
3. Create a PostHog experiment with the feature flag
4. Run for the planned duration without peeking
5. Evaluate at 95% significance. Implement winners, document losers.

Track cumulative lift from all experiments: what is the total activation improvement from testing?

### 3. Build automated churn prevention

Run the `churn-prevention` drill. Configure automated interventions for onboarding-specific risk signals:

**Detection (daily via n8n):**
- Signed up 3+ days ago, no milestone progress → "stalled at zero"
- Completed step 1 but no progress for 48h → "stalled mid-funnel"
- Completed tour but no activation for 5+ days → "stalled post-tour"
- Login frequency declining in first 14 days → "fading engagement"

**Tiered interventions:**
- Low risk (stalled 48h): Contextual Intercom tooltip highlighting the next step
- Medium risk (stalled 3+ days): Loops email with a specific tutorial for their stuck point, include a calendar link for a human onboarding call
- High risk (stalled 7+ days, fading engagement): Create a task in Attio for manual outreach from customer success, include the user's progress data

**Feedback loop:**
Track which interventions succeed (user re-engages within 48h) vs fail (no activity). Feed success/failure data back into signal weighting. Signals that produce false positives (user was on vacation, seasonal business) get lower weight over time.

### 4. Scale monitoring

Build PostHog dashboards tracking:
- Overall activation rate with 4-week trendline
- Per-persona activation rates side by side
- Active experiments and their current metrics
- Churn prevention: interventions sent, re-engagement rate, save rate
- Email sequence performance by step and persona

Set alerts:
- Any persona activation rate drops below 35% for 3+ consecutive days
- Overall activation rate drops below 40%
- Any experiment's guardrail metric (bounce rate, unsubscribe rate) spikes

### 5. Monthly review and optimization

At the end of each month:

1. Compile experiment results: tests run, winners, cumulative lift
2. Review per-persona performance: which persona needs the most improvement?
3. Analyze stalled-user patterns: where are users getting stuck? Is it changing?
4. Update tour content based on findings
5. Plan next month's experiments targeting the weakest areas

### 6. Evaluate at 2 months

Query PostHog for the trailing 2 months:
- Monthly signup volume >=500?
- Activation rate >=45% for both months?
- No persona segment below 35%?

**PASS**: Document the persona variants, test results, and intervention rules. Proceed to Durable.
**FAIL**: Identify the weakest persona or funnel step. Focus all testing effort there. Run one more month before re-evaluating.

## Time Estimate

- 12 hours: Build persona-specific tours and routing (week 1-2)
- 8 hours: Set up A/B testing framework and run first experiments (week 2-3)
- 10 hours: Build churn prevention automation (week 3-4)
- 20 hours: Run experiments, analyze results, iterate tours (month 1-2)
- 6 hours: Monthly reviews and planning (2 reviews)
- 4 hours: Final evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, experiments, feature flags, cohorts | Free up to 1M events/mo; ~$50/mo for 2M events ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Product tours (per-persona), in-app messages | Essential $39/seat/mo + Proactive Support Plus $99/mo; 500+ messages add usage fees ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Behavioral email sequences | $49/mo for 1K+ contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Automation: churn detection, PostHog-Loops bridge, intervention triggers | Pro: EUR 60/mo (10K executions) or self-hosted free ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated monthly cost at this level:** $248-$400/mo (Intercom ~$138-$250 depending on message volume + Loops $49 + n8n $60 + PostHog $0-$50)

## Drills Referenced

- `ab-test-orchestrator` — runs rigorous A/B tests on tour variants, timing, and messaging with proper hypothesis formation and statistical analysis
- `onboarding-personalization` — builds persona-specific tours and routes users via PostHog feature flags and Intercom targeting
- `churn-prevention` — detects stalled and at-risk new users and triggers automated interventions to re-engage them before they abandon
