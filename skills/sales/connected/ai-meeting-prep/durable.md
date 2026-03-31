---
name: ai-meeting-prep-durable
description: >
  AI-Powered Meeting Preparation — Durable Intelligence. Always-on AI agents continuously optimize
  brief generation quality, data source weighting, prompt variants, and section ordering. The
  autonomous-optimization loop detects brief quality anomalies, generates improvement hypotheses,
  runs A/B experiments on prompts and data sources, and auto-implements winners. Weekly optimization
  briefs track convergence toward peak brief effectiveness.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving call outcomes (>=30% lift vs non-prepped) over 6 months via continuous agent-driven brief optimization, insight prioritization, and market adaptation"
kpis: ["Call outcome trend", "Agent experiment win rate", "Brief personalization impact", "Predictive accuracy"]
slug: "ai-meeting-prep"
install: "npx gtm-skills add sales/connected/ai-meeting-prep"
drills:
  - autonomous-optimization
---

# AI-Powered Meeting Preparation — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

Always-on AI agents finding the local maximum. The brief generation system runs itself: account research, intelligence assembly, brief generation, post-call feedback, and quality monitoring all execute autonomously. The `autonomous-optimization` drill runs the core loop: detect anomalies in brief quality or call outcomes, generate hypotheses about what to change (prompt structure, data source weighting, section ordering, question style), run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs track convergence. The system converges when successive experiments produce <2% improvement in brief usefulness or call outcome lift — at that point, meeting preparation has reached its optimal performance given current data sources and LLM capabilities.

**Pass threshold:** Sustained or improving call outcomes (>=30% lift vs non-prepped) over 6 months via continuous agent-driven brief optimization, insight prioritization, and market adaptation.

## Leading Indicators

- Autonomous optimization loop runs daily without manual intervention
- Weekly optimization briefs are generated and posted to Slack
- At least 2 experiments per month are initiated, evaluated, and decided
- Brief usefulness scores trend upward or hold steady over successive months
- Predictive accuracy improves: brief's predicted objections match actual objections at higher rates
- Convergence signal: last 3 experiments produced <2% improvement each

## Instructions

### 1. Deploy Autonomous Optimization

Run the `autonomous-optimization` drill configured for the meeting prep play. This is the drill that makes Durable fundamentally different from Scalable.

**Configure the optimization loop:**

**Phase 1 — Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check meeting prep KPIs:
  - Brief adoption rate (briefs generated / meetings held)
  - Average brief usefulness score (from feedback loop)
  - Average brief accuracy score (from feedback loop)
  - Call outcome lift (prepped vs non-prepped next-step conversion)
  - Data completeness score (intelligence profile richness)
  - Brief generation failure rate
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +-10%), plateau (+-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context: current prompt templates, data source configuration, section ordering, meeting type routing
- Pull 8-week metric history from PostHog via the brief quality monitor
- Pull aggregate feedback data: which sections score highest/lowest, which meeting types see biggest lift, which data sources contribute most to accuracy
- Run `hypothesis-generation` with the anomaly data and context
- Example hypotheses the system might generate:
  - "Brief usefulness score dropped 15% this week. Hypothesis: recent Clay API changes are returning less detailed news data. Test: supplement with a second Claygent query specifically for industry news."
  - "Discovery call briefs plateau at 3.8/5 usefulness while demo briefs score 4.2/5. Hypothesis: discovery briefs include too many talk tracks that the caller does not use. Test: reduce talk tracks to 2 and add 3 more discovery questions."
  - "Outcome lift declining for repeat meetings. Hypothesis: multi-meeting context chains are too long and diluting key insights. Test: summarize prior call context to 3 bullet points instead of full detail."
  - "Objection prediction accuracy is 40%. Hypothesis: competitive intelligence is stale. Test: re-run competitive enrichment for every account 7 days before the meeting instead of relying on cached data."
- Store hypotheses in Attio. If risk = "high", alert human. If "low" or "medium", proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Use `posthog-experiments` to create a feature flag splitting brief generation between control (current prompt/config) and variant (hypothesis change)
- Implement the variant:
  - If testing prompt structure: deploy the new prompt template via n8n workflow config
  - If testing data sources: add or modify Clay enrichment columns
  - If testing section ordering: modify the brief generation prompt's section sequence
  - If testing question style: adjust the question generation instructions
  - If testing context chain length: modify the multi-meeting context summarization logic
- Set experiment duration: minimum 7 days or 30+ briefs per variant, whichever is longer
- Log experiment in Attio with hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog: compare usefulness scores, accuracy scores, and outcome lift between control and variant
- Run `experiment-evaluation` to determine: Adopt, Iterate, Revert, or Extend
- If Adopt: update the live prompt/configuration to use the winning variant. Log the change. Move to Phase 5.
- If Iterate: the result was inconclusive or showed partial improvement. Generate a refined hypothesis. Return to Phase 2.
- If Revert: the variant performed worse. Restore the control configuration. Log the failure with reasoning. Return to Phase 1.
- Store the full evaluation in Attio (decision, confidence, metric deltas, reasoning)

**Phase 5 — Report (weekly via n8n cron):**
- Generate weekly optimization brief:
  - Anomalies detected this week (brief quality, adoption, outcome)
  - Experiments running, completed, decided
  - Net impact on meeting prep KPIs from all adopted changes
  - Current brief configuration: which prompt variant is live, which data sources are active, which sections are included per meeting type
  - Distance from estimated local maximum (based on rate of improvement declining)
  - Recommended focus for next week
- Post to Slack, store in Attio

### 2. Deploy Enhanced Brief Quality Monitor

Extend the `autonomous-optimization` drill for Durable-level depth:

**Add these dashboard panels:**
- **Experiment tracker**: Current experiments running, their hypotheses, and time remaining
- **Optimization history**: All experiments run, their outcomes, and cumulative impact
- **Convergence plot**: Graph the magnitude of improvement from each adopted experiment over time. When the line flattens to <2%, the system is converging.
- **Predictive accuracy trend**: Track how often the brief's predicted objections, pain points, and stakeholder roles match what actually happened in the call

**Add these alerts:**
- If experiment revert rate exceeds 50% (2 of last 4 experiments reverted), pause optimization and alert for human review
- If brief generation latency exceeds 5 minutes (infrastructure issue), alert immediately
- If predictive accuracy drops below 30% for any meeting type, flag that meeting type's prompt for manual review

### 3. Configure Optimization Guardrails

Apply the guardrails from the `autonomous-optimization` drill:

- **Rate limit:** Maximum 1 active experiment at a time on the meeting prep play
- **Revert threshold:** If call outcome lift drops below 15% during any experiment (half the target), auto-revert immediately
- **Human approval required for:**
  - Changes to the core brief structure (adding or removing sections)
  - Changes to data source providers (switching from Clay to a different enrichment tool)
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review
- **Never optimize what isn't measured:** All brief events must have PostHog tracking before experiments can target them

### 4. Build Predictive Intelligence

As the optimization loop accumulates months of data, build predictive capabilities:

- **Objection prediction model**: Track which objections the brief predicted vs which actually occurred. Over time, the system should achieve >60% objection prediction accuracy for repeat meeting types.
- **Outcome prediction**: Using deal data (stage, BANT score, stakeholder map completeness, brief quality score), predict whether a meeting will result in a committed next step. Alert the caller when a meeting has <30% predicted success rate — these need extra preparation.
- **Optimal meeting cadence**: Analyze deal velocity data to recommend when to schedule the next meeting. If deals that move to demo within 5 days of discovery close 2x faster, the brief should recommend booking the demo before the discovery call ends.

Log prediction accuracy as PostHog metrics so the optimizer can track and improve these models.

### 5. Monitor Convergence

Track the magnitude of improvement from each adopted experiment:

- If the last 3 consecutive experiments each produced <2% improvement in either usefulness scores or outcome lift:
  1. The meeting prep system is converged — current performance is near-optimal given available data sources and LLM capabilities
  2. Reduce monitoring frequency from daily to weekly
  3. Reduce experiment frequency from 4/month to 1/month (maintenance mode)
  4. Generate a convergence report:
     ```
     Meeting Prep Optimization Converged.
     Current performance:
     - Brief usefulness: {X}/5
     - Outcome lift vs non-prepped: {X}%
     - Adoption rate: {X}%
     - Objection prediction accuracy: {X}%

     Further gains require:
     - New data sources (e.g., intent data, product usage data)
     - New LLM capabilities (e.g., longer context, multimodal)
     - Strategic changes (new meeting formats, new buyer personas)

     Tactical optimization has reached its limit.
     ```
  5. Post to Slack, store in Attio

### 6. Handle Strategic Shifts

When external conditions change, the optimizer detects the shift via metric anomalies:

- **New product launch**: Brief templates need updating with new feature catalog. The optimizer should detect that pain-to-feature mappings are missing the new features.
- **New market segment**: Existing prompts may not work for a different buyer persona. The optimizer should detect lower brief quality for the new segment and recommend segment-specific prompts.
- **LLM capability changes**: When a better model becomes available (e.g., new Claude version), the optimizer should test it as a variant against the current model.
- **Competitive shift**: If competitive mentions in calls suddenly increase, the optimizer should detect this and prioritize competitive intelligence enrichment.

In these cases: alert the founder that tactical optimization is insufficient and strategic review is needed. Provide the data to support the diagnosis.

## Time Estimate

- 15 hours: Autonomous optimization setup (n8n workflows, PostHog experiments, guardrails)
- 8 hours: Enhanced brief quality monitor (additional dashboard panels, alerts, convergence tracking)
- 5 hours: Predictive intelligence initial setup (objection prediction, outcome prediction)
- 72 hours: Ongoing optimization over 6 months (~3 hours/week for monitoring, experiment design, evaluation)
- 10 hours: Monthly strategic reviews (human reviews optimization brief, approves high-risk changes)
- 10 hours: Convergence analysis and maintenance mode transition

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal context, experiment logging, convergence tracking | $29/user/mo (Plus) or $59/user/mo (Pro) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — account research, competitive intelligence refresh | $185/mo (Launch) or $495/mo (Growth) — [clay.com/pricing](https://www.clay.com/pricing) |
| Anthropic API | AI — brief generation, feedback scoring, hypothesis generation, experiment evaluation | Usage-based, ~$15-40/mo at volume — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| n8n | Automation — optimization loop, monitoring, reporting, experiment routing | $60/mo (Pro, 10K executions) — [n8n.io/pricing](https://n8n.io/pricing) |
| Fireflies | Transcription — feedback loop and context chains | $19/seat/mo (Pro) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Cal.com | Scheduling — meeting trigger source | Free (self-hosted) or $12/seat/mo — [cal.com/pricing](https://cal.com/pricing) |
| PostHog | Analytics — dashboards, experiments, anomaly detection, convergence | Free up to 1M events/mo, then usage-based — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost this level:** ~$100-300/mo. Primary cost drivers: Clay ($185-495), n8n Pro ($60), Anthropic API (~$25-40 for optimization loop + brief generation), Fireflies ($19/seat).

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: detect anomalies in brief quality and call outcomes, generate hypotheses about prompt and data source changes, run A/B experiments, evaluate results, auto-implement winners. Weekly optimization briefs. Converges when successive experiments produce <2% improvement.
- `autonomous-optimization` — enhanced monitoring with experiment tracking, optimization history, convergence plotting, and predictive accuracy trends. Provides the data substrate the optimization loop reads from.
