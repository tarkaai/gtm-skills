---
name: support-ticket-analysis
description: Extract, classify, and analyze support ticket patterns to identify churn signals and product gaps
category: Product
tools:
  - Intercom
  - Anthropic
  - PostHog
  - Attio
fundamentals:
  - intercom-conversations-export
  - intercom-ticket-tagging
  - posthog-custom-events
  - attio-custom-attributes
---

# Support Ticket Analysis

This drill extracts support tickets from Intercom, classifies them by category/severity/sentiment, and produces an account-level summary that feeds into churn scoring and product improvement workflows.

## Input

- Intercom API access token
- Time range to analyze (default: last 90 days for backfill, last 7 days for ongoing)
- PostHog project for event logging
- Attio workspace for CRM enrichment

## Steps

### 1. Export conversations from Intercom

Use the `intercom-conversations-export` fundamental to pull all closed and open conversations for the analysis period. For initial setup, pull the last 90 days. For ongoing runs, pull only conversations created or updated since the last sync.

Store the raw conversation data locally or in a staging table. Key fields: conversation_id, contact_id, company_id, created_at, closed_at, state, message_count, first_message_body, conversation_rating, time_to_resolution.

### 2. Classify each conversation

Use the `intercom-ticket-tagging` fundamental to classify every untagged conversation. For each ticket, the LLM assigns:
- **Category**: bug, feature-request, billing, how-to, integration, performance, access, data-loss
- **Severity**: critical, high, medium, low
- **Sentiment**: frustrated, neutral, positive
- **Churn signals**: churn-risk, escalation, repeat-issue, competitor-mention, cancellation-intent

Apply the resulting tags back to Intercom so human agents also benefit from the classification.

### 3. Aggregate by account

Group classified tickets by company_id (or contact_id for non-company accounts). For each account, compute:

- Total tickets in period
- Ticket velocity (tickets per week, compared to their historical average)
- Category distribution (% bug, % billing, etc.)
- Severity distribution
- Average CSAT rating
- Repeat issues (same category + similar description appearing 2+ times)
- Sentiment trend (improving, stable, declining based on chronological sentiment scores)
- Escalation count
- Competitor mentions
- Cancellation intent signals

### 4. Log events to PostHog

Use the `posthog-custom-events` fundamental to fire events for tracking:

- `support_ticket_classified` per ticket: properties include category, severity, sentiment, churn_signals
- `support_account_summary_updated` per account: properties include total_tickets, velocity_change, avg_csat, risk_signals_count

These events enable PostHog dashboards, cohort analysis, and correlation with other product events (usage decline, feature abandonment).

### 5. Enrich CRM records

Use the `attio-custom-attributes` fundamental to update company records in Attio with:
- `support_tickets_30d`: count
- `support_severity_trend`: improving/stable/worsening
- `support_top_category`: most frequent category
- `support_repeat_issues`: list of recurring problems
- `support_avg_csat`: rating

This gives CS reps account context without switching tools.

## Output

- Classified and tagged conversations in Intercom
- Per-account ticket summary data in PostHog and Attio
- Ready for downstream scoring by `support-churn-correlation` drill

## Triggers

- **Backfill**: Run once during initial setup (Step 1 of Smoke level)
- **Ongoing**: Run daily via n8n cron to process new/updated conversations
- **Real-time**: Intercom webhook on `conversation.created` triggers immediate classification
