---
name: conference-planning-pipeline
description: End-to-end annual user conference planning workflow covering venue logistics, speaker curation, agenda design, registration management, and sponsor coordination
category: Events
tools:
  - Attio
  - Loops
  - PostHog
  - Cal.com
  - Luma
  - Clay
  - Tally
  - n8n
fundamentals:
  - event-platform-management
  - attio-lists
  - attio-contacts
  - attio-deals
  - loops-broadcasts
  - loops-audience
  - loops-sequences
  - posthog-custom-events
  - calcom-event-types
  - clay-people-search
  - clay-enrichment-waterfall
  - tally-form-setup
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
---

# Conference Planning Pipeline

This drill builds the complete operational backbone for an annual user conference -- from initial planning through post-event follow-up. It covers the agent-managed logistics, promotion, registration, speaker coordination, and attendee tracking that make a multi-session, multi-day event repeatable and measurable.

## Prerequisites

- Attio workspace with contacts and deal pipeline configured
- Loops account for email communications
- PostHog for event tracking
- n8n instance for workflow automation
- Budget approved for venue, A/V, and catering (Smoke: $0 for virtual; Baseline+: varies by scale)
- At least 200 active customers or product-aware contacts in your CRM

## Steps

### 1. Define the conference strategy

Before any logistics, answer five questions and store the answers as an Attio note on a "Conference 20XX" record:

- **Audience**: Who is the primary attendee? (customers, prospects, partners, developers). Use `attio-lists` to pull counts for each segment and confirm sufficient demand.
- **Goal**: What does success look like? (product adoption, expansion revenue, community building, brand credibility). Pick one primary and one secondary.
- **Format**: Virtual, in-person, or hybrid? Virtual scales cheaply. In-person creates stronger relationships. Hybrid adds operational complexity with little upside at small scale.
- **Scale**: Target attendee count based on your customer base size. Rule of thumb: aim for 15-25% of your active customer base as a starting target.
- **Date**: Choose a date 10-16 weeks out. Avoid major holidays, competing industry conferences, and end-of-quarter crunch. Tuesday-Thursday works best for B2B audiences.

### 2. Build the registration system

Using `event-platform-management`, create the conference event on Luma (recommended for tech audiences) or Eventbrite (broader reach):

- Set up the main conference event page with: conference name, date/time range, agenda overview, speaker highlights, and registration form
- For paid conferences, configure ticket tiers: Early Bird (20% discount, limited quantity), Standard, and VIP/Speaker Dinner
- For free conferences, still require registration to manage capacity and enable follow-up

Using `tally-form-setup`, create a detailed registration form that captures:
- Name, email, company, role, company size
- Which sessions they plan to attend (multi-select from agenda)
- Dietary restrictions (if in-person with catering)
- "What topic would you most like covered?" (open text -- this feeds future content planning)
- How they heard about the conference (attribution tracking)

Configure a webhook from the registration form to n8n using `n8n-triggers`. The n8n workflow should:
1. Create or update the contact in Attio using `attio-contacts` with tag `conference-20XX-registrant`
2. Add them to the conference Attio list using `attio-lists`
3. Enroll them in the conference email sequence in Loops using `loops-audience`
4. Fire a `conference_registered` PostHog event using `posthog-custom-events`

### 3. Curate the speaker lineup

Using `clay-people-search`, identify potential speakers from three pools:

- **Customer speakers**: Search your Attio customer list for people with: high product usage, interesting use cases, strong LinkedIn presence, and willingness to speak. These are the highest-value speakers -- they provide social proof.
- **Industry experts**: Use Clay to find people who have spoken at similar conferences, published on your topic area, or hold thought-leader positions in your ICP's industry.
- **Internal team**: Your own product, engineering, and leadership team for roadmap sessions, technical deep-dives, and keynotes.

For each potential speaker, enrich with `clay-enrichment-waterfall` to get LinkedIn profile, recent posts, and speaking history.

Create a speaker management list in Attio using `attio-lists` with fields: name, email, company, talk_title, talk_abstract, session_slot, confirmed (boolean), travel_required (boolean), prep_call_completed (boolean).

Using `calcom-event-types`, create a "Conference Speaker Prep Call" event type (30 min) for scheduling prep conversations with confirmed speakers.

### 4. Design the agenda

Build an agenda that balances three content types:

- **Keynotes (2-3)**: Big-picture talks from leadership or notable guests. Open and close the conference. 20-30 minutes each.
- **Breakout sessions (4-8)**: Focused talks on specific topics. Customer case studies, technical deep-dives, product workshops. 30-45 minutes each.
- **Interactive sessions (2-4)**: Roundtables, Q&A panels, hands-on workshops, networking breaks. These drive the highest engagement and relationship-building.

Map sessions to time slots. For a 1-day virtual conference: 4-5 hours of content with breaks. For a 2-day in-person conference: 6 hours of content per day with longer networking breaks and a social event on night 1.

Store the finalized agenda in Attio and update the registration page on Luma/Eventbrite.

### 5. Launch the promotion engine

Using `n8n-scheduling`, build an automated promotion workflow:

**Week -10**: Announce the conference
- Using `loops-broadcasts`, send announcement email to your full customer and prospect list
- Create a landing page with early bird registration
- Draft 4 LinkedIn posts (announcement, first speaker reveal, agenda teaser, early bird deadline)

**Week -6**: Speaker spotlight wave
- Using `loops-broadcasts`, send "Featured Speaker" emails highlighting 2-3 confirmed speakers
- Invite registrants to share with colleagues (include a forwarding incentive if possible)
- Use `clay-people-search` to find and invite ICP-matched prospects who have not yet registered

**Week -3**: Urgency wave
- Send "Agenda finalized" email with full session list
- If capacity-limited, send "X spots remaining" messages
- Personal invites from Attio to high-value prospects in active pipeline using `attio-lists`

**Week -1**: Final push
- Send "Next week" reminder to registrants with logistics (join link, agenda, prep materials)
- Send "Last chance to register" to non-registrants
- Post final LinkedIn countdown

**Day -1**: Pre-event
- Send join instructions with technical requirements, agenda, and speaker bios
- Confirm all speakers have their prep materials and tech setup

### 6. Execute day-of operations

**Human action required:** The conference itself requires human delivery -- keynotes, moderation, live Q&A management.

The agent manages:
- Monitor registration vs attendance in real-time using `posthog-custom-events`: fire `conference_attended` when someone joins, `conference_session_attended` for each session
- Track session engagement: questions asked, poll responses, chat activity
- Log engagement scores per attendee in Attio using `attio-contacts`: number of sessions attended, questions asked, interactions
- If virtual: monitor tech issues and alert the team via n8n workflows

### 7. Execute post-conference follow-up

Within 24 hours of the conference ending:

Using `loops-sequences`, send segmented follow-up emails:

- **Active attendees (3+ sessions)**: Recording links, key takeaways document, exclusive CTA (book a strategy call, early access to new feature). These are your warmest expansion leads.
- **Partial attendees (1-2 sessions)**: Recording links for sessions they missed, highlights document, softer CTA (join the community, try a new feature).
- **No-shows**: "Sorry we missed you" with recording access and an invite to the next event.

Using `tally-form-setup`, create a post-conference feedback survey:
- Overall satisfaction (1-10 NPS scale)
- Favorite session
- Suggested topics for next year
- Would they attend again? (yes/no/maybe)
- Would they recommend to a colleague? (yes/no)

Fire `conference_feedback_submitted` in PostHog when survey responses arrive.

Using `attio-deals`, create deals for attendees who: attended 3+ sessions AND asked questions or engaged in chat AND match expansion criteria (current customer on a lower tier, or prospect in active evaluation). Tag the deal source as `conference-20XX`.
