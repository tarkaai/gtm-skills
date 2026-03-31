---
name: virtual-summit-hosting-baseline
description: >
  Virtual Summit Hosting — Baseline Run. Run 2-3 summits to prove repeatable demand.
  Build the operational infrastructure for always-on summit operations with
  speaker pipelines, automated promotion, and post-summit nurture sequences.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Content, Email"
level: "Baseline Run"
time: "50 hours over 3 months"
outcome: "≥400 registrations and ≥25 qualified leads across 2-3 summits with repeatable operations"
kpis: ["Registration count per summit", "Show rate", "Multi-session attendance rate", "Qualified leads per summit", "Registrant-to-pipeline conversion rate", "Promotion channel attribution"]
slug: "virtual-summit-hosting"
install: "npx gtm-skills add marketing/solution-aware/virtual-summit-hosting"
drills:
  - summit-attendee-nurture
  - posthog-gtm-events
  - threshold-engine
---

# Virtual Summit Hosting — Baseline Run

> **Stage:** Marketing → SolutionAware | **Motion:** MicroEvents | **Channels:** Events, Content, Email

## Outcomes

Run 2-3 summits over 3 months to prove repeatable demand and build operational infrastructure. Validate that different themes generate consistent registration and pipeline. Establish the speaker recruitment pipeline, promotion cadence, and post-summit nurture system that will power automation at Scalable level. Pass threshold: ≥400 total registrations AND ≥25 qualified leads across the 2-3 summits, with each summit showing improvement or consistency vs the previous.

## Leading Indicators

- Second summit registrations within ±20% of first summit (proves repeatability)
- Speaker pipeline has ≥2 confirmed speakers per summit recruited without manual outreach (returning or inbound speakers)
- Promotion engine drives registrations from at least 3 channels (email, LinkedIn, speaker-driven)
- Post-summit nurture generates ≥5 meeting bookings per summit within 14 days
- Registrant-to-pipeline conversion rate stabilizes within a measurable range across summits

## Instructions

### 1. Configure summit event analytics

Run the `posthog-gtm-events` drill to establish the full summit event taxonomy in PostHog. Track these events with consistent naming:

- `summit_page_viewed` (properties: summit_slug, source, utm_campaign)
- `summit_registered` (properties: summit_slug, company_size, role, source)
- `summit_reminder_clicked` (properties: summit_slug, reminder_type)
- `summit_session_joined` (properties: summit_slug, session_id, join_time)
- `summit_session_left` (properties: summit_slug, session_id, leave_time, duration_minutes)
- `summit_question_asked` (properties: summit_slug, session_id)
- `summit_poll_responded` (properties: summit_slug, session_id)
- `summit_cta_clicked` (properties: summit_slug, session_id, cta_type)
- `summit_nurture_email_sent` (properties: summit_slug, tier, sequence_step)
- `summit_nurture_reply_received` (properties: summit_slug, tier)
- `summit_nurture_meeting_booked` (properties: summit_slug, tier, source_email_step)
- `summit_recording_watched` (properties: summit_slug, session_id, percent_watched)

Build a PostHog funnel: `summit_page_viewed` → `summit_registered` → `summit_session_joined` → `summit_question_asked` → `summit_nurture_meeting_booked`. Save as "Summit Pipeline Funnel."

### 2. Run summit 1 using the full pipeline

Run the the summit pipeline workflow (see instructions below) drill for the first summit. This is the same pipeline used in Smoke, but now with full PostHog tracking instrumented. Focus on:

- **Theme selection**: Choose a theme that performed well at Smoke or a new theme that addresses a different ICP pain point. Document the theme hypothesis in Attio.
- **Speaker recruitment**: Use the the summit pipeline workflow (see instructions below) drill's speaker recruitment process. For this summit, track every step: outreach count, acceptance rate, and speaker-driven registrations. This data builds the speaker pipeline for automation.
- **Promotion**: Execute the full 8-week promotion cadence from the summit pipeline workflow (see instructions below). Track registrations per channel per week in PostHog.
- **Production and execution**: Run the summit with full session-level tracking. Log all engagement events.

**Human action required:** Moderate the summit live. Deliver any internal sessions.

### 3. Execute structured post-summit nurture

Run the `summit-attendee-nurture` drill. This builds on the basic follow-up from Smoke with a full 5-tier segmentation and differentiated nurture sequences:

- Tier 1 (power attendees): 4-email sequence over 10 days with personalized video responses to their questions.
- Tier 2 (engaged attendees): 3-email sequence with session-specific resources.
- Tier 3 (passive attendees): 2-email sequence with recordings and highlights.
- Tier 4 (no-shows): 2-email sequence with recordings and next-event invite.
- Tier 5 (replay viewers): 2-email triggered sequence based on replay behavior.

Track every nurture touchpoint in PostHog. Measure reply rates and meeting booking rates by tier.

### 4. Analyze and iterate for summit 2

After the 14-day nurture window closes on summit 1, analyze:

- **Registration analysis**: Which channels drove the most registrations? What was the cost per registrant per channel? Did speaker promotion meet the 20% target?
- **Attendance analysis**: What was the show rate? Where in the session lineup did the biggest drop-off occur? Which sessions had the highest engagement?
- **Conversion analysis**: Which tier generated the most meetings? What was the reply rate per tier vs targets? How does the registrant-to-pipeline conversion compare to other plays?
- **Speaker analysis**: Which speakers drove the most registrations? Which sessions had the highest engagement? Who would you invite back?

Document findings in Attio. Use them to adjust summit 2:
- If registration was the bottleneck: change the theme, expand promotion channels, or recruit higher-profile speakers.
- If show rate was the bottleneck: improve reminder cadence, adjust event timing, or shorten the summit.
- If conversion was the bottleneck: improve nurture personalization, change CTAs, or adjust the session content to be more product-adjacent.

### 5. Run summit 2 (and optionally summit 3) with adjustments

Run the the summit pipeline workflow (see instructions below) drill again with the adjustments identified in step 4. Change one major variable per summit to isolate what works:

- Summit 2: Change theme OR speaker lineup OR promotion channels (not all three)
- Summit 3 (if needed): Change the next variable

For each summit, run the `summit-attendee-nurture` drill with the same tier structure but updated messaging based on what worked in the previous summit's nurture.

### 6. Evaluate against threshold

Run the `threshold-engine` drill after the final summit's 14-day nurture window closes. Measure across all summits:

- Total registrations across all summits (target: ≥400)
- Total qualified leads across all summits (target: ≥25)
- Per-summit trend: are registrations and qualified leads flat, growing, or declining?
- Operational repeatability: did the second/third summit require less setup time than the first?

**PASS → Scalable**: Hit both thresholds AND the per-summit trend is flat or growing. The summit model works and is ready for automation.
**MARGINAL → Re-run**: Close but inconsistent (e.g., summit 1 hit targets but summit 2 regressed). Run one more summit to prove consistency.
**FAIL → Pivot**: Consistently below threshold after 3 attempts. Summits may be too heavy for your current audience size. Consider smaller-format events (webinars, roundtables).

## Time Estimate

- PostHog event taxonomy setup: 3 hours
- Summit 1 full pipeline (speaker recruitment through follow-up): 18 hours
- Summit 1 analysis and iteration planning: 3 hours
- Summit 2 full pipeline: 15 hours (less setup time with established processes)
- Summit 2 analysis: 2 hours
- Summit 3 (if needed): 15 hours
- Threshold evaluation: 2 hours
- Human moderation time (×2-3 summits): 4 hours × 2-3 = 8-12 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Riverside | Summit hosting and recording | $15/mo (Standard) — https://riverside.fm/pricing |
| Cal.com | Speaker prep scheduling | Free tier — https://cal.com/pricing |
| Loops | Email sequences and broadcasts | Free up to 1,000 contacts; $49/mo if over — https://loops.so/pricing |
| Attio | CRM for registrant, speaker, and pipeline tracking | Free up to 3 seats — https://attio.com/pricing |
| PostHog | Full funnel analytics and event tracking | Free up to 1M events — https://posthog.com/pricing |
| Clay | Speaker sourcing and prospect enrichment | $149/mo (Explorer) — https://clay.com/pricing |

**Estimated play-specific cost: $164-213/mo** (Riverside + Clay; Loops if over free tier)

## Drills Referenced

- the summit pipeline workflow (see instructions below) — full summit lifecycle: speaker recruitment, registration, promotion, production, follow-up. Run once per summit.
- `summit-attendee-nurture` — post-summit 5-tier segmentation and differentiated nurture sequences. Converts attendees into pipeline.
- `posthog-gtm-events` — establishes the full summit event taxonomy in PostHog for consistent measurement across all summits.
- `threshold-engine` — evaluates aggregate metrics across all summits and recommends advance, iterate, or pivot.
