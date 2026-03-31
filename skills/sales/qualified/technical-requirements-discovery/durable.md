---
name: technical-requirements-discovery-durable
description: >
  Technical Requirements Discovery — Durable Intelligence. Always-on AI agents monitor technical
  requirement patterns, auto-refine scoring models, detect market demand shifts, and run experiments
  on discovery approaches. The autonomous-optimization loop finds and maintains the local maximum
  of technical fit prediction accuracy and blocker early-detection rate.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "60 hours setup + ongoing over 6 months"
outcome: "Technical fit prediction accuracy sustained at >=85% with blocker early-detection rate >=90% over 6 months via autonomous optimization"
kpis: ["Technical fit prediction accuracy", "Blocker early-detection rate", "Technical win rate", "Time-to-technical-qualification", "Scoring model drift", "Experiment win rate"]
slug: "technical-requirements-discovery"
install: "npx gtm-skills add sales/qualified/technical-requirements-discovery"
drills:
  - autonomous-optimization
  - technical-intelligence-monitor
  - technical-fit-scoring
---

# Technical Requirements Discovery — Durable Intelligence

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

The technical discovery system runs itself. AI agents monitor performance metrics, detect when prediction accuracy drifts, generate hypotheses for improvement, run experiments, and auto-implement winners. The system continuously improves technical fit prediction accuracy and blocker early-detection rate toward their local maximum. Weekly intelligence briefs surface technical demand shifts before they impact deal outcomes. The founder's involvement is limited to reviewing weekly briefs and approving high-risk experiments.

## Leading Indicators

- The `autonomous-optimization` loop is running: anomalies detected, hypotheses generated, experiments running
- Technical fit prediction accuracy is stable or improving month-over-month (not drifting)
- The weekly technical intelligence brief surfaces actionable insights (not just reporting numbers)
- New technical demand patterns (new certifications, new integrations) are detected within 2 weeks of appearing in the pipeline
- Scoring model weights auto-adjust based on closed deal data without manual intervention
- Experiment velocity: at least 2 experiments per month are completing and producing learnings

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the technical-requirements-discovery play. The optimization loop monitors these primary KPIs:

- **Technical fit prediction accuracy:** Compare the composite score at time of scoring vs. deal outcome (won/lost + implementation success). Target: >=85% accurate.
- **Blocker early-detection rate:** Percentage of deals where all technical blockers were identified before the proposal stage. Target: >=90%.
- **Time-to-technical-qualification:** Hours from deal entering "Qualified" to technical scores applied. Target: <=24 hours.

Configure the optimization loop phases:

**Phase 1 — Monitor (daily via n8n cron):**
- Query PostHog for `tech_fit_score_accuracy_check` events from the last 14 days
- Compare prediction accuracy against 4-week rolling average
- Query `tech_blocker_identified` and `tech_blocker_resolved` events to calculate early-detection rate
- Classify: normal (within +-10%), plateau (+-2% for 3+ weeks), drop (>15% decline)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Pull 8 weeks of technical scoring data from PostHog
- Pull current scoring model weights and rubric from Attio configuration
- Pull recent deal outcomes and their technical profiles
- Send to Claude with `hypothesis-generation`:

Example hypotheses the system might generate:
- "Security score weight should increase from 25% to 35% — 4 of the last 6 lost deals had security as the weakest category but composite score didn't reflect this"
- "Integration complexity scoring is too generous — deals scored 'moderate complexity' are taking 3x longer to implement than predicted"
- "Pre-call research is missing on-premise deployment requirements for healthcare prospects — add an industry-specific question to the Claygent prompt"
- "Technical discovery calls with engineering stakeholders produce 20% higher accuracy than calls with IT managers — adjust scheduling to prioritize engineering contacts"

Rank hypotheses by expected impact and risk. Store in Attio. If risk = "high", alert the founder for approval.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment using PostHog feature flags
- For scoring model changes: split new deals into control (current weights) and variant (proposed weights). Score both ways and compare accuracy after 2 weeks.
- For discovery process changes: A/B test different Claygent prompts, question guides, or scoring rubrics on alternating deals.
- For routing changes: test different SE involvement thresholds and measure resolution speed.
- Set experiment duration: minimum 14 days or 20+ deals scored, whichever is longer
- Log experiment start in Attio

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` to determine: Adopt, Iterate, Revert, or Extend
- If Adopt: update the live scoring model, Claygent prompts, or routing rules. Log the change.
- If Revert: restore previous configuration. Log the failure and reason.
- Store full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron, every Monday 8am):**
- Aggregate all optimization activity for the week
- Calculate net metric change from adopted experiments
- Generate weekly optimization brief:
  - Prediction accuracy trend and current level
  - Blocker detection rate
  - Experiments running, completed, and results
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

### 2. Deploy the technical intelligence monitor

Run the `technical-intelligence-monitor` drill to create the always-on monitoring layer:

- PostHog dashboard tracking technical demand patterns across all deals
- Anomaly alerts for: new certification demand spikes, integration demand shifts, rising technical disqualification rate, composite score decline
- Weekly intelligence briefs analyzing what the technical landscape is telling you
- Quarterly trend analysis feeding product roadmap decisions

The technical intelligence monitor answers strategic questions:
- "What certifications are becoming table stakes in our market?"
- "Which integrations do we keep losing deals over?"
- "Is our market moving upmarket (more complex technical requirements) or downmarket?"
- "What are competitors doing technically that we're not?"

### 3. Build adaptive scoring model

Using the `technical-fit-scoring` drill in continuous refinement mode:

- Every time a deal closes (won or lost), the agent compares the technical score at time of scoring against the actual outcome
- If accuracy drifts below 85% for 2 consecutive weeks, the autonomous optimization loop auto-triggers a scoring model experiment
- The agent can adjust: category weights, score thresholds for each verdict, blocker severity classifications, and routing rules
- The agent cannot change: what counts as a blocker (this is a product capability fact), or routing destinations (these are organizational decisions)

Track scoring model versions in Attio:
```json
{
  "event": "scoring_model_updated",
  "properties": {
    "version": "v3.2",
    "change": "Increased security weight from 25% to 30%, decreased infrastructure from 15% to 10%",
    "reason": "Experiment #12 showed 8% accuracy improvement",
    "previous_accuracy": 0.82,
    "projected_accuracy": 0.88
  }
}
```

### 4. Set guardrails

**Rate limits:**
- Maximum 1 active experiment at a time on the scoring model
- Maximum 2 active experiments total across all discovery process variables
- Maximum 4 experiments per month

**Revert thresholds:**
- If prediction accuracy drops >15% during any experiment, auto-revert immediately
- If blocker early-detection rate drops below 80%, pause all experiments and alert the founder

**Human approval required for:**
- Scoring model weight changes >10 percentage points on any single category
- Routing rule changes that would affect >30% of deals
- Any change flagged "high risk" by the hypothesis generator
- Changes to what constitutes a technical blocker (product capability questions)

**Convergence detection:**
When 3 consecutive experiments produce <2% improvement, the system has found its local maximum. At convergence:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment cadence from monthly to quarterly
3. Report: "Technical discovery is optimized. Current accuracy: {X}%. Further gains require product changes (new integrations, new certifications) rather than process optimization."

### 5. Evaluate sustainability

Measure over 6 months:
- Technical fit prediction accuracy: sustained >=85%
- Blocker early-detection rate: sustained >=90%
- Technical win rate: improving or stable
- Time-to-technical-qualification: stable or improving
- Scoring model drift: <5% variance month-over-month without intervention

If all metrics sustain, this play is durable. If metrics decay, the autonomous optimization loop should be catching and correcting. If the loop itself is failing to correct, investigate: has the market shifted fundamentally (new compliance requirement you can't meet), or has the product changed (new capabilities not reflected in scoring)?

## Time Estimate

- Autonomous optimization loop setup: 16-20 hours
- Technical intelligence monitor setup: 8-10 hours
- Adaptive scoring model configuration: 8-10 hours
- Guardrail and convergence logic: 4-6 hours
- Weekly review of optimization briefs: 30 min/week ongoing
- Monthly strategic review: 2 hours/month ongoing

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with technical scoring, routing, experiment tracking | Pro $59/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Fireflies | Call recording with transcript webhook | Pro $10/user/mo annual — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Cal.com | Discovery call scheduling | Free (1 user) — [cal.com/pricing](https://cal.com/pricing) |
| Clay | Tech stack enrichment via Claygent and API | Growth $495/mo — [clay.com/pricing](https://clay.com/pricing) |
| PostHog | Event tracking, dashboards, experiments, feature flags | Free (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Workflow automation for optimization loops | Pro EUR 60/mo (10K executions) — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | Transcript analysis, hypothesis generation, experiment evaluation | Sonnet 4.6: $3/$15 per 1M tokens — [claude.com/pricing](https://claude.com/pricing) |
| Gong (optional) | Call analytics with built-in topic detection | ~$1,600/user/year — [gong.io/pricing](https://gong.io/pricing) |

**Estimated play-specific cost:** $550-750/mo (Attio Pro $59, Fireflies $10, Clay Growth $495, n8n ~$60, Anthropic API ~$40-80 for daily monitoring + experiments. Gong is optional but adds significant cost.)

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: monitor metrics, generate hypotheses, run experiments, evaluate results, auto-implement winners. This is what makes Durable fundamentally different.
- `technical-intelligence-monitor` — always-on monitoring of technical requirement patterns, demand shifts, and strategic intelligence
- `technical-fit-scoring` — continuous refinement of the scoring model based on closed deal accuracy data
