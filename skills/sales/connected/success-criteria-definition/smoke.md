---
name: success-criteria-definition-smoke
description: >
  Success Criteria Definition — Smoke Test. Manually run success criteria workshops with 5-8
  Connected-stage deals. Use AI extraction from discovery call transcripts to draft criteria,
  then co-create measurable success plans with prospects in 30-minute workshops. Validate that
  deals with defined criteria show higher close rates than those without.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=5 deals with mutual success plans agreed, with >=3 quantifiable criteria per deal and >=60% of criteria having achievability score >60"
kpis: ["Success criteria definition rate", "Average criteria count per deal", "Average achievability score", "Prospect agreement rate", "Close rate (criteria vs no-criteria deals)"]
slug: "success-criteria-definition"
install: "npx gtm-skills add sales/connected/success-criteria-definition"
drills:
  - success-criteria-workshop
  - threshold-engine
---

# Success Criteria Definition — Smoke Test

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Prove that co-creating measurable success criteria with prospects during the Connected stage produces a leading indicator of better deal outcomes. At this level, the agent prepares AI-extracted draft criteria from discovery transcripts — the founder conducts the workshop conversations. No automation, no always-on processes.

**Pass threshold:** >=5 deals with mutual success plans agreed, with >=3 quantifiable criteria per deal and >=60% of criteria having achievability score >60.

## Leading Indicators

- AI extraction produces >=3 draft criteria per discovery transcript
- Prospects agree to schedule the 30-minute workshop call (>=70% acceptance rate)
- During workshops, prospects add or refine criteria (engagement signal — they care about defining success)
- At least 1 prospect references the mutual success plan in a follow-up conversation
- Deals with defined criteria show any forward momentum compared to the control group

## Instructions

### 1. Select 5-8 Active Deals for the Test

Query Attio for deals currently at Connected stage that have at least 1 recorded discovery call in Fireflies. Choose deals where:
- The champion or primary contact is engaged (responded to last outreach within 7 days)
- The deal has enough context to define success (not just an intro call — needs substantive discovery)
- A mix of deal sizes and industries if possible (tests whether the approach generalizes)

Log these as the test cohort in Attio. Identify 5 comparable Connected-stage deals as the control group (no success criteria intervention — business as usual).

### 2. Run the Success Criteria Workshop Drill

Run the `success-criteria-workshop` drill for each test deal:

**Pre-call (agent executes):**
- Retrieve the Fireflies transcript for each deal's discovery call(s)
- Run `success-criteria-extraction` to generate 3-5 draft criteria per deal
- Review achievability scores: remove any criterion scored <30, flag those between 30-60
- Store draft criteria in Attio as a note tagged `success-criteria-draft`
- Generate a Cal.com booking link for a 30-minute "Success Criteria Workshop"
- Send the booking link to the champion with a brief message: "I'd like to spend 30 minutes making sure we're aligned on what success looks like for {company}. No pitch — just making sure we measure the right things."

**Workshop call (founder executes):**

**Human action required:** The founder conducts each 30-minute workshop. Use the AI-prepared draft as a conversation starter, not a script. The goal is collaborative — let the prospect define what matters to them, then sharpen it into measurable criteria together.

Workshop structure:
1. Share the 2-3 strongest draft criteria: "Based on our conversation, here's what I think success looks like for you. Am I on track?"
2. Let the prospect react, modify, and add criteria
3. For each criterion, nail down: the specific metric, the target number, the timeline, and who on their team will measure it
4. Ask: "If we hit all of these, would you consider this a successful purchase?"
5. Agree on a review checkpoint (e.g., 30 days post-launch, 90 days post-launch)

**Post-call (agent executes):**
- Retrieve the workshop call transcript from Fireflies
- Run `success-criteria-extraction` again with the refined conversation
- Generate the mutual success plan document and store in Attio
- Update deal record: `success_criteria_status` = "defined", `success_criteria_count`, `avg_achievability_score`
- Fire PostHog events: `success_criteria_defined`, `mutual_success_plan_created`

### 3. Track Results for 1 Week

Over 7 days, monitor both the test and control groups:
- Log any deal stage changes in both groups
- Track whether prospects reference the success criteria in follow-up communications
- Note any deals where the success criteria conversation surfaced new information (hidden objections, additional stakeholders, budget constraints)
- Monitor whether the workshop call led to a next step being booked (demo, technical deep dive, proposal)

### 4. Evaluate Against Threshold

Run the `threshold-engine` drill:
- Count: How many deals have mutual success plans? (target: >=5)
- Average criteria count per deal? (target: >=3)
- Average achievability score? (target: >=60% of criteria scored >60)
- Compare: stage progression for test deals vs control deals over the same week
- Note: close rate correlation requires longer observation — log the initial data but don't expect statistical significance in 1 week

If PASS: The approach produces signal. Proceed to Baseline to systematize and automate.
If FAIL: Diagnose — was the issue transcript quality (not enough discovery data), workshop scheduling (prospects didn't accept), or criteria quality (vague, unmeasurable)? Adjust and re-run.

## Time Estimate

- 1 hour: Select deals, set up test/control groups
- 2 hours: Run AI extraction for 5-8 deals (agent work — minimal human time)
- 3 hours: Conduct 5-8 workshop calls (30 min each, human time)
- 1 hour: Post-call processing and mutual plan generation (agent work)
- 1 hour: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal tracking, success criteria attributes, mutual plans | Free plan (up to 3 users) or $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Fireflies | Transcription — discovery and workshop call transcripts | Free (800 min/mo) or $18/user/mo (Pro) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics — event tracking for threshold evaluation | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Cal.com | Scheduling — workshop booking links | Free (1 calendar) or $12/user/mo (Team) — [cal.com/pricing](https://cal.com/pricing) |
| Anthropic API | AI — success criteria extraction from transcripts | Usage-based, ~$3/1M input tokens (Claude Sonnet) — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** ~$0-20. Most tools are on free tiers at this volume. Anthropic API usage for 5-8 extractions is <$1.

## Drills Referenced

- `success-criteria-workshop` — end-to-end workflow for preparing, conducting, and documenting success criteria conversations with prospects
- `threshold-engine` — evaluate test results against the pass threshold using Attio and PostHog data
