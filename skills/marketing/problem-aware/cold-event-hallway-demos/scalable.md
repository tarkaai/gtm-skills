---
name: cold-event-hallway-demos-scalable
description: >
  Event Hallway Demos — Scalable. Scale from ad-hoc event attendance to a systematic
  multi-city event circuit with automated scouting, pre-event outreach to targets,
  A/B-tested demo approaches, and a full follow-up machine.
stage: "Marketing > ProblemAware"
motion: "MicroEvents"
channels: "Other"
level: "Scalable"
time: "60 hours over 2 months"
outcome: ">= 40 demos, >= 12 meetings, and >= 3 pipeline deals across 8+ events in 2 months"
kpis: ["Demos given per event", "Demo-to-meeting rate", "Cost per meeting", "Pipeline generated ($)", "Events attended per month"]
slug: "cold-event-hallway-demos"
install: "npx gtm-skills add marketing/problem-aware/cold-event-hallway-demos"
drills:
  - event-scouting
  - hallway-demo-operations
  - follow-up-automation
  - ab-test-orchestrator
  - signal-detection
---

# Event Hallway Demos — Scalable

> **Stage:** Marketing > ProblemAware | **Motion:** MicroEvents | **Channels:** Other

## Outcomes

Scale from attending a few local events to running a systematic event circuit across multiple cities. The agent continuously scouts events, enriches attendee lists, sends pre-event outreach to warm targets before you arrive, and runs automated post-event follow-up. You test different demo approaches across events and identify the 10x lever: which event types, venues, conversation openings, and demo formats produce the most pipeline per hour invested. The goal is to turn event attendance into a predictable pipeline channel, not a one-off tactic.

## Leading Indicators

- Events scouted and scored per month >= 20 (the funnel of opportunities)
- Pre-event outreach response rate >= 15% (warming targets before arrival)
- Demos given per event trending up (improving conversation-to-demo rate)
- Demo-to-meeting rate >= 25% (demo quality improving from A/B testing)
- Cost per meeting trending down (better event selection = less wasted travel)
- Pipeline-to-travel-cost ratio >= 5:1 (each dollar of travel generates $5+ in pipeline)

## Instructions

### 1. Automate continuous event scouting

Run the `event-scouting` drill on a monthly cadence to maintain a rolling 90-day event calendar. Configure the agent to:
- Scout events in all target cities (expand beyond local to 2-3 additional markets)
- Auto-score every event using the scouting rubric (ICP density, venue accessibility, size, timing, cost)
- Auto-enrich attendee/speaker lists for events scoring 70+
- Push the scored calendar to Attio with expected ROI per event
- Alert you weekly with the top 5 upcoming events to consider

Run the `signal-detection` drill to add signal-based event prioritization: if a target account just raised funding, changed leadership, or posted relevant job openings AND someone from that account is speaking at an upcoming event, that event gets a priority boost.

### 2. Launch pre-event outreach

For each event you plan to attend, run pre-event outreach 7-10 days before the event:

Using `hallway-demo-operations` (pre-event step), identify the top 10 targets per event. Then send a personalized LinkedIn message or email:
- Reference the specific event and something about their role or company
- Mention you will be there and would love to grab 5 minutes to show them something relevant to [their pain point]
- Do NOT pitch the product in the message -- the goal is to schedule an in-person touchpoint, not a remote demo

Track pre-event outreach responses. People who agree to meet at the event are your highest-priority targets on event day.

### 3. A/B test demo approaches

Run the `ab-test-orchestrator` drill to systematically test variables across events:

**Experiment 1 — Demo length:** At Event A, lead with the 60-second pitch. At Event B, lead with the 3-minute demo. Compare demo-to-meeting conversion rates.

**Experiment 2 — Conversation opener:** Alternate between context-based openers ("What did you think of [session]?"), pain-based openers ("Are you dealing with [specific challenge]?"), and social openers ("Where are you joining from?"). Track which opener type leads to demos.

**Experiment 3 — CTA format:** Test QR code booking (scan and schedule) vs verbal booking ("Let me pull up my calendar") vs follow-up promise ("I will send you a link tonight"). Track which closes the most meetings.

**Experiment 4 — Follow-up timing:** For half your contacts, follow up within 4 hours. For the other half, follow up next morning. Compare response rates.

Log all experiment data in PostHog with variant tags. Each experiment needs 15+ observations per variant for a meaningful signal.

### 4. Build the follow-up machine

Run the `follow-up-automation` drill to create n8n workflows for post-event follow-up:

**Trigger 1 — Same-day hot follow-up:** When a conversation is logged with interest level 4-5, automatically:
- Create Attio deal at "Demo Given" stage
- Send personal email within 4 hours (template references event name and conversation topic, pulled from Attio notes)
- Queue LinkedIn connection request

**Trigger 2 — Next-day warm follow-up:** For interest level 3, send email at 9 AM next business day with a relevant resource and soft CTA.

**Trigger 3 — Week-after nurture:** For interest level 2, send a single touchpoint 7 days after the event: a piece of content relevant to the event topic, no sales ask.

**Trigger 4 — Meeting no-show:** If a booked meeting gets a no-show, auto-send a reschedule message 2 hours after the missed time.

**Trigger 5 — Post-meeting deal advance:** When a follow-up meeting happens (Cal.com marks it completed), update the Attio deal to "Meeting Completed" and create a task for next steps.

### 5. Scale to multi-city event circuit

With automation handling scouting, enrichment, and follow-up, increase event attendance to 2-3 events per week. Expand to new cities where your ICP concentrates. Use Baseline data to set minimum thresholds: only attend events scoring 70+ on the scouting rubric. Drop events that consistently underperform.

Consider deploying team members: share the demo kit, conversation framework, and logging process. The agent prepares per-event briefings for whoever is attending.

**Human action required:** Someone still attends events in person and runs conversations. The 10x is not removing the human -- it is ensuring every hour of human event time is maximally productive through better event selection, pre-warmed targets, and zero-effort follow-up.

### 6. Evaluate against threshold

Pass threshold: >= 40 demos given, >= 12 meetings booked, AND >= 3 pipeline deals created across 8+ events in 2 months.

If PASS: hallway demos are a predictable pipeline channel. You know which events work, which approaches convert, and the cost per meeting. Proceed to Durable.
If FAIL: review experiment results. If certain event types consistently perform, narrow focus. If the funnel breaks at a specific stage (lots of demos but no meetings), fix that stage before scaling further.

## Time Estimate

- 4 hours/month: event scouting review and calendar planning
- 2 hours per event: pre-event outreach and preparation
- 3-4 hours per event: attendance and execution
- 1 hour per event: post-event logging (follow-up is automated)
- 4 hours/month: experiment analysis and optimization

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Continuous event scouting and attendee enrichment | Growth: $495/mo (higher volume needed) (https://www.clay.com/pricing) |
| Attio | Contact/deal management, event records | Free or Plus depending on team size (https://attio.com/pricing) |
| Cal.com | Meeting booking with QR codes | Free tier (https://cal.com/pricing) |
| PostHog | Funnel analytics, experiment tracking | Free up to 1M events/mo (https://posthog.com/pricing) |
| Loops | Automated follow-up sequences | $49/mo for 1,000+ contacts (https://loops.so/pricing) |
| n8n | Follow-up automation workflows | Self-hosted free; Cloud from $24/mo (https://n8n.io/pricing) |
| Fireflies | Meeting transcription and action items | Pro: $10/user/mo annual (https://fireflies.ai/pricing) |

**Play-specific cost at Scalable level:** ~$550-600/mo (Clay Growth + Loops paid). Plus travel costs per event, which should decrease per-meeting as event selection improves.

## Drills Referenced

- `event-scouting` — continuous 90-day event calendar with auto-scoring and enrichment
- `hallway-demo-operations` — per-event execution with pre-event outreach addition
- `follow-up-automation` — n8n workflows for tiered post-event follow-up
- `ab-test-orchestrator` — systematic testing of demo approaches, openers, CTAs, and timing
- `signal-detection` — prioritize events where signal-hot accounts will be present
