---
name: cohort-insight-generation
description: Analyze cohort retention data to generate ranked, actionable insights with root-cause hypotheses and recommended interventions
category: Retention
tools:
  - Anthropic
  - PostHog
  - Attio
fundamentals:
  - posthog-retention-analysis
  - posthog-cohorts
  - posthog-user-path-analysis
  - hypothesis-generation
  - attio-notes
---

# Cohort Insight Generation

This drill takes the structured retention data from `cohort-retention-extraction` and produces ranked insights: what is driving retention differences between cohorts, what the probable root causes are, and what specific actions to take. Insights are stored in Attio and logged to PostHog for tracking.

## Input

- Structured JSON output from `cohort-retention-extraction` (cohort survival data, divergent cohort flags)
- PostHog session recording access for behavioral investigation
- Attio records for logging insights and tracking action outcomes

## Steps

### 1. Classify divergent cohorts by pattern

Group the divergent cohorts from the extraction output into pattern categories:

- **Activation gap:** Early droppers with Week 1 retention 30%+ below baseline. These users signed up but never found value.
- **Habit failure:** Normal Week 1-2 but steep decline at Week 3-4. These users tried the product but did not form a habit.
- **Value plateau:** Retention holds through Week 4 then drops at Week 6-8. These users got initial value but hit a ceiling.
- **Consistent outperformer:** Above-baseline retention at every interval. Something about this cohort drives stickiness.

Each pattern implies a different root cause and different intervention.

### 2. Investigate root causes with PostHog data

For each divergent cohort, pull additional context:

**For underperformers — use `posthog-user-path-analysis`:**
- Pull the most common user paths for the divergent cohort vs. the baseline population
- Identify where paths diverge: do underperformers skip onboarding? Use fewer features? Visit different pages?
- Check: do underperformers come from a specific acquisition channel, geography, or device type?

**For outperformers — use `posthog-cohorts`:**
- Create a PostHog cohort for the outperforming users
- Compare their properties against the general population: plan type, company size, acquisition source, onboarding completion status
- Identify which features outperformers use that others do not

### 3. Generate hypotheses using Claude

Pass the following context to the `hypothesis-generation` fundamental:

- The cohort survival data (baseline vs. divergent curves)
- The user path analysis showing behavioral differences
- The property comparison showing demographic/acquisition differences

Prompt structure:
```
You are analyzing retention cohort data for a SaaS product. Here is the data:

[cohort survival JSON]
[user path divergence summary]
[property comparison summary]

For each divergent cohort, generate:
1. A root cause hypothesis (what is driving the retention difference)
2. Confidence level (high/medium/low based on data strength)
3. A specific intervention recommendation (what to change and for whom)
4. Expected impact (estimated retention improvement if the intervention works)
5. How to test the hypothesis (what experiment to run)

Rank the hypotheses by expected impact * confidence.
```

### 4. Structure insights for action

Format each insight as:

```json
{
  "insight_id": "RCA-2026-W13-001",
  "cohort": "2026-W08",
  "pattern": "habit_failure",
  "hypothesis": "Users from paid ads skip the onboarding checklist at 3x the rate of organic users, resulting in 40% lower Week 3 retention. They land directly on the dashboard without context.",
  "confidence": "high",
  "intervention": "For paid-ad users, force the onboarding checklist before dashboard access. Use Intercom product tour triggered by utm_source=paid.",
  "expected_impact": "+8pp Week 4 retention for paid-ad cohorts",
  "test_method": "A/B test forced onboarding vs. current flow for paid-ad signups using PostHog feature flag",
  "priority_score": 8.5
}
```

### 5. Log insights to Attio and PostHog

Using the `attio-notes` fundamental, create a note on the relevant campaign or product record in Attio with:
- The ranked insight list
- Date generated
- Status: "pending_action" (updated later to "actioned", "tested", "validated", or "rejected")

Using `posthog-custom-events`, log:
- Event: `cohort_insight_generated`
- Properties: `insight_id`, `pattern`, `confidence`, `priority_score`, `cohort_label`

### 6. Track insight-to-action conversion

An insight only counts toward the play's pass threshold when it leads to an action:
- "Action" means: a PostHog feature flag was created for the experiment, an Intercom message was configured, a Loops sequence was modified, or a product change was deployed
- Track this by updating the Attio note status from `pending_action` to `actioned`
- Log: `cohort_insight_actioned` event in PostHog with `insight_id` and `action_type`

## Output

- Ranked list of insights with root-cause hypotheses, intervention recommendations, and priority scores
- Attio notes with insight details and tracking status
- PostHog events for pipeline measurement
- Ready-to-act recommendations that feed into `ab-test-orchestrator` or `autonomous-optimization`

## Triggers

At Smoke: run once manually after extraction. At Baseline: run weekly after `cohort-retention-extraction` completes. At Scalable+: run weekly with multi-dimensional cohort data.
