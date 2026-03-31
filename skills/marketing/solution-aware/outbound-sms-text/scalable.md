---
name: outbound-sms-text-scalable
description: >
  SMS Outbound Sequences — Scalable Automation. Scale SMS outreach to 800+
  messages per month with full automation: Twilio for sending, n8n for
  orchestration, Clay for continuous list building, and A/B testing on copy,
  timing, and segmentation. Maintain >=3% response rate at 4-8x volume.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Scalable Automation"
time: "60 hours over 3 months"
outcome: "≥3% response rate at 800+ SMS/month over 3 months"
kpis: ["Response rate", "Cost per reply", "Cost per meeting", "A/B test win rate", "Delivery rate"]
slug: "outbound-sms-text"
install: "npx gtm-skills add marketing/solution-aware/outbound-sms-text"
drills:
  - ab-test-orchestrator
  - follow-up-automation
  - tool-sync-workflow
---

# SMS Outbound Sequences — Scalable Automation

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

Scalable is the 10x multiplier. Move from 200 SMS over 2 weeks to 800+ per month without proportional founder effort. All sending, reply handling, and CRM logging are fully automated. A/B testing identifies winning copy, timing, and segmentation. The response rate holds within 80% of Baseline (>=3%) at 4-8x volume. Cost per meeting from SMS trends downward as winning variants compound.

## Leading Indicators

- Automated SMS sequences running daily in n8n without manual intervention for 2+ weeks
- Delivery rate sustained above 95% at higher volume
- A/B tests producing statistically significant winners within 2-week cycles
- Response rate per ICP segment identified (some segments outperform)
- Cost per reply declining month-over-month as winning variants compound
- Opt-out rate below 3% sustained at higher volume (validates messaging at scale)
- Pipeline value from SMS-sourced meetings growing month-over-month

## Instructions

### 1. Scale the prospect pipeline

Expand list building to produce 200 new SMS-ready prospects every 2 weeks using the `build-prospect-list` drill:

1. Source from Apollo with broader ICP filters (add secondary segments validated in Baseline)
2. Enrich in Clay with the phone waterfall: primary phone provider -> secondary provider -> Twilio Lookup for mobile verification
3. Score prospects: 80+ = Tier 1 (high personalization), 65-79 = Tier 2 (template with light customization), below 65 = exclude from SMS
4. Push to Attio with campaign tags and tier assignments
5. Set up Clay as a continuous pipeline: new prospects matching your ICP criteria auto-populate weekly, run through enrichment, and push to Attio when scoring threshold is met

Target: 200 fresh, mobile-verified prospects loaded into the SMS sequence every 2 weeks.

### 2. Deploy AI-generated copy at scale

Run the the sms copy generation workflow (see instructions below) drill at volume. For each new batch of 200 prospects:

1. Pull enrichment data and buying signals from Clay/Attio
2. Generate personalized 3-message sequences via Claude for each prospect
3. For Tier 1 (80+ score): full personalization — unique opener referencing their specific signal, tailored proof point from similar company
4. For Tier 2 (65-79 score): template-based with merge field personalization (first_name, company, industry pain point)
5. Validate all messages under 160 characters
6. Store in Attio with variant tracking for A/B analysis

### 3. Add phone number rotation

At 800+ messages per month, add 2-3 additional Twilio phone numbers to the Messaging Service:

1. Purchase 2 additional local numbers ($1.15/mo each) in different area codes
2. Add all numbers to your Twilio Messaging Service — Twilio automatically rotates across them
3. This distributes carrier load and reduces the risk of any single number being flagged
4. Monitor per-number delivery rates in PostHog. If one number drops below 90% delivery, remove it and provision a replacement.

### 4. Launch A/B testing

Run the `ab-test-orchestrator` drill. Set up parallel experiments on SMS-specific variables:

**Message copy experiments:**
- Opening line: signal-reference vs. pain-reference vs. social-proof
- CTA style: question ("Worth a chat?") vs. directive ("Reply YES") vs. booking link
- Message length: ultra-short (<100 chars) vs. full segment (~155 chars)
- Proof point: named customer vs. anonymous metric vs. industry stat

**Timing experiments:**
- Send time: 9am vs. 11am vs. 2pm (in prospect's timezone)
- Day of week: Monday vs. Tuesday vs. Thursday
- Sequence spacing: Day 1/3/6 vs. Day 1/2/4 vs. Day 1/4/7

**Segmentation experiments:**
- ICP segment A vs. segment B response rates
- Signal-triggered sends (within 48h of signal) vs. batch sends (weekly)

Use PostHog feature flags to randomly assign prospects to variants. Run each test for minimum 100 prospects per variant (3-4 weeks at scale). Declare winner at 90% statistical confidence. Implement winner as new default and start next test.

Maximum 1 active experiment at a time on SMS (carrier-level variables are hard to isolate if stacked).

### 5. Build cross-channel follow-up automation

Run the `follow-up-automation` drill to create n8n workflows connecting SMS to other outbound channels:

- **SMS reply positive + no meeting booked in 48h**: trigger a follow-up email from Instantly referencing the SMS conversation
- **SMS delivered but no reply after full sequence**: add prospect to a LinkedIn connection request queue (if LinkedIn URL available)
- **SMS opt-out**: suppress from all outbound channels (email, LinkedIn, calls) in Attio
- **Meeting booked via SMS**: cancel any pending email or LinkedIn sequences for this prospect, update Attio deal to "Meeting Booked"

Run the `tool-sync-workflow` drill to connect: Twilio delivery events -> PostHog, Twilio inbound replies -> n8n -> Attio deals, Attio contact updates -> suppress in other tools.

### 6. Implement intelligent send throttling

Build n8n logic to manage volume and deliverability:

1. **Daily volume cap**: maximum 50 SMS per number per day (150 total with 3 numbers)
2. **Hourly throttle**: maximum 20 per hour per number to avoid carrier burst filtering
3. **Weekend pause**: no sends Saturday/Sunday unless A/B test data shows weekend outperformance
4. **Deliverability circuit breaker**: if delivery rate drops below 90% in any 4-hour window, pause all sends and alert via Slack
5. **Opt-out rate breaker**: if opt-out rate exceeds 5% in any single day, pause and flag for copy review
6. **Queue management**: if daily cap is reached, overflow to next business day automatically

### 7. Monitor and evaluate over 3 months

Track weekly in PostHog (build a saved view):
- Total SMS sent and delivered
- Response rate by sequence step and variant
- Meetings booked from SMS
- Cost per reply = (Twilio spend + Anthropic spend) / positive replies
- Cost per meeting = total SMS play spend / meetings booked
- A/B test results and winning variants adopted
- Opt-out trend (flag if increasing)

**Pass threshold: >=3% response rate at 800+ SMS/month** sustained over 3 months.

- **PASS**: Document the optimized send infrastructure, winning copy variants, best timing, and highest-performing ICP segments. Record cost per meeting. Proceed to Durable.
- **FAIL**: Identify bottleneck. If response rate dropped with scale: list quality is likely the issue (enrich more aggressively, tighten ICP). If delivery rate dropped: carrier filtering (review A2P registration, message content). If opt-outs spiked: message fatigue (rotate copy more frequently). Fix and re-run.

## Time Estimate

- Continuous list building setup in Clay: 4 hours
- AI copy generation pipeline: 4 hours
- Phone number rotation and Messaging Service config: 2 hours
- A/B test design and implementation: 8 hours
- Cross-channel follow-up automation: 6 hours
- Intelligent throttling and circuit breakers: 4 hours
- Ongoing list building (bi-weekly): 6 hours
- Monitoring and A/B analysis (weekly): 12 hours
- Founder reply handling for QUESTION/POSITIVE: 8 hours
- Monthly strategic review: 6 hours

Total: ~60 hours over 3 months.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Twilio | SMS sending at scale (800+/mo) | ~$0.011-0.013/msg; 3 numbers ~$3.45/mo; ~$10-12/mo at 800 msgs (https://www.twilio.com/en-us/sms/pricing/us) |
| Clay | Continuous enrichment + phone verification | Team: $349/mo at this volume (https://www.clay.com/pricing) |
| Apollo | Contact sourcing at volume | Professional: $99/mo (https://www.apollo.io/pricing) |
| Attio | CRM + deal tracking + suppression | Plus: $29/user/mo (https://attio.com/pricing) |
| n8n | Orchestration, throttling, reply routing | Starter: $20/mo (https://n8n.io/pricing) |
| PostHog | Event tracking + experiments + funnels | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Anthropic API | Copy generation + reply classification | ~$20-40/mo at this volume (https://www.anthropic.com/pricing) |
| Cal.com | Meeting booking | Free tier (https://cal.com/pricing) |

**Estimated play-specific cost: ~$60-100/mo** (Twilio ~$12 + Anthropic ~$30 + n8n $20; Clay and Apollo costs shared across plays)

## Drills Referenced

- the sms outreach sequence workflow (see instructions below) — automated 3-step SMS sequence with volume throttling and reply handling
- the sms copy generation workflow (see instructions below) — AI-generated personalized copy at scale with variant tracking
- `ab-test-orchestrator` — run A/B tests on copy, timing, and segmentation with statistical rigor
- `follow-up-automation` — cross-channel follow-ups connecting SMS to email and LinkedIn
- `tool-sync-workflow` — connect Twilio, Attio, PostHog, and n8n into a unified data flow
