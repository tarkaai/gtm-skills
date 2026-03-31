---
name: outbound-sms-text-smoke
description: >
  SMS Outbound Sequences — Smoke Test. Manually send 50 personalized SMS messages
  from the founder's phone to solution-aware B2B prospects to validate whether SMS
  produces responses and meetings within 1 week. No automation, no always-on.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥3% response rate from 50 SMS messages in 1 week"
kpis: ["Response rate", "Time to first reply", "Positive reply ratio"]
slug: "outbound-sms-text"
install: "npx gtm-skills add marketing/solution-aware/outbound-sms-text"
drills:
  - icp-definition
  - build-prospect-list
  - threshold-engine
---

# SMS Outbound Sequences — Smoke Test

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

The Smoke Test proves that SMS can reach solution-aware B2B prospects and generate responses. Success means at least 2 positive replies (response rate >=3%) from 50 manually sent SMS messages within 1 week. No automation, no SMS platform spend — the founder sends texts from a business phone number to validate the channel before investing in tooling.

## Leading Indicators

- First reply received within 24 hours of sending batch 1
- At least 1 reply per batch of 10 sends
- Positive-to-negative reply ratio above 2:1
- At least 1 prospect asks a follow-up question or agrees to a call
- Delivery confirmations on >90% of messages sent

## Instructions

### 1. Define your ICP for SMS outreach

Run the `icp-definition` drill. Document firmographic criteria (company size, industry, funding stage), buyer persona (title, seniority), top 3 pain points, and 3 triggering events. SMS works best for personas who are mobile-first: founders, sales leaders, field operators, and executives who check texts faster than email. Add a filter: prioritize prospects whose role suggests they are away from a desktop most of the day.

Output: ICP document with SMS-specific persona notes saved to your project's `docs/` directory.

### 2. Build a prospect list of 50 contacts with verified mobile numbers

Run the `build-prospect-list` drill. Source contacts from Apollo matching your ICP. Import into Clay, run the enrichment waterfall to fill mobile phone numbers. Use Clay's phone type enrichment or Twilio Lookup to verify each number is a mobile number (not a landline — landlines cannot receive SMS).

Filter to 50 contacts with:
- Verified mobile phone number
- Enriched first name, company name, title
- At least one buying signal (job change, funding, hiring)

Push to Attio with tags `play:outbound-sms-text` and `level:smoke`.

### 3. Write SMS copy manually

Write 3 message variants targeting different pain points from your ICP. Each message must be:

- Under 160 characters (one SMS segment)
- Conversational in tone — written like a human text, not a marketing blast
- Includes the prospect's first name and company
- References something specific (their signal, their industry challenge)
- Ends with a soft question as CTA
- First message to each contact includes "Reply STOP to opt out"

Example structure:
```
Hi [Name], [Founder] here from [Company]. Saw [Company] is [signal]. We help teams [value prop]. Worth a quick chat? Reply STOP to opt out.
```

Write 3 variants:
- Variant A: Signal-based (references their specific buying signal)
- Variant B: Pain-based (references an industry-common pain point)
- Variant C: Social-proof (leads with a customer result)

### 4. Send 50 messages manually over 5 days

**Human action required:** Send all messages from a business phone number (Google Voice, OpenPhone/Quo free trial, or your personal phone with a business line). Send 10 messages per day, Monday through Friday, between 9am-11am in the prospect's timezone.

Assign variants evenly: ~17 prospects get Variant A, ~17 get Variant B, ~16 get Variant C.

For each send, log in Attio immediately:
- Contact record: `sms_sent=true`, `sms_sent_date`, `sms_variant` (A/B/C)
- Note: full message text sent

**Compliance:** Do NOT send before 8am or after 9pm in the prospect's timezone. Include opt-out language. If anyone replies STOP, do not send again — mark as `sms_opted_out=true` in Attio.

### 5. Handle replies manually

When a reply comes in, classify it yourself:
- **Positive** (interested, asks question, agrees to call): Reply within 30 minutes. Send Cal.com booking link. Create Attio deal at "Interested" stage.
- **Negative** (not interested, wrong person): Reply politely. Mark contact as `sms_not_interested=true`. Do not re-contact.
- **Opt-out** (STOP, unsubscribe): Do not reply. Mark as `sms_opted_out=true`.
- **Question** (wants more info): Reply with a brief answer and soft CTA for a 10-minute call.

Log every reply in Attio with: reply text, sentiment classification, time-to-reply in hours.

### 6. Evaluate against threshold

Run the `threshold-engine` drill. Pull logged data from Attio. Calculate:
- Total messages sent (target: 50)
- Total replies received
- Response rate = replies / messages sent
- Positive reply count
- Opt-out count
- Time to first reply (hours)
- Best-performing variant (A/B/C) by reply rate

**Pass threshold: >=3% response rate** (at least 2 replies from 50 messages).

- **PASS**: Document which variant performed best, which ICP segment responded, and average time-to-reply. Proceed to Baseline.
- **FAIL**: Diagnose — was it phone number quality (high failure rate), message copy (no interest), targeting (wrong ICP for SMS), or timing (sent at wrong hours)? Adjust and re-run Smoke.

## Time Estimate

- ICP definition and list building: 1.5 hours
- Phone number verification and Clay enrichment: 1 hour
- SMS copy writing (3 variants): 30 minutes
- Manual sending (10/day for 5 days): 1.5 hours total (15-20 min/day)
- Reply handling and logging: 1 hour
- Evaluation: 30 minutes

Total: ~6 hours of active work spread over 1 week.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Prospect enrichment and phone verification | Free tier: 100 credits/mo; Pro: $149/mo (https://www.clay.com/pricing) |
| Apollo | Contact sourcing with phone numbers | Free tier: 50 contacts/mo; Basic: $49/mo (https://www.apollo.io/pricing) |
| Attio | CRM for logging all SMS activity | Free tier: 3 users; Plus: $29/user/mo (https://attio.com/pricing) |
| OpenPhone (Quo) | Business phone number for sending | Starter: $15/user/mo, includes SMS (https://www.quo.com/blog/quo-pricing/) |
| Cal.com | Booking link in reply messages | Free tier available (https://cal.com/pricing) |

**Estimated play-specific cost: $0-15** (free tiers sufficient for Smoke; OpenPhone Starter if you need a business number)

## Drills Referenced

- `icp-definition` — define ideal customer profile with SMS-specific persona filters
- `build-prospect-list` — source, enrich, and verify mobile phone numbers for 50 contacts
- `threshold-engine` — evaluate pass/fail against >=3% response rate threshold
