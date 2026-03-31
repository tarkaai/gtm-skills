---
name: nps-response-routing
description: Automatically route NPS survey responses to segment-specific follow-up actions based on score and context
category: Product
tools:
  - n8n
  - Intercom
  - Loops
  - Attio
  - PostHog
fundamentals:
  - n8n-triggers
  - n8n-workflow-basics
  - intercom-in-app-messages
  - loops-transactional
  - attio-contacts
  - attio-notes
  - attio-lists
  - posthog-custom-events
  - posthog-cohorts
---

# NPS Response Routing

This drill builds the automation layer that takes raw NPS survey responses and routes each one to the correct follow-up action. It replaces manual triaging of NPS data with a system that acts within minutes of a response arriving.

## Prerequisites

- NPS survey deployed and collecting responses (run `nps-feedback-loop` first)
- n8n instance for automation
- Intercom configured for in-app messaging
- Loops configured for transactional email
- Attio with contact records for all surveyed users

## Steps

### 1. Build the response ingestion workflow

Using `n8n-triggers`, create a workflow triggered by NPS survey submission. The trigger source depends on how the survey is deployed:

- **Intercom surveys**: n8n webhook listens for Intercom conversation event with survey tag
- **Typeform/custom**: n8n webhook receives form submission payload
- **In-app custom widget**: PostHog event `nps_survey_submitted` triggers n8n via webhook

The workflow receives: user_id, email, nps_score (0-10), open_text_response, survey_trigger_context (e.g., "30-day milestone", "quarterly", "post-support").

### 2. Enrich the response with usage context

Using `n8n-workflow-basics`, add context from PostHog and Attio before routing:

1. Query PostHog using `posthog-cohorts` for the user's segment: plan type, usage tier (power/regular/light), tenure (days since signup), recent activity trend (increasing/stable/declining)
2. Query Attio using `attio-contacts` for: current MRR, account size, previous NPS scores, open support tickets, account owner

Store the enriched response object:
```json
{
  "user_id": "usr_123",
  "nps_score": 9,
  "open_text": "Love the new dashboard feature",
  "plan": "pro",
  "mrr": 299,
  "usage_tier": "power",
  "tenure_days": 180,
  "activity_trend": "increasing",
  "previous_nps": [7, 8],
  "nps_trend": "improving",
  "open_tickets": 0,
  "account_owner": "sarah@company.com"
}
```

### 3. Classify and route by segment

Using `n8n-workflow-basics`, implement the routing logic:

**Promoters (9-10):**
- If tenure > 90 days AND usage_tier = "power": route to advocacy pipeline. Add to Attio "Advocacy Candidates" list using `attio-lists`. Tag the response with `advocacy_ready`.
- If open_text mentions a specific feature: log as testimonial candidate in Attio using `attio-notes`. Include the exact quote and the feature mentioned.
- All promoters: send a thank-you via `loops-transactional` within 1 hour. Include a referral link and a one-click review request.
- Fire PostHog event `nps_response_routed` with properties: segment=promoter, action=thank_you_sent, advocacy_candidate=true/false.

**Passives (7-8):**
- If activity_trend = "declining": escalate to medium priority. Send a personalized Loops email: "Thanks for your feedback. We noticed [feature they used most] — here's what's new there." Include a help article link and a feedback call booking link.
- If nps_trend = "declining" (previous score was higher): flag in Attio as "NPS Declining Passive" using `attio-notes`. Assign a follow-up task to the account owner.
- If activity_trend = "increasing": send a lighter touch. Intercom in-app message using `intercom-in-app-messages`: "Thanks for the feedback! Here's a feature you might not have tried yet: [unused feature based on PostHog data]."
- Fire PostHog event `nps_response_routed` with properties: segment=passive, action_taken, risk_level.

**Detractors (0-6):**
- If nps_score <= 3 OR mrr >= 500: critical priority. Create an Attio note using `attio-notes` with full context. Assign an urgent task to the account owner with a 24-hour SLA. Do NOT send an automated email — this requires personal outreach.
- If nps_score 4-6 AND open_text contains keywords (bug, broken, slow, crash, error, frustrated): route to support. Create an Attio note tagged "NPS Detractor - Product Issue". Send a Loops email: "We're sorry about your experience. Here's how we're fixing [category of issue]. A team member will follow up within 48 hours."
- If nps_score 4-6 AND open_text is feature request or pricing concern: send a Loops email acknowledging their feedback. Link to the public roadmap or pricing FAQ. Log in Attio for product team review.
- All detractors: fire PostHog event `nps_response_routed` with properties: segment=detractor, severity=critical/standard, has_open_tickets, action_taken.

### 4. Aggregate for product intelligence

Using `posthog-custom-events`, fire summary events that feed dashboards:

- `nps_daily_summary`: total responses, promoters count, passives count, detractors count, calculated NPS score, top 3 open-text themes (extracted by Claude via n8n AI node)
- `nps_theme_detected`: when the same keyword/theme appears in 3+ detractor responses in a 7-day window, fire an alert. This surfaces emerging product issues before they become widespread.

Using `attio-notes`, create a weekly NPS summary note on the company record: score trend, segment breakdown, top promoter quotes, top detractor themes, actions taken.

### 5. Close the loop tracking

Using `posthog-custom-events`, track whether routed actions actually completed:

- For promoters: did they submit a review, referral, or testimonial within 14 days?
- For passives: did their usage increase in the 14 days after follow-up?
- For detractors: was the follow-up completed within SLA? Did the user's next NPS score improve?

Log close-the-loop outcomes in Attio. These feed back into the `nps-health-monitor` drill at Durable level.

## Output

- Real-time NPS response routing with segment-specific actions
- Enriched response records in Attio with usage context
- Automated promoter thank-you and advocacy pipeline feeding
- Tiered detractor response with SLA-based escalation
- Product intelligence aggregation (theme detection, weekly summaries)
- Close-the-loop tracking for all segments

## Triggers

Runs on every NPS survey submission (event-driven via n8n webhook). Summary aggregation runs daily. Weekly report runs Monday morning.
