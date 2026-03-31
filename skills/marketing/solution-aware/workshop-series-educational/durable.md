---
name: workshop-series-educational-durable
description: >
  Workshop Series — Durable Intelligence. Always-on AI agents continuously
  monitor the workshop series funnel, detect metric anomalies, generate
  improvement hypotheses, run A/B experiments on topic selection, difficulty
  calibration, exercise design, promotion, and nurture sequences, then
  auto-implement winners. Weekly optimization briefs track progress toward the
  local maximum. Converges when successive experiments produce less than 2%
  improvement.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Content"
level: "Durable Intelligence"
time: "180 hours over 6 months"
outcome: "Sustained workshop attendance and >=45 qualified leads/quarter over 6 months via AI-driven optimization of topics, exercises, promotion, and nurture sequences. Agents detect degradation, diagnose causes, experiment, and auto-implement improvements. Convergence when 3 consecutive experiments produce <2% improvement."
kpis: ["Registrations per workshop (vs rolling average)", "Show rate trend", "Exercise completion trend", "Qualified leads per workshop trend", "Cost per qualified lead trend", "Experiment win rate", "Time to convergence"]
slug: "workshop-series-educational"
install: "npx gtm-skills add marketing/solution-aware/workshop-series-educational"
drills:
  - autonomous-optimization
  - workshop-performance-monitor
---

# Workshop Series — Durable Intelligence

> **Stage:** Marketing > SolutionAware | **Motion:** MicroEvents | **Channels:** Events, Content

## Outcomes

- Maintain or improve workshop series performance over 6 months without manual optimization effort
- Detect and respond to metric degradation (topic fatigue, exercise difficulty miscalibration, show rate decline, nurture effectiveness drop) before they become critical
- Continuously experiment on every lever: topic selection, difficulty level, exercise format, promotion channel mix, email copy, event timing, nurture sequences, CTA variants
- Find the local maximum -- the best achievable performance given your market, audience, and competitive landscape
- Generate weekly optimization briefs that summarize what changed, why, and what to try next
- Converge: when 3 consecutive experiments produce <2% improvement, the play is optimized

## Leading Indicators

- Anomaly detection fires within 24 hours of any metric moving >15% from the 4-event rolling average
- At least 1 experiment running at all times (the loop never idles until convergence)
- Experiment win rate >30% (not every experiment wins, but enough do to drive improvement)
- Weekly optimization briefs generated on schedule with actionable recommendations
- No metric declines for 3+ consecutive workshops without an experiment addressing it

## Instructions

### 1. Deploy continuous workshop funnel monitoring

Run the `workshop-performance-monitor` drill to build the always-on monitoring layer:

- **Post-event automated checks**: After each workshop, the agent runs immediate health checks -- show rate vs target, exercise completion rate vs target, exercise participation depth, and nurture launch verification. Alerts fire if any metric falls below critical thresholds (show rate <25%, exercise participation <30%).
- **Rolling trend analysis**: Weekly n8n cron compares the last workshop's metrics against the 4-event rolling average. If any metric declines >15%, it flags for investigation and triggers the optimization loop.
- **Workshop post-mortems**: 14 days after each workshop (when nurture window closes), auto-generate a structured post-mortem: metrics vs targets, exercise analysis (which exercises had highest completion, which caused the most help requests), what worked, what needs attention, and recommendations.
- **Monthly series reports**: Aggregate all workshops for the month into a series health report: registration trends, show rate trends, exercise completion trends, pipeline generated, cost per qualified lead, and overall series health rating (GREEN/YELLOW/RED).

The monitoring outputs feed directly into the autonomous optimization loop.

### 2. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the workshop series:

**Phase 1 -- Monitor (runs daily via n8n cron):**
- Pull the workshop series KPIs from PostHog using anomaly detection
- Compare the last 2 workshops' metrics against the 4-event rolling average
- Classify each metric: normal (within +/-10%), plateau (+/-2% for 3+ events), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 -- Diagnose (triggered by anomaly):**
- Gather the current series configuration from Attio: active topic category, difficulty level, exercise format, promotion channel mix, email copy variants, event timing, prep sequence structure, nurture sequence structure
- Pull 8-event metric history from PostHog
- Run hypothesis generation with anomaly data + configuration context
- Receive 3 ranked hypotheses. Examples of workshop-specific hypotheses:
  - "Registration decline is caused by topic fatigue -- the last 3 workshops covered similar Python-related skills. Hypothesis: switching to a data infrastructure topic will increase registrations by 20%."
  - "Exercise completion dropped because the intermediate exercises assume prior knowledge that 40% of registrants lack. Hypothesis: adding a 5-minute prerequisite check at workshop start will increase completion by 15%."
  - "Show rate dropped because Friday 2pm competes with end-of-week obligations. Hypothesis: moving to Tuesday 11am will increase show rate by 10 percentage points."
  - "Nurture reply rate declining because Tier 1 emails are generic. Hypothesis: referencing the specific exercise each attendee completed will increase reply rate by 20%."
  - "Qualified lead conversion dropped because the CTA asks for a generic demo instead of a follow-up review session. Hypothesis: offering a 1-on-1 exercise review will increase conversion by 25%."
- If top hypothesis has risk = "high" (e.g., changing the core workshop format from hands-on to lecture), send Slack alert for human approval. Otherwise, proceed.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
- Design the experiment using PostHog feature flags where applicable
- Implement the variant. Examples:
  - Topic test: Run the next 2 workshops with a new topic category, compare against the previous 2 workshops' registration and conversion rates
  - Difficulty test: Offer the same topic at two difficulty levels in successive weeks, compare exercise completion and pipeline conversion
  - Exercise format test: Run alternate workshops with guided vs open-ended exercises, compare engagement and follow-up conversion
  - Promotion test: Split the invite list and send variant A (current subject line) and variant B (new subject line) for the same workshop
  - Nurture test: Route 50% of Tier 1 attendees into a variant nurture sequence with exercise-specific references, 50% into the current sequence
  - Prep sequence test: Send variant prep emails with video walkthroughs vs text-only instructions, compare show rate and exercise readiness
- Set experiment duration: minimum 2 workshops or 4 weeks, whichever is longer
- Log experiment start in Attio with hypothesis, variants, success criteria, and expected duration

**Phase 4 -- Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run experiment evaluation: statistical significance, practical significance, and secondary metric impact
- Decision:
  - **Adopt**: Winner improves primary metric with 95% confidence. Update the series configuration. Log the change.
  - **Iterate**: Promising direction but not conclusive. Refine the hypothesis and re-run.
  - **Revert**: Variant performed worse. Restore the control. Log the failure and the learning.
  - **Extend**: Insufficient data. Run for 2 more workshops.

**Phase 5 -- Report (weekly via n8n cron):**
- Generate weekly optimization brief:
  - Anomalies detected this week
  - Experiments in progress (status, preliminary data)
  - Experiments completed (decisions, impact)
  - Net metric change from adopted experiments
  - Distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

### 3. Configure workshop-specific guardrails

The `autonomous-optimization` drill has standard guardrails. Add these workshop-specific constraints:

- **Topic diversity guard**: Never run the same topic category more than 2 workshops in a row, even if it performs well. Audience fatigue is real. Alternate between 3+ topic categories.
- **Difficulty progression guard**: Do not skip difficulty levels. If an audience has only done beginner workshops, do not jump to advanced. Offer intermediate first.
- **Exercise stability guard**: Do not change the exercise format more than once per month. Attendees build expectations about the hands-on experience.
- **Facilitator coordination guard**: Any experiment that requires a guest facilitator change must be planned 3+ weeks in advance. Facilitators are humans, not variables.
- **Promotion budget guard**: Never increase paid promotion spend by more than 50% per workshop without human approval.
- **List fatigue guard**: Track unsubscribe rate on workshop invite emails. If it exceeds 1% on any send, pause and review targeting.
- **Maximum 1 active experiment per workshop**: Never test multiple variables on the same workshop. One change at a time for clean attribution.
- **Exercise quality guard**: If exercise completion drops below 40% on any workshop, auto-flag for immediate curriculum review. Do not run another workshop on that topic until the exercise is fixed.

### 4. Build the convergence detection system

The optimization loop should detect when the series has reached its local maximum:

- Track the percentage improvement from each adopted experiment
- When 3 consecutive experiments produce <2% improvement on the primary metric (qualified leads per workshop):
  1. The series is converging -- most tactical levers have been optimized
  2. Reduce monitoring frequency from post-event to weekly
  3. Reduce experimentation frequency to 1 experiment per month (maintenance mode)
  4. Generate a convergence report: "This workshop series is optimized at [current metrics]. The best-performing configuration is [topic category, difficulty level, exercise format, time slot, promotion mix, prep sequence, nurture sequence]. Further improvement requires strategic changes: new audience segments, product changes, or market shifts."

**Human action required:** At convergence, review the report. Decide whether to:
- Accept the local maximum and keep the series running in maintenance mode
- Reset by targeting a new audience segment or entering a new market
- Invest in a strategic change (e.g., in-person workshops, multi-session courses, certification programs) that shifts the performance ceiling
- Expand the topic backlog into adjacent skill areas to attract new audience segments

### 5. Sustain the series over 6 months

Over a 6-month Durable run, the agent:

- Manages a 12-18 workshop series with automated ops
- Runs 8-16 experiments across all workshop variables
- Generates 24+ weekly optimization briefs
- Produces monthly series health reports
- Detects and responds to seasonal patterns (holiday dips, end-of-quarter busy periods, summer slowdowns)
- Refreshes the topic backlog quarterly based on new ICP research, audience feedback, and exercise completion data
- Identifies when the workshop audience is saturating (repeat attendees > new attendees) and recommends audience expansion strategies
- Monitors exercise difficulty calibration and recommends curriculum adjustments when completion rates drift
- Tracks skill progression across the attendee base: how many beginners graduate to intermediate, how many become customers

The play is durable when the agent can maintain qualified leads per workshop above the Scalable baseline (50 leads / 3 months) without human optimization effort.

## Time Estimate

- Monitoring setup (PostHog dashboards, n8n cron jobs, alert configuration): 8 hours
- Autonomous optimization loop configuration: 6 hours
- Guardrail and convergence detection setup: 4 hours
- Per-workshop agent-managed effort (promotion, prep, nurture, analysis): 3 hours x 15 workshops = 45 hours
- Per-workshop human effort (curriculum prep + content delivery): 2 hours x 15 workshops = 30 hours
- Experiment design and implementation: 4 hours x 12 experiments = 48 hours
- Content repurposing (clips, tutorials, templates): 1 hour x 15 workshops = 15 hours
- Weekly brief review and strategic decisions: 1 hour x 24 weeks = 24 hours
- Monthly series report review: 2 hours x 6 months = 12 hours
- Quarterly topic refresh and strategic review: 6 hours x 2 = 12 hours
- **Total: ~180 hours over 6 months** (split: ~120 hours agent, ~60 hours human)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Riverside | Workshop recording + production | $29/mo Pro (4K, 15hr transcription) -- [riverside.com/pricing](https://riverside.com/pricing) |
| Loops | Email invites, prep, reminders, nurture | $49/mo (up to 5,000 contacts) -- [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Event tracking, funnels, experiments, anomaly detection | Free tier: 1M events/mo -- [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM, workshop lists, deal tracking, reporting | $29/user/mo Plus -- [attio.com](https://attio.com) |
| n8n | Monitoring crons, optimization loop, series automation | Self-hosted free or Cloud Pro EUR60/mo -- [n8n.io/pricing](https://n8n.io/pricing) |
| Clay | Prospect sourcing per workshop | $185/mo Launch (2,500 credits) -- [clay.com/pricing](https://www.clay.com/pricing) |
| Descript | Recording clips + content repurposing | $24/mo Hobbyist -- [descript.com/pricing](https://www.descript.com/pricing) |
| Loom | Personalized follow-up clips | $12.50/mo Business -- [loom.com/pricing](https://www.loom.com/pricing) |
| Cal.com | Meeting booking CTA | Free tier -- [cal.com/pricing](https://cal.com/pricing) |
| Anthropic API | Hypothesis generation + evaluation (Claude Sonnet) | Usage-based ~$15-30/mo for this play -- [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost at Durable: $360-600/mo** (all tools above + Anthropic API usage)

## Drills Referenced

- `autonomous-optimization` -- the core always-on loop: monitor metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, and generate weekly optimization briefs
- `workshop-performance-monitor` -- continuous monitoring of workshop-specific signals (exercise completion, engagement depth, skill progression), post-event post-mortems, and monthly series health reports that feed data into the optimization loop
