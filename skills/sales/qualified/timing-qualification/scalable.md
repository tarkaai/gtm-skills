---
name: timing-qualification-scalable
description: >
  Timing Qualification Process — Scalable Automation. Automated pre-qualification pipeline
  predicts buying timeline from enrichment signals before any human contact. Every new deal
  gets auto-scored within minutes of CRM entry. A/B experiments optimize scoring weights,
  cadence timing, and urgency messaging. The 10x multiplier: automated prediction eliminates
  wasted discovery calls on Long-term prospects.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Email, Direct"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: ">=70% timeline qualification rate at 100+ leads/month with auto-scoring prediction accuracy >=65% and forecast accuracy within 21 days"
kpis: ["Timeline qualification rate at scale", "Auto-score prediction accuracy (pre vs post-call)", "Forecast accuracy (predicted vs actual close date)", "Slippage rate", "Cost per timeline-qualified lead", "Leads processed per month"]
slug: "timing-qualification"
install: "npx gtm-skills add sales/qualified/timing-qualification"
drills:
  - follow-up-automation
  - ab-test-orchestrator
  - timing-qualification-reporting
---

# Timing Qualification Process — Scalable Automation

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Outcomes

Scale timing qualification from manual discovery-call-based scoring to an automated pre-scoring pipeline. Every new deal gets a predicted timeline category within minutes of entering the CRM — before any human contact. The auto-score routes Immediate deals to fast-track outreach and filters Long-term deals to nurture, so the founder only spends discovery call time on prospects with genuine urgency. The 10x multiplier: automated timeline prediction eliminates wasted calls on prospects who are 6+ months away, concentrating human effort on deals that will close in the near term.

## Leading Indicators

- Auto-scoring pipeline processes new leads within 5 minutes of CRM entry
- Pre-score prediction accuracy exceeds 65% (auto-predicted category matches post-call human-validated category)
- Founder is only running timing discovery calls on leads pre-scored as Immediate or Near-term
- A/B experiments on scoring weights and cadence timing are producing measurable improvements
- Slippage rate is trending down as early-stage timeline prediction improves
- Cost per timeline-qualified lead is lower than Baseline (due to automation replacing manual qualification)

## Instructions

### 1. Deploy automated timeline pre-scoring

Run the the play's scoring criteria drill to build the automated pipeline:

1. **Trigger:** n8n workflow fires when a new deal is created in Attio (from any source: outbound list, inbound form, referral)
2. **Enrich:** Push the lead to Clay for timing-relevant signals: last funding round, open job postings, technology stack changes, competitor contract renewal estimates, fiscal year end, recent news, company growth rate
3. **Predict:** Clay enrichment data is sent to Claude, which classifies the deal into a timeline category with confidence score and predicted urgency drivers
4. **Route:** Scores are written back to Attio and the deal is routed:
   - Immediate (confidence >= 3): Slack alert to founder. Book a call within 24 hours.
   - Near-term (confidence >= 3): Add to active outreach. Priority follow-up within the week.
   - Medium-term: Add to standard cadence. Discovery call optional.
   - Long-term: Nurture sequence. No discovery call unless signal changes.
5. **Log:** Fire PostHog event `timing_auto_score_completed` with all scores

This runs on autopilot. Every lead that enters the CRM gets timeline-predicted within minutes.

### 2. Build score-based follow-up workflows

Run the `follow-up-automation` drill to extend Baseline cadences with auto-score awareness:

- **Auto-scored Immediate:** Trigger an urgency-aware outreach immediately. Reference the specific urgency signal detected (e.g., "I noticed your team just raised a Series B — companies at your stage usually need {product} in place before scaling hiring. When are you planning to have this solved?")
- **Auto-scored Near-term:** Enroll in an evaluation-focused sequence referencing their likely timeline ("Most companies in your space implement this over 60-90 days. Would it make sense to start the evaluation now?")
- **Score upgrade alerts:** When a Long-term prospect's signals change (new funding, job posting, competitive move), trigger re-scoring. If the category shifts to Near-term or Immediate, alert the founder and promote to active pipeline.
- **Discovery call prioritization:** Build a daily queue of prospects rank-ordered by timeline urgency. The founder works this queue top-down instead of handling leads in arrival order.

### 3. Run A/B experiments

Run the `ab-test-orchestrator` drill to set up experiments that improve prediction and conversion:

**Experiment 1 — Scoring signal weighting:**
- Control: Equal weight across all enrichment signals
- Variant: 2x weight on "recent funding" and "job postings in relevant department" (the two signals that most often correlated with Immediate/Near-term in Baseline data)
- Measure: prediction accuracy (auto-score vs post-call validation)
- Duration: 4 weeks, minimum 50 prospects per variant

**Experiment 2 — Cadence timing by category:**
- Control: Standard Baseline cadences (daily for Immediate, 2-3x/week for Near-term)
- Variant: Accelerated cadences (2x daily for Immediate within first 72 hours, daily for Near-term)
- Measure: deal velocity (days from first touch to proposal)
- Duration: 4 weeks

**Experiment 3 — Urgency messaging approach:**
- Control: Feature-focused outreach ("Here's what we can do for you")
- Variant: Consequence-focused outreach ("Here's what happens if you don't solve this by {their deadline}")
- Measure: reply rate and meeting booking rate
- Duration: 100 sends per variant

Use PostHog feature flags to randomly assign variants. The `ab-test-orchestrator` drill handles statistical significance checks.

### 4. Scale volume

Increase prospect volume to 200-500 per month by:
- Expanding Clay enrichment tables with new ICP segments validated in Baseline
- Adding new lead sources (inbound forms, partner referrals, event attendees) that all flow through the same auto-scoring pipeline
- Setting up signal-based prospecting: Clay monitors for timing signals (funding, job postings, leadership changes) and auto-creates deals for companies that match ICP + have urgency signals

All new leads, regardless of source, enter the same auto-scoring pipeline. No manual triage.

### 5. Build scaled reporting

Run the `timing-qualification-reporting` drill to extend Baseline dashboards with:

- **Auto-score accuracy panel:** Prediction accuracy over time (auto-predicted category vs human-validated)
- **A/B experiment tracker:** Active experiments, their status, and cumulative wins
- **Cost per qualified lead trend:** Should be declining as automation replaces manual qualification
- **Pipeline concentration risk:** Alert if >50% of Immediate pipeline comes from a single urgency driver (over-reliance on one signal)

### 6. Evaluate against threshold

After 2 months, measure against: >=70% timeline qualification rate at 100+ leads/month with auto-scoring prediction accuracy >=65% and forecast accuracy within 21 days.

Review:
- Is auto-scoring accurate enough to route deals without human pre-screening?
- Which A/B experiments produced winners? Implement winning variants as defaults.
- What is the cost per timeline-qualified lead? Is it lower than Baseline?
- Where are the remaining bottlenecks: scoring accuracy, signal coverage, or cadence effectiveness?

If PASS, proceed to Durable. If FAIL, diagnose:
- Low prediction accuracy: enrichment signals are not timing-predictive — add better signal sources
- Low qualification rate at scale: too many leads entering with insufficient data — tighten lead source quality
- Slippage rate increasing: predictions look good at scoring time but don't hold — add validation steps

## Time Estimate

- Auto-scoring pipeline setup: 8 hours
- Follow-up automation (score-based): 6 hours
- A/B experiment design and setup: 6 hours
- Reporting dashboards: 4 hours
- Ongoing discovery calls (qualified leads only): 16 hours over 2 months
- Monitoring, optimization, and analysis: 10 hours over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with timeline pipeline | Plus $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment with timing signals at scale | Launch $185/mo or Growth $495/mo — [clay.com/pricing](https://clay.com/pricing) |
| Instantly | Email sequences (timeline-specific) | Hypergrowth $97/mo — [instantly.ai/pricing](https://instantly.ai/pricing) |
| n8n | Automation: scoring, routing, cadences | Pro $60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Fireflies | Call transcription for validated calls | Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics, experiments, feature flags | Free or usage-based ~$50-100/mo at scale — [posthog.com/pricing](https://posthog.com/pricing) |
| Cal.com | Scheduling | Free — [cal.com/pricing](https://cal.com/pricing) |
| Anthropic API | Auto-scoring and transcript extraction | ~$15-40/mo at scaled volume — [docs.anthropic.com/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |

**Estimated play-specific cost:** ~$350-850/mo (Clay $185-495 + Instantly $97 + n8n $60 + Fireflies $18 + PostHog ~$50-100 + Anthropic ~$15-40)

## Drills Referenced

- the play's scoring criteria — automated pre-qualification pipeline: CRM trigger > Clay enrichment > Claude scoring > Attio routing
- `follow-up-automation` — n8n workflows for score-based outreach, cadence management, and re-scoring alerts
- `ab-test-orchestrator` — A/B experiments on scoring weights, cadence timing, and urgency messaging
- `timing-qualification-reporting` — dashboards with prediction accuracy, experiment tracking, and cost analysis
