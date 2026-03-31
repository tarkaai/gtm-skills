---
name: outbound-gift-campaigns-baseline
description: >
  Outbound Gift Campaigns — Baseline Run. Send 50 personalized gifts per month with
  automated tracking, delivery attribution, and a coordinated follow-up sequence.
  First always-on gift outreach operation.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Direct"
level: "Baseline Run"
time: "18 hours over 1 month"
outcome: "≥ 25% response rate from 50 targeted gifts per month, with ≥ 5 meetings booked"
kpis: ["Response rate", "Cost per response", "Cost per meeting", "Meetings booked"]
slug: "outbound-gift-campaigns"
install: "npx gtm-skills add OutboundFounderLed/Marketing/SolutionAware/outbound-gift-campaigns"
drills:
  - posthog-gtm-events
  - follow-up-automation
  - threshold-engine
---

# Outbound Gift Campaigns — Baseline Run

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Direct

## Outcomes

Run gift outreach as an always-on outbound channel with automated tracking, response attribution, and a coordinated multi-channel follow-up triggered by gift delivery. Send 50 gifts per month with full event tracking in PostHog and response logging in Attio. Prove that the response rate holds at 25%+ over sustained sending and that the cost per meeting justifies the gift spend.

## Leading Indicators

- Delivery success rate ≥ 90% for physical gifts, ≥ 98% for eGifts
- eGift redemption rate ≥ 60% (recipients actually use the gift cards)
- Follow-up emails increasing response rate by ≥ 30% vs. gift-only (measured in Smoke)
- Cost per response below $75
- At least 1 meeting booked per week from gift recipients

## Instructions

### 1. Set up event tracking

Run the `posthog-gtm-events` drill to configure the gift campaign event taxonomy in PostHog. Define these events:

- `gift_sent` — Gift dispatched via platform (properties: contact_id, campaign_id, gift_type, gift_value, platform, signal_type, variant_id)
- `gift_delivered` — Platform confirms delivery (properties: contact_id, days_to_deliver, platform)
- `gift_failed` — Delivery failed (properties: contact_id, failure_reason)
- `gift_redeemed` — eGift card redeemed by recipient (properties: contact_id, gift_value, days_to_redeem)
- `gift_response` — Any response attributed to a gift (properties: contact_id, response_type, days_since_delivery, gift_type)
- `gift_meeting_booked` — Meeting attributed to gift campaign (properties: contact_id, gift_type, days_since_delivery, meeting_source)
- `gift_deal_created` — Deal in CRM attributed to gift campaign (properties: contact_id, deal_value, days_since_gift)

Set up webhooks from your gifting platform (Tremendous, Sendoso, or Reachdesk) to n8n, which fires the corresponding PostHog events.

### 2. Configure delivery tracking and response attribution

Set up the gift tracking and attribution pipeline:

**Tremendous webhooks (for eGift cards):**
Register a webhook in Tremendous to POST to your n8n webhook URL on events: `REWARDS.DELIVERY.SUCCEEDED`, `REWARDS.REDEEMED`. n8n parses the webhook payload, extracts the contact_id from metadata, and fires the corresponding PostHog event.

**Sendoso/Reachdesk webhooks (for physical gifts):**
Register webhooks for `shipped`, `delivered`, `returned` events. n8n processes these and updates both PostHog and Attio.

**Attribution logic:**
Any response from a gift recipient within 30 days of confirmed delivery is attributed to the gift. Track the response source (direct email reply, follow-up sequence reply, LinkedIn, inbound booking) to measure which follow-up channel converts best.

### 3. Build the follow-up automation

Run the `follow-up-automation` drill to create an n8n workflow triggered by gift delivery confirmation:

**Trigger:** Gift delivery webhook (Tremendous `REWARDS.DELIVERY.SUCCEEDED` or Sendoso/Reachdesk `delivered` event) via n8n.

**Sequence:**

1. **Day 0 (delivery confirmed):** No action. Let the gift make its impression.

2. **Day 3:** Send a short email from the founder's address via Instantly:
   ```
   Subject: Hope the {{gift_description}} landed well

   Hey {{first_name}},

   I sent you {{gift_description}} earlier this week — {{one_sentence_reason}}.

   I've been following what {{company}} is doing with {{specific_initiative}},
   and I think there's a strong fit with what we're building at {{your_company}}.

   Would 15 minutes this week work to explore?

   {{founder_name}}
   ```

3. **Day 7 (if no response):** Send a LinkedIn connection request with a personalized note referencing the gift: "Hey {{first_name}} — I sent you {{gift_description}} last week. Wanted to connect here too. Would love to chat about {{topic}}."

4. **Day 12 (if no response):** Final follow-up email with a different angle — share a relevant case study or a short insight specific to their industry/role. No further mention of the gift.

5. **Day 30 (if no response):** Mark as `gift_no_response` in Attio and PostHog. Do not send more follow-ups. The prospect may convert later via other channels — the gift planted a seed.

**Important:** The follow-up sequence is what turns a gift from a nice gesture into a pipeline-generating play. In Smoke, you likely saw that most responses came after the follow-up email, not from the gift alone. Track which step generates each response.

### 4. Scale to 50 gifts per month

Run the the gift campaign send workflow (see instructions below) drill at Baseline volume:

- Source 50 new signal-detected prospects per month via Clay and push to Attio
- Run AI gift selection for each prospect (review in batches of 10-15 rather than individually)
- Send in weekly batches of ~12-13 gifts to spread follow-up workload evenly
- Use the gift type(s) that performed best in Smoke; if you tested both eGifts and books, standardize on the winner for now

**Budget allocation per month:**
- 50 gifts x $25-50 average value = $1,250-$2,500 in gift costs
- Platform fees: $0 (Tremendous) to ~$1,700/mo (Sendoso Essential prorated)
- Enrichment: ~$149/mo (Clay)
- Follow-up tools: ~$30/mo (Instantly)

**Human action required:** Review AI gift selections in weekly batches (~15 minutes per batch). Override any low-confidence selections. Approve the personalized notes before the batch is sent.

### 5. Monitor and evaluate weekly

Each week, review in PostHog:
- Gifts sent vs. delivered (delivery rate)
- eGift redemption rate
- Responses this week (by type: email, meeting, LinkedIn)
- Which follow-up step generated each response
- Cost per response and cost per meeting this week

At the end of month 1, calculate:
- Overall response rate (all responses / gifts delivered)
- Cost per response
- Cost per meeting
- Pipeline value generated from gift-attributed meetings
- ROI: pipeline generated / total gift spend

**Pass threshold:** ≥ 25% response rate from 50 gifts per month, with ≥ 5 meetings booked.

If PASS: The channel sustains at Baseline volume. Proceed to Scalable to introduce signal-triggered automation and A/B testing.

If FAIL: Diagnose by funnel stage:
- **Delivery failures?** Fix addresses or switch to eGift-only.
- **Low redemption rate?** Gift cards are going to spam — check email deliverability.
- **Responses but no meetings?** The follow-up sequence needs work — adjust the ask.
- **No responses at all?** Re-evaluate ICP targeting and gift relevance.

## Time Estimate

- 4 hours: Event tracking, webhook setup, and attribution configuration (one-time)
- 4 hours: Follow-up automation workflow in n8n (one-time)
- 2 hours/week: Prospect sourcing, AI gift selection review, and batch sending (8 hours over 4 weeks)
- 30 minutes/week: Monitoring and evaluation (2 hours over 4 weeks)
- Total: ~18 hours over 1 month (8 hours one-time setup + 10 hours ongoing)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Tremendous | Send eGift cards (no platform fee) | Free — pay only gift face value. https://www.tremendous.com/pricing |
| Sendoso | Send physical gifts, books, swag (alternative) | From ~$20,000/yr. https://www.sendoso.com/compare-plans |
| Clay | Signal detection and prospect enrichment | From $149/mo. https://www.clay.com/pricing |
| Attio | CRM — contacts, send logs, response tracking | Free for small teams. https://attio.com/pricing |
| PostHog | Event tracking, attribution analytics | Free up to 1M events/mo. https://posthog.com/pricing |
| n8n | Webhook processing, follow-up automation | Free (self-hosted) or from $24/mo. https://n8n.io/pricing |
| Instantly | Follow-up email sequences | From $30/mo. https://instantly.ai/pricing |
| Anthropic API | AI gift selection | ~$0.75/mo for 50 selections. https://www.anthropic.com/pricing |

**Estimated total monthly cost (eGift path):** $1,250-$2,500 (gifts) + ~$200 (tools) = **$1,450-$2,700/mo**

**Estimated total monthly cost (Sendoso path):** $1,250-$2,500 (gifts) + ~$1,900 (platform + tools) = **$3,150-$4,400/mo**

## Drills Referenced

- the gift campaign send workflow (see instructions below) — AI-powered gift selection, batch sending, and CRM logging for 50 gifts/month
- `posthog-gtm-events` — Set up standardized gift campaign event taxonomy in PostHog
- `follow-up-automation` — Multi-channel follow-up sequence triggered by gift delivery
- `threshold-engine` — Evaluate results against the 25% response rate pass threshold
