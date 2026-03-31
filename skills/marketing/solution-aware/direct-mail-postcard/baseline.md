---
name: direct-mail-postcard-baseline
description: >
  Direct Mail Postcards — Baseline Run. Send 100-200 postcards per month with automated
  tracking, delivery attribution, and a digital follow-up sequence triggered by postcard
  delivery. First always-on direct mail operation.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Other"
level: "Baseline Run"
time: "15 hours over 1 month"
outcome: "≥ 5% response rate (URL visits + meetings + replies) from 100-200 postcards over 1 month"
kpis: ["Delivery rate", "Response rate", "Cost per response", "Meetings booked"]
slug: "direct-mail-postcard"
install: "npx gtm-skills add marketing/solution-aware/direct-mail-postcard"
drills:
  - postcard-campaign-send
  - posthog-gtm-events
  - follow-up-automation
---

# Direct Mail Postcards — Baseline Run

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Other

## Outcomes

Run direct mail as an always-on outbound channel with automated tracking and digital follow-up. Send 100-200 postcards per month with full delivery tracking, response attribution, and a coordinated email/LinkedIn follow-up triggered by postcard delivery confirmation. Prove that the response rate holds at 5%+ over sustained sending.

## Leading Indicators

- Delivery rate ≥ 90% (address verification working correctly)
- Tracking URLs receiving clicks within 7 days of delivery
- Digital follow-ups (email after delivery) increasing overall response rate vs. postcard-only
- Cost per response below $20

## Instructions

### 1. Set up event tracking

Run the `posthog-gtm-events` drill to configure a standardized event taxonomy for direct mail. Define these events in PostHog:

- `direct_mail_sent` — Postcard created in Lob (properties: contact_id, campaign_id, variant)
- `direct_mail_delivered` — Lob webhook confirms delivery (properties: contact_id, days_to_deliver)
- `direct_mail_returned` — Postcard returned to sender (properties: contact_id, reason)
- `direct_mail_url_visited` — Tracking URL clicked (properties: contact_id, variant, campaign_id)
- `direct_mail_meeting_booked` — Meeting attributed to postcard (properties: contact_id, days_since_delivery)
- `direct_mail_response` — Any response attributed to postcard (properties: contact_id, response_type)

### 2. Configure delivery tracking and attribution

Run the the postcard response tracking workflow (see instructions below) drill to set up:
- Lob webhook integration with n8n for real-time delivery updates
- Automated CRM updates when postcards are delivered or returned
- Response attribution linking URL visits and meetings to specific postcards
- A 14-day attribution window for response measurement

### 3. Build the digital follow-up workflow

Run the `follow-up-automation` drill to create an n8n workflow triggered by postcard delivery:

**Trigger:** Lob `postcard.delivered` webhook event via n8n

**Sequence:**
1. Day 0 (delivery confirmed): No action — let the postcard speak for itself
2. Day 3: Send a short email from the founder's address: "I sent you a quick note in the mail earlier this week about {{pain_point}}. Did it land on your desk?" Keep it to 2-3 sentences. Reference the postcard specifically — this multiplies its impact.
3. Day 7 (if no response to email): Send a LinkedIn connection request with a note referencing both the postcard and the email
4. Day 10 (if no response): Final follow-up email with a different angle — share a relevant case study or data point

**Important:** This follow-up sequence is what turns direct mail from a standalone channel into a multi-touch play. The postcard creates physical awareness; the email/LinkedIn follow-up captures the response. Track which step in the sequence generates the response.

### 4. Scale to 100-200 postcards per month

Run the `postcard-campaign-send` drill at Baseline volume:

- Source 100-200 new prospects per month via Clay and push to Attio
- Verify all addresses before sending
- Send in weekly batches of 25-50 (not all at once) so follow-up workload is spread evenly
- Use a single postcard variant (the one that worked in Smoke) — do not A/B test yet, focus on proving the channel sustains

**Cost estimate:** 100-200 postcards x $0.77/piece = $77-$154/month on Lob's Developer plan. At $0.51/piece on the Small Business plan ($260/mo platform): $51-$102/mo + $260 platform = $311-$362/mo total.

### 5. Monitor and evaluate weekly

Each week, review in PostHog:
- Postcards sent vs. delivered (delivery rate should be ≥ 90%)
- Tracking URL visits this week
- Meetings booked attributed to postcards
- Which step in the follow-up sequence generated the most responses

At the end of 1 month, calculate:
- Overall response rate (all responses / postcards delivered)
- Cost per response
- Cost per meeting
- Pipeline value generated

**Pass threshold:** ≥ 5% response rate from 100-200 postcards over 1 month.

If PASS: The channel sustains at Baseline volume. Proceed to Scalable to introduce A/B testing and higher volume.
If FAIL: Diagnose by funnel stage — delivery issues (bad addresses), awareness issues (postcard not noticed), or conversion issues (postcard noticed but no action taken). Adjust and re-run.

## Time Estimate

- 3 hours: Event tracking and webhook setup (one-time)
- 3 hours: Follow-up automation workflow in n8n (one-time)
- 2 hours/week: List building, address verification, and sending (8 hours over 4 weeks)
- 30 minutes/week: Monitoring and evaluation (2 hours over 4 weeks)
- Total: ~15 hours over 1 month (6 hours one-time setup + 9 hours ongoing)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Lob | Print, mail, and track postcards | $0/mo + $0.77/pc (Developer) or $260/mo + $0.51/pc (Small Business). https://www.lob.com/pricing |
| Clay | Enrich prospects with mailing addresses | From $149/mo. https://www.clay.com/pricing |
| Attio | CRM — store contacts, send data, responses | Free for small teams. https://attio.com/pricing |
| PostHog | Event tracking and attribution analytics | Free up to 1M events/mo. https://posthog.com/pricing |
| n8n | Webhook processing, follow-up automation | Free (self-hosted) or from $24/mo (cloud). https://n8n.io/pricing |
| Instantly | Send follow-up emails triggered by delivery | From $30/mo. https://instantly.ai/pricing |

**Estimated total monthly cost:** $200-$500/mo depending on volume and plan tiers

## Drills Referenced

- `postcard-campaign-send` — Verify addresses, create templates, and send 100-200 postcards/month
- the postcard response tracking workflow (see instructions below) — Lob webhook integration, delivery tracking, response attribution
- `posthog-gtm-events` — Set up standardized direct mail event taxonomy in PostHog
- `follow-up-automation` — Digital follow-up sequence triggered by postcard delivery
