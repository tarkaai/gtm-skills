---
name: partnerships-warm-intros-baseline
description: >
  Partnerships & Warm Intros — Baseline Run. Systematize warm intro requests with tracked events,
  formalized ask templates, and a meeting booking flow. First always-on automation: CRM logging
  and PostHog tracking run continuously while you execute intro requests weekly.
stage: "Sales > Qualified"
motion: "PartnershipsWarmIntros"
channels: "Other"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 6 intros received and ≥ 4 meetings booked over 2 weeks"
kpis: ["Intro requests sent", "Intros received", "Meetings booked from intros", "Request-to-intro rate", "Intro-to-meeting rate"]
slug: "partnerships-warm-intros"
install: "npx gtm-skills add sales/qualified/partnerships-warm-intros"
drills:
  - warm-intro-request
  - posthog-gtm-events
  - meeting-booking-flow
---

# Partnerships & Warm Intros — Baseline Run

> **Stage:** Sales > Qualified | **Motion:** PartnershipsWarmIntros | **Channels:** Other

## Outcomes

Prove that warm intros produce repeatable results with proper measurement. At Baseline, you instrument everything in PostHog and Attio, formalize your ask templates, and connect a meeting booking flow. The agent runs tracking continuously; you execute the intro requests.

Pass threshold: **>= 6 intros received AND >= 4 meetings booked over 2 weeks.**

## Leading Indicators

- Request-to-intro rate by connector (target: >40% average across all connectors)
- Intro-to-meeting rate (target: >60%)
- Average days from request to intro (target: <4 days)
- Meeting show rate from warm intros (target: >85%)
- Connector re-engagement rate (target: >50% of Smoke connectors accept a second ask)

## Instructions

### 1. Configure partnership tracking

Run the `posthog-gtm-events` drill to set up these custom events in PostHog:

| Event Name | Trigger | Properties |
|-----------|---------|------------|
| `warm_intro_request_sent` | Agent logs request in Attio | `connector_name`, `target_name`, `channel`, `ask_template_id` |
| `warm_intro_received` | Connector makes the intro | `connector_name`, `target_name`, `days_to_intro` |
| `warm_intro_meeting_booked` | Meeting scheduled from intro | `connector_name`, `target_name`, `meeting_type`, `days_to_meeting` |
| `warm_intro_meeting_held` | Meeting completed | `connector_name`, `target_name`, `outcome` (discovery/demo/no-show/declined) |
| `warm_intro_deal_created` | Deal created from meeting | `connector_name`, `target_name`, `deal_value` |

Build a PostHog funnel: `warm_intro_request_sent` -> `warm_intro_received` -> `warm_intro_meeting_booked` -> `warm_intro_meeting_held` -> `warm_intro_deal_created`. Save as "Warm Intro Funnel — Baseline."

### 2. Formalize the intro request process

Run the `warm-intro-request` drill with these Baseline-specific additions:

**Create 3 ask templates** tailored to different connector types:

- **Template A — Advisor/Investor:** Reference the advisory relationship. Lead with how the intro benefits the target. Include a one-line forwardable blurb.
- **Template B — Customer/Partner:** Reference your shared work. Lead with social proof (what you delivered for the connector). Include a one-line forwardable blurb.
- **Template C — Weak Tie:** Reference the specific context you share (event, community, mutual connection). Lead with what you can offer the target. Include a one-line forwardable blurb.

Store templates in Attio as note templates or in a shared document the agent can reference. Tag each outgoing request with the template ID so PostHog tracks which templates produce the highest intro rate.

**Expand your connector list to 20+.** Pull in connectors from Smoke who responded (proven willingness) plus new connectors identified by reviewing your LinkedIn connections against your target list. For each new connector, check mutual connections with your target prospects using the `warm-intro-request` drill's connection mapping step.

### 3. Set up the meeting booking flow

Run the `meeting-booking-flow` drill to create:

- A Cal.com event type specifically for warm intro meetings: "Warm Intro — Discovery" (30 min)
- UTM-tagged booking links: `?utm_source=warm_intro&utm_medium=partner&utm_campaign=partnerships-warm-intros&utm_content={connector_slug}`
- n8n workflow: when a Cal.com booking fires with `utm_source=warm_intro`, automatically create an Attio deal at "Meeting Booked" stage, link to the connector record, and fire the `warm_intro_meeting_booked` PostHog event
- Automated pre-meeting prep: n8n pulls the target's company data from Attio and sends you a brief 1 hour before the meeting

### 4. Execute intro requests at Baseline volume

Send 15-20 intro requests over 2 weeks (roughly 2 per day). For each request:

1. Select the best connector-target pair from your mapped list
2. Choose the appropriate ask template (A, B, or C)
3. Personalize the template with specific context (why this target, why now)
4. Send via the connector's preferred channel
5. Log in Attio and fire the `warm_intro_request_sent` PostHog event

**Human action required:** Send intro requests personally. At Baseline, the agent handles tracking and booking infrastructure, but the asks themselves must come from you.

Follow up on pending requests after 5 days with a single gentle nudge. Never follow up more than once.

### 5. Evaluate against threshold

After 2 weeks, check the PostHog funnel and Attio records:

- **Intro requests sent:** >= 15 (input volume)
- **Intros received:** >= 6 (pass threshold)
- **Meetings booked:** >= 4 (pass threshold)
- **Request-to-intro rate:** Track by connector and by template
- **Intro-to-meeting rate:** Track overall and by connector

**PASS (>= 6 intros AND >= 4 meetings):** Document:
- Which connectors had the highest intro rate
- Which ask templates performed best
- Average time-to-intro and time-to-meeting
- Any patterns in which targets converted vs. did not
Proceed to Scalable.

**FAIL:** Diagnose using PostHog funnel:
- Drop-off at request -> intro: Improve ask quality, try different connectors, or change the value proposition to the target
- Drop-off at intro -> meeting: Improve follow-up speed and meeting positioning after the intro
- Insufficient request volume: Expand connector list or increase request cadence

## Time Estimate

- 3 hours: Set up PostHog events, Cal.com booking flow, n8n automations
- 6 hours: Craft templates, send 15-20 requests over 2 weeks, handle intros
- 2 hours: Follow up on pending requests, book meetings, log outcomes
- 1 hour: Evaluate results, document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — connector records, target records, deal tracking | Free for 3 users; $29/user/mo Plus ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Event tracking — warm intro funnel, per-connector metrics | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Cal.com | Meeting booking with UTM tracking | Free for 1 user ([cal.com/pricing](https://cal.com/pricing)) |
| n8n | Automation — booking-to-CRM sync, pre-meeting prep | Free self-hosted; Cloud from ~$24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated Baseline cost: $0-29/mo** (free tiers for PostHog, Cal.com, n8n self-hosted; Attio free or $29/user if >3 users)

## Drills Referenced

- `warm-intro-request` — formalized intro request process with templates and connection mapping
- `posthog-gtm-events` — warm intro event taxonomy and funnel tracking
- `meeting-booking-flow` — Cal.com booking with UTM attribution, CRM sync, and pre-meeting prep
