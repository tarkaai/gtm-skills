---
name: user-conference-annual-smoke
description: >
  Annual User Conference -- Smoke Test. Host a single virtual half-day
  conference for your existing customers and product-aware prospects.
  Validate that you can drive registrations from your base, achieve
  viable attendance, and generate expansion conversations from a single event.
stage: "Marketing > ProductAware"
motion: "MicroEvents"
channels: "Events"
level: "Smoke Test"
time: "8 hours over 2 weeks"
outcome: ">=50 registrations, >=60% show rate, >=5 expansion conversations initiated within 14 days"
kpis: ["Total registrations", "Show rate", "Sessions attended per attendee", "Expansion conversations initiated"]
slug: "user-conference-annual"
install: "npx gtm-skills add marketing/product-aware/user-conference-annual"
drills:
  - icp-definition
  - conference-planning-pipeline
  - threshold-engine
---

# Annual User Conference -- Smoke Test

> **Stage:** Marketing -> Product Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Confirm that your customer base will register for and attend a multi-session event you organize (not just a single webinar)
- Achieve a show rate that proves registrant commitment (>=60% for virtual)
- Generate at least 5 expansion conversations from attendees within 14 days -- these are existing customers who express interest in upgrading, expanding usage, or new features
- Validate the conference concept (topics, format, speaker mix) before investing in recurring or in-person events

## Leading Indicators

- Registration page conversion rate >15% from direct email traffic
- 50+ registrations reached at least 5 days before the event (not last-minute scramble)
- Average sessions attended per attendee >=2 out of 4-5 offered (people stay for multiple sessions, not just one)
- At least 10 attendees engage in chat, ask questions, or respond to polls
- At least 3 attendees click the post-conference CTA (book an expansion call, request a demo of a new feature)

## Instructions

### 1. Define your conference audience and theme

Run the `icp-definition` drill scoped to your conference audience. For this smoke test, the primary audience is existing customers. Document:

- **Who**: Which customer segments should attend? Filter your Attio customer list by: plan tier, usage level, industry vertical, and account health. Prioritize active customers on mid-tier plans (expansion candidates).
- **Theme**: Choose a theme at the intersection of your product roadmap and your customers' top pain points. The theme should be broad enough to support 4-5 sessions but specific enough that attendees know what they will get. Example: "Building [Outcome] with [Your Product] in 2026" or "[Industry] Operations Summit."
- **Why attend**: Write a one-paragraph value proposition. What will attendees learn, see, or experience that they cannot get from your documentation, blog, or a regular webinar?

### 2. Plan the conference structure

Run the `conference-planning-pipeline` drill for a virtual half-day conference:

- **Format**: Virtual, half-day (3-4 hours including breaks). Use Zoom (free for 40-min sessions, $13.33/mo Pro for longer) or Google Meet (free with Workspace) for the live sessions.
- **Agenda**: Plan 4-5 sessions:
  - Opening keynote (20 min): Product vision, roadmap preview, or industry state-of-the-art. Delivered by a founder or product lead.
  - Customer case study (30 min): A customer presents how they use your product. This is the highest-value session -- it provides social proof and inspires other customers.
  - Technical deep-dive or workshop (30 min): Hands-on session on a power feature or new capability.
  - Panel or AMA (30 min): 2-3 customers or team members discuss a topic relevant to the theme. Open Q&A.
  - Closing + roadmap preview (15 min): What is coming next. End with a clear CTA.
- **Breaks**: 10-minute breaks between sessions. These reduce drop-off and give people time to process.

Using `conference-planning-pipeline`, set up registration via Luma (free) with a Tally form for detailed attendee data capture. Configure the registration webhook to create contacts in Attio and enroll them in the conference email sequence in Loops.

### 3. Recruit speakers

**Human action required:** Speaker recruitment requires personal outreach.

- Identify 1-2 customer speakers by reviewing your Attio customer list for: high product usage, positive support interactions, and engaged contacts. Send personal emails asking if they would present a 20-30 minute case study.
- Schedule speaker prep calls via Cal.com to align on content, format, and logistics.
- Internal speakers (founder, product lead) should prepare their sessions using the conference theme.

The agent prepares the speaker outreach list, drafts invitation emails, and manages the prep call scheduling. The human sends the outreach and has the conversations.

### 4. Promote the conference

**Human action required:** For this smoke test, promotion is semi-manual.

- Using Loops, send a targeted announcement email to your customer list. Segment by relevance: customers using features related to the conference theme should get a more tailored invite.
- Send a second email 1 week before: "Agenda finalized" with the full session list and speaker bios.
- Send a reminder email the day before with join instructions.
- Post on LinkedIn with a hook focused on the conference theme, not just "we're hosting an event." Example: "We asked our customers what they struggle with most about [topic]. Their answers shaped our first user conference. Here's the agenda."
- Send personal emails or Slack messages to your top 20 accounts inviting them specifically.

### 5. Execute the conference

**Human action required:** You deliver the content and moderate sessions live.

The agent manages:
- Fire PostHog events for each attendee action: `conference_registered`, `conference_attended`, `conference_session_attended` (per session), `conference_engaged` (question, poll, chat)
- Log attendance and engagement per attendee in Attio
- Monitor the chat for questions to surface to the moderator

Tips for execution:
- Start the opening keynote on time. Open with something valuable (an insight, a data point, a customer story), not housekeeping.
- Between sessions, prompt the chat: "What's your biggest takeaway so far?" or "Drop your question for the next session."
- During the closing, share a clear CTA: "If you want to explore how [new feature / upgrade] could work for your team, book a call here." Drop the Cal.com link in chat.

### 6. Execute basic follow-up

Within 24 hours of the conference:

- Send a thank-you email to attendees: recording links for all sessions, a key takeaways document, and the expansion CTA (book a call to discuss upgrades, new features, or expanded usage)
- Send a "Sorry we missed you" email to no-shows with recording links and the same CTA
- For attendees who engaged heavily (3+ sessions attended AND asked questions), send a personal email or LinkedIn message referencing their participation and offering a 1:1 call

Log all follow-up actions in Attio. Tag attendees who clicked the CTA or replied.

### 7. Evaluate against the threshold

Run the `threshold-engine` drill to measure:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Registrations | >=50 | Count of Attio conference registrant list |
| Show rate | >=60% | Attendees (joined >=1 session) / Registrations |
| Sessions per attendee | >=2.0 | Average across all attendees |
| Expansion conversations | >=5 | Cal.com bookings + email replies expressing expansion interest within 14 days |

**PASS**: All four metrics met. Proceed to Baseline. Your customer base values a multi-session event and it generates expansion opportunities.

**FAIL**: Diagnose which metric missed:
- Low registrations (<50): Theme not compelling, or email list too small. Try a different theme that maps more directly to a current customer pain point. Expand promotion to product-aware prospects, not just customers.
- Low show rate (<60%): Scheduling issue or insufficient perceived value. Survey registrants who did not attend. Test a different day/time. Add a hook: "exclusive roadmap preview" or "limited early access."
- Low sessions per attendee (<2.0): Sessions not differentiated or agenda too long. Shorten to 3 sessions. Make each session title clearly distinct in value.
- Low expansion conversations (<5): Content too educational, not action-oriented. Strengthen the CTA during sessions. Add a "next steps for your account" session at the end.

## Time Estimate

- Conference strategy and ICP definition: 1 hour
- Registration and infrastructure setup (Luma, Tally, Loops, Attio): 1.5 hours
- Speaker recruitment and prep: 1.5 hours
- Promotion emails and LinkedIn posts: 1 hour
- Conference delivery (live): 4 hours (including 30 min pre-event setup)
- Post-event follow-up and analysis: 1 hour
- **Total: ~8 hours over 2 weeks** (setup in week 1, event + follow-up in week 2)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Zoom | Virtual conference platform | Free (40-min limit per session) or $13.33/mo Pro -- [zoom.us/pricing](https://zoom.us/pricing) |
| Google Meet | Virtual conference platform (alternative) | Free with Google Workspace |
| Luma | Registration page and RSVP management | Free for unlimited events -- [lu.ma](https://lu.ma) |
| Tally | Detailed registration form with webhooks | Free (unlimited forms + submissions) -- [tally.so/pricing](https://tally.so/pricing) |
| Loops | Email invitations, reminders, follow-up | Free tier: 1,000 contacts, 4,000 sends/mo -- [loops.so/pricing](https://loops.so/pricing) |
| Attio | Registrant and attendee tracking | Free tier: up to 3 users -- [attio.com](https://attio.com) |
| Cal.com | Expansion call booking CTA | Free tier: 1 user, unlimited event types -- [cal.com/pricing](https://cal.com/pricing) |
| PostHog | Event tracking | Free tier: 1M events/mo -- [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost at Smoke: $0-13/mo** (free if using Zoom free tier + all free tiers; $13 if upgrading Zoom Pro for longer sessions)

## Drills Referenced

- `icp-definition` -- define who should attend and what theme to build around
- `conference-planning-pipeline` -- set up registration, agenda, speaker coordination, promotion, and follow-up operations
- `threshold-engine` -- evaluate pass/fail against registration, attendance, and expansion conversation targets
