---
name: webinar-series-program-baseline
description: >
  Educational Webinar Series — Baseline Run. Run 3 webinars over 6 weeks with
  proper analytics tracking and a tiered attendee nurture system to prove
  repeatable lead generation from events.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Content, Email"
level: "Baseline Run"
time: "18 hours over 6 weeks"
outcome: "≥100 registrations and ≥15 qualified leads across 3 webinars in 6 weeks"
kpis: ["Registrations per event", "Show rate", "Nurture reply rate by tier", "Meetings booked per event", "Registration-to-pipeline conversion rate"]
slug: "webinar-series-program"
install: "npx gtm-skills add marketing/solution-aware/webinar-series-program"
drills:
  - posthog-gtm-events
  - webinar-attendee-nurture
---

# Educational Webinar Series — Baseline Run

> **Stage:** Marketing → SolutionAware | **Motion:** MicroEvents | **Channels:** Events, Content, Email

## Outcomes

Run 3 webinars over 6 weeks (bi-weekly cadence) with full PostHog funnel tracking and a tiered post-event nurture system. Prove that webinars are a repeatable lead generation channel, not a one-off success. Pass threshold: ≥100 total registrations AND ≥15 qualified leads across the 3 events.

## Leading Indicators

- Event-over-event registration growth (event 2 registrations > event 1)
- Show rate holding steady or improving across events (target: ≥30%)
- Tier 1 attendees (asked questions) generating ≥20% reply rate from nurture
- Repeat registrants appearing by event 3 (signals community forming)
- Post-event recording consumption rate ≥40% among no-shows

## Instructions

### 1. Configure webinar funnel analytics

Run the `posthog-gtm-events` drill to set up the full webinar tracking funnel. Create these events:

- `webinar_page_viewed` — registration page loaded (properties: `webinar_slug`, `source_channel`)
- `webinar_registered` — form submitted (properties: `webinar_slug`, `registrant_email`, `company`, `role`)
- `webinar_reminder_clicked` — clicked join link from reminder email (properties: `webinar_slug`, `reminder_type`)
- `webinar_attended` — joined the live session (properties: `webinar_slug`, `duration_minutes`)
- `webinar_question_asked` — submitted a question or poll response (properties: `webinar_slug`, `question_text`)
- `webinar_nurture_email_sent` — follow-up email sent (properties: `webinar_slug`, `tier`, `sequence_step`)
- `webinar_nurture_reply_received` — reply to nurture email (properties: `webinar_slug`, `tier`)
- `webinar_meeting_booked` — meeting booked from webinar lead (properties: `webinar_slug`, `tier`, `days_since_event`)

Build a PostHog funnel: `webinar_page_viewed` → `webinar_registered` → `webinar_attended` → `webinar_question_asked` → `webinar_nurture_reply_received` → `webinar_meeting_booked`

Save this as "Webinar Series Funnel" dashboard.

### 2. Plan a 3-event series

Select 3 topics based on Smoke Test learnings. Each topic should address a different angle of your ICP's core problem:

- **Event 1**: The problem overview — "Why [ICP pain point] is getting worse" (broadest appeal, highest registration)
- **Event 2**: A specific solution approach — "How to [specific tactic] for [ICP outcome]" (more qualified audience)
- **Event 3**: Advanced/implementation — "Building [specific system] step by step" (highest intent, most qualified)

This progression filters: event 1 attracts the curious, event 3 attracts the committed. Schedule bi-weekly.

For each event, use the `webinar-pipeline` drill from Smoke level (already proven) to handle registration, promotion, and logistics.

### 3. Deploy tiered attendee nurture

Run the `webinar-attendee-nurture` drill after each event. This drill segments every registrant into 4 tiers based on engagement:

- **Tier 1 (Active attendee)**: Attended AND asked a question. Receives personalized follow-up within 4 hours including a Loom clip answering their question. 3-email sequence over 7 days ending with a direct meeting request.
- **Tier 2 (Passive attendee)**: Attended but did not engage. Receives recording + key takeaways. 3-email sequence over 10 days with softer CTAs.
- **Tier 3 (No-show)**: Registered but did not attend. Receives recording with "Sorry we missed you" framing. 2-email sequence over 7 days.
- **Tier 4 (Late registrant)**: Registered after the event. Receives recording + next event invite. 2-email sequence over 5 days.

The drill configures all sequences in Loops, builds n8n automation triggers for tier assignment, and creates escalation workflows that auto-create Attio deals when Tier 1 or Tier 2 contacts reply.

### 4. Run the 3-event series and track cross-event patterns

Execute all 3 events. After each event, the `webinar-attendee-nurture` drill runs the full post-event workflow. Between events, analyze:

- Which promotion channel drove the most registrations? (Check `source_channel` property on `webinar_registered` events)
- Which topic had the highest show rate?
- Which tier produced the most meetings booked?
- Are any registrants appearing in multiple events? (These are your highest-intent leads — prioritize them.)

Log all cross-event insights as Attio notes.

### 5. Evaluate against threshold

After the 3rd event's nurture window closes (14 days post-event), measure cumulative results:

- Total registrations across 3 events (target: ≥100)
- Total qualified leads across 3 events (target: ≥15)
- Show rate trend (flat or improving = healthy)
- Nurture reply rate by tier (benchmark: Tier 1 >30%, Tier 2 >15%, Tier 3 >5%)
- Meetings booked per event (benchmark: ≥5)

**PASS → Scalable**: Hit both thresholds and show rate is stable. Document the winning topic formula, best promotion channels, and nurture sequence performance.
**MARGINAL → Optimize**: Close but inconsistent (e.g., one event hit targets, two missed). Stay at Baseline for one more 3-event cycle. Focus on the weakest link: registration, attendance, or conversion.
**FAIL → Iterate or Pivot**: Consistently below thresholds after two cycles. Either change the event format fundamentally (switch from webinar to workshop, for example) or try a different play.

## Time Estimate

- PostHog event setup and funnel: 2 hours
- Series planning (3 topics, scheduling): 1 hour
- Per-event execution (×3): registration/promotion (2 hours) + delivery (1 hour) + nurture setup (1.5 hours) = 4.5 hours × 3 = 13.5 hours
- Cross-event analysis and threshold evaluation: 1.5 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Riverside | Webinar recording + production quality | ~$25/mo (Standard plan) — https://riverside.fm/pricing |
| Loops | Nurture email sequences (4 tiers) | Free up to 1,000 contacts; $49/mo for higher volume — https://loops.so/pricing |
| PostHog | Funnel analytics + event tracking | Free up to 1M events — https://posthog.com/pricing |
| Attio | CRM for lead tracking + segmentation | Free up to 3 seats — https://attio.com/pricing |
| Loom | Personalized follow-up video clips | Free (25 videos); $15/mo for Business — https://www.loom.com/pricing |
| Cal.com | Registration and scheduling | Free tier — https://cal.com/pricing |
| n8n | Automation for nurture triggers | Free self-hosted; $20/mo cloud — https://n8n.io/pricing |

**Estimated play-specific cost: $25-90/mo** (Riverside + optional Loom Business + optional n8n cloud)

## Drills Referenced

- `posthog-gtm-events` — configures the full webinar funnel tracking in PostHog so every step from page view to meeting booked is measured
- `webinar-attendee-nurture` — builds the 4-tier post-event follow-up system that segments registrants by engagement and runs differentiated nurture sequences
