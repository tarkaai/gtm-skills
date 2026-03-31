---
name: win-loss-analysis-smoke
description: >
  Win/Loss Analysis Program — Smoke Test. Manually interview 4+ recently closed deal contacts
  (won and lost) to validate that structured buyer interviews produce actionable insights
  about why deals are won and lost.
stage: "Product > Retain"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=4 win/loss interviews completed and >=3 actionable insights identified within 1 week"
kpis: ["Interview completion rate", "Insights per interview", "Actionable insight quality", "Time from close to interview"]
slug: "win-loss-analysis"
install: "npx gtm-skills add product/retain/win-loss-analysis"
drills:
  - win-loss-interview-pipeline
  - win-loss-insight-extraction
  - threshold-engine
---
# Win/Loss Analysis Program — Smoke Test

> **Stage:** Product → Retain | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Prove that structured win/loss interviews produce real, actionable insights you can use to improve sales effectiveness and product direction. At this level, everything is manual. You personally interview 4+ recent deal contacts, extract insights, and validate that the signal is worth systematizing.

**Pass threshold:** >=4 win/loss interviews completed AND >=3 actionable insights identified within 1 week.

## Leading Indicators

- Interview request acceptance rate (target: >=40% of outreach leads to a scheduled call)
- Average insights extracted per interview (target: >=2 actionable insights per interview)
- Interviewee willingness to be candid (are they giving real answers or polite deflections?)
- Time from outreach to completed interview (target: <5 business days)

## Instructions

### 1. Identify your first interview candidates

Manually query your Attio CRM for deals that closed in the last 30 days. Pull the `win-loss-interview-pipeline` drill's candidate identification logic, but do it by hand: list all Closed Won and Closed Lost deals, grab the primary contact for each, and select 8-10 candidates (mix of wins and losses). Prioritize deals where you had a real evaluation — skip one-call closes and no-shows.

**Human action required:** Review the candidate list. Remove anyone with a strained relationship or active support escalation. Aim for a 50/50 mix of won and lost deals.

### 2. Send personal outreach

Do NOT use automated sequences yet. Send personal emails from the founder or sales lead to each candidate. For won deals: "Thanks for choosing us. I'd love 20 minutes to understand what worked and what almost didn't." For lost deals: "No sales pitch, I promise. I genuinely want to understand what drove your decision so we can get better."

Include a Cal.com booking link (create one using the `calcom-booking-links` fundamental with a 20-minute event type). If they decline a call, offer the Typeform survey as a fallback (set up using the `typeform-win-loss-survey` fundamental from the `win-loss-interview-pipeline` drill).

### 3. Conduct the interviews

**Human action required:** Conduct each 20-minute interview personally. Have Fireflies join to transcribe (configure using the `fireflies-transcription` fundamental). Follow this structure:

- Minutes 0-2: Thank them. Explain this is confidential, for internal improvement only.
- Minutes 2-5: "Walk me through how you first heard about us and your evaluation process."
- Minutes 5-10: "What were the top 3 factors in your decision?" Probe each factor.
- Minutes 10-15: "What competitors did you look at? What did they do well? What did we do better or worse?"
- Minutes 15-18: "If you could change one thing about our product or sales process, what would it be?"
- Minutes 18-20: "Anything else I should know?" Thank them.

Take notes during the call even with Fireflies running — capture your immediate impressions.

### 4. Extract insights from each interview

After each interview, run the `win-loss-insight-extraction` drill manually. Retrieve the Fireflies transcript, then use the Claude API (via the `transcript-insight-extraction` fundamental) to extract: outcome, primary reason, competitors mentioned, product feedback, sales process feedback, pricing feedback, decision criteria, actionable insights, sentiment score, and key quotes.

Store the structured insights as a tagged note on the deal in Attio. If you do not have the Anthropic API set up yet, do the extraction manually: read the transcript and fill in the same 10 fields by hand. The structure matters more than the automation at Smoke level.

### 5. Synthesize your findings

After completing 4+ interviews, review all extracted insights together. Look for patterns:
- Are the same competitors coming up repeatedly?
- Is there a consistent product gap that lost deals mention?
- Is there a feature or experience that won deals consistently praise?
- Are loss reasons concentrated in one category (price, features, process) or spread out?

Write a one-page summary: top 3 win reasons, top 3 loss reasons, most mentioned competitor, and 3 actionable changes you could make.

### 6. Evaluate against threshold

Run the `threshold-engine` drill to evaluate: did you complete >=4 interviews AND identify >=3 actionable insights? An "actionable insight" means a specific change you could make (not "improve the product" — that is not actionable; "add Slack integration — 3 of 4 lost prospects cited it as a dealbreaker" is actionable).

If PASS: Proceed to Baseline. You have validated that win/loss interviews produce signal.
If FAIL: Diagnose — was the issue low interview acceptance (outreach problem), shallow answers (interview technique problem), or no patterns (too few interviews)? Adjust and re-run.

## Time Estimate

- 1 hour: Identify candidates and set up Cal.com/Typeform/Fireflies
- 2 hours: Send outreach and manage scheduling
- 2 hours: Conduct 4 interviews (20 min each + buffer)
- 2 hours: Extract and analyze insights
- 1 hour: Synthesize findings and evaluate against threshold

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Query closed deals, store insights | Free tier or existing plan |
| Cal.com | Schedule interviews | Free tier (1 event type) |
| Fireflies | Transcribe interviews | Free tier (limited transcription) or Pro $10/mo/seat — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Typeform | Fallback survey for non-callers | Free tier (10 responses/mo) or Basic $25/mo — [typeform.com](https://www.typeform.com) |
| Claude API | Insight extraction (optional at Smoke) | ~$0.50 per transcript — [anthropic.com](https://console.anthropic.com) |

**Estimated play-specific cost:** Free (using free tiers) to ~$15 (if using Fireflies Pro for one month)

## Drills Referenced

- `win-loss-interview-pipeline` — Identifies candidates, sends outreach, schedules and records interviews
- `win-loss-insight-extraction` — Analyzes transcripts and extracts structured, categorized insights
- `threshold-engine` — Evaluates results against the pass threshold
