---
name: ai-chatbot-deployment
description: Deploy an AI-powered support chatbot, connect knowledge sources, and verify it resolves basic user questions
category: Enablement
tools:
  - Intercom
  - PostHog
fundamentals:
  - intercom-fin-ai-setup
  - intercom-help-articles
  - intercom-bots
  - intercom-user-properties
  - posthog-custom-events
  - posthog-feature-flags
---

# AI Chatbot Deployment

This drill deploys an AI support chatbot inside your product, connects it to your knowledge base, and instruments tracking so you can measure resolution rates and user satisfaction from day one.

## Input

- Intercom workspace with Messenger installed on your product
- At least 10 help articles covering your most common support questions
- PostHog project with user identification configured
- List of your top 20 support questions (from historical tickets or team knowledge)

## Steps

### 1. Prepare knowledge base

Use the `intercom-help-articles` fundamental to verify you have articles covering your top 20 support questions. For each question, confirm an article exists with a clear answer. If gaps exist, write and publish articles before proceeding.

Group articles into collections that match your product areas (Getting Started, Billing, Core Feature, Integrations, Troubleshooting). Aim for 5-15 articles per collection.

### 2. Configure Fin AI agent

Use the `intercom-fin-ai-setup` fundamental to enable Fin AI on your workspace:
- Set tone to match your brand (professional, friendly, technical)
- Connect your Help Center as the primary knowledge source
- Add your docs site and API reference as external URL sources
- Create custom answers for the 5 most common questions not covered by articles

### 3. Configure escalation rules

Use the `intercom-bots` fundamental to set up escalation paths:
- User explicitly requests human → immediate handoff
- Confidence below 50% → handoff with conversation context
- 4+ bot replies without resolution → handoff with context
- Billing disputes, security incidents, data deletion → immediate human routing
- Enterprise/VIP customers → human-first (no bot intermediary)

### 4. Set up user properties for targeting

Use the `intercom-user-properties` fundamental to ensure these properties flow into Intercom:
- `plan_type` — controls VIP routing
- `signup_date` — identifies new users who may need more help
- `last_active_date` — identifies potentially frustrated inactive users
- `support_churn_score` — if available from churn prediction, routes high-risk users to humans

### 5. Instrument chatbot tracking events

Use the `posthog-custom-events` fundamental to fire events at each interaction point:

- `chatbot_conversation_started` — user opens chat or asks first question
  - Properties: `user_id`, `page_url`, `user_plan`, `is_first_contact`
- `chatbot_resolved_by_ai` — Fin resolves without human handoff
  - Properties: `topic`, `resolution_time_seconds`, `messages_count`
- `chatbot_escalated_to_human` — Fin hands off to human agent
  - Properties: `reason` (low_confidence, user_request, max_replies, topic_rule), `messages_before_handoff`
- `chatbot_csat_submitted` — user rates the conversation
  - Properties: `rating` (1-5), `resolved_by` (ai, human), `topic`
- `chatbot_article_suggested` — Fin links to a help article
  - Properties: `article_id`, `article_title`, `user_clicked` (true/false)

Wire these events via an n8n webhook that listens to Intercom conversation webhooks and forwards to PostHog.

### 6. Deploy with feature flag

Use the `posthog-feature-flags` fundamental to create a feature flag `ai-support-chatbot` that controls which users see the AI chatbot. Start with 10-20% rollout to a test cohort.

Rollout plan:
- Week 1: 10-20% of users (monitor resolution rate and CSAT)
- Week 2: 50% if metrics are healthy (resolution rate >30%, CSAT >3.5)
- Week 3: 100% if metrics hold

### 7. Verify deployment

Run end-to-end tests from a test account:
1. Ask a question covered by articles → Fin should resolve
2. Ask a question not in knowledge base → Fin should offer handoff
3. Say "talk to a human" → immediate handoff
4. Ask a billing dispute question → immediate escalation
5. Verify all 5 PostHog events fire correctly with correct properties

## Output

- Fin AI agent live and answering questions for the test cohort
- Escalation rules routing edge cases to humans
- Full PostHog event tracking on every chatbot interaction
- Feature flag controlling rollout percentage

## Triggers

- **Initial deployment**: Run once during Smoke level setup
- **Configuration updates**: Re-run Steps 2-3 when adding knowledge sources or adjusting escalation rules
