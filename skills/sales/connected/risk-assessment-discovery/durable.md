---
name: risk-assessment-discovery-durable
description: >
  Risk & Concern Discovery -- Durable Intelligence. Autonomous optimization loop continuously
  improves risk prediction accuracy, mitigation effectiveness, and question bank performance.
  Agent detects metric anomalies, generates improvement hypotheses, runs experiments, and
  auto-implements winners. Converges when successive experiments produce <2% improvement.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "138 hours over 6 months"
outcome: "Sustained or improving risk mitigation success and deal predictability over 6 months via autonomous optimization"
kpis: ["Risk prediction accuracy", "Mitigation success rate trend", "Late-stage surprise elimination rate", "Close rate improvement (risk-assessed vs unassessed)", "Autonomous optimization experiment win rate"]
slug: "risk-assessment-discovery"
install: "npx gtm-skills add sales/connected/risk-assessment-discovery"
drills:
  - autonomous-optimization
  - risk-intelligence-monitor
  - risk-pattern-analysis
---

# Risk & Concern Discovery -- Durable Intelligence

> **Stage:** Sales > Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

The risk discovery system finds its local maximum. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in risk discovery performance, generate improvement hypotheses, run A/B experiments on risk prediction prompts, question bank variants, and mitigation delivery strategies, evaluate results, and auto-implement winners. Weekly optimization briefs report what changed and why. The system converges when successive experiments produce <2% improvement -- at that point, risk discovery is optimized for the current market and audience.

## Leading Indicators

- Autonomous optimization loop is running: at least 2 experiments per month
- Risk prediction accuracy is trending upward (or plateauing at a high level after convergence)
- Mitigation success rate is improving across all 5 risk categories
- Late-stage surprise rate is approaching zero
- Close rate gap between risk-assessed and unassessed deals is widening (risk discovery is clearly adding value)
- Optimization experiments are producing diminishing returns (approaching convergence)
- Weekly briefs show the system self-correcting when metrics dip

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the risk discovery play. This creates the always-on agent loop:

**Phase 1 -- Monitor (daily via n8n cron):**
- Check primary KPIs via PostHog: risk discovery rate, mitigation success rate, late-stage surprise rate, prediction accuracy, close rate impact
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 -- Diagnose (triggered by anomaly):**
- Gather context: current risk extraction prompts, question bank, mitigation library, segment targeting
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data
- Receive 3 ranked hypotheses. Examples of what the optimizer might test:
  - "Risk extraction prompt is missing organizational risks for SMB segment -- add SMB-specific probes"
  - "Mitigation email open rates dropped because subject lines reference 'concern' -- test neutral framing"
  - "Prediction model over-weights deal age -- reduce weight, increase weight on stakeholder count"
  - "Financial risk mitigation success rate dropped -- the ROI calculator is outdated, update benchmarks"
- Store hypotheses in Attio. If top hypothesis is high-risk, send for human review and stop.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
- Design the experiment via PostHog feature flags:
  - For prompt changes: split new calls between control (current prompt) and variant
  - For mitigation changes: A/B test delivery message, asset selection, or timing
  - For prediction model changes: run both models in parallel, compare accuracy
- Minimum experiment duration: 7 days or 20+ data points per variant, whichever is longer
- Log experiment start in Attio

**Phase 4 -- Evaluate (triggered by experiment completion):**
- Pull results from PostHog. Run `experiment-evaluation`.
- **Adopt:** Variant wins -- update live configuration, log the change
- **Iterate:** Results inconclusive -- generate a refined hypothesis, return to Phase 2
- **Revert:** Variant loses -- restore control, log the failure, return to Phase 1
- Store full evaluation with decision, confidence, and reasoning

**Phase 5 -- Report (weekly via n8n cron):**
- Aggregate: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes
- Generate weekly optimization brief:
  - What changed and why
  - Net impact on risk discovery KPIs
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack, store in Attio

### 2. Maintain the risk intelligence monitor

The `risk-intelligence-monitor` from Scalable continues running. At Durable level, the autonomous optimizer can modify its configuration:
- Adjust predictive scoring weights based on experiment results
- Update risk extraction prompts based on pattern analysis
- Tune alert thresholds based on false positive/negative rates

The monitor provides the raw data that the optimizer uses to detect anomalies.

### 3. Evolve pattern analysis with optimization feedback

The `risk-pattern-analysis` drill continues bi-weekly. At Durable level, it feeds directly into the optimization loop:
- Pattern analysis identifies declining mitigation success in a category -> optimizer generates hypothesis -> experiment tests a new mitigation approach
- Segment analysis reveals a new risk pattern -> optimizer updates prediction prompts -> experiment validates the improvement
- Question bank analysis shows surface rate dropping for a question -> optimizer generates replacement candidates -> experiment tests new vs. old

### 4. Implement adaptive risk prediction

As the optimization loop runs experiments on the prediction model, the system evolves:
- Segment-specific risk profiles become more precise (e.g., "Healthcare Series B companies have 92% organizational risk, weighted toward HIPAA compliance adoption")
- Risk scores become more calibrated (predicted scores match actual severity more closely)
- Mitigation recommendations become personalized (e.g., "For this segment, reference calls resolve vendor risk 3x faster than documentation")

### 5. Set Durable-level guardrails

All Scalable guardrails remain active. Add:
- **Experiment rate limit:** Maximum 1 active experiment at a time. Never stack experiments.
- **Revert threshold:** If any primary KPI drops >30% during an experiment, auto-revert immediately.
- **Human approval required for:**
  - Changes to risk extraction prompts that affect >50% of calls
  - Changes to mitigation content that modify factual claims (security, compliance, legal)
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing the same variable.
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review.
- **Convergence detection:** When 3 consecutive experiments produce <2% improvement, reduce optimization frequency from weekly to monthly. Report: "Risk discovery system has reached local maximum."

### 6. Monitor for 6 months

This level runs continuously. Monthly review:
- Is prediction accuracy still improving or has it converged?
- Are new risk patterns emerging that the model has not seen before (market shifts, product changes)?
- Is the mitigation content library staying current (case studies from recent customers, updated security docs)?
- Are the weekly optimization briefs actionable, or has the system run out of meaningful experiments?

At convergence, the system shifts from active optimization to maintenance monitoring. The daily risk intelligence monitor continues, but experiments only run when a significant anomaly is detected.

## Time Estimate

- Autonomous optimization setup: 8 hours (PostHog experiments, n8n cron workflows, hypothesis/evaluation prompts)
- Integration with existing risk monitor: 4 hours (connect optimizer to monitor configuration)
- Pattern analysis optimization feedback loop: 3 hours (bidirectional data flow)
- Guardrail configuration: 3 hours (experiment limits, revert thresholds, human approval gates)
- Weekly optimization brief review: 30 min/week x 24 weeks = 12 hours
- Monthly deep review: 2 hours/month x 6 months = 12 hours
- Experiment monitoring and intervention: 1 hour/week x 24 weeks = 24 hours
- Content library maintenance: 2 hours/month x 6 months = 12 hours
- Convergence assessment: 2 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Fireflies | Call transcription for all sales calls | Pro: $10/user/mo annual ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |
| Clay | Prospect enrichment for risk prediction | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Anthropic (Claude) | Risk extraction, optimization hypotheses, experiment evaluation | ~$30-80/mo with experiments ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Instantly | Mitigation email delivery | Growth: $30/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Gong (optional) | Advanced call analytics for risk signal detection | ~$1,600/user/year ([gong.io/pricing](https://www.gong.io/pricing)) |

**Total play-specific cost:** ~$255-505/mo (without Gong); ~$390-640/mo (with Gong)

_Your CRM (Attio), PostHog, and automation platform (n8n) are standard stack -- not included._

## Drills Referenced

- `autonomous-optimization` -- the core Durable loop: monitor metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, report weekly
- `risk-intelligence-monitor` -- always-on scanning of transcripts, emails, and deal data (from Scalable); configuration now modified by the optimizer
- `risk-pattern-analysis` -- bi-weekly aggregation feeding into the optimization loop with bidirectional data flow
