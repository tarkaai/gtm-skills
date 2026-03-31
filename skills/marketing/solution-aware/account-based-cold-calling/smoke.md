---
name: account-based-cold-calling-smoke
description: >
  Account-Based Cold Calling — Smoke Test. Agent builds a researched target list of 50 solution-aware
  accounts, enriches with direct phone numbers and buying signals, generates personalized call scripts
  per account, and the founder executes 50 calls in 1 week. Validates that signal-driven cold calling
  to solution-aware prospects produces meetings at a rate worth automating.
stage: "Marketing > Solution Aware"
motion: "OutboundFounderLed"
channels: "Direct"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=2 meetings booked from 50 targeted calls in 1 week"
kpis: ["Connect rate", "Conversation rate (calls >60s)", "Meeting conversion rate"]
slug: "account-based-cold-calling"
install: "npx gtm-skills add marketing/solution-aware/account-based-cold-calling"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-call-framework
  - threshold-engine
---

# Account-Based Cold Calling — Smoke Test

> **Stage:** Marketing > Solution Aware | **Motion:** OutboundFounderLed | **Channels:** Direct

## Outcomes

Prove that cold calling solution-aware accounts with signal-based personalization generates meetings worth pursuing. After 50 calls in 1 week, at least 2 meetings booked with qualified decision-makers. The smoke test validates that this channel works for your ICP before investing in dialer infrastructure or automation.

## Leading Indicators

- Prospect list of 50 accounts with direct phone numbers and at least 1 buying signal each, built within first 2 days
- Call scripts generated with account-specific openers referencing buying signals
- Connect rate above 15% (reaching a live person on 8+ of 50 calls)
- At least 3 conversations lasting longer than 60 seconds (prospects engaging, not immediately hanging up)
- At least 1 follow-up requested even if not an immediate meeting (signal that the message resonates)

## Instructions

### 1. Define your cold calling ICP

Run the `icp-definition` drill. For account-based cold calling, the ICP must include:
- **Company profile**: size, industry, funding stage, technology stack
- **Buyer persona**: job title, seniority level, department (these are the people you will call)
- **Solution awareness signals**: prospects must already know the category of solution you offer — they are evaluating options, not unaware of the problem. This means targeting accounts that show signals like competitor usage, relevant job postings, or content engagement with solution-category topics.
- **Phone accessibility**: roles where direct dial numbers are obtainable (VP and above are harder; director-level and individual contributors are easier via enrichment)

Document the ICP in Attio as a note on a campaign record named `account-based-cold-calling`.

Estimated time: 1 hour.

### 2. Build and enrich the prospect list

Run the `build-prospect-list` drill to source 50 contacts matching your ICP from Apollo and Clay. Then run the `enrich-and-score` drill to:

1. Enrich every contact with direct phone numbers using Clay's enrichment waterfall (Cognism -> Lusha -> People Data Labs -> Apollo). If a contact has no phone number after the waterfall, replace them — phone numbers are non-negotiable for a cold calling play.
2. Enrich with buying signals: recent funding (Crunchbase), job changes in target department (LinkedIn), hiring activity (job board scraper), competitor technology detected (BuiltWith).
3. Score each prospect 0-100 using the ICP weights defined in step 1. Keep the top 50 with the strongest signal + fit combination.
4. Push the final list to Attio with phone numbers, signal data, and scores attached to each contact record.

Target: 50 contacts, all with verified phone numbers, all with at least 1 active buying signal.

Estimated time: 2 hours.

### 3. Generate account-specific call scripts

Run the `cold-call-framework` drill. For each of the 50 prospects, the agent generates a personalized call script using the framework:

- **Opener**: Reference the specific buying signal. "I noticed [company] just raised a Series B — congrats" or "I saw you're hiring 3 data engineers — sounds like the team is scaling."
- **Problem statement**: Tie the signal to the problem your product solves, in the prospect's language. One sentence.
- **Question**: An open-ended question about how they handle the problem today. The goal is to get the prospect talking.
- **Bridge**: One-sentence description of how you help, only if there is interest.
- **CTA**: "Would it make sense to grab 15 minutes on Thursday to explore this?"

Prepare responses for the top 5 objections: "not interested," "we already have something," "send me an email," "bad timing," "who are you?" For each, acknowledge, ask one clarifying question, pivot or exit gracefully.

Store each prospect's script in Attio as a note on their contact record so the founder can pull it up during call blocks.

Estimated time: 1.5 hours.

### 4. Execute call blocks

**Human action required:** The founder makes the calls. The agent does not make calls — this is a founder-led motion where the founder's credibility and context are the differentiator.

Call execution guidelines:
- Block 2 hours per day for calling, 5 days = 10 calls per day
- Call between 8-10am and 4-5pm in the prospect's timezone (highest connect windows)
- Before each call, review the prospect's script and signal data in Attio (60 seconds)
- After each call, log the outcome immediately in Attio:
  - Disposition: `connected`, `voicemail`, `gatekeeper`, `no_answer`, `wrong_number`
  - If connected: duration, objections raised, outcome (`meeting_booked`, `follow_up_requested`, `not_interested`, `callback_later`)
  - Notes: any relevant context the prospect shared
- If voicemail: leave a 15-second message referencing the signal. "Hi [name], this is [founder] from [company]. I noticed [signal]. Would love 15 minutes to discuss [problem]. My number is [number]."
- If no answer after 2 attempts on different days/times, move to the next prospect.

Estimated time: 2.5 hours (5 days x 30 min call blocks).

### 5. Evaluate against threshold

Run the `threshold-engine` drill to evaluate results against the pass threshold: >=2 meetings booked from 50 targeted calls in 1 week.

The threshold engine pulls call outcomes from Attio and computes:
- Total calls attempted
- Connect rate (connected / attempted)
- Conversation rate (calls >60 seconds / connected)
- Meeting conversion rate (meetings / connected)
- Which signals correlated with connects and meetings
- Which objections were most common and how they were handled

If PASS (>=2 meetings): Document the winning signals, best call times, and effective openers. Proceed to Baseline.

If FAIL: Diagnose the failure point:
- Low connect rate (<15%): phone number quality issue or bad call timing. Re-enrich numbers or shift call windows.
- Low conversation rate (<30% of connects): opener is not compelling. Rewrite openers with stronger signal references.
- Low meeting rate (conversations but no meetings): CTA is weak or prospect is not truly solution-aware. Tighten ICP to higher-intent signals.

Adjust and re-run the smoke test.

Estimated time: 1 hour.

## Time Estimate

- ICP definition: 1 hour
- Prospect list build and enrichment: 2 hours
- Script generation: 1.5 hours
- Call execution (5 days x 30 min): 2.5 hours
- Threshold evaluation: 1 hour

**Total: ~8 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — contact records, call logging, campaign tracking | Standard stack (excluded) |
| PostHog | Event tracking for call outcomes | Standard stack (excluded) |
| Clay | Prospect enrichment, phone number waterfall, signal detection | Growth: $495/mo. [clay.com/pricing](https://www.clay.com/pricing) |
| Cal.com | Meeting scheduling for booked calls | Standard stack (excluded) |

**Play-specific cost: Free** (Clay is standard stack; no dialer needed at Smoke — founder dials from personal phone or Zoom)

## Drills Referenced

- `icp-definition` — defines the target company and buyer persona with solution-awareness criteria
- `build-prospect-list` — sources and imports 50 contacts from Apollo into Clay
- `enrich-and-score` — enriches with phone numbers, signals, and scores; pushes to Attio
- `cold-call-framework` — generates personalized call scripts with signal-based openers and objection handling
- `threshold-engine` — evaluates call outcomes against the >=2 meetings pass threshold
