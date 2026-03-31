---
name: demo-storytelling-framework-smoke
description: >
  Demo Storytelling Framework — Smoke Test. Manually build a small customer story library, select
  stories for 5 upcoming demos, restructure those demos around customer narratives instead of feature
  walkthroughs, and measure whether story-driven demos produce stronger engagement signals than
  traditional demos.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=5 storytelling demos delivered in 1 week with >=70% showing strong engagement signals (prospect relates to story, asks questions about the customer, or verbally commits to next step)"
kpis: ["Storytelling demo count", "Prospect engagement signal rate", "Story connection rate", "Demo-to-proposal conversion"]
slug: "demo-storytelling-framework"
install: "npx gtm-skills add sales/connected/demo-storytelling-framework"
drills:
  - story-library-curation
  - threshold-engine
---

# Demo Storytelling Framework — Smoke Test

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Product

## Outcomes

Prove that structuring demos around customer stories — rather than feature walkthroughs — produces stronger prospect engagement. At this level, the agent helps curate stories and prepare narrative-structured demo outlines. The founder delivers the demos and logs engagement signals manually. No automation, no Gong analysis.

**Pass threshold:** >=5 storytelling demos delivered in 1 week with >=70% showing strong engagement signals (prospect relates to story, asks questions about the customer, or verbally commits to next step).

## Leading Indicators

- Story library has >=3 approved stories covering at least 2 distinct ICP segments
- For each of the 5 demos, a customer story is selected that shares at least 1 pain theme with the prospect
- During demos, the prospect verbalizes connection to the customer story ("That sounds like us", "How did they handle...", "We have the same problem")
- Prospects ask more questions during story-driven demos than they did during prior feature walkthroughs
- Demos end with a committed next step more often than the baseline

## Instructions

### 1. Build the Initial Story Library

Run the `story-library-curation` drill to create your first set of customer stories:

- Identify 3-5 customers with strong, measurable results. Pull them from Attio: look for customers with high NPS, strong usage, or who have shared positive feedback.
- For each customer, check if a Fireflies transcript exists from a recent call (QBR, check-in, success review). If yes, extract the story from the transcript using Claude.
- If no transcript exists, interview the customer. Schedule a 20-minute call. Ask: What was your situation before? What did you try? What changed after using our product? What specific results can you share?
- Structure each story with: company, industry, headcount, challenge (in their words), solution approach, primary metric, secondary metrics, key quotes, and tags (industry, size bucket, pain themes, use case, stakeholder persona).
- Store all stories in Attio as structured records.

Validate: each story must have at least 1 quantified result and 1 direct customer quote. Stories without numbers or quotes are drafts, not approved stories.

### 2. Select Stories for 5 Upcoming Demos

Identify your next 5 scheduled demos from Attio deals in the Connected stage.

For each demo, manually match a story:
- Review the prospect's industry, company size, and pain points from discovery notes
- Select the story where the customer's challenge most closely matches the prospect's stated pain
- If no story matches well, note the gap — this tells you which segments need new stories

Document the match for each demo: which story, why it was selected, and which prospect pain it maps to.

### 3. Restructure Each Demo Around the Story

For each of the 5 demos, prepare a story-driven demo outline. Replace the feature-walkthrough structure:

**Instead of:** "Let me show you our dashboard. Here's how reporting works. Here's the automation engine."

**Use this structure:**
1. **Open with the customer's pain** (2 min): "Before I show you the product, let me tell you about {Customer}. They were dealing with {challenge that mirrors prospect's pain}."
2. **Walk through the customer's journey** (10-12 min): Show each product capability as something the customer used. "Here's what {Customer} did to solve it" — then demonstrate the feature in that context.
3. **Share the result** (2 min): "{Customer} went from {before} to {after} in {timeframe}." Use the customer's exact quote at the emotional peak.
4. **Bridge to the prospect** (2 min): "Given what you told me about {prospect's pain}, I'd expect a similar path for your team. What would it mean for you to achieve {customer's result}?"

Write the outline as an Attio note on the deal record.

### 4. Deliver the Demos and Log Engagement

**Human action required:** The founder delivers all 5 demos using the story-driven structure. During and immediately after each demo, log these signals in Attio:

- **Story connection moment**: Did the prospect say anything indicating they related to the customer story? Log the exact words if possible.
- **Questions about the customer**: Did the prospect ask follow-up questions about the customer's experience? Count them.
- **Emotional engagement**: Did the prospect show visible or verbal engagement — leaning in, excitement, surprise, concern? Note what triggered it.
- **Next step committed**: Did the demo end with a clear, committed next step (not "we'll think about it")?
- **Comparison to prior demos**: Was this demo more engaging than a typical feature walkthrough for this kind of prospect?

Score each demo 1-5 on overall engagement: 1 = no connection, 3 = moderate interest, 5 = prospect deeply engaged with the story.

### 5. Evaluate Against Threshold

Run the `threshold-engine` drill to evaluate:

- Count: How many of the 5 demos were delivered with story-driven structure? (Target: >=5)
- Engagement rate: What % showed strong engagement signals — score 4+ or any story connection moment? (Target: >=70%, meaning >=4 of 5 demos)
- Comparison: For deals where you have both a story-driven demo and prior feature demos, compare engagement signals and next-step commitment rates.

**If PASS:** Story-driven demos outperform feature walkthroughs. Proceed to Baseline to automate story matching and prep.
**If FAIL:** Diagnose:
- If stories didn't resonate: were they well-matched to the prospect's pain? Revise story selection criteria.
- If delivery was flat: was the narrative structure followed, or did it revert to a feature tour? Practice the story arc.
- If engagement was moderate but not strong: the stories may need stronger emotional elements — better quotes, more vivid pain descriptions, or more impressive results.

## Time Estimate

- 2 hours: Story library curation (transcript extraction + structuring for 3-5 stories)
- 1 hour: Story-to-demo matching for 5 upcoming demos
- 1.5 hours: Demo outline preparation (20 min per demo)
- 0.5 hours: Post-demo engagement logging (10 min per demo)
- 1 hour: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal tracking, story records, engagement logging | Free plan (up to 3 users) or $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Fireflies | Transcription — extract stories from customer calls | Free (800 min/mo) or $18/user/mo (Pro) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics — event tracking for threshold evaluation | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost this level:** $0 incremental (Attio and Fireflies likely already in stack). If Fireflies is new: ~$18/mo.

## Drills Referenced

- `story-library-curation` — build and structure the initial customer story library from transcripts and interviews
- `threshold-engine` — evaluate demo results against the pass threshold using Attio engagement data and PostHog events
