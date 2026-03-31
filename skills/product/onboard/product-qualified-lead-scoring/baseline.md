---
name: product-qualified-lead-scoring-baseline
description: >
  PQL Scoring System — Baseline Run. Automate the PQL scoring pipeline so every
  new user is scored within minutes of signup, scores update in real-time as
  product behavior changes, and PQLs route to sales automatically.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "Automated scoring pipeline live; ≥70% of users who converted in the last 30 days were scored Hot or Warm before conversion"
kpis: ["Scoring accuracy (% of converters correctly identified)", "Time-to-score (minutes from signup to first score)", "PQL-to-meeting conversion rate", "Score decay compliance"]
slug: "product-qualified-lead-scoring"
install: "npx gtm-skills add product/onboard/product-qualified-lead-scoring"
drills:
  - engagement-score-computation
  - lead-routing
---

# PQL Scoring System — Baseline Run

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Always-on PQL scoring pipeline: every new user is enriched, scored, tiered, and synced to Attio within minutes of signup. Scores update in real-time when product behavior changes (pricing page view, feature usage, teammate invite). Stale scores decay automatically. PQLs route to the correct sales rep without manual intervention. At least 70% of users who actually converted in the last 30 days were scored Hot or Warm before their conversion event.

## Leading Indicators

- New signups receive a `lead_scored` event in PostHog within 10 minutes of account creation
- Real-time re-scoring fires when intent signals arrive (visible as updated `lead_scored` events with higher intent scores)
- Score decay workflow runs daily and reduces intent scores for inactive users
- PQL alerts reach the correct sales rep within 1 hour of a user crossing the Hot threshold
- Attio pipeline shows PQLs entering the sales funnel automatically

## Instructions

### 1. Build the automated scoring pipeline

Run the the lead score automation workflow (see instructions below) drill to create the always-on scoring infrastructure. This builds four n8n workflows:

**Workflow 1 — New-user scoring:** Triggered by Attio webhook on new person creation. Enriches the user in Clay (firmographics for fit score), queries PostHog for their product events (intent signals), computes composite PQL score, writes to Attio, and logs to PostHog.

**Workflow 2 — Intent-update re-scoring:** Triggered by PostHog webhook events (`pricing_page_viewed`, `core_feature_used`, `invite_sent`, `integration_connected`). Looks up the person in Attio, recalculates intent score with the new signal, updates composite score and tier. If the tier changed (e.g., Cold to Warm, or Warm to Hot), fires a `lead_tier_changed` event in PostHog.

**Workflow 3 — Score decay:** Daily cron. Queries Attio for users where `last_scored` > 14 days ago and `intent_score` > 0. Applies 50% decay to intent score. Recalculates composite and tier. Logs `lead_score_decayed` event.

**Workflow 4 — Model update re-scoring:** Manual webhook trigger. Re-scores all leads in Attio when scoring criteria or weights change.

### 2. Build per-user engagement scores

Run the `engagement-score-computation` drill to compute daily engagement scores for every active user. This provides a richer behavioral signal than raw event counts:

- Configure the four scoring dimensions: frequency (30% weight), breadth (25%), depth (25%), recency (20%)
- Build the daily n8n pipeline that computes scores and writes `engagement_score`, `engagement_tier`, and `engagement_trend` to Attio
- Create PostHog cohorts for each engagement tier (Power User, Engaged, Casual, At Risk, Dormant)
- Feed engagement score as an input to the PQL intent score: users in the Power User or Engaged tier get +10 bonus intent points; users in At Risk or Dormant tiers get intent score reduced by 10 points

This creates a two-layer scoring system: raw PQL score (fit + intent) enhanced by engagement score trend data.

### 3. Auto-route PQLs to sales

Run the `lead-routing` drill to build automated PQL-to-sales routing:

- **Hot tier (PQL score >=70):** Create a deal in Attio, assign to the appropriate sales rep based on routing rules (territory, deal size, industry), send a Slack notification to the rep with the user's profile, engagement history, and top product actions.
- **Warm tier with rising engagement (score 40-69, engagement trend = Rising):** Add to a "Watch" list in Attio. If engagement continues rising for 3 consecutive days, auto-promote to Hot routing.
- **Warm tier stable:** Add to a nurture Loops sequence with product tips and case studies.
- **Cold tier:** No sales routing. Monitor only.

Include context in every PQL alert sent to sales: the user's company, role, plan, top 3 product actions, days since signup, engagement tier, and engagement trend. Sales reps should have enough context to personalize their outreach without additional research.

### 4. Evaluate scoring accuracy

After 2 weeks of automated scoring, measure accuracy against the threshold:

- Query Attio for all users who converted (upgraded to paid or booked a sales meeting) in the last 30 days
- Check their PQL tier at the time of conversion (from `lead_scored` events in PostHog)
- **Primary threshold:** >=70% of converters were scored Hot or Warm before conversion
- **Secondary check:** Time-to-score for new signups is under 10 minutes (check timestamps between `signup_completed` and first `lead_scored` event)

If PASS: Automated scoring reliably identifies converters. Proceed to Scalable.

If FAIL on accuracy: Review which converters were scored Cold. Identify what intent signals they exhibited that the model missed. Add those signals to the scoring criteria and re-run Workflow 4 (model update re-scoring).

If FAIL on latency: Debug the n8n workflow execution time. Common fixes: reduce Clay enrichment timeout, pre-cache frequently-queried PostHog data, optimize webhook processing.

## Time Estimate

- 6 hours: Build 4 n8n scoring workflows (new-user, re-scoring, decay, model update)
- 4 hours: Set up engagement score computation pipeline
- 3 hours: Build PQL routing rules and Slack/Attio notifications
- 3 hours: Monitor, debug, and evaluate scoring accuracy

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Product event tracking, behavioral queries, cohorts | Free up to 1M events/month; paid ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Scoring automation workflows (4 workflows) | Self-hosted free; Cloud from EUR 24/month ([n8n.io/pricing](https://n8n.io/pricing)) |
| Clay | Firmographic enrichment for fit scoring | Pro $149/month ([clay.com/pricing](https://www.clay.com/pricing)) |
| Attio | CRM: score storage, deal creation, routing | Pro $29/seat/month ([attio.com/pricing](https://attio.com/pricing)) |
| Loops | Nurture sequences for Warm-tier PQLs | Free up to 1,000 contacts; Starter $49/month ([loops.so/pricing](https://loops.so/pricing)) |

## Drills Referenced

- the lead score automation workflow (see instructions below) — builds the 4 n8n workflows for automated scoring, re-scoring, decay, and model updates
- `engagement-score-computation` — computes daily per-user engagement scores that enhance PQL intent scoring
- `lead-routing` — auto-routes PQLs to the correct sales rep with full context
