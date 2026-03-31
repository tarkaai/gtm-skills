---
name: champion-identification-smoke
description: >
  Champion Identification & Development — Smoke Test. Manually identify and vet potential internal
  champions at 5 target accounts using enrichment signals and direct outreach. Validate that
  champion-led deals show faster progression than non-champion deals.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=3 deals with identified champion candidates who responded positively, and >=30% faster stage progression vs non-champion deals in 1 week"
kpis: ["Champion candidates identified per account", "Champion response rate", "Deal velocity (champion vs non-champion)", "Champion engagement score"]
slug: "champion-identification"
install: "npx gtm-skills add sales/connected/champion-identification"
drills:
  - champion-profiling
  - threshold-engine
---

# Champion Identification & Development — Smoke Test

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Prove that systematically identifying and reaching potential champions produces a leading indicator of faster deal progression. At this level, the agent helps identify and score candidates — the founder executes outreach manually. No automation, no budget beyond the default stack.

**Pass threshold:** >=3 deals with identified champion candidates who responded positively, and >=30% faster stage progression vs non-champion deals in 1 week.

## Leading Indicators

- Champion candidates scored 75+ found at >=4 of 5 target accounts
- At least 1 champion candidate per account responds to manual outreach
- Response sentiment is positive or curious (not "not interested" or "wrong person")
- Deals where champions were contacted show any forward movement (next meeting booked, new stakeholder introduced, information shared)

## Instructions

### 1. Select 5 Active Deals for the Test

Query Attio for 5 deals currently at the "Connected" stage. Choose deals that are:
- Similar in deal size (control for value)
- At companies with 50+ employees (enough org complexity for champions to matter)
- Not already multi-threaded (currently single-contact deals)

Log these 5 deals as the test cohort. Also identify 5 comparable deals as the control group (no champion intervention).

### 2. Run Champion Profiling

Run the `champion-profiling` drill for each of the 5 test deals:
- Export the 5 target companies to Clay
- Find 3-5 champion candidates per account using the champion signal search
- Score candidates on behavioral signals (frustration, competitor engagement, learning signals, job change)
- Push scored candidates to Attio with `champion_status` = "Candidate"
- Generate AI briefings for Hot candidates (score 75+)

Review the output manually. For each account, select the strongest 1-2 candidates to contact.

### 3. Execute Manual Outreach

**Human action required:** The founder personally reaches out to each selected champion candidate. This is intentionally manual — the goal is to test whether the champion thesis works before investing in automation.

For each candidate:
1. Read the AI-generated champion briefing in Attio
2. Send a personalized email or LinkedIn message referencing their specific signal (the pain point they posted about, the competitor they engaged with, or the role change they made)
3. Frame the outreach around helping them, not selling: "I noticed you're dealing with {pain}. We've helped teams like yours with {specific approach}. Would a quick conversation be useful?"
4. Log the outreach in Attio: create a note with the message sent, channel used, and date

### 4. Track Responses for 1 Week

Over 7 days, monitor responses and deal movement:
- Log every reply in Attio with sentiment (positive, neutral, negative, no response)
- Track whether any champion candidate: booked a meeting, asked a question, forwarded your message, introduced a colleague
- For the 5 control deals, track stage progression over the same week (do nothing different for these)

### 5. Evaluate Against Threshold

Run the `threshold-engine` drill to compare test vs control:
- Count deals where at least 1 champion candidate responded positively
- Calculate average stage progression for test deals vs control deals
- Pass threshold: >=3 of 5 test deals had a positive champion response AND test deals showed >=30% faster progression

If PASS: The champion thesis is validated. Proceed to Baseline.
If FAIL: Diagnose — was the issue candidate selection (wrong people), messaging (wrong angle), or timing (wrong moment)? Adjust and re-run.

## Time Estimate

- 1 hour: Select deals and set up test/control groups
- 2 hours: Run champion profiling drill (Clay enrichment + scoring)
- 1.5 hours: Manual outreach to 10-15 candidates across 5 accounts
- 0.5 hours: Daily response monitoring (5 min/day x 7 days)
- 1 hour: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal tracking, champion attributes, notes | Free plan (up to 3 users) or $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — champion signal search and scoring | $185/mo (Launch, 15K actions) — [clay.com/pricing](https://www.clay.com/pricing) |
| PostHog | Analytics — event tracking for threshold evaluation | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost this level:** $0 incremental (Clay and Attio likely already in stack for other plays). If Clay is new: ~$185/mo.

## Drills Referenced

- `champion-profiling` — identify and score champion candidates at target accounts using Clay behavioral signals and AI briefing generation
- `threshold-engine` — evaluate test results against the pass threshold using Attio and PostHog data
