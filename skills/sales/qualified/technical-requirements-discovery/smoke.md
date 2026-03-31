---
name: technical-requirements-discovery-smoke
description: >
  Technical Requirements Discovery — Smoke Test. Run pre-call tech stack research and a structured
  technical discovery call on a small batch of qualified deals to validate that systematic technical
  assessment surfaces blockers early and produces actionable technical fit signals.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=5 deals with technical discovery completed and scored in 1 week, with >=1 blocker identified before proposal stage"
kpis: ["Technical discovery completion rate", "Technical fit score distribution", "Blocker identification rate", "Pre-call research accuracy"]
slug: "technical-requirements-discovery"
install: "npx gtm-skills add sales/qualified/technical-requirements-discovery"
drills:
  - tech-stack-discovery
  - threshold-engine
---

# Technical Requirements Discovery — Smoke Test

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Prove that structured technical discovery surfaces deal-critical requirements and blockers that would otherwise emerge late in the sales cycle. After running technical discovery on 5+ qualified deals, at least 1 should reveal a technical blocker that — without this process — would have surfaced during implementation or contract review. The technical fit scores should differentiate between deals that can close quickly and deals that need additional technical work.

## Leading Indicators

- Technical discovery calls are producing different fit scores across deals (not all clustering around the same number)
- At least one technical category (integrations, security, infrastructure, performance, migration) is consistently weaker than the others — this tells you where your product-market fit needs work
- Pre-call tech stack research is partially accurate: some predictions match what the prospect confirms on the call, indicating the research approach is viable
- Deals with technical blockers identified early are being routed differently than unblocked deals

## Instructions

### 1. Set up technical scoring infrastructure

Run the the technical fit scoring workflow (see instructions below) drill to create technical scoring custom attributes on your Attio Deals object. This creates:
- Score fields (0-100) for each of 5 technical categories: integrations, security/compliance, infrastructure, performance, data migration
- Composite fit score with weighted formula
- Verdict field: Strong Fit (>=75), Moderate Fit (50-74), Weak Fit (25-49), No Fit (<25)
- Routing status for technical pipeline stages

### 2. Research tech stacks for 5-8 qualified deals

Select 5-8 currently qualified deals from your Attio pipeline. For each, run the `tech-stack-discovery` drill:
- The agent queries Clay Claygent to detect the prospect's tech stack from their website, job postings, and public data
- It identifies likely integration requirements, security posture, and technical maturity
- It generates a call prep brief with priority questions to ask

Review each call prep brief before the discovery call. Note which predictions seem plausible and which feel like guesses.

### 3. Conduct technical discovery calls

**Human action required:** Schedule and conduct technical discovery calls with each prospect's technical stakeholder (IT lead, engineering manager, CTO, or security lead). Use the the technical discovery call workflow (see instructions below) drill for each call:

1. Before each call: review the tech stack research and generated question guide. Customize questions for this specific prospect.
2. During the call: work through integration, security, infrastructure, performance, and data migration questions naturally. Do not interrogate — frame questions as "helping us scope the implementation correctly."
3. After each call: the agent extracts technical requirements from the Fireflies transcript using `call-transcript-tech-requirements-extraction`, scores technical fit, and logs everything to Attio.

### 4. Score and route each deal

After each discovery call, review the technical fit scores the agent generated. For each deal:
- Check the composite score and per-category breakdown
- Review blockers identified and whether they are addressable
- Verify the routing recommendation makes sense (Technically Qualified, Needs SE Review, Needs Product Review, or Technically Disqualified)

Compare the post-call scores against the pre-call predictions from tech stack research. Note discrepancies — this calibrates future research accuracy.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to evaluate results against the pass threshold: >=5 deals with technical discovery completed and scored in 1 week, with >=1 blocker identified before proposal stage.

Analyze the results:
- What was the overall technical fit distribution?
- Which technical category was weakest across your pipeline?
- Did pre-call research correctly predict any requirements?
- Did any deal reveal a blocker that would have been missed without this process?
- How long did each technical discovery take end-to-end?

If PASS (>=5 scored, >=1 blocker found), proceed to Baseline. If FAIL, diagnose: are your deals not technically complex enough to need this (good problem — simplify), or is the discovery call not uncovering real requirements (refine questions)?

## Time Estimate

- Technical scoring setup in Attio: 30 minutes
- Tech stack research per deal (5-8 deals): 2-3 hours total (agent does most work)
- Technical discovery calls (5-8 at 30-45 min each): 3-4 hours
- Post-call scoring and analysis: 1 hour
- Threshold evaluation: 30 minutes

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with technical scoring custom fields | Free (up to 3 users) — [attio.com/pricing](https://attio.com/pricing) |
| Fireflies | Call recording and transcription | Free (800 min/mo) or Pro $10/user/mo annual — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Cal.com | Technical discovery call scheduling | Free (1 user) — [cal.com/pricing](https://cal.com/pricing) |
| Clay | Tech stack enrichment via Claygent | Launch $185/mo — [clay.com/pricing](https://clay.com/pricing) |
| PostHog | Event tracking | Free (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API | Transcript analysis and requirement extraction | Sonnet 4.6: $3/$15 per 1M tokens — [claude.com/pricing](https://claude.com/pricing) |

**Estimated play-specific cost:** $0-20/mo (Fireflies Pro optional; Clay credits for Claygent ~$5-10 worth; Anthropic API ~$1-5 for transcript analysis. Everything else fits in free tiers for a smoke test.)

## Drills Referenced

- `tech-stack-discovery` — research prospect tech stack, integrations, and security posture from public signals before the call
- the technical discovery call workflow (see instructions below) — structured technical discovery call with transcript extraction and fit scoring
- the technical fit scoring workflow (see instructions below) — set up and apply the 5-category technical scoring rubric
- `threshold-engine` — evaluate results against the pass threshold
