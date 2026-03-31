---
name: case-study-content-program-durable
description: >
  Case Study Content Program — Durable Intelligence. Autonomous AI agents optimize
  the entire case study lifecycle: detect engagement and conversion anomalies per
  case study, generate hypotheses for story and format improvements, run A/B
  experiments on narratives and distribution strategies, auto-implement winners,
  and produce weekly optimization briefs. The system finds the local maximum for
  case study impact on deal close rate and maintains it as market conditions change.
stage: "Marketing > ProductAware"
motion: "LeadCaptureSurface"
channels: "Content, Website"
level: "Durable Intelligence"
time: "90 hours over 6 months"
outcome: "Case study-influenced deal close rate sustained at ≥ Scalable benchmark for 6 consecutive months, with ≤ 3 hours/week team involvement"
kpis: ["Monthly case-study-influenced deal close rate (sustained at Scalable benchmark or improving)", "Monthly case study page views (sustained ≥ 4,000)", "Monthly conversions (sustained ≥ 60)", "Case study engagement rate across all formats (target ≥ 5%)", "Story refresh velocity (target: refresh top 5 case studies at least once per quarter)", "Production velocity (sustained ≥ 3/month)", "Recruitment pipeline health (acceptance rate ≥ 25%)"]
slug: "case-study-content-program"
install: "npx gtm-skills add marketing/product-aware/case-study-content-program"
drills:
  - autonomous-optimization
  - case-study-recruitment-health-monitor
  - dashboard-builder
---

# Case Study Content Program — Durable Intelligence

> **Stage:** Marketing > ProductAware | **Motion:** LeadCaptureSurface | **Channels:** Content, Website

## Outcomes

The case study program runs autonomously. AI agents monitor every case study for engagement and conversion anomalies, track the recruitment pipeline health, generate hypotheses when metrics change, run A/B experiments on story structure and distribution strategies, auto-implement winners, and produce weekly optimization briefs. The system finds the local maximum for case study impact on deal close rate and maintains it as traffic patterns, competitor content, and prospect behavior change over time.

Pass: Case study-influenced deal close rate stays at or above the Scalable benchmark for 6 consecutive months, with ≥ 4,000 page views/month, ≥ 60 conversions/month, and ≤ 3 hours/week of team involvement (reviewing briefs and approving high-risk changes only).
Fail: Close rate lift drops below 10% for 3 consecutive weeks despite automated interventions, or the system requires more than 5 hours/week of manual effort.

## Leading Indicators

- The `autonomous-optimization` loop produces a winning experiment at least once per month for the first 3 months (the system is still finding improvements to case study format, placement, or distribution)
- Recruitment pipeline health stays in the "healthy" range on all 7 metrics tracked by the `case-study-recruitment-health-monitor` (the input side of the program is stable)
- Case study refresh cycle keeps the top 5 case studies updated with the customer's latest metrics at least once per quarter (stories stay current and credible)
- The deal matching engine's forward rate (sales reps actually using the matched case studies) stays above 30% for 6 months (the matching remains relevant)
- Successive experiments produce diminishing returns after month 4 (convergence toward local maximum -- this is the goal, not a failure)
- Weekly optimization briefs are generated and delivered without human triggering

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the case study program's core metrics. This is the system that makes Durable fundamentally different from Scalable -- an always-on agent loop that monitors, diagnoses, experiments, and implements.

**Configure the monitoring phase (daily via n8n cron):**

The agent checks daily against 4-week rolling averages:

- Overall case study page conversion rate (across all case studies)
- Per-case-study conversion rates (identify which stories are underperforming)
- Case study hub traffic and filter usage patterns
- PDF download rate (gated content conversion)
- Deal routing forward rate (are sales reps using the matched case studies)
- Case-study-influenced deal close rate (the primary business outcome metric)
- Multi-format engagement rates: email snippet click rate, LinkedIn post engagement, in-app banner click rate

Classification thresholds:
- **Normal:** within +/- 10% of 4-week rolling average
- **Plateau:** within +/- 2% for 3+ weeks (no improvement, no degradation)
- **Drop:** > 20% decline from rolling average
- **Spike:** > 50% increase (investigate -- could be a viral share or a content quality issue with a new case study)

If anomaly detected on any metric: trigger the diagnosis phase.

**Configure the diagnosis phase (triggered by anomaly):**

The agent gathers context:
1. Pull current case study library metadata from Attio: industries covered, use cases, publish dates, last refresh dates
2. Pull 8-week metric history from PostHog for the affected metric
3. Pull traffic source breakdown: did the anomaly correlate with a traffic source shift (e.g., organic dropping, direct increasing)?
4. Pull deal routing data: did the anomaly correlate with changes in deal volume or sales team behavior?
5. Run `hypothesis-generation` with the anomaly data + context

Example hypotheses the agent might generate:
- "Case study page conversion rate dropped 18% because the 3 highest-traffic case studies are all 6+ months old and prospects are seeing stale metrics. Hypothesis: refresh the top 3 case studies with updated customer results and republish."
- "PDF download rate dropped 25% on case studies published in the last month. Hypothesis: the new case studies use a results-first format that gives away the key metric upfront, reducing incentive to download the PDF. Test reverting to challenge-first structure for PDF-gated versions."
- "Deal close rate lift declined from +18% to +9% over the last 4 weeks. Hypothesis: the deal matching engine is routing case studies that match on industry but not on use case -- prospects see a company in their industry but doing something different. Weight use case match higher in the scoring algorithm."
- "LinkedIn post engagement for case study content declined 30%. Hypothesis: the derivative posts have become formulaic. Test a conversation-starter format (ask a question based on the case study insight) instead of a summary format."

Store hypotheses in Attio. If risk = "high" (e.g., changing the deal matching algorithm weights, altering the gated/ungated strategy, or refreshing a case study that the customer has not re-approved), send Slack alert and wait for human approval. Otherwise proceed to experiment.

**Configure the experiment phase (triggered by hypothesis acceptance):**

Use PostHog feature flags to test changes:
1. For case study page experiments: split traffic between the current version (control) and the modified version (variant) -- e.g., results-first vs challenge-first structure, different CTA copy, shorter vs longer format
2. For distribution experiments: split the audience -- e.g., test a new LinkedIn post format on 50% of case study promotions, or test a different email snippet structure on half of deal routing notifications
3. For deal matching experiments: shadow-test a new scoring algorithm by computing match scores with the new weights alongside the old weights and tracking which set predicts deal outcomes better (without changing what sales sees until evaluated)

Set experiment duration: minimum 14 days or 300 impressions per variant for page experiments, minimum 21 days for deal matching experiments (need deal cycle time for outcome data).

Log every experiment in Attio: hypothesis, start date, expected duration, success criteria, and the specific variable being tested.

**Configure the evaluation phase (triggered by experiment completion):**

The agent pulls PostHog results and runs `experiment-evaluation`:
- **Adopt:** Variant wins with ≥ 95% statistical significance and ≥ 5% relative improvement. The primary metric improved and the secondary metric (lead quality / deal close rate) did not decline by more than 10%. Update the live configuration. Log the change.
- **Iterate:** Results inconclusive or improvement < 5%. Generate a new hypothesis building on this result. Return to diagnosis.
- **Revert:** Variant performed worse, or lead quality / deal influence declined. Disable variant, restore control. Log the failure. Return to monitoring.

**Guardrails (enforced by n8n):**
- Maximum 2 active experiments at a time (1 on case study pages, 1 on distribution/matching). Never stack experiments on the same variable.
- If case study conversion rate drops > 30% during an experiment, auto-revert immediately.
- If deal close rate lift drops below 5% for 2 consecutive weeks, pause all experiments and alert the team.
- Maximum 4 page experiments and 2 matching experiments per month. If all fail in a month, pause optimization and flag for human strategic review.
- Never change a published case study's content without re-confirming customer approval. Refreshes require customer sign-off.
- Always monitor deal close rate as the ultimate business outcome metric. Optimizing page views or conversion rate at the expense of deal influence is a false win.

### 2. Deploy the recruitment health monitor

Run the `case-study-recruitment-health-monitor` drill. This provides the play-specific monitoring layer that keeps the input side of the program healthy. It tracks 7 recruitment metrics daily:

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Candidate pool (accounts with score ≥ 70) | 20+ | 10-19 | < 10 |
| Outreach acceptance rate | 25%+ | 15-24% | < 15% |
| Outreach response rate | 40%+ | 25-39% | < 25% |
| Interview completion rate | 85%+ | 70-84% | < 70% |
| Case study completion rate | 75%+ | 60-74% | < 60% |
| Time to publish (median days) | < 21 | 21-35 | > 35 |
| Pipeline velocity (published/month) | ≥ 3 | 1-2 | 0 |

The drill implements automated interventions:
- Stale outreach subject lines: flagged for refresh when open rate drops below 30% for 2 weeks
- No-show prevention: 3-touch reminder sequence (24h, 1h, 5min before interview)
- Draft approval nudge: follow-up at 7 days and 14 days if customer has not reviewed draft
- Pipeline stall: alert if no new case study published in 3 weeks

Diagnostics run when any metric enters warning or critical. The drill checks upstream causes (user base growth, scoring model calibration, competitive landscape) and recommends specific fixes.

Escalation: any metric critical for 5+ consecutive days, or zero case studies published in 4 weeks, triggers a Slack alert for human intervention.

### 3. Build the Durable performance dashboard

Run the `dashboard-builder` drill to create the comprehensive PostHog dashboard:

**Dashboard panels:**
- **Case study funnel:** hub_viewed -> page_viewed -> cta_clicked -> converted (8-week trend with Scalable baseline line)
- **Per-case-study heatmap:** conversion rate for each published case study, color-coded (green ≥ 3%, yellow 1-3%, red < 1%)
- **Deal influence tracker:** deals with case study routed -> deal owner forwarded -> prospect viewed -> deal won (conversion rates at each step)
- **Close rate lift:** rolling 4-week comparison of close rate for deals with case studies vs without
- **Recruitment pipeline funnel:** scored -> outreach sent -> interview scheduled -> case study published
- **Content freshness:** days since last update for each case study, flagged when > 90 days
- **Multi-format engagement:** views/clicks/shares across PDFs, blog posts, social posts, email snippets, in-app banners
- **Active experiment status:** current test, variant description, days running, interim results
- **Coverage gap map:** industries and use cases with active deals but no matching case study
- **Production velocity:** case studies published per month, trailing 6-month trend
- **Monthly page views and conversions:** trend with Scalable benchmarks

**Alerts (via n8n):**
- Any case study's conversion rate drops to 0 for 5+ days -> check if the page is accessible and CTAs are working
- Overall close rate lift drops below 10% for 2 weeks -> escalate to the optimization loop
- Recruitment pipeline velocity drops to 0 for 3 weeks -> check the recruitment health monitor for diagnostics
- Content freshness: any top-5 case study not updated in 120+ days -> trigger refresh workflow
- No experiments completed in 21+ days -> check if the optimization loop is running

### 4. Implement the case study refresh cycle

Build an n8n workflow that runs monthly:

1. Query Attio for all published case studies with `publish_date` or `last_refresh_date` older than 90 days
2. For each stale case study, query PostHog for current engagement and conversion metrics
3. Rank stale case studies by impact: high-traffic + high-influence case studies with stale metrics are the top refresh priority
4. For the top 2-3 refresh candidates, trigger an outreach email to the original customer via Loops: "It has been [X months] since we published your story. Your team has achieved even more since then -- we would love to update the case study with your latest results. It is a quick 15-minute conversation."
5. If the customer agrees: schedule a 15-minute refresh interview via Cal.com, update the case study with new metrics, regenerate derivative assets via the `case-study-content-scaling` pipeline (still running from Scalable)
6. If the customer declines or does not respond within 14 days: keep the current version but add a "Last verified: [date]" label. If the case study is the sole coverage for an important industry/use case, prioritize recruiting a new customer in that segment.

**Human action required:** Approve refreshed case studies before republication. The customer must sign off on updated metrics and quotes.

### 5. Generate weekly optimization briefs

Build an n8n workflow (configured in `autonomous-optimization` Phase 5) that runs every Monday:

1. **Case study program health:** Total page views, conversions, and close rate lift this week vs prior 4-week average
2. **Recruitment pipeline status:** Which metrics are healthy/warning/critical, any interventions fired
3. **Content performance ranking:** Top 3 and bottom 3 case studies by conversion rate and deal influence
4. **Experiment update:** What experiment ran, result, what was implemented or reverted
5. **Coverage gap update:** Which industries/use cases still lack case study coverage, ranked by active deal count
6. **Refresh status:** Which case studies were refreshed, which are due for refresh
7. **Distance from local maximum:** Are experiments still producing meaningful improvements, or has the system converged?
8. **Recommendations:** Specific actions for the team (e.g., "Recruit a Fintech case study -- 8 active deals, zero coverage" or "The results-first format won the last 2 experiments -- apply to all new case studies")

Deliver via Slack. Store in Attio as a program note.

**Human action required:** The team reads the weekly brief (5-10 minutes). Strategic decisions (new industry prioritization, format changes across all case studies, adjustments to the deal matching algorithm) require human sign-off. All tactical changes (CTA copy rotation, individual case study refreshes, Tier 1 asset regeneration) execute automatically.

### 6. Sustain for 6 months

The system runs continuously. The agent's responsibilities:
- Monitor all case study pages and distribution channels daily for engagement and conversion anomalies
- Run the optimization loop: detect -> diagnose -> experiment -> evaluate -> implement
- Monitor the recruitment pipeline health and trigger interventions when metrics decline
- Refresh stale case studies quarterly
- Generate weekly optimization briefs and monthly deep reviews
- Maintain deal matching accuracy (adjust scoring weights when experiments reveal better configurations)
- Detect convergence and reduce optimization intensity when the local maximum is reached

The team's responsibilities:
- Read the weekly Slack brief (5-10 minutes)
- Approve high-risk experiments and strategic changes
- Approve refreshed case study content (customer sign-off required)
- Review monthly coverage gap report and prioritize new industries/use cases (~15 minutes/month)

### 7. Evaluate sustainability after 6 months

Compute over the full 6-month period:

- Monthly close rate lift for each of the 6 months (target: ≥ Scalable benchmark every month)
- Monthly page views and conversions for each of the 6 months (target: ≥ 4,000 views and ≥ 60 conversions)
- Total case studies published (target: ≥ 18 new + refreshes)
- Recruitment pipeline health: acceptance rate, velocity, and candidate pool stability
- Number of A/B experiments run, number that produced significant improvements
- Convergence status: has the system found its local maximum?
- Cost per case study produced, cost per influenced deal
- Total team hours / total case studies = team time per case study

- **PASS (close rate lift sustained, views/conversions sustained, ≤ 3 hours/week team time):** The case study program is a durable, self-optimizing sales asset. Consider: expanding to video-first case studies, customer reference programs (connecting prospects directly with case study customers), or building case study-based ad campaigns targeting prospect lookalike audiences.
- **CONVERGED (metrics stable but experiments no longer produce gains):** The local maximum has been found. Reduce the optimization loop from daily to weekly monitoring. Shift experiment resources to other plays. The case study program is in maintenance mode -- focus on production velocity and refreshes.
- **DECLINING (metrics held for 4+ months then decayed):** Market conditions changed. Diagnose: Has the competitive landscape shifted (competitors publishing stronger case studies)? Has the product evolved but case studies still reference old features? Has the prospect profile changed? The agent should detect this via anomaly monitoring and recommend strategic changes.
- **FAIL (close rate lift below 5% for 3+ consecutive weeks):** The optimization loop is not adapting fast enough. Diagnose: Are experiments targeting the right variables? Is the deal matching algorithm still routing relevant case studies? Is the content quality declining as production scales? Has something changed in the sales process that makes case studies less influential? Fix the specific broken component or accept that this play requires more manual oversight.

## Time Estimate

- Autonomous optimization loop setup: 12 hours (Month 1)
- Recruitment health monitor deployment: 6 hours (Month 1)
- Dashboard and alert system: 6 hours (Month 1)
- Case study refresh workflow: 4 hours (Month 1)
- Weekly brief and monthly review workflows: 4 hours (Month 1)
- Setup subtotal: 32 hours
- Weekly agent monitoring and loop execution: 3 hours/week x 24 weeks = 72 hours (agent compute)
- Weekly team time: 30 min/week x 24 weeks = 12 hours
- Monthly team review: 15 min x 6 months = 1.5 hours
- Experiment execution and implementation: 3 hours/month x 6 months = 18 hours
- Case study refresh coordination: 2 hours/quarter x 2 = 4 hours
- Ongoing subtotal: ~58 hours (32 setup + 13.5 team + 12.5 buffer)
- Grand total: ~90 hours over 6 months (72 agent compute, 14 team, 4 buffer)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnels, experiments, feature flags, anomaly detection, dashboards | Free tier: 1M events/mo; paid ~$0.00005/event beyond ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Optimization loop, recruitment monitoring, refresh workflows, briefs | Pro ~$60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Case study metadata, deal pipeline, experiment log, program notes | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Ghost | Case study publishing and refreshes | Free self-hosted; Pro $9/mo ([ghost.org/pricing](https://ghost.org/pricing)) |
| Loops | Recruitment sequences, deal routing notifications, refresh outreach | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Intercom | In-app social proof banners | Essential $29/seat/mo annual ([intercom.com/pricing](https://intercom.com/pricing)) |
| Riverside | Video interviews for refreshes and new case studies | Standard $19/mo annual ([riverside.com/pricing](https://riverside.com/pricing)) |
| Cal.com | Interview and refresh call scheduling | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation, asset generation, brief writing | Usage-based ~$3/1M input tokens for Sonnet ([anthropic.com/pricing](https://anthropic.com/pricing)) |

**Estimated monthly cost for Durable:** $200-350/mo (n8n Pro + Attio + Loops + Intercom + Riverside; PostHog and Ghost on free tiers; Anthropic API ~$10-25/mo at this volume)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect metric anomalies across case study pages and distribution channels, generate improvement hypotheses, run A/B experiments via PostHog, evaluate results, auto-implement winners, and produce weekly optimization briefs. Converges when successive experiments produce < 2% improvement.
- `case-study-recruitment-health-monitor` — play-specific monitoring for the recruitment pipeline: 7 daily health metrics (candidate pool, acceptance rate, response rate, interview completion, case study completion, time to publish, pipeline velocity), diagnostic triggers for each declining metric, automated interventions for common failure modes, and escalation rules for human handoff.
- `dashboard-builder` — build the Durable PostHog dashboard with per-case-study conversion heatmap, deal influence tracker, close rate lift trend, recruitment pipeline funnel, content freshness tracking, coverage gap map, and experiment status.
