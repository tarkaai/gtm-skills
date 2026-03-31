---
name: outbound-email-li-calls-scalable
description: >
  Outbound Email/LI/Calls — Scalable Automation. Scale multi-channel outbound
  to 500-1000 contacts/month with full automation: Instantly for email, Dripify/Expandi
  for LinkedIn, cloud dialer for calls, n8n for cross-channel orchestration.
  A/B test everything. Maintain ≥ 1.6% meeting rate at 5-10x volume.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "Meeting rate ≥ 1.6% over 2 months at 500-1000 contacts/month"
kpis: ["Meeting rate", "Cost per meeting", "Channel conversion by tier"]
slug: "outbound-email-li-calls"
install: "npx gtm-skills add marketing/solution-aware/outbound-email-li-calls"
drills:
  - multi-channel-cadence
  - follow-up-automation
  - tool-sync-workflow
  - ab-test-orchestrator
---

# Outbound Email/LI/Calls — Scalable Automation

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Outcomes

Scalable is the 10x multiplier. Move from 200 contacts in 2 weeks to 500-1000 contacts per month without proportional effort. All three channels (email, LinkedIn, calls) run as coordinated automations. n8n orchestrates cross-channel timing. A/B testing identifies winning variants. The meeting rate holds within 20% of Baseline (≥ 1.6%) at 5-10x volume.

## Leading Indicators

- Automated email sequences running in Instantly with no manual intervention
- LinkedIn automation tool sending connection requests and follow-ups on schedule
- Cloud dialer call blocks populating from automated priority queues
- Cross-channel suppression working (no double-touching on the same day)
- A/B tests producing statistically significant winners within 2-week cycles
- Cost per meeting declining month-over-month as winning variants compound
- Pipeline value from outbound growing month-over-month

## Instructions

### 1. Build the coordinated multi-channel cadence

Run the `multi-channel-cadence` drill to design and implement a 14-day synchronized outreach sequence across all three channels:

**Day 1**: LinkedIn profile visit (via Dripify/Expandi — use `linkedin-automation-sequence` fundamental)
**Day 2**: Email 1 — problem-aware opener via Instantly
**Day 3**: LinkedIn connection request with personalized note
**Day 5**: Email 2 — proof point / value angle
**Day 6**: LinkedIn content engagement (like/comment if connected)
**Day 7**: Phone call attempt 1 (prioritize: email openers who did not reply + new LinkedIn connections)
**Day 8**: LinkedIn message 1 (if connected and no email reply)
**Day 10**: Email 3 — soft CTA with Cal.com link
**Day 12**: Phone call attempt 2 (prioritize: email openers 3+ times, LinkedIn message readers)
**Day 14**: Breakup email + final LinkedIn message (if connected)

Build this as an n8n master workflow using the `n8n-workflow-basics` fundamental. The workflow:
- Triggers each channel step on schedule per prospect
- Checks Attio for status before each step (do NOT call someone who already replied)
- Pauses all channels instantly when a prospect engages positively on any channel
- Routes positive responses to Attio pipeline at "Meeting Requested" stage

### 2. Set up LinkedIn automation at scale

Using the `linkedin-automation-sequence` fundamental, configure Dripify or Expandi:

1. Create a campaign with the LinkedIn steps from the cadence above
2. Import prospects from Clay with personalization variables (first_name, company, topic, pain_point, booking_link)
3. Set daily limits: 20 connection requests/day, 40 messages/day (start at 15 and ramp over 2 weeks)
4. Schedule: weekdays 8am-5pm in prospect's timezone
5. Configure webhooks to fire to n8n on connection_accepted and message_replied events
6. n8n routes these events to Attio and updates the master cadence status

### 3. Set up cloud dialer for scaled calling

Using the `cloud-dialer-call` fundamental, configure your dialer (Aircall, JustCall, or Orum):

1. Import daily call lists from Attio — automatically populated by n8n based on engagement signals (email opens 3+, LinkedIn connection accepted, website visit)
2. Configure call disposition logging: meeting_set, follow_up, not_interested, voicemail, no_answer
3. Set up voicemail drop with 2-3 pre-recorded variants referencing the email sequence
4. Route call outcomes to Attio via API and fire PostHog events for each call
5. Call blocks: 2 hours/day, 30-40 calls. Priority queue: signal-detected prospects first, then cadence-scheduled calls

### 4. Build automated cross-channel follow-ups

Run the `follow-up-automation` drill to create n8n workflows for:

- **Email opened 3+ times, no reply**: Bump phone call priority for next call block
- **LinkedIn connection accepted**: Trigger LinkedIn message sequence step. Adjust email tone in next step to be warmer: "Great connecting on LinkedIn..."
- **Phone voicemail left**: Trigger a follow-up email referencing the voicemail: "Left you a quick message — here's the gist..."
- **Positive reply on any channel**: Stop all automation, create Attio deal at "Interested" stage, notify founder via Slack
- **Meeting booked**: Cancel remaining cadence steps, update Attio deal to "Meeting Booked", confirm meeting via Cal.com

Run the `tool-sync-workflow` drill to connect: Instantly replies -> Attio deals, LinkedIn automation webhooks -> Attio contacts, cloud dialer outcomes -> Attio notes, all events -> PostHog.

### 5. Scale volume to 500-1000 contacts/month

Using Clay and Apollo, build prospect lists of 250 contacts every 2 weeks:
1. Use `build-prospect-list` drill process but at higher volume
2. Run `enrich-and-score` drill with stricter scoring (80+ threshold for Tier 1, 65+ for Tier 2)
3. Separate lists by tier — Tier 1 gets all 3 channels, Tier 2 gets email + LinkedIn only, Tier 3 gets email only
4. Push to Instantly, LinkedIn automation tool, and Attio simultaneously via n8n

Monitor daily limits: never exceed 50 emails/day per sending account, 20 LinkedIn connections/day, 40 calls/day.

### 6. Launch A/B testing across channels

Run the `ab-test-orchestrator` drill. Set up parallel experiments:

**Email experiments (via Instantly A/B):**
- Subject line variants (2 at a time)
- Email 1 opening line variants
- CTA wording variants (question vs. statement vs. social proof)
- Send time variants (8am vs. 10am vs. 2pm)

**LinkedIn experiments (via automation tool variants):**
- Connection note: reference post vs. reference signal vs. mutual connection
- Follow-up message: question-based vs. value-share vs. case study

**Call experiments:**
- Opening line: signal reference vs. email reference vs. direct pain statement
- Best call windows: track connect rate by time of day and day of week

Use PostHog feature flags to randomly assign prospects to variants. Run each test for minimum 100 prospects per variant. Declare winner at 95% confidence. Implement winner and start next test.

### 7. Monitor and evaluate over 2 months

Track weekly in PostHog:
- Total prospects in cadence
- Meeting rate by channel and by tier
- Cost per meeting (total tool spend / meetings booked)
- A/B test results and winning variants adopted

**Pass threshold: Meeting rate ≥ 1.6%** at 500-1000 contacts/month volume over 2 months.

- **PASS**: Document the complete automated workflow, winning variants, and channel-tier allocation. Proceed to Durable.
- **FAIL**: Identify the bottleneck — if volume scaled but conversion dropped, the issue is likely list quality or message fatigue. If cost per meeting rose, investigate which channel became less efficient. Fix and re-run.

## Time Estimate

- Multi-channel cadence design and n8n build: 8 hours
- LinkedIn automation setup: 4 hours
- Cloud dialer setup: 3 hours
- Follow-up automation and tool sync: 8 hours
- Call block execution: 20 hours (2 hrs/day, 2-3 days/week over 2 months)
- A/B test setup and analysis: 8 hours
- List building and enrichment (bi-weekly): 5 hours
- Monitoring and evaluation: 4 hours

Total: ~60 hours over 2 months.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Cold email at scale (multiple accounts) | Hypergrowth: $77.6/mo for 25K contacts (https://instantly.ai/pricing) |
| Clay | Enrichment + AI personalization | Pro: $149/mo; Team: $349/mo at this volume (https://www.clay.com/pricing) |
| Apollo | Contact sourcing at volume | Professional: $99/mo (https://www.apollo.io/pricing) |
| Dripify / Expandi | LinkedIn automation | Dripify: $59/mo; Expandi: $99/mo (https://dripify.io/pricing / https://expandi.io/pricing) |
| Aircall / JustCall | Cloud dialer | Aircall: $30/user/mo; JustCall: $19/user/mo (https://aircall.io/pricing / https://justcall.io/pricing) |
| LinkedIn Sales Navigator | Prospecting + InMail | Core: $99.99/mo (https://business.linkedin.com/sales-solutions) |
| n8n | Cross-channel orchestration | Starter: $20/mo (https://n8n.io/pricing) |
| Attio | CRM deal tracking | Plus: $29/user/mo (https://attio.com/pricing) |
| PostHog | Event tracking + experiments | Free tier likely sufficient; Teams: $0 for first 1M events (https://posthog.com/pricing) |
| Cal.com | Meeting booking | Free tier (https://cal.com/pricing) |

**Estimated play-specific cost: ~$460-830/mo** (Instantly + Clay + Apollo + LinkedIn automation + dialer + Sales Nav)

## Drills Referenced

- `multi-channel-cadence` — design and build the 14-day coordinated outreach sequence across email, LinkedIn, and calls
- `follow-up-automation` — build n8n workflows for automated cross-channel follow-ups and signal-based triggers
- `tool-sync-workflow` — connect Instantly, LinkedIn automation, dialer, Attio, and PostHog into a single data flow
- `ab-test-orchestrator` — run A/B tests on email copy, LinkedIn messages, call scripts, and timing
