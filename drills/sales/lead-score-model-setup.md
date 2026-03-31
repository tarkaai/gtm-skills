---
name: lead-score-model-setup
description: Design a lead scoring model with fit and intent dimensions, assign point values, and manually score an initial batch of leads
category: Sales
tools:
  - Attio
  - Clay
  - PostHog
fundamentals:
  - attio-lead-scoring
  - attio-contacts
  - clay-scoring
  - posthog-custom-events
---

# Lead Score Model Setup

This drill designs a lead scoring model from scratch: define fit criteria (firmographics), intent signals (behaviors), assign point values, and manually score a batch of leads to validate the model predicts engagement.

## Input

- ICP document (output from `icp-definition` drill)
- 20+ leads in Attio CRM with basic company and contact data
- PostHog tracking configured on your website (for intent signal capture)

## Steps

### 1. Define fit criteria and point values

Using your ICP document, select 3-5 firmographic attributes that distinguish good-fit leads from poor-fit ones. Assign point values that sum to a maximum of 50:

| Fit Criterion | Condition | Points |
|---------------|-----------|--------|
| Company size | 20-500 employees (ICP range) | +15 |
| Industry | Target industry match | +10 |
| Buyer role | Decision-maker title (VP+, Head of, Director) | +15 |
| Tech stack | Uses complementary/competing tool | +5 |
| Geography | Target market | +5 |

Store these criteria as a scoring rubric in Attio notes on your lead scoring campaign record.

### 2. Define intent signals and point values

Select 3-5 behavioral signals that indicate purchase readiness. Assign point values that sum to a maximum of 50:

| Intent Signal | Condition | Points |
|---------------|-----------|--------|
| Demo request | Submitted demo/contact form | +20 |
| Pricing page view | Visited pricing page (PostHog event) | +15 |
| Email reply | Replied to outreach email | +10 |
| Content download | Downloaded case study or whitepaper | +5 |
| Repeat website visit | 3+ sessions in 14 days | +5 |

Note: At Smoke level, some intent signals may need manual observation (checking PostHog for website events, checking email tool for replies). Automation comes at Baseline.

### 3. Build the scoring formula in Clay

Using the `clay-scoring` fundamental, create a Clay table with your 20+ leads and add formula columns:

- **Fit Score (0-50):** Sum of fit criterion points based on enriched data
- **Intent Score (0-50):** Sum of intent signal points (manually populated at Smoke; automated later)
- **Composite Score (0-100):** `fit_score + intent_score`
- **Tier:** `IF(composite >= 80, "Hot", IF(composite >= 50, "Warm", "Cold"))`

### 4. Score the initial batch

For each of the 20+ leads:

1. Check enriched firmographic data against fit criteria. Assign fit points.
2. Check PostHog for website activity (use `posthog-custom-events` to query page views). Assign intent points.
3. Check email/outreach tool for reply history. Assign intent points.
4. Compute composite score and tier.

### 5. Push scores to Attio

Using the `attio-lead-scoring` fundamental, write fit_score, intent_score, lead_score, and lead_tier to each person record in Attio. Set last_scored to today's date.

### 6. Log scoring events to PostHog

Using `posthog-custom-events`, fire a `lead_scored` event for each lead with properties:

```json
{
  "person_id": "...",
  "company_name": "...",
  "fit_score": 35,
  "intent_score": 25,
  "lead_score": 60,
  "lead_tier": "Warm",
  "scoring_method": "manual",
  "scoring_model_version": "v1"
}
```

### 7. Validate score distribution

Check that the score distribution is reasonable:
- At least 15-25% of leads should be Hot (if <15%, thresholds are too strict; if >40%, too lenient)
- Cold leads should represent the bottom 30-50%
- If all leads cluster in one tier, adjust point values to create separation

### 8. Document the model

Create an Attio note on the lead scoring campaign record with:
- Fit criteria and point values
- Intent signals and point values
- Tier thresholds
- Initial score distribution (X Hot, Y Warm, Z Cold)
- Date created and version number (v1)

## Output

- A documented lead scoring model with specific criteria and point values
- 20+ leads scored and tiered in Attio CRM
- `lead_scored` events in PostHog for analysis
- Score distribution validated

## Triggers

This is a one-time setup drill. Re-run when model criteria need updating (after analyzing which criteria correlate with closed deals).
