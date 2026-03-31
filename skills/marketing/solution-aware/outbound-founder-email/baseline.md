---
name: outbound-founder-email-baseline
description: >
  Outbound founder-led email — Baseline Run. First always-on automation: the founder's
  email sequence runs through Instantly to 100+ solution-aware prospects with Clay
  enrichment, reply routing to Attio, and PostHog tracking. Validates that the Smoke
  results hold at 100-contact scale over 2 weeks.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Email"
level: "Baseline Run"
time: "14 hours over 2 weeks"
outcome: "≥ 2% meeting rate (meetings booked / contacts emailed) over 2 weeks from 100+ contacts"
kpis: ["Meeting rate (target ≥ 2%)", "Positive reply rate (target ≥ 5%)", "Bounce rate (target < 3%)", "Time from first email to meeting booked"]
slug: "outbound-founder-email"
install: "npx gtm-skills add marketing/solution-aware/outbound-founder-email"
drills:
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - posthog-gtm-events
---

# Outbound Founder-Led Email — Baseline Run

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Email

## Outcomes

Move from manual sending to automated delivery at 100+ contacts while maintaining or improving the reply and meeting rates proven in Smoke. The founder's voice and solution-aware positioning remain the same — what changes is that Instantly handles the sending, Clay handles enrichment, and PostHog tracks the funnel.

Pass: 2% or higher meeting rate (meetings / contacts emailed) over 2 weeks from at least 100 contacts.
Fail: Below 2% meeting rate after 2 full weeks with 100+ contacts.

## Leading Indicators

- Bounce rate stays below 3% (confirms Clay email verification is working)
- Positive reply rate ≥ 5% in the first 50 sends (confirms Smoke messaging holds at scale)
- First meeting books within 5 days of campaign launch
- No spam complaints or deliverability warnings from Instantly

## Instructions

### 1. Set up sending infrastructure

The founder needs dedicated sending domains — do NOT send Baseline volume from their primary inbox (that risks deliverability for all their regular email).

Use the `instantly-account-setup` fundamental to:
- Purchase 2 secondary domains similar to the primary domain (e.g., if primary is acme.com, buy getacme.com and acmehq.com). Cost: ~$10-15/domain/year.
- Create 2 Google Workspace accounts on each domain using the founder's first name (e.g., dan@getacme.com, dan@acmehq.com).
- Configure SPF, DKIM, DMARC for each domain.
- Connect all accounts to Instantly.

Use the `instantly-warmup` fundamental to start warmup on all accounts immediately. Accounts need 14 days of warmup before sending. Start this step on Day 1 while you build the list.

### 2. Build and enrich a 150-contact prospect list

Run the `build-prospect-list` drill to source 150 contacts matching your Smoke-validated ICP from Apollo and Clay. Over-build by 50% because enrichment and verification will filter some out.

Run the `enrich-and-score` drill to:
- Verify email addresses (target 80%+ valid rate)
- Enrich with company data, role, tech stack
- Score and filter to keep only prospects scoring ≥ 70
- Add a `likely_alternative` column: use Clay's AI (via `clay-claygent` fundamental) to infer which alternative each prospect probably uses based on their tech stack, company size, and industry

Target: 100+ verified, scored, enriched contacts with personalization data ready for Instantly.

### 3. Write and load the email sequence

Run the the founder cold email copy workflow (see instructions below) drill to produce the 3-step sequence. Use the same competitive positioning that worked in Smoke, but update the proof points if you booked meetings in Smoke — those meetings may have given you sharper customer stories.

Using the `cold-email-sequence` drill, load the sequence into Instantly:
- Map Clay personalization variables to Instantly merge fields: `{{firstName}}`, `{{companyName}}`, `{{personalization_line}}`, `{{likely_alternative}}`, `{{similar_customer}}`, `{{proof_metric}}`
- Set sending schedule: weekdays, 7:30am-9:30am in the prospect's timezone
- Set daily limit: 20 sends/day per account (80 total/day across 4 accounts)
- Disable open tracking
- Set step delays: Email 2 at Day 3, Email 3 at Day 7
- Include the founder's Cal.com booking link in Email 3 only

### 4. Configure tracking in PostHog

Run the `posthog-gtm-events` drill to set up event tracking for this play. Configure these specific events via Instantly webhooks routed through n8n:

- `email_sent` with properties: `{source: "outbound-founder-email", level: "baseline", step: 1|2|3, campaign_id}`
- `email_replied` with properties: `{source: "outbound-founder-email", sentiment: "positive|negative|neutral", level: "baseline"}`
- `meeting_booked` with properties: `{source: "outbound-founder-email", level: "baseline", days_from_first_email}`

Create a PostHog funnel: `email_sent` -> `email_replied (positive)` -> `meeting_booked`. This is your core conversion funnel for this play.

### 5. Launch and manage replies

Activate the campaign in Instantly. Send to the first 30 contacts on Day 1 as a test batch. After 24 hours, check:
- Deliverability: bounce rate < 3%? If higher, check DNS configuration and email verification quality.
- Personalization: pull 5 rendered emails from Instantly and verify merge fields populated correctly.
- Schedule: are emails arriving in the morning window?

If the test batch is clean, activate the remaining contacts.

**Human action required:** The founder must monitor Instantly's Unibox and respond to positive replies within 1 hour. At Baseline volume (100 contacts), expect 5-10 replies total over 2 weeks. This is not yet high enough volume to justify automation — the founder's personal, fast replies are part of what makes this work.

For each positive reply: respond with meeting times or Cal.com link, create a deal in Attio at "Meeting Booked" stage.
For each "not now" reply: respond acknowledging timing, set a follow-up reminder in Attio for 60 days out.
For each unsubscribe: remove from all Instantly campaigns immediately.

### 6. Evaluate results after 2 weeks

Pull the PostHog funnel data. Compute:
- Meeting rate = meetings booked / total unique contacts emailed
- Positive reply rate = positive replies / total unique contacts emailed
- Bounce rate = bounced / total sent
- Average time from first email to meeting booked

- **PASS (≥ 2% meeting rate):** Baseline is proven. Document: which ICP segments produced the most meetings, which email step produced the most positive replies, which proof points resonated. Proceed to Scalable.
- **MARGINAL (1-1.9% meeting rate):** Close but not there. Diagnose: Is the list quality issue (low scores producing meetings at lower rate)? Is it a messaging issue (low reply rate overall)? Is it a conversion issue (replies but no meetings)? Fix the weakest link and re-run Baseline with 100 fresh contacts.
- **FAIL (< 1% meeting rate):** The Smoke result did not hold at scale. Possible causes: Smoke list was cherry-picked (higher quality than a systematic list), messaging feels less personal at scale (personalization variables are too generic), or the ICP is too broad. Re-tighten ICP, improve Clay personalization quality, and re-run.

## Time Estimate

- Sending infrastructure setup + warmup initiation: 2 hours (Day 1)
- List building, enrichment, scoring: 3 hours (Days 1-3)
- Email copywriting and Instantly setup: 2 hours (Days 3-4)
- PostHog event configuration: 2 hours (Day 4)
- Campaign launch and test batch review: 1 hour (Day 14, after warmup)
- Reply management over 2 weeks: 2 hours total
- Results evaluation: 2 hours
- Total: ~14 hours over 2 weeks (first 2 weeks are warmup; active campaign runs weeks 3-4)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Email sequencing, warmup, sending | Growth plan $37/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Clay | Enrichment, personalization, email verification | Launch plan $185/mo ([clay.com/pricing](https://clay.com/pricing)) |
| Attio | CRM, deal tracking, contact management | Free for up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Event tracking, funnel analysis | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Cal.com | Meeting booking link | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Secondary domains (x2) | Sending infrastructure | ~$25/year total |
| Google Workspace (x2) | Sending accounts | ~$14/mo total ($7/user/mo) |

**Estimated monthly cost for Baseline:** ~$236/mo + $25/year for domains

## Drills Referenced

- `build-prospect-list` — source 150 contacts from Apollo/Clay matching the validated ICP
- `enrich-and-score` — verify emails, enrich firmographics, score against ICP, add personalization data
- the founder cold email copy workflow (see instructions below) — write the 3-step founder email sequence with solution-aware positioning
- `cold-email-sequence` — load the sequence into Instantly with proper configuration
- `posthog-gtm-events` — set up event tracking to measure the email-to-meeting funnel
