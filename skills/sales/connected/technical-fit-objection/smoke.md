---
name: technical-fit-objection-smoke
description: >
  Technical Fit Objection Handling — Smoke Test. Manually assess technical gaps on 5 active deals,
  build response strategies per gap type, and validate that structured technical objection handling
  resolves objections and advances deals faster than ad-hoc responses.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=5 technical objections handled with structured gap assessment in 1 week, >=60% reaching satisfactory resolution and deal advancement"
kpis: ["Technical objection resolution rate", "Workaround acceptance rate", "Deal progression after resolution", "Time to resolution (days)"]
slug: "technical-fit-objection"
install: "npx gtm-skills add sales/connected/technical-fit-objection"
drills:
  - threshold-engine
---

# Technical Fit Objection Handling — Smoke Test

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct

## Outcomes

Prove that systematically assessing technical gaps and matching each to a response strategy (roadmap commit, workaround demo, custom dev scope, or honest no-fit) produces better resolution rates than ad-hoc responses. At this level, the agent runs the gap assessment and generates response plans — the founder executes the technical conversations manually. No automation, no always-on.

**Pass threshold:** >=5 technical objections handled with structured gap assessment in 1 week, >=60% reaching satisfactory resolution and deal advancement.

## Leading Indicators

- Gap assessments completed for all 5 deals within 24 hours of the technical objection being raised
- Each assessment produces a clear gap classification (no_gap, roadmap, workaround, custom_dev, no_fit) for every stated requirement
- Response plans include specific proof assets or commitments (not generic "we can do that")
- At least 3 of 5 prospects respond positively to the structured technical response (request next meeting, share additional requirements, introduce technical stakeholder)
- Deals where gap assessment was used show any forward movement vs deals where objections were handled ad-hoc

## Instructions

### 1. Select 5 Deals with Active Technical Objections

Query Attio for deals at the "Connected" stage where the prospect has raised technical concerns. Look for deals where:
- The prospect questioned a specific capability ("Do you integrate with X?", "Can you handle Y?")
- A technical evaluation is underway or stalled
- The prospect mentioned a competitor's technical advantage
- A feature gap was identified during a demo

If fewer than 5 deals have active technical objections, include deals approaching technical discovery where objections are likely (based on the prospect's tech stack complexity or industry requirements).

Log these 5 deals as the test cohort. Identify 3-5 comparable deals as the control group (handle objections without the structured assessment).

### 2. Run Technical Gap Assessment

Run the the technical gap assessment workflow (see instructions below) drill for each of the 5 test deals:

- Pull all technical requirements from call transcripts, emails, and deal notes
- If call transcripts exist, run the call transcript tech requirements extraction workflow (see instructions below) to get structured requirements
- If no transcripts exist, extract requirements manually from deal notes in Attio
- Match each requirement against the product capability matrix
- Classify every gap: `no_gap`, `roadmap`, `workaround_available`, `custom_dev_required`, `partner_solution`, `no_fit`
- Score gap severity: `none`, `low`, `medium`, `high`, `dealbreaker`
- Generate a response strategy for each gap with specific proof needed
- Store the gap assessment and response plan as an Attio note on the deal

Review the output manually. For each deal, identify the 1-3 highest-severity gaps that need immediate attention.

### 3. Execute Technical Objection Responses

**Human action required:** The founder personally delivers the technical objection responses. This is intentionally manual — the goal is to test whether structured gap assessment produces better outcomes before investing in automation.

For each deal, follow the response plan:

**For roadmap gaps:**
1. Read the response plan specifying the planned delivery date
2. Present the roadmap timeline to the prospect: "This capability is planned for {quarter}. Here is the product brief showing the spec."
3. If the prospect needs a contractual commitment, draft a roadmap commitment clause
4. Log in Attio: `roadmap_commitment_made` with the feature, date, and whether a contract clause was requested

**For workaround gaps:**
1. Read the alternative approach described in the response plan
2. Demonstrate the workaround live on a call, or send a recorded walkthrough
3. Gauge the prospect's reaction: does the workaround satisfy their need or is it insufficient?
4. Log in Attio: `workaround_demonstrated` with the prospect's response (accepted, partially_accepted, rejected)

**For custom development gaps:**
1. Read the scoping estimate in the response plan
2. Present the custom development option: effort, timeline, cost (if any), and what it achieves
3. Log in Attio: `custom_dev_scoped` with the prospect's interest level

**For no-fit gaps:**
1. Acknowledge the gap honestly: "This is not something we do today or plan to build"
2. If the gap is not a dealbreaker for the prospect, continue the deal
3. If it is a dealbreaker, document the loss reason for product feedback
4. Log in Attio: `no_fit_acknowledged` with whether it killed the deal

### 4. Track Responses for 1 Week

Over 7 days, monitor responses and deal movement for both test and control cohorts:
- Log every technical objection response outcome in Attio with resolution status (resolved, partially_resolved, unresolved, deal_lost)
- Track whether the prospect: booked a follow-up technical call, introduced a technical stakeholder, moved forward with evaluation, or stalled/exited
- For control deals, track stage progression over the same week without structured assessment

### 5. Evaluate Against Threshold

Run the `threshold-engine` drill to compare test vs control:
- Count deals where technical objections were resolved or partially resolved
- Calculate resolution rate: resolved / total objections handled
- Compare deal progression: test cohort vs control cohort
- Pass threshold: >=5 objections handled AND >=60% resolved with deal advancement

If PASS: The structured gap assessment approach is validated. Proceed to Baseline.
If FAIL: Diagnose — was the issue gap classification accuracy (wrong response strategy), proof quality (unconvincing evidence), or timing (too slow to respond)? Adjust and re-run.

## Time Estimate

- 1 hour: Select deals and set up test/control groups
- 2 hours: Run technical gap assessment drill (requirements extraction + capability matching)
- 1.5 hours: Execute manual technical objection responses across 5 deals
- 0.5 hours: Daily response monitoring (5 min/day x 7 days)
- 1 hour: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal tracking, gap assessment storage, objection logging | Free plan (up to 3 users) or $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — tech stack detection for requirement prediction | $185/mo (Launch) — [clay.com/pricing](https://www.clay.com/pricing) |
| Fireflies | Transcription — call transcript extraction for requirements | Free (800 min/mo) or $10/user/mo (Pro, annual) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics — event tracking for threshold evaluation | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API | AI — gap classification and response generation | Claude Sonnet 4.6: $3/$15 per 1M tokens — [claude.com/pricing](https://claude.com/pricing) |

**Estimated play-specific cost this level:** $0-5 incremental (Clay, Fireflies, and Attio likely already in stack; Anthropic API usage minimal at 5 deals).

## Drills Referenced

- the technical gap assessment workflow (see instructions below) — assess prospect technical requirements against product capabilities, classify gaps by severity, and generate response strategies per gap type
- `threshold-engine` — evaluate test results against the pass threshold using Attio and PostHog data
