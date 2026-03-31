---
name: meddic-qualification-scalable
description: >
  MEDDIC Qualification System — Scalable Automation. Deploy always-on deal health monitoring,
  automated element gap alerts, A/B test discovery question strategies, and scale MEDDIC
  qualification to 50+ concurrent deals without proportional founder time.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: ">=50% of deals with >80% MEDDIC completeness and >=15% higher close rate over 2 months"
kpis: ["MEDDIC completeness rate", "Deal health score", "Close rate by MEDDIC quartile", "Velocity by MEDDIC score"]
slug: "meddic-qualification"
install: "npx gtm-skills add sales/connected/meddic-qualification"
drills:
  - meddic-deal-health-monitor
  - meddic-qualification-reporting
  - ab-test-orchestrator
  - tool-sync-workflow
  - follow-up-automation
---

# MEDDIC Qualification System — Scalable Automation

> **Stage:** Sales > Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Scale MEDDIC qualification from a manual process that requires founder attention per-deal to an automated system that monitors 50+ concurrent deals, surfaces risks proactively, and routes founder time to the highest-impact actions. The 10x multiplier: instead of the founder reviewing every deal, the agent monitors all deals continuously and only escalates when specific MEDDIC elements degrade or require human intervention. Close rate for MEDDIC-qualified deals should be 15%+ higher than unqualified deals over 2 months.

## Leading Indicators

- Deal health monitor running daily, processing all active deals without manual intervention
- At least 1 critical alert triggered and acted on (champion loss, economic buyer disengagement) within the first 2 weeks
- MEDDIC qualification dashboards showing per-element completion trends
- A/B test on discovery question strategies launched within first 3 weeks
- Founder time per deal decreasing while deal visibility increasing (measured via call prep time and post-call processing time)
- Stalled deal alerts triggering re-engagement actions automatically

## Instructions

### 1. Deploy always-on deal health monitoring

Run the `meddic-deal-health-monitor` drill. This creates an n8n workflow that runs daily at 7am:

1. Computes a health score for every active deal based on: MEDDIC composite (50%), element progression (20%), activity recency (15%), stage velocity (15%)
2. Classifies each deal as Healthy (70+), At Risk (40-69), or Critical (<40)
3. Fires critical alerts via Slack when:
   - Champion score drops below 30 (champion may be lost)
   - Economic Buyer score drops below 30 (budget holder disengaged)
   - Deal stuck in "Needs Work" for 21+ days with no element improvement
   - Pain score drops below 30 (pain may have resolved)
4. Generates a daily pipeline health digest with: critical deals requiring action, at-risk deal count, element trends, stalled deals
5. Auto-creates Attio tasks for critical deals: "Re-engage champion," "Request intro to economic buyer," "Re-validate pain"

This is the core scalability unlock — the agent watches every deal so the founder does not have to.

Estimated time: 6 hours setup, then always-on.

### 2. Build MEDDIC qualification dashboards and reporting

Run the `meddic-qualification-reporting` drill. This builds:

1. **PostHog dashboard** with 6 panels: qualification volume by verdict, score distribution, element completion heatmap, per-element trend lines, pre-score vs. post-call accuracy, deal health distribution
2. **Pipeline velocity funnel:** meddic_score_created -> qualification_passed -> champion_identified -> economic_buyer_engaged -> proposal_sent -> deal_closed_won
3. **Scoring accuracy cohorts:** True Positives (scored Qualified, closed won), False Positives (scored Qualified, closed lost), True Negatives, False Negatives
4. **Weekly automated report** via n8n: every Monday, generates a MEDDIC performance summary with element health table, pipeline movement, top deals, and action items
5. **Anomaly alerts** for: qualification rate below 20%, champion completion below 25%, false positive rate above 30%

Estimated time: 8 hours setup.

### 3. Connect and sync your full tool stack

Run the `tool-sync-workflow` drill to build n8n sync workflows ensuring no MEDDIC data is siloed:
- Clay enrichment scores -> Attio deal attributes
- Fireflies transcripts -> PostHog events (MEDDIC extraction completed, element scores)
- Attio deal stage changes -> PostHog events
- PostHog qualification milestones -> Slack notifications
- Attio deal health changes -> Slack alerts

Ensure every MEDDIC-related data point flows through the full stack without manual intervention.

Estimated time: 6 hours.

### 4. Launch A/B testing on discovery strategies

Run the `ab-test-orchestrator` drill. Set up experiments on:

1. **Discovery question ordering:** Test whether leading with pain questions vs. leading with metrics questions produces higher post-call MEDDIC completeness
2. **Call prep depth:** Test minimal prep (just weakest element questions) vs. comprehensive prep (questions for all 6 elements) — measure call duration and completeness
3. **Follow-up strategy by element gap:** Test different follow-up materials based on the weakest MEDDIC element:
   - Weak Champion: send internal advocacy toolkit vs. executive summary
   - Weak Economic Buyer: request warm intro vs. send business case directly
   - Weak Decision Criteria: send comparison matrix vs. offer technical deep-dive call
4. **Re-qualification timing:** Test re-scoring deals at 7 days vs. 14 days after initial assessment

Use PostHog feature flags to randomly assign variants. Run each test for minimum 20 deals per variant before evaluating.

Estimated time: 10 hours setup + monitoring.

### 5. Set up automated follow-ups for MEDDIC element gaps

Run the `follow-up-automation` drill to create n8n workflows that automatically trigger follow-up actions based on MEDDIC element gaps:

- **Champion gap (score < 40 after discovery):** Auto-send champion enablement materials (product one-pager, ROI calculator, internal presentation template) via email sequence
- **Economic Buyer gap (score < 40):** Auto-create task for founder: "Request warm introduction to {economic_buyer_title} at {company}" with suggested email draft
- **Decision Criteria gap (score < 40):** Auto-send competitive comparison document tailored to their tech stack
- **Decision Process gap (score < 40):** Auto-send email asking about procurement timeline with offer to provide compliance/security documentation
- **Metrics gap (score < 40):** Auto-send case study with quantified outcomes from a similar company
- **Pain gap (score < 40):** Auto-send industry benchmark report highlighting the cost of inaction

Each follow-up is logged in Attio and tracked in PostHog.

Estimated time: 8 hours.

### 6. Scale deal volume

With monitoring, reporting, and automated follow-ups in place, scale to 50+ concurrent deals:
- Auto-scoring handles all new deal pre-qualification
- Deal health monitor watches every deal daily
- Follow-up automation addresses element gaps without founder time
- Founder focuses only on: discovery calls (with auto-generated prep), critical deal interventions (from alerts), and economic buyer meetings

Monitor system health weekly: check n8n execution logs for errors, review deal health distribution, ensure no bottlenecks.

Estimated time: 32 hours ongoing over 2 months.

### 7. Evaluate against threshold

After 2 months, measure:
- **MEDDIC completeness rate:** >=50% of deals with >80% completeness. Break down by element — which elements are hardest to complete?
- **Close rate by MEDDIC quartile:** Deals in the top MEDDIC quartile (75+) should close at >=15% higher rate than bottom quartile (<50). If not, scoring weights need recalibration.
- **Deal health score distribution:** Is the pipeline getting healthier over time? Track weekly average health score.
- **Velocity by MEDDIC score:** Do higher-scored deals close faster? Measure time from Connected to Won by score quartile.

Also measure operational efficiency:
- Founder time per deal at Baseline vs. Scalable (should decrease)
- Number of stalled deals caught by monitoring (should increase)
- A/B test results: which strategies won?

If PASS, proceed to Durable. If FAIL, focus on the weakest metric. Common failure modes:
- Low completeness: auto-scoring may not be firing or discovery calls are inconsistent
- Low close rate lift: scoring model may not reflect actual deal dynamics — run monthly calibration
- Low velocity improvement: element gap follow-ups may not be converting — review A/B test data

## Time Estimate

- Deal health monitor setup: 6 hours
- Reporting and dashboards: 8 hours
- Tool sync workflows: 6 hours
- A/B test setup: 10 hours
- Follow-up automation: 8 hours
- Ongoing operations (2 months): 32 hours

**Total: ~70 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, MEDDIC pipeline, task creation | Standard stack (excluded) |
| PostHog | Dashboards, funnels, cohorts, feature flags, anomaly alerts | Standard stack (excluded) |
| n8n | Orchestration — health monitor, auto-scoring, follow-ups, reporting | Standard stack (excluded) |
| Clay | Prospect enrichment at scale (50+ deals/month) | Growth: $495/mo (more credits for scale). [clay.com/pricing](https://www.clay.com/pricing) |
| Fireflies.ai | Call transcription for all discovery calls | Business: $19/user/mo (API access, team analytics). [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Instantly | Email sequences for element-gap follow-ups | Growth: $37/mo. [instantly.ai/pricing](https://instantly.ai/pricing) |
| Anthropic API | Claude for transcript extraction, call prep, follow-up copy | ~$30-80/mo at scale volume. [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Play-specific cost: ~$580-630/mo** (Clay Growth $495 + Fireflies Business $19 + Instantly $37 + Anthropic ~$30-80)

## Drills Referenced

- `meddic-deal-health-monitor` — daily health scoring with risk alerts and stalled deal detection
- `meddic-qualification-reporting` — dashboards, funnels, accuracy cohorts, and weekly reports
- `ab-test-orchestrator` — A/B testing on discovery strategies and follow-up approaches
- `tool-sync-workflow` — connects all tools so no MEDDIC data is siloed
- `follow-up-automation` — automated element-gap follow-ups triggered by low MEDDIC scores
