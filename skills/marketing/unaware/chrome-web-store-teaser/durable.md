---
name: chrome-web-store-teaser-durable
description: >
  Chrome Extension Teaser — Durable Intelligence. Always-on AI agents run the autonomous
  optimization loop: detect metric anomalies in CWS performance, generate hypotheses for
  listing and popup improvements, run A/B experiments, evaluate results, and auto-implement
  winners. Weekly optimization briefs. Converges when successive experiments yield <2% lift.
stage: "Marketing > Unaware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving install velocity and lead generation over 6 months via autonomous agent optimization; install-to-lead conversion rate at or above Scalable peak; agents detect and adapt to CWS algorithm changes, competitor moves, and seasonal patterns."
kpis: ["Store listing views", "Install rate", "Popup open rate", "Waitlist signups", "Install-to-lead conversion rate", "CWS search ranking position", "Weekly installs trend", "Experiment win rate"]
slug: "chrome-web-store-teaser"
install: "npx gtm-skills add marketing/unaware/chrome-web-store-teaser"
drills:
  - autonomous-optimization
  - chrome-store-performance-monitor
  - dashboard-builder
---

# Chrome Extension Teaser — Durable Intelligence

> **Stage:** Marketing > Unaware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Outcomes

The Chrome Web Store channel runs itself. AI agents continuously monitor extension performance, detect when install velocity or lead conversion changes, generate hypotheses for what to adjust (listing copy, popup UX, keyword targeting, screenshot selection), run controlled experiments, evaluate results, and auto-implement winners. The play sustains or exceeds Scalable-level performance over 6 months with minimal human intervention. The agents converge when successive experiments produce < 2% improvement, indicating the local maximum has been reached.

## Leading Indicators

- Autonomous optimization loop running: at least 1 experiment launched per month
- Weekly install velocity within 15% of 4-week rolling average (stable performance)
- No unaddressed anomalies older than 48 hours (monitor-to-diagnose latency)
- Experiment win rate above 30% (agents are generating viable hypotheses)
- Weekly optimization briefs delivered on schedule

## Instructions

### 1. Build the CWS performance dashboard

Run the `dashboard-builder` drill to create a comprehensive PostHog dashboard for this play:

| Panel | Metric | Visualization |
|-------|--------|---------------|
| Weekly installs | `extension_installed` per week, 12-week trend | Line chart with target line |
| Install-to-lead funnel | `extension_installed` > `popup_opened` > `waitlist_form_submitted` | Funnel chart, weekly |
| Listing conversion | Install rate (installs / listing visits) | Percentage, weekly trend |
| Lead quality | CWS leads that progress to demo or trial | Bar chart, monthly |
| Review health | Average rating + review count over time | Dual-axis chart |
| Search rankings | Position for top 3 keywords | Table, weekly snapshot |
| Experiment tracker | Active experiments, outcomes, cumulative lift | Table |
| Uninstall rate | 7-day uninstall rate as % of installs | Percentage, weekly trend |

Set threshold indicators on each panel using the winning metrics from Scalable level as the baseline.

### 2. Deploy the Chrome Store performance monitor

Run the `chrome-store-performance-monitor` drill to establish always-on monitoring:

- Configure daily anomaly detection for: install velocity, popup engagement rate, lead conversion rate, uninstall rate, review sentiment
- Anomaly classification: Normal (within +/-15% of 4-week average), Watch (+/-15-30%), Alert (>30% deviation)
- Build the daily n8n monitoring workflow:
  1. Fetch yesterday's metrics from PostHog
  2. Compare against 7-day and 28-day rolling averages
  3. Classify each metric
  4. Log to Attio
  5. Alert via Slack if any metric is in Alert state
- Build the weekly performance report workflow:
  1. Aggregate week's data
  2. Calculate: installs, leads, conversion rates, ranking changes
  3. Compare against previous 3 weeks
  4. Generate structured report with headline metric, conversion data, health indicators, and one specific recommendation
  5. Post to Slack and log in Attio

### 3. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for this play:

**Phase 1 — Monitor (daily via n8n):**
The `chrome-store-performance-monitor` feeds anomaly data into this phase. When the monitor classifies any metric as Alert or when a metric plateaus (< 2% change for 3+ weeks), Phase 2 triggers automatically.

**Phase 2 — Diagnose (triggered by anomaly):**
1. Gather context: current listing configuration (title, description, screenshots, keywords), popup variant in production, recent experiment history, competitor landscape from the Scalable-level competitor monitor
2. Pull 8-week metric history from PostHog
3. Run `hypothesis-generation` with the anomaly data + context. The agent generates 3 ranked hypotheses. Example hypotheses for this play:
   - "Install rate dropped because competitor X updated their listing with a similar title — change title to differentiate on [specific benefit]"
   - "Popup-to-lead conversion plateaued — test adding a 15-second product demo GIF above the waitlist form"
   - "Uninstall rate spiked after last update — the new feature has a bug or the permissions prompt changed"
4. Store hypotheses in Attio. If top hypothesis risk = "high" (e.g., requires changing permissions, major popup redesign), send Slack alert for human review and STOP. If risk = "low" or "medium", proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Design the experiment using PostHog feature flags:
   - For popup changes: feature flag splits users between current popup (control) and modified popup (variant)
   - For listing changes: no feature flag possible — publish the change and compare 2-week pre/post metrics
2. Implement the variant:
   - Popup copy/UX changes: update `popup.html` behind a feature flag, publish extension update
   - Listing copy changes: update via Chrome Web Store API
   - Screenshot changes: upload new screenshots via CWS Developer Dashboard
3. Set experiment duration: minimum 14 days or 100+ samples per variant for popup tests; minimum 14 days for listing tests
4. Log experiment in Attio: hypothesis, start date, expected duration, success metric, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog (popup tests) or CWS Developer Dashboard (listing tests)
2. Run `experiment-evaluation`:
   - **Adopt**: Variant outperforms control with 95% confidence and practical significance (> 5% relative lift). Make the variant permanent. Log the change.
   - **Iterate**: Results inconclusive or marginal. Generate a refined hypothesis. Return to Phase 2.
   - **Revert**: Variant underperforms control. Disable the variant. Log the failure with reasoning. Wait 7 days before testing the same variable again.
   - **Extend**: Insufficient data. Continue the experiment for another period.
3. Store full evaluation in Attio: decision, confidence level, reasoning, metric impact

**Phase 5 — Report (weekly via n8n):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes
3. Generate weekly optimization brief:
   - What changed and why
   - Net impact on installs, leads, and conversion rates
   - Current distance from estimated local maximum (based on diminishing returns curve)
   - Recommended focus for next week
4. Post to Slack and store in Attio

### 4. Guardrails

These guardrails are enforced automatically by the optimization loop:

- **One experiment at a time**: Never run concurrent experiments on this extension. Queue hypotheses.
- **Auto-revert**: If installs drop > 30% or uninstalls spike > 2x during an experiment, revert immediately.
- **Human approval required for**: Permission changes, adding new host_permissions, major feature changes, any change flagged as "high risk" by hypothesis generation.
- **Cooldown**: After a revert, wait 7 days before testing the same variable.
- **Monthly cap**: Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review.
- **Never optimize unmeasured variables**: If a metric does not have PostHog tracking, fix tracking first before experimenting.

### 5. Detect convergence

The optimization loop should detect when the play has reached its local maximum:

- Track the cumulative lift from all adopted experiments over trailing 90 days
- If 3 consecutive experiments produce < 2% improvement each, the play has converged
- At convergence:
  1. Reduce monitoring frequency from daily to weekly
  2. Reduce experiment cadence to 1 per month (maintenance mode)
  3. Report: "Chrome Web Store Teaser has reached local maximum. Current performance: [X installs/week, Y% conversion, Z leads/week]. Further gains require strategic changes: new extension features, additional distribution channels, or product changes."
- Monitor continues at weekly cadence to detect external disruptions (CWS algorithm changes, new competitors, seasonal shifts) that could push performance below the converged baseline.

## Time Estimate

- 20 hours: Dashboard build + performance monitor setup + n8n workflows
- 10 hours: Autonomous optimization loop configuration and initial test
- 120 hours: Ongoing optimization loop execution over 6 months (~5 hours/week agent compute)
- 30 hours: Experiment implementation (popup updates, listing changes, extension updates)
- 20 hours: Monthly reviews, strategic adjustments, convergence analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Chrome Web Store | Extension hosting and distribution | $5 one-time (already paid) |
| PostHog | Event tracking, dashboards, feature flags, experiments, anomaly detection | Free tier: 1M events + 1M feature flag requests/month; paid: ~$0.00005/event over free tier ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Lead capture, nurture, transactional emails | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Automation: daily monitor, weekly reports, optimization loop scheduling | Self-hosted free; Cloud Pro $60/mo for 10K executions ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | CRM: lead tracking, experiment logs, competitive intel | Free tier available ([attio.com/pricing](https://attio.com/pricing)) |
| Anthropic API | Claude for hypothesis generation and experiment evaluation | ~$15-30/mo estimated for weekly optimization cycles ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |

**Estimated monthly cost at Durable level: $125-200/mo** (n8n Cloud Pro + Loops Starter + Anthropic API; PostHog and Attio within free tiers at this volume)

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: monitor > diagnose > experiment > evaluate > implement. Runs always-on, producing weekly optimization briefs and auto-implementing winning experiments.
- `chrome-store-performance-monitor` — daily anomaly detection and weekly performance reports specific to Chrome Web Store metrics. Feeds data into the autonomous optimization loop.
- `dashboard-builder` — builds the PostHog dashboard for real-time visibility into all CWS metrics and experiment results.
