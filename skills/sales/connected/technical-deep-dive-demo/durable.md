---
name: technical-deep-dive-demo-durable
description: >
  Technical Deep-Dive Demo — Durable Intelligence. Always-on AI agents finding the local maximum
  of technical demo effectiveness. The autonomous-optimization drill runs the core loop: detect
  metric anomalies, generate improvement hypotheses, run A/B experiments, evaluate results, and
  auto-implement winners. Converges when successive experiments produce <2% improvement.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Durable Intelligence"
time: "155 hours over 6 months"
outcome: "Sustained or improving POC conversion rate and technical validation speed over 6 months via continuous autonomous optimization of demo content, sequencing, and follow-up strategy"
kpis: ["POC conversion rate (sustained ≥45%)", "Technical validation speed trend", "Demo module effectiveness convergence", "Autonomous experiment win rate", "Technical close rate"]
slug: "technical-deep-dive-demo"
install: "npx gtm-skills add sales/connected/technical-deep-dive-demo"
drills:
  - autonomous-optimization
  - demo-performance-monitor
  - technical-demo-content-assembly
---
# Technical Deep-Dive Demo — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Outcomes
The play runs autonomously with AI agents continuously optimizing every lever of technical demo effectiveness. POC conversion rate sustains at or above 45%. Technical validation speed (days from demo to POC commitment) continues to improve or holds at the Scalable-level best. The `autonomous-optimization` drill runs the core monitor-diagnose-experiment-evaluate-implement loop. When successive experiments produce less than 2% improvement for 3 consecutive cycles, the play has reached its local maximum.

## Leading Indicators
- Anomaly detection fires within 24 hours of any metric degradation
- Hypotheses generated within 4 hours of anomaly detection
- Experiments launched within 48 hours of hypothesis approval (or auto-approved for low/medium risk)
- Weekly optimization briefs delivered on schedule
- Convergence signal: experiment win margins shrinking toward 2% threshold

## Instructions

### 1. Deploy the autonomous optimization loop
Run the `autonomous-optimization` drill configured for the technical demo pipeline. This creates the always-on agent loop:

**Phase 1 — Monitor (daily via n8n cron):**
The agent checks the play's primary KPIs daily using `posthog-anomaly-detection`:
- POC conversion rate (from `technical_demo_completed` to `poc_started`)
- Technical validation speed (days between events)
- Demo module effectiveness scores (from `demo-performance-monitor` weekly reports)
- Follow-up package engagement rate
- Technical close rate (from `poc_started` to `deal_closed_won`)

Compare last 2 weeks against 4-week rolling average. Classify as: **normal** (within ±10%), **plateau** (±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase). If anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context from Attio (current demo configuration, module ordering, follow-up strategy), pulls 8-week metric history from PostHog, and runs `hypothesis-generation` with the anomaly data. Returns 3 ranked hypotheses. Examples specific to this play:
- "POC conversion dropped because new prospects in {segment} have different technical requirements than the module ordering was optimized for"
- "Technical validation speed increased because follow-up packages are missing {integration} documentation that prospects need for internal review"
- "Demo engagement plateaued because the API walkthrough module has not been updated to reflect the latest product API changes"

If the top hypothesis has risk = "high" (e.g., changing the entire demo structure), send a Slack alert for human review. If risk = "low" or "medium," proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
Design and run the experiment:
- Use `posthog-experiments` to create a feature flag splitting demos between control and variant
- Implement the variant by modifying the relevant input to `technical-demo-content-assembly` (e.g., change module ordering, add a new integration demo, adjust the security review depth)
- Minimum duration: 7 days or 15 demos per variant, whichever is longer
- Log experiment start in Attio with hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
Pull experiment results from PostHog. Run `experiment-evaluation`:
- **Adopt:** Variant wins by ≥5% with statistical significance. Update the default demo configuration. Log the change.
- **Iterate:** Results inconclusive or marginal (<5% improvement). Generate a refined hypothesis. Return to Phase 2.
- **Revert:** Variant performs worse. Disable variant, restore control. Log the failure with reasoning.
- **Extend:** Insufficient sample size. Keep running for another period.

**Phase 5 — Report (weekly via n8n cron):**
Generate a weekly optimization brief:
- Anomalies detected this week
- Experiments running, completed, or started
- Net metric change from adopted changes
- Current distance from estimated local maximum (based on diminishing experiment returns)
- Recommended focus for next week

Post to Slack and store in Attio as a campaign note.

### 2. Maintain the demo performance monitor
Keep the `demo-performance-monitor` drill (deployed at Scalable) running as the data backbone for autonomous optimization:
- Daily funnel monitoring with anomaly alerts
- Weekly pain-to-feature effectiveness rankings
- Demo quality scoring from transcript analysis
- Conversion breakdown by attendee role, module, tech stack, and segment

The autonomous optimization loop reads from these monitoring outputs. Do not disable or modify the monitor without updating the optimization loop's data source configuration.

### 3. Evolve technical demo content based on experiment outcomes
As the `autonomous-optimization` drill implements winners, the `technical-demo-content-assembly` drill's behavior changes:
- Module ordering shifts based on A/B test results (e.g., if API-first wins for engineer-heavy audiences, the assembly drill adjusts ordering by attendee profile)
- Integration code templates are updated when new integrations prove more compelling
- Security review depth is calibrated per industry segment based on conversion data
- Follow-up package contents are adjusted based on engagement tracking (remove sections that are never opened, expand sections with high engagement)

Configure n8n to apply experiment outcomes to the assembly drill's configuration automatically. Store the current "winning configuration" as an Attio note tagged `demo-config-current` so the agent always references the latest optimized settings.

### 4. Build adaptive technical intelligence
Beyond the optimization loop, deploy continuous intelligence gathering:

**Competitive technical monitoring:**
- n8n cron (weekly) checks competitor changelog pages, API documentation changes, and new feature announcements
- When a competitor adds a feature that prospects frequently ask about, the agent updates demo Q&A prep to include a comparison talking point
- Store competitive updates in Attio tagged `competitive-technical-intel`

**Product change integration:**
- When the product team ships a new API endpoint, integration, or security feature, the agent updates the demo module library
- n8n webhook listens for product release events and triggers an update to the demo content assembly configuration
- New features are flagged for A/B testing: "Does showing {new_feature} improve POC conversion?"

**Technical blocker pattern analysis:**
- Monthly, the agent aggregates all `technical_blockers_identified` from demo outcomes
- Clusters blockers by category (missing integration, API limitation, security gap, performance concern)
- Generates a prioritized product feedback report: "These technical blockers have cost X POCs this month"
- Stores in Attio and posts to Slack for product team review

### 5. Guardrails (CRITICAL)

- **Rate limit:** Maximum 1 active experiment on the demo pipeline at a time. Never stack experiments.
- **Revert threshold:** If POC conversion drops >30% at any point during an experiment, auto-revert immediately and alert the team.
- **Human approval required for:**
  - Changes that affect more than 50% of demo content (e.g., replacing the entire module structure)
  - New demo modules that have never been tested at any level
  - Changes to sandbox provisioning that could affect prospect experience
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing a new hypothesis on the same variable.
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for strategic review — the issue may be product-market fit, not demo optimization.
- **Never optimize what is not measured:** If a KPI does not have PostHog tracking, fix tracking first before running experiments on it.

### 6. Detect convergence
The optimization loop runs indefinitely. However, it detects convergence: when successive experiments produce diminishing returns (<2% improvement for 3 consecutive experiments). At convergence:

1. The play has reached its local maximum for the current product, market, and audience
2. Reduce monitoring frequency from daily to weekly
3. Reduce experiment cadence from continuous to monthly check-ins
4. Generate a convergence report: "Technical deep-dive demo is optimized. Current performance: {POC conversion rate}, {validation speed}, {close rate}. Further gains require strategic changes (new product capabilities, new market segments, new competitive positioning) rather than tactical demo optimization."
5. Post convergence report to Slack and store in Attio

Re-enter active optimization if: the product ships a major new capability, a new competitor enters the market, or any primary KPI drops below Scalable-level baseline for 2+ consecutive weeks.

---

## Time Estimate
- Autonomous optimization loop setup: 16 hours
- Demo performance monitor maintenance: 2 hours/month (12 total)
- Adaptive content configuration: 8 hours initial + 2 hours/month (20 total)
- Competitive and product intelligence pipelines: 12 hours
- Experiment design, monitoring, and evaluation: 6 hours/month (36 total)
- Weekly brief review and strategic decisions: 2 hours/month (12 total)
- Convergence analysis and reporting: 4 hours

**Agent compute:** ~15 n8n executions/day for monitoring + experiment management. ~$15-30/mo in Claude API for hypothesis generation, experiment evaluation, and brief writing.

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal pipeline, experiment logs, intelligence storage, config state | Plus $29/user/mo |
| PostHog | Anomaly detection, experiments (feature flags + A/B), funnel tracking, dashboards | Free up to 1M events/mo; experiments: 1M flag requests free |
| n8n | Orchestration — daily monitoring crons, experiment management, intelligence pipelines, weekly briefs | Pro €60/mo (10,000 executions) or self-hosted for higher volume |
| Clay | Ongoing account enrichment and tech stack detection | Launch $185/mo or Growth $495/mo |
| Fireflies | Demo call transcription for intelligence extraction | Business $29/user/mo (video + unlimited storage) |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, brief writing, competitive analysis, transcript intelligence | Sonnet 4.6: $3/$15 per 1M tokens (~$30/mo for all agent operations) |
| Cal.com | Scheduling infrastructure | Free or Teams $15/user/mo |

**Play-specific cost:** ~$200-400/mo (n8n Pro + Clay credits + Claude API for agent operations + Fireflies Business; scales with demo volume and experiment frequency)

**Agent compute cost:** Variable. At steady state, ~$30-50/mo for Claude API calls across all autonomous operations. During active experimentation, may spike to $75/mo.

## Drills Referenced
- `autonomous-optimization` — the core Durable drill that creates the always-on monitor-diagnose-experiment-evaluate-implement loop, finding the local maximum of demo effectiveness and maintaining it as conditions change
- `demo-performance-monitor` — continuous monitoring of the discovery-to-demo-to-deal funnel, providing the data backbone for autonomous optimization decisions
- `technical-demo-content-assembly` — generates prospect-customized demo materials; at Durable level, its configuration evolves automatically as experiments produce winners
