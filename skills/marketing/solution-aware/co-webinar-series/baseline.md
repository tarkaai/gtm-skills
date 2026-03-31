---
name: co-webinar-series-baseline
description: >
  Co-Webinar Series — Baseline Run. Run co-webinars with 3 different partners
  over 6 weeks with proper event tracking and per-partner attribution to validate
  that the channel is repeatable across different partner audiences before
  automating.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Events, Email"
level: "Baseline Run"
time: "20 hours over 6 weeks"
outcome: "≥ 150 registrations and ≥ 10 qualified leads across 3 co-webinars in 6 weeks"
kpis: ["Total registrations", "Show rate", "Qualified leads per event", "Partner contribution ratio", "Meeting booking rate"]
slug: "co-webinar-series"
install: "npx gtm-skills add marketing/solution-aware/co-webinar-series"
drills:
  - posthog-gtm-events
  - webinar-attendee-nurture
  - co-webinar-partner-matching
---

# Co-Webinar Series — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Events, Email

## Outcomes

Co-webinars completed with 3 different partners over 6 weeks. At least 150 total registrations and at least 10 qualified leads across all events. This level proves the channel is repeatable across multiple partners with different audiences — not a one-off win from a single lucky pairing. It also establishes per-partner performance baselines and identifies which partner types, topics, and formats drive the most pipeline.

## Leading Indicators

- 3+ partners agree to co-webinar within the first 2 weeks of outreach (signal: the co-webinar pitch works across different companies)
- Per-event registration volume is consistent (within ±30%) across events with partners of similar audience size (signal: results are not partner-dependent flukes)
- Partner contribution ratio holds at 30%+ across all 3 events (signal: partners are genuinely co-promoting, not free-riding)
- Show rate holds above 30% across all 3 events (signal: topic selection and reminder cadence are working)
- At least 2 events produce qualified leads (signal: the channel converts across different audiences)
- Recording watch rate for no-shows exceeds 30% (signal: on-demand content extends the event's value)
- At least 1 partner proactively proposes a second co-webinar (signal: the partnership felt valuable to them)

## Instructions

### 1. Set up event tracking

Run the `posthog-gtm-events` drill to configure a standardized event taxonomy for this play. Create these PostHog events with standard properties:

- `cowebinar_page_viewed` — registration page visit. Properties: `partner_slug`, `utm_source`, `utm_medium`, `utm_campaign`.
- `cowebinar_registered` — visitor submits registration form. Properties: `partner_slug`, `registration_source` (own/partner, derived from UTM), `registrant_company`, `registrant_role`.
- `cowebinar_reminder_sent` — reminder email dispatched. Properties: `partner_slug`, `reminder_type` (1_week/1_day/1_hour).
- `cowebinar_reminder_clicked` — registrant clicked the join link in a reminder. Properties: `partner_slug`.
- `cowebinar_attended` — registrant joined the live event. Properties: `partner_slug`, `registration_source`.
- `cowebinar_engaged` — attendee asked a question, responded to a poll, or clicked an in-session CTA. Properties: `partner_slug`, `engagement_type`.
- `cowebinar_recording_watched` — no-show or late registrant watched the recording. Properties: `partner_slug`, `percent_watched`.
- `cowebinar_nurture_reply` — attendee replied to a follow-up email. Properties: `partner_slug`, `tier`, `sequence_step`.
- `cowebinar_meeting_booked` — attendee booked a follow-up meeting. Properties: `partner_slug`, `tier`, `source_email_step`.

Build a PostHog insight: bar chart of registrations per event grouped by `registration_source` (own vs partner) and `partner_slug`.

### 2. Expand partner outreach

Run the `co-webinar-partner-matching` drill with a larger scope: identify 10-15 candidates. From these, secure 3 confirmed co-webinar partners for the next 6 weeks. Select partners that represent different audience segments so you can test which partner archetype converts best:

- 1 partner from a closely adjacent product category (e.g., complementary tool in the same workflow)
- 1 partner from a slightly different vertical but with the same buyer persona
- 1 partner with a larger audience than yours (tests whether you can "borrow" a bigger audience through partnership)

For partners where you lack a direct relationship, leverage mutual connections or engage with their content on LinkedIn for 1-2 weeks before pitching. Log every outreach attempt in Attio with the `cowebinar_partner_contacted` event.

**Human action required:** Send the co-webinar pitch. Partnership requests convert better from a founder or marketing lead, not an automated sequence.

### 3. Plan 3 co-webinars with differentiated topics and formats

Schedule events bi-weekly over 6 weeks. Vary the format to test what works:

- **Event 1 (Week 2)**: Expert panel — both speakers present, followed by moderated Q&A. 45 minutes.
- **Event 2 (Week 4)**: Live workshop — interactive walkthrough of a workflow using both products. 60 minutes.
- **Event 3 (Week 6)**: Fireside chat — conversational discussion on a shared pain point, less structured, more audience interaction. 30 minutes.

For each event, create:
- A dedicated registration page with partner co-branding
- UTM-tagged promotion links for both sides
- Attio list for registrants tagged by partner and source
- Reminder sequence in Loops (confirmation, 1-week, 1-day, 1-hour)

### 4. Execute the post-event nurture

After each event, run the `webinar-attendee-nurture` drill:

- Segment registrants into tiers: Tier 1 (engaged attendees), Tier 2 (passive attendees), Tier 3 (no-shows), Tier 4 (late registrants from replay promotion)
- Deploy tier-specific nurture sequences via Loops
- Create Attio deals for Tier 1 contacts matching your ICP
- Track all nurture events in PostHog for per-partner attribution

Critically: track whether partner-sourced registrants convert at the same rate as your own. This determines the actual value of the partner's audience contribution.

### 5. Build per-partner and per-event performance analysis

After all 3 events have completed their nurture windows (14 days post each event), analyze:

**Per-partner performance:**
- Total registrations driven by each partner vs by you
- Show rate for partner-sourced vs your-sourced registrants
- Qualified leads per partner (Tier 1 attendees + replies + meetings)
- Meeting booking rate from partner-sourced attendees
- Partner effort level: did they promote once or across multiple channels?

**Per-format performance:**
- Which format (panel, workshop, fireside) produced the most registrations?
- Which format had the highest show rate and engagement rate?
- Which format generated the most qualified leads?

**Topic performance:**
- Which topic drove the highest registration conversion on the page?
- Which topic produced the most Q&A engagement?
- Which topic generated the most post-event meetings?

**Audience overlap analysis:**
- Did any partner-sourced registrants already exist in your Attio database? (overlap = they were already in your funnel)
- What % of partner-sourced registrants were genuinely net-new to you?

### 6. Evaluate against threshold

Measure aggregate results across all 3 co-webinars:

**Pass threshold: >= 150 registrations AND >= 10 qualified leads across 3 co-webinars in 6 weeks**

- **Pass**: Document per-partner performance, top formats and topics, registration source breakdown, and qualified lead conversion rates. Rank partners by pipeline generated. Identify the partner archetype, topic type, and format that work best. Proceed to Scalable.
- **Marginal**: 100-149 registrations or 6-9 qualified leads. The channel works but needs refinement. Diagnose: is the bottleneck partner quality (low contribution), topic selection (low registration), event execution (low engagement), or follow-up (low conversion)? Run 1-2 more events targeting the weak link.
- **Fail**: <100 registrations across 3 events. Diagnose: Are partners actually promoting? Are the topics compelling enough to register for? Is the landing page converting? Are you reaching solution-aware prospects or educating unaware ones? Fix the largest bottleneck and re-test.

## Time Estimate

- Event tracking setup: 1.5 hours
- Partner outreach (10-15 candidates, secure 3): 4 hours
- Event planning and setup (3 events): 4.5 hours
- Promotion per event (3 events x 1 hour): 3 hours
- Event execution (3 events x 1 hour, human action): 3 hours
- Post-event nurture setup (3 events x 30 min): 1.5 hours
- Monitoring and per-event analysis: 1.5 hours
- Final cross-event analysis and evaluation: 1 hour

Total: ~20 hours of active work over 6 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnel analytics, per-partner attribution | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | Partner CRM, registrant tracking, deal creation | Free for up to 3 users; Plus: $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Loops | Confirmation emails, reminders, tiered nurture sequences | Free up to 1K contacts; paid from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Clay | Partner enrichment (if expanding research) | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Riverside | Webinar hosting and recording | Free plan; Business: $24/mo ([riverside.fm/pricing](https://riverside.fm/pricing)) |
| Anthropic Claude | Topic ideation, nurture email copy, per-event analysis | Sonnet: ~$0.50-2.00 total ([docs.anthropic.com/en/docs/about-claude/models](https://docs.anthropic.com/en/docs/about-claude/models)) |

**Estimated cost for this level: ~$25-75/mo** (Riverside Business plan + Loops paid tier if beyond free limits; everything else within free tiers)

## Drills Referenced

- `posthog-gtm-events` — set up standardized event tracking with per-partner attribution
- `webinar-attendee-nurture` — post-event tiered nurture sequences that convert attendees into pipeline
- `co-webinar-partner-matching` — find and qualify co-webinar partners (run with expanded scope to secure 3 partners)
