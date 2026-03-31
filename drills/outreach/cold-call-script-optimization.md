---
name: cold-call-script-optimization
description: Continuously analyze call transcripts, extract objection patterns, score script variants, and generate improved cold call scripts based on conversion data
category: Outreach
tools:
  - PostHog
  - Attio
  - n8n
  - Fireflies
  - Anthropic
fundamentals:
  - posthog-custom-events
  - posthog-dashboards
  - posthog-anomaly-detection
  - attio-deals
  - attio-notes
  - n8n-scheduling
  - n8n-workflow-basics
  - fireflies-transcription
  - fireflies-action-items
  - hypothesis-generation
  - experiment-evaluation
---

# Cold Call Script Optimization

This drill creates an always-on feedback loop that ingests call transcripts, extracts what works and what fails, and generates improved script variants. It is the play-specific monitoring layer that feeds structured cold-calling insights into the `autonomous-optimization` drill at Durable level.

## Prerequisites

- Fireflies transcribing all outbound calls
- PostHog tracking call events (`call_attempted`, `call_connected`, `call_meeting_booked`)
- Attio with call dispositions and deal outcomes logged
- At least 4 weeks of call data from Scalable level
- n8n instance running

## Steps

### 1. Build the transcript analysis pipeline

Create an n8n workflow triggered daily via `n8n-scheduling`:

1. Pull all new call transcripts from Fireflies API using `fireflies-transcription`
2. For each connected call transcript, extract structured data using Claude:
   - **Opener used**: which script variant (A/B/C)
   - **Signal referenced**: what buying signal the caller mentioned (funding, hiring, tech change, etc.)
   - **Objections raised**: categorize into standard buckets (not interested, have something, bad timing, send email, who are you)
   - **Objection handling outcome**: did the caller recover (continued conversation) or lose (call ended)
   - **Talk ratio**: percentage of time prospect vs. caller spoke
   - **Meeting outcome**: booked, follow-up requested, rejected, callback
   - **Call duration**: total seconds
3. Store extracted data as structured PostHog events using `posthog-custom-events`:
   - `call_transcript_analyzed` with all properties above
4. Store a summary note in Attio on the contact record using `attio-notes`

### 2. Build objection frequency tracking

Using `posthog-dashboards`, create a dashboard panel "Cold Call Objection Patterns" with:

- Objection frequency distribution (bar chart by category)
- Objection recovery rate by category (what percentage of each objection type leads to continued conversation)
- Objection frequency trend by week (are new objections emerging?)
- Objection-to-meeting rate: for calls where an objection was raised, what percentage still converted to a meeting
- Signal-to-objection correlation: which signals trigger which objections

Set anomaly detection via `posthog-anomaly-detection` for:
- New objection category appearing in >10% of calls (emerging market shift)
- Recovery rate on any objection category dropping below 20% (script needs updating)
- Talk ratio trending above 70% caller-side (caller is pitching, not listening)

### 3. Score script variants

Track each script variant (opener + problem statement + CTA combination) as a named variant in PostHog. For each variant, compute:

- Connect-to-conversation rate (call lasted >60 seconds)
- Conversation-to-meeting rate
- Average call duration
- Objection frequency
- Prospect talk ratio

Using `posthog-dashboards`, create a variant leaderboard panel showing all active variants ranked by meeting conversion rate. Minimum 20 calls per variant before ranking.

### 4. Generate improved script variants

Create an n8n workflow triggered weekly via `n8n-scheduling`:

1. Pull the variant leaderboard from PostHog
2. Pull the top 5 objections and their recovery rates
3. Pull the 3 best-performing transcripts (highest talk ratio + meeting booked) from Fireflies
4. Run `hypothesis-generation` with this context:
   - Current best variant's opener, problem statement, CTA
   - Most common unrecovered objections
   - Patterns from best-performing calls
   - Prospect segments where conversion is lowest
5. Output: 1-2 new script variant proposals with specific language changes and the rationale
6. Store the proposals in Attio as campaign notes
7. Post to Slack for founder review before activating

**Human action required:** The founder reviews proposed script changes and approves activation. The agent does not deploy new scripts without approval since the founder is the one making the calls.

### 5. Track script evolution over time

Maintain a version history in Attio: each script variant gets a record with creation date, hypothesis that inspired it, performance metrics, and status (active/retired/testing). This creates an institutional memory of what has been tried, what worked, and what failed — preventing the optimization loop from re-testing failed approaches.

### 6. Generate the weekly call optimization brief

As part of the weekly n8n workflow:

```
## Cold Call Optimization Brief — Week of {date}

### Call Volume & Conversion
- Calls attempted: {n} | Connected: {n} ({pct}%) | Meetings: {n} ({pct}%)
- Week-over-week: volume {delta}%, connect rate {delta}%, meeting rate {delta}%

### Script Variant Performance
| Variant | Calls | Connect Rate | Meeting Rate | Avg Duration | Status |
|---------|-------|-------------|-------------|-------------|--------|
| {name}  | {n}   | {pct}%      | {pct}%      | {sec}s      | {status} |

### Objection Landscape
- Top objection: {category} ({pct}% of calls) — recovery rate: {pct}%
- Emerging objection: {category} (up {pct}% this week)
- Weakest recovery: {category} at {pct}% — recommended script adjustment: {suggestion}

### Best Call Windows
- Highest connect rate: {day} {time_range} ({pct}%)
- Highest meeting rate: {day} {time_range} ({pct}%)

### Signal Effectiveness
- Best signal: {signal_type} — {pct}% meeting rate
- Worst signal: {signal_type} — {pct}% meeting rate (consider deprioritizing)

### Proposed Changes
- {description of proposed script variant and rationale}

### Convergence Status
- Consecutive minor improvements (<2%): {count}/3
```

Post to Slack and store in Attio.

## Output

- Daily transcript analysis with structured extraction
- Objection pattern tracking and anomaly detection
- Script variant leaderboard with statistical ranking
- Weekly script improvement proposals backed by data
- Weekly optimization brief connecting call behavior to outcomes
- Version-controlled script history preventing repeated experiments

## Triggers

Daily transcript analysis runs via n8n cron at 7am. Weekly optimization brief and script proposals run Monday at 8am. Anomaly alerts fire in real-time when thresholds are breached.
