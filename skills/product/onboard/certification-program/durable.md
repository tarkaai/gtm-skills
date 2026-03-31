---
name: certification-program-durable
description: >
  Product Certification Program — Durable Intelligence. Always-on AI agents monitor
  certification health, detect anomalies, generate hypotheses, run experiments, and
  auto-implement winners. The autonomous-optimization drill drives continuous
  improvement toward the local maximum. Weekly optimization briefs. Converges when
  successive experiments produce <2% improvement.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email, Content"
level: "Durable Intelligence"
time: "Ongoing (20 hours setup + 2 hours/week monitoring)"
outcome: "Sustained or improving certification metrics over 6 months via autonomous optimization; convergence detected when experiments yield <2% lift"
kpis: ["Certification volume trend", "Completion rate trend", "Retention lift trend", "Experiment velocity", "Net optimization lift", "Convergence status"]
slug: "certification-program"
install: "npx gtm-skills add product/onboard/certification-program"
drills:
  - autonomous-optimization
  - certification-health-monitor
  - nps-feedback-loop
---

# Product Certification Program — Durable Intelligence

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Content

## Outcomes

The certification program is self-optimizing. An AI agent continuously monitors certification health, detects when metrics plateau or degrade, generates hypotheses for improvement, runs A/B experiments, evaluates results, and auto-implements winners. The goal is to find and maintain the local maximum — the best possible certification performance given the current product, audience, and competitive landscape. The optimization loop converges when successive experiments produce <2% improvement for 3 consecutive cycles.

## Leading Indicators

- Anomaly detection fires within 24 hours of a metric shift (monitoring is responsive)
- Hypotheses generated per anomaly ≥3 (diagnosis is comprehensive)
- Experiment cycle time ≤2 weeks (optimization velocity is high)
- Net optimization lift positive for 4+ consecutive weeks (improvements are compounding)
- Weekly optimization briefs are generated on schedule (the loop is running)

## Instructions

### 1. Deploy the certification health monitor

Run the `certification-health-monitor` drill to establish the monitoring layer:
- Daily health check across 8 certification metrics: enrollment rate, Tier 1 completion, tier transition, median completion time, module pass rate, stall rate, retention lift, and advocate rate
- Weekly health digest with trend analysis and experiment status
- Certified vs non-certified retention comparison
- Per-module content quality monitoring
- Alert system for Critical metric degradation (>20% decline from 4-week baseline)

This monitoring layer feeds anomalies directly into the autonomous optimization loop.

### 2. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the certification program:

**Phase 1 — Monitor (daily via n8n cron):**
- Pull the 8 certification health metrics from PostHog
- Compare last 2 weeks against 4-week rolling average
- Classify each metric: normal (±10%), plateau (±2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If normal for all metrics → log to Attio, no action
- If anomaly detected → trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Pull the anomaly context: which metric, which segment, which cohort, which time period
- Gather current certification configuration: enrollment prompts, module content, stall thresholds, email copy, cohort size
- Run hypothesis generation with anomaly data + configuration context
- Receive 3 ranked hypotheses with expected impact and risk

Example hypotheses the agent might generate:
- "Enrollment rate dropped because the in-app banner is now competing with a new product tour. Hypothesis: move enrollment to a post-tour trigger." (Risk: low)
- "Tier 2 completion fell because Module 3 assessment pass rate dropped after last product update broke the tracked action. Hypothesis: fix the PostHog event mapping." (Risk: low)
- "Stall rate increased because cohort size doubled and social proof messaging is less effective with larger groups. Hypothesis: segment cohorts to max 30 users." (Risk: medium)

If top hypothesis risk = "high" → alert human for review and STOP.
If risk = "low" or "medium" → proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment using PostHog experiments: control (current) vs variant (hypothesis change)
- Implement the variant:
  - For enrollment changes: update Intercom message targeting or Loops email copy
  - For module changes: update Intercom Product Tour or assessment criteria
  - For stall changes: update n8n workflow thresholds or nudge content
  - For cohort changes: update n8n batching logic
- Set experiment duration: minimum 7 days or 100+ samples per variant, whichever is longer
- Log experiment start in Attio

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run experiment evaluation: statistical significance, practical significance, secondary metric impact
- Decision:
  - **Adopt:** Primary metric improved ≥2% with statistical significance, no secondary metric degraded. Auto-implement the winner. Log the change.
  - **Iterate:** Result not significant but directionally positive. Generate a refined hypothesis and return to Phase 2.
  - **Revert:** Variant performed worse or secondary metric degraded. Disable variant, restore control. 7-day cooldown on that variable.
  - **Extend:** Insufficient sample size. Continue for another period.

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate the week's optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes
- Generate weekly optimization brief:
  - What changed and why
  - Net impact on certification KPIs
  - Current distance from estimated local maximum
  - Recommended focus for next week
  - Convergence status: are successive experiments producing diminishing returns?
- Post to Slack and store in Attio

### 3. Configure optimization guardrails

Apply the guardrails from the `autonomous-optimization` drill to the certification context:

- **Rate limit:** Maximum 1 active experiment at a time on the certification program
- **Revert threshold:** If enrollment rate or completion rate drops >30% during an experiment, auto-revert immediately
- **Human approval required for:**
  - Changes to the curriculum structure (adding/removing modules or tiers)
  - Changes that affect >50% of enrolled users mid-certification
  - Any change flagged as "high risk" by the hypothesis generator
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review
- **Never optimize unmeasured variables:** If a certification metric does not have PostHog tracking, fix tracking first

### 4. Launch NPS feedback loop for certified users

Run the `nps-feedback-loop` drill targeted at certified users:
- Trigger NPS survey 14 days after badge earned (not immediately — let them use the product with their new skills first)
- Segment responses:
  - **Promoters (9-10):** Ask for a review, case study, or referral. Feed into the advocate tracking pipeline.
  - **Passives (7-8):** Ask what would make the certification more valuable. Feed answers into the hypothesis generator.
  - **Detractors (0-6):** Personal follow-up. What did the certification NOT teach that they needed? This is curriculum design input.
- Route feedback themes to the optimization loop: if multiple detractors cite the same issue, generate a hypothesis for it

### 5. Build the Durable dashboard

Extend the Scalable dashboard with optimization-specific panels:

| Panel | Type | Purpose |
|-------|------|---------|
| Optimization loop status | Status indicator | Is the loop running? Last anomaly? Current experiment? |
| Experiment history | Table | All experiments: hypothesis, duration, result, impact |
| Net optimization lift (cumulative) | Area chart | Total improvement from all adopted experiments |
| Convergence tracker | Line chart | Lift % from last 5 experiments — declining = approaching local maximum |
| Weekly optimization brief | Text/link | Latest brief with click-through to full report |
| NPS by certification tier | Bar chart | Are higher tiers producing more promoters? |
| Certified advocate pipeline | Funnel | Badge earned → shared → referred → referral converted |

### 6. Detect convergence

The optimization loop should detect when the certification program has reached its local maximum:
- Track the improvement percentage from each successive adopted experiment
- If 3 consecutive experiments produce <2% improvement, the program is converged
- At convergence:
  1. Reduce monitoring frequency from daily to weekly
  2. Reduce experiment cadence from continuous to monthly spot-checks
  3. Generate a convergence report: "Certification program optimized. Current performance: [metrics]. Further gains require strategic changes (new content types, new tiers, product changes, audience expansion) rather than tactical optimization."
  4. Shift optimization agent resources to other plays

## Time Estimate

- 8 hours: Deploy certification health monitor
- 6 hours: Configure autonomous optimization loop (n8n workflows, hypothesis templates, experiment pipeline)
- 3 hours: Set up guardrails and alert routing
- 3 hours: Configure NPS feedback loop for certified users
- 2 hours/week: Review weekly optimization briefs, approve high-risk hypotheses, strategic oversight

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, dashboards, cohorts | Usage-based: ~$0-100/mo depending on volume — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app messages, Product Tours, NPS surveys | Advanced: $85/seat/mo + Proactive Support: $349/mo — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Automated sequences (enrollment, stall, celebration, NPS follow-up) | Starter: $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Optimization loop orchestration, health monitoring, experiment management | Self-hosted: Free; Cloud: from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | Hypothesis generation, experiment evaluation, brief generation | Usage-based: ~$15-50/mo at experiment velocity of 1/week — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost:** Intercom ~$434/mo + Loops ~$49/mo + Anthropic API ~$30/mo = ~$513/mo + variable PostHog usage

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: monitor → diagnose → experiment → evaluate → implement. This is what makes Durable fundamentally different from Scalable.
- `certification-health-monitor` — daily/weekly monitoring of 8 certification metrics with anomaly detection feeding the optimization loop
- `nps-feedback-loop` — collect and act on feedback from certified users to inform optimization hypotheses
