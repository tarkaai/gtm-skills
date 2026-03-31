---
name: email-subject-test-pipeline
description: Run structured A/B tests on email subject lines across lifecycle sequences to improve open rates for retained users
category: Messaging
tools:
  - Loops
  - PostHog
  - n8n
fundamentals:
  - loops-ab-testing
  - loops-broadcasts
  - loops-audience
  - loops-sequences
  - posthog-custom-events
  - posthog-funnels
  - n8n-workflow-basics
---

# Email Subject-Line Test Pipeline

This drill runs a structured subject-line A/B test on retention-focused email campaigns. It covers variant generation, send splitting, metric collection, winner selection, and rollout of the winning subject to the full segment.

## Input

- A lifecycle email campaign (sequence or broadcast) in Loops targeting retained users
- Baseline open-rate data for the campaign (at least 2 prior sends)
- A test hypothesis: what framing change you expect to lift opens (e.g., question vs. statement, personalization vs. generic, urgency vs. curiosity)

## Steps

### 1. Select the email to test

Choose one email from an active Loops sequence or an upcoming broadcast that targets retained users. Prioritize emails with:
- High send volume (>500 recipients per send)
- Below-average open rate compared to your account median
- A clear retention goal (re-engagement, feature adoption, renewal reminder)

Pull the current subject line and its historical open rate via the Loops API. This becomes the control.

### 2. Generate subject-line variants

Create 1 variant (A/B test) using a specific framing change. Variant categories that move open rates for retention emails:

- **Personalization:** Include the user's name, company, or product usage data (e.g., "{{firstName}}, your 3 reports from last week")
- **Curiosity gap:** Tease a benefit without revealing it (e.g., "The feature 73% of power users missed")
- **Social proof:** Reference peer behavior (e.g., "Teams like yours are saving 4 hours/week")
- **Direct value:** State the benefit plainly (e.g., "New: export reports as PDF in one click")
- **Urgency:** Time-bound framing (e.g., "Your annual renewal is in 14 days")

The variant MUST differ from the control in exactly one dimension. Same body content, same sender, same send time.

### 3. Configure the test split in Loops

Using the `loops-ab-testing` fundamental:

- For broadcasts: send variant A (control) to 25% of the segment, variant B to 25%, hold 50% for the winner
- For sequences: duplicate the sequence step, assign each variant to a random 50/50 split of new entrants
- Set the test duration: 24-48 hours for broadcasts, or until 200+ opens per variant for sequences

### 4. Instrument tracking in PostHog

Using the `posthog-custom-events` fundamental, fire events when Loops sends and when users engage:

```
email_subject_test_sent: { test_id, variant (A|B), email_id, user_id }
email_subject_test_opened: { test_id, variant, email_id, user_id }
email_subject_test_clicked: { test_id, variant, email_id, user_id, link_url }
email_subject_test_unsubscribed: { test_id, variant, email_id, user_id }
```

Build an n8n workflow using `n8n-workflow-basics` that listens for Loops webhook events (send, open, click, unsubscribe) and forwards them to PostHog with the test_id and variant properties.

Using `posthog-funnels`, create a funnel: sent -> opened -> clicked. Filter by test_id. This shows the full engagement path per variant.

### 5. Evaluate results

After the test period:

1. Pull open rate, click rate, and unsubscribe rate per variant from PostHog
2. Check sample size: need 200+ sends per variant for reliable open-rate comparison
3. Winner criteria: variant with higher open rate AND no increase in unsubscribe rate >0.5%
4. If open rate difference is <3 percentage points, declare it a tie and keep the simpler subject

### 6. Roll out the winner

- For broadcasts: send the winning subject to the held-back 50%
- For sequences: update the sequence step in Loops to use the winning subject for all future entrants using `loops-sequences`
- Log the result: test_id, winning variant, open rate lift, and the subject-line pattern that won

## Output

- A tested subject line with measured open-rate lift
- PostHog funnel showing sent -> opened -> clicked per variant
- A documented pattern (e.g., "personalization beats generic by +8pp for re-engagement emails")
- Updated Loops sequence or broadcast using the winning subject

## Triggers

Run this drill on every major lifecycle email before scaling it. At Baseline, run 1 test per week. At Scalable, run 2-3 tests per week across all active sequences.
