---
name: chatbot-escalation-routing
description: Configure intelligent escalation routing from AI chatbot to human agents based on topic, sentiment, user value, and churn risk
category: Product
tools:
  - Intercom
  - n8n
  - Attio
  - PostHog
fundamentals:
  - intercom-bots
  - intercom-ticket-tagging
  - intercom-user-properties
  - n8n-triggers
  - attio-deals
  - posthog-cohorts
---

# Chatbot Escalation Routing

This drill builds intelligent routing for conversations that the AI chatbot cannot resolve. Instead of dumping all escalations into a generic queue, it routes based on the user's value, the topic's severity, and the user's churn risk — ensuring high-value and at-risk users get faster, more attentive human support.

## Input

- AI chatbot deployed with escalation events flowing (see `ai-chatbot-deployment` drill)
- Intercom workspace with team inboxes configured
- Attio CRM with account records and support churn scores (if available)
- n8n instance for routing logic

## Steps

### 1. Define routing tiers

Establish escalation priority tiers:

- **P0 — Immediate**: Security incidents, data loss, billing disputes, cancellation requests. Route to senior support or CS lead. SLA: first response within 15 minutes.
- **P1 — High**: Enterprise accounts, churn-risk-critical accounts, production-blocking bugs. Route to dedicated account support or CS owner. SLA: first response within 1 hour.
- **P2 — Standard**: General technical issues, how-to questions the bot could not answer, feature requests. Route to general support queue. SLA: first response within 4 hours.
- **P3 — Low**: Non-urgent feedback, minor UI issues, general questions. Route to general queue, lowest priority. SLA: first response within 24 hours.

### 2. Build classification logic in n8n

Use the `n8n-triggers` fundamental to create a workflow triggered by Intercom's `conversation.user.replied` webhook when Fin escalates:

1. **Receive webhook**: Extract conversation ID, user ID, escalation reason, and the last few messages
2. **Classify topic**: Use the `intercom-ticket-tagging` fundamental to run LLM classification on the conversation. Output: category, severity, sentiment, churn signals
3. **Enrich with CRM data**: Query Attio via `attio-deals` for the user's company record: plan type, MRR, support churn score, CS owner
4. **Compute priority tier**: Apply rules:
   - Category in [security-incident, data-loss, billing-dispute] OR cancellation intent detected → P0
   - Plan = enterprise OR support_churn_score > 75 OR severity = critical → P1
   - Severity = high OR sentiment = frustrated → P2
   - Everything else → P3

### 3. Configure Intercom routing

Route conversations to the correct team inbox based on priority:

```
POST https://api.intercom.io/conversations/{id}/parts
{
  "message_type": "assignment",
  "assignee_id": "{team_inbox_id}",
  "body": "Auto-routed: P{tier} — {category} — {company_name} ({plan}). Churn score: {score}."
}
```

Add a note to the conversation with context so the human agent has full background before replying:

```
POST https://api.intercom.io/conversations/{id}/parts
{
  "message_type": "note",
  "admin_id": "{bot_admin_id}",
  "body": "Escalation context:\n- Topic: {category}\n- Severity: {severity}\n- Sentiment: {sentiment}\n- Churn signals: {signals}\n- Account: {company_name} ({plan}, ${mrr}/mo)\n- Churn risk score: {score}/100\n- Bot attempted: {messages_before_handoff} messages\n- Escalation reason: {reason}"
}
```

### 4. Set up SLA monitoring

Use `posthog-cohorts` to create cohorts for each priority tier. Track:
- Time from escalation to first human response (by tier)
- Time from escalation to resolution (by tier)
- Whether SLA was met for each conversation

Fire PostHog events:
- `escalation_routed` — properties: tier, category, company_id, mrr
- `escalation_first_response` — properties: tier, response_time_seconds, sla_met (boolean)
- `escalation_resolved` — properties: tier, resolution_time_seconds, csat_rating

### 5. Build the escalation quality loop

Weekly, review escalation routing accuracy:

1. Sample 10 routed conversations from each tier
2. Verify the assigned tier was correct (was the priority appropriate?)
3. Check whether context notes helped the agent resolve faster
4. If misrouted conversations exceed 15%, adjust routing rules

### 6. Scale with segment-specific routing

As volume grows, create specialized routing for high-volume topics:
- Billing questions → Billing team inbox
- Integration issues → Technical support inbox
- Feature requests → Product feedback inbox (lower priority, async processing)
- Enterprise accounts → Dedicated CS owner via Attio lookup

## Output

- Automated priority classification for every escalated conversation
- Intelligent routing to the correct team inbox with full context
- SLA tracking per priority tier via PostHog
- Escalation quality monitoring with weekly accuracy reviews

## Triggers

- **Real-time**: Fires on every Fin AI escalation via Intercom webhook → n8n
- **Weekly review**: Routing accuracy audit via n8n cron every Monday
