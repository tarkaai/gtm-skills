---
name: local-field-prospecting-scalable
description: >
  Local Field Prospecting — Scalable. Find the 10x multiplier by expanding territories,
  enriching venue-adjacent businesses for pre-visit outreach, optimizing routes with data,
  and running A/B tests on pitch and follow-up approaches.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Other"
level: "Scalable"
time: "50 hours over 2 months"
outcome: "≥ 10 qualified meetings over 2 months with improving conversation-to-meeting rate"
kpis: ["Meetings booked per month", "Conversation-to-meeting rate", "Pipeline value from field", "Meetings per hour in field", "Follow-up conversion rate"]
slug: "local-field-prospecting"
install: "npx gtm-skills add sales/qualified/local-field-prospecting"
drills:
  - field-contact-logging
  - enrich-and-score
  - ab-test-orchestrator
---

# Local Field Prospecting — Scalable

> **Stage:** Sales > Qualified | **Motion:** OutboundFounderLed | **Channels:** Other (In-Person)

## Outcomes

Field prospecting becomes a data-driven, optimized machine. The agent identifies which venues, neighborhoods, days, and times produce the most meetings. Venue-adjacent businesses are enriched in advance so the founder walks in knowing who to talk to. Pitch variants and follow-up sequences are A/B tested. The founder's time in the field is maximized — more meetings per hour, higher conversion rates, and expanding territory coverage. At least 10 meetings over 2 months, with the rate improving month over month.

## Leading Indicators

- Territory score improving (higher-yield venues replacing dead zones)
- Pre-visit enrichment hit rate (what % of businesses at a venue match ICP)
- Meetings per field hour trending up
- A/B test win rate (are experiments producing improvements)
- New venues discovered and tested per month
- Pipeline value per field session trending up
- Repeat visits to high-yield venues producing diminishing or sustained returns

## Instructions

### 1. Analyze Baseline data and optimize territories

Run the the field territory optimization workflow (see instructions below) drill using your 2+ weeks of Baseline data:

- Build the field performance dashboard in PostHog with venue-level breakdowns
- Identify high-yield venues (high conversations AND high meeting conversion) — increase frequency
- Identify dead zones (low traffic or low conversion) — remove from rotation
- Analyze day-of-week and time-of-day patterns — shift sessions to peak times
- Calculate cost per meeting by venue (travel time + session time / meetings booked)
- Discover new venues in adjacent areas that match the profile of your top performers

Output: an optimized weekly schedule with venue priorities and new venues to test each month.

### 2. Pre-enrich venue businesses for targeted conversations

This is the 10x lever. Instead of walking into a coworking space cold, the founder walks in knowing which companies there match the ICP.

Run the `enrich-and-score` drill for each high-priority venue:

1. **Source tenant lists**: Many coworking spaces list member companies on their website. Scrape or manually collect company names. For business parks, check the building directory or property management website.
2. **Import to Clay**: Create a Clay table per venue with the company list.
3. **Enrich**: Run the Clay enrichment waterfall to get: company size, industry, funding stage, key personnel (name, title, LinkedIn), technology stack.
4. **Score against ICP**: Apply your ICP scoring model. Filter to companies scoring 70+.
5. **Prepare per-venue hit lists**: For each venue visit, the agent produces a list: "At WeWork SoMa, these 5 companies match your ICP: [Company A — CTO is Jane Smith, Series A, 20 employees, uses [competitor]]. Talk to them first."

The founder now walks in with targets, not just hope.

### 3. Launch pitch and follow-up A/B testing

Run the `ab-test-orchestrator` drill to systematically test what works:

**Pitch variants to test** (rotate across sessions, track which yields higher meeting rates):
- **Pain-led opener**: "I've been hearing a lot of [pain] from [role] at companies like yours. Is that something you deal with?"
- **Curiosity-led opener**: "I'm building something for [ICP] and I'm trying to understand how companies here handle [problem]. Do you have 2 minutes?"
- **Social-proof opener**: "We just helped [similar company] solve [problem]. I noticed a few companies here that might face the same thing."
- **Event-led opener**: Reference a local meetup, tech event, or industry news as a conversation starter.

**Follow-up variants to test:**
- Email timing: same-day vs. next-morning follow-up
- Email format: short and direct vs. resource-attached vs. video message
- CTA: Cal.com link vs. "reply with your availability" vs. specific proposed time
- Channel: email-only vs. email + LinkedIn connection request

Track all variants in PostHog using feature flags. Minimum 20 conversations per variant before declaring a winner.

### 4. Expand territory coverage

Using patterns from the field territory optimization workflow (see instructions below):

- **Adjacent neighborhoods**: If downtown coworking spaces work, test the ones 2 miles away in emerging neighborhoods
- **Different venue types**: If coworking spaces work, test business incubators, accelerator offices, industry-specific hubs, and co-located startup campuses
- **Event-enhanced visits**: Time venue visits to coincide with community events (demo days, lunch-and-learns, networking hours). Events concentrate ICP-matching people and create natural conversation starters.
- **Seasonal adjustment**: Test whether summer outdoor co-working events, conference hallways, or seasonal business fairs open new prospecting surfaces

Add 2-3 new venues to the test rotation each month. Run each test venue at least twice before scoring.

### 5. Build the referral flywheel

Field prospecting has a unique advantage over digital outreach: referrals happen naturally in person.

- After every good conversation (even with non-ICP contacts), ask: "Do you know anyone here who deals with [pain]?"
- Log every referral in Attio with the referrer tagged. Track referral-sourced meetings separately.
- For contacts who gave referrals, send a thank-you note and keep them in a warm-network list for future asks.
- Track referral rate as a KPI: what % of conversations produce a referral to someone else at the venue?

### 6. Scale the cadence

Increase from 2 sessions/week to 3-4 sessions/week, each covering a different territory:

- **Monday**: Agent runs the field visit planning workflow (see instructions below) for the week with pre-enriched target lists
- **Tuesday/Wednesday/Thursday**: Field sessions (2-3 hours each)
- **Friday**: Agent runs territory optimization analysis, A/B test evaluation, and plans next week
- **Ongoing**: Automated follow-ups run continuously via n8n

### 7. Evaluate against threshold

After 2 months, evaluate: >= 10 meetings with improving conversion rate.

Key metrics to assess:
- Meetings booked: >= 10 (month 2 should be higher than month 1)
- Conversation-to-meeting rate: should be improving from A/B test winners
- Meetings per field hour: should be improving from territory optimization
- Pipeline value: track revenue attribution back to field sessions
- Pre-enrichment ROI: do enriched-target conversations convert better than cold?

If **PASS**: The play scales predictably. Proceed to Durable for autonomous optimization.
If **FAIL**: Identify the ceiling. Is it venues (saturated the area)? Pitch (plateaued conversion)? Follow-up (leaking at conversion)? ICP (wrong market for in-person)? If the ceiling is geographic saturation, this play may have hit its natural limit for your area.

## Time Estimate

- 4 hours/week: Visit planning, enrichment, and territory analysis (agent)
- 6 hours/week: Field sessions — 3 sessions x 2 hours each (founder, human action)
- 1 hour/week: Contact logging and debrief (agent + founder)
- 1 hour/week: A/B test analysis, follow-up monitoring, territory optimization (agent)

Total: ~50 hours over 2 months (~6 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Maps | Venue discovery, route optimization | Free tier or Starter $100/mo (if high API volume) |
| Attio | CRM — contacts, deals, notes, reporting | Plus at $29/user/mo |
| Cal.com | Meeting booking with tracking | Free tier (1 user) |
| PostHog | Analytics, funnels, feature flags for A/B tests | Free tier (1M events/mo) |
| n8n | Automation — follow-ups, syncs, alerts | Starter at $24/mo or self-hosted free |
| Clay | Venue business enrichment and scoring | Launch at $185/mo |
| Apollo | Initial contact sourcing for venue tenants | Free tier (10K credits/mo) |

**Total Scalable cost: $238-338/mo** (Clay is the primary new cost for pre-enrichment)

## Drills Referenced

- the field visit planning workflow (see instructions below) — weekly venue research with pre-enriched target lists
- `field-contact-logging` — structured CRM logging with A/B test variant tracking
- the field territory optimization workflow (see instructions below) — data-driven venue/territory/timing optimization
- `enrich-and-score` — pre-enrich venue businesses so founder has targets before arriving
- `ab-test-orchestrator` — systematically test pitch variants and follow-up approaches
