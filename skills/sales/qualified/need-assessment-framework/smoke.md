---
name: need-assessment-framework-smoke
description: >
  Need Assessment Framework — Smoke Test. Run structured need assessment manually on a small batch
  of prospects to validate that scoring business needs by category, severity, and urgency produces
  actionable qualification signal. Agent helps prep, founder executes discovery calls by hand.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Email, Direct"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=10 need assessments completed in 1 week with >=60% meeting minimum viable need threshold (score >=12, >=2 Critical)"
kpis: ["Need assessment completion rate", "Average need score", "Qualification rate (% meeting threshold)", "Critical need identification rate", "Need score distribution spread"]
slug: "need-assessment-framework"
install: "npx gtm-skills add sales/qualified/need-assessment-framework"
drills:
  - icp-definition
  - build-prospect-list
  - threshold-engine
---

# Need Assessment Framework — Smoke Test

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Outcomes

Prove that structured need assessment produces meaningful qualification signal. After assessing 15-20 prospects via discovery calls, at least 10 should have complete need assessments, and >=60% of those should meet the minimum viable need threshold (total score >=12, >=2 Critical needs). The scoring system should differentiate between prospects who have genuine business needs your product solves and those who do not.

## Leading Indicators

- Discovery calls are producing varied need scores across categories (not all clustering around the same numbers)
- At least one need category is consistently scoring Critical across multiple prospects — this is your strongest value proposition signal
- Some need categories are consistently Low or unassessed — this tells you which parts of your pitch are not resonating or are irrelevant to your ICP
- Prospects scoring High Need are expressing urgency and asking about next steps, while Low Need prospects are politely uninterested
- The spread between highest and lowest need scores is meaningful (variance >3 points)

## Instructions

### 1. Define your ICP and need categories

Run the `icp-definition` drill to document your Ideal Customer Profile. Then run the the need scorecard setup workflow (see instructions below) drill to:

- Define 5-7 business need categories your product addresses. Each category must be specific and tied to a measurable business outcome. Examples: "reducing manual data entry," "improving data accuracy across systems," "accelerating workflow execution," "eliminating cross-tool friction," "reducing operational cost," "improving reporting visibility," "scaling operations without adding headcount."
- Create the scoring infrastructure in Attio: per-category severity fields (1-3 scale), aggregate total score, need tier classification, and qualification verdict
- Set up PostHog events for tracking need assessments
- Document the qualification threshold: total score >=12 with >=2 Critical needs

### 2. Build a small prospect list

Run the `build-prospect-list` drill to source 15-20 contacts matching your ICP. Keep the list small — this is a smoke test. Source from Clay or Apollo, enrich with basic firmographics, and push to Attio. For each prospect, manually estimate which need categories might be relevant based on public data (industry, company size, job postings, tech stack).

### 3. Run need discovery calls

**Human action required:** Book and conduct 10-15 discovery calls over the week. Use the the need discovery call workflow (see instructions below) drill for each call:

1. Before each call: review the prospect's public data and generate a need hypothesis — which of your 5-7 need categories are likely relevant, and what questions will probe each one?
2. During the call: work through need categories naturally. For each area, ask about current pain severity, business impact, prior solution attempts, and urgency. Do not interrogate — frame questions around understanding their challenges.
3. After each call: use the Fireflies transcript and the call transcript need extraction workflow (see instructions below) fundamental to extract structured need scores. Update all fields in Attio.
4. Score each need on the 3-point scale: Critical (3) = severe pain with urgency, Moderate (2) = acknowledged problem with some impact, Low (1) = mentioned but not a priority.

### 4. Track and compare results

After each call, log the need assessment in Attio and fire PostHog events. Track:
- Which need categories are scored Critical most often? This is your strongest value prop.
- Which need categories are consistently Low or unassessed? Consider removing these or rethinking how you probe for them.
- Are need scores varied (good — the scoring system differentiates) or clustered (bad — the rubric needs adjustment)?
- Do higher-scoring prospects express more interest in continuing the conversation?

### 5. Evaluate against threshold

Run the `threshold-engine` drill to evaluate results: >=10 need assessments completed in 1 week with >=60% meeting the minimum viable need threshold (score >=12, >=2 Critical).

Analyze the results:
- What was the overall qualification rate?
- Which ICP segment had the highest average need score?
- Did the scoring system produce meaningful differentiation between prospects?
- Which need categories are strongest predictors of deal progression interest?

If PASS, proceed to Baseline. Document the need categories that work, the qualification threshold, and any adjustments to the scoring rubric.

If FAIL, diagnose:
- If completion rate is low (<10 assessments): booking or scheduling problem, not need assessment problem
- If qualification rate is low (<60% meeting threshold): either your ICP is wrong (targeting people who do not have these needs), your need categories are wrong (not aligned to real market pain), or your scoring rubric is too generous/strict
- If scores are all similar: your need categories lack specificity — refine them to be more distinct

## Time Estimate

- ICP definition and need category design: 1.5 hours
- CRM scorecard setup: 30 minutes
- Prospect list build: 1 hour
- Discovery calls (10-15 at 25-30 min each): 4-5 hours
- Post-call scoring and analysis: 1 hour

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with need assessment custom fields | Free tier (up to 3 users) — [attio.com/pricing](https://attio.com/pricing) |
| Fireflies | Call recording and transcription | Free (800 min/mo) or Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Cal.com | Discovery call scheduling | Free (1 user) — [cal.com/pricing](https://cal.com/pricing) |
| Clay | Prospect enrichment | Launch plan $185/mo — [clay.com/pricing](https://clay.com/pricing) |
| PostHog | Event tracking | Free (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost:** $0-18/mo (Fireflies Pro is optional; everything else fits in free tiers for a smoke test)

## Drills Referenced

- `icp-definition` — define ICP and identify which business problems your product solves
- `build-prospect-list` — source and enrich 15-20 prospects from Clay/Apollo
- the need scorecard setup workflow (see instructions below) — create need assessment scoring infrastructure in Attio with categories, severity scales, and thresholds
- the need discovery call workflow (see instructions below) — structured need discovery call with transcript extraction and per-category scoring
- `threshold-engine` — evaluate results against the pass threshold
