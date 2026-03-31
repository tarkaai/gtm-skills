---
name: micro-roundtables-smoke
description: >
  Micro-Roundtable — Smoke Test. Host a single invite-only roundtable discussion
  with 5-10 solution-aware execs to test whether intimate peer conversations yield
  follow-up meetings and justify the format. No tooling budget. Manual execution.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Smoke Test"
time: "4 hours over 1 week"
outcome: "≥ 6 attendees and ≥ 2 follow-up meetings booked within 2 weeks"
kpis: ["RSVP rate (target ≥ 40%)", "Show rate (target ≥ 75%)", "Meeting conversion rate (target ≥ 25% of attendees)"]
slug: "micro-roundtables"
install: "npx gtm-skills add marketing/solution-aware/micro-roundtables"
drills:
  - icp-definition
  - roundtable-pipeline
  - threshold-engine
---

# Micro-Roundtable — Smoke Test

> **Stage:** Marketing > SolutionAware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

Prove that hosting a small, invite-only roundtable discussion with 5-10 solution-aware execs produces follow-up meetings. This is a manual test — the agent prepares invitations, guest lists, and briefings, but the host facilitates the live discussion. If a single roundtable with 6+ attendees yields 2+ meetings, the format justifies investing in automation at Baseline.

Pass: 6 or more attendees AND 2 or more follow-up meetings booked within 2 weeks of the event.
Fail: Fewer than 6 attendees OR fewer than 2 meetings after 2 weeks.

## Leading Indicators

- 8+ RSVPs confirmed by Day -3 (signals the topic and guest profile are right)
- At least 1 attendee asks a question or makes a statement that reveals a pain point related to your product domain during the discussion (signals the topic creates natural openings)
- At least 1 attendee replies to the follow-up email within 24 hours (signals the discussion created genuine connection)

## Instructions

### 1. Define your roundtable ICP and topic

Run the `icp-definition` drill to define who should attend. For this play, add two extra requirements:

- **Seniority filter**: Attendees must be VP+, Director+, or Founders. Roundtables with mixed seniority levels produce shallow discussions because junior people defer to senior people.
- **Peer compatibility**: All attendees should be at roughly the same company stage and size. A Series A founder and a Fortune 500 VP will not have a productive peer conversation.

Choose a discussion topic that meets three criteria: (1) peer-relevant — something execs discuss with peers but rarely get honest answers about, (2) non-promotional — about a problem space, not your product, (3) opinionated — reasonable people should disagree.

Write 3 discussion questions and store them in Attio as a note.

### 2. Build a guest list of 15-20 targets

Manually search Attio, LinkedIn, and your network for 15-20 people matching your roundtable ICP. You need 2-3x your target attendance to account for declines. For each target, record:

- Name, email, company, role
- Why they would care about this topic (a recent post, a company initiative, a known challenge)
- Whether they compete with any other invitee (never put competitors in the same session)

Use the `attio-contacts` fundamental to log each person in Attio with tag "roundtable-smoke-invited".

### 3. Send personal invitations

Run the `roundtable-pipeline` drill. At Smoke level, send invitations manually from the host's email. Each invitation must include:

- The format: "small group of 8-10 [role] leaders, off-the-record discussion, no presentations"
- The topic and 1 discussion question as a teaser
- Date, time (45-60 minutes), and video link (Zoom free tier or Google Meet)
- A direct reply-to-RSVP CTA: "Reply 'in' to confirm your spot"

Send in two waves: top 10 targets on Day -21, remaining targets on Day -14. If under 8 confirmed by Day -7, send a follow-up with "3 spots remaining" urgency.

**Human action required:** The host must send the invitations from their personal email. The agent drafts the copy, but the host sends it.

### 4. Prepare and execute the roundtable

Run the `roundtable-pipeline` drill steps 5-7 for execution and data capture.

3 days before: send confirmed attendees the attendee list (first names + companies only), the 3 discussion questions, and the join link.

1 hour before: send a reminder with just the join link.

**Human action required:** The host facilitates the discussion live. Open with a 2-minute frame: "This is off the record, no pitches, pure peer discussion." Start with the easiest question. Save the provocative question for when the group is warmed up. Call on quiet participants by name. Target 45-60 minutes. End with: "What was the most surprising thing you heard today?"

If Fireflies.ai is available (free tier: 800 min/month), connect it for transcription. If not, the host takes manual notes on who said what.

### 5. Follow up within 24 hours

Within 4 hours of the event, send a personal follow-up email to each attendee. Reference something specific they said during the discussion. Include:

- A 3-5 bullet point discussion summary
- For attendees who expressed a relevant pain point: "I'd love to continue this conversation 1:1 — here are a few times: [provide 3 specific slots or a Cal.com link]"
- For all others: "Thanks for the great discussion. I'll keep you posted on the next one."

Log each attendee in Attio: engagement level (high/medium/low), key opinions expressed, follow-up interest signals.

### 6. Evaluate results after 2 weeks

Count: invitations sent, RSVPs confirmed, attendees, follow-up meetings booked. Compute RSVP rate, show rate, and meeting conversion rate.

Run the `threshold-engine` drill to evaluate:

- **PASS (≥ 6 attendees AND ≥ 2 meetings):** The format works. Document which topic angle and guest profile drove the best engagement. Proceed to Baseline.
- **MARGINAL (6+ attendees but only 1 meeting):** The event format works but the follow-up needs improvement. Review: did you reference specific discussion points in follow-up emails? Did you follow up fast enough? Adjust and re-run.
- **FAIL (< 6 attendees):** Diagnose: Was the guest list wrong (wrong ICP)? Was the topic wrong (not opinionated enough)? Was the invitation copy weak (not enough exclusivity)? Fix the weakest link and re-run once. If the second run also fails, this motion may not work for your market.

## Time Estimate

- ICP definition and topic selection: 1 hour
- Guest list building (manual): 1 hour
- Invitation copywriting and sending: 30 minutes
- Event preparation (briefing, logistics): 30 minutes
- Facilitating the roundtable (live): 1 hour
- Follow-up emails and data logging: 30 minutes
- Total: ~4.5 hours of active work spread over 1-2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Log invitees, track RSVPs and engagement | Free for up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| Cal.com | Booking link for follow-up meetings | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Zoom / Google Meet | Host the roundtable | Free tier (40-min limit on Zoom free; Google Meet unlimited for Google Workspace users) |
| Fireflies.ai | Transcription (optional at Smoke) | Free plan: 800 min/month ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |

**Estimated monthly cost for Smoke:** $0

## Drills Referenced

- `icp-definition` — define the target guest profile, seniority filter, and peer compatibility criteria
- `roundtable-pipeline` — plan invitees, execute the roundtable, capture discussion insights
- `threshold-engine` — evaluate results against the pass threshold and decide next action
