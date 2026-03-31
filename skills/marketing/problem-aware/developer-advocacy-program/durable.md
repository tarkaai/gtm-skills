---
name: developer-advocacy-program-durable
description: >
  Developer Advocacy Program — Durable Intelligence. Always-on AI agents find the local maximum of
  the developer advocacy program. The autonomous-optimization drill runs the core loop: detect metric
  anomalies across content, community, and speaking → generate improvement hypotheses → run A/B
  experiments → evaluate results → auto-implement winners. Weekly optimization briefs. Converges
  when successive experiments produce <2% improvement.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Events, Communities"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained content output and ≥50 qualified leads/quarter over 12 months with autonomous optimization converging on local maximum"
kpis: ["Sustained content-to-lead conversion rate", "AI experiment win rate", "Optimization convergence rate", "Cost efficiency trend (leads per advocate hour)", "Lead quality score (lead-to-meeting rate)"]
slug: "developer-advocacy-program"
install: "npx gtm-skills add marketing/problem-aware/developer-advocacy-program"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Developer Advocacy Program — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Events, Communities

## Outcomes

The developer advocacy program runs autonomously with AI agents monitoring performance, diagnosing issues, running experiments, and implementing improvements. The `autonomous-optimization` drill creates the always-on optimization loop that finds the local maximum — the best possible performance given the current market, audience, and competitive landscape.

Success: sustained content output and ≥50 qualified developer leads per quarter over 12 months, with the optimization loop converging (successive experiments produce <2% improvement for 3 consecutive tests).

## Leading Indicators

- Autonomous optimization loop running: ≥1 experiment in flight at all times
- Weekly optimization briefs generated automatically with metric deltas and next actions
- Anomaly detection fires within 24 hours of any metric deviation >20%
- Experiment win rate ≥30% (at least 1 in 3 experiments produces measurable improvement)
- Cost per developer lead trending flat or downward month over month
- No metric drops >15% sustained for more than 2 weeks (anomaly → diagnosis → fix cycle completes fast)
- Content-to-meeting conversion rate stable within ±10% of 4-week rolling average

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the developer advocacy program:

**Phase 1 — Monitor (daily via n8n cron):**
The agent checks all devrel KPIs daily:
- Content reach: tutorial views, GitHub clones, social impressions (4-week rolling averages)
- Lead generation: developer leads captured, content-to-lead conversion rate, lead-to-meeting rate
- Community health: engagement scores, referral traffic, active threads
- Speaking pipeline: CFPs in queue, acceptance rate trend, post-talk lead yield
- Efficiency: leads per advocate hour, pipeline value per tutorial, pipeline value per talk

Classify each metric: **normal** (within ±10% of rolling average), **plateau** (±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase).

If anomaly detected → trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context from PostHog and Attio: current content strategy, recent experiments, audience composition, competitive landscape. It runs the hypothesis generator with the anomaly data.

Developer advocacy-specific diagnosis patterns:
- Content reach declining → hypothesize: topic fatigue, algorithm change, posting time shift, competitor content spike
- GitHub clones dropping → hypothesize: README quality decay, outdated code samples, competitor repo gaining visibility
- Community engagement declining → hypothesize: community norms shifted, over-posting, topic mismatch
- CFP acceptance rate dropping → hypothesize: proposal quality, talk topic saturation, wrong conference tier
- Lead conversion declining → hypothesize: CTA mismatch, tutorial-to-product bridge weak, wrong audience segment

Receive 3 ranked hypotheses with expected impact and risk. If risk = "high" (e.g., changing target audience segment), send Slack alert for human review. If risk = "low" or "medium," proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
The agent designs and launches an experiment:

- **Content experiments:** Use PostHog feature flags to serve different tutorial formats, CTA placements, or hook styles to different visitor cohorts. Measure: views, read time, scroll depth, CTA clicks, leads captured.
- **Distribution experiments:** A/B test posting schedules, platform priority, and social derivative formats. Measure: engagement rate, referral traffic, lead attribution.
- **Community experiments:** Test different response templates, contribution formats, and community focus strategies. Measure: engagement, referral visits, leads.
- **Speaking experiments:** Test different proposal styles, talk abstracts, and post-talk follow-up sequences. Measure: acceptance rate, post-talk leads.

Minimum experiment duration: 7 days or 100+ samples per variant. Maximum 1 active experiment per channel at a time. Log experiment start in Attio.

**Phase 4 — Evaluate (triggered by experiment completion):**
The agent pulls results from PostHog and runs the evaluation:

- **Adopt:** Variant outperforms control with statistical significance → update the live configuration. Log the change and its impact.
- **Iterate:** Inconclusive results → generate a refined hypothesis. Return to Phase 2.
- **Revert:** Variant underperforms → disable, restore control. Log the failure. Cool down 7 days before testing the same variable.
- **Extend:** Nearly significant → run for another period.

Store the full evaluation (decision, confidence, reasoning) in Attio.

**Phase 5 — Report (weekly via n8n cron):**
Generate a weekly optimization brief:
- Anomalies detected this week and actions taken
- Experiments running: current status and preliminary results
- Experiments completed: decisions and net metric impact
- Overall program trajectory: trending toward or away from targets
- Recommended focus for next week
- Distance from estimated local maximum (based on diminishing returns curve)

Post to Slack and store in Attio.

### 2. Build the devrel performance monitoring system

Run the `autonomous-optimization` drill to create the always-on monitoring layer:

1. **Real-time dashboard** in PostHog with 6 panels: content production, content reach, community health, speaking program, full-funnel attribution, and efficiency metrics
2. **Anomaly detection** running daily for content, community, lead, and speaking signals — each anomaly trigger feeds into the autonomous optimization loop
3. **Cross-channel attribution** tracking the complete journey: tutorial published → engaged → website visit → lead captured → meeting booked → deal created — broken down by source (content, community, speaking)
4. **Automated weekly and monthly reports** with narrative analysis generated by Claude
5. **Alert routing** for opportunities (viral post, trending repo) and issues (lead drought, community stall)

### 3. Build executive-level program dashboards

Run the `dashboard-builder` drill to create a high-level view:

1. **Program health dashboard:** Total developer leads this quarter, pipeline value attributed to devrel, cost per developer lead, advocate time efficiency, content production vs target
2. **Channel comparison:** Content vs community vs speaking — which channel produces the most leads, the highest-quality leads (measured by lead-to-meeting rate), and the best ROI (leads per hour invested)?
3. **Trend dashboards:** 12-month rolling views of all primary KPIs. Overlay experiment markers to show which optimizations drove which improvements.
4. **Convergence tracker:** Plot the magnitude of improvement from each successive experiment. When the trend line approaches zero, the program has found its local maximum.

### 4. Manage program maturity

As the optimization loop converges:

**Active optimization phase (months 1-6):**
- Run experiments aggressively: 3-4 per month across content, distribution, community, and speaking
- Expect win rate of 30-40%
- Major metric improvements from early experiments

**Diminishing returns phase (months 6-9):**
- Experiment improvements shrink from 10-20% to 2-5%
- Focus experiments on efficiency (same output, less effort) rather than volume
- Begin testing new frontiers: new communities, new content formats (workshops, interactive playgrounds), new speaking venues (podcasts, webinars vs conferences)

**Convergence phase (months 9-12):**
- Successive experiments produce <2% improvement for 3 consecutive tests
- The program has reached its local maximum
- Reduce optimization frequency from weekly to monthly
- Report to team: "Developer advocacy is optimized at [current metrics]. Further gains require strategic changes: new developer segments, new product capabilities, or new market positioning."

### 5. Sustain and defend the local maximum

Once converged, the agent shifts from optimization to maintenance:

- **Daily monitoring** continues — detect external changes (algorithm shifts, competitor moves, community changes) that could degrade performance
- **Monthly experiments** to verify the maximum still holds — conditions change over 3-6 month cycles
- **Quarterly strategic review** with human: should the program expand to new segments, new platforms, or new content formats? Strategic pivots restart the optimization cycle.

## Time Estimate

- Autonomous optimization setup (n8n workflows, PostHog experiments, Attio logging): 12 hours
- Devrel performance monitoring setup: 8 hours
- Dashboard building: 4 hours
- Ongoing: agent runs autonomously (~2 hours compute/week), human reviews weekly brief (15 min/week), monthly strategic review (2 hours/month)
- Total: ~180 hours over 12 months (24 hours setup, then monitoring + periodic review)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, experiments, anomaly detection | Growth: ~$50-150/mo at scale |
| n8n | Automation (optimization loop, monitoring, reports) | Self-hosted free / Cloud: $20/mo |
| Claude API (Anthropic) | Hypothesis generation, experiment evaluation, report writing | ~$30-80/mo |
| Attio | CRM + experiment log + campaign records | Plus: $29/seat/mo |
| Ghost / blog | Tutorial publishing | Ghost Pro: $9/mo |
| GitHub | Sample repos | Free |
| Clay | Enrichment + CFP discovery | Starter: $149/mo |
| Buffer or Typefully | Social scheduling | $6-12/mo |
| Taplio | LinkedIn analytics | $49/mo |

**Total play-specific cost:** ~$100-500/mo + agent compute costs (variable based on monitoring frequency)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor → diagnose → experiment → evaluate → implement. Finds the local maximum of program performance through continuous experimentation.
- `autonomous-optimization` — real-time dashboards, anomaly detection, cross-channel attribution, and automated reporting specific to developer advocacy programs
- `dashboard-builder` — executive-level program dashboards showing health, channel comparison, trends, and convergence tracking
