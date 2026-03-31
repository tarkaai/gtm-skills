---
name: price-objection-handling-scalable
description: >
  Price Objection Handling — Scalable Automation. Auto-detect price objections in
  call transcripts and emails, trigger classification and response workflows without
  manual intervention, run A/B tests on response frameworks, and prevent objections
  through upstream deal scoring.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: ">=65% of price objections overcome with <=10 days to close after resolution over 2 months"
kpis: ["Objection overcome rate", "Objection resolution time", "Objection prevention rate", "Discount rate by objection type"]
slug: "price-objection-handling"
install: "npx gtm-skills add sales/proposed/price-objection-handling"
drills:
  - objection-detection-automation
  - ab-test-orchestrator
---

# Price Objection Handling — Scalable Automation

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Remove manual objection detection entirely. Every sales call and email is monitored for price objections automatically. When detected, the classification-response-follow-up pipeline fires within 2 hours. A/B test response frameworks to find the 10x multiplier: the optimal framework per root cause. Prevent objections upstream by flagging at-risk deals before the proposal call.

## Leading Indicators

- Time from objection occurrence to workflow trigger: <=2 hours (measured by detection latency)
- Auto-detection coverage: >=90% of known objections caught by the system (vs manual logging)
- A/B test velocity: at least 2 experiments completed per month on response frameworks
- Predictive objection score generated for >=80% of deals entering the proposal stage
- Discount rate trending flat or downward (not creeping up as volume grows)

## Instructions

### 1. Deploy auto-detection across all calls and emails

Run the `objection-detection-automation` drill to build always-on monitoring:

**Call transcript monitoring:**
- Configure Fireflies webhook to notify n8n on every new transcript
- n8n workflow: fetch transcript -> match to Attio deal -> run objection extraction via Claude -> route by severity
- For `deal_risk_level` "high" or "critical": send Slack alert AND trigger `price-objection-response` drill
- For `deal_risk_level` "low" or "medium": trigger `price-objection-response` drill silently

**Email objection detection:**
- Configure Attio webhook to notify n8n on new email activity logged to deals in Proposed/Negotiation stage
- n8n workflow: send email body to Claude for objection detection -> if price objection found, classify and trigger response workflow

**Predictive scoring (daily cron):**
- Query Attio for all deals entering or in the Proposed stage
- Score each deal for objection likelihood based on: pain-to-price ratio, champion strength, economic buyer engagement, competitor evaluation, deal size vs typical spend
- Deals scoring >=50 objection risk points: flag in Attio and alert the seller with recommended pre-emptive actions

### 2. A/B test response frameworks

Run the `ab-test-orchestrator` drill to systematically test which response frameworks produce the highest overcome rate per root cause.

**Month 1 experiments (pick 2):**
- Test `anchor_to_pain` vs `roi_proof` for `value_gap` objections. Hypothesis: "Anchoring to the prospect's own pain quote will outperform a generic ROI calculation because it's more emotionally resonant." Minimum sample: 10 objections per variant.
- Test follow-up timing: Day 1 + Day 3 + Day 7 vs Day 1 + Day 2 + Day 5 for the `no_budget` sequence. Hypothesis: "Faster cadence resolves budget objections sooner because budget cycles have fixed deadlines."

**Month 2 experiments:**
- Test the winning framework from Month 1 against a new variant that combines two frameworks (e.g., anchor_to_pain + payment_flexibility)
- Test asset type: ROI calculator vs business case document for `value_gap` objections

For each experiment:
1. Use PostHog feature flags to randomly assign incoming objections to control or variant
2. Run for minimum 7 days or until 10+ objections per variant
3. Measure primary metric: overcome rate. Secondary metrics: days to resolution, discount offered.
4. Auto-promote winners using `ab-test-orchestrator` evaluation logic

### 3. Scale the follow-up sequences

Ensure the the objection follow up sequence workflow (see instructions below) drill's n8n workflows handle increased volume without manual intervention:
- Verify Instantly sending limits can handle the follow-up volume (upgrade to Hypergrowth at $97/mo if exceeding 5,000 emails/mo)
- Monitor n8n workflow execution logs for failures — set up error alerting
- Confirm Attio webhook delivery is reliable (check n8n execution history for missed triggers)

Add new sequence variants for root causes discovered through the detection system that were not covered in Baseline (e.g., if a new objection pattern emerges like "we already built this internally").

### 4. Build objection prevention workflows

The highest-leverage improvement at this level is preventing objections from occurring:

Using data from PostHog, analyze which deal characteristics predict price objections:
- Deals with `pain_to_price_ratio < 5` face 3x more objections -> require stronger discovery before advancing to proposal
- Deals without economic buyer engagement face 2x more `authority_gap` objections -> require multi-threading before proposal
- Deals where the competitor was mentioned in discovery face 2x more `competitor_comparison` objections -> require competitive positioning in the demo

Implement these as Attio automation rules:
- If `pain_to_price_ratio < 5` and deal stage is "Proposal Sent": block stage advancement, flag for additional discovery
- If `economic_buyer_engaged = false` and deal stage is "Proposal Sent": alert seller to multi-thread first

### 5. Track and evaluate at scale

Build a PostHog dashboard tracking:
- Objection overcome rate (weekly, target >=65%)
- Detection latency (time from call end to workflow trigger, target <=2 hours)
- Auto-detection coverage (auto-detected / total known objections)
- A/B test results and active experiments
- Discount rate by root cause (target: flat or declining)
- Prevention rate (deals that closed won without any price objection / total closed won)

After 2 months, evaluate:
- If overcome rate >=65% AND average resolution <=10 days: proceed to Durable
- If overcome rate is high but resolution is slow: tighten follow-up cadence, test shorter sequences
- If overcome rate is low on specific root causes: the framework for that root cause needs replacement — run more experiments
- If discount rate is climbing: the team is reaching for discounts instead of using frameworks — retrain or restrict discount authority

## Time Estimate

- 15 hours: deploying objection-detection-automation (Fireflies webhook, n8n workflows, email detection, predictive scoring)
- 10 hours: setting up A/B test infrastructure and first experiments
- 10 hours: scaling follow-up sequences and building prevention rules
- 25 hours: monitoring, iterating on experiments, and adjusting over 2 months
- 10 hours: analysis, reporting, and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, webhooks, automation rules | Standard stack (excluded) |
| PostHog | Event tracking, funnels, feature flags, experiments | Standard stack (excluded) |
| n8n | Workflow orchestration for detection + follow-up | Standard stack (excluded) |
| Fireflies | Call transcription + webhook | Pro: $18/user/mo or ~$10/user/mo annual — [pricing](https://fireflies.ai/pricing) |
| Instantly | Follow-up email delivery | Hypergrowth: $97/mo — [pricing](https://instantly.ai/pricing) |
| Clay | Enrichment for predictive scoring | Launch: $185/mo — [pricing](https://www.clay.com/pricing) |
| Anthropic Claude API | Objection extraction, classification, response generation | ~$30-80/mo at 50+ objections/month — [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |

**Play-specific cost:** ~$330-380/mo (Fireflies + Instantly + Clay + Claude API)

## Drills Referenced

- `objection-detection-automation` — always-on monitoring of calls and emails for price objections with auto-classification and workflow triggering
- `ab-test-orchestrator` — designs, runs, and evaluates A/B tests on response frameworks and follow-up sequences
- the objection follow up sequence workflow (see instructions below) — automated multi-touch follow-ups scaled to handle increased volume from auto-detection
