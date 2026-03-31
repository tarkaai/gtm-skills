---
name: funnel-optimization-smoke
description: >
  Conversion Funnel Optimization — Smoke Test. Instrument one critical funnel (signup, activation,
  or upgrade), identify the primary bottleneck via drop-off analysis and session recordings,
  and validate that the diagnosis produces at least one testable improvement hypothesis.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=10% funnel improvement at the primary bottleneck step within 1 week, validated by PostHog funnel data"
kpis: ["Funnel step conversion rate", "Drop-off reduction at bottleneck", "Hypothesis quality score"]
slug: "funnel-optimization"
install: "npx gtm-skills add product/retain/funnel-optimization"
drills:
  - signup-funnel-audit
  - threshold-engine
---

# Conversion Funnel Optimization — Smoke Test

> **Stage:** Product → Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Prove that systematic funnel instrumentation and diagnosis produces actionable improvement opportunities. At this level, you instrument one critical funnel, identify the biggest conversion bottleneck, diagnose its root cause from session recordings and path analysis, and implement one quick fix to validate the approach.

**Pass threshold:** >=10% conversion improvement at the primary bottleneck step within 1 week, validated by PostHog funnel data comparing before and after.

## Leading Indicators

- All funnel steps instrumented with distinct PostHog events (target: 100% step coverage within 2 hours)
- Primary bottleneck identified with >=20% absolute drop-off quantified
- Session recording review completed (>=15 recordings classified by friction type)
- At least 1 hypothesis generated with expected lift >10%
- Quick fix deployed and tracking confirms variant is live

## Instructions

### 1. Choose the critical funnel

Select the funnel with the highest traffic AND most revenue impact. For most products, this is one of: signup (landing page to account created), activation (account created to aha moment), or upgrade (free to paid). If you are unsure which has the biggest drop-off, instrument all three at step 1 and pick the worst performer.

### 2. Run the signup-funnel-audit drill

Run the `signup-funnel-audit` drill against your chosen funnel. This produces:

- PostHog events for every funnel step (field-level if applicable)
- A PostHog funnel insight showing conversion rates between each step
- Baseline metrics with values and dates
- The primary bottleneck (step with largest absolute drop-off)

If your critical funnel is activation or upgrade rather than signup, adapt the audit drill's event schema to match your funnel steps. The structure is the same: define events for each step, build the funnel in PostHog, measure conversion between steps.

**Human action required:** Verify that PostHog events are firing correctly. Load each funnel step in your browser, complete the actions, and check that events appear in PostHog's live events view. Fix any instrumentation gaps before proceeding.

### 3. Diagnose the bottleneck

Run the the funnel drop off diagnosis workflow (see instructions below) drill against the primary bottleneck step identified in step 2. This produces:

- Segment-level conversion breakdown (device, source, user type)
- Path analysis comparing completers vs droppers
- Session recording friction classification from 15-25 recordings
- 3-5 ranked hypotheses with proposed fixes

Focus the session recording review on the segment with the worst conversion rate. If mobile conversion is 40% lower than desktop, watch mobile recordings specifically.

### 4. Implement the top quick fix

Take the #1 hypothesis from the diagnosis (the one with highest expected lift and lowest effort). Implement it as a direct code change — no feature flag needed at Smoke level. Examples of quick fixes:

- Remove 2 non-essential form fields
- Fix a validation error that blocks 15% of users
- Add an OAuth option above the email form
- Fix a mobile layout issue causing tap target overlap
- Add a loading indicator where users think the page is broken

**Human action required:** Deploy the code change. Verify the fix is live by walking through the funnel yourself.

### 5. Measure the impact

Wait 7 days. Then pull the same PostHog funnel from step 2 for the post-fix period. Compare:

- Bottleneck step conversion rate: before vs after
- End-to-end funnel conversion rate: before vs after
- Volume: confirm sample sizes are comparable (at least 50 users through the bottleneck step)

### 6. Evaluate against threshold

Run the `threshold-engine` drill: did the bottleneck step conversion rate improve by >=10%?

If PASS: Proceed to Baseline. You have validated that instrumentation + diagnosis + fix produces measurable conversion lifts.
If FAIL: Review the hypothesis ranking from step 3. Was the #1 fix actually addressing the primary friction? Try the #2 hypothesis. If 2 fixes fail to produce >=10% lift, the bottleneck may require a deeper product change rather than a surface fix — note this and proceed to Baseline with realistic expectations.

## Time Estimate

- 1.5 hours: Instrument the funnel (PostHog events for each step, verify firing)
- 1 hour: Build the PostHog funnel, identify bottleneck, establish baselines
- 1 hour: Session recording review and friction classification (15-25 recordings)
- 0.5 hours: Generate hypotheses and select the top fix
- 0.5 hours: Implement and deploy the quick fix
- 0.5 hours: Measure impact after 7 days and evaluate

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnel tracking, session recordings, path analysis | Free tier (1M events/mo, 5K recordings/mo) — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost:** Free (PostHog free tier covers Smoke-level volume)

## Drills Referenced

- `signup-funnel-audit` — Instruments the funnel, builds PostHog funnels, identifies the primary bottleneck with baseline metrics
- the funnel drop off diagnosis workflow (see instructions below) — Diagnoses root cause of the bottleneck using segment analysis, path comparison, and session recording review
- `threshold-engine` — Evaluates whether the >=10% improvement threshold was met
