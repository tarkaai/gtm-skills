---
name: gift-ab-testing
description: Design and execute A/B tests on gift type, value, personalization, and timing to optimize response rates
category: Gifting
tools:
  - PostHog
  - Attio
  - Anthropic
fundamentals:
  - posthog-experiments
  - posthog-dashboards
  - gift-tracking-attribution
  - attio-contacts
  - experiment-evaluation
---

# Gift A/B Testing

Design, execute, and evaluate A/B tests for outbound gift campaigns. Tests one variable at a time across gift type, value, personalization approach, and timing. Uses PostHog experiments for statistical rigor and attribution.

## Input

- A hypothesis to test (e.g., "Books produce higher response rates than eGift cards for VP-level prospects")
- Minimum sample size per variant (recommended: 50+ per variant at Scalable, 20+ at Baseline)
- The metric to optimize (primary: response rate; secondary: cost per meeting, pipeline per dollar spent)
- Attribution window: 30 days from delivery

## Testable Variables

### 1. Gift Type
- Control: eGift cards ($25-50)
- Variants: books, gourmet food, branded swag, experiential gifts, charitable donations

### 2. Gift Value
- Control: $25 eGift card
- Variants: $50, $75, $100 — test whether higher value produces proportionally higher response

### 3. Personalization Depth
- Control: Generic note ("Thought you might enjoy this")
- Variant A: Signal-personalized ("Congrats on the Series B — thought this would help with the scaling challenges ahead")
- Variant B: Deep research personalized ("Saw your post about {{specific_topic}} — this book covers exactly that")

### 4. Timing Relative to Signal
- Control: Send within 48 hours of signal detection
- Variants: Same day, 1 week after, 2 weeks after — test freshness vs. processing time

### 5. Follow-up Sequence
- Control: Gift only, no follow-up
- Variant A: Gift + email follow-up 3 days after delivery
- Variant B: Gift + email + LinkedIn follow-up

## Steps

### 1. Set up the experiment in PostHog

Use the `posthog-experiments` fundamental to create a feature flag that assigns contacts to control vs. treatment:

```json
{
  "name": "gift-test-{{test_id}}",
  "key": "gift-ab-{{variable}}-{{date}}",
  "filters": {
    "groups": [
      {"variant": "control", "rollout_percentage": 50},
      {"variant": "treatment", "rollout_percentage": 50}
    ]
  }
}
```

### 2. Assign contacts to variants

When a contact enters the gift campaign pipeline, evaluate the PostHog feature flag to assign them to control or treatment. Store the assignment in Attio: `gift_variant = control|treatment` and `gift_test_id = {{test_id}}`.

### 3. Execute the test

Send gifts according to the variant assignment. For the variable being tested, apply the control configuration to control contacts and the treatment configuration to treatment contacts. All other variables remain constant across both groups.

### 4. Wait for the attribution window

Gift campaign A/B tests require patience. Physical gifts take 3-7 days to deliver, and responses trickle in over 2-4 weeks. Minimum test duration: 4 weeks from the last send in the batch.

Monitor the experiment weekly using `posthog-dashboards`:
- Sample size per variant (are both groups filling?)
- Preliminary response rates (do NOT make decisions on preliminary data)
- Any anomalies (one variant getting all the high-value accounts?)

### 5. Evaluate results

After the attribution window closes, run the `experiment-evaluation` fundamental:

Pass control and treatment data:
- Sample size per variant
- Response count per variant
- Response rate per variant
- Cost per response per variant
- Meetings booked per variant
- Pipeline generated per variant

The evaluation returns:
- Statistical significance (p-value)
- Confidence interval for the difference
- Recommendation: ADOPT (treatment wins), REVERT (control wins), EXTEND (need more data), ITERATE (result suggests a new hypothesis)

### 6. Implement the decision

- **ADOPT:** Update the default campaign configuration to use the winning variant. Log the change in Attio as a campaign note. Update the PostHog experiment status to "completed — winner adopted."
- **REVERT:** Keep the control configuration. Log the result. The hypothesis was wrong — that is valuable data.
- **EXTEND:** Continue running the experiment for another 2 weeks. This happens when sample size is borderline.
- **ITERATE:** The result suggests a modified hypothesis. Log the insight and design the next test.

## Output

- A completed A/B test with statistical results
- A clear decision (adopt, revert, extend, iterate) with reasoning
- Updated campaign configuration if a winner was adopted
- Documented learnings stored in Attio and PostHog

## Guardrails

- Never run more than 1 active gift A/B test at a time per campaign
- Minimum 50 contacts per variant for reliable results at Scalable level
- Never test more than 1 variable simultaneously
- If response rate for either variant drops below 3% mid-test, investigate for confounding factors before continuing
- Maximum 2 gift A/B tests per month (attribution windows are long)
