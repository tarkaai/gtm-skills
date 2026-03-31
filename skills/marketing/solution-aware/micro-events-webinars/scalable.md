---
name: micro-events-webinars-scalable
description: >
  Micro-Event or Webinar — Scalable Automation. Transform one-off webinars into
  an automated bi-weekly series with agent-managed promotion, Clay-powered
  prospect sourcing, content repurposing, and A/B testing across topics,
  formats, and promotion channels. Multiply registrations and pipeline
  without proportional manual effort.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=100 total registrations, >=30% average show rate, >=8 meetings booked over 2 months"
kpis: ["Registrations per event", "Show rate", "Meetings booked", "Cost per meeting", "Repeat attendance rate"]
slug: "micro-events-webinars"
install: "npx gtm-skills add marketing/solution-aware/micro-events-webinars"
drills:
  - webinar-series-automation
  - ab-test-orchestrator
  - content-repurposing
---

# Micro-Event or Webinar — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Scale from ad-hoc events to a consistent bi-weekly or monthly series with automated operations
- Reach 100+ total registrations across events with agent-managed promotion and prospect sourcing
- Generate 8+ meetings over 2 months through automated nurture and scaled promotion
- Identify the winning combination of topic, format, timing, and promotion channel via A/B testing
- Build a content flywheel: each webinar produces derivative content that drives future registrations

## Leading Indicators

- Net-new registrations per event increasing (list growth, not just re-engaging existing contacts)
- At least 20% of registrations come from Clay-sourced net-new prospects
- Repeat attendance rate >15% (community building signal)
- Content derivatives (clips, posts, newsletter sections) drive >10% of next event's registrations
- Cost per meeting trending down as automation efficiency improves

## Instructions

### 1. Launch the automated webinar series

Run the `webinar-series-automation` drill to build the full series engine:

- Create a topic backlog scored by ICP pain alignment, competitive differentiation, and funnel position. Queue at least 6 topics.
- Build the n8n promotion engine that auto-triggers 21 days before each event: registration page generation, email invite waves (day -14 and day -7), LinkedIn post scheduling, personal invite lists from Attio, and day-of reminders.
- Configure Clay to find 200-500 net-new, topic-relevant prospects per event using `clay-people-search` and `clay-enrichment-waterfall`. Import into Loops for targeted invitation.
- Set up speaker coordination workflows for events with guest panelists or interviewees: prep call scheduling, technical check reminders, and post-event thank-you.

Target cadence: bi-weekly events for the first month (4 events), then evaluate whether to maintain bi-weekly or shift to monthly based on performance data.

### 2. A/B test event variables

Run the `ab-test-orchestrator` drill to systematically test one variable at a time across successive events:

**Variables to test (in priority order):**

1. **Topic category**: Which pain point area drives the most registrations and pipeline? Test at least 3 distinct topic categories over the first 4 events.
2. **Event format**: Presentation vs. workshop vs. panel vs. fireside chat. Keep topic constant, change format.
3. **Day and time**: Tuesday 11am vs. Wednesday 2pm vs. Thursday 10am. Track show rate by slot.
4. **Promotion channel mix**: Measure registration source by channel. Shift budget toward highest-converting channels.
5. **Email subject line**: A/B test invite email subject lines within the same send using Loops.

For each test, define the hypothesis, success metric, and minimum sample size before running. After each event, log the result and the learning in Attio. After 4 events, compile a "winning formula" document: best topic category, format, time slot, and promotion channel.

### 3. Build the content repurposing flywheel

Run the `content-repurposing` drill after each webinar to multiply content output:

- **Recording → clips**: Extract 3-5 highlight clips (60-90 seconds each) from each recording using Descript. Focus on: the strongest insight, the best audience question + answer, and a quotable moment from the speaker.
- **Recording → blog post**: Transcribe the webinar and transform it into a 1,500-word blog post covering the key frameworks and takeaways.
- **Clips → LinkedIn posts**: Each clip becomes a LinkedIn post with a text hook, the video clip, and a CTA to register for the next event.
- **Q&A → newsletter section**: The best audience questions become a "questions from our community" section in your newsletter via Loops.
- **Talk track → email sequence**: The webinar's core argument becomes a 3-email educational sequence that warms up future webinar registrants.

Schedule derivative content to publish over the 2 weeks between events. Each piece of content should link to the next event's registration page, creating a flywheel where this event's content drives next event's registrations.

### 4. Scale registration through multi-channel promotion

Expand beyond manual outreach and email to a multi-channel promotion system:

- **Email (owned list)**: Segmented broadcasts via Loops. Send topic-relevant invites to the right audience segments — do not blast everyone.
- **Clay prospecting**: 200-500 net-new prospects per event enriched and imported into the invite flow.
- **LinkedIn organic**: 3 posts per event (announcement, speaker spotlight, countdown) using content derivatives from previous events.
- **LinkedIn paid (optional)**: If budget allows, promote the registration page via LinkedIn Sponsored Content. Target by title + industry matching your ICP. Start with $200/event and measure cost per registration.
- **Personal invites**: Use Attio to identify high-value prospects in active pipeline. A webinar invite is a low-friction way to re-engage stalled deals.
- **Cross-promotion**: If you have guest speakers, they promote to their audience. Negotiate this as part of the speaker agreement.

Track registrations by source channel in PostHog. After 4 events, you should know your cost per registration and cost per meeting by channel.

### 5. Evaluate against the threshold

After 2 months (4-8 events), evaluate:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Total registrations | >=100 | Sum of all event registrations in Attio |
| Average show rate | >=30% | Mean show rate across all events |
| Meetings booked | >=8 | Cal.com bookings attributed to webinar funnel |
| Cost per meeting | Trending down | Total spend / meetings booked, event over event |
| Repeat attendance rate | >=15% | Contacts who attended 2+ events / total unique attendees |

**PASS**: All core metrics met (registrations, show rate, meetings). Proceed to Durable. You have a scalable series with working automation.

**FAIL**: Diagnose by metric:
- Low registrations: Clay prospecting not producing enough net-new contacts, or topic backlog exhausted. Refresh the topic backlog based on ICP research. Expand Clay searches.
- Low show rate: Reminder sequence not effective, or events scheduled at suboptimal times. Test different time slots. Add a value-add to the reminder ("Here's a preview of what we'll cover").
- Low meetings: Events attract curious but not high-intent attendees. Shift topics closer to product-relevant pain points (solution-aware, not problem-aware). Improve the CTA during and after the event.

## Time Estimate

- Series automation setup (n8n workflows, Clay integration, Loops sequences): 12 hours
- A/B test planning and implementation: 4 hours
- Content repurposing system setup (Descript, templates): 4 hours
- Per-event effort (promotion review, content delivery, analysis): 4 hours x 6 events = 24 hours
- Cross-event analysis and optimization: 8 hours
- Content derivative creation: 8 hours total (spread across events)
- **Total: ~60 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Riverside | Webinar recording + production | $19/mo Standard or $29/mo Pro (4K) — [riverside.com/pricing](https://riverside.com/pricing) |
| Loops | Email invites, reminders, nurture | $49/mo (up to 5,000 contacts) — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Event tracking, funnels, experiments | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM, event lists, deal tracking | Free (3 users) or $29/user/mo Plus — [attio.com](https://attio.com) |
| n8n | Series automation workflows | Self-hosted free or Cloud Starter EUR24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Clay | Prospect sourcing per event | $185/mo Launch (2,500 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| Descript | Recording clips + transcription | $24/mo Creator — [descript.com/pricing](https://www.descript.com/pricing) |
| Loom | Personalized follow-up clips | Free (25 videos, 5 min each) or $12.50/mo Business — [loom.com/pricing](https://www.loom.com/pricing) |
| Cal.com | Meeting booking CTA | Free tier — [cal.com/pricing](https://cal.com/pricing) |
| LinkedIn Ads | Paid promotion (optional) | ~$200-500/event budget — [linkedin.com/ad](https://www.linkedin.com/ad) |

**Estimated play-specific cost at Scalable: $275-530/mo** (Riverside + Loops + Clay + Descript + optional paid promotion)

## Drills Referenced

- `webinar-series-automation` — automate recurring series operations, promotion engine, prospect sourcing, and cross-event analytics
- `ab-test-orchestrator` — systematically test topic, format, timing, and promotion variables across events
- `content-repurposing` — transform each webinar recording into derivative content that drives future registrations
