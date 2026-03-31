---
name: micro-influencer-b2b-creators-durable
description: >
  Micro-Influencer B2B Post — Durable Intelligence. Always-on AI agents continuously optimize
  the creator program: detect metric anomalies, generate hypotheses about creator selection and
  messaging, run experiments, evaluate results, and auto-implement winners. Weekly optimization
  briefs. Converges when successive experiments produce <2% improvement.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving leads over 6 months; CPL at or below Scalable baseline; autonomous agent finds local maximum of creator program performance"
kpis: ["Monthly leads from creator channel", "CPL trend (target: flat or declining)", "Experiment win rate", "Creator program ROI", "Weeks since last significant improvement (convergence signal)"]
slug: "micro-influencer-b2b-creators"
install: "npx gtm-skills add marketing/problem-aware/micro-influencer-b2b-creators"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Micro-Influencer B2B Post — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Outcomes

Sustain or improve leads from the creator channel over 6 months through continuous, agent-driven optimization. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in creator performance, generate hypotheses about what to change (creator mix, messaging angles, formats, posting cadence, audience targeting), run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs report what changed and why. The play converges when successive experiments produce less than 2% improvement — at that point, the creator program has reached its local maximum.

## Leading Indicators

- Agent detects anomalies within 24 hours of metric deviations (confirms monitoring is working)
- At least 2 experiments per month are designed and launched (confirms the hypothesis-experiment loop is active)
- Experiment win rate above 30% (confirms hypotheses are data-driven and actionable)
- CPL stays within 10% of Scalable baseline or improves (confirms optimization is maintaining quality)
- Weekly optimization brief delivered every Monday (confirms the reporting loop is reliable)
- No manual intervention needed for standard operations for 4+ consecutive weeks (confirms true autonomy)

## Instructions

### 1. Build the Durable monitoring dashboard

Run the `dashboard-builder` drill to create a comprehensive PostHog dashboard for the creator program:

**Panel 1 — Health Monitor (agent checks daily):**
- Weekly leads from creator channel: 4-week rolling average vs. current week
- Weekly CPL: 4-week rolling average vs. current week
- Creator booking pipeline: prospects → outreach → booked → posted → completed (flow rate)
- Budget utilization: spend vs. allocation

**Panel 2 — Creator Intelligence:**
- Creator performance decay: for each Tier 1 creator, plot leads per post over time. Detect fatigue (declining returns from the same creator's audience)
- New-vs-returning creator lead ratio: are new creators contributing, or is the program over-reliant on a few?
- Format effectiveness trend: LinkedIn post CPL, newsletter CPL, YouTube CPL, Twitter CPL over time

**Panel 3 — Experiment Tracker:**
- Active experiments: what is being tested right now
- Completed experiments: hypothesis, result (win/lose/inconclusive), impact on primary KPI
- Cumulative improvement from all experiments (running total)

**Panel 4 — Convergence Signal:**
- Improvement from last 5 experiments plotted over time
- If the last 3 experiments each produced <2% improvement, display "CONVERGENCE REACHED"

### 2. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill with creator-specific configuration:

**Phase 1 — Monitor (daily via n8n cron):**
- Query PostHog for creator channel metrics: leads this week, CPL, click-through rate, conversion rate by creator
- Compare to 4-week rolling average
- Classify: normal (within 10%), plateau (within 2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Pull context from Attio: current active creators, recent posts, creator tiers, last experiment results
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data. Creator-specific hypothesis categories:
  - **Creator fatigue:** a Tier 1 creator's CPL has risen 3+ consecutive posts. Hypothesis: their audience has seen your brand too many times. Action: rotate to a new creator in the same niche.
  - **Format shift:** one format's CPL rising while another's falls. Hypothesis: audience behavior has shifted. Action: reallocate budget to the better-performing format.
  - **Messaging decay:** conversion rate dropping but click rate stable. Hypothesis: the landing page offer is stale. Action: test a new offer or headline.
  - **Audience saturation:** overall leads declining despite consistent posting volume. Hypothesis: the reachable ICP audience through current creators is exhausted. Action: expand to new creator niches or platforms.
  - **Seasonal pattern:** metric changes correlate with industry events, holidays, or budget cycles. Hypothesis: timing, not content, is the variable. Action: shift posting cadence around high-activity periods.
- Rank hypotheses by expected impact and risk
- If risk = "high" (budget changes >20%, targeting shift >50%), send Slack alert for human review and STOP
- If risk = "low" or "medium", proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment: use `posthog-experiments` to create a feature flag if applicable, or structure as parallel creator posts with different variables
- Example experiments:
  - "Test: Brief creators with 'pain-point' angle vs. 'success-story' angle for the next 4 posts"
  - "Test: Rebook Creator A (showing fatigue) vs. replace with Creator B (new, similar audience) for 2 posts each"
  - "Test: Landing page with demo CTA vs. landing page with content download CTA"
- Set experiment duration: minimum 4 creator posts per variant (2 per variant minimum)
- Log experiment start in Attio

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation`: compare CPL, conversion rate, lead quality between variants
- Decision:
  - **Adopt:** winner becomes the new default. Update creator briefs, pipeline settings, or landing pages accordingly.
  - **Iterate:** results are directional but not conclusive. Design a follow-up experiment.
  - **Revert:** variant performed worse. Restore previous approach. Log the failure.
- Store evaluation in Attio with full reasoning

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity for the week
- Calculate net metric change from adopted changes
- Generate weekly optimization brief:
  - Anomalies detected this week
  - Experiments in progress and their status
  - Experiments completed and their outcomes
  - Net CPL change from all optimizations this month
  - Convergence status: distance from local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

### 3. Run creator-specific monitoring

Run the `autonomous-optimization` drill in always-on mode:

**Creator Health Checks (weekly):**
- For each Tier 1 creator: is CPL still within 20% of their personal best? If not, flag for rotation.
- For each Tier 2 creator tested in the last month: did they earn a Tier 1 promotion? If yes, add to the recurring booking schedule.
- Creator churn tracking: if a Tier 1 creator declines to rebook or raises rates >30%, trigger prospecting for a replacement.

**Program-Level Health (monthly):**
- Total leads from creator channel vs. all other channels (share of pipeline)
- Creator program ROI: (pipeline_value_from_creators * close_rate) / total_creator_spend
- Concentration risk: if any single creator accounts for >25% of leads, flag for diversification

### 4. Guardrails (CRITICAL)

- **Rate limit:** Maximum 1 active experiment at a time. Never stack experiments on the creator channel.
- **Revert threshold:** If CPL rises >30% during any experiment, auto-revert immediately.
- **Human approval required for:**
  - Monthly creator budget changes >20%
  - Dropping a Tier 1 creator from the recurring schedule
  - Expanding to a new platform (e.g., TikTok, podcast sponsorships)
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment, wait 2 weeks before testing the same variable again.
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review.
- **Never optimize what is not measured:** If a new creator's posts do not have UTM tracking, fix tracking before including them in experiments.

### 5. Convergence and maintenance

When the last 3 consecutive experiments each produce <2% improvement:
1. The creator program has reached its local maximum
2. Reduce monitoring from daily to weekly
3. Reduce experiment frequency from 2/month to 1/month (maintenance experiments)
4. Generate a convergence report:
   - Current CPL, leads/month, ROI
   - All optimizations applied and their cumulative impact
   - Recommendations for breaking through the local maximum (new platforms, new creator categories, product changes, audience expansion) — these require strategic human decisions, not tactical agent optimization

## Time Estimate

- 20 hours: Initial Durable setup (dashboards, n8n workflows, optimization loop configuration)
- 10 hours/month: Agent-run monitoring, hypothesis generation, experiment management (largely automated)
- 5 hours/month: Human review of weekly briefs, approval of high-risk changes, strategic decisions
- 5 hours/month: Creator pipeline maintenance (new prospecting, rebooking, relationship management)
- Total over 6 months: ~20 setup + ~120 ongoing + ~30 human oversight + ~30 pipeline = 200 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Monitoring, experiments, dashboards, funnels | Free up to 1M events/mo. [Pricing](https://posthog.com/pricing) |
| n8n | Optimization loop automation, cron jobs, alerts | Cloud Pro: $60/mo. [Pricing](https://n8n.io/pricing) |
| Attio | Creator CRM, experiment log, optimization audit trail | Plus: $29/user/mo. [Pricing](https://attio.com/pricing) |
| Anthropic API | Hypothesis generation and experiment evaluation via Claude | Pay per token. ~$15/1M input tokens, ~$75/1M output tokens. Estimate: $50-150/mo for weekly optimization cycles. [Pricing](https://www.anthropic.com/pricing) |
| SparkToro | Ongoing creator discovery for pipeline refresh | Standard: $50/mo. [Pricing](https://sparktoro.com/pricing) |
| Clay | Creator enrichment for new prospects | Growth: $495/mo. [Pricing](https://www.clay.com/pricing) |
| Passionfroot | Creator booking | 2% transaction fee. [Pricing](https://www.passionfroot.me/creator-pricing) |

**Estimated Durable cost:** $5,000-10,000/mo creator fees + ~$700-900/mo tooling + ~$50-150/mo AI compute = $5,750-11,050/mo

## Drills Referenced

- `autonomous-optimization` — the core monitor → diagnose → experiment → evaluate → implement loop that finds the local maximum
- `autonomous-optimization` — always-on dashboards, weekly reports, creator health checks
- `dashboard-builder` — build the comprehensive Durable monitoring dashboard in PostHog
