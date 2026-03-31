---
name: personalized-onboarding-path-durable
description: >
  Adaptive Onboarding Paths — Durable Intelligence. Always-on AI agents
  autonomously monitor per-persona onboarding health, detect activation
  anomalies, generate improvement hypotheses, run A/B experiments, and
  auto-implement winners. Converges each persona path toward its local
  maximum.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "40 hours setup + continuous operation over 6 months"
outcome: "Activation rate sustained or improving >= 55% over 6 months via autonomous optimization, with experiment velocity >= 2 per persona per month"
kpis: ["Activation rate by persona (weekly trend)", "Experiment velocity (tests run per month)", "Experiment win rate (% of tests that produce >= 3pp improvement)", "Time to activation by persona (trend)", "Persona parity gap (best minus worst)", "Convergence status (consecutive sub-2% improvement experiments)"]
slug: "personalized-onboarding-path"
install: "npx gtm-skills add product/onboard/personalized-onboarding-path"
drills:
  - autonomous-optimization
  - onboarding-health-monitor
---

# Adaptive Onboarding Paths — Durable Intelligence

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Deploy always-on AI agents that autonomously optimize every persona's onboarding path. The agents monitor per-persona activation rates daily, detect when any persona's metrics plateau or drop, generate improvement hypotheses using Claude, design and run A/B experiments via PostHog feature flags, evaluate results, and auto-implement winners. Each persona path converges toward its local maximum — the best activation rate achievable given the current product, audience, and competitive landscape. Pass threshold: activation rate sustained or improving >= 55% over 6 months via autonomous optimization, with experiment velocity >= 2 per persona per month.

## Leading Indicators

- Daily anomaly detection workflow executes without errors for 7 consecutive days (automation is stable)
- First autonomous hypothesis generated within 48 hours of detecting an anomaly (the diagnosis loop works)
- First autonomous A/B experiment launched within 1 week of setup (the full loop completes end-to-end)
- Weekly optimization brief generated and posted to Slack by Monday 09:00 UTC (reporting is operational)
- Per-persona health dashboard shows all personas with populated trend data (monitoring is comprehensive)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill. This is the core loop that makes Durable fundamentally different from Scalable. Configure it specifically for this play:

**Phase 1 — Monitor (daily via n8n cron at 08:00 UTC):**

Build an n8n workflow that runs daily:

1. Use `posthog-anomaly-detection` to check each persona's primary KPIs: activation rate, tour completion rate, email click rate, time to activation
2. For each persona, compare the last 2 weeks against its 4-week rolling average
3. Classify each persona's health:
   - **Normal:** All metrics within +/-10% of rolling average
   - **Plateau:** Activation rate within +/-2% for 3+ consecutive weeks (optimization has stalled)
   - **Drop:** Activation rate declined > 15% from rolling average (something broke or changed)
   - **Spike:** Activation rate increased > 30% (investigate — is this a real improvement or a data artifact?)
4. If normal for all personas: log "healthy" status to Attio, no action needed
5. If any persona shows plateau, drop, or spike: trigger Phase 2 for that persona

**Phase 2 — Diagnose (triggered by anomaly detection):**

1. Gather context for the anomalous persona:
   - Pull the persona's current configuration from Attio: tour structure (step count, content), email sequence (subject lines, CTAs, timing), classification rules, stall-point nudge timing
   - Pull 8-week per-persona metric history from PostHog using `posthog-dashboards`
   - Pull the persona's funnel showing which step has the biggest new drop-off
2. Run `hypothesis-generation` with the anomaly data + context. Prompt structure:
   ```
   Persona: {persona_type}
   Anomaly: {classification} — {metric} changed from {baseline} to {current}
   Funnel drop-off: Step {N} ({step_name}) has the largest new decline
   Current tour: {step_count} steps, {content_summary}
   Current email: {email_count} emails, open rate {open_rate}%, click rate {click_rate}%
   Recent changes: {any product changes, traffic source shifts, or prior experiment results}

   Generate 3 ranked hypotheses for improving this persona's activation rate.
   For each hypothesis: predicted impact (pp improvement), risk level (low/medium/high),
   specific change to implement, and how to measure success.
   ```
3. Receive 3 ranked hypotheses. Store them in Attio as notes on the play record.
4. **Guardrail:** If the top hypothesis has risk = "high" (e.g., changes affect > 50% of that persona's traffic, or requires a product code change), send a Slack alert for human review and STOP. Do not auto-implement high-risk changes.
5. If risk = "low" or "medium": proceed to Phase 3 with the top-ranked hypothesis.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

1. Design the experiment for the anomalous persona:
   - Use `posthog-experiments` to create a feature flag splitting that persona's traffic: 50% control (current path), 50% variant (hypothesis change)
   - Implement the variant. Examples:
     - **Tour change hypothesis:** Create a new Intercom product tour variant for this persona using `intercom-product-tours`
     - **Email change hypothesis:** Create a new Loops email variant using `loops-sequences`
     - **Timing change hypothesis:** Adjust the n8n stall-nudge workflow timing for this persona
     - **Classification change hypothesis:** Update the n8n classification rules to re-route borderline users
2. Set experiment duration: minimum 7 days OR until 100+ users per variant, whichever is longer
3. Log the experiment start in Attio: hypothesis text, persona, start date, expected duration, success criteria
4. **Guardrail:** Maximum 1 active experiment per persona at a time. Never stack experiments on the same persona.

**Phase 4 — Evaluate (triggered by experiment completion):**

1. Pull experiment results from PostHog: activation rate for control vs variant, per the persona
2. Run `experiment-evaluation`:
   - **Adopt (significant improvement >= 3pp at 95% confidence):** Disable the feature flag, make the variant the new default for this persona. Log the change. Update the persona's configuration in Attio.
   - **Iterate (directional improvement but not significant):** Generate a new hypothesis that builds on the promising direction. Return to Phase 2.
   - **Revert (no improvement or negative):** Disable the variant, restore control. Log the failure with learnings. Return to Phase 1 monitoring.
   - **Extend (trending positive but insufficient sample):** Keep running for another period. Set an n8n reminder.
3. Store the full evaluation in Attio: decision, confidence interval, reasoning, net impact.
4. **Guardrail — revert threshold:** If the variant's activation rate drops > 20% below control at any point during the experiment, auto-revert immediately via the PostHog feature flag API. Do not wait for the experiment to complete.

**Phase 5 — Report (weekly via n8n cron, Monday 09:00 UTC):**

1. Aggregate all optimization activity for the week across all personas:
   - Anomalies detected (which personas, what type)
   - Hypotheses generated (which personas, top hypothesis for each)
   - Experiments running (which personas, current sample size, days remaining)
   - Experiments completed (which personas, outcome, net impact)
   - Changes adopted (which personas, what changed, measured improvement)
2. Calculate: net activation rate change from all adopted changes this week, per persona and overall
3. Generate a weekly optimization brief using Claude:
   ```
   # Onboarding Optimization Brief — Week of {date}

   ## Summary
   - Overall activation rate: {X}% (prev week: {Y}%, 4-week avg: {Z}%)
   - Experiments completed: {N} ({wins} wins, {losses} losses, {extends} extended)
   - Net improvement this week: {delta}pp

   ## Per-Persona Status
   | Persona | Activation | Trend | Health | Active Experiment | Last Change |
   |---------|-----------|-------|--------|-------------------|-------------|
   | {A}     | {rate}%   | {↑/↓/→} | {normal/plateau/drop} | {yes/no: description} | {date: what changed} |

   ## Convergence Status
   - Personas at local maximum: {list of personas where last 3 experiments produced < 2% improvement}
   - Personas still optimizing: {list of personas with active experiments or recent > 2% improvements}
   - Estimated distance from local maximum: {based on diminishing returns trend}

   ## Recommended Focus
   - {Prioritized list of what to test next, based on which persona has the most room to improve}
   ```
4. Post the brief to Slack and store in Attio as a note on the play record.

### 2. Deploy per-persona health monitoring

Run the `onboarding-health-monitor` drill. This provides the detailed monitoring layer that feeds into the autonomous optimization loop:

**Per-persona health dashboard in PostHog:**
- Activation rate by persona (weekly trend, 12-week window, target line at 55%)
- Time to activation by persona (distribution histogram — rightward shift = getting slower = problem)
- Tour completion rate by persona (weekly bar chart — a drop here causes downstream activation drops)
- Email sequence engagement by persona (open rate and click rate per persona, weekly)
- Persona classification distribution (pie chart — sudden shift means user mix changed or classification broke)
- Drop-off heatmap: table showing which tour step or email has highest abandonment per persona

**Anomaly thresholds per metric:**
| Metric | Warning | Critical |
|--------|---------|----------|
| Activation rate | 10-20% below 4-week average for 1 week | > 20% below OR below 55% for 2 weeks |
| Tour completion | 15-25% below average for 1 week | > 25% below OR below 40% absolute |
| Email open rate | 20-35% below average for 1 week | > 35% below OR below 15% absolute |
| Time to activation | 20-40% above median | > 40% above median |
| Persona distribution | Any persona drops > 50% of its usual share | Classification returning > 30% "default" |

**Daily monitoring workflow (n8n, 08:00 UTC):**
- Query PostHog for each persona's metrics from last 7 days
- Compare against 4-week rolling average
- Classify: normal, warning, critical
- Critical: immediate Slack alert with persona name, metric, current value, expected value, and suggested investigation
- Warning: log to Attio as observation
- Normal: log "healthy" status

**Weekly health report (n8n, Monday 09:00 UTC):**
- Per-persona breakdown: signups, activation rate, trend direction, tour completion, email CTR
- Anomalies detected this week
- Experiments in flight from autonomous optimization
- Cohort drift detection: has the profile of new signups changed?

**Cohort drift detection:**
- Weekly comparison of new signup cohort vs 4-week historical average on persona distribution, signup source, company size
- Significant drift (e.g., a persona jumps from 15% to 40% of signups) is flagged as a strategic change, not a path optimization problem. It requires updating paths for the growing persona, not fixing the declining one.

### 3. Configure guardrails and convergence detection

**Guardrails (enforced by the autonomous optimization loop):**
- **Rate limit:** Maximum 1 active experiment per persona. Maximum 4 experiments total across all personas at once.
- **Revert threshold:** If any persona's activation rate drops > 20% during an experiment, auto-revert immediately.
- **Human approval required for:** Budget changes > 20%, classification rule changes affecting > 50% of a persona's traffic, any high-risk hypothesis.
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing a new hypothesis on the same variable for that persona.
- **Monthly cap:** Maximum 4 experiments per persona per month. If all 4 fail, pause that persona's optimization and flag for human strategic review.

**Convergence detection:**
- Track each persona's experiment results over time. When a persona has 3 consecutive experiments producing < 2% improvement, that persona has reached its local maximum.
- At convergence for a persona:
  1. Reduce that persona's monitoring from daily anomaly checks to weekly
  2. Log convergence status in Attio
  3. Report: "Persona {X} has converged at {rate}% activation. Further gains require strategic changes (new product features, new audience segment, or path restructure) rather than tactical optimization."
- The play reaches overall convergence when all 5+ personas have converged. At that point, the optimization loop shifts to maintenance mode: weekly monitoring for anomalies only, no proactive experimentation.

### 4. Evaluate sustainability

This level runs continuously for 6 months. Monthly review checkpoints:

**Month 1:** Verify automation stability. All workflows execute without errors. At least 1 autonomous experiment completed end-to-end.
**Month 2:** Verify experimentation velocity. At least 2 experiments per persona completed. At least 1 winning experiment adopted.
**Month 3:** Verify sustained performance. Overall activation rate still >= 55%. No persona has regressed > 5pp from its Scalable-level baseline.
**Month 4-5:** Verify optimization impact. Total activation improvement from adopted experiments >= 3pp above Scalable-level baseline. Experiment velocity maintained.
**Month 6:** Final evaluation against threshold:

- **Activation rate sustained or improving >= 55%** over the full 6 months (check each month individually — no single month below 50%)
- **Experiment velocity >= 2 per persona per month** (averaged over 6 months)
- **At least 3 winning experiments adopted** across all personas
- **No persona regressed** more than 5pp from its Month 1 baseline for more than 2 consecutive weeks without autonomous intervention correcting it

**Human action required:** Review the monthly optimization brief. Confirm that autonomous changes align with product strategy. Flag any experiments that, while metrics-positive, conflict with brand positioning or user experience principles.

## Time Estimate

- 12 hours: Autonomous optimization loop setup (n8n workflows for all 5 phases, PostHog anomaly detection, Claude API integration)
- 8 hours: Health monitoring setup (PostHog dashboard, anomaly thresholds, daily/weekly monitoring workflows in n8n)
- 6 hours: Guardrails and convergence detection configuration
- 4 hours: End-to-end testing of the full loop (trigger an artificial anomaly, verify hypothesis generation, verify experiment creation)
- 10 hours: Monthly reviews and strategic oversight (2 hours/month x 5 months)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Per-persona dashboards, anomaly detection, experiments, feature flags | Usage-based: $0.00005/event above 1M free; experiments included — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | Persona-specific tours and in-app messages (modified by experiments) | Essential $29/seat/mo + Proactive Support Plus $99/mo — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Persona-specific email sequences (modified by experiments) | $49+/mo based on contacts — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Optimization loop orchestration (daily monitoring, experiment management, reporting) | Pro: €60/mo (10K executions); self-hosted: free — [n8n.io/pricing](https://n8n.io/pricing/) |
| Anthropic Claude API | Hypothesis generation and experiment evaluation | Haiku 3.5: $1/$5 per MTok (sufficient for hypothesis generation); ~$5-15/mo at 2 hypotheses/week — [claude.ai/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Attio | Experiment audit trail, persona configuration logging, optimization notes | Included in standard CRM plan — [attio.com/pricing](https://attio.com/pricing) |

**Estimated monthly cost at this level:** $250-550/mo (PostHog $0-50 event overage; Intercom $128-200; Loops $49+; n8n $60; Claude API $5-15; Attio standard plan)

## Drills Referenced

- `autonomous-optimization` — the always-on monitor-diagnose-experiment-evaluate-implement loop that autonomously finds each persona's local maximum activation rate. Runs daily monitoring, generates Claude-powered hypotheses on anomalies, creates PostHog experiments, evaluates results, and auto-implements winners. Produces weekly optimization briefs.
- `onboarding-health-monitor` — per-persona health monitoring with anomaly thresholds, daily automated checks, weekly structured reports, and cohort drift detection. Feeds anomaly data into the autonomous optimization loop for automated response.
