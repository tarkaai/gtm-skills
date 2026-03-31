---
name: need-assessment-framework-scalable
description: >
  Need Assessment Framework — Scalable Automation. Automated pre-call need hypothesis pipeline
  that predicts likely need profiles before discovery, routes based on predicted score, and runs
  A/B experiments on scoring weights, question sequences, and qualification thresholds to find
  the 10x multiplier.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Email, Direct"
level: "Scalable Automation"
time: "55 hours over 2 months"
outcome: ">=70% need assessment completion at 100+ leads/month with automated pre-scoring and need score predicting close rate within 20% accuracy"
kpis: ["Need assessment completion rate at scale", "Pre-hypothesis accuracy vs post-call", "Time saved by auto-hypothesis", "False positive rate (High Need but lost)", "Cost per qualified lead", "Leads processed per month"]
slug: "need-assessment-framework"
install: "npx gtm-skills add sales/qualified/need-assessment-framework"
drills:
  - follow-up-automation
  - ab-test-orchestrator
  - dashboard-builder
---

# Need Assessment Framework — Scalable Automation

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Outcomes

Scale need assessment from manual discovery calls to an automated pre-scoring pipeline that handles 100+ leads per month. Every new lead gets a need hypothesis generated automatically via enrichment data before any human contact. Discovery calls are pre-loaded with tailored questions that probe the specific gaps in each prospect's need profile. The 10x multiplier: automated pre-qualification reduces wasted discovery calls on Low Need prospects and focuses founder time on the highest-need opportunities.

## Leading Indicators

- Auto-hypothesis pipeline processes new leads within 10 minutes of CRM entry
- Pre-hypothesis accuracy exceeds 65% (hypothesis scores within 4 points of post-call scores)
- Founder is only spending discovery call time on leads pre-scored at Medium Need or above
- A/B experiments on need question sequences and scoring weights are producing measurable accuracy improvements
- Cost per qualified lead is trending down month-over-month
- Need-triggered content (case studies, ROI examples matching specific need categories) is improving meeting booking rate

## Instructions

### 1. Deploy automated need hypothesis generation

Run the the play's scoring criteria drill to build the automated pipeline:

1. **Trigger:** n8n workflow fires when a new deal is created in Attio (from any source: outbound list, inbound form, referral)
2. **Enrich:** Push the lead to Clay for need-relevant enrichment — job postings, tech stack, growth signals, industry context (see `clay-enrichment-waterfall` and `clay-intent-scoring` fundamentals)
3. **Hypothesize:** Claude synthesizes enrichment signals into a per-category need prediction with confidence scores
4. **Route:** Push hypothesis scores back to Attio and move the deal to the appropriate stage:
   - Predicted High Need (>=15): "Need Hypothesized" + Slack alert to founder with tailored discovery questions
   - Predicted Medium Need (10-14): "Need Hypothesized" + note listing which categories are uncertain
   - Predicted Low Need (<10): "Need Hypothesized" at lower priority + consider batch discovery
5. **Log:** Fire PostHog event `need_hypothesis_generated` with all scores and confidence

This runs on autopilot. Every lead that enters your CRM gets a need hypothesis within minutes, and the founder gets a pre-populated question guide for the discovery call.

### 2. Build automated follow-up workflows

Run the `follow-up-automation` drill to create n8n workflows that act on need assessment scores:

- **High Need leads (score >=15):** Auto-generate a personalized outreach email referencing their predicted strongest need category. Example: "Saw you're hiring 3 data analysts — we help companies at your stage eliminate the manual data work that creates that headcount need." Send via Instantly.
- **Medium Need leads (10-14):** Enroll in a need-specific nurture sequence. If their predicted weakest need category is "reducing operational cost," send case studies showing ROI and cost savings. If "improving data accuracy," send content about error rates and data quality.
- **Need score change alerts:** When a prospect's enrichment data changes (new job posting, funding announcement, tech stack change), trigger re-hypothesis. Alert the founder if the predicted score crosses the 15 threshold.
- **Post-assessment follow-up:** After a discovery call scores a prospect Medium Need (12-14), auto-send need-specific content addressing the gap categories. Example: if "improving reporting visibility" was the only non-Critical category, send a reporting dashboard case study.

### 3. Run A/B experiments on scoring and discovery

Run the `ab-test-orchestrator` drill to set up experiments that improve need assessment accuracy and qualification:

**Experiment 1 — Need category weight optimization:**
- Control: Equal weight per category (each contributes 3 max to total of 21)
- Variant: Weighted scoring where categories that historically predict closed-won get higher weight (e.g., "reducing manual work" counts as 4 max while "improving reporting visibility" counts as 2 max)
- Measure: which weighting produces higher need-score-to-close correlation
- Duration: 4 weeks, minimum 50 prospects per variant

**Experiment 2 — Discovery question sequence:**
- Control: Ask about need categories in order of predicted severity (strongest first)
- Variant: Ask about need categories in order of uncertainty (unknown first, to maximize information gain)
- Measure: which sequence produces more complete need assessments (fewer categories scored 0) and more accurate scores
- Duration: 20+ calls per variant

**Experiment 3 — Qualification threshold tuning:**
- Control: Qualified = total score >=12, >=2 Critical
- Variant A: Qualified = total score >=10, >=2 Critical (lower bar)
- Variant B: Qualified = total score >=12, >=3 Critical (higher bar on Critical count)
- Measure: which threshold maximizes true positive rate while minimizing false positives
- Duration: 4 weeks

Use PostHog feature flags to randomly assign variants. Evaluate using the `ab-test-orchestrator` drill's statistical significance checks.

### 4. Scale volume

Increase prospect volume to 200-500 per month by:
- Expanding Clay enrichment tables with new ICP segments validated in Baseline
- Adding new lead sources (inbound forms, partner referrals, event attendees) that all flow through the same need hypothesis pipeline
- Monitoring enrichment credit usage and optimizing waterfall provider order

All new leads, regardless of source, enter the same need hypothesis pipeline. No manual triage.

### 5. Build need assessment reporting

Run the `dashboard-builder` drill to create:

- **PostHog dashboard:** Assessment volume by week, need category heatmap, score distribution, hypothesis accuracy trend
- **Pipeline velocity funnel:** Hypothesis > Assessment > Qualified > Demo > Proposal > Won
- **Scoring accuracy cohorts:** True positives, false positives, true negatives, false negatives
- **Need pattern analysis:** Winning need combinations, deal size correlation, speed correlation
- **Weekly automated report:** Slack summary every Monday with key metrics and hypothesis accuracy trend
- **Anomaly alerts:** Qualification rate drop, hypothesis accuracy degradation, pipeline stall

### 6. Evaluate against threshold

After 2 months, measure against: >=70% need assessment completion at 100+ leads/month with need score predicting close rate within 20% accuracy.

Review:
- Is the auto-hypothesis accurate enough to prioritize discovery calls effectively?
- Which A/B experiments produced winners?
- What is the cost per qualified lead?
- Which need categories are strongest predictors of close?

If PASS, proceed to Durable. If FAIL, diagnose:
- Low hypothesis accuracy: enrichment signals are weak need proxies — add providers or rethink signal mapping
- Low completion rate at scale: discovery call bottleneck — consider hiring or implementing self-serve need assessment
- High false positive rate: scoring model is too generous — raise thresholds or add a validation step

## Time Estimate

- Auto-hypothesis pipeline setup: 8 hours
- Follow-up automation workflows: 6 hours
- A/B experiment design and setup: 8 hours
- Reporting dashboard and alerts: 4 hours
- Ongoing discovery calls (scaled): 16 hours over 2 months
- Monitoring, optimization, and analysis: 13 hours over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with need assessment pipeline | Plus $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment with need signals at scale | Launch $185/mo or Growth $495/mo — [clay.com/pricing](https://clay.com/pricing) |
| Instantly | Cold email sequences | Hypergrowth $97/mo — [instantly.ai/pricing](https://instantly.ai/pricing) |
| n8n | Automation orchestration | Starter $24/mo or Pro $60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Fireflies | Call transcription | Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics, experiments, feature flags | Free (1M events/mo) or usage-based — [posthog.com/pricing](https://posthog.com/pricing) |
| Cal.com | Scheduling | Free — [cal.com/pricing](https://cal.com/pricing) |
| Anthropic API | Need hypothesis generation + transcript extraction | ~$3/MTok input (Sonnet) — [docs.anthropic.com/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |

**Estimated play-specific cost:** ~$370-720/mo (Clay $185-495 + Instantly $97 + n8n $24-60 + Fireflies $18 + Anthropic ~$20-50)

## Drills Referenced

- the play's scoring criteria — automated pre-call need hypothesis pipeline: CRM trigger > Clay enrichment > Claude hypothesis > Attio routing
- `follow-up-automation` — n8n workflows for need-tier-based outreach, nurture, and re-hypothesis alerts
- `ab-test-orchestrator` — A/B experiments on scoring weights, discovery question sequences, and qualification thresholds
- `dashboard-builder` — dashboards, funnel analytics, accuracy cohorts, need pattern analysis, and weekly reports
