---
name: summit-series-automation
description: Automate recurring virtual summit operations including theme planning, speaker pipeline, promotion cadence, and cross-summit analytics
category: Events
tools:
  - n8n
  - Loops
  - Attio
  - PostHog
  - Cal.com
  - Riverside
  - Clay
fundamentals:
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - loops-broadcasts
  - loops-audience
  - attio-lists
  - attio-contacts
  - attio-automation
  - attio-reporting
  - posthog-custom-events
  - posthog-funnels
  - calcom-event-types
  - riverside-recording
  - clay-people-search
  - clay-enrichment-waterfall
  - linkedin-organic-posting
---

# Summit Series Automation

This drill transforms one-off virtual summits into a repeatable, automated series that runs quarterly with minimal manual overhead. The agent handles theme planning, speaker pipeline management, promotion sequencing, sponsor coordination, and cross-summit analytics. The human delivers the moderation and makes final editorial decisions.

## Prerequisites

- At least 2 completed summits with performance data (from Baseline level)
- n8n instance with active connections to Loops, Attio, and PostHog
- Riverside account for recording and production
- A theme backlog with at least 4 summit themes
- Clay table with ICP-matched prospects for targeted invites
- Speaker database in Attio with past performance data

## Steps

### 1. Build the summit series calendar

Create a theme backlog ranked by expected registration pull. Score each theme:

- **ICP pain alignment (1-5)**: Does this theme address a top-3 pain point?
- **Speaker availability (1-5)**: Can you recruit 6+ strong speakers for this theme?
- **Competitive differentiation (1-5)**: Is this a topic where you have unique authority?
- **Timeliness (1-3)**: Is there a market event, regulatory change, or technology shift that makes this theme urgent now?

Using `attio-lists`, create a "Summit Calendar" list with fields: theme, target_date, speaker_count_confirmed, sponsor_count, registration_target, status (planned/in-promotion/live/complete). Schedule summits quarterly for the next 12 months.

### 2. Automate the speaker pipeline

Using `n8n-scheduling`, create a workflow that triggers 12 weeks before each summit:

**Week T-12: Speaker sourcing**
- Using `clay-people-search`, identify 20-30 potential speakers matching the summit theme: recent LinkedIn posts on the topic, conference speaking history, book authors, podcast guests, and customer success stories related to the theme.
- Enrich with `clay-enrichment-waterfall` for contact details.
- Import into Attio using `attio-contacts` tagged "Speaker Prospect — [Summit Theme]."
- Score prospects by: audience reach (LinkedIn followers + company size), topic expertise (content volume), and speaking track record.

**Week T-10: Speaker outreach**
- Send personalized speaker invitations from Attio using `attio-lists`. Each invitation includes: theme, expected audience size and profile, session format options, date commitment, and promotion expectations.
- Using `n8n-triggers`, track responses and auto-update Attio status: invited → accepted → confirmed.
- If a speaker declines, auto-trigger the next prospect on the ranked list.

**Week T-8: Speaker confirmation**
- All speakers confirmed. Send logistics email: session format, timing, AV requirements, prep call scheduling.
- Using `calcom-event-types`, create prep call booking links for each speaker.
- Add confirmed speakers to the promotion assets: bios, headshots, session titles.

**Week T-4: Speaker prep**
- Auto-send prep call reminders using `n8n-scheduling`.
- After each prep call, log notes in Attio: confirmed topic, talking points, AV setup status.
- Send final logistics email with: run-of-show, session order, technical check schedule.

### 3. Automate the promotion engine

Using `n8n-scheduling`, create a cascading promotion workflow for each summit:

**T-8 weeks: Launch**
- Generate the registration page and connect to Attio.
- Draft 5 LinkedIn posts (theme announcement, speaker spotlights x3, agenda reveal) using `linkedin-organic-posting`.
- Send save-the-date email via `loops-broadcasts` to the full subscriber list.
- Activate speaker promotion: send each speaker a pre-written social post they can customize and share.

**T-6 weeks: Main push**
- Send full invitation email to subscriber list segmented by ICP via `loops-broadcasts`.
- Using `clay-people-search` and `clay-enrichment-waterfall`, build a net-new prospect list of 500-1000 people matching the summit ICP. Import to Loops via `loops-audience`.
- Send targeted invitations to the net-new list.
- Post speaker spotlight series on LinkedIn.

**T-4 weeks: Urgency push**
- Resend to non-openers from wave 1.
- Send speaker-specific emails: "Hear [Name] from [Company] on [specific insight]."
- Activate sponsor promotion: sponsors email their lists.
- Partner cross-promotion emails.

**T-2 weeks: Final push and prep**
- "Limited spots" email.
- LinkedIn countdown posts.
- Configure reminder sequence via `loops-sequences`: 1-week, 1-day, 1-hour reminders.
- Finalize Riverside production setup using `riverside-recording`.

**T+1 day: Post-summit**
- Trigger the `summit-attendee-nurture` drill with full engagement data.
- Export and process all session recordings.
- Update summit status in Attio to "complete."
- Send speaker thank-you emails with engagement stats for their sessions.

### 4. Automate sponsor coordination

For summits with sponsors, build an n8n workflow using `n8n-workflow-basics`:

- T-10 weeks: Send sponsorship proposal to the pipeline (managed in Attio via `attio-deals`).
- T-6 weeks: Confirmed sponsors receive logistics email: logo placement, session slot, attendee data sharing agreement.
- T-2 weeks: Sponsor materials collected (logos, booth content, speaking materials).
- T+2 days: Send sponsors their session engagement data and the qualified lead list per their tier agreement.

### 5. Build cross-summit analytics

Using `posthog-custom-events` and `posthog-funnels`, track metrics across the entire series:

- **Registration funnel per summit**: page_viewed → registered → reminded → attended → multi_session → engaged → meeting_booked
- **Series-level metrics**: Registration growth trend, repeat attendee rate (what % attend 2+ summits), theme-to-pipeline correlation, speaker-to-registration pull, promotion channel effectiveness per summit
- **Cumulative pipeline**: Total meetings booked across all summits, average pipeline per summit, cost per qualified lead trend, revenue attribution (90-day window)
- **Speaker performance**: Registrations driven by each speaker's promotion, session attendance rates, engagement rates per speaker

Create a PostHog dashboard for the series showing: registrations by summit (bar chart), show rate trend (line chart), pipeline generated per summit (bar chart), promotion channel breakdown (pie chart), repeat attendee count (counter), and top-performing speakers by attendance (table).

Using `attio-reporting`, generate a quarterly series report: aggregate metrics, top/bottom performing summits, speaker ROI ranking, promotion channel ROI, and recommendations for next quarter's themes and speaker lineup.

### 6. Scale registration through targeted prospecting

For each upcoming summit, use Clay to find net-new prospects:

- Using `clay-people-search`, search for people who match the summit ICP AND have recently engaged with the theme topic: published LinkedIn posts, attended related conferences, changed roles into relevant positions, or work at companies showing intent signals.
- Using `clay-enrichment-waterfall`, enrich with verified email and company data.
- Import into Attio via `attio-contacts` tagged "Summit Prospect — [Theme]."
- Add to Loops via `loops-audience` for the targeted invitation sequence.

Target: 500-1000 net-new, theme-relevant prospects per summit to supplement the existing list. Track which net-new segments convert best and feed that data back into Clay search criteria.
