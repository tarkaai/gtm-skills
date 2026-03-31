---
name: competitive-situation-analysis-durable
description: >
  Competitive Situation Assessment — Durable Intelligence. Always-on AI agents running the
  autonomous optimization loop on competitive intelligence: detecting win rate anomalies,
  generating positioning hypotheses, running A/B experiments on competitive frameworks,
  and auto-implementing winners. Converges at the local maximum of competitive win rates.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "135 hours over 6 months"
outcome: "Sustained or improving win rates against all tracked competitors over 6 months via autonomous competitive optimization"
kpis: ["Win rate by competitor (sustained or improving)", "Autonomous experiment win rate", "Competitive intelligence freshness (<7 days)", "Positioning framework convergence rate", "Optimization cycle throughput (experiments/month)"]
slug: "competitive-situation-analysis"
install: "npx gtm-skills add sales/qualified/competitive-situation-analysis"
drills:
  - autonomous-optimization
---

# Competitive Situation Assessment — Durable Intelligence

> **Stage:** Sales → Qualified | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

An always-on AI agent continuously optimizes competitive win rates. The agent monitors win rate trends per competitor, detects when positioning effectiveness degrades, generates hypotheses for what to change (new frameworks, different trap questions, updated battlecard emphasis), runs controlled experiments, evaluates results, and auto-implements winners. Weekly optimization briefs summarize what changed and why. The system converges when successive experiments produce <2% improvement — at that point, the play has reached its local maximum against each competitor.

## Leading Indicators

- Optimization loop executing on schedule (daily monitor, weekly experiments)
- Hypotheses grounded in data (referencing specific competitor win rate changes or deal pattern shifts)
- Experiments completing with sufficient sample size before decisions are made
- Win rate against each competitor either stable or improving month-over-month
- Convergence signals appearing for mature competitors (diminishing returns from experiments)
- Competitor change detection feeding new hypotheses (external changes drive internal adaptation)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for competitive situation analysis. The loop operates in 5 phases:

**Phase 1 — Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` to check competitive KPIs:
   - Win rate by competitor (rolling 4-week window)
   - Competitive discovery rate
   - Battlecard delivery rate and latency
   - Positioning framework effectiveness (win rate per framework per competitor)
2. Compare last 2 weeks against 4-week rolling average
3. Classify: **normal** (within ±10%), **plateau** (±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
4. If anomaly detected → trigger Phase 2
5. If normal → log to Attio, no action needed

**Phase 2 — Diagnose (triggered by anomaly):**
1. Gather context from Attio: current positioning frameworks per competitor, recent battlecard versions, latest competitor changes detected, deal patterns in affected segment
2. Pull 8-week competitive metric history from PostHog
3. Run `hypothesis-generation` with the anomaly data + competitive context
4. Receive 3 ranked hypotheses. Examples of competitive hypotheses the agent might generate:
   - "Win rate against Competitor X dropped 15% because their recent pricing change (detected by competitor monitoring) undercuts our TCO argument. Hypothesis: switch from `tco_comparison` to `pain_alignment` framework."
   - "Plateau against Competitor Y: current trap questions no longer surface gaps because they shipped Feature Z last month. Hypothesis: update trap questions to target their integration limitations instead."
   - "Discovery rate dropped: new reps are not asking competitive questions. Hypothesis: add automated competitive discovery question prompts to pre-call prep."
5. Store hypotheses in Attio as notes on the Competitive Intelligence campaign record
6. If risk = "high" → send Slack alert for human review and STOP
7. If risk = "low" or "medium" → proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Take the top-ranked hypothesis
2. Design the experiment using `posthog-experiments`: create a feature flag that splits competitive deals between control (current positioning/framework) and variant (hypothesis change)
3. Implement the variant:
   - If the hypothesis is about positioning framework → update the `competitive-positioning-generation` call to use the new framework for variant deals
   - If the hypothesis is about trap questions → update the battlecard's trap question set for variant deals
   - If the hypothesis is about battlecard emphasis → modify which sections are highlighted in delivery for variant deals
   - If the hypothesis is about discovery process → update pre-call prep content for variant deals
4. Set experiment duration: minimum 14 days or 50+ competitive deals per variant, whichever is longer
5. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria, competitor affected

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog: win rate control vs variant, sample size, confidence interval
2. Run `experiment-evaluation` with the data
3. Decision:
   - **Adopt:** Win rate improved ≥5% with ≥90% confidence. Update the default positioning framework / trap questions / battlecard for this competitor. Log the change. Move to Phase 5.
   - **Iterate:** Results directionally positive but not significant. Generate a refined hypothesis building on this result. Return to Phase 2.
   - **Revert:** Variant performed worse or no different. Restore control. Log the failure reason. Return to Phase 1 monitoring.
   - **Extend:** Sample size insufficient after minimum duration. Keep running for another period.
4. Store full evaluation in Attio: decision, confidence, reasoning, competitor impact

**Phase 5 — Report (weekly via n8n cron):**
1. Aggregate all optimization activity for the week: anomalies detected, hypotheses generated, experiments running, decisions made
2. Calculate: net win rate change from all adopted changes this week, per competitor
3. Generate a weekly competitive optimization brief:
   - What changed and why (per competitor)
   - Net impact on win rates
   - Active experiments and their interim results
   - Competitor changes detected this week and their implications
   - Current distance from estimated local maximum per competitor
   - Recommended focus for next week
4. Post the brief to Slack and store in Attio

### 2. Keep competitive intelligence fresh

Continue running the the competitive intelligence automation workflow (see instructions below) drill (from Scalable) with these Durable-level enhancements:

- **Increase competitor monitoring frequency** from weekly to twice-weekly for top 3 competitors
- **Feed competitor changes into the optimization loop:** When a competitor ships a product change with `competitive_impact` ≥ 3, automatically trigger Phase 2 (Diagnose) for that competitor's positioning strategy
- **Auto-refresh battlecards** when new deal data accumulates: if 5+ new deals mention a competitor since last battlecard refresh, trigger `competitive-battlecard-assembly` to rebuild
- **Track battlecard version effectiveness:** does the newest battlecard version produce higher win rates than the previous version? If not, the refresh may have degraded quality — revert and investigate.

### 3. Generate monthly deep-dive competitive reports

Continue running the `autonomous-optimization` drill (from Scalable) with Durable-level additions:

- **Include optimization experiment results:** which experiments were run, which were adopted, and their measured impact
- **Convergence tracking per competitor:** for each competitor, are experiments still producing meaningful improvement or has the play reached its local maximum?
- **Predictive competitive analytics:** use Claude to analyze deal patterns and predict which open deals are at highest risk of competitive loss. Prioritize those for human strategy intervention.
- **Quarterly strategic review:** every 3 months, generate a comprehensive report that looks beyond tactical positioning to strategic competitive questions: Is the competitive landscape shifting? Are new entrants emerging? Should we invest in new capabilities to address persistent competitive gaps?

### 4. Apply guardrails

The `autonomous-optimization` drill enforces these guardrails. Verify they are active:

- **Rate limit:** Maximum 1 active experiment per competitor at a time. Never stack experiments on the same competitor.
- **Revert threshold:** If win rate against any competitor drops >30% during an experiment, auto-revert immediately.
- **Human approval required for:**
  - Positioning changes that affect the core brand narrative (not just framework selection)
  - Battlecard changes that alter how we describe our own capabilities
  - Any experiment the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment, wait 14 days before testing a new hypothesis on the same competitor.
- **Maximum experiments per month:** 4 across all competitors. If all 4 fail in a month, pause optimization and flag for human strategic review.
- **Never optimize without measurement:** If a competitive KPI lacks PostHog tracking, fix tracking first.

### 5. Detect convergence and maintain

The optimization loop runs indefinitely. However, it detects **convergence** per competitor — when successive experiments produce diminishing returns (<2% improvement for 3 consecutive experiments against the same competitor):

1. Declare that competitor matchup "optimized at local maximum"
2. Reduce monitoring frequency for that competitor from daily to weekly
3. Reduce experiment frequency — only re-engage when competitor monitoring detects a significant change (impact ≥ 3) or when win rate drops >10% from the established maximum
4. Report: "Win rate against {Competitor} has converged at {rate}%. Further improvement requires strategic changes (new capabilities, new proof points, pricing changes) rather than tactical positioning optimization."
5. Shift optimization resources to competitors where experiments are still producing gains

## Time Estimate

- 20 hours: Configure autonomous optimization loop (Phases 1-5) and connect to competitive data sources
- 10 hours: Enhance competitive intelligence automation for Durable-level frequency and feedback loops
- 10 hours: Configure guardrails, convergence detection, and human escalation paths
- 80 hours: Ongoing monitoring, experiment management, and iteration over 6 months (~3.5 hours/week)
- 15 hours: Monthly deep-dive reports and quarterly strategic reviews (6 monthly + 2 quarterly)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Fireflies | Call transcription (always-on) | Pro $10/user/mo annual — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Anthropic Claude API | Extraction + positioning + hypothesis generation + evaluation | ~$100-200/mo at Durable scale — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| Attio | CRM: deals + Competitors + campaign records + automation | Included in standard stack — [attio.com/pricing](https://attio.com/pricing) |
| PostHog | Events + experiments + anomaly detection + dashboards | Growth plan ~$0.00045/event — [posthog.com/pricing](https://posthog.com/pricing) |
| Clay | Competitor enrichment + changelog monitoring (2x/week) | Growth $495/mo — [clay.com/pricing](https://www.clay.com/pricing) |
| n8n | Orchestration: optimization loop + all automations | Self-hosted free or Cloud from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Gong (optional) | Deal intelligence for richer competitive extraction | ~$100-250/user/mo (annual contract) — [gong.io/pricing](https://www.gong.io/pricing) |

**Estimated play-specific cost:** ~$300-700/mo without Gong, ~$500-1000/mo with Gong (Clay Growth + Claude API at scale are the main drivers)

## Drills Referenced

- `autonomous-optimization` — the core monitor → diagnose → experiment → evaluate → implement loop that finds the local maximum of competitive win rates
- the competitive intelligence automation workflow (see instructions below) — competitor change monitoring, battlecard delivery, and web behavior triggers (enhanced for Durable frequency)
- `autonomous-optimization` — monthly deep-dive competitive reports with optimization experiment results and convergence tracking
