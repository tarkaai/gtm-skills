---
name: personal-usage-analytics-scalable
description: >
  Personal Usage Analytics — Scalable Automation. Run A/B tests to prove causal retention impact.
  Personalize metrics per user segment. Scale to all user cohorts with automated optimization.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "40 hours over 6 weeks"
outcome: "Statistically significant ≥5pp retention lift in A/B test (analytics surface ON vs. OFF) at 95% confidence, sustained across 500+ users"
kpis: ["A/B test retention lift (causal)", "Segment-specific view rates", "Personalized CTA conversion rate", "Analytics-driven feature adoption rate"]
slug: "personal-usage-analytics"
install: "npx gtm-skills add product/retain/personal-usage-analytics"
drills:
  - ab-test-orchestrator
  - usage-analytics-engagement-monitor
  - churn-prevention
---

# Personal Usage Analytics — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Pass threshold: an A/B test (analytics surface enabled vs. disabled) shows a statistically significant ≥5 percentage point improvement in 30-day retention at 95% confidence, measured across 500+ users.

This establishes CAUSAL impact — not just correlation. Baseline showed that analytics viewers retain better. Scalable proves the analytics surface CAUSES better retention, not just that already-engaged users happen to view it.

## Leading Indicators

- A/B test enrollment rate hitting target sample size on schedule
- Treatment group (analytics ON) showing higher weekly session frequency by week 2
- Personalized CTAs converting at 2x+ the rate of generic CTAs
- Segment-specific view rates (each segment above 35%)
- At-risk user intervention via analytics surface reducing churn signals

## Instructions

### 1. Design and launch the causal A/B test

Run the `ab-test-orchestrator` drill to set up the experiment:

- **Hypothesis:** "If users see their personal usage analytics, their 30-day retention rate will improve by ≥5 percentage points, because seeing quantified value reinforces the habit loop and makes switching costs visible."
- **Control group:** Analytics surface hidden (feature flag OFF). Users see the product without the analytics page or any discovery prompts.
- **Treatment group:** Analytics surface enabled (feature flag ON). Full analytics experience with discovery prompts.
- **Primary metric:** 30-day retention rate (% of users with a session 30 days after enrollment)
- **Secondary metrics:** Weekly session frequency, feature breadth (distinct features used), churn rate
- **Guardrail metric:** Support ticket rate (ensure the analytics surface does not confuse users)
- **Sample size:** Calculate using baseline retention rate from Baseline level. For a 5pp lift from a 40% baseline, you need approximately 800 per variant at 80% power.
- **Duration:** Minimum 30 days after the last user enrolls (to measure 30-day retention). Total test duration: 6-8 weeks depending on enrollment velocity.

Enroll NEW users only (users already exposed to analytics at Baseline would contaminate the control). Use PostHog feature flags for random assignment at the user level.

### 2. Personalize analytics by user segment

While the A/B test runs, improve the treatment group experience. Using the `usage-analytics-engagement-monitor` drill data, identify which user segments have the lowest view rates or engagement depth. For each segment, customize:

- **Power users** (top 20% by activity): Show percentile ranking ("You're in the top 5% of users"), comparative benchmarks, and advanced metrics (API calls, integration usage). CTA: promote advanced features or beta programs.
- **Regular users** (middle 60%): Show growth trends and streaks. Highlight weekly momentum: "You completed 12 workflows this week, up 20% from last week." CTA: suggest underused features based on their usage pattern.
- **Light users** (bottom 20% by activity): Show cumulative value to combat abandonment: "You've saved X hours total with [Product]." Emphasize simple wins. CTA: "Pick up where you left off" with deep link to their last active workspace.
- **Declining users** (week-over-week activity drop >30%): Show their peak usage period vs. current: "In February you were running 5 automations/day. This week: 1." CTA: "Reconnect with your workflows" or "Schedule a refresher session."

Implement segment-specific analytics surfaces using PostHog cohorts for segmentation and feature flags for variant selection.

### 3. Integrate analytics with churn prevention

Run the `churn-prevention` drill integrated with the analytics surface. For users whose analytics data shows declining engagement:

1. The n8n aggregation workflow (from `usage-analytics-surface-build`) detects declining trends in the user's metrics
2. Flag these users in PostHog as "analytics-declining" cohort
3. Trigger a targeted Intercom in-app message on their analytics page: "We noticed your [metric] is down this week. Here's what might help: [contextual recommendation]"
4. If the user does not re-engage within 7 days, escalate to the standard churn prevention flow (email outreach, personal touch for high-value accounts)

The analytics surface becomes both the retention tool AND the early warning system. Users who stop checking their stats are themselves a churn signal.

### 4. Run segment-level engagement experiments

Use the `ab-test-orchestrator` to run smaller experiments within the treatment group:

- Test different metric selections for each segment (which 3-5 stats resonate most?)
- Test CTA types: feature suggestion vs. resume-work vs. milestone-chase vs. social-proof
- Test email digest frequency: weekly vs. bi-weekly vs. monthly
- Test discovery prompt timing: immediate on login vs. after first action vs. end of session

Run one experiment at a time per segment. Each experiment needs 200+ users per variant minimum. Log results in Attio for hypothesis refinement.

### 5. Evaluate against threshold

After the primary A/B test reaches sample size and 30-day retention is measurable for all enrolled users:

- Query PostHog experiment results. Check: is the retention lift ≥5pp at 95% confidence?
- Check secondary metrics: did the treatment group also show higher session frequency and feature breadth?
- Check guardrails: did support ticket rate stay stable?

If PASS: The analytics surface causally improves retention. Roll it out to 100% of users. Proceed to Durable for autonomous optimization.

If FAIL (lift exists but <5pp or not significant): The surface helps, but not enough. Review segment-level results — does the surface work for some segments but not others? Focus on the segments where it works, redesign for segments where it does not. Extend the test with improved personalization.

If FAIL (no lift or negative): The analytics surface does not cause retention improvement. The Baseline correlation was driven by selection bias (engaged users both view analytics and retain). Pivot: instead of a standalone analytics page, embed usage stats directly into the product workflow where users already are (sidebar widget, email footer, login splash).

## Time Estimate

- 6 hours: A/B test design, sample size calculation, and PostHog experiment setup
- 10 hours: segment-specific analytics surface personalization
- 8 hours: churn prevention integration
- 8 hours: segment-level engagement experiments (2 hours each x 4 experiments)
- 4 hours: weekly monitoring during the 6-week test period
- 4 hours: final evaluation, cohort analysis, and decision

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | A/B testing, feature flags, experiments, cohort analysis | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | Segment-specific in-app messages, churn intervention prompts | From $39/mo — https://www.intercom.com/pricing |
| n8n | Aggregation pipeline, churn detection workflows | Free self-hosted or from $24/mo cloud — https://n8n.io/pricing |
| Attio | Experiment logging, play health tracking | From $29/seat/mo — https://attio.com/pricing |

**Estimated play-specific cost:** ~$100-200/mo (increased n8n compute for personalization, higher PostHog event volume from A/B tracking)

## Drills Referenced

- `ab-test-orchestrator` — designs and runs the causal A/B test proving retention impact, plus segment-level experiments
- `usage-analytics-engagement-monitor` — provides segment-level engagement data for personalization decisions
- `churn-prevention` — integrates declining analytics trends with automated churn interventions
