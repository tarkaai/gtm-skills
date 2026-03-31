---
name: follow-up-ab-testing
description: Run structured A/B tests on demo follow-up variables — timing, subject lines, content types, and CTAs — using PostHog experiments
category: Sales
tools:
  - PostHog
  - n8n
  - Attio
  - Anthropic
fundamentals:
  - posthog-experiments
  - posthog-feature-flags
  - posthog-custom-events
  - n8n-workflow-basics
  - n8n-scheduling
  - attio-deals
  - attio-notes
  - hypothesis-generation
  - experiment-evaluation
---

# Follow-Up A/B Testing

This drill runs structured experiments on demo follow-up sequences to find the highest-converting combination of timing, messaging, content, and CTAs. Each experiment isolates one variable, runs until statistical significance, and promotes the winner into the default sequence.

## Input

- Active demo follow-up automation (from `demo-follow-up-automation` drill) processing 10+ demos per month
- PostHog tracking events from the follow-up cadence (`demo_follow_up_sent`, `demo_follow_up_replied`, `next_step_booked`)
- At least 4 weeks of baseline performance data
- n8n instance for experiment orchestration

## Steps

### 1. Build the experiment backlog

Using `hypothesis-generation`, generate hypotheses for follow-up optimization. Feed Claude the baseline data:

```
POST https://api.anthropic.com/v1/messages

Prompt: "Given this demo follow-up performance data, generate 5 experiment hypotheses ranked by expected impact.

Baseline metrics:
- Recap email open rate: {X}%
- Day 1 check-in reply rate: {X}%
- Day 3 value asset click rate: {X}%
- Overall sequence response rate: {X}%
- Next step booking rate: {X}%
- Average touches to booking: {X}

For each hypothesis, return JSON:
{
  'hypotheses': [
    {
      'variable': 'timing|subject_line|content_type|cta|personalization',
      'hypothesis': 'Changing X from A to B will increase Y by Z%',
      'control': 'current value/approach',
      'variant': 'proposed change',
      'primary_metric': 'the metric to measure',
      'min_sample_size': estimated samples needed per variant,
      'risk': 'low|medium|high',
      'expected_impact': 'percentage improvement estimate'
    }
  ]
}"
```

Store hypotheses in Attio as campaign notes with status "queued."

Common experiment categories for demo follow-ups:
- **Timing:** Recap within 1 hour vs 4 hours. Day 1 check-in vs Day 2. Day 3 asset vs Day 5.
- **Subject lines:** Reference demo topic vs prospect name vs question-based vs benefit-based.
- **Content type:** Case study vs integration guide vs ROI calculator vs Loom video.
- **CTA:** Cal.com link vs "reply with your availability" vs specific proposed time.
- **Personalization depth:** Light (name + company) vs deep (demo-specific pain quotes + feature references).

### 2. Set up experiment infrastructure in PostHog

Using `posthog-feature-flags`, create a feature flag for each active experiment:

```json
{
  "key": "demo-followup-exp-{experiment_id}",
  "filters": {
    "groups": [
      {
        "variant": "control",
        "rollout_percentage": 50
      },
      {
        "variant": "test",
        "rollout_percentage": 50
      }
    ]
  }
}
```

Using `posthog-experiments`, create the experiment linked to the feature flag:
- Primary metric: the hypothesis's primary_metric
- Secondary metrics: open rate, click rate, reply rate, booking rate
- Minimum sample size: from hypothesis
- Maximum duration: 28 days

### 3. Wire experiments into the follow-up automation

Using `n8n-workflow-basics`, modify the `demo-follow-up-automation` workflows to check experiment flags:

At each follow-up touch point:
1. Query PostHog for the prospect's experiment variant assignment
2. If assigned to "test" variant: use the experimental version (different timing, subject line, content, or CTA)
3. If assigned to "control": use the current default
4. Log the variant in PostHog event properties: `experiment_id`, `variant`, `touch_number`

Example for a timing experiment on the Day 3 value asset:
```
- Control: send value asset email exactly 72 hours after recap
- Test: send value asset email 120 hours after recap (Day 5 instead of Day 3)
- Metric: asset click rate and next-step booking rate within 7 days of asset send
```

### 4. Monitor running experiments

Using `n8n-scheduling`, create a daily experiment monitor:

1. For each running experiment, query PostHog for current results
2. Check: has the experiment reached minimum sample size in both variants?
3. Check guardrails: is the test variant's reply rate or booking rate >30% worse than control? If yes, auto-disable the experiment and revert to control.
4. If sample size reached, mark as "ready-for-evaluation"
5. Send daily status to founder: experiment name, samples per variant, current lift, days remaining

### 5. Evaluate and promote winners

When an experiment reaches "ready-for-evaluation":

Using `experiment-evaluation`, run the statistical analysis:

```
POST https://api.anthropic.com/v1/messages

Prompt: "Evaluate this A/B test result:

Control ({n_control} samples): {metric} = {control_value}
Test ({n_test} samples): {metric} = {test_value}

Calculate:
1. Relative lift (test vs control)
2. Statistical significance (p-value using chi-squared for proportions or t-test for continuous)
3. 95% confidence interval for the lift
4. Practical significance (is the lift large enough to matter for this play?)

Decision framework:
- If p < 0.05 AND lift > 10%: ADOPT the variant
- If p < 0.05 AND lift between 0-10%: ADOPT only if cost-neutral
- If p > 0.05: INCONCLUSIVE, extend or abandon
- If lift is negative with p < 0.05: REVERT immediately"
```

For winners (ADOPT):
1. Update the follow-up automation to use the winning variant as the new default
2. Log the change in Attio: what changed, the measured lift, and the date
3. Fire PostHog event: `experiment_winner_adopted`
4. Queue the next experiment from the backlog

For losers or inconclusive:
1. Disable the feature flag
2. Log the result
3. If inconclusive: decide whether to extend (need more data) or abandon (not worth testing further)
4. Queue the next experiment

### 6. Track cumulative optimization impact

Using `posthog-custom-events`, maintain a running log of all experiment results and their impact on the overall follow-up performance:

- Total experiments run
- Experiments won / lost / inconclusive
- Cumulative lift from all adopted changes
- Current "best known" configuration (the combination of all winners)

Generate a monthly optimization report showing: what was tested, what changed, and the net impact on demo-to-next-step conversion.

## Output

- Structured experiment backlog with prioritized hypotheses
- PostHog experiments running on follow-up sequences
- Automated monitoring and guardrail enforcement
- Statistical evaluation of each experiment
- Cumulative performance improvement tracking
- Monthly optimization reports

## Triggers

Experiment monitoring runs daily via n8n cron. Experiments launch automatically when a slot opens. Evaluations trigger when sample size is reached. The backlog is refreshed monthly or when it empties.
