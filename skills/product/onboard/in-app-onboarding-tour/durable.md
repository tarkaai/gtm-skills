---
name: in-app-onboarding-tour-durable
description: >
  Interactive Product Tour — Durable Intelligence. AI agent runs the continuous optimization loop:
  detect metric anomalies, generate improvement hypotheses, run A/B experiments, evaluate results,
  and auto-implement winners. Weekly optimization briefs. Converges when successive experiments
  produce <2% improvement.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving activation >=45% over 6 months via autonomous AI optimization"
kpis: ["7-day activation rate", "Tour completion rate", "Median time to activation", "Experiment velocity (experiments/month)", "Cumulative AI lift (pp)", "Optimization convergence rate"]
slug: "in-app-onboarding-tour"
install: "npx gtm-skills add product/onboard/in-app-onboarding-tour"
drills:
  - autonomous-optimization
  - onboarding-health-monitor
  - nps-feedback-loop
---

# Interactive Product Tour — Durable Intelligence

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The AI agent takes over the optimization loop. It monitors all onboarding metrics daily, detects anomalies, generates hypotheses for improvement, runs A/B experiments, evaluates results, and auto-implements winners. Human involvement is limited to reviewing weekly briefs and approving high-risk changes. The system finds the local maximum of onboarding performance and maintains it as conditions change.

Pass threshold: Activation rate sustained at >=45% (or improving) over 6 consecutive months with at least 4 experiments per month. The play is considered converged when 3 consecutive experiments produce <2% improvement.

## Leading Indicators

- Weekly optimization briefs generated on schedule with actionable insights
- At least 1 experiment running at all times (no idle periods)
- Anomalies detected and diagnosed within 24 hours of occurrence
- Experiment win rate >=30% (at least 1 in 3 experiments produces a significant improvement)
- No activation rate drop below 40% lasting more than 2 consecutive weeks without auto-revert
- NPS scores for onboarding-specific questions trending stable or improving
- Convergence progress: diminishing returns detected and reported

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill. Configure it specifically for the onboarding play:

**Phase 1 — Monitor (daily via n8n cron):**
- Query PostHog for onboarding KPIs: activation rate (7-day trailing cohort), tour completion rate, per-persona activation rates, time to activation, email engagement rates
- Compare each metric to its 4-week rolling average
- Classify: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
- If normal: log to Attio, no action
- If anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context from Attio: current tour variants, persona distribution, recent experiments, recent product deployments
- Pull 8-week onboarding metric history from PostHog
- Generate 3 ranked hypotheses using Claude (Anthropic API). Hypothesis format: "If we [change], then [metric] will [improve by X%], because [reasoning based on data]."
- Example hypotheses for a drop in activation:
  - "Tour step 3 completion dropped after the latest product deploy — a CSS selector may be targeting a renamed element. Fixing it will restore tour completion by 15%."
  - "Persona B activation dropped while A and C are stable — the team_lead tour may need an updated invitation flow that matches the new UI."
  - "Email 2 open rate dropped — the subject line may have been flagged by spam filters after a domain reputation change."
- Store hypotheses in Attio. If top hypothesis is high-risk (affects >50% of users or requires budget change), alert human for approval and STOP. Otherwise proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment: create a PostHog experiment with feature flag splitting traffic between control (current) and variant (hypothesis change)
- Implement the variant using the appropriate fundamental (e.g., update Intercom tour step, change Loops email copy, adjust n8n trigger timing)
- Set duration: minimum 7 days or 100+ samples per variant, whichever is longer
- Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull results from PostHog. Require 95% statistical significance.
- Decision:
  - **Adopt**: Variant wins. Roll out to 100%. Log the change with before/after metrics.
  - **Iterate**: Result was directionally positive but not significant. Generate a refined hypothesis. Return to Phase 2.
  - **Revert**: Control wins. Disable variant. Log the failure. Return to Phase 1.
  - **Extend**: Insufficient sample size. Keep running for one more period.
- Store full evaluation in Attio: decision, confidence, reasoning, net metric change.

**Phase 5 — Report (weekly via n8n cron, every Monday):**
- Aggregate the week's optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate: net metric change from all adopted changes this week
- Generate the weekly optimization brief:
  - What changed and why
  - Net impact on activation rate, tour completion, and time to activation
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

### 2. Deploy onboarding health monitoring

Run the `onboarding-health-monitor` drill. This provides the daily monitoring layer that feeds into the autonomous optimization loop:

- Daily health checks at 09:00 UTC: activation rate, tour completion, email engagement, stalled user count
- Anomaly detection: flag any metric declining for 3+ consecutive days or dropping 25%+ in a single day
- Stalled-user analysis: group stalled users by stuck-point and persona, feed patterns into hypothesis generation
- Guardrail alerts:
  - Activation rate below 25% for 48h: urgent alert (likely product bug or broken tour)
  - Tour completion below 10%: tour may be broken (DOM changes after a deploy)
  - Email bounce rate above 5%: pause enrollments and investigate
- Weekly activation report with trend analysis and recommended actions

### 3. Launch NPS feedback loops

Run the `nps-feedback-loop` drill for onboarding-specific feedback:

- Trigger NPS survey via Intercom at day 14 post-signup (after the onboarding window closes)
- Two questions: "How likely are you to recommend [product]?" (0-10) + "What is the main reason for your score?" (open text)
- Segment responses by persona, tour variant, and activation status
- Close the loop:
  - Promoters (9-10): Ask for review or case study. Feed into referral program.
  - Passives (7-8): Send resource addressing their stated concern. Offer a call.
  - Detractors (0-6): Personal outreach within 48 hours. Log in Attio for account owner.
- Feed detractor themes into the autonomous optimization loop as hypothesis inputs
- Track NPS monthly. Declining NPS in a specific persona triggers investigation.

### 4. Implement guardrails

Configure critical guardrails for the autonomous loop:

- **Rate limit**: Maximum 1 active experiment at a time. Never stack experiments on the onboarding flow.
- **Revert threshold**: If activation rate drops >30% during any experiment, auto-revert immediately.
- **Human approval required for**:
  - Changes affecting >50% of users (e.g., replacing the entire tour)
  - Changes to email content that affect all personas
  - Any hypothesis flagged as high-risk
- **Cooldown**: After a failed experiment (revert), wait 7 days before testing the same variable.
- **Monthly cap**: Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review.
- **Never optimize what is not measured**: If a KPI lacks PostHog tracking, fix tracking first.

### 5. Detect convergence

The optimization loop monitors for convergence — when the onboarding experience has reached its local maximum:

- Track the magnitude of improvement from each experiment
- If 3 consecutive experiments produce <2% improvement, declare convergence
- At convergence:
  1. Reduce monitoring frequency from daily to weekly
  2. Report: "Onboarding is optimized. Current activation rate is [X%]. Tour completion is [Y%]. Further gains require strategic changes (new product features, new user segments, redesigned core flows) rather than tactical optimization."
  3. Shift optimization effort to other plays

### 6. Monthly executive review

Generate a monthly report summarizing:
- Activation rate trend (6-month chart)
- Experiments run, won, lost, and net cumulative lift
- NPS trend and key feedback themes
- Convergence progress (are improvements getting smaller?)
- Cost efficiency: cost per activated user trend
- Recommendation: continue optimizing, declare convergence, or escalate strategic issues

## Time Estimate

- 20 hours: Deploy autonomous optimization loop and monitoring (month 1)
- 10 hours: Configure NPS feedback loops and guardrails (month 1)
- 15 hours/month: Agent compute for daily monitoring, hypothesis generation, experiment management (months 1-6)
- 5 hours/month: Human review of weekly briefs and monthly reports (months 1-6)
- 10 hours: Convergence analysis and documentation (month 5-6)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, experiments, feature flags, anomaly detection | Free up to 1M events/mo; ~$50-100/mo at scale ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Product tours, in-app messages, NPS surveys | Essential $39/seat/mo + Proactive Support Plus $99/mo + usage ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Behavioral emails, NPS follow-ups | $49/mo for 1K+ contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Automation: optimization loop scheduling, monitoring, intervention triggers | Pro: EUR 60/mo (10K executions) or self-hosted free ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation, report generation | Sonnet 4.6: $3/$15 per MTok; estimated ~$20-50/mo for weekly optimization ([platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing)) |
| Attio | Audit trail, campaign records, experiment logs | Included in standard stack |

**Estimated monthly cost at this level:** $318-$510/mo (Intercom ~$150-250 + Loops $49 + n8n $60 + PostHog $50-100 + Anthropic API $20-50)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect anomalies → generate hypotheses → run A/B experiments → evaluate results → auto-implement winners. This is what makes Durable fundamentally different from Scalable.
- `onboarding-health-monitor` — daily health checks, stalled-user detection, weekly activation reports, and guardrail alerts specific to the onboarding funnel
- `nps-feedback-loop` — collects and acts on user feedback to surface qualitative insights that quantitative metrics miss, feeding detractor themes into the optimization loop
