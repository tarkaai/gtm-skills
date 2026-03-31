---
name: ai-user-segmentation-scalable
description: >
  AI Behavior Segmentation -- Scalable Automation. Expand personalization to all segments,
  run A/B tests on segment-specific experiences, and scale to 500+ users with >=75%
  segment assignment accuracy and >=10% personalization retention lift.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: ">=75% segment accuracy at 500+ users and >=10% retention lift from personalized segment experiences vs control"
kpis: ["Segment stability at scale", "Retention lift vs control", "Personalization conversion rate per segment", "Segment count", "Experiment velocity"]
slug: "ai-user-segmentation"
install: "npx gtm-skills add product/retain/ai-user-segmentation"
drills:
  - ab-test-orchestrator
  - cohort-insight-generation
  - threshold-engine
---
# AI Behavior Segmentation -- Scalable Automation

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Find the 10x multiplier for behavioral segmentation. Expand personalization from 3 segments to all identified segments. Run systematic A/B tests on personalized experiences to find what drives the biggest retention lift per segment. Scale to 500+ users while maintaining segment accuracy and growing personalization lift from 5% to 10%+.

**Pass threshold:** >=75% segment assignment accuracy (stability) across 500+ users AND >=10% retention lift from personalized experiences vs. the control group.

## Leading Indicators

- All identified segments (5-8) have live personalized experiences
- A/B tests running on at least 2 segments simultaneously
- Week-over-week segment stability holds at >75% as user count grows past 500
- Personalization conversion rate (CTA clicks) diverges meaningfully across segments (each segment responds to different content)
- Cohort insights identify at least 2 actionable improvements per month
- Retention lift trending upward month-over-month

## Instructions

### 1. Expand personalization to all segments

At Baseline, you personalized for the top 3 segments. Now extend the the segment personalization routing workflow (see instructions below) drill to cover all identified segments:

For each remaining segment:
1. Create Intercom in-app messages using the segment's personalization strategy from the cluster definitions
2. Build a 4-email Loops sequence tailored to the segment's behavior pattern
3. Configure a PostHog feature flag that delivers the segment-specific experience
4. Set up the n8n routing to enroll users on segment assignment

**For small segments (<5% of users):** Do not build fully custom experiences. Instead, map small segments to the nearest large segment's experience and note the mapping. At scale, re-evaluate whether small segments should be merged or given distinct treatment.

### 2. Scale the segmentation pipeline

Verify the the behavior segmentation pipeline workflow (see instructions below) handles 500+ active users:

- Test the weekly n8n workflow with the full user base. Measure execution time. If it exceeds 30 minutes, optimize: batch PostHog queries by 200 users, parallelize assignment API calls.
- Monitor Claude API costs at scale. At 500 users in batches of 30, you need ~17 assignment calls per week. At current Sonnet pricing, this costs ~$0.35/week.
- Increase the monthly cluster refresh to also include a segment quality validation pass (from the behavior segmentation pipeline workflow (see instructions below) step 10).

### 3. Run systematic A/B tests per segment

Run the `ab-test-orchestrator` drill to test personalization variants within each segment:

**Test 1 -- Message content:**
For the 2 largest segments, create a variant in-app message with a different CTA and value proposition. Split each segment's treatment group: 50% see variant A (current), 50% see variant B. Run for 2 weeks. Measure: CTA click rate, downstream action completion, 14-day retention.

**Test 2 -- Email cadence:**
For the segment with the lowest email engagement, test a different cadence: 3 emails over 7 days (faster) vs. the current 4 emails over 14 days. Measure: open rate, click rate, unsubscribe rate, 14-day retention.

**Test 3 -- Feature flag gating:**
For the "Casual Browser" archetype (or your equivalent low-engagement segment), test a guided experience: a product tour that fires on the first session after segment assignment. Compare against the current approach (in-app message only). Measure: feature adoption rate, session depth, 14-day retention.

Run 1 test at a time per segment (no stacking). Target: 2 experiments per month across all segments.

### 4. Generate cohort insights

Run the `cohort-insight-generation` drill monthly:

1. Compare retention curves across all behavioral segments
2. For each segment, identify the biggest drop-off point in the retention curve
3. Generate hypotheses for why each segment retains or churns at different rates
4. Prioritize interventions: focus on the segment with the highest churn rate AND the largest potential lift

Feed the top-ranked insight into the next A/B test cycle. This creates a flywheel: segmentation -> insights -> experiments -> improved personalization -> better retention -> refined segmentation.

### 5. Tune segment boundaries

As A/B test results accumulate, refine the segmentation model:

- If two segments respond identically to personalization (same engagement rates, same retention), merge them. Fewer, more distinct segments are better than many similar ones.
- If one segment has very high variance in outcomes (some users retain, some churn), it may contain two sub-populations. Re-run cluster discovery with more behavior dimensions to split it.
- If the "Unclassified" group grows beyond 15%, the cluster definitions are stale. Trigger an immediate cluster refresh.

Update the cluster definitions in the the behavior segmentation pipeline workflow (see instructions below) and propagate to all downstream personalization.

### 6. Build the scale monitoring dashboard

Extend the PostHog dashboard from Baseline with scale-specific panels:

- **Segment distribution at scale:** Stacked area chart showing segment sizes over time. Watch for concentration drift.
- **Personalization lift trend:** Line chart comparing treatment vs. control retention, week-over-week. This is the primary signal that personalization is working.
- **Experiment tracker:** Table showing active and completed A/B tests, their status, and results.
- **Per-segment retention funnel:** Side-by-side funnels for each segment showing the path from segment assignment to 30-day retention.
- **API cost tracker:** Monthly Claude API spend for clustering. Should stay under $5/mo at 500 users.

### 7. Evaluate against threshold

Run the `threshold-engine` drill after 2 months:

- **Segment accuracy at scale:** >=75% of 500+ users remain in the same segment week-over-week. Lower than Baseline threshold (80%) because larger populations naturally have more boundary cases.
- **Retention lift:** >=10% higher 14-day retention in the treatment group vs. control. This is a doubling of the Baseline lift, driven by expanded personalization and A/B test wins.

If PASS: Proceed to Durable. The segmentation scales, personalization works, and experiments are improving outcomes.

If FAIL on stability at scale: The clustering model breaks down at volume. Likely causes: too many segments for the population size (merge small ones), behavior vectors are too sensitive to weekly noise (smooth with 14-day rolling averages instead of 7-day), or the monthly cluster refresh is not frequent enough (move to bi-weekly).

If FAIL on retention lift: The personalization content is not bold enough. Review A/B test results: if no variant ever outperforms the default significantly, the differentiation between segment experiences is too subtle. Try fundamentally different experiences: feature gating by segment, different onboarding paths, or segment-specific pricing prompts.

## Time Estimate

- 8 hours: Expand personalization to all segments (in-app messages, emails, tours)
- 6 hours: Scale the pipeline and optimize for 500+ users
- 12 hours: Design and run 4-6 A/B tests over 2 months
- 8 hours: Generate and act on cohort insights (monthly)
- 6 hours: Tune segment boundaries based on test results
- 5 hours: Build monitoring dashboard, evaluate threshold
- 5 hours: Documentation and preparation for Durable handoff

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, cohorts, feature flags, experiments | Growth plan ~$0/mo up to usage limits -- [posthog.com/pricing](https://posthog.com/pricing) |
| Claude API (Anthropic) | Weekly clustering at scale | ~$2-5/mo at 500 users -- [anthropic.com/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| Intercom | Segment-specific in-app messages and tours for all segments | ~$74-300/mo depending on user count -- [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Segment-specific email sequences for all segments | Starter $49/mo or Growth $99/mo -- [loops.so/pricing](https://loops.so/pricing) |

**Estimated play-specific cost:** ~$125-400/mo (Intercom + Loops primary costs; Claude API marginal)

## Drills Referenced

- the behavior segmentation pipeline workflow (see instructions below) -- Weekly pipeline scaled to 500+ users with quality validation
- the segment personalization routing workflow (see instructions below) -- Expanded personalization for all segments
- `ab-test-orchestrator` -- Systematic A/B testing of personalization variants per segment
- `cohort-insight-generation` -- Monthly insights driving the experiment roadmap
- `threshold-engine` -- Evaluates scale metrics against pass thresholds
