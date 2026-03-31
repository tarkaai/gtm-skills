---
name: regional-field-events-scalable
description: >
  Regional Field Events — Scalable Automation. Transform one-off events into
  a recurring multi-city series with automated city rotation, Clay-powered
  prospect sourcing per market, standardized ops, A/B testing across formats
  and topics, and a content repurposing flywheel that drives future attendance.
  Target 2-4 events per month across target markets.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Direct"
level: "Scalable Automation"
time: "80 hours over 3 months"
outcome: ">=150 total attendees, >=65% average show rate, >=15 meetings booked across 8-12 events over 3 months"
kpis: ["Attendees per event", "Show rate", "Meetings booked", "Cost per meeting", "Repeat attendance rate", "City coverage"]
slug: "regional-field-events"
install: "npx gtm-skills add marketing/solution-aware/regional-field-events"
drills:
  - ab-test-orchestrator
---

# Regional Field Events — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events, Direct

## Outcomes

- Scale from ad-hoc events to a consistent 2-4 events per month across 3-5 target markets
- Reach 150+ total attendees over 3 months with automated prospect sourcing and invitation workflows
- Generate 15+ meetings through automated nurture and scaled multi-city operations
- Identify winning combinations of city, format, topic, and invitation channel via A/B testing
- Build a content flywheel: each event produces derivative content that drives RSVPs for future events
- Establish a venue database and city rotation that sustains indefinitely

## Leading Indicators

- Net-new invitees per event increasing (Clay sourcing expanding reach beyond existing network)
- At least 25% of RSVPs come from Clay-sourced prospects (not just personal network)
- Repeat attendance rate >15% in cities with 3+ events (community building signal)
- Content derivatives (LinkedIn posts, recap emails) drive >10% of next event's RSVPs
- Cost per meeting trending down as operational efficiency improves
- At least 3 cities producing consistent pipeline

## Instructions

### 1. Launch the automated multi-city series

Run the the field event series automation workflow (see instructions below) drill to build the full operations engine:

- **City rotation calendar:** Rank target markets by ICP density, active pipeline, and existing customer presence. Build a 3-month calendar with each city getting an event every 6-8 weeks. Target 8-12 total events over 3 months.
- **Automated prospect sourcing:** For each event, n8n triggers Clay to find 200-500 ICP-matching prospects in the target metro at T-28. Enrichment waterfall verifies emails. Deduplication prevents re-inviting recent attendees too soon.
- **Parameterized invitation engine:** Build reusable Loops sequences that auto-populate with event-specific details (city, date, venue, topic, confirmed attendee count for social proof). No manual email writing per event.
- **Venue database:** After each event, rate the venue and log feedback. For return visits to a city, the agent recommends the highest-rated venue. For new cities, the agent produces a ranked shortlist.
- **Post-event automation cascade:** Marking attendance in Attio triggers: nurture sequences, venue feedback request, series metrics update, and next-event scheduling for this city.

**Human action required:** The host still books venues (phone/email), delivers the event in person, and records post-event notes. Everything else is automated.

### 2. A/B test event variables

Run the `ab-test-orchestrator` drill to systematically test one variable at a time across successive events:

**Variables to test (in priority order):**

1. **Format:** Dinner vs happy hour vs lunch in the same city. Keep topic constant. Measure: show rate, Tier 1 percentage, meetings per event.
2. **Topic:** Which pain point or discussion theme drives the most RSVPs and highest-quality conversations? Test 3+ distinct topics over the first 6 events.
3. **Day and time:** Tuesday dinner vs Thursday dinner. Wednesday happy hour vs Friday happy hour. Track show rate and no-show rate by slot.
4. **Invitation channel mix:** Measure RSVP source: personal email, Clay-sourced outreach, LinkedIn DM, referral from previous attendee. Shift effort toward highest-converting channels.
5. **Headcount and exclusivity:** Compare intimate dinner (8-12) vs larger dinner (15-20). Does smaller group size produce more Tier 1 attendees per person?
6. **Topic framing in invitation:** A/B test subject lines and invitation copy. "Executive dinner on [topic]" vs "[Topic] roundtable with [N] [title] leaders" vs personal-tone invitation.

For each test: define the hypothesis, success metric, and comparison baseline before running. After each event, log the result in Attio. After 6 events, compile a "winning formula": best city, format, topic category, time slot, headcount range, and invitation approach.

### 3. Build the content repurposing flywheel

Run the the field event content capture workflow (see instructions below) drill after each event to multiply value:

- **Host debrief → structured insights:** Record a 5-10 minute voice debrief within 2 hours. Extract top themes, notable quotes, pain points, and market intelligence.
- **Theme → LinkedIn post:** Take the most resonant discussion topic and publish a LinkedIn post from the host's perspective: "Hosted a dinner with [N] [title]s in [city] last week. The conversation that dominated the night: [theme]." CTA drives RSVPs to the next event.
- **Insights → recap email:** Send an attendee recap email with 3 key takeaways and a "quote of the night." No-shows receive the same recap with "here's what you missed" framing.
- **Market intelligence → newsletter segment:** Write a "What we heard in [city]" section for the company newsletter.
- **Cross-event patterns → data post:** After 4+ events, aggregate trends: "We hosted dinners in 4 cities this quarter. Here's what [title]s are saying about [trend]."

Schedule content publication over the 2 weeks between events. Each piece links to the next event's RSVP page — creating a flywheel where this event's content drives next event's RSVPs.

### 4. Scale multi-channel promotion

Expand beyond email invitations to a coordinated multi-channel promotion system per event:

- **Email (owned list):** Segmented invitations via Loops. Previous attendees get "We're back in [city]" messaging. New prospects get the full 3-touch sequence.
- **Clay prospecting:** 200-500 net-new, ICP-matching prospects per event with verified emails.
- **LinkedIn organic:** 2 posts per event from the host: announcement post + recap post. Use content derivatives from previous events to build anticipation.
- **Referral channel:** After each event, ask Tier 1 and Tier 2 attendees to invite one peer to the next event. Referred invitees have the highest show rates.
- **Previous attendee re-engagement:** In cities with 3+ events, maintain a "city community" list. These people get a personalized invitation that references the previous gathering.

Track RSVPs by source channel in PostHog. After 6 events, know the cost per RSVP and cost per meeting by channel.

### 5. Evaluate against the threshold

After 3 months (8-12 events), evaluate:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Total attendees | >=150 | Sum of all event attendance in Attio |
| Average show rate | >=65% | Mean show rate across all events |
| Meetings booked | >=15 | Cal.com bookings attributed to event funnel |
| Cost per meeting | Trending down | Total spend / meetings booked, month over month |
| Repeat attendance rate | >=15% | Contacts who attended 2+ events / total unique attendees |
| City coverage | >=3 cities | Number of cities with at least 2 events |

**PASS**: Core metrics met (attendees, show rate, meetings). Proceed to Durable. You have a scalable multi-city series with working automation and a content flywheel.

**FAIL**: Diagnose by metric:
- Low total attendees: Clay sourcing not deep enough, or cities chosen do not have sufficient ICP density. Expand Clay searches. Focus on metro areas with higher prospect density. Consider virtual-hybrid events for thin markets.
- Low show rate: Invitation-to-attendance gap. Strengthen the confirmation sequence. Add social proof ("12 confirmed, including [titles] from [companies]"). For dinners, emphasize the commitment ("We've reserved your seat").
- Low meetings: Events generate warm conversations but follow-up is not converting. Review the nurture sequences — are Tier 1 emails personal enough? Is the CTA clear? Add Loom clips to Tier 1 follow-up.
- High cost per meeting: Venue costs too high relative to conversion. Test happy hour format (lower per-person cost). Negotiate F&B minimums with repeat venues. Compare dinner ROI vs happy hour ROI.

## Time Estimate

- Series automation setup (n8n workflows, Clay integration, Loops sequences, PostHog dashboards): 16 hours
- A/B test planning and implementation: 4 hours
- Content capture system setup (templates, Fireflies, posting workflow): 4 hours
- Per-event effort (venue coordination, review invitees, event execution, debrief): 4 hours x 10 events = 40 hours
- Content derivative production per event: 1 hour x 10 events = 10 hours
- Cross-event analysis and monthly reviews: 6 hours
- **Total: ~80 hours over 3 months** (split: ~30 hours agent, ~50 hours human — field events are inherently human-heavy)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Cal.com | RSVP pages and meeting booking | Free tier — [cal.com/pricing](https://cal.com/pricing) |
| Loops | Invitation sequences, nurture, recap emails | $49/mo (up to 5,000 contacts) — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Event tracking, funnels, dashboards | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM, event lists, venue database, deal tracking | $29/user/mo Plus — [attio.com](https://attio.com) |
| Clay | Prospect sourcing per city | $185/mo Launch (2,500 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| n8n | Series automation, prospect sourcing triggers, nurture orchestration | Self-hosted free or Cloud Pro EUR60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Fireflies | Discussion capture (optional, for structured segments) | $19/mo Pro — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Loom | Personalized Tier 1 follow-up clips | $12.50/mo Business — [loom.com/pricing](https://www.loom.com/pricing) |
| Venue (x10) | F&B for 8-12 events | $2,000-15,000 total depending on format |

**Estimated play-specific cost at Scalable: $3,000-17,000 over 3 months** (venue F&B + software: ~$300-350/mo)

## Drills Referenced

- the field event series automation workflow (see instructions below) — multi-city rotation calendar, automated prospect sourcing, parameterized invitation engine, venue database, and post-event automation cascade
- `ab-test-orchestrator` — systematically test format, topic, timing, channel, and invitation variables across successive events
- the field event content capture workflow (see instructions below) — capture host debriefs, extract structured insights, and produce derivative content that promotes future events
