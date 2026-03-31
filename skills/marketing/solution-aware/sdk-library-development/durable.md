---
name: sdk-library-development-durable
description: >
  SDK & Library Development — Durable Intelligence. Always-on AI agents autonomously
  optimize SDK metadata, README CTAs, release timing, and language prioritization.
  The autonomous-optimization loop detects download anomalies, generates improvement
  hypotheses, runs experiments, and auto-implements winners.
stage: "Marketing > Solution Aware"
motion: "Directories & Marketplaces"
channels: "Communities, Product"
level: "Durable Intelligence"
time: "20 hours setup + continuous autonomous operation over 12 months"
outcome: "Sustained download growth (>=10% QoQ) and >=50 developer signups/month from SDKs over 12 months via autonomous optimization"
kpis: ["Quarter-over-quarter download growth rate", "Developer signups/month from SDKs", "Autonomous experiment win rate", "SDK-sourced revenue attribution", "Time to convergence per optimization variable", "Cost efficiency trend (signups per engineering hour)"]
slug: "sdk-library-development"
install: "npx gtm-skills add marketing/solution-aware/sdk-library-development"
drills:
  - autonomous-optimization
  - sdk-adoption-monitor
---
# SDK & Library Development — Durable Intelligence

> **Stage:** Marketing -> Solution Aware | **Motion:** Directories & Marketplaces | **Channels:** Communities, Product

## Outcomes
An always-on AI agent system that monitors SDK adoption across all registries, detects when metrics plateau or drop, autonomously generates and tests improvement hypotheses, and auto-implements winners. The system finds and maintains the local maximum of SDK-driven developer acquisition. Weekly optimization briefs report what changed, why, and what the net impact was. The system converges when successive experiments produce <2% improvement -- meaning the SDK channel is fully optimized within current market conditions.

## Leading Indicators
- The autonomous optimization loop completes its first full cycle (detect -> hypothesize -> experiment -> evaluate -> implement) within the first 2 weeks
- At least 1 experiment per month produces a statistically significant improvement
- Weekly optimization briefs are generated and posted automatically with no human intervention
- Anomaly detection fires and self-corrects within 48 hours of a metric deviation
- SDK-sourced developer LTV exceeds the product average by >=20%

## Instructions

### 1. Configure the autonomous optimization loop for SDKs
Run the `autonomous-optimization` drill, configured for SDK-specific variables:

**Phase 1 -- Monitor (daily via n8n cron):**
Use the PostHog tracking from Baseline/Scalable to check:
- Download trends per registry (compare last 2 weeks to 4-week rolling average)
- README CTA click-through rates per SDK
- Signup conversion rates per registry
- Developer activation rates per language
- Classify each metric: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)

**Phase 2 -- Diagnose (triggered by anomaly):**
When an anomaly is detected, the agent:
1. Pulls SDK configuration from Attio: current README copy, CTA text, keyword set, release cadence, registry metadata
2. Pulls 8-week metric history from PostHog
3. Runs `hypothesis-generation` with anomaly data + context
4. Receives 3 ranked hypotheses. Examples:
   - "npm downloads dropped because a competitor published a similar SDK last week -- update README to add a comparison section"
   - "PyPI CTA click rate plateaued -- test a more specific CTA: 'Get your API key' vs current 'Try free'"
   - "Go SDK activation rate dropped after v1.2.0 release -- check for breaking change in the upgrade path"

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
1. Design the experiment using PostHog feature flags
2. For README experiments: create variant README content, push to a branch, use a redirect or flag-based routing for docs traffic
3. For metadata experiments: update registry keywords/description on the variant
4. Minimum duration: 14 days or 200+ samples per variant, whichever is longer
5. Log experiment in Attio

**Phase 4 -- Evaluate (triggered by experiment completion):**
1. Run `experiment-evaluation` on control vs variant
2. Decision: Adopt (implement winner), Iterate (new hypothesis building on result), Revert (restore control), or Extend (keep running)
3. If Adopt: update the live SDK README/metadata with the winning variant
4. Store full evaluation in Attio

**Phase 5 -- Report (weekly via n8n cron):**
Generate a weekly optimization brief:
- Anomalies detected this week
- Experiments in progress (which SDK, which variable, current sample size vs target)
- Experiments completed (result, confidence, decision)
- Net impact: aggregate metric change from all adopted changes
- Distance from estimated local maximum
- Convergence status: how many consecutive experiments produced <2% improvement?

### 2. Build the SDK adoption monitoring system
Run the `sdk-adoption-monitor` drill to:
- Build a comprehensive PostHog dashboard with download trends, per-SDK performance, funnels, developer activation, and competitive landscape
- Configure anomaly detection for 6 key metric categories (download drops, CTA conversion drops, activation drops, new competitors, staleness, breaking changes)
- Set up weekly competitive tracking via Clay across all registries
- Instrument deeper activation signals: first API call, error rates by SDK version, version adoption curves, SDK-sourced paid conversions
- Generate weekly SDK health reports with competitive intelligence

### 3. Define the optimization variable space
The agent autonomously experiments on these variables (one at a time per SDK):

| Variable | Experiment Type | Measurement |
|----------|----------------|-------------|
| README CTA copy | A/B test on docs landing page | CTA click-through rate |
| README CTA placement | A/B test (after quick start vs bottom of page) | CTA click-through rate |
| Registry description | Direct update, measure before/after | Search result click rate |
| Registry keywords/topics | Direct update, measure before/after | Download trend change |
| Release cadence | Compare weekly vs biweekly vs monthly release cycles | Download trend, star velocity |
| Quick start complexity | A/B test (3-line vs 10-line example) | Time to first API call |
| Docs page structure | A/B test (unified vs per-language) | Signup conversion rate |
| Community seeding | Test different subreddits/forums for announcements | Referral traffic from each source |

### 4. Set guardrails
Apply the `autonomous-optimization` drill guardrails, plus SDK-specific rules:
- **Never break the install command:** Any README experiment must preserve a working `npm install` / `pip install` command at the top
- **Never publish a broken SDK:** All experiments that involve code changes must pass the shared test suite before deployment
- **Rate limit registry metadata changes:** Maximum 1 keyword/description update per SDK per month (registries may flag frequent changes)
- **Human approval required for:** New language SDKs, major version bumps (breaking changes), deprecating an SDK

### 5. Track SDK-sourced revenue attribution
Connect SDK adoption data to revenue:
1. In Attio, create a report: deals where the primary contact has `first_touch_channel = sdk`
2. Calculate: SDK-sourced pipeline value, win rate, average deal size, time to close
3. Compare SDK-sourced deals to other channels
4. Feed this data back into the optimization loop: languages that produce higher-LTV developers get more optimization investment

### 6. Detect convergence and adapt
The optimization loop runs indefinitely. When convergence is detected (<2% improvement for 3 consecutive experiments on the same variable):
1. Mark that variable as optimized for that SDK
2. Move to the next variable in the optimization space
3. When all variables for an SDK are converged: reduce monitoring frequency from daily to weekly
4. Report: "The {language} SDK has reached its local maximum. Current performance: {metrics}. Further gains require strategic changes (new API features, new language support, or market shift) rather than tactical optimization."

If market conditions change (new competitor, API update, developer ecosystem shift), the monitoring system detects the anomaly and restarts the optimization loop.

## Time Estimate
- Autonomous optimization loop configuration: 6 hours
- SDK adoption monitor setup: 6 hours
- Optimization variable space definition: 2 hours
- Guardrails and approval workflows: 2 hours
- Revenue attribution pipeline: 2 hours
- Initial audit of existing SDKs: 2 hours
- Ongoing: autonomous operation with weekly human review of optimization briefs (1 hour/week)

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| GitHub | SDK repos, CI/CD, feature branches for experiments | Free for public repos |
| npm / PyPI / crates.io / registries | Package distribution | Free to publish |
| PostHog | Dashboards, funnels, experiments, anomaly detection | Free up to 1M events/mo; experiments included (https://posthog.com/pricing) |
| n8n | Optimization loop scheduling, download collection, reporting | Free self-hosted or from EUR 20/mo cloud (https://n8n.io/pricing) |
| Anthropic API | Hypothesis generation and experiment evaluation via Claude | Usage-based, ~$3/1M input tokens (https://www.anthropic.com/pricing) |
| Clay | Competitive SDK landscape monitoring | From $149/mo (https://www.clay.com/pricing) |
| Attio | Lead tracking, experiment logging, revenue attribution | Free for small teams (https://attio.com/pricing) |

## Drills Referenced
- `autonomous-optimization` -- the core always-on loop that detects metric anomalies, generates improvement hypotheses, runs A/B experiments, evaluates results, and auto-implements winners. Produces weekly optimization briefs. Converges when successive experiments produce <2% improvement.
- `sdk-adoption-monitor` -- continuous monitoring of SDK adoption metrics across all registries with anomaly detection, competitive tracking, developer activation instrumentation, and weekly health reports
