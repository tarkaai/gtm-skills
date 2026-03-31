---
name: co-webinar-series-scalable
description: >
  Co-Webinar Series — Scalable Automation. Automate a portfolio of 6+ co-webinar
  partners with scheduled events, automated promotion workflows, attendee
  nurture, and cross-event analytics — running bi-weekly events with minimal
  manual coordination.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Events, Email"
level: "Scalable Automation"
time: "80 hours over 3 months"
outcome: "≥ 500 registrations and ≥ 40 qualified leads from bi-weekly co-webinars over 3 months"
kpis: ["Total registrations per event", "Show rate", "Qualified leads per event", "Partner contribution ratio", "Meetings booked per event", "Repeat attendance rate"]
slug: "co-webinar-series"
install: "npx gtm-skills add marketing/solution-aware/co-webinar-series"
drills:
  - webinar-series-automation
  - partner-pipeline-automation
---

# Co-Webinar Series — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Events, Email

## Outcomes

A portfolio of 6+ active co-webinar partners with automated event scheduling, promotion workflows, attendee nurture, and cross-event analytics. Bi-weekly co-webinars producing at least 500 total registrations and at least 40 qualified leads over 3 months. The 10x multiplier at this level comes from: (a) managing more partners simultaneously without proportional coordination effort, (b) reusing proven webinar formats and promotion templates across similar partner audiences, (c) automating the promotion engine that was manual at Baseline, (d) building a content calendar and partner rotation that sustains the series without scrambling for topics or speakers, and (e) using cross-event analytics to double down on winning partner-topic-format combinations.

## Leading Indicators

- Partner pipeline converts at >= 30% (prospects contacted to confirmed co-webinar partners)
- Event cadence is bi-weekly (2 co-webinars per month) for 3+ consecutive months
- Average registrations per event holds at or above 80 (Baseline average)
- Partner contribution ratio stays above 30% across all events (partners are pulling their weight)
- Qualified lead conversion rate holds at or above 6% of registrants (Baseline benchmark)
- Repeat attendance rate reaches 15%+ (people attend 2+ co-webinars in the series)
- Time spent on per-event coordination drops below 3 hours/event (down from 6+ at Baseline)
- At least 2 partners request to co-host a second event with you (signal: partners see value in recurring collaboration)
- Automation handles promotion, reminders, and follow-up without manual intervention

## Instructions

### 1. Build the event series automation

Run the `webinar-series-automation` drill to create n8n workflows that automate the full co-webinar lifecycle:

**Series calendar workflow (triggered by new event creation in Attio):**
- When a new co-webinar is added to the Attio events list, auto-generate: registration page with co-branding, UTM-tagged promotion links for both sides, reminder email sequence in Loops, recording distribution plan
- Schedule promotion cadence: Day -21 (partner coordination), Day -14 (first email wave), Day -7 (second wave + LinkedIn), Day -1 (final reminder), Day 0 (event), Day +1 (nurture launch)

**Promotion engine workflow (daily cron during active promotion windows):**
- Day -14: Send targeted registration emails to the most relevant Attio segment via Loops. Use Clay to find and enrich 100-200 net-new prospects who match the event topic's ICP segment, add them to the invite list.
- Day -7: Send second email to non-openers. Post speaker spotlight on LinkedIn. Send personal invites from Attio to high-value prospects in active pipeline.
- Day -1: Send final reminder to all registrants.
- Day 0: 1-hour reminder with join link. Configure recording platform.
- Day +1: Trigger the `webinar-attendee-nurture` drill with attendee data segmented by source.

**Partner coordination workflow:**
- When a co-webinar is scheduled, auto-send the partner: their UTM-tagged promotion link, suggested promotion copy (email and LinkedIn drafts), speaker prep logistics (date, time, platform link, prep call booking link), and content outline
- 7 days before: auto-check if partner promotion has started (track registrations from partner UTM). If partner-sourced registrations are 0, fire alert: "Partner has not started promotion — follow up."
- 3 days before: auto-send partner a technical check reminder with platform test link

### 2. Scale the partner portfolio

Run the `partner-pipeline-automation` drill to automate partner lifecycle management:

**Partner pipeline stages:**
- Prospect → Pitched → Confirmed → Scheduled → Completed → Repeat (or Retired)

**Cadence tiering based on Baseline performance:**
- **Monthly partners (top 2-3)**: Partners whose co-webinars produced the most qualified leads. Schedule a recurring monthly slot.
- **Quarterly partners (3-5)**: Solid performers or new partners in trial. Schedule one event per quarter.
- **New partners (2-3 per quarter)**: Fresh additions from the co-webinar partner matching pipeline. Run their first event to establish a performance baseline.

**Partner portfolio rules:**
- Maintain 6+ active co-webinar partners at all times
- Never co-host with the same partner more than once per month (prevent audience fatigue on both sides)
- Rotate topics: never repeat the same topic with the same partner within 6 months
- Maintain a partner prospect pipeline of 10+ candidates in the "Pitched" or "Prospect" stage

### 3. Build the content calendar and topic backlog

Create a topic backlog in Attio ranked by expected registration pull. Score each topic on three factors:

- **ICP pain alignment (1-5)**: How directly does this topic address a top-3 pain point?
- **Competitive differentiation (1-5)**: Can you + the partner say something others cannot? Unique data, unique workflow, unique integration?
- **Funnel position (1-3)**: 1 = broad awareness, 2 = solution consideration, 3 = product evaluation. Mix across the series.

Map topics to partners: each topic should match a partner whose product is naturally part of the story. Schedule events bi-weekly for the next 3 months. Alternate between high-performing formats identified at Baseline (panel, workshop, fireside).

### 4. Automate attendee nurture at scale

Deploy the `webinar-attendee-nurture` drill as an automated pipeline that triggers after every event:

- Auto-segment registrants into tiers based on attendance and engagement data
- Auto-enroll each tier in the appropriate Loops sequence
- Auto-create Attio deals for Tier 1 contacts matching your ICP
- Auto-escalate: if a Tier 1 or Tier 2 contact replies to any nurture email, notify the founder or sales lead via Slack
- Track all nurture outcomes in PostHog with per-partner attribution so you know which partner's audience converts best

### 5. Build cross-event analytics

Build PostHog dashboards for series-level performance:

- **Registrations by event** (bar chart, colored by partner): which events and partners drive the most registrations?
- **Show rate trend** (line chart, last 12 events): is show rate improving, flat, or declining?
- **Qualified leads per event** (bar chart): which events generate the most pipeline?
- **Partner contribution ratio by event** (stacked bar): is each partner pulling their promotional weight?
- **Promotion channel effectiveness** (by event): email vs LinkedIn vs personal invites — which channel drives the most registrations?
- **Repeat attendee count** (counter): how many people have attended 2+ events? These are your most engaged prospects.
- **Topic performance heatmap**: topic category vs qualified lead conversion rate.
- **Format performance comparison**: panel vs workshop vs fireside — which format converts best?

After every 4 events, the agent analyzes:
- Which partner-topic-format combinations drove the most pipeline?
- Which promotion channels had the highest conversion per event?
- What day of week and time slot produced the best show rate?
- Are any partners underperforming their historical average? (flag for replacement or topic change)

Store findings in Attio. Adjust the upcoming calendar based on data.

### 6. Scale registration through targeted prospecting

For each upcoming co-webinar, use Clay to find net-new prospects:

- Use `clay-people-search` to find people with titles and companies matching the event topic's ICP
- Use `clay-enrichment-waterfall` to enrich with email and company data
- Import into Attio with a "Co-Webinar Prospect" tag and the specific event slug
- Add to the targeted invite list in Loops

Target: 100-300 net-new, topic-relevant prospects per event to supplement your existing list and the partner's audience.

### 7. Evaluate against threshold

After 3 months (approximately 6 co-webinars), measure aggregate results:

**Pass threshold: >= 500 registrations AND >= 40 qualified leads from bi-weekly co-webinars over 3 months**

- **Pass**: Document the partner portfolio, automation workflows, per-partner economics, top formats and topics, and cross-event trends. Identify anchor partners (top 2-3 who consistently produce the most pipeline). Proceed to Durable.
- **Marginal**: 350-499 registrations or 25-39 qualified leads. Scale is working but conversion needs optimization. Test: different topics with existing partners, different nurture sequences, or different registration page positioning. Run one more month.
- **Fail**: <350 registrations. Diagnose: Is the partner pipeline too small? Are events actually running bi-weekly? Is promotion quality declining as you automate? Are the wrong partners in the portfolio? Fix the bottleneck and run one more month.

## Time Estimate

- Series automation setup (n8n workflows, Loops sequences, Attio pipeline): 20 hours
- Partner pipeline expansion (research + outreach + confirmation): 12 hours
- Content calendar and topic backlog creation: 4 hours
- Ongoing per-event management (12 events x 2.5 hours): 30 hours
- Cross-event analytics build and monthly reviews: 8 hours
- Net-new prospect sourcing via Clay: 6 hours

Total: ~80 hours over 3 months (heavily front-loaded in month 1; months 2-3 run mostly on automation)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| n8n | Workflow automation (event scheduling, promotion engine, partner coordination) | Cloud Pro: ~EUR 60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Partner CRM, event calendar, registrant tracking, deal pipeline | Plus: $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Event tracking, funnel analytics, cross-event dashboards | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Confirmation emails, reminders, tiered nurture sequences at scale | Paid from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Clay | Net-new prospect sourcing per event | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Riverside | Webinar hosting and recording | Business: $24/mo ([riverside.fm/pricing](https://riverside.fm/pricing)) |
| Loom | Personalized follow-up clips for Tier 1 attendees | Business: $15/user/mo ([loom.com/pricing](https://www.loom.com/pricing)) |
| Anthropic Claude | Topic ideation, promotion copy, analysis generation | Sonnet: ~$15-30/mo at this volume ([docs.anthropic.com/en/docs/about-claude/models](https://docs.anthropic.com/en/docs/about-claude/models)) |

**Estimated cost for this level: ~$200-400/mo** (n8n Pro + Attio Plus + Loops paid + Clay + Riverside + Anthropic API)

## Drills Referenced

- `webinar-series-automation` — automate recurring event operations including promotion engine, speaker coordination, cross-event analytics, and post-event nurture triggers
- `partner-pipeline-automation` — automate partner outreach, onboarding, cadence tiering, and lifecycle management
