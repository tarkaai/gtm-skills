---
name: onboarding-webinar-series-baseline
description: >
  Live Onboarding Webinars — Baseline Run. Automate the promotion, registration,
  and post-webinar nurture pipeline. Run 2-4 webinars over 4 weeks. Validate that
  the activation lift holds with always-on automation handling everything except delivery.
stage: "Product > Onboard"
motion: "MicroEvents"
channels: "Product, Email, Events"
level: "Baseline Run"
time: "20 hours over 4 weeks"
outcome: ">=50% attendee activation rate sustained across 2+ webinars AND show rate >=35%"
kpis: ["Registration rate", "Show rate", "Attendee activation rate", "Post-webinar meeting booking rate", "Nurture reply rate by tier"]
slug: "onboarding-webinar-series"
install: "npx gtm-skills add product/onboard/onboarding-webinar-series"
drills:
  - webinar-attendee-nurture
  - posthog-gtm-events
---

# Live Onboarding Webinars — Baseline Run

> **Stage:** Product > Onboard | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Events

## Outcomes

Run 2-4 onboarding webinars over 4 weeks with automated promotion, registration, and tiered post-webinar nurture. The agent handles the full pipeline (invitation emails, reminders, attendee segmentation, follow-up sequences) while the human delivers the webinar content. Validate that the activation lift proven in Smoke holds at higher volume with automated operations. Pass threshold: >=50% attendee activation rate sustained across 2+ webinars AND show rate >=35%.

## Leading Indicators

- Automated invitation emails achieve >=30% open rate and >=8% click-to-register rate — confirms the promotion pipeline reaches the right users
- Reminder sequence (2-day + 1-hour) produces show rate >=35% — confirms the automation drives attendance
- Tier 1 (active attendees) reply rate >=30% on follow-up emails — confirms the nurture segmentation is working
- At least 2 meetings booked from Tier 1 attendees across 2 webinars — confirms the pipeline conversion path works
- Activation rate for no-shows who watch the recording >=30% — confirms async value capture works

## Instructions

### 1. Set up full event tracking

Run the `posthog-gtm-events` drill to instrument the complete webinar funnel. Create these PostHog events:

| Event | Trigger | Properties |
|-------|---------|------------|
| `webinar_invite_sent` | Invitation email sent | `webinar_slug`, `recipient_email`, `signup_days_ago` |
| `webinar_page_viewed` | Registration page loaded | `webinar_slug`, `utm_source` |
| `webinar_registered` | Registration form submitted | `webinar_slug`, `email`, `company`, `role` |
| `webinar_reminder_sent` | Reminder email sent | `webinar_slug`, `reminder_type` (2day/1hour) |
| `webinar_reminder_clicked` | Reminder link clicked | `webinar_slug`, `reminder_type` |
| `webinar_attended` | User joins the live session | `webinar_slug`, `email`, `join_time` |
| `webinar_question_asked` | User asks a question in chat | `webinar_slug`, `email` |
| `webinar_cta_clicked` | User clicks the in-session CTA | `webinar_slug`, `cta_type` |
| `webinar_nurture_email_sent` | Post-webinar email sent | `webinar_slug`, `tier`, `sequence_step` |
| `webinar_nurture_reply_received` | User replies to nurture email | `webinar_slug`, `tier` |
| `webinar_nurture_meeting_booked` | User books a follow-up meeting | `webinar_slug`, `tier` |
| `webinar_recording_watched` | User watches the recording | `webinar_slug`, `percent_watched`, `tier` |

Build a PostHog funnel: `webinar_invite_sent` -> `webinar_registered` -> `webinar_reminder_clicked` -> `webinar_attended` -> `webinar_question_asked` -> `webinar_nurture_reply_received` -> `webinar_nurture_meeting_booked`.

Create a PostHog dashboard with: registration funnel (bar), show rate per webinar (line), activation rate by attendance status (bar grouped by attended/no-show/control), and nurture performance by tier (table).

### 2. Automate promotion and registration

Build an n8n workflow that triggers 7 days before each scheduled webinar:

**Day -7: Invitation send.**
- Query Attio for users who signed up in the last 21 days and have NOT yet activated
- Exclude users who attended a previous webinar in the last 30 days (avoid fatigue)
- Send personalized invitation via Loops. Subject: "Get [product] set up in 30 minutes — live this [day]"
- Log `webinar_invite_sent` in PostHog for each recipient

**Day -2: Reminder 1.**
- Send reminder to all registrants who have not cancelled
- Subject: "Your live setup session is in 2 days — here's what to prepare"
- Include: pre-session checklist (log in, have a project/workspace ready), join link
- Log `webinar_reminder_sent` with `reminder_type: "2day"`

**Day 0, 1 hour before: Reminder 2.**
- Send final reminder with join link prominently displayed
- Subject: "Starting in 1 hour — join link inside"
- Log `webinar_reminder_sent` with `reminder_type: "1hour"`

Use the Cal.com registration page from Smoke. Add an Intercom in-app banner for users who are logged into the product and have not yet activated: "Live onboarding session this [day] — [register link]."

### 3. Build tiered post-webinar nurture

Run the `webinar-attendee-nurture` drill. Configure the four-tier segmentation:

- **Tier 1 — Active attendee:** Attended AND asked a question or clicked the in-session CTA. Highest intent.
- **Tier 2 — Passive attendee:** Attended but did not engage beyond watching.
- **Tier 3 — No-show:** Registered but did not attend.
- **Tier 4 — Late registrant:** Registered after the event (from replay promotion).

Build the n8n automation that:
1. Exports the attendee list from Riverside/Zoom within 2 hours of the event ending
2. Matches attendees against registrants in Attio
3. Assigns each registrant to a tier
4. Enrolls them in the corresponding Loops nurture sequence
5. Fires `webinar_nurture_email_sent` events in PostHog for each send

The drill specifies the email content and timing for each tier. Key details for onboarding webinars specifically:

- **Tier 1 follow-up** should reference the specific question the attendee asked. If they asked about a feature, link to the relevant help doc or offer a 15-minute 1:1 session via Cal.com.
- **Tier 2 follow-up** should include the recording timestamped to the Q&A section (this is the part they missed by not engaging).
- **Tier 3 follow-up** should include a Loom recording of the key 5-minute segment — not the full recording. Lower the ask.

### 4. Deliver the webinars

**Human action required:** Deliver 2-4 webinars over 4 weeks. Use the same workshop format from Smoke.

Between webinars, the agent should analyze Q&A patterns:
- Pull all `webinar_question_asked` events from PostHog
- Cluster questions by topic (integration setup, data import, team configuration, etc.)
- Identify the top 3 question themes
- Adjust the next webinar's content to address the most common questions proactively

This feedback loop means each successive webinar should have fewer stuck attendees and higher activation.

### 5. Track and measure across webinars

After each webinar's nurture window closes (14 days post-event), calculate:

| Metric | Target |
|--------|--------|
| Registration rate (registrations / invites) | >=15% |
| Show rate (attendees / registrations) | >=35% |
| Engagement rate (questions + CTA clicks / attendees) | >=25% |
| Attendee activation rate (7-day window) | >=50% |
| Tier 1 nurture reply rate | >=30% |
| Tier 2 nurture reply rate | >=15% |
| Meetings booked from nurture | >=2 per webinar |
| No-show recording watch rate | >=40% |

Compare metrics across the 2-4 webinars. Look for improvement or degradation trends.

### 6. Evaluate against threshold

Pass criteria:
- **Attendee activation rate >=50% sustained across 2+ webinars** — the webinar effect is repeatable, not a one-off
- **Show rate >=35%** — the automated promotion and reminder pipeline drives reliable attendance

If PASS: The webinar pipeline works as an always-on system. Proceed to Scalable to multiply frequency and automate series operations.

If FAIL on activation rate: Check whether the content addresses the actual activation action. Review PostHog session recordings from attendees who did NOT activate after the webinar. Where did they get stuck post-session?

If FAIL on show rate: Review reminder open rates. If reminders are opened but show rate is low, the timing or friction to join is the problem. Test a different day/time for the next webinar. If reminders are not opened, the subject lines or sender reputation need work.

## Time Estimate

- 3 hours: Set up PostHog event tracking, build the PostHog dashboard and funnels
- 3 hours: Build n8n promotion workflow (invitation, 2 reminders, in-app banner)
- 3 hours: Build the tiered nurture automation (n8n + Loops sequences + Attio tagging)
- 4 hours: Deliver 2-4 webinars (1 hour each, human action)
- 3 hours: Content iteration between webinars (analyze Q&A, adjust slides)
- 2 hours: Measure and analyze per-webinar metrics
- 2 hours: Final threshold evaluation and documentation

Total: ~20 hours spread over 4 weeks.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loops | Invitation emails, reminders, tiered nurture sequences | Free up to 1,000 contacts. Paid from $49/mo for 5,000 contacts. [Pricing](https://loops.so/pricing) |
| PostHog | Full-funnel event tracking, funnels, dashboards, cohort analysis | Free up to 1M events/mo. [Pricing](https://posthog.com/pricing) |
| Riverside | Webinar recording and production | Free: 2 hours. Standard: $19/mo. [Pricing](https://riverside.com/pricing) |
| Cal.com | Registration page and scheduling | Free for 1 user. [Pricing](https://cal.com/pricing) |
| Intercom | In-app webinar promotion banner | Essential: $29/seat/mo. [Pricing](https://www.intercom.com/pricing) |
| Loom | Short recording clips for Tier 3 no-show follow-up | Free: 25 videos. Business: $12.50/user/mo. [Pricing](https://www.loom.com/pricing) |

**Estimated monthly cost: $49-100/mo** (Loops paid plan if >1,000 contacts, Riverside Standard for recording quality. PostHog, Cal.com, and Loom free tiers likely sufficient.)

## Drills Referenced

- `webinar-attendee-nurture` — builds the tiered post-webinar nurture system that segments registrants by engagement level and runs differentiated follow-up sequences
- `posthog-gtm-events` — instruments the complete webinar funnel with PostHog events, funnels, and dashboards
