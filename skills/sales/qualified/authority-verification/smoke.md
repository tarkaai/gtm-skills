---
name: authority-verification-smoke
description: >
  Authority Verification — Smoke Test. Manually research org charts and run discovery calls
  on a small batch of qualified deals to prove that structured authority verification identifies
  Economic Buyers and separates real decision-makers from influencers.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=3 deals with authority verified (Economic Buyer confirmed and engaged) in 1 week from 8-10 active deals"
kpis: ["Authority verification rate", "Economic Buyer identification rate", "Time to authority confirmation", "Stakeholder map completeness"]
slug: "authority-verification"
install: "npx gtm-skills add sales/qualified/authority-verification"
drills:
  - stakeholder-research
  - authority-discovery-call
  - threshold-engine
---

# Authority Verification — Smoke Test

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Prove that structured authority verification produces actionable signal. After researching and calling on 8-10 active deals, at least 3 should have a confirmed Economic Buyer who is engaged (has attended a call or replied to outreach). The process should clearly separate deals where you are talking to a decision-maker from deals where you are talking to an influencer or end user.

## Leading Indicators

- Org chart research is surfacing people at each deal who were not previously in the CRM
- Discovery calls are revealing the actual approval process (not just the contact's self-reported authority)
- At least one deal's primary contact turns out NOT to be the Economic Buyer, and you identify who IS
- Stakeholder maps are exposing single-threaded risks (only 1 contact engaged at a deal)

## Instructions

### 1. Select target deals and research org charts

Pick 8-10 deals currently in Qualified stage in Attio. For each deal, run the `stakeholder-research` drill:

1. Pull existing contacts linked to the deal from Attio
2. Run `org-chart-research` in Clay to discover additional stakeholders at Director+ level across Engineering, Product, Finance, IT, and Procurement departments
3. Classify each discovered person using `stakeholder-role-classification` — determine who is likely the Economic Buyer, Champion, Influencer, Blocker, End User, or Gatekeeper
4. Store the complete stakeholder map as a note on the deal in Attio with role, confidence level, and engagement status
5. Flag gaps: which deals have no identified Economic Buyer? Which are single-threaded?

Budget approximately 30 minutes per deal for this research step.

### 2. Prepare and run authority discovery calls

For each deal, run the `authority-discovery-call` drill:

1. Review the stakeholder map from step 1 — identify what authority questions remain unanswered
2. Generate authority-focused questions using Claude: who controls the budget, what the approval process looks like, whether the contact can sign unilaterally, who else must be involved
3. **Human action required:** Book and conduct discovery calls with your primary contacts. Use Cal.com booking links. Fireflies auto-joins and transcribes.
4. During each call, probe for budget ownership, approval workflows, and the last time the company purchased similar software
5. After each call, run the transcript through Claude to extract authority signals — the drill provides the extraction prompt and expected JSON schema
6. Update the stakeholder map in Attio: set `authority_verification_status` to verified/identified/unverified on the deal, update `stakeholder_role` and `stakeholder_confidence` for each person

Target 5-8 calls over the week. Some deals will have authority verified through enrichment research alone (e.g., CEO at a 10-person company is the Economic Buyer with high confidence).

### 3. Log results in Attio

For each deal, populate these fields:
- `authority_verification_status`: verified / identified / unverified
- `authority_verified_date`: date if verified
- `economic_buyer_name`: name of confirmed EB
- `buying_process_notes`: how the company makes purchasing decisions (single signer, committee, procurement-gated)
- `stakeholder_count`: total classified stakeholders discovered
- `engaged_stakeholder_count`: stakeholders with at least one interaction

Track what worked: which research methods surfaced the EB fastest? Which discovery questions produced the clearest authority signals? Which deals remain stuck?

### 4. Evaluate against threshold

Run the `threshold-engine` drill to evaluate: >=3 deals with authority verified (Economic Buyer confirmed and engaged) in 1 week from 8-10 active deals.

Analyze the results:
- What was the verification rate across the batch?
- How many deals had the wrong person classified as decision-maker before this process?
- How long did verification take per deal (from first research to confirmed EB)?
- What was the most effective method: enrichment research, direct questioning on a call, or referral from a Champion?

If PASS (>=3 verified), proceed to Baseline. If FAIL, diagnose: are deals entering Qualified without enough contact depth? Is org chart research returning stale data? Are contacts being evasive about the buying process?

## Time Estimate

- Org chart research (8-10 deals at 30 min each): 4-5 hours
- Discovery call prep (5-8 calls at 10 min each): 1 hour
- Discovery calls (5-8 at 20-30 min each): 2-4 hours
- Post-call transcript analysis and CRM updates: 1 hour
- Threshold evaluation: 15 minutes

Org chart research and call prep overlap with scheduling wait times. Actual focused effort is approximately 6 hours spread over 1 week.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with stakeholder custom fields | Free tier (up to 3 users) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Org chart research and people enrichment | Launch plan $185/mo — [clay.com/pricing](https://clay.com/pricing) |
| Fireflies | Call recording and transcription | Free (800 min/mo) or Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Cal.com | Call scheduling | Free (1 user) — [cal.com/pricing](https://cal.com/pricing) |
| Anthropic Claude | Stakeholder classification and transcript analysis | Pay-per-use ~$3/MTok input — [anthropic.com/pricing](https://anthropic.com/pricing) |

**Estimated play-specific cost:** $0-20/mo (Clay credits for enrichment; everything else fits free tiers for a smoke test)

## Drills Referenced

- `stakeholder-research` — manually research and classify all stakeholders at each target account's buying committee
- `authority-discovery-call` — structured discovery call focused on verifying decision-making authority with transcript extraction
- `threshold-engine` — evaluate results against the pass threshold and recommend next action
