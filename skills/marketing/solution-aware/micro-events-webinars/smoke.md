---
name: micro-events-webinars-smoke
description: >
  Micro-Event or Webinar — Smoke Test. Host one small webinar (20-50 attendees)
  on a topic at the intersection of your expertise and your ICP's pain points.
  Validate that you can drive registrations, achieve a viable show rate, and
  generate at least one qualified meeting from a single session.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: ">=15 registrations, >=30% show rate, >=1 meeting booked within 2 weeks"
kpis: ["Registrations", "Show rate", "Meetings booked"]
slug: "micro-events-webinars"
install: "npx gtm-skills add marketing/solution-aware/micro-events-webinars"
drills:
  - icp-definition
  - webinar-pipeline
  - threshold-engine
---

# Micro-Event or Webinar — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Confirm that your target audience will register for a webinar on your chosen topic
- Achieve a show rate that proves registrant commitment (>=30%)
- Generate at least 1 qualified meeting from attendees within 2 weeks of the event
- Validate the topic-audience fit before investing in automation or recurring events

## Leading Indicators

- Registration page conversion rate >25% from direct traffic
- Registrations reach 15+ at least 3 days before the event (not last-minute panic)
- At least 3 attendees ask questions or engage in chat during the session
- At least 2 attendees click the post-event CTA (book a call, try product, download resource)

## Instructions

### 1. Define your webinar ICP and topic

Run the `icp-definition` drill to document who should attend. Then select a topic that meets three criteria: (a) it addresses a top-3 pain point for your ICP, (b) you have unique expertise or data on this topic, (c) it naturally leads to a conversation about your product without being a product pitch. Write a one-sentence benefit statement: "After this session, you will be able to [specific outcome]."

### 2. Set up the webinar infrastructure

Run the `webinar-pipeline` drill to configure the event end to end:

- Create a registration page with: benefit-focused headline, 3 bullet points on what attendees learn, speaker bio, date/time with timezone, and a simple form (name, email, company, role)
- Set up a webinar platform — use Zoom free tier (up to 100 participants, 40-min limit on free) or Google Meet (no participant limit, no time limit with Google Workspace). For recording and higher production quality, use Riverside ($19/mo Standard plan)
- Configure email confirmations and a single reminder (1 day before) via Loops
- Create an Attio list for registrants with fields: name, email, company, role, registered_date, attended (boolean), engaged (boolean)

### 3. Promote the event manually

**Human action required:** This is a smoke test — promotion is manual, not automated.

- Send personal emails or LinkedIn messages to 30-50 people in your network who match the ICP. Personal invites convert 3-5x better than broadcast emails at this stage.
- Post the event on LinkedIn with a hook that leads with the problem, not the event. Example: "Most [ICP role] struggle with [pain point]. I'm running a 30-minute session on [specific solution approach] next [day]."
- If you have an existing email list, send one targeted invitation via Loops to the most relevant segment using the `webinar-pipeline` drill's promotion step.

### 4. Execute the webinar

**Human action required:** You deliver the content live.

- Start on time. Open with a hook or surprising data point, not housekeeping.
- Share the agenda in 30 seconds. Keep the session to 30-45 minutes total.
- Encourage chat participation early — ask a poll question or "where are you joining from?" in the first 2 minutes.
- Reserve 25% of the time for Q&A. This is where the highest-intent engagement happens.
- End with a clear, single CTA: "If you want to explore how this applies to your situation, book a 15-minute call here." Share the Cal.com link in chat.

### 5. Execute basic follow-up

Within 24 hours of the event:

- Send an email to attendees: recording link (if recorded), 3 key takeaways, and the CTA link
- Send an email to no-shows: recording link with "Sorry we missed you" framing, and the same CTA
- For anyone who asked a question during Q&A, send a personal email or LinkedIn message referencing their question and offering a call

Log all follow-up actions in Attio. Tag attendees who clicked the CTA or replied.

### 6. Evaluate against the threshold

Run the `threshold-engine` drill to measure:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Registrations | >=15 | Count of Attio registrant list |
| Show rate | >=30% | Attendees / Registrations |
| Meetings booked | >=1 | Cal.com bookings within 14 days of event |

**PASS**: All three metrics met. Proceed to Baseline. The topic and format work — now add automation.

**FAIL**: Diagnose which metric missed:
- Low registrations (<15): Topic not compelling enough, or promotion reach too narrow. Try a different topic or expand your invite list.
- Low show rate (<30%): Registrants not committed. Check: was the event time convenient? Were reminders sent? Was the value proposition clear?
- Zero meetings: Attendees interested but CTA not compelling. Review your post-event follow-up and CTA clarity.

## Time Estimate

- Topic selection and ICP definition: 30 minutes
- Registration page and infrastructure setup: 45 minutes
- Promotion (manual outreach): 30 minutes
- Event delivery: 45 minutes
- Follow-up emails and logging: 30 minutes
- **Total: ~3 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Zoom | Webinar platform | Free tier: 100 participants, 40-min limit |
| Google Meet | Webinar platform (alternative) | Free with Google Workspace |
| Riverside | Recording + production (optional) | $19/mo Standard — [riverside.com/pricing](https://riverside.com/pricing) |
| Cal.com | Meeting booking CTA | Free tier: 1 user, unlimited event types — [cal.com/pricing](https://cal.com/pricing) |
| Loops | Confirmation + reminder emails | Free tier: 1,000 contacts, 4,000 sends/mo — [loops.so/pricing](https://loops.so/pricing) |
| Attio | Registrant tracking | Free tier: up to 3 users — [attio.com](https://attio.com) |

**Estimated play-specific cost at Smoke: $0-19/mo** (free if using Zoom/Meet + free tiers)

## Drills Referenced

- `icp-definition` — define who should attend and what pain points to address
- `webinar-pipeline` — set up registration, promotion, execution, and follow-up
- `threshold-engine` — evaluate pass/fail against registration, show rate, and meeting targets
