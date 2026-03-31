---
name: win-loss-analysis-baseline
description: >
  Win/Loss Analysis Program — Baseline Run. Automate interview scheduling and insight extraction
  so every closed deal triggers outreach, and transcripts are automatically analyzed. Prove the
  system produces consistent insights over 2 weeks of continuous operation.
stage: "Product > Retain"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "24 hours over 2 weeks"
outcome: ">=10 interviews completed, >=5 high-priority insights identified, and >=2 implemented changes over 2 weeks"
kpis: ["Interview completion rate", "Insights identified", "Changes implemented", "Win/loss reason distribution"]
slug: "win-loss-analysis"
install: "npx gtm-skills add product/retain/win-loss-analysis"
drills:
  - threshold-engine
---
# Win/Loss Analysis Program — Baseline Run

> **Stage:** Product → Retain | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Move from manual interviews to an always-on system. Every deal that closes (won or lost) automatically triggers outreach, interview scheduling, transcription, and insight extraction. Prove the system produces consistent, reliable insights over 2 continuous weeks and that those insights actually drive changes.

**Pass threshold:** >=10 interviews completed, >=5 high-priority insights identified, AND >=2 changes implemented based on insights over 2 weeks.

## Leading Indicators

- Automation trigger rate (every closed deal should fire the outreach workflow — target: 100%)
- Interview acceptance rate (target: >=30% of outreach converts to interview or survey)
- Insight extraction accuracy (spot-check: >=90% of AI-extracted insights match human review)
- Time from deal close to completed analysis (target: <10 business days end-to-end)
- Team engagement with insights (are people reading and acting on the win/loss notes in Attio?)

## Instructions

### 1. Deploy the automated interview pipeline

Run the full the win loss interview pipeline workflow (see instructions below) drill to build the always-on system:

- Configure the n8n workflow that triggers on Attio deal stage changes to Closed Won or Closed Lost
- Set up the Loops email sequences (won path and lost path) with Cal.com booking links and Typeform survey fallbacks
- Configure Fireflies to auto-join all calendar events booked through the win/loss Cal.com event type
- Test the full flow: manually move a test deal to Closed Won in Attio and verify the entire chain fires (outreach sent, booking link works, Fireflies joins, transcript generated)

### 2. Deploy automated insight extraction

Run the the win loss insight extraction workflow (see instructions below) drill with the automation workflow enabled:

- Build the n8n workflow that triggers on Fireflies transcript-ready webhook
- Build the parallel n8n workflow that triggers on Typeform submission webhook
- Both workflows call the Claude API for structured extraction, then store insights in Attio
- Configure Slack notifications for high-priority product-gap insights
- Test with a real transcript: run a test interview, wait for Fireflies to process, verify the n8n workflow fires, and check the Attio deal note

### 3. Process the Smoke-level backlog

If you have interviews from the Smoke test that were not processed through the automated pipeline, run them through now. This gives you a head start on the 10-interview target and validates the automation against known data.

### 4. Conduct interviews for 2 weeks

**Human action required:** Continue conducting interviews personally. The automation handles everything except the actual conversation. Check daily:
- Are outreach emails being sent for new closed deals? (Check Loops delivery logs)
- Are interviews being booked? (Check Cal.com bookings)
- Are transcripts being processed? (Check n8n execution logs)
- Are insights appearing on deal records in Attio?

If any step breaks, diagnose and fix. Common issues: Fireflies fails to join (calendar permission), n8n workflow errors (API rate limit), Typeform webhook not firing (URL misconfigured).

### 5. Generate your first win/loss report

After accumulating 10+ analyzed interviews, run the the win loss reporting workflow (see instructions below) drill manually:

- Pull all "win-loss-insight" tagged notes from Attio for the 2-week period
- Calculate aggregate metrics: win rate, top win/loss reasons, competitor frequency, insight category distribution
- Use Claude to synthesize patterns and generate recommendations
- Format the report and share with the sales team and product team

### 6. Implement changes based on insights

**Human action required:** From the report's recommended actions, select at least 2 changes to implement:

Possible changes by category:
- **Sales process:** Update your sales deck to address the #1 objection. Change your demo flow to highlight the feature buyers care most about. Adjust your follow-up cadence.
- **Messaging:** Rewrite your homepage hero based on what won deals say they value. Update battle cards with real competitor comparisons from buyer quotes.
- **Product:** File specific feature requests with direct buyer quotes. Reprioritize the roadmap based on what lost deals needed.
- **Pricing:** If pricing is a top loss reason, test a new packaging option or discount structure.

Document what you changed, when, and why (linked to specific insights). This creates the feedback loop you will measure at Scalable level.

### 7. Evaluate against threshold

Run the `threshold-engine` drill: >=10 interviews completed, >=5 high-priority insights, >=2 implemented changes.

If PASS: Proceed to Scalable. The system works and produces actionable intelligence.
If FAIL: Diagnose which metric fell short. Low interview count = outreach/acceptance problem. Low insight quality = extraction/interview technique problem. No changes implemented = organizational adoption problem.

## Time Estimate

- 6 hours: Set up automation (n8n workflows, Loops sequences, Fireflies config, Typeform webhooks)
- 2 hours: Test and debug the full pipeline end-to-end
- 8 hours: Conduct 10+ interviews over 2 weeks (20 min each + buffer)
- 4 hours: Monitor automation, fix issues, process backlog
- 2 hours: Generate first report and synthesize findings
- 2 hours: Implement changes and document the feedback loop

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal tracking, insight storage, reporting | Free tier or existing plan |
| Cal.com | Interview scheduling | Free tier — [cal.com](https://cal.com) |
| Fireflies | Interview transcription | Pro $10/mo/seat — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Typeform | Fallback survey | Basic $25/mo — [typeform.com](https://www.typeform.com) |
| Loops | Automated outreach sequences | Free (<1k contacts) or from $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Workflow automation | Free (self-hosted) or Starter €24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Claude API | Insight extraction | ~$0.50/transcript, est. $5-10/mo — [anthropic.com](https://console.anthropic.com) |

**Estimated play-specific cost:** ~$35-110/mo (Fireflies Pro + Typeform Basic + Loops free tier or paid + n8n self-hosted or Cloud + Claude API)

## Drills Referenced

- the win loss interview pipeline workflow (see instructions below) — Automated outreach, scheduling, recording for every closed deal
- the win loss insight extraction workflow (see instructions below) — AI-powered analysis of transcripts and surveys into structured insights
- the win loss reporting workflow (see instructions below) — Aggregate insights into a periodic report with patterns and recommendations
- `threshold-engine` — Evaluates results against the pass threshold
