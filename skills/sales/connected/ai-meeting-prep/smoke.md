---
name: ai-meeting-prep-smoke
description: >
  AI-Powered Meeting Preparation — Smoke Test. Agent researches a target account, assembles intelligence
  from CRM and enrichment sources, and generates a structured meeting brief with talking points,
  tailored questions, objection preparation, and a recommended agenda. Founder uses the brief in 3-5
  real calls and scores whether it reduced prep time and improved call quality.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=50% reduction in prep time and >=3 actionable insights per call within 1 week"
kpis: ["Prep time reduction", "Insights per call", "AI brief quality score", "Call outcome improvement"]
slug: "ai-meeting-prep"
install: "npx gtm-skills add sales/connected/ai-meeting-prep"
drills:
  - threshold-engine
---

# AI-Powered Meeting Preparation — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

Prove that an AI-generated meeting brief produces materially better call preparation than the founder's current manual process. At this level the agent does the research and generates the brief; the founder reviews it, uses it in real calls, and manually scores the quality. No automation, no always-on workflows. Just agent-assisted prep for 3-5 upcoming meetings.

**Pass threshold:** >=50% reduction in prep time and >=3 actionable insights per call within 1 week.

## Leading Indicators

- Brief generated in under 10 minutes vs founder's manual prep taking 30+ minutes
- Brief surfaces at least 1 insight the founder did not already know per meeting
- Founder uses at least 3 of the brief's tailored questions during the call
- Call conversations go deeper (prospect shares more detail) than non-prepped calls
- The opening line from the brief gets a positive reaction ("You did your homework")

## Instructions

### 1. Select 3-5 Upcoming Meetings as the Test Cohort

Query Attio for deals at the "Connected" stage that have meetings scheduled in the next 7 days. Select 3-5 meetings that represent a mix:
- At least 1 discovery call
- At least 1 demo or follow-up call
- Different company sizes or industries if possible

For each selected meeting, record the founder's estimated prep time for their normal manual process. This is the baseline to measure reduction against.

### 2. Run the Account Research Brief Drill

For each selected meeting, run the the account research brief workflow (see instructions below) drill:

1. Pull the deal context from Attio (company, contacts, prior notes, pain points documented)
2. Enrich the account in Clay: firmographics, recent news, job openings, tech stack
3. Research each meeting attendee via Claygent: LinkedIn activity, career history, shared connections
4. Check for competitive intelligence in the deal record
5. Feed the assembled intelligence into Claude to generate the structured meeting brief
6. Store the brief as an Attio note on the deal tagged `meeting-brief`

Review the brief before each call. Note how long the entire process took (agent research + founder review) vs the founder's normal prep time.

### 3. Use the Brief in Real Meetings

**Human action required:** The founder uses the AI-generated brief in the actual meeting. During and after each call, take quick notes:

- Which brief sections were most useful? (questions, talk tracks, objection prep, stakeholder map)
- Which sections were inaccurate or irrelevant?
- Did the personalized opening land well?
- Were there topics the prospect raised that the brief did NOT prepare for?
- How many actionable insights from the brief were actually used in the conversation?
- What was the meeting outcome? (next step committed, follow-up needed, stalled, lost)

Log these notes in Attio as a note on the deal tagged `brief-feedback`.

### 4. Score Brief Quality

After all 3-5 meetings, score each brief:

| Metric | How to Measure |
|--------|---------------|
| Prep time reduction | (manual_prep_minutes - ai_prep_minutes) / manual_prep_minutes |
| Actionable insights | Count of brief items the founder actually used in the call |
| Accuracy | Did the brief's predictions (objections, stakeholder roles, pain priorities) match reality? (1-5) |
| Usefulness | Would the founder use this brief format again? (1-5) |
| Outcome impact | Did the call achieve a better outcome than typical? (yes/no/same) |

### 5. Evaluate Against Threshold

Run the `threshold-engine` drill to aggregate results:

- Average prep time reduction across all test meetings. Target: >=50%.
- Average actionable insights per call. Target: >=3.
- If both thresholds are met: PASS. Proceed to Baseline.
- If only one threshold is met: iterate. Which data sources were weak? Which brief sections need prompt improvement? Adjust and re-run on 3 more meetings.
- If neither threshold is met: the meeting type may not benefit from AI prep, or the intelligence sources need significant improvement. Diagnose root cause before re-running.

## Time Estimate

- 0.5 hours: Select test meetings and record baseline prep times
- 3 hours: Run account-research-brief drill for 3-5 meetings (~30-40 min each including review)
- 1 hour: Post-meeting scoring and notes (15-20 min per meeting)
- 0.5 hours: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal context, brief storage, feedback notes | Free plan (up to 3 users) or $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — company research, contact research, news signals | $185/mo (Launch, 15K actions) — [clay.com/pricing](https://www.clay.com/pricing) |
| Anthropic API | AI — brief generation from intelligence profile | Usage-based, ~$0.05 per brief — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| PostHog | Analytics — event tracking for threshold evaluation | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost this level:** ~$0-5 incremental. Clay and Attio likely already in stack. Anthropic API cost for 5 briefs is under $0.50.

## Drills Referenced

- the account research brief workflow (see instructions below) — assemble account intelligence from CRM and enrichment sources, then generate a structured meeting brief with talking points, questions, objection prep, and agenda
- `threshold-engine` — evaluate test results against the pass threshold using Attio and PostHog data
