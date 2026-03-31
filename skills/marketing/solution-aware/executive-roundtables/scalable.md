---
name: executive-roundtables-scalable
description: >
  Executive Roundtables — Scalable Automation. Transform one-off roundtables into
  an automated bi-monthly series with agent-managed guest curation via Clay,
  topic calendar scheduling, cross-event analytics, A/B testing on invitation
  approaches and discussion formats, and a growing executive guest pool. Multiply
  pipeline without proportional host effort.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Scalable Automation"
time: "60 hours over 6 months"
outcome: ">=80 executive attendees and >=30 meetings from bi-monthly roundtables over 6 months"
kpis: ["Attendees per event", "Meeting conversion rate", "Cost per meeting", "Guest pool depth", "Referral rate"]
slug: "executive-roundtables"
install: "npx gtm-skills add marketing/solution-aware/executive-roundtables"
drills:
  - ab-test-orchestrator
---

# Executive Roundtables — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Scale from ad-hoc roundtables to a consistent bi-monthly series (6 events over 6 months) with automated guest sourcing, invitation ops, and post-event workflows
- Reach 80+ total executive attendees across the series with agent-managed guest curation
- Generate 30+ follow-up meetings through automated nurture and systematized host follow-up
- Build and maintain a deep executive guest pool: always have 50+ uninvited ICP-matched executives ready for the next event
- Identify the winning formula: which topic categories, guest profiles, facilitation styles, and invitation approaches produce the highest meeting conversion
- Create a content flywheel: discussion summaries and insights from each roundtable drive future guest recruitment

## Leading Indicators

- Net-new executives per event increasing (guest pool growth, not just re-engaging past attendees)
- At least 30% of guests per event are sourced from Clay enrichment (not just existing CRM contacts)
- Referral rate >20%: 1 in 5 attendees proactively refers a peer for the next event
- Guest pool depth stays above 50 uninvited ICP contacts at all times
- Cost per meeting trending down as series reputation builds and organic demand increases
- At least 3 past attendees request invitations to future events without being asked

## Instructions

### 1. Launch the automated roundtable series engine

Run the the roundtable series automation workflow (see instructions below) drill to build the full series operations system:

**Topic calendar:**
Create a topic backlog with at least 8 topics scored on: timeliness (is this urgent now?), discussion potential (will execs disagree?), and guest availability (can you find 20+ targets with direct experience?). Schedule 6 events bi-monthly for the next 12 months. Store the calendar in Attio.

Rotate topic categories to prevent fatigue. If event 1 is about organizational strategy, event 2 should cover technology bets or market dynamics. Never repeat the same topic category in consecutive events.

**Guest curation engine (n8n workflow, triggers 28 days before each event):**

- Day -28: Source guests.
  - Query Attio for contacts matching the event's target profile.
  - Filter out: anyone who attended the last roundtable (prevent fatigue), anyone who declined the last 2 invitations (respect their time), anyone in an active sales cycle (avoid awkwardness).
  - Target a 60/40 mix: 60% new invitees, 40% returning high-engagement past attendees.
  - Use `clay-people-search` and `clay-enrichment-waterfall` to find 10-15 net-new C-level prospects per event who match the topic and ICP but are not yet in Attio. Enrich with: verified email, company size, recent news, LinkedIn activity.
  - Import new contacts to Attio with tag "exec-roundtable-prospect".

- Day -21: Send Wave 1 personal invitations to the top 12-15 targets via Loops. Personalize the first line for each recipient based on Attio notes, recent LinkedIn activity, or company news.

- Day -14: Send Wave 2 to remaining targets + follow-ups to Wave 1 non-responders. Include confirmed count: "8 leaders confirmed, including executives from [industry/company type]."

- Day -7: If under 8 confirmed, send urgent outreach to new Clay-sourced targets. If 10+ confirmed, stop invitations and activate waitlist.

- Day -3: Send attendee briefing packet: attendee list, discussion questions, meeting link.

- Day -1: Generate host briefing: one paragraph per attendee with background, recent activity, and a suggested personal question.

- Day +1: Auto-trigger `roundtable-attendee-nurture` drill. Generate discussion summary from Fireflies transcript. Update all Attio records.

**Human action required:** The host facilitates each discussion live. Everything else is agent-managed.

### 2. A/B test roundtable variables

Run the `ab-test-orchestrator` drill to systematically test one variable at a time across successive events:

**Variables to test (in priority order):**

1. **Topic category**: Which strategic theme drives the highest RSVP rate and post-event meeting conversion? Test at least 3 distinct categories over the first 4 events (e.g., technology strategy, organizational design, market positioning).

2. **Guest composition**: Does a vertical-specific group (all fintech CROs) produce better discussions than a cross-industry group? Compare meeting conversion rates.

3. **Invitation approach**: Test personal email from the host (Wave 1 style) vs host-endorsed broadcast (Wave 2 style) for the same contact tier. Measure RSVP rate by approach.

4. **Discussion format**: 45-minute open discussion vs 60-minute structured format with a brief guest speaker opening. Measure engagement tier distribution and meeting conversion.

5. **Day and time**: Test different slots (Tuesday 10am vs Thursday 2pm vs Friday 11am). Measure show rate by slot. Executive schedules make certain slots significantly better.

6. **Follow-up timing**: Does sending Tier 1 follow-up within 2 hours produce higher reply rates than within 4 hours? Test across 2 events.

For each test: define the hypothesis, success metric, and comparison methodology before running. After each event, log the result in Attio. After 4 events, compile a "winning formula" document.

### 3. Build cross-event analytics and guest pool management

Using PostHog and Attio, build:

**Cross-event funnel tracking:**
- Invited -> Confirmed -> Attended -> Engaged -> Meeting Booked -> Deal Created per event
- Series-level totals: cumulative pipeline, average meetings per roundtable, guest repeat rate, pipeline trend
- Guest freshness ratio per event (% new vs returning — target 50-70% new)

**Guest pool management system (n8n workflow, runs weekly):**
- **Always-on sourcing**: Weekly, use `clay-people-search` to find 5 new executive-level contacts based on recent signals (job changes, company funding rounds, LinkedIn posts on roundtable-relevant topics, conference appearances). Import to Attio with tag "exec-roundtable-prospect".
- **Engagement scoring**: After each roundtable, update every attendee's cumulative score in Attio. Factors: number of roundtables attended, average engagement tier, meeting conversion, referrals made, discussion quality (based on transcript analysis).
- **Graduated promotion**: Contacts who attend 3+ roundtables and engage highly should be flagged for a different relationship track: advisory board invitation, case study collaboration, or strategic partnership discussion.
- **Retirement**: Remove from active pool after 3 consecutive declines or 2 no-shows.

**Content flywheel:**
After each roundtable, produce derivative content from the discussion:
- Anonymized discussion insights document (share-worthy, not gated): "5 things C-suite leaders are saying about [topic]"
- LinkedIn post from the host referencing a theme from the discussion (without attribution): drives inbound interest in future events
- Targeted email to non-attendees in the ICP: "We recently hosted 10 [title]-level leaders to discuss [topic]. Here are 3 takeaways." CTA: "Want to join the next one?"

Each piece of derivative content serves as recruitment for the next event.

### 4. Evaluate against the threshold

After 6 months (6 events), evaluate:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Total executive attendees | >=80 | Sum of attendees across all events in Attio |
| Follow-up meetings booked | >=30 | Cal.com + email-confirmed meetings in Attio |
| Average show rate | >=75% | Mean show rate across all events |
| Cost per meeting | Trending down | Total tool costs / meetings booked |
| Guest pool depth | >=50 uninvited | Active Attio contacts with "exec-roundtable-prospect" tag |
| Referral rate | >=20% | Referrals received / total attendees |

**PASS**: Core metrics met (>=80 attendees, >=30 meetings). Proceed to Durable. The series is repeatable, automated, and producing predictable pipeline.

**FAIL**: Diagnose by metric:
- Low attendance (<80 total): Guest pool exhaustion or topic fatigue. Expand Clay sourcing criteria. Add new industry verticals. Increase the geographic scope.
- Low meeting conversion (<30 total): Discussions are interesting but not commercially productive. Shift topics closer to decision-relevant themes. Ensure Tier 1 follow-up references specific pain points from transcripts, not generic copy.
- Low show rate (<70%): Executive commitment is declining. Add a personal confirmation call from the host 5 days before the event. Reduce confirmed capacity to 10 to increase exclusivity.
- Shrinking guest pool: Sourcing cadence is too slow or retirement rules are too aggressive. Double the Clay weekly sourcing volume. Relax retirement to 4 consecutive declines.

## Time Estimate

- Series automation setup (n8n workflows, Clay integration, Loops sequences, topic calendar): 10 hours
- A/B test planning and implementation: 4 hours
- Guest pool management setup: 3 hours
- Per-event agent effort (guest curation, invitations, briefings, follow-up, analysis): 5 hours x 6 events = 30 hours
- Per-event human effort (facilitation only): 1 hour x 6 events = 6 hours
- Cross-event analysis and optimization: 4 hours
- Content derivative creation: 3 hours (spread across events)
- **Total: ~60 hours over 6 months** (split: ~50 hours agent, ~10 hours human)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM, guest pool, event lists, deal tracking | Free (3 users) or $29/user/mo Plus — [attio.com](https://attio.com) |
| Fireflies.ai | Roundtable transcription | Pro $18/user/mo (unlimited transcription) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Loops | Invitation sequences, reminders, nurture | $49/mo (up to 5,000 contacts) — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Event tracking, funnels, cross-event analytics | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Series automation, guest curation, monitoring | Self-hosted free or Cloud Starter EUR24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Clay | Net-new executive prospect sourcing | $185/mo Launch (2,500 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| Cal.com | Meeting booking CTA | Free tier — [cal.com/pricing](https://cal.com/pricing) |
| Zoom / Google Meet | Host the roundtable | Free tier or Zoom Pro $13.33/mo — [zoom.us/pricing](https://zoom.us/pricing) |

**Estimated play-specific cost at Scalable: $250-430/mo** (Fireflies Pro + Loops + Clay + optional Attio Plus + optional n8n Cloud)

## Drills Referenced

- the roundtable series automation workflow (see instructions below) — automate the full bi-monthly series: topic calendar, guest curation engine, invitation scheduling, cross-event analytics, and guest pool management
- `ab-test-orchestrator` — systematically test topic category, guest composition, invitation approach, discussion format, timing, and follow-up variables across events
