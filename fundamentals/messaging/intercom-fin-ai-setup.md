---
name: intercom-fin-ai-setup
description: Configure Intercom Fin AI agent for automated support resolution
tool: Intercom
difficulty: Config
---

# Set Up Intercom Fin AI Agent

Configure Fin AI to resolve inbound support conversations autonomously using your knowledge base, with escalation rules for questions it cannot answer.

## Prerequisites
- Intercom account (Essential plan minimum, $29/mo)
- Help articles published in Intercom Help Center (see `intercom-help-articles`)
- Intercom Messenger installed on your product

## Step 1: Enable Fin AI Agent

In the Intercom API or dashboard, enable Fin on your workspace. Fin is an add-on billed at $0.99 per resolution (you are only charged when Fin successfully resolves a conversation without human handoff).

Via the Intercom REST API, configure Fin's behavior:

```
PUT https://api.intercom.io/ai/agent/config
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "enabled": true,
  "languages": ["en"],
  "tone": "professional",
  "answer_length": "concise",
  "handoff_behavior": "offer_to_connect"
}
```

## Step 2: Connect Knowledge Sources

Fin answers questions from three source types:

1. **Intercom Help Center articles** (automatically indexed when published)
2. **External URLs** — add your docs site, changelog, API reference:
   ```
   POST https://api.intercom.io/ai/content_sources
   {
     "type": "url",
     "url": "https://docs.yourproduct.com",
     "crawl_depth": 3,
     "refresh_frequency": "weekly"
   }
   ```
3. **Custom answers** — manually authored Q&A pairs for questions not covered by articles:
   ```
   POST https://api.intercom.io/ai/custom_answers
   {
     "question": "What is your refund policy?",
     "answer": "We offer full refunds within 30 days of purchase. Email billing@yourproduct.com or reply here and we'll process it within 2 business days.",
     "tags": ["billing"]
   }
   ```

## Step 3: Configure Escalation Rules

Define when Fin should hand off to a human agent:

```
PUT https://api.intercom.io/ai/agent/escalation_rules
{
  "rules": [
    {"trigger": "user_requests_human", "action": "handoff_immediate"},
    {"trigger": "confidence_below", "threshold": 0.5, "action": "handoff_with_context"},
    {"trigger": "max_bot_replies", "count": 4, "action": "handoff_with_context"},
    {"trigger": "sentiment_negative", "action": "handoff_with_context"},
    {"trigger": "topic_match", "topics": ["billing-dispute", "data-deletion", "security-incident"], "action": "handoff_immediate"}
  ]
}
```

Critical: never trap users in a bot loop. If Fin cannot resolve in 4 exchanges, escalate with full conversation context.

## Step 4: Set Audience Targeting

Control which users see Fin vs. direct human support:

```
PUT https://api.intercom.io/ai/agent/targeting
{
  "default": "fin_first",
  "overrides": [
    {"segment": "enterprise_plan", "behavior": "human_first"},
    {"segment": "churn_risk_critical", "behavior": "human_first"}
  ]
}
```

Start with Fin for all users, then carve out VIP segments for human-first routing.

## Step 5: Verify Deployment

Test Fin's behavior by opening a conversation from a test user account:
1. Ask a question covered by your help articles — Fin should resolve it
2. Ask an off-topic question — Fin should say it cannot help and offer human handoff
3. Type "talk to a human" — Fin should immediately hand off
4. Ask a billing dispute question — should trigger immediate escalation

Query Fin metrics via API:
```
GET https://api.intercom.io/ai/agent/metrics?period=7d
```

Response includes: total_conversations, resolutions, handoffs, avg_resolution_time, resolution_rate, csat_score.

## Pricing

- Fin AI Agent: $0.99 per resolution (minimum 50 resolutions/mo = $49.50/mo minimum)
- Intercom Essential base: $29/seat/mo
- Proactive Support Plus (optional): $99/mo
- [intercom.com/pricing](https://www.intercom.com/pricing)

## Error Handling

- If Fin returns no answer, check knowledge source sync status via `GET /ai/content_sources`
- If resolution rate is below 30%, add more custom answers for frequently asked questions
- If CSAT is below 3.5, review Fin conversations for incorrect answers and update knowledge sources

## Alternative Tools

- **Zendesk AI** — similar resolution-based AI agent, $1.00/automated resolution — [zendesk.com/pricing](https://www.zendesk.com/pricing)
- **Freshdesk Freddy AI** — included in Pro plan ($49/agent/mo) — [freshdesk.com/pricing](https://www.freshdesk.com/pricing)
- **HelpScout AI** — AI drafts included in Plus plan ($40/user/mo) — [helpscout.com/pricing](https://www.helpscout.com/pricing)
- **Crisp AI** — chatbot included in Pro plan ($25/mo) — [crisp.chat/pricing](https://crisp.chat/en/pricing/)
- **Tidio Lyro AI** — $0.50/resolved conversation — [tidio.com/pricing](https://www.tidio.com/pricing/)
