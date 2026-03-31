---
name: bant-qualification-scalable
description: >
  BANT Qualification Framework — Scalable Automation. Automated pre-qualification pipeline that
  BANT-scores every new lead before human contact, routes based on score, and runs A/B experiments
  on scoring weights, outreach copy, and qualification thresholds to find the 10x multiplier.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=35% qualification rate at 100+ leads/month with automated pre-scoring and <15 min average human time per qualified lead"
kpis: ["Qualification rate at scale", "Pre-score accuracy vs post-call", "Time saved by auto-scoring", "False positive rate", "Cost per qualified lead", "Leads processed per month"]
slug: "bant-qualification"
install: "npx gtm-skills add sales/qualified/bant-qualification"
drills:
  - bant-auto-scoring
  - follow-up-automation
  - ab-test-orchestrator
  - bant-qualification-reporting
---

# BANT Qualification Framework — Scalable Automation

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Scale BANT qualification from manual discovery calls to an automated pre-scoring pipeline that handles 100+ leads per month. Every new lead gets BANT-scored automatically via enrichment data before any human contact. Founder time is reserved for qualified leads only. The 10x multiplier: automated pre-qualification reduces human touch per lead from 30+ minutes (Baseline) to under 15 minutes (only the discovery call itself, with all prep automated).

## Leading Indicators

- Auto-scoring pipeline processes new leads within 5 minutes of CRM entry
- Pre-score accuracy exceeds 70% (pre-enrichment BANT scores within 15 points of post-call scores)
- Founder is only spending time on leads pre-scored at 50+ (no wasted calls)
- A/B experiments on scoring weights are producing measurable accuracy improvements
- Cost per qualified lead is trending down month-over-month

## Instructions

### 1. Deploy automated BANT pre-scoring

Run the `bant-auto-scoring` drill to build the automated pipeline:

1. **Trigger:** n8n workflow fires when a new deal is created in Attio (from any source: outbound list, inbound form, referral)
2. **Enrich:** Push the lead to Clay for BANT-specific enrichment — funding data, org chart, tech stack, job postings, news mentions (see `clay-bant-enrichment` fundamental)
3. **Score:** Clay formula columns compute per-dimension BANT scores and composite
4. **Route:** Push scores back to Attio and move the deal to the appropriate pipeline stage:
   - Composite >=70: "BANT Pre-Scored" stage + Slack alert to founder
   - Composite 40-69: "BANT Pre-Scored" + note listing weak dimensions for discovery
   - Composite <40: "BANT Disqualified" + add to nurture sequence
5. **Log:** Fire PostHog event `bant_auto_score_completed` with all scores

This runs on autopilot. Every lead that enters your CRM gets BANT-scored within minutes.

### 2. Build automated follow-up workflows

Run the `follow-up-automation` drill to create n8n workflows that act on BANT scores:

- **High-score leads (70+):** Auto-generate a personalized outreach email referencing their specific BANT signals (e.g., "Saw you just raised your Series A — congrats. We help companies at your stage solve [Need]"). Send via Instantly or as a founder-direct email.
- **Medium-score leads (40-69):** Enroll in a nurture sequence that addresses the weakest BANT dimension. If Budget is weak, send case studies showing ROI. If Authority is weak, send content designed to be forwarded to decision makers.
- **Score change alerts:** When a prospect's BANT score changes (e.g., they raise funding, change jobs, or post about a relevant problem), trigger a re-scoring and alert the founder if they cross the 70 threshold.

### 3. Run A/B experiments on scoring and outreach

Run the `ab-test-orchestrator` drill to set up experiments that improve qualification accuracy and conversion:

**Experiment 1 — Scoring weight optimization:**
- Control: Budget 25%, Authority 25%, Need 30%, Timeline 20%
- Variant: Budget 20%, Authority 20%, Need 40%, Timeline 20%
- Measure: which weighting produces higher qualification-to-closed-won correlation
- Duration: 4 weeks, minimum 50 prospects per variant

**Experiment 2 — Pre-score threshold tuning:**
- Control: Qualified threshold at composite >=70
- Variant: Qualified threshold at composite >=60
- Measure: does a lower threshold capture more true positives without flooding the pipeline with false positives?
- Duration: 4 weeks

**Experiment 3 — Outreach personalization by BANT dimension:**
- Control: Generic personalized outreach (company + role mention)
- Variant: BANT-dimension-specific personalization (lead with their strongest signal)
- Measure: reply rate and meeting booking rate
- Duration: 100 sends per variant

Use PostHog feature flags to randomly assign variants. Evaluate using the `ab-test-orchestrator` drill's statistical significance checks.

### 4. Scale volume

Increase prospect volume to 200-500 per month by:
- Expanding Clay enrichment tables with new ICP segments validated in Baseline
- Adding new lead sources (inbound forms, partner referrals, event attendees) that all flow through the same auto-scoring pipeline
- Monitoring enrichment credit usage and optimizing waterfall provider order to reduce cost per enrichment

All new leads, regardless of source, enter the same BANT auto-scoring pipeline. No manual triage.

### 5. Build qualification reporting

Run the `bant-qualification-reporting` drill to create:

- **PostHog dashboard:** Qualification volume by week, score distribution, dimension breakdown, pre-score vs post-call accuracy
- **Pipeline velocity funnel:** Outreach > Reply > Discovery > Qualified > Proposal > Won
- **Scoring accuracy cohorts:** True positives, false positives, true negatives, false negatives
- **Weekly automated report:** Slack summary every Monday with key metrics
- **Anomaly alerts:** Qualification rate drop, scoring accuracy degradation, pipeline stall

### 6. Evaluate against threshold

After 2 months, measure against: >=35% qualification rate at 100+ leads/month with <15 min human time per qualified lead.

Review:
- Are automated pre-scores accurate enough to skip discovery calls for obvious qualifications/disqualifications?
- Which A/B experiments produced winners?
- What is the cost per qualified lead?
- Where are the remaining bottlenecks?

If PASS, proceed to Durable. If FAIL, diagnose:
- Low pre-score accuracy: enrichment data is stale or incomplete — add providers to the waterfall
- Low qualification rate at scale: ICP may need tightening, or scoring formula needs recalibration
- High false positive rate: threshold is too generous — raise the bar

## Time Estimate

- Auto-scoring pipeline setup: 8 hours
- Follow-up automation workflows: 6 hours
- A/B experiment design and setup: 8 hours
- Reporting dashboard and alerts: 4 hours
- Ongoing discovery calls (scaled): 20 hours over 2 months
- Monitoring, optimization, and analysis: 14 hours over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with BANT scoring pipeline | Plus $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment with BANT signals at scale | Launch $185/mo or Growth $495/mo — [clay.com/pricing](https://clay.com/pricing) |
| Instantly | Cold email sequences | Hypergrowth $97/mo — [instantly.ai/pricing](https://instantly.ai/pricing) |
| n8n | Automation orchestration | Starter $24/mo or Pro $60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Fireflies | Call transcription | Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics, experiments, feature flags | Free (1M events/mo) or usage-based — [posthog.com/pricing](https://posthog.com/pricing) |
| Cal.com | Scheduling | Free — [cal.com/pricing](https://cal.com/pricing) |
| Anthropic API | LLM scoring and transcript analysis | ~$3/MTok input (Sonnet) — [docs.anthropic.com/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |

**Estimated play-specific cost:** ~$350-700/mo (Clay $185-495 + Instantly $97 + n8n $24-60 + Fireflies $18 + Anthropic ~$15-30)

## Drills Referenced

- `bant-auto-scoring` — automated pre-qualification pipeline: CRM trigger > Clay enrichment > BANT scoring > Attio routing
- `follow-up-automation` — n8n workflows for score-based outreach, nurture, and re-scoring alerts
- `ab-test-orchestrator` — A/B experiments on scoring weights, thresholds, and outreach personalization
- `bant-qualification-reporting` — dashboards, funnel analytics, accuracy cohorts, and weekly reports
