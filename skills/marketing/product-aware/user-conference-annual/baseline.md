---
name: user-conference-annual-baseline
description: >
  Annual User Conference -- Baseline Run. Run your first full-production conference
  with automated registration ops, multi-channel promotion, post-event nurture
  sequences, and PostHog tracking across the complete attendee funnel. Validate
  repeatable demand and measurable pipeline generation.
stage: "Marketing > ProductAware"
motion: "MicroEvents"
channels: "Events"
level: "Baseline Run"
time: "30 hours over 6 weeks"
outcome: ">=150 registrations, >=55% show rate, >=15 expansion meetings booked within 30 days"
kpis: ["Total registrations", "Show rate", "Sessions per attendee", "Expansion meetings booked", "NPS score", "Follow-up reply rate"]
slug: "user-conference-annual"
install: "npx gtm-skills add marketing/product-aware/user-conference-annual"
drills:
  - conference-planning-pipeline
  - posthog-gtm-events
  - webinar-attendee-nurture
---

# Annual User Conference -- Baseline Run

> **Stage:** Marketing -> Product Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Scale from the Smoke Test's minimal event to a full-production conference with 150+ registrations
- Establish automated pre-event promotion, registration ops, and post-event nurture that run without manual intervention
- Build the PostHog event tracking foundation for all future measurement, attribution, and optimization
- Generate measurable expansion pipeline: 15+ meetings booked from conference attendees within 30 days
- Collect structured feedback (NPS) to guide next year's conference planning

## Leading Indicators

- Registration velocity matches or exceeds the week-by-week target curve (slow start, acceleration in final 3 weeks)
- At least 30% of registrations come from product-aware prospects (not just existing customers) -- validates the conference's reach beyond your base
- Automated reminder sequence improves show rate vs. Smoke (target: 55%+)
- Segmented post-event nurture generates replies from >=15% of active attendees
- Feedback survey completion rate >=25% (enough data to be actionable)

## Instructions

### 1. Configure conference event tracking

Run the `posthog-gtm-events` drill to implement the full conference event taxonomy in PostHog:

- `conference_page_viewed` -- registration page visit (properties: conference_slug, source_channel, utm_params)
- `conference_registered` -- form submitted (properties: conference_slug, company, role, company_size, segment [customer/prospect])
- `conference_reminder_sent` -- reminder email delivered (properties: conference_slug, reminder_number, days_before)
- `conference_attended` -- joined at least 1 session (properties: conference_slug, join_time, attendee_segment)
- `conference_session_attended` -- attended a specific session (properties: conference_slug, session_slug, session_type [keynote/case-study/workshop/panel])
- `conference_engaged` -- asked a question, responded to poll, or clicked CTA (properties: conference_slug, engagement_type, session_slug)
- `conference_recording_watched` -- watched a session replay (properties: conference_slug, session_slug, percent_watched)
- `conference_nurture_email_sent` -- follow-up email sent (properties: conference_slug, tier, sequence_step)
- `conference_nurture_reply_received` -- attendee replied to nurture (properties: conference_slug, tier)
- `conference_meeting_booked` -- expansion meeting booked from conference funnel (properties: conference_slug, tier, source)
- `conference_feedback_submitted` -- post-event survey completed (properties: conference_slug, nps_score, would_attend_again)

Build a PostHog funnel: `conference_page_viewed` -> `conference_registered` -> `conference_attended` -> `conference_session_attended` (2+) -> `conference_engaged` -> `conference_meeting_booked`

### 2. Build full-production conference operations

Run the `conference-planning-pipeline` drill with these Baseline-level enhancements:

**Registration upgrades:**
- Move to Riverside ($19/mo Standard) or Zoom Pro ($13.33/mo) for recording. Every session gets recorded for replay distribution and content repurposing.
- Build a dedicated conference landing page with: theme description, full agenda with session descriptions, speaker bios with photos, registration form, and FAQ section.
- Configure registration segmentation in Attio: tag registrants as `customer` or `prospect` based on CRM match. Track which customer tier they are on.

**Promotion upgrades:**
- Build the full 10-week automated promotion engine from `conference-planning-pipeline`: announcement wave (week -10), speaker spotlight wave (week -6), urgency wave (week -3), final push (week -1).
- Use Clay to find and invite 200-500 product-aware prospects: people who have visited your pricing page, signed up for a trial, or downloaded a resource but have not yet converted. These are your best non-customer conference targets.
- Build automated reminder sequences in Loops: 1 week before, 3 days before, 1 day before, 1 hour before. Each reminder re-sells a specific session's value.

**Agenda upgrades:**
- Expand to 6-8 sessions across a full day (virtual) or add a second half-day for in-person.
- Add interactive elements: live polls during keynotes, breakout discussion rooms after case studies, a networking segment.
- Add a "product roadmap" session -- this is the session customers value most and the best driver of expansion conversations.

**Human action required:** You still deliver keynotes and moderate sessions live. The agent handles everything before and after the event: promotion, registration ops, reminders, nurture, and follow-up.

**Speaker upgrades:**
- Recruit 2-3 customer speakers (vs. 1 in Smoke). Diversity of company size, industry, and use case makes the content more relevant to a broader audience.
- Add 1 external speaker: an industry analyst, thought leader, or partner executive. This adds credibility and draws registrants who are not yet in your ecosystem.

### 3. Build post-conference nurture automation

Run the `webinar-attendee-nurture` drill adapted for conference scale:

Immediately after the conference, classify every registrant into engagement tiers using Attio:

- **Tier 1 -- Power attendee (3+ sessions + engaged)**: Attended most sessions AND asked questions or interacted. Highest expansion intent.
- **Tier 2 -- Active attendee (2+ sessions)**: Attended multiple sessions but limited engagement. Showed commitment.
- **Tier 3 -- Light attendee (1 session)**: Dipped in for one session. Interested but not committed.
- **Tier 4 -- No-show**: Registered but did not attend. Still expressed interest via registration.

Build tier-specific nurture sequences in Loops:

**Tier 1 sequence (4 emails over 10 days):**
- Email 1 (within 4 hours): All recording links + personalized note referencing their engagement. CTA: "Book an expansion call to discuss how [feature previewed in roadmap session] applies to your account." Include Cal.com link with pre-populated context.
- Email 2 (day 3): Key takeaways document + the specific session recordings most relevant to their account (based on sessions they attended).
- Email 3 (day 6): Case study or resource that extends the conference theme. CTA: reply with their biggest takeaway or challenge.
- Email 4 (day 10): Direct meeting request. "We'd love to discuss your [specific plan tier] and whether [expansion feature] could help your team."

**Tier 2 sequence (3 emails over 10 days):**
- Email 1 (within 6 hours): All recording links + highlights document. CTA: "Which session resonated most? Reply and we'll send you deeper resources on that topic."
- Email 2 (day 4): Recording links for sessions they missed. "You caught [session X] -- here's what you missed in [session Y] that builds on the same theme."
- Email 3 (day 10): Expansion CTA + invite to an upcoming smaller event (webinar, workshop) as a bridge.

**Tier 3 sequence (2 emails over 7 days):**
- Email 1 (within 6 hours): All recording links + the 3 most-attended session highlights. CTA: watch another session recording.
- Email 2 (day 7): Feedback survey + soft CTA for a call.

**Tier 4 sequence (2 emails over 5 days):**
- Email 1 (within 2 hours): "Sorry we missed you" with recording links and highlights. CTA: watch recordings.
- Email 2 (day 5): Feedback survey (shorter version) + invite to the next event.

Configure n8n triggers: when any Tier 1 or Tier 2 contact replies, auto-create an Attio deal with source `conference-20XX` and notify the founder or account owner via Slack.

### 4. Collect and analyze feedback

Using a Tally form (configured in `conference-planning-pipeline`), send a feedback survey to all attendees 24 hours after the event:

- Overall satisfaction (1-10 NPS)
- Rate each session attended (1-5 stars)
- "What was the most valuable part of the conference?" (open text)
- "What topic should we cover next year?" (open text)
- "Would you attend again?" (yes/no/maybe)
- "Would you recommend this conference to a colleague?" (yes/no)

Fire `conference_feedback_submitted` in PostHog with: nps_score, session_ratings, would_attend_again, would_recommend.

Analyze: calculate NPS, identify top-rated and bottom-rated sessions, extract common themes from open-text responses. Store the analysis in Attio on the conference record.

### 5. Evaluate against the threshold

After the 30-day post-conference window closes, evaluate:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Total registrations | >=150 | Count of Attio conference registrant list |
| Show rate | >=55% | Attendees (joined >=1 session) / Registrations |
| Sessions per attendee | >=2.5 | Average across all attendees |
| Expansion meetings booked | >=15 | Cal.com bookings + email replies converted to meetings within 30 days |
| NPS score | >=40 | Calculated from feedback survey |
| Follow-up reply rate (Tier 1) | >=20% | Tier 1 replies / Tier 1 emails sent |

**PASS**: Core metrics met (registrations, show rate, meetings). Proceed to Scalable. You have a production-grade conference that generates measurable pipeline.

**FAIL**: Diagnose by metric:
- Low registrations: Promotion window too short, or theme not compelling enough for prospects. Extend promotion to 12+ weeks. Test a theme that addresses a trending industry pain point.
- Low show rate: Too many sessions or scheduling conflict. Survey no-shows. Consider splitting into 2 half-days. Add a stronger incentive for attendance (exclusive content, early access).
- Low meetings: Content too educational, not enough product connection. Add more product-focused sessions. Strengthen the expansion CTA in every session. Personalize Tier 1 follow-up with account-specific context.
- Low NPS: Execution quality issues. Review session ratings to find underperformers. Invest more in speaker prep and production quality.

## Time Estimate

- PostHog event tracking setup: 3 hours
- Conference operations build (registration, promotion engine, Loops sequences): 6 hours
- Speaker recruitment and coordination: 4 hours
- Content preparation and agenda design: 3 hours
- Promotion execution (email waves, LinkedIn posts, personal invites): 3 hours
- Conference delivery (live): 5 hours (including setup and teardown)
- Post-event nurture build and execution: 3 hours
- Feedback analysis and evaluation: 3 hours
- **Total: ~30 hours over 6 weeks** (4 weeks promotion + event week + 1 week follow-up)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Riverside | Conference recording + production | $19/mo Standard -- [riverside.com/pricing](https://riverside.com/pricing) |
| Zoom Pro | Virtual conference platform (alternative) | $13.33/mo -- [zoom.us/pricing](https://zoom.us/pricing) |
| Luma | Registration and event page | Free -- [lu.ma](https://lu.ma) |
| Tally | Registration form + feedback survey | Free -- [tally.so/pricing](https://tally.so/pricing) |
| Loops | Email invites, reminders, nurture sequences | Free tier or $49/mo (5,000 contacts) -- [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Event tracking + funnels | Free tier: 1M events/mo -- [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | Registrant tracking + deal creation | Free (3 users) or $29/user/mo Plus -- [attio.com](https://attio.com) |
| n8n | Registration webhooks + nurture automation | Self-hosted free or Cloud Starter EUR24/mo -- [n8n.io/pricing](https://n8n.io/pricing) |
| Clay | Prospect sourcing for invites | $185/mo Launch (2,500 credits) -- [clay.com/pricing](https://www.clay.com/pricing) |
| Cal.com | Expansion call booking CTA | Free tier -- [cal.com/pricing](https://cal.com/pricing) |

**Estimated play-specific cost at Baseline: $19-280/mo** (depends on Loops tier and whether you use Clay for prospect sourcing)

## Drills Referenced

- `conference-planning-pipeline` -- full-production conference operations: registration, promotion engine, speaker coordination, day-of logistics, follow-up
- `posthog-gtm-events` -- implement standard conference event taxonomy for measurement and attribution
- `webinar-attendee-nurture` -- automated post-conference segmented nurture sequences adapted for conference engagement tiers
