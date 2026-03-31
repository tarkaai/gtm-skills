---
name: stakeholder-mapping-durable
description: >
  Stakeholder Mapping Framework — Durable Intelligence. Always-on AI agents continuously monitor
  stakeholder dynamics, detect org changes, optimize role-specific engagement, and autonomously
  experiment to find the local maximum of multi-threading impact on deal velocity.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Social, Email"
level: "Durable Intelligence"
time: "100 hours over 6 months"
outcome: "Sustained >=30% faster close time for multi-threaded deals over 6 months, with autonomous optimization maintaining or improving deal health scores as market conditions change"
kpis: ["Multi-threading rate", "Deal velocity delta (sustained)", "Stakeholder prediction accuracy", "Autonomous experiment win rate", "Org change detection speed"]
slug: "stakeholder-mapping"
install: "npx gtm-skills add sales/connected/stakeholder-mapping"
drills:
  - autonomous-optimization
  - stakeholder-intelligence-monitor
---

# Stakeholder Mapping Framework — Durable Intelligence

> **Stage:** Sales > Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Social, Email

## Outcomes

Deploy always-on AI agents that continuously monitor stakeholder dynamics across all deals, detect org changes before they impact deal velocity, and autonomously experiment on role-specific engagement strategies. The system finds and maintains the local maximum of multi-threading impact — sustaining or improving the 30%+ velocity advantage indefinitely.

## Leading Indicators

- Org change detection identifies champion departures and new hires within 48 hours
- Sentiment tracking predicts deal stalls 3+ weeks in advance (validated against actual outcomes)
- Autonomous experiments produce 2+ winning engagement strategies per quarter
- Weekly intelligence briefs drive specific actions on 80%+ of flagged deals
- Convergence detection fires when successive experiments produce <2% improvement (local maximum reached)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the stakeholder mapping play. This creates the always-on monitor > diagnose > experiment > evaluate > implement cycle:

**Monitor (daily via n8n cron):**
- Check primary KPIs: multi-threading rate, deal health score distribution, deal velocity delta, role-specific engagement rates
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger the diagnosis phase

**Diagnose (triggered by anomaly):**
- Gather context: current role-specific outreach templates, cadence timing, engagement scoring weights, org chart refresh frequency
- Pull 8-week metric history from PostHog
- Generate 3 ranked hypotheses with Claude. Examples:
  - "Economic Buyer engagement rate dropped because the ROI email template is stale — competitors updated their messaging"
  - "Multi-threading rate declined because new deal volume increased but enrichment credit budget did not scale"
  - "Champion cooling rate increased because follow-up cadence is too long — reduce from 7 days to 3 days"
- If top hypothesis is high-risk (affects >50% of deals), pause and flag for human review

**Experiment (triggered by hypothesis acceptance):**
- Design the experiment using PostHog feature flags
- Example: if hypothesis is "shorten Champion follow-up cadence from 7 to 3 days," split deals 50/50 between control (7-day) and variant (3-day)
- Minimum 14 days or 20 deals per variant, whichever takes longer
- Log experiment start in Attio

**Evaluate (triggered by experiment completion):**
- Pull results from PostHog
- Adopt the winner if statistically significant AND practically meaningful (>5% improvement)
- If winner adopted: update live configuration, log the change, move to reporting
- If inconclusive: extend experiment or generate a new hypothesis
- If loser won: revert, log the learning, return to monitoring

**Report (weekly via n8n cron):**
- Generate optimization brief: what anomalies detected, what hypotheses tested, what experiments ran, net impact on KPIs
- Calculate distance from estimated local maximum
- Post to Slack and store in Attio

### 2. Deploy stakeholder intelligence monitoring

Run the `stakeholder-intelligence-monitor` drill to set up:

**Org change detection (weekly):**
- Refresh all active account org charts via Clay
- Compare against stored Attio data
- Detect: new hires, departures, title changes, department restructures
- Classify impact: CRITICAL (Champion departed), HIGH (new Economic Buyer), MEDIUM (Influencer promoted), LOW (new IC hire)
- Alert deal owners immediately for CRITICAL and HIGH changes

**Sentiment tracking (continuous):**
- After each meeting: extract per-stakeholder sentiment from Fireflies transcripts
- After each email: classify reply tone (enthusiastic, professional, cold, combative)
- Maintain a `sentiment_trend` field per stakeholder: Improving, Stable, Declining
- Alert when a Champion or Economic Buyer's sentiment shifts to Declining

**Engagement decay detection (daily):**
- Monitor individual engagement scores for sudden drops
- Detect deal-level health score declines >20 points in a week
- Flag when all Influencers on a deal go Cold simultaneously (indicates internal priority shift)

**Weekly intelligence brief:**
Generate and distribute:
```
## Stakeholder Intelligence Brief — Week of {date}

### Critical Alerts
- {Company}: Champion {Name} left the company. Deal at risk.
- {Company}: Economic Buyer {Name} unresponsive for 21 days. Sentiment: Declining.

### Org Changes
- {Company}: New VP Engineering {Name} — classified as Influencer. Recommended: LinkedIn connection + technical content.
- {Company}: {Name} promoted to SVP. Was Influencer, may now be closer to Economic Buyer.

### Deal Health
- Deals improving: {list with delta}
- Deals declining: {list with delta and probable cause}
- At single-threaded risk: {list}

### Optimization Activity
- Experiments running: {list}
- Experiments completed: {results}
- Net KPI impact this week: {summary}
```

### 3. Configure guardrails

**Critical guardrails for the autonomous loop:**
- Maximum 1 active experiment at a time for this play
- Auto-revert if multi-threading rate drops >15% during any experiment
- Human approval required for: changes to Economic Buyer outreach templates, changes affecting >50% of deals, any hypothesis flagged as high-risk
- Cooldown: 7 days after a failed experiment before testing the same variable
- Maximum 4 experiments per month; if all 4 fail, pause and flag for strategic review
- Never optimize engagement scoring weights without 4+ weeks of baseline data

### 4. Build the feedback loop

Connect intelligence monitoring outputs to the optimization loop:
- Org change frequency → informs how often Clay enrichment should refresh (if many changes, increase from weekly to twice-weekly)
- Sentiment trajectories → inform whether messaging experiments are working
- Engagement decay patterns → generate hypotheses about cadence or content changes
- Deal velocity data → primary success metric for all experiments

### 5. Monitor for convergence

The optimization loop runs indefinitely. It should detect convergence — when successive experiments produce diminishing returns:
- Track the net improvement from each adopted experiment
- If 3 consecutive experiments produce <2% improvement → convergence reached
- At convergence:
  1. The play has reached its local maximum for the current market conditions
  2. Reduce monitoring from daily to weekly
  3. Reduce experiments from monthly to quarterly
  4. Report: "Stakeholder mapping is optimized. Current performance: {metrics}. Further gains require strategic changes (new channels, larger deal sizes, different ICP segments) rather than tactical optimization."
- Continue intelligence monitoring even at convergence — org changes and market shifts can disrupt the local maximum

### 6. Evaluate sustainability

This level runs continuously. Monthly check:
- Multi-threaded deals still closing >=30% faster than single-threaded
- Deal health scoring still predictive (alerts preceding stalls by 2+ weeks)
- Autonomous experiments producing at least 1 winning change per quarter
- Intelligence briefs driving action on 80%+ of flagged items

If metrics degrade, the autonomous loop should self-diagnose. If it cannot recover within 2 months, escalate for strategic review: has the market shifted, has the ICP changed, or has the competitive landscape altered the buying process?

## Time Estimate

- Autonomous optimization loop setup: 15 hours
- Stakeholder intelligence monitor setup: 12 hours
- Guardrail and convergence detection configuration: 8 hours
- Monthly review and strategic adjustment (6 months x 5 hours): 30 hours
- Experiment design and evaluation (ongoing): 20 hours
- Intelligence brief review and action (ongoing): 15 hours

**Total: ~100 hours over 6 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM for stakeholder data, scoring, and deal tracking | Pro at $59/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Clay | Weekly org chart refresh across all accounts | Growth at $495/mo (40,000 actions) ([clay.com/pricing](https://clay.com/pricing)) |
| n8n | Orchestration: optimization loop, intelligence monitor, alerts, reports | Pro at $60/mo or self-hosted free ([n8n.io/pricing](https://n8n.io/pricing)) |
| PostHog | Engagement tracking, experiments, anomaly detection, dashboards | ~$100-200/mo at scale ([posthog.com/pricing](https://posthog.com/pricing)) |
| Anthropic | Claude for hypothesis generation, classification, briefs | ~$30-60/mo at Durable volume ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Instantly | Email sequences for role-specific outreach experiments | Growth at $30/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| LinkedIn Sales Navigator | Org chart research and relationship mapping | Core at $99.99/mo ([business.linkedin.com/sales-solutions](https://business.linkedin.com/sales-solutions/compare-plans)) |
| Fireflies | Meeting transcription for sentiment extraction | Pro at $18/user/mo ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |

**Estimated monthly cost for this level: $890-1,120** (Attio Pro $59 + Clay Growth $495 + n8n Pro $60 + PostHog $100-200 + Claude API $30-60 + Instantly $30 + LinkedIn SN $100 + Fireflies $18)

## Drills Referenced

- `autonomous-optimization` — The always-on monitor > diagnose > experiment > evaluate > implement loop that finds the local maximum of stakeholder mapping performance
- `stakeholder-intelligence-monitor` — Continuous monitoring of org changes, sentiment shifts, engagement decay, and stakeholder dynamics with weekly intelligence briefs
