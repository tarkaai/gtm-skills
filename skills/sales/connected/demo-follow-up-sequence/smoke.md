---
name: demo-follow-up-sequence-smoke
description: >
  Demo Follow-Up Sequence — Smoke Test. Agent extracts demo signals from a Fireflies transcript,
  assembles a personalized recap email with resources and next steps, and the founder executes
  the follow-up cadence manually on 8+ demos to validate that structured follow-ups accelerate
  deal progression.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Email, Direct"
level: "Smoke Test"
time: "6 hours over 2 weeks"
outcome: ">=8 demos followed up within 2 hours with structured recap, >=50% scheduling a next step within 10 days"
kpis: ["Recap delivery speed (hours after demo)", "Follow-up completion rate", "Response rate by touch", "Next step scheduling rate", "Content engagement rate"]
slug: "demo-follow-up-sequence"
install: "npx gtm-skills add sales/connected/demo-follow-up-sequence"
drills:
  - demo-recap-assembly
  - threshold-engine
---

# Demo Follow-Up Sequence — Smoke Test

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Email, Direct

## Outcomes

Prove that assembling a structured, personalized demo recap within 2 hours of a demo — referencing the prospect's specific pains, questions, and interest signals — produces a measurably higher next-step booking rate than ad-hoc follow-ups. At this level, the agent generates the recap content; the founder reviews, sends, and executes the follow-up touches manually.

**Pass threshold:** >=8 demos followed up within 2 hours with structured recap, >=50% scheduling a next step within 10 days.

## Leading Indicators

- Recap emails assembled within 30 minutes of transcript availability for >=80% of demos
- Recap emails reference >=2 specific pain points or questions from the demo transcript
- Prospects open the recap email within 4 hours (engagement signal)
- At least 1 prospect per week responds positively to a follow-up touch before the next step is formally proposed
- Loom recap videos (if sent) achieve >50% watch rate

## Instructions

### 1. Verify Prerequisites

Confirm that Fireflies is recording and transcribing demo calls. Check that Attio has deal records for each upcoming demo with at least: company name, contact name, contact email, deal stage. Ensure Cal.com booking links are set up for next-step meeting types (technical deep dive, proposal review, stakeholder demo).

If Fireflies is not configured, set it up: connect to your calendar, enable auto-join for meetings with "demo" in the title, and verify transcripts appear within 30 minutes of call end.

### 2. Run Demo Recap Assembly for Each Demo

After each demo call, run the `demo-recap-assembly` drill:

1. Wait for the Fireflies transcript to become available (typically 10-30 minutes post-call)
2. The agent fetches the transcript, extracts demo signals (features shown, questions asked, concerns raised, interest signals, stakeholders mentioned, suggested next step)
3. The agent generates a personalized recap email: subject line, body with what-was-covered, questions-addressed, resources, and next-step proposal with Cal.com link
4. The agent stores the recap in Attio as a deal note and updates the deal record with extracted signals

Review the agent's output. Check that:
- Pain points and questions match what actually happened in the demo
- Resource recommendations are relevant to what the prospect asked about
- The suggested next step is appropriate for where the deal is
- The tone reads as a real founder email, not a template

**Human action required:** Edit the recap if needed and send it from your personal email within 2 hours of the demo ending. Do not send from a sequence tool — this is a founder email. After sending, update Attio: `demo_recap_sent: true`.

### 3. Execute the Follow-Up Cadence Manually

For each demo, execute this 5-touch cadence manually over 10 days. The agent prepares the content; you send it.

**Day 0 (within 2 hours):** Send the recap email (Step 2).

**Day 1:** Send a brief check-in: "Any questions come up since our call?" If the agent identified unanswered questions from the demo, include the answers now.

**Day 3:** Send a value asset matched to the demo context. The agent selects the asset based on what the prospect showed interest in:
- Technical questions → integration guide or API docs
- Mentioned stakeholders → one-page executive summary they can forward
- Specific use case interest → relevant case study
- Pricing/ROI discussion → ROI calculator pre-filled with their numbers

**Day 5-7:** Check engagement. If the prospect opened emails or clicked links, propose the next step directly with a Cal.com link. If no engagement, try a different angle — reference something from the demo not covered in previous touches.

**Day 10:** If no response, send a brief momentum check: "Is {solving their primary pain} still a priority this quarter?"

**Human action required:** Send each touch manually. Log every send and response in Attio with a note: touch number, content type, response (if any), and sentiment.

### 4. Track Results

After each follow-up touch, log the outcome in Attio:
- `touch_number`: 0-4
- `touch_type`: recap, check_in, value_asset, engagement_based, momentum_check
- `response`: none, positive, neutral, negative
- `next_step_booked`: true/false
- `next_step_type`: technical_deep_dive, proposal, stakeholder_demo, pilot, none

Note which follow-up touches generate the most responses and which assets drive the most engagement.

### 5. Evaluate Against Threshold

After completing follow-up sequences on >=8 demos over 2 weeks, run the `threshold-engine` drill:

1. Pull all deals with `demo_recap_sent: true` in the evaluation window
2. Count: total recaps sent, sent within 2 hours, responses received, next steps booked
3. Calculate: recap delivery speed, response rate by touch number, next-step scheduling rate
4. Compare against threshold: >=8 demos followed up AND >=50% scheduled a next step

If PASS: The structured follow-up approach works. Proceed to Baseline to add always-on tooling.
If FAIL: Diagnose — was the issue recap quality (prospects not engaging with content), timing (too slow), or targeting (wrong next step proposed)? Adjust and re-run.

## Time Estimate

- 0.5 hours: Verify prerequisites and configure Fireflies
- 3 hours: Run demo-recap-assembly after each demo (~20 min per demo x 8-10 demos)
- 2 hours: Execute manual follow-up cadence (~15 min per touch x 8 deals)
- 0.5 hours: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Fireflies | Demo call transcription and signal extraction | Free (800 min/mo) or $18/user/mo Pro — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Attio | CRM — deal tracking, recap storage, follow-up logging | Free (up to 3 users) or $29/user/mo Plus — [attio.com/pricing](https://attio.com/pricing) |
| PostHog | Event tracking for threshold evaluation | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Cal.com | Booking links for next-step meetings | Free (1 user) or $12/user/mo — [cal.com/pricing](https://cal.com/pricing) |
| Loom | Optional recap video recording | Free (25 videos) or $15/user/mo Business — [loom.com/pricing](https://www.loom.com/pricing) |

**Estimated play-specific cost this level:** $0 incremental if Fireflies free tier covers your demo volume. If you exceed 800 min/mo: ~$18/mo for Fireflies Pro.

## Drills Referenced

- `demo-recap-assembly` — extract demo signals from Fireflies transcript and generate a personalized recap email with resources and next steps
- `threshold-engine` — evaluate follow-up results against the pass threshold using Attio and PostHog data
