---
name: ai-meeting-prep-baseline
description: >
  AI-Powered Meeting Preparation — Baseline Run. Automate brief generation to run before every
  scheduled meeting. n8n triggers the account-research-brief drill 24 hours before each Cal.com
  meeting, and a feedback loop scores every brief after the call completes. Always-on preparation
  with quality tracking.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=60% prep time reduction and >=25% higher next-step conversion for AI-prepped calls over 2 weeks"
kpis: ["Prep time reduction", "Next-step conversion rate", "AI brief usefulness score", "Discovery quality improvement"]
slug: "ai-meeting-prep"
install: "npx gtm-skills add sales/connected/ai-meeting-prep"
drills:
  - account-research-brief
  - posthog-gtm-events
---

# AI-Powered Meeting Preparation — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

First always-on automation. Every scheduled meeting automatically gets an AI-generated brief 24 hours before the call. After each call, the feedback loop runs to score brief quality and extract new intelligence. The system runs continuously for 2 weeks across all meetings to prove that automated prep consistently improves outcomes vs the manual baseline established in Smoke.

**Pass threshold:** >=60% prep time reduction and >=25% higher next-step conversion for AI-prepped calls over 2 weeks.

## Leading Indicators

- Briefs generated automatically for >=90% of scheduled meetings (no manual triggering needed)
- Founder reviews brief in under 5 minutes before each call (the brief is scannable)
- Brief usefulness score averages >=3.5/5 across all meetings
- Post-call feedback loop runs within 24 hours of each completed meeting
- Attio deal records show richer notes and updated intelligence after each call (the feedback loop is populating data)
- Discovery calls surface more pain points than before (founder asks better questions from the brief)

## Instructions

### 1. Set Up Automated Brief Triggering

Build an n8n workflow that automatically generates meeting briefs:

**Trigger:** Cal.com webhook fires when a meeting is scheduled or 24 hours before an existing meeting.

**Workflow steps:**
1. Receive Cal.com event (attendee name, email, meeting type, date, duration)
2. Match the attendee to an Attio contact and deal record (search by email)
3. If no deal exists: create a skeleton deal in Attio and proceed
4. Run the `account-research-brief` drill with the deal ID, meeting type, and attendees
5. Store the generated brief as an Attio note on the deal
6. Send a Slack notification to the founder: "Meeting brief ready for {company_name} — {meeting_date}. View in Attio."

**Error handling:**
- If Cal.com attendee does not match any Attio contact, create the contact first, then proceed with reduced context
- If Clay enrichment fails (API down, no credits), generate a brief from CRM data only and flag it as "limited intelligence"
- If the meeting is in less than 2 hours (late scheduling), skip the 24-hour delay and generate immediately

### 2. Set Up the Post-Call Feedback Loop

Build a second n8n workflow that scores briefs after calls:

**Trigger:** Fireflies webhook fires when a transcript is ready (typically 15-30 minutes after a call ends).

**Workflow steps:**
1. Receive Fireflies transcript webhook
2. Match the transcript to a deal in Attio (by attendee email or meeting title)
3. Find the meeting brief note for this deal (tagged `meeting-brief`)
4. Run the the call brief feedback loop workflow (see instructions below) drill: compare brief predictions to actual call, score quality, extract new intelligence
5. Store the feedback as an Attio note tagged `brief-feedback`
6. Update deal properties with new intelligence (pain points, stakeholders, competitive mentions, next steps)
7. Log `meeting_brief_scored` event to PostHog

**If no brief exists for this meeting:** Log `meeting_no_brief` event to PostHog. This creates the denominator for adoption tracking.

### 3. Configure PostHog Event Tracking

Run the `posthog-gtm-events` drill to set up the event taxonomy for this play:

| Event | When Fired | Key Properties |
|-------|-----------|----------------|
| `meeting_brief_generated` | Brief created | deal_id, meeting_type, data_completeness_score, generation_time_seconds |
| `meeting_brief_scored` | Feedback loop completed | deal_id, overall_accuracy, overall_usefulness, meeting_outcome, best_section, worst_section |
| `meeting_no_brief` | Meeting completed with no brief | deal_id, reason (no_deal_match, late_schedule, error) |
| `meeting_outcome_logged` | Deal stage updated after meeting | deal_id, outcome, had_brief (boolean) |

Set up a PostHog funnel: `meeting_brief_generated` → `meeting_brief_scored` → `meeting_outcome_logged` with outcome = "next_step_committed". This funnel shows the conversion from brief generation to positive meeting outcomes.

### 4. Run for 2 Weeks Across All Meetings

Let the automation run. Monitor daily:
- Are briefs being generated for every meeting? Check the n8n execution log for failures.
- Are feedback scores being captured? If Fireflies transcripts are not triggering the feedback loop, check webhook configuration.
- Are deal records being enriched with post-call intelligence? Spot-check 2-3 deals per day.

Intervene only if the automation fails. The goal is hands-off operation.

### 5. Evaluate Against Threshold

After 2 weeks, measure:

**Prep time reduction:** Compare time-from-brief-generated-to-meeting vs pre-Smoke manual prep time. Target: >=60%. The founder should now be spending under 5 minutes reviewing the brief vs 30+ minutes researching manually.

**Next-step conversion:** Compare the rate of meetings that result in a committed next step (demo booked, proposal requested, follow-up scheduled) for AI-prepped calls vs the founder's historical baseline (from before this play started). Target: >=25% lift.

If PASS: proceed to Scalable. If FAIL: diagnose using the brief quality scores. Is the problem data quality (sparse intelligence), brief quality (low usefulness scores), or execution (founder not reading the briefs)? Address the root cause and re-run.

## Time Estimate

- 4 hours: Build n8n workflows (brief trigger + feedback loop)
- 2 hours: Configure PostHog event tracking and funnel
- 2 hours: Test the automation with 2-3 meetings, debug issues
- 8 hours: Monitoring and spot-checking over 2 weeks (~30 min/day)
- 2 hours: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal context, brief storage, feedback notes | $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — automated account research | $185/mo (Launch) — [clay.com/pricing](https://www.clay.com/pricing) |
| Anthropic API | AI — brief generation and feedback scoring | Usage-based, ~$2-5/mo at 50 meetings — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| n8n | Automation — brief triggering and feedback loop | $24/mo (Starter) or $60/mo (Pro) — [n8n.io/pricing](https://n8n.io/pricing) |
| Fireflies | Transcription — post-call feedback loop | $19/seat/mo (Pro) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Cal.com | Scheduling — meeting trigger source | Free (self-hosted) or $12/seat/mo — [cal.com/pricing](https://cal.com/pricing) |
| PostHog | Analytics — quality tracking, funnels | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost this level:** ~$20-65/mo. n8n ($24-60), Fireflies ($19), Anthropic API (~$3). Clay and Attio are shared stack costs.

## Drills Referenced

- `account-research-brief` — assemble account intelligence and generate a structured meeting brief (now triggered automatically 24 hours before every meeting)
- the call brief feedback loop workflow (see instructions below) — after each call, compare brief predictions to actual outcomes, score quality, extract new intelligence
- `posthog-gtm-events` — set up event tracking for brief generation, quality scoring, and outcome correlation
