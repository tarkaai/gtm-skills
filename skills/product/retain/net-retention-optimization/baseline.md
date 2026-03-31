---
name: net-retention-optimization-baseline
description: >
  Net Retention Optimization — Baseline Run. Deploy always-on churn detection, automated
  at-risk interventions, and expansion triggers. First continuous automation targeting
  the primary NDR lever identified at Smoke.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "20 hours over 4 weeks"
outcome: "NDR improves 3+ points from Smoke baseline"
kpis: ["Net dollar retention", "Churn save rate", "Expansion conversion rate", "Intervention volume", "Revenue churn rate"]
slug: "net-retention-optimization"
install: "npx gtm-skills add product/retain/net-retention-optimization"
drills:
  - churn-risk-scoring
  - churn-prevention
  - upgrade-prompt
---

# Net Retention Optimization — Baseline Run

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

First always-on automation. Deploy three systems that run continuously: churn risk scoring that identifies at-risk accounts daily, automated interventions that attempt to save them, and expansion triggers that prompt healthy accounts to upgrade. Prove that automated retention and expansion efforts move NDR up from the Smoke baseline.

The pass threshold is a 3+ point NDR improvement. If your Smoke baseline was 104%, you need to reach 107%. This proves the automation is having a real effect, not just measurement noise.

## Leading Indicators

- Churn risk scoring runs daily and produces scored cohorts across all risk tiers (not clustered in one tier)
- At least 10 at-risk interventions fire in the first 2 weeks (system is detecting and acting)
- Churn save rate exceeds 20% (at least 1 in 5 at-risk users who received intervention did not churn)
- Expansion prompts fire for usage-based triggers and at least 5% of prompted users start the upgrade flow

## Instructions

### 1. Deploy churn risk scoring

Run the `churn-risk-scoring` drill to build a daily scoring pipeline. This drill:

1. Analyzes PostHog usage data to identify behavioral churn signals: usage decline, feature abandonment, login gaps, support spikes, billing page visits, team shrinkage, data exports
2. Scores every active user on a 0-100 churn risk scale daily via an n8n workflow
3. Classifies users into risk tiers: Low (0-25), Watch (26-45), Medium (46-65), High (66-85), Critical (86-100)
4. Syncs risk scores to PostHog cohorts and Attio contact records
5. Creates Attio tasks when users reach Critical tier

After the drill runs for 7 days, validate the model: do the scores match your intuition about which accounts are at risk? Adjust signal weights if false positive rate exceeds 40%.

**Human action required:** Review the first week's scored output. Check 10 accounts across different risk tiers. Confirm the scoring makes sense before enabling automated interventions.

### 2. Activate automated interventions

Run the `churn-prevention` drill to connect churn risk scores to tiered interventions:

- **Medium risk (46-65):** Intercom in-app message highlighting an unused feature relevant to their usage pattern. Uses `intercom-in-app-messages`. Template: "Your team hasn't used [Feature] recently — here's how [similar company] uses it to [outcome]."
- **High risk (66-85):** Loops triggered email from the account context. Uses `loops-transactional`. Template: personalized around the specific declining signal. Include a help link and a calendar booking link for a call.
- **Critical (86-100):** Attio task for the account owner with full context: risk score, signals firing, usage data, recommended talking points. **Human action required:** Account owner reaches out personally within 48 hours.

Log every intervention as a PostHog event (`retention_intervention_sent`) with properties: `intervention_tier`, `risk_score`, `primary_signal`, `account_mrr`.

### 3. Deploy expansion triggers

Run the `upgrade-prompt` drill to detect expansion opportunities and deliver contextual prompts:

Configure these triggers:
- **Limit proximity:** User at 80%+ of plan limits (seats, storage, API calls). In-app message via Intercom showing current usage vs. limit and the next tier.
- **Feature gate hit:** User attempted a premium feature. In-app message explaining what they get with the upgrade.
- **Growth signal:** Account added 3+ team members in the last 30 days or usage volume doubled. Email via Loops suggesting the team plan.
- **Power user behavior:** Account using advanced features, API access, or integrations. Email suggesting enterprise tier.

Log every expansion prompt as a PostHog event (`expansion_prompt_shown`) and track the funnel: prompt shown -> upgrade started -> upgrade completed.

### 4. Monitor intervention effectiveness

After 2 weeks of both systems running, measure:

- **Churn save rate:** Of accounts scored Medium+ that received intervention, what percentage did NOT churn within 30 days? Target: >20%.
- **Expansion conversion rate:** Of accounts that received an upgrade prompt, what percentage started the upgrade flow? Target: >5%.
- **False positive rate:** Of accounts scored High/Critical, what percentage turned out to be healthy? If >40%, tighten scoring thresholds.
- **Net NDR impact:** Compare trailing 4-week NDR (with interventions) against the Smoke baseline. Target: +3 points.

### 5. Evaluate against threshold

At 4 weeks, compute NDR using the `ndr-baseline-measurement` drill. Compare to the Smoke baseline.

If PASS (NDR improved 3+ points): the automation is working. Document which intervention type had the highest save rate and which expansion trigger had the highest conversion rate. Proceed to Scalable.
If FAIL (NDR improved <3 points): diagnose. Check whether the problem is detection (risk scoring not catching real churners), intervention (messages not compelling enough), or expansion (prompts not converting). Adjust the weakest link and run for another 2-week cycle.

## Time Estimate

- 6 hours: deploy churn risk scoring and validate the model
- 6 hours: configure churn prevention interventions and expansion triggers
- 4 hours: monitor and tune over weeks 2-3
- 4 hours: measure results, diagnose gaps, document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage tracking, churn signals, cohorts, event logging | Free up to 1M events/mo; paid from $0.00031/event — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app messages for at-risk nudges and expansion prompts | From $39/mo (Essential); $99/mo (Advanced) — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Triggered retention and expansion emails | Free up to 1,000 contacts; paid from $49/mo — [loops.so/pricing](https://loops.so/pricing) |

**Estimated cost for Baseline: $50-150/mo** (Intercom Essential + Loops, depending on contact volume)

## Drills Referenced

- `churn-risk-scoring` — builds the daily behavioral churn risk model that scores every user and classifies into risk tiers
- `churn-prevention` — connects risk scores to tiered automated interventions (in-app, email, human outreach)
- `upgrade-prompt` — detects usage-based expansion signals and delivers contextual upgrade prompts
