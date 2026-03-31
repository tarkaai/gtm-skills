---
name: authority-verification-scalable
description: >
  Authority Verification — Scalable Automation. Scale authority verification across the full pipeline
  with continuous org chart refreshes, multi-threading coverage scoring, and A/B tested approaches
  to Economic Buyer engagement. Find the 10x multiplier without proportional effort.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Scalable Automation"
time: "30 hours over 2 months"
outcome: "Authority verified in >=85% of pipeline deals at 3x volume with deal velocity +25% vs. pre-play baseline and multi-threading rate >=60%"
kpis: ["Authority verification rate at scale", "Time to authority confirmation", "Deal velocity improvement", "Multi-threading rate", "Stakeholder coverage per deal", "Authority classification accuracy"]
slug: "authority-verification"
install: "npx gtm-skills add sales/qualified/authority-verification"
drills:
  - stakeholder-org-mapping
  - stakeholder-engagement-scoring
  - ab-test-orchestrator
  - threshold-engine
---

# Authority Verification — Scalable Automation

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Authority verification operates across the full pipeline without manual enrichment or classification work. Org charts refresh automatically, multi-threading health is scored daily, and A/B tests identify the fastest paths to Economic Buyer engagement. At 3x the deal volume of Baseline, verification rate holds at >=85%, deal velocity improves >=25% compared to pre-play baseline, and >=60% of deals have 3+ engaged stakeholders.

## Leading Indicators

- Weekly org chart refresh is catching org changes (new hires, departures) before they affect deals
- Multi-threading coverage score is identifying single-threaded deals before they stall
- A/B tests on EB engagement tactics are producing statistically significant winners
- Deals flagged "authority unverified" are being resolved within 7 days of the alert
- Authority classification accuracy (verified EB actually signs the contract) is >=85%

## Instructions

### 1. Scale org chart monitoring across all deals

Run the `stakeholder-org-mapping` drill to upgrade from one-shot enrichment (Baseline) to continuous monitoring:

1. Build a persistent Clay table "Stakeholder Mapping — Active Accounts" synced from all active Attio deals at Qualified stage or later
2. Configure weekly refresh via n8n cron (Mondays at 6 AM): re-enrich all companies, detect deltas (new hires, departures, title changes)
3. For each delta, run role classification: new arrivals are classified and added to Attio; departures trigger alerts if they were a Champion or Economic Buyer
4. Build Attio filtered views for deal reviews:
   - **Under-mapped deals**: fewer than 3 classified stakeholders
   - **Missing Economic Buyer**: no contact tagged as Economic Buyer
   - **Single-threaded**: only 1-2 contacts at engagement level Active or Warm
   - **Stale maps**: stakeholder_map_date older than 30 days
5. Schedule weekly n8n workflow that generates a stakeholder coverage report: total stakeholders mapped per deal, multi-threading rate, deals with new risks

### 2. Deploy multi-threading engagement scoring

Run the `stakeholder-engagement-scoring` drill to build always-on scoring:

1. Define the engagement event taxonomy: `stakeholder_email_sent`, `stakeholder_email_replied`, `stakeholder_meeting_attended`, `stakeholder_call_completed`, `stakeholder_linkedin_connected`, `stakeholder_content_shared`
2. Build a daily n8n workflow that computes per-stakeholder engagement scores (rolling 14-day window) and writes them to Attio
3. Compute deal-level health scores: `multi_thread_ratio` (engaged stakeholders / total stakeholders) and `role_coverage_score` (1 point per role type with Active or Warm engagement)
4. Set up alerts:
   - Single-threaded alert: deal has only 1 engaged stakeholder AND deal value > threshold
   - Champion cooling alert: Champion drops from Active to Cold
   - Economic Buyer dark alert: EB has not engaged in 14+ days
   - Blocker activation alert: contact tagged as Blocker becomes Active

### 3. A/B test Economic Buyer engagement tactics

Run the `ab-test-orchestrator` drill to experiment on how quickly and effectively you reach the Economic Buyer:

1. **Experiment 1 — Introduction path**: Test Champion-mediated intro vs. direct outreach to EB. Split by alternating deals. Measure: time from EB identification to EB first meeting.
2. **Experiment 2 — EB outreach message**: Test 3 variants of initial EB engagement email: ROI-focused, competitive-focused, peer-reference-focused. Use PostHog feature flags for assignment. Measure: reply rate and meeting conversion.
3. **Experiment 3 — Authority discovery timing**: Test verifying authority on first call vs. second call. Measure: accuracy of verification and contact comfort level (sentiment from transcript analysis).

Run each experiment for minimum 4 weeks or 30 deals per variant. Use `posthog-experiments` for statistical analysis.

### 4. Scale deal volume

Increase to 3x Baseline deal volume. The automation stack should handle the additional load without proportional effort:
- Auto-enrichment fires on every new Qualified deal (no manual work)
- Weekly org chart refresh covers all active accounts (no manual research)
- Engagement scoring runs daily across all deals (no manual tracking)
- Alerts surface only the deals that need attention (founder focuses on exceptions, not routine)

Monitor n8n workflow execution metrics: success rate, average execution time, error frequency. Fix any workflow that fails >5% of the time.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to evaluate: authority verified in >=85% of pipeline deals at 3x volume with deal velocity +25% vs. pre-play baseline and multi-threading rate >=60%.

Measure:
- Authority verification rate at 3x volume (target: >=85%)
- Deal velocity improvement vs. pre-play baseline (target: >=25%)
- Multi-threading rate (target: >=60% of deals with 3+ engaged stakeholders)
- Authority classification accuracy (target: >=85% — verified EB is the actual contract signer)
- Time to authority confirmation (target: <10 days at scale)

If PASS, proceed to Durable. If FAIL, diagnose: is enrichment degrading at scale (Clay credit burn, stale data)? Are engagement scores miscalibrated? Are A/B test winners not being adopted?

## Time Estimate

- Org mapping automation build: 6 hours
- Engagement scoring build: 4 hours
- A/B test design and setup: 4 hours
- Ongoing monitoring (30 min/week for 8 weeks): 4 hours
- Weekly deal review using new dashboards (1 hour/week for 8 weeks): 8 hours
- Threshold evaluation and analysis: 2 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with stakeholder scoring fields | Pro $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Continuous org chart enrichment | Growth plan $375/mo (~15 credits/company/refresh) — [clay.com/pricing](https://clay.com/pricing) |
| n8n | Workflow automation for enrichment, scoring, alerts | Pro $50/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| PostHog | Experiments, dashboards, engagement tracking | Free (1M events/mo) or Growth $0+ — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic Claude | Classification, transcript analysis | Pay-per-use ~$3/MTok input — [anthropic.com/pricing](https://anthropic.com/pricing) |
| Fireflies | Call transcription | Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |

**Estimated play-specific cost:** $200-500/mo (Clay at Growth tier is the main cost driver; n8n Pro needed for higher workflow volume)

## Drills Referenced

- `stakeholder-org-mapping` — continuous org chart monitoring with weekly refresh, delta detection, and automated stakeholder population
- `stakeholder-engagement-scoring` — daily multi-threading health scoring with role coverage and alert thresholds
- `ab-test-orchestrator` — experiment design and execution for EB engagement tactics
- `threshold-engine` — evaluate pass/fail and recommend level progression
