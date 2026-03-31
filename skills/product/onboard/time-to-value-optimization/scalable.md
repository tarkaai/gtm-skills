---
name: time-to-value-optimization-scalable
description: >
  Time-to-Value Acceleration — Scalable Automation. Segment-based onboarding personalization,
  systematic A/B testing of onboarding variants, and real-time activation dashboards. Maintain
  55%+ activation rate with median TTV <8 minutes at 500+ monthly signups.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=55% activation rate with median TTV <8 minutes at 500+ monthly signups"
kpis: ["Median time to first value by segment (minutes)", "Activation rate by segment (%)", "Step completion rate by segment", "Experiment win rate (%)", "Activation rate at volume (500+ signups/mo)"]
slug: "time-to-value-optimization"
install: "npx gtm-skills add product/onboard/time-to-value-optimization"
drills:
  - ab-test-orchestrator
  - lead-capture-surface-setup
  - dashboard-builder
---

# Time-to-Value Acceleration — Scalable Automation

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Activation rate holds at 55%+ with median TTV under 8 minutes while handling 500+ monthly signups. The 10x multiplier comes from three sources: (1) segment-based onboarding paths that match user context, (2) systematic A/B testing that continuously improves each path, and (3) an optimized lead capture surface that converts more visitors into the funnel.

## Leading Indicators

- At least 3 distinct onboarding segments defined (by signup source, plan type, or use case)
- PostHog feature flags live for at least 2 active experiments
- Activation dashboard showing per-segment metrics updated in real-time
- Lead capture surface deployed with tracked conversion events
- At least 2 completed A/B tests with statistically significant results

## Instructions

### 1. Segment the onboarding experience

Using PostHog cohorts from the Baseline data, identify 3-5 user segments with meaningfully different activation patterns. Common segmentation axes:

- **Signup source:** Organic search vs. paid ads vs. referral vs. direct (each has different intent levels)
- **Plan type:** Free trial vs. paid vs. freemium (different urgency)
- **Use case:** If your signup flow captures intent, segment by stated use case
- **Company size:** Solo users vs. teams (different activation paths)

For each segment, analyze:
1. Current activation rate (from PostHog cohorts)
2. Median TTV (from PostHog)
3. Most common drop-off step (from PostHog funnel breakdown by segment)
4. Whether the drop-off is at the same step across segments or different steps

Build segment-specific onboarding variants:
- Different Intercom product tours per segment (solo user sees a simplified tour; team user sees a collaboration-focused tour)
- Different Loops email sequences per segment (adjust use case examples, social proof, and CTAs to match the segment's context)
- Different Intercom contextual messages per segment at each drop-off step

Use PostHog feature flags to assign users to the correct segment and serve the matching variant. Do not hardcode segments — use feature flag payloads so variants can be changed without deploys.

### 2. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill. Plan a testing roadmap for the 2-month period. Test one element at a time per segment:

**Month 1 tests (high impact):**
- Test 1: Welcome email subject line and CTA (measure: email click rate and activation from email)
- Test 2: Product tour length — 3 steps vs. 5 steps vs. no tour (measure: first core action completion rate)
- Test 3: Nudge timing — 2 hours vs. 6 hours vs. 24 hours for first stall nudge (measure: milestone_2 completion rate)

**Month 2 tests (refinement):**
- Test 4: Winning tour variant + different CTA copy (measure: activation rate)
- Test 5: Social proof email variant — case study vs. aggregate stats vs. testimonial (measure: activation from email)
- Test 6: Segment-specific activation metric — for team users, test "invite teammate" vs. "complete first workflow" as the activation trigger (measure: 30-day retention)

For each test:
1. Form the hypothesis with predicted outcome and reasoning (see `ab-test-orchestrator` Step 1)
2. Calculate required sample size. If a segment has fewer than 200 signups/month, extend the test duration or test across segments
3. Set up the PostHog experiment with feature flag, metric definition, and duration
4. Let the test run to completion — do not peek and declare early winners
5. Analyze results and implement winners permanently

### 3. Optimize the lead capture surface

Run the `lead-capture-surface-setup` drill. The onboarding funnel starts before signup — the lead capture surface determines who enters the funnel and with what context. Optimize:

1. **Surface type:** If using a form, test reducing fields (email-only vs. email + company). If using a chat widget, test qualification bot vs. direct signup. If using an inline calendar, consider whether self-serve signup converts better.
2. **Context capture:** Add a qualifying question to the signup flow that feeds into segmentation: "What are you looking to accomplish?" with 3-4 options. This question both qualifies the lead and enables personalized onboarding from Step 1.
3. **PostHog tracking:** Instrument `cta_impression`, `cta_clicked`, `signup_started`, and `signup_completed` on the lead capture surface. Build a funnel from impression to activation to see the full picture from visitor to activated user.
4. **UTM passthrough:** Ensure all traffic sources carry UTM parameters through signup into PostHog. This feeds the segment analysis — you need to know which sources produce users who activate fastest.

### 4. Build the activation dashboard

Run the `dashboard-builder` drill. Create a "Time-to-Value Operations" dashboard with these panels:

1. **Activation rate by week** — trend line for the last 8 weeks, target line at 55%
2. **Median TTV by week** — trend line, target line at 8 minutes
3. **Activation rate by segment** — table showing each segment's current week rate vs. 4-week average
4. **Funnel by segment** — selectable dropdown showing the onboarding funnel for each segment
5. **Active experiments** — list of running A/B tests with current variant performance (do not use for early stopping — informational only)
6. **Volume tracker** — monthly signup count with a marker at 500 to confirm scale threshold is met

Set up alerts:
- Activation rate drops below 50% for any segment for 3 consecutive days
- Median TTV exceeds 12 minutes for any segment for 2 consecutive days
- Any experiment's guardrail metric (e.g., error rate) spikes above threshold

### 5. Evaluate against threshold

At the end of 2 months, measure:
- **Primary:** >= 55% activation rate with median TTV < 8 minutes at 500+ monthly signups
- **Supporting:** At least 3 experiments completed, at least 1 statistically significant winner implemented

If PASS: Document all segment-specific onboarding paths, experiment results, and the dashboard configuration. Proceed to Durable.

If FAIL: Diagnose whether the issue is scale-related (activation rate was fine at 100 signups but degraded at 500) or optimization-related (experiments did not produce wins). For scale issues: check if the infrastructure handled volume (email deliverability, webhook throughput, feature flag evaluation speed). For optimization issues: test bigger changes — different activation metrics, different onboarding modalities (video vs. text), or fundamentally different first-time experiences.

## Time Estimate

- 8 hours: Segment analysis and building segment-specific onboarding variants
- 12 hours: Setting up and running 6 A/B tests over 2 months
- 6 hours: Optimizing lead capture surface with tracking
- 4 hours: Building the activation dashboard with alerts
- 30 hours: Ongoing monitoring, experiment analysis, and iteration (distributed across 2 months)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom | Segment-specific product tours and in-app messages | Essential $29/seat/mo (annual); Advanced $85/seat/mo (annual) — https://www.intercom.com/pricing |
| Loops | Segment-specific behavioral email sequences | Paid from $49/mo, scales with contacts — https://loops.so/pricing |
| Loom | Onboarding video content for specific segments | Business $12.50/creator/mo (annual) — https://www.atlassian.com/software/loom/pricing |
| PostHog | Feature flags, experiments, funnels, dashboards | Free up to 1M events/mo; usage-based after — https://posthog.com/pricing |

## Drills Referenced

- `ab-test-orchestrator` — design, run, and analyze A/B tests on onboarding elements using PostHog experiments
- `lead-capture-surface-setup` — optimize the signup capture surface with tracking and CRM routing
- `dashboard-builder` — build real-time activation dashboards for monitoring and alerting
