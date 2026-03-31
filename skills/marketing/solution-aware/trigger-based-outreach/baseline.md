---
name: trigger-based-outreach-baseline
description: >
  Trigger-based Outreach — Baseline Run. First always-on automation: Clay monitors
  buying signals daily, enriches and scores triggered prospects, routes them into
  Instantly campaigns with signal-specific sequences, and tracks the full
  signal-to-meeting funnel in PostHog. Validates that Smoke results hold at 150+
  contacts over 2 weeks with automated signal detection.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Email, Social"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥ 4% meeting rate from 150 trigger-based contacts over 2 weeks"
kpis: ["Meeting rate (target ≥ 4%)", "Signal-to-outreach latency (target < 4 hours for high-priority signals)", "Positive reply rate (target ≥ 8%)", "Bounce rate (target < 3%)"]
slug: "trigger-based-outreach"
install: "npx gtm-skills add marketing/solution-aware/trigger-based-outreach"
drills:
  - signal-detection
  - enrich-and-score
  - cold-email-sequence
  - posthog-gtm-events
---

# Trigger-based Outreach — Baseline Run

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Email, Social

## Outcomes

Move from manual signal scanning (Smoke) to automated signal detection and outreach at 150+ contacts. Clay runs daily signal scans, enriches triggered prospects, and pushes them into signal-specific Instantly campaigns. The core hypothesis shifts from "does trigger timing work?" (proven in Smoke) to "does automated signal detection produce the same quality at 5x volume?" The signal-to-outreach latency must stay under 4 hours for high-priority signals — stale triggers lose their edge.

Pass: 4% or higher meeting rate (meetings / trigger-based contacts emailed) over 2 weeks from at least 150 contacts.
Fail: Below 4% meeting rate after 2 full weeks with 150+ contacts.

## Leading Indicators

- Bounce rate stays below 3% (confirms Clay enrichment and email verification are working)
- Signal-to-outreach latency under 4 hours for funding and new-hire signals (confirms automation speed)
- Positive reply rate ≥ 8% in the first 50 sends (confirms Smoke messaging quality holds with automated personalization)
- First meeting books within 3 days of campaign launch
- Signal-triggered contacts reply faster than the founder's prior cold outreach (validates the timing advantage)

## Instructions

### 1. Set up sending infrastructure

Use the `instantly-account-setup` fundamental to create dedicated sending domains. Do NOT send Baseline volume from the founder's primary inbox.

- Purchase 2 secondary domains similar to the primary domain (e.g., getacme.com, acmehq.com). Cost: ~$10-15/domain/year.
- Create 2 Google Workspace accounts on each domain using the founder's first name.
- Configure SPF, DKIM, DMARC for each domain.
- Connect all 4 accounts to Instantly.

Use the `instantly-warmup` fundamental to start warmup immediately. Accounts need 14 days of warmup before sending. Start this on Day 1 while you build the signal automation.

### 2. Configure automated signal detection in Clay

Run the `signal-detection` drill to set up automated monitoring. Create Clay tables for each validated signal type from Smoke:

**Table 1 — Funding Signals:**
- Source: Crunchbase enrichment via Clay
- Filter: Companies matching ICP that raised Series A-C in the last 30 days
- Enrichment: company name, funding amount, date, CEO/founder name, employee count
- Schedule: daily refresh
- Use `clay-company-search` fundamental to configure the initial search criteria
- Use `clay-enrichment-waterfall` fundamental to chain Crunchbase data with firmographic enrichment

**Table 2 — Job Change Signals:**
- Source: People Data Labs or LinkedIn via Clay
- Filter: People matching buyer persona titles who changed companies in the last 60 days, where the new company matches your ICP
- Enrichment: person name, new title, new company, previous company, email
- Schedule: daily refresh
- Use `clay-people-search` fundamental to configure person-level searches

**Table 3 — Hiring Spree Signals:**
- Source: Job board scrapers via Clay
- Filter: Companies matching ICP that posted 3+ roles in your product's domain in the last 14 days
- Enrichment: company name, open roles, department, hiring manager name and email
- Schedule: every 3 days

**Table 4 — Competitor Churn Signals (if validated in Smoke):**
- Source: G2 review monitoring, Reddit/Twitter keyword monitoring via Clay's Claygent
- Filter: Negative reviews or complaints about competitors your ICP uses
- Enrichment: reviewer/poster identity (if public), company, role
- Schedule: daily

For each table, run the `enrich-and-score` drill to:
- Verify email addresses (target 85%+ valid rate)
- Score each prospect using ICP fit + signal strength (recency + signal type priority from Smoke data)
- Tag with signal type and signal detail for downstream personalization

### 3. Build signal-specific email sequences in Instantly

Run the `cold-email-sequence` drill to create separate Instantly campaigns per signal type. Use the templates that worked in Smoke, adapted for merge-field personalization:

**Funding signal campaign (3-step):**
- Email 1: "{{firstName}}, congrats on the {{fundingRound}} — {{personalization_line}}" (under 80 words)
- Email 2 (Day 3): Proof point from a similar post-funding customer (under 70 words)
- Email 3 (Day 7): Direct ask with Cal.com link (under 60 words)

**Job-change signal campaign (3-step):**
- Email 1: "{{firstName}}, congrats on the move to {{companyName}} — {{personalization_line}}" (under 80 words)
- Email 2 (Day 4): Resource relevant to the first 90 days in their role (under 70 words)
- Email 3 (Day 8): Direct ask (under 60 words)

**Hiring-spree signal campaign (2-step — shorter because hiring sprees are time-sensitive):**
- Email 1: "{{firstName}}, noticed {{companyName}} is scaling the {{department}} team — {{personalization_line}}" (under 80 words)
- Email 2 (Day 3): Direct ask with Cal.com link (under 60 words)

**Competitor-churn signal campaign (2-step):**
- Email 1: "{{firstName}}, heard you're evaluating options for {{category}} — {{personalization_line}}" (under 80 words)
- Email 2 (Day 4): Comparison resource or specific migration story (under 70 words)

Configure each campaign:
- Sending schedule: weekdays, 7:30am-9:30am in the prospect's timezone
- Daily limit: 15 sends/day per account (60 total across 4 accounts)
- Disable open tracking (reduces spam risk)
- Use `clay-claygent` fundamental to generate the `{{personalization_line}}` for each prospect referencing their specific signal detail

### 4. Configure event tracking in PostHog

Run the `posthog-gtm-events` drill to set up a signal-to-meeting funnel. Configure these events via Instantly webhooks routed through n8n:

- `trigger_signal_detected` with properties: `{signal_type, signal_freshness_days, company, source: "trigger-based-outreach", level: "baseline"}`
- `trigger_outreach_sent` with properties: `{signal_type, step: 1|2|3, campaign_id, signal_to_send_hours, source: "trigger-based-outreach"}`
- `trigger_reply_received` with properties: `{signal_type, sentiment: "positive|negative|neutral", source: "trigger-based-outreach"}`
- `trigger_meeting_booked` with properties: `{signal_type, days_from_signal, days_from_first_email, source: "trigger-based-outreach"}`

Create a PostHog funnel: `trigger_signal_detected` -> `trigger_outreach_sent` -> `trigger_reply_received (positive)` -> `trigger_meeting_booked`. Break down by `signal_type` to compare which signals convert best.

### 5. Launch and manage the pipeline

Activate all Clay tables and Instantly campaigns once warmup completes (~Day 14). For the first 3 days, monitor closely:

- Check that Clay signals are flowing: at least 5 new triggered prospects per day across all tables. If fewer, widen the ICP filters or add signal sources.
- Check signal-to-outreach latency: from the time Clay detects a signal to the time Instantly sends Email 1. Target: under 4 hours for funding and job-change signals.
- Spot-check 10 rendered emails in Instantly to verify personalization lines reference the actual signal.
- Verify bounce rate stays below 3%.

After the 3-day verification window, let the system run.

**Human action required:** The founder monitors Instantly's Unibox and responds to positive replies within 1 hour. At 150 contacts over 2 weeks, expect 12-20 replies. The founder's fast, personal response is still critical at Baseline volume.

For each positive reply: respond with meeting times or Cal.com link. Create a deal in Attio at "Meeting Booked" stage with signal type noted.
For each "not now" reply: acknowledge, set 45-day follow-up in Attio.
For each unsubscribe: remove from all campaigns immediately.

### 6. Evaluate results after 2 weeks

Pull PostHog funnel data. Compute per signal type and overall:
- Meeting rate = meetings booked / contacts emailed
- Positive reply rate = positive replies / contacts emailed
- Signal-to-outreach latency (median hours)
- Signal-to-meeting conversion by signal type
- Bounce rate
- Which signal types produced the highest meeting rate

- **PASS (≥ 4% meeting rate overall):** Baseline is proven. Document: top-performing signal types (rank by meeting rate), optimal signal freshness windows per type, best-performing email templates, and signal-to-outreach latency achieved. Proceed to Scalable.
- **MARGINAL (2-3.9% meeting rate):** Automated detection may be introducing noise. Diagnose: Is one signal type dragging down the average? Is the automated personalization as good as the manual Smoke personalization? Is signal freshness adequate (are some signals too old by the time outreach happens)? Fix the weakest signal type (improve or remove it) and re-run with 100 fresh contacts.
- **FAIL (< 2% meeting rate):** The automation layer is losing the quality that made Smoke work. Likely causes: signal detection is too broad (catching noise, not real buying intent), personalization is too generic (Clay merge fields are shallow vs. Smoke's hand-crafted references), or signal-to-outreach latency is too high (signals are stale by the time email sends). Fix the root cause or accept that this play works best at Smoke scale with manual signal scanning.

## Time Estimate

- Sending infrastructure setup + warmup initiation: 2 hours (Day 1)
- Clay signal detection tables (4 signal types): 4 hours (Days 1-3)
- Enrichment and scoring configuration: 2 hours (Days 3-4)
- Signal-specific email sequences in Instantly (4 campaigns): 3 hours (Days 4-5)
- PostHog event tracking setup: 2 hours (Day 5)
- Campaign launch verification: 1 hour (Day 14)
- Reply management over 2 weeks: 2 hours total
- Results evaluation: 2 hours
- Total: ~18 hours over 2 weeks (warmup runs in background for first 14 days)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Email sequencing, warmup, sending, reply detection | Growth plan $37/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Clay | Signal detection, enrichment, email verification, personalization | Launch plan $185/mo ([clay.com/pricing](https://clay.com/pricing)) |
| Attio | CRM, deal tracking, signal source attribution | Free for up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Signal-to-meeting funnel tracking, event analytics | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Webhook routing from Instantly to PostHog | Starter $24/mo or self-host free ([n8n.io/pricing](https://n8n.io/pricing)) |
| Cal.com | Meeting booking link | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Secondary domains (x2) | Sending infrastructure | ~$25/year total |
| Google Workspace (x2) | Sending accounts | ~$14/mo total ($7/user/mo) |

**Estimated monthly cost for Baseline:** ~$260/mo + $25/year for domains

## Drills Referenced

- `signal-detection` — automated Clay tables monitoring funding, job changes, hiring sprees, and competitor churn
- `enrich-and-score` — email verification, firmographic enrichment, signal strength scoring
- `cold-email-sequence` — signal-specific multi-step campaigns in Instantly with personalized merge fields
- `posthog-gtm-events` — signal-to-meeting funnel tracking with signal-type breakdown
