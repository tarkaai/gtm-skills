---
name: intent-signal-tracking-baseline
description: >
  Intent Signal Tracking — Baseline Run. Deploy always-on signal collection from website visitors
  and third-party intent sources. Automate scoring and routing to CRM. Run continuous intent-based
  outreach sequences and prove the pipeline sustains over 2 weeks.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=20 high-intent accounts identified and >=35% reply rate from intent-based outreach over 2 weeks"
kpis: ["High-intent accounts per week", "Reply rate by intent tier", "Signal-to-outreach time (median)", "Meeting rate from intent outreach"]
slug: "intent-signal-tracking"
install: "npx gtm-skills add sales/qualified/intent-signal-tracking"
drills:
  - cold-email-sequence
  - posthog-gtm-events
---

# Intent Signal Tracking — Baseline Run

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Outcomes

Transition from manual signal checking to always-on automated signal collection and scoring. Deploy a website visitor identification tool, automate signal routing to your CRM, and run continuous intent-based email sequences. Prove the pipeline sustains >=20 high-intent accounts and >=35% reply rate over 2 weeks.

## Leading Indicators

- Website visitor identification tool is firing and sending data to n8n within the first 2 days
- Signals are flowing into Clay and scores are being calculated automatically
- Hot-tier accounts are appearing in Attio within 30 minutes of signal detection
- Cold email sequences are sending on schedule with no deliverability issues
- Reply rate on intent-based sequences is above 25% after the first week

## Instructions

### 1. Install website visitor identification

Choose and install a visitor identification tool. For Baseline, start with a free or low-cost option:

- **RB2B** (recommended for Baseline): Free tier gives 150 identifications/month. Install the pixel on your website. Configure the webhook to send identified visitors to your n8n instance.
- **Koala** (alternative): Free tier gives 250 identifications/month with product usage integration.

Run the the intent signal automation workflow (see instructions below) drill, specifically Step 1 (website visitor signal workflow). Configure the n8n webhook to receive visitor data, filter for high-signal pages (pricing, demo, case studies, docs), and push to Clay for scoring.

### 2. Automate signal scoring

Set up the Clay intent scoring table from the `intent-score-model` drill (which you validated manually during Smoke). Import your proven weights and thresholds. Connect the n8n webhook output to Clay so every identified visitor is automatically scored.

Run the the intent signal automation workflow (see instructions below) drill, Step 3 (enrichment signal workflow) to set up weekly refresh of contextual signals (funding, hiring, tech stack changes).

If you have a G2 paid profile, also configure the G2 intent webhook (Step 2 of the intent signal automation workflow (see instructions below)).

### 3. Configure outreach sequences

Run the `cold-email-sequence` drill to set up Instantly with:
- A **Hot-tier sequence**: 3 emails over 7 days. First email uses the signal-specific copy you validated in Smoke. More aggressive cadence (Day 0, Day 2, Day 5).
- A **Warm-tier sequence**: 4 emails over 14 days. Less personalized but still references intent category. Slower cadence (Day 0, Day 4, Day 8, Day 12).

Import your Smoke-validated email copy as the starting templates. Set up Instantly reply detection to classify responses and route positive replies to Attio.

### 4. Set up measurement

Run the `posthog-gtm-events` drill to configure tracking for intent-specific events:
- `intent_signal_received` (properties: source, signal_type, company_domain, intent_score)
- `intent_outreach_triggered` (properties: tier, channel, company_domain, personalization_type)
- `intent_email_replied` (properties: sentiment, tier, company_domain)
- `intent_meeting_booked` (properties: source_signal, tier, company_domain)

Build a PostHog funnel: `intent_signal_received` -> `intent_outreach_triggered` -> `intent_email_replied` -> `intent_meeting_booked`

### 5. Run for 2 weeks and monitor daily

Each morning, check:
- How many new signals arrived in the last 24 hours?
- How many Hot-tier accounts were identified?
- Were all Hot-tier accounts contacted within 4 hours?
- What is the cumulative reply rate by tier?
- Are there any n8n workflow errors?

Adjust mid-flight: if reply rates are below 20% after 50 sends, revisit your email copy. If signal volume is too low (fewer than 3 Hot accounts per week), lower scoring thresholds by 10 points temporarily.

### 6. Evaluate against threshold

After 2 weeks, measure:
- Total high-intent accounts identified: target >=20
- Reply rate on intent-based outreach: target >=35%
- Comparison: intent reply rate vs cold outreach reply rate from Smoke (should be consistently 2x+)
- Median signal-to-outreach time: target under 4 hours

If PASS, proceed to Scalable. If FAIL, diagnose: is signal volume the issue (need more traffic or additional signal sources)? Is scoring the issue (wrong weights)? Is messaging the issue (low reply rate despite good targeting)?

## Time Estimate

- 4 hours: install visitor ID tool, configure n8n webhooks, set up Clay scoring table
- 3 hours: build Instantly sequences, configure reply routing
- 2 hours: set up PostHog events and funnels
- 6 hours: daily monitoring over 2 weeks (30 min/day)
- 3 hours: analysis, evaluation, and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| RB2B | Website visitor identification | Free (150/mo) or Pro+ $149/mo |
| Clay | Intent signal scoring and enrichment | Explorer $149/mo (~2,400 credits) |
| Instantly | Cold email sequencing | Growth $30/mo (1,000 contacts) |
| PostHog | Event tracking and funnels | Free tier (1M events/mo) |
| Attio | CRM for account and deal tracking | Free tier (3 users) |
| n8n | Workflow automation | Free (self-hosted) or Starter $24/mo |

**Total play-specific cost: ~$50-200/mo** (depending on tool tiers selected)

## Drills Referenced

- the intent signal automation workflow (see instructions below) — automate signal collection, scoring, and CRM routing via n8n
- `cold-email-sequence` — build and launch intent-triggered email sequences in Instantly
- `posthog-gtm-events` — configure intent-specific event tracking for measurement
