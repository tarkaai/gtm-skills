---
name: lead-scoring-system-smoke
description: >
  Lead Scoring System — Smoke Test. Define fit + intent scoring criteria, manually score 20 leads,
  and validate that Hot-tier leads book meetings at >=2x the rate of Cold-tier leads.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Hot leads have >=2x meeting rate vs Cold leads in 1 week"
kpis: ["Meeting rate by tier", "Score distribution across tiers", "Time to first meeting by tier"]
slug: "lead-scoring-system"
install: "npx gtm-skills add sales/qualified/lead-scoring-system"
drills:
  - icp-definition
  - lead-score-model-setup
---

# Lead Scoring System — Smoke Test

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Outcomes

Hot-tier leads (score >=80) book meetings at >=2x the rate of Cold-tier leads (score <50) within 1 week of outreach. This validates that the scoring model predicts engagement before investing in automation.

## Leading Indicators

- Score distribution shows meaningful separation (not all leads in one tier)
- Hot leads respond to outreach faster than Cold leads (measured in hours to first reply)
- Hot leads require fewer touchpoints before booking (1-2 vs 4+)

## Instructions

### 1. Define your ICP

Run the `icp-definition` drill. Analyze your closed-won deals in Attio to extract firmographic patterns (company size, industry, buyer persona, pain points). Document the ICP with must-have and disqualification criteria. This takes 1-2 hours.

### 2. Design the scoring model

Run the `lead-score-model-setup` drill. Define 3-5 fit criteria (firmographics, max 50 points) and 3-5 intent signals (behaviors, max 50 points). Set tier thresholds: Hot >=80, Warm 50-79, Cold <50. Build the scoring formula in Clay and document the rubric. This takes 1-2 hours.

### 3. Score 20 leads

Pull 20 recent leads from Attio. For each lead:

1. Check enriched firmographic data against fit criteria using Clay. Assign fit points.
2. Check PostHog for website activity (pricing page views, content downloads). Assign intent points manually.
3. Check your email tool for any reply history. Assign intent points.
4. Compute composite score and assign tier.
5. Write scores back to Attio using the `attio-lead-scoring` fundamental.
6. Fire `lead_scored` events in PostHog with fit_score, intent_score, lead_score, and lead_tier properties.

### 4. Validate score distribution

Check the distribution: aim for 15-25% Hot, 30-50% Warm, 30-50% Cold. If all leads cluster in one tier, adjust point values in the scoring model to create better separation. Re-score if needed.

### 5. Outreach all 20 leads with identical messaging

**Human action required:** Send the same outreach message to all 20 leads (email or LinkedIn). Do not vary the message by tier — this isolates scoring quality from messaging quality. Log every touchpoint in Attio with status (sent, opened, replied, meeting booked).

### 6. Track results for 1 week

For each lead, log the outcome in Attio: replied (positive/negative), meeting booked, ignored, bounced. Fire corresponding PostHog events: `outreach_sent`, `outreach_replied`, `meeting_booked` with `lead_tier` as a property.

### 7. Evaluate against threshold

After 1 week, compute meeting rate by tier:
- Hot tier meeting rate = (Hot leads who booked) / (total Hot leads)
- Cold tier meeting rate = (Cold leads who booked) / (total Cold leads)
- **Pass:** Hot rate >= 2x Cold rate
- **Fail:** Hot rate < 2x Cold rate

If PASS: document the scoring model and proceed to Baseline.

If FAIL: analyze which fit criteria and intent signals are not predictive. Check false negatives (Cold leads that booked — what signals did the model miss?) and false positives (Hot leads that ignored — what inflated their score?). Adjust criteria and re-run the Smoke test.

## Time Estimate

- ICP definition: 1.5 hours
- Scoring model design: 1.5 hours
- Scoring 20 leads: 1 hour
- Outreach execution (human): 0.5 hours
- Tracking and evaluation: 0.5 hours
- Total: ~5 hours of effort spread over 1 week (waiting for responses)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — store leads, scores, outreach logs | Standard stack (excluded from play budget) |
| PostHog | Analytics — track scoring events and outreach outcomes | Standard stack (excluded from play budget) |
| Clay | Enrichment — firmographic data for fit scoring | Free tier: 100 credits/month ([clay.com/pricing](https://www.clay.com/pricing)) |

**Play-specific cost: Free** (Clay free tier covers 20 leads)

## Drills Referenced

- `icp-definition` — defines firmographic and behavioral criteria that feed the scoring model
- `lead-score-model-setup` — designs the scoring formula, assigns point values, and scores the initial batch
