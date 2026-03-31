---
name: sandbox-environment-demo-durable
description: >
  Sandbox Environment Demo — Durable Intelligence. Always-on AI agents continuously optimize the
  sandbox program: detect metric anomalies, generate improvement hypotheses, run experiments,
  auto-implement winners, and produce weekly intelligence reports correlating usage patterns
  with deal outcomes. Converges when successive experiments produce <2% improvement.
stage: "Sales > Connected"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "152 hours over 6 months"
outcome: "Sustained or improving sandbox-to-close conversion over 6 months via autonomous optimization loop finding the local maximum"
kpis: ["Sandbox-to-close conversion", "Optimization loop velocity (experiments/month)", "Prediction accuracy", "Usage personalization effectiveness", "Active usage rate", "Deal velocity improvement"]
slug: "sandbox-environment-demo"
install: "npx gtm-skills add sales/connected/sandbox-environment-demo"
drills:
  - autonomous-optimization
  - sandbox-intelligence-reporting
---

# Sandbox Environment Demo — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

The sandbox program reaches its local maximum — the best possible sandbox-to-close conversion rate given the current market, product, and audience. An always-on AI optimization loop monitors sandbox KPIs daily, detects anomalies, generates hypotheses, runs experiments, and auto-implements winners. Weekly intelligence reports surface pipeline risk and optimization opportunities. The system converges when 3 consecutive experiments each produce less than 2% improvement, at which point monitoring frequency reduces and the team is notified that further gains require strategic changes (new product features, new market segments) rather than tactical optimization.

## Leading Indicators

- Optimization loop activity: experiments launched per month (target: 2-4)
- Experiment win rate: percentage of experiments that produce statistically significant improvement
- Prediction model accuracy: weekly close predictions vs. actual outcomes (target: >70%)
- Metric stability: primary KPIs staying within ±10% of local maximum for 4+ consecutive weeks
- Intelligence report action rate: percentage of report recommendations that the sales team acts on

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the sandbox program. This creates the always-on monitor-diagnose-experiment-evaluate-implement cycle:

**Phase 1 — Monitor (daily via n8n cron):**
Use PostHog anomaly detection to check sandbox KPIs daily against their 4-week rolling averages. The agent classifies each KPI as normal (within ±10%), plateau (±2% for 3+ weeks), drop (>20% decline), or spike (>50% increase). KPIs monitored:
- Sandbox-to-close conversion rate
- Active usage rate
- Time to first login
- Milestone completion rate
- Engagement score distribution
- Auto-provisioning success rate

If all KPIs are normal, log the check and take no action. If any anomaly is detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context: current sandbox configuration from Attio (persona distribution, checklist designs, intervention timing), 8-week metric history from PostHog, and recent A/B test results. Claude generates 3 ranked hypotheses for the anomaly, each with expected impact and risk level. Example hypotheses:
- "Milestone completion dropped 25% because the new checklist item 'Connect integration' requires technical setup most prospects cannot complete alone. Hypothesis: replace with 'Invite a teammate' which requires less effort." (Medium risk, High impact)
- "First-login rate declined 15% because kickoff emails are landing in spam for Gmail users. Hypothesis: switch from HTML to plain-text format." (Low risk, Medium impact)

High-risk hypotheses (budget changes >20%, targeting changes affecting >50% of traffic) require human approval before proceeding. Low and medium risk proceed automatically to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
The agent designs and launches an experiment via PostHog feature flags. Control = current configuration, Variant = hypothesis change. Minimum experiment duration: 7 days or 100 samples per variant, whichever is longer. Maximum 1 active experiment at a time.

**Phase 4 — Evaluate (triggered by experiment completion):**
Pull results from PostHog. Claude evaluates: Adopt (implement winner permanently), Iterate (refine hypothesis and test again), Revert (restore control, log failure), or Extend (keep running for more data). Auto-implement Adopt decisions. Store the full evaluation in Attio.

**Phase 5 — Report (weekly via n8n cron):**
Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made. Calculate net metric change from all adopted changes. Post the weekly optimization brief to Slack and store in Attio.

**Guardrails (enforced automatically):**
- Maximum 1 active experiment per play at a time
- Auto-revert if primary metric drops >30% during an experiment
- Human approval required for high-risk hypotheses
- 7-day cooldown after a failed experiment on the same variable
- Maximum 4 experiments per month; if all 4 fail, pause and flag for human review
- Never optimize a KPI that does not have PostHog tracking

### 2. Launch sandbox intelligence reporting

Run the `sandbox-intelligence-reporting` drill to produce weekly intelligence alongside the optimization brief:

1. **Predictive model refinement**: Monthly, retrain the close-probability model using the latest outcome data. Track which usage signals gain or lose predictive power as the market and product evolve.

2. **Weekly pipeline risk report**: For every active sandbox deal, compute the current close probability. Classify as Likely to close (>60%), Needs attention (30-60%), or At risk (<30%). Send direct Slack alerts to deal owners for "Needs attention" and "At risk" deals with specific recommended actions:
   - "Jane at Acme Corp has not logged in since Tuesday. Her engagement score dropped from 62 to 34. Recommend: personal outreach asking if she hit a blocker."
   - "Tom at Finco completed all 5 milestones and uploaded their own data. Close probability: 84%. Recommend: send proposal this week."

3. **Sandbox experience quality tracking**: Monitor error rates, help request patterns, and feature usage gaps across all sandboxes. Surface recurring friction points that the product team should address. Example: "18% of sandbox users encounter an error when trying to export reports. This blocks milestone 4 for most prospects."

4. **Prediction accuracy tracking**: Log each weekly prediction and compare to actual deal outcomes. If accuracy drops below 65%, flag the model for retraining with the latest data.

### 3. Implement adaptive sandbox personalization

Use the optimization loop's learnings to continuously improve personalization:

1. **Dynamic persona selection**: As the model learns which configurations drive the highest engagement by segment, update the AI config prompt to weight these learnings. Example: if the model discovers that fintech prospects engage 40% more with the "compliance_workflow" sample data persona than the generic "fintech_default", update the persona selection logic.

2. **Adaptive success checklists**: Track which checklist items are most predictive of close across all sandboxes. Retire low-signal milestones and promote high-signal ones. The checklist should evolve quarterly based on outcome data.

3. **Intervention timing optimization**: The optimization loop tests intervention timing as a variable. Let the agent experiment with earlier vs. later check-ins, different message formats, and different escalation thresholds to find the optimal intervention cadence.

### 4. Monitor convergence

The optimization loop runs indefinitely. However, the agent detects convergence — when 3 consecutive experiments each produce less than 2% improvement in the primary metric (sandbox-to-close conversion). At convergence:

1. Reduce monitoring from daily to weekly.
2. Reduce experiment frequency to 1 per month (maintenance testing).
3. Report to the team: "The sandbox program has reached its local maximum. Current sandbox-to-close conversion is [X%]. Deal velocity improvement is [Y days]. Further gains require strategic changes: new product features for the sandbox, new market segments to target, or new channels to combine with sandbox access."

### 5. Set durable guardrails

If any KPI degrades more than 10% from the established local maximum for 2 or more consecutive weeks:

1. The agent generates a diagnostic report: what changed, when, and possible causes (market shift, product change, competitive response, seasonal effect).
2. Alert the team with the diagnostic and recommended action.
3. Re-enter active optimization (daily monitoring, monthly experiments) until metrics stabilize.

Evaluate sustainability continuously. This level does not have a fixed end date.

## Time Estimate

- 30 hours: Configure autonomous optimization loop (5 phases, guardrails, n8n workflows)
- 20 hours: Set up intelligence reporting (predictive model, pipeline risk, experience quality)
- 15 hours: Build adaptive personalization logic
- 12 hours: Initial optimization cycle (first month of experiments)
- 75 hours: Ongoing monitoring, experiment cycles, and model retraining over 6 months (approximately 3 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loom | Walkthrough videos | $12.50/creator/mo (Business, annual) — [loom.com/pricing](https://www.loom.com/pricing) |
| Loops | Lifecycle emails, intervention sequences | $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app guidance, contextual messages in sandboxes | $85/seat/mo (Advanced for automation, annual) — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Clay | Ongoing prospect enrichment for AI personalization | ~$150-350/mo — [clay.com/pricing](https://www.clay.com/pricing) |
| Anthropic API | Optimization loop (hypothesis generation, evaluation, reporting, personalization) | ~$50-150/mo (higher volume for continuous optimization) — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost:** ~$350-650/mo (Loops + Intercom Advanced + Clay + Anthropic + Loom)

_CRM (Attio), analytics (PostHog), and automation (n8n) are standard stack — not included in play budget._

## Drills Referenced

- `autonomous-optimization` — the always-on monitor → diagnose → experiment → evaluate → implement loop that finds the local maximum; detects anomalies, generates hypotheses, runs A/B tests, auto-implements winners, and produces weekly optimization briefs
- `sandbox-intelligence-reporting` — generates weekly intelligence reports correlating sandbox usage with deal outcomes, maintains the close-probability predictive model, and surfaces pipeline risk and sandbox experience quality issues
