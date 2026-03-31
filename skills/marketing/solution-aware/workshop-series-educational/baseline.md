---
name: workshop-series-educational-baseline
description: >
  Workshop Series — Baseline Run. Run 3 workshops over 6 weeks with automated
  registration ops, post-workshop nurture sequences segmented by participation
  depth, and PostHog tracking across the full funnel. Validate repeatable demand
  and that hands-on engagement converts to pipeline at a higher rate than
  passive events.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Content"
level: "Baseline Run"
time: "18 hours over 6 weeks"
outcome: ">=50 total registrations, >=40% average show rate, >=18 qualified leads across 3 workshops"
kpis: ["Registrations per workshop", "Show rate", "Exercise completion rate", "Nurture reply rate", "Qualified leads"]
slug: "workshop-series-educational"
install: "npx gtm-skills add marketing/solution-aware/workshop-series-educational"
drills:
  - posthog-gtm-events
---

# Workshop Series — Baseline Run

> **Stage:** Marketing > SolutionAware | **Motion:** MicroEvents | **Channels:** Events, Content

## Outcomes

- Prove that workshop demand is repeatable across 3 events (not a one-time fluke)
- Establish automated post-workshop nurture that converts hands-on participants to pipeline without manual follow-up
- Build the PostHog event tracking foundation for all future measurement and optimization
- Identify which topics, difficulty levels, and exercise formats produce the best results
- Confirm that workshops convert to qualified leads at a higher rate than passive event formats

## Leading Indicators

- Second workshop registrations reach at least 80% of first workshop registrations (demand holds)
- Nurture email reply rate >12% for active participants (Tier 1)
- At least 2 meetings booked from automated nurture sequences (not just manual follow-up)
- Exercise completion rate consistent across workshops (>=60% -- validates the format, not just one topic)
- Recording + materials download rate >30% among no-shows (content has lasting value)

## Instructions

### 1. Configure workshop event tracking

Run the `posthog-gtm-events` drill to implement the full workshop event taxonomy in PostHog:

- `workshop_page_viewed` -- registration page visit (properties: workshop_slug, source_channel)
- `workshop_registered` -- form submitted (properties: workshop_slug, company, role, skill_level)
- `workshop_prep_email_opened` -- opened preparation email (properties: workshop_slug, prep_step)
- `workshop_reminder_sent` -- reminder email delivered (properties: workshop_slug, reminder_number)
- `workshop_attended` -- joined the live session (properties: workshop_slug, join_time, duration_watched)
- `workshop_exercise_started` -- began a hands-on exercise (properties: workshop_slug, exercise_id)
- `workshop_exercise_completed` -- finished a hands-on exercise (properties: workshop_slug, exercise_id, completion_quality)
- `workshop_question_asked` -- asked a question in chat or verbally (properties: workshop_slug, question_type)
- `workshop_cta_clicked` -- clicked the post-workshop CTA (properties: workshop_slug, cta_type)
- `workshop_recording_watched` -- watched the replay (properties: workshop_slug, percent_watched, viewer_tier)
- `workshop_nurture_email_sent` -- follow-up email sent (properties: workshop_slug, tier, sequence_step)
- `workshop_nurture_reply_received` -- registrant replied to nurture (properties: workshop_slug, tier)
- `workshop_meeting_booked` -- meeting booked from workshop funnel (properties: workshop_slug, tier, source)

Build a PostHog funnel: `workshop_page_viewed` -> `workshop_registered` -> `workshop_attended` -> `workshop_exercise_completed` -> `workshop_nurture_reply_received` -> `workshop_meeting_booked`

### 2. Upgrade workshop operations

Run the the workshop pipeline workflow (see instructions below) drill with these Baseline-level enhancements:

- Move to Riverside ($19/mo Standard) for recording capability. Every session gets recorded for replay distribution and future content repurposing.
- Build automated email sequences in Loops: confirmation with prerequisites on registration, prep check 3 days before ("Have you set up [tool/account]?"), reminder 1 day before with setup verification, and "starting in 1 hour" reminder with join link. Each prep email re-sells the outcome: "Tomorrow you will build [deliverable]."
- Create a standardized registration page template that you clone per workshop (swap topic, date, difficulty level, exercises).
- Set up Attio lists per workshop with automatic tagging from the registration form. Include skill_level as a tracked property.
- Prepare exercise materials as standalone documents that work both live and asynchronously. This maximizes value for no-shows who watch the recording.

### 3. Build post-workshop nurture automation

Run the the workshop attendee nurture workflow (see instructions below) drill to create segmented follow-up:

- After each workshop, automatically segment registrants into 4 tiers: active participant (attended + completed exercises), observer (attended but did not complete exercises), no-show, and late registrant.
- Enroll each tier in the appropriate Loops nurture sequence. Active participants get materials + personalized follow-up referencing their exercise output. Observers get the exercise as a standalone resource to try on their own.
- Configure n8n triggers: when a Tier 1 or Tier 2 contact replies, auto-create an Attio deal and notify via Slack.
- Track nurture performance with PostHog events at every step.

This replaces the manual follow-up from Smoke with automated, participation-aware sequences that scale.

### 4. Run 3 workshops over 6 weeks

Execute a small series to validate repeatable demand:

**Workshop 1**: Use the same topic and format that passed Smoke (proven demand). Focus on testing the new automation: do prep emails improve show rate? Does segmented nurture generate replies? Does exercise completion tracking work reliably?

**Workshop 2**: Test a different topic within the same ICP pain area. Keep the format and difficulty level identical. This isolates topic performance from format performance. If Workshop 1 was beginner-level, Workshop 2 is also beginner-level but on a different skill.

**Workshop 3**: Test a different difficulty level on the best-performing topic from Workshops 1-2. If beginners registered well, try an intermediate session. This identifies whether your audience wants depth or breadth.

**Human action required:** You still deliver the content and facilitate exercises live. The agent handles everything before and after each workshop.

### 5. Analyze cross-workshop performance

After all workshops complete and nurture windows close (14 days post-last-event), compare:

| Metric | WS 1 | WS 2 | WS 3 | Target |
|--------|------|------|------|--------|
| Registrations | ? | ? | ? | >=50 total |
| Show rate | ? | ? | ? | >=40% avg |
| Exercise completion rate | ? | ? | ? | >=60% avg |
| Nurture reply rate (Tier 1) | ? | ? | ? | >=12% |
| Qualified leads | ? | ? | ? | >=18 total |

Identify: Which topic drove the most registrations? Which difficulty level had the best exercise completion? Which promotion channel (email, LinkedIn, personal invite) produced the highest-quality registrants? How does workshop pipeline conversion compare to other event formats you have run?

### 6. Evaluate against the threshold

**PASS** (all core metrics met): >=50 total registrations, >=40% average show rate, >=18 qualified leads. Proceed to Scalable. You have repeatable demand and working automation.

**FAIL**: Diagnose by metric:
- Low registrations: Topic selection or promotion reach. Try broader topics or expand your invite list. Check whether prerequisites are blocking sign-ups.
- Low show rate: Prep email sequence not effective, or event timing suboptimal. Test different days/times. Add a "what to expect" video to the prep sequence.
- Low exercise completion: Exercises too complex for the audience skill level. Simplify, provide more scaffolding, or offer a pre-workshop prep session.
- Low qualified leads: Nurture sequence quality. Review email copy, CTA clarity, and how well the follow-up references the specific exercise the attendee completed.

## Time Estimate

- PostHog event tracking setup: 2 hours
- Workshop operations upgrade (Riverside, Loops sequences, Attio lists): 2 hours
- Nurture automation build (n8n workflows, Loops sequences): 3 hours
- Workshop delivery (3 workshops x 75 min each): 4 hours
- Per-workshop materials preparation: 3 hours total
- Analysis and iteration: 2 hours
- **Total: ~18 hours over 6 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Riverside | Workshop recording + production | $19/mo Standard -- [riverside.com/pricing](https://riverside.com/pricing) |
| Loops | Confirmation, prep, reminders, nurture sequences | Free tier (up to 1,000 contacts) or $49/mo (up to 5,000) -- [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Event tracking + funnels | Free tier: 1M events/mo -- [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | Registrant tracking + deal creation | Free tier: 3 users -- [attio.com](https://attio.com) |
| n8n | Nurture automation workflows | Self-hosted free or Cloud Starter EUR24/mo -- [n8n.io/pricing](https://n8n.io/pricing) |
| Cal.com | Meeting booking CTA | Free tier -- [cal.com/pricing](https://cal.com/pricing) |

**Estimated play-specific cost at Baseline: $19-70/mo** (Riverside + Loops if over free tier)

## Drills Referenced

- the workshop pipeline workflow (see instructions below) -- registration, curriculum design, delivery, and follow-up operations
- `posthog-gtm-events` -- implement standard workshop event taxonomy for measurement
- the workshop attendee nurture workflow (see instructions below) -- automated post-workshop segmented nurture based on participation depth
