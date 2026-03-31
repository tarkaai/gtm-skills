---
name: executive-roundtables-baseline
description: >
  Executive Roundtables — Baseline Run. Run 3 roundtables over 8 weeks with
  automated invitation ops, Fireflies transcription, tiered post-event nurture
  sequences, and PostHog tracking across the full executive engagement funnel.
  Validate repeatable demand and conversion at C-level.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Baseline Run"
time: "18 hours over 8 weeks"
outcome: ">=25 executive attendees and >=10 follow-up meetings across 3 roundtables in 8 weeks"
kpis: ["RSVP rate per event", "Show rate per event", "Meeting conversion rate", "Nurture reply rate by tier"]
slug: "executive-roundtables"
install: "npx gtm-skills add marketing/solution-aware/executive-roundtables"
drills:
  - roundtable-pipeline
  - posthog-gtm-events
  - roundtable-attendee-nurture
---

# Executive Roundtables — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Prove that executive roundtable demand is repeatable across 3 events (not a one-time fluke from Smoke)
- Establish automated post-event nurture that converts high-engagement executives to pipeline without manual follow-up for every attendee
- Build the PostHog event tracking foundation for all future measurement and optimization of the roundtable funnel
- Identify which topics, guest profiles, and facilitation styles produce the highest meeting conversion at C-level
- Generate a growing guest pool: each roundtable should produce 2-3 referrals or introductions to new executive prospects

## Leading Indicators

- Second roundtable RSVP rate within 80% of the first (demand holds at this seniority level)
- Tier 1 nurture reply rate >40% (high-engagement execs respond to personalized follow-up)
- At least 2 meetings booked from automated nurture sequences (not only from manual host follow-up)
- At least 1 attendee proactively refers a peer for the next roundtable (organic demand signal)
- Discussion summary email open rate >70% (content is valued beyond the live event)

## Instructions

### 1. Configure executive roundtable event tracking

Run the `posthog-gtm-events` drill to implement the roundtable event taxonomy in PostHog:

- `exec_roundtable_invited` — invitation sent (properties: roundtable_slug, contact_id, wave_number, invitation_channel)
- `exec_roundtable_confirmed` — RSVP received (properties: roundtable_slug, contact_id, title, company_size)
- `exec_roundtable_reminded` — reminder sent (properties: roundtable_slug, reminder_type)
- `exec_roundtable_attended` — joined the live session (properties: roundtable_slug, contact_id, duration_minutes)
- `exec_roundtable_engaged` — spoke during discussion (properties: roundtable_slug, contact_id, engagement_level, pain_signal_detected)
- `exec_roundtable_summary_sent` — discussion summary email sent (properties: roundtable_slug, tier)
- `exec_roundtable_summary_opened` — summary email opened (properties: roundtable_slug, tier)
- `exec_roundtable_nurture_sent` — nurture email sent (properties: roundtable_slug, tier, sequence_step)
- `exec_roundtable_nurture_replied` — executive replied to nurture (properties: roundtable_slug, tier)
- `exec_roundtable_meeting_booked` — meeting booked from roundtable funnel (properties: roundtable_slug, tier, source)

Build a PostHog funnel: `exec_roundtable_invited` -> `exec_roundtable_confirmed` -> `exec_roundtable_attended` -> `exec_roundtable_engaged` -> `exec_roundtable_nurture_replied` -> `exec_roundtable_meeting_booked`

### 2. Upgrade roundtable operations for repeatability

Run the `roundtable-pipeline` drill with these Baseline-level enhancements:

- **Fireflies.ai transcription**: Connect Fireflies to every roundtable session for automatic transcription and action item extraction. This replaces manual note-taking and ensures every attendee's contribution is captured verbatim.
- **Loops invitation sequences**: Move from manual host-sent emails to semi-automated sequences. The host still sends Wave 1 (top targets) personally, but Wave 2 and reminders run via Loops. Build templates: Wave 1 personal draft, Wave 2 broadcast, Day -7 reminder, Day -3 attendee briefing, Day -1 join link reminder.
- **Attio event tracking lists**: Create a standardized list template for each roundtable with fields: contact, title, company, company_size, invited_date, RSVP_status, attended, engagement_tier, pain_signals, meeting_booked, referral_made.
- **Discussion summary template**: Standardize the post-event summary format: 3-5 key themes, points of agreement, points of disagreement, surprising insights, open questions for the next session.

### 3. Build automated post-event nurture

Run the `roundtable-attendee-nurture` drill to create tiered follow-up:

After each roundtable, automatically segment confirmed invitees into three tiers based on Attio engagement data:

**Tier 1 — High engagement (spoke 3+ times, expressed a pain point):**
- Email 1 (within 4 hours): Reference a specific point they made. Attach the discussion summary. CTA: "I'd love to continue this 1:1 — [Cal.com link]"
- Email 2 (day 3): Share a resource directly relevant to the pain point they expressed. One-line note: "This reminded me of what you said about [specific thing]."
- Email 3 (day 7): Direct meeting request. Reference their specific situation from the discussion.

**Tier 2 — Medium engagement (attended, spoke 1-2 times):**
- Email 1 (within 6 hours): Share the discussion summary. Highlight 2-3 insights.
- Email 2 (day 10): Invite to the next roundtable. Frame as: "Based on the [topic] discussion, I think you'd find the next one on [next topic] particularly relevant."

**Tier 3 — No-show:**
- Email 1 (within 2 hours): 3 key takeaways (create FOMO). CTA: "Want me to save you a spot at the next one?"
- Email 2 (day 5): Full discussion summary. CTA: "Reply 'in' to secure a spot."

Configure n8n triggers: when a Tier 1 contact replies or books via Cal.com, auto-create an Attio deal with source "executive-roundtable" and notify the host.

### 4. Run 3 roundtables over 8 weeks

Execute a small series to validate repeatable demand at executive level:

**Roundtable 1 (week 1-2):** Use the topic and guest profile that passed Smoke. Focus on testing the new automation: do Loops sequences improve RSVP rates? Does Fireflies transcription improve follow-up quality?

**Roundtable 2 (week 4-5):** Test a different topic within the same ICP. Keep the seniority, company size, and industry constant. This isolates topic performance from guest profile performance.

**Roundtable 3 (week 7-8):** Test a different guest mix: either a different industry vertical, a different seniority band (VP vs C-suite), or a different company size range. This identifies which guest profile produces the highest meeting conversion.

Between events, track referrals: ask attendees who express high engagement, "Who else should be in the next conversation?" Log referrals in Attio.

**Human action required:** The host facilitates all 3 discussions live. The agent handles everything before and after.

### 5. Analyze cross-event performance

After all 3 roundtables complete and nurture windows close (14 days post-last-event), compare:

| Metric | RT 1 | RT 2 | RT 3 | Target |
|--------|------|------|------|--------|
| Invitations sent | ? | ? | ? | 20-25 per event |
| Confirmed | ? | ? | ? | 10-12 per event |
| Attended | ? | ? | ? | 8+ per event |
| Show rate | ? | ? | ? | >=75% avg |
| Tier 1 attendees | ? | ? | ? | >=3 per event |
| Tier 1 reply rate | ? | ? | ? | >=40% |
| Meetings booked | ? | ? | ? | >=10 total |
| Referrals received | ? | ? | ? | >=2 per event |

Identify: Which topic drove the highest engagement quality? Which guest profile converted best? Which invitation wave (personal vs broadcast) had the highest RSVP rate? Does the discussion summary email drive re-engagement?

### 6. Evaluate against the threshold

**PASS (all met):** >=25 total executive attendees across 3 events, >=10 follow-up meetings booked, >=75% average show rate. Proceed to Scalable. You have repeatable executive demand and working automation.

**FAIL**: Diagnose by metric:
- Low attendance (<25 total): Invitation pool too small or topic not compelling. Expand the guest list to 25-30 per event. Test more polarizing topics.
- Low show rate (<70%): Executive commitment is fragile. Add a personal confirmation call or video from the host 3 days before the event. Limit each event to 10 confirmed max to increase exclusivity pressure.
- Low meeting conversion (<10 total): Events attract senior people but follow-up does not convert. Review: are Tier 1 follow-ups sent within 4 hours? Do they reference specific discussion points? Is the CTA low-friction enough for executives?
- Low nurture reply rate: The automated emails feel generic. Increase personalization — insert specific quotes or positions from the transcript.

## Time Estimate

- PostHog event tracking setup: 2 hours
- Roundtable operations upgrade (Fireflies, Loops sequences, Attio templates): 2 hours
- Nurture automation build (n8n workflows, Loops sequences, Cal.com integration): 3 hours
- Per-event agent work (guest curation, invitations, briefings, follow-up): 3 hours x 3 events = 9 hours
- Per-event human work (facilitation): 1 hour x 3 events = 3 hours
- Cross-event analysis: 2 hours
- **Total: ~18 hours over 8 weeks** (split: ~15 hours agent, ~3 hours human)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM, event lists, engagement tracking, deal creation | Free for 3 users — [attio.com/pricing](https://attio.com/pricing) |
| Fireflies.ai | Roundtable transcription + action item extraction | Free plan: 800 min/month, or Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Loops | Invitation sequences, reminders, nurture emails | Free (up to 1,000 contacts) or $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Event tracking, funnels, dashboards | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Nurture automation workflows, triggers | Self-hosted free or Cloud Starter EUR24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Cal.com | Meeting booking CTA | Free tier — [cal.com/pricing](https://cal.com/pricing) |
| Zoom / Google Meet | Host the roundtable | Free tier — [zoom.us/pricing](https://zoom.us/pricing) |

**Estimated play-specific cost at Baseline: $0-70/mo** (Fireflies free tier + Loops free tier, or paid tiers if over limits)

## Drills Referenced

- `roundtable-pipeline` — plan invitees, send tiered invitations, execute the roundtable, capture discussion insights and generate summaries
- `posthog-gtm-events` — implement the executive roundtable event taxonomy for full-funnel measurement
- `roundtable-attendee-nurture` — automated post-event tiered follow-up that converts high-engagement executives to meetings
