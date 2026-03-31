---
name: ab-testing-framework-scalable
description: >
  Product A/B Testing — Scalable Automation. Automated experiment pipeline that continuously
  generates hypotheses, launches tests, collects results, and reports business impact. Agent manages
  the pipeline; humans review results. Target 10+ experiments per 2 months with measurable
  cumulative lift.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=10 experiments in 2 months with measurable cumulative lift across 3+ product areas"
kpis: ["Experiment velocity", "Win rate", "Cumulative lift", "Cycle time", "Product area coverage"]
slug: "ab-testing-framework"
install: "npx gtm-skills add product/retain/ab-testing-framework"
drills:
  - experiment-pipeline-automation
  - experiment-impact-reporting
---

# Product A/B Testing — Scalable Automation

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The experiment pipeline runs continuously with minimal manual intervention. The agent automates hypothesis backlog management, experiment launching, completion monitoring, result collection, and impact reporting. Experiments cover 3+ product areas (onboarding, conversion, feature adoption, retention, pricing). The program produces measurable cumulative lift and the business impact is documented in regular reports. This is the 10x multiplier: instead of manually orchestrating each test, the agent manages a pipeline that always has an experiment running.

## Leading Indicators

- Experiment pipeline automation is live: when one experiment completes, the next launches within 24 hours without human intervention
- Backlog always has 3+ queued hypotheses (replenished automatically or on agent prompt)
- No experiment stall longer than 3 days between completion and next launch
- Impact reports generated bi-weekly with cumulative lift calculations
- Experiments span at least 3 distinct product areas (not all testing the same surface)

## Instructions

### 1. Deploy the automated experiment pipeline

Run the `experiment-pipeline-automation` drill to build the always-on experiment system. This creates 4 n8n workflows:

**Experiment launcher (daily cron at 09:00 UTC):**
- Checks Attio for running experiments. If none, selects the top "next" hypothesis from the backlog.
- Creates the PostHog feature flag and experiment configuration automatically.
- Updates the Attio record with status "running", start date, and PostHog experiment ID.
- Sends a notification: "Experiment launched: [hypothesis] -- expected duration [X] days."

**Completion monitor (daily cron at 10:00 UTC):**
- Queries PostHog for running experiments' sample sizes.
- If an experiment reached its target sample size, marks it "ready-for-evaluation" in Attio.
- If a guardrail metric is breached (error rate, crash rate, or unsubscribe rate spikes above 2x baseline), auto-disables the feature flag, marks the experiment "reverted-guardrail", and sends an urgent notification.
- If an experiment exceeds 28 days without reaching sample size, marks it "underpowered" and notifies with options.

**Result collector (triggered by "ready-for-evaluation" status):**
- Pulls full experiment results from PostHog (control vs variant, primary and secondary metrics, confidence intervals, p-values).
- Stores raw results in the Attio experiment record.
- Logs an `experiment_completed` event in PostHog for long-term tracking.
- Sends a result summary to Slack for human review and decision.

**Auto-queue (triggered by experiment completion or revert):**
- Promotes the next highest-priority hypothesis from "queued" to "next".
- If the backlog is empty, sends a notification to run the `experiment-hypothesis-design` drill.

**Human action required:** At Scalable level, humans still make the adopt/revert/iterate decision after reviewing results. The agent collects and presents the data; the human decides. At Durable level, this decision is automated.

### 2. Scale hypothesis generation across product areas

Run the `experiment-hypothesis-design` drill every 2 weeks to replenish the backlog. Each run should target a different product area to ensure coverage:

- **Week 1-2:** Onboarding and activation experiments (time to value, onboarding completion, activation metric)
- **Week 3-4:** Conversion experiments (trial-to-paid, pricing page, checkout flow)
- **Week 5-6:** Feature adoption experiments (new feature discovery, feature engagement depth)
- **Week 7-8:** Retention experiments (re-engagement flows, churn prevention triggers, usage milestone rewards)

Maintain a minimum backlog of 5 queued hypotheses at all times. Each hypothesis must have: structured statement, expected lift, sample size calculation, and feasibility assessment.

### 3. Generate business impact reports

Run the `experiment-impact-reporting` drill bi-weekly. The report includes:

- **Experiment velocity:** experiments completed in the period, compared to the target (5/month)
- **Win rate:** percentage of experiments with adopted results (healthy: 25-40%)
- **Cumulative lift:** per-metric sum of all adopted experiment lifts (e.g., "activation rate improved +4.2pp from 3 adopted experiments")
- **Product area analysis:** which areas have the highest win rates and lifts, which are under-tested
- **Cycle time:** median days from hypothesis to completed experiment (target: under 21 days)
- **Testing ROI:** estimated revenue impact of cumulative lift vs. cost of the testing program

Distribute the report to stakeholders. Store in Attio for historical tracking.

### 4. Evaluate against threshold

After 2 months, measure against: >=10 experiments completed with measurable cumulative lift across 3+ product areas.

Evaluate:
- Total experiments completed (target: >=10)
- Product areas covered (target: >=3)
- Cumulative lift: is there a measurable, sustained improvement in at least one primary metric?
- Pipeline health: is the automation running reliably? (no stalls >3 days, no missed launches)

If PASS, proceed to Durable. If FAIL, diagnose:
- If <10 experiments: pipeline automation is stalling (fix n8n workflows), backlog is depleting faster than hypotheses are generated (increase hypothesis generation frequency), or experiments are taking too long (test higher-traffic surfaces or bolder changes)
- If 10+ experiments but no cumulative lift: win rate is too low (improve hypothesis quality with better data), effect sizes are too small (test bigger changes), or adopted changes are reverting (novelty effects -- extend post-adoption monitoring)

## Time Estimate

- 15 hours: build and test the 4 n8n automation workflows (launcher, monitor, collector, auto-queue)
- 8 hours: initial hypothesis generation across 4 product areas, populate backlog
- 25 hours: ongoing pipeline management, hypothesis review, adopt/revert decisions (~3 hours/week)
- 8 hours: bi-weekly impact reporting and stakeholder communication
- 4 hours: threshold evaluation, Durable preparation, documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, event tracking, funnels, dashboards | Free up to 1M events/mo; paid from $0.00005/event -- [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API (Claude Sonnet) | Hypothesis generation, result interpretation, impact report narratives | ~$5-15/mo at Scalable volume ($3/$15 per 1M input/output tokens) -- [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| n8n | Experiment pipeline automation (launcher, monitor, collector, auto-queue) | Self-hosted free; cloud from EUR20/mo -- [n8n.io/pricing](https://n8n.io/pricing) |

**Estimated play-specific cost: $25-50/mo** (PostHog likely still on free tier at this scale; n8n cloud + Anthropic API)

## Drills Referenced

- `experiment-pipeline-automation` -- automates the experiment lifecycle from backlog through launch, monitoring, result collection, and auto-queuing
- `experiment-impact-reporting` -- aggregates experiment results into business impact reports showing cumulative lift, win rates, and ROI
