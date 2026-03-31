---
name: trade-show-presence-durable
description: >
  Trade Show Presence — Durable Intelligence. Always-on AI agents continuously
  monitor the trade show motion's full funnel, detect metric anomalies across
  shows, generate improvement hypotheses on show selection, booth execution,
  nurture sequences, and content strategy, run A/B experiments, and
  auto-implement winners. Weekly optimization briefs track progress toward
  the local maximum. Converges when successive experiments produce less than
  2% improvement.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Durable Intelligence"
time: "200 hours over 12 months"
outcome: "Sustained or improving trade show ROI over 12 months. >=100 qualified leads/quarter. Agents detect degradation, diagnose causes, experiment, and auto-implement improvements. Convergence when 3 consecutive experiments produce <2% improvement."
kpis: ["Qualified leads per show (vs rolling average)", "Cost per meeting trend", "Nurture conversion rate trend", "Pipeline per dollar spent", "Experiment win rate", "Time to convergence"]
slug: "trade-show-presence"
install: "npx gtm-skills add marketing/solution-aware/trade-show-presence"
drills:
  - autonomous-optimization
  - trade-show-performance-monitor
---

# Trade Show Presence — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Maintain or improve trade show ROI over 12 months without manual optimization effort
- Detect and respond to metric degradation (audience saturation, nurture fatigue, cost inflation, competitive pressure) before they become critical
- Continuously experiment on every lever: show selection, booth messaging, demo approach, pre-show outreach, nurture sequences, content strategy, follow-up timing
- Find the local maximum — the best achievable performance given your market, show circuit, and competitive landscape
- Generate weekly optimization briefs that summarize what changed, why, and what to try next
- Converge: when 3 consecutive experiments produce <2% improvement, the motion is optimized

## Leading Indicators

- Anomaly detection fires within 48 hours of any show-level metric deviating >15% from the 4-show rolling average
- At least 1 experiment running at all times (the loop never idles until convergence)
- Experiment win rate >30% (enough experiments win to drive sustained improvement)
- Weekly optimization briefs generated on schedule with actionable recommendations
- No metric declines for 2+ consecutive shows without an experiment addressing it
- Show selection intelligence improves: predicted ROI correlates within 25% of actual ROI

## Instructions

### 1. Deploy continuous trade show funnel monitoring

Run the `trade-show-performance-monitor` drill to build the always-on monitoring layer:

- **Post-show automated health checks**: After each show, the agent runs immediate health checks within 48 hours: booth conversation volume vs target, demo rate vs target, Tier 1 lead volume vs target, and on-site meeting bookings vs target. Alerts fire if any metric falls below critical thresholds (demo rate <15%, Tier 1 leads <5).
- **Nurture window monitoring**: During the 30-day post-show nurture window, the agent tracks daily: emails sent, opens, replies, meetings booked from nurture. If Tier 2 reply rate drops below 5% at the midpoint (day 15), flag for sequence review.
- **Rolling trend analysis**: After each show's 30-day nurture window closes, compare the show's full-funnel metrics against the 4-show rolling average. If any metric declines >15%, flag for investigation and trigger the optimization loop.
- **Post-show post-mortems**: 30 days after each show (when the nurture window closes), auto-generate a structured post-mortem: metrics vs targets, what worked, what needs attention, competitive observations, and specific recommendations for the next show.
- **Quarterly motion reports**: Aggregate all shows for the quarter. Compare: which shows produced the best ROI? How does the trade show motion compare to outbound, paid, and content in pipeline per dollar? Generate strategic recommendations: shows to continue, shows to drop, new shows to evaluate, budget reallocation.

The monitoring outputs feed directly into the autonomous optimization loop.

### 2. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the trade show motion:

**Phase 1 — Monitor (runs weekly via n8n cron + post-show triggers):**
- Pull the trade show motion's primary KPIs from PostHog using anomaly detection
- Compare the latest show's metrics against the 4-show rolling average
- Classify each metric: normal (within +/-10%), plateau (+/-2% for 3+ shows), drop (>15% decline), spike (>30% increase)
- If anomaly detected, trigger Phase 2
- Between shows: monitor nurture sequence metrics weekly for active sequences

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather current configuration from Attio: active show calendar, booth messaging, demo paths, pre-show outreach templates, nurture sequences, content strategy
- Pull 8-show metric history from PostHog (approximately 6-8 months of data)
- Run hypothesis generation with anomaly data + configuration context
- Receive 3 ranked hypotheses. Examples of trade-show-specific hypotheses:
  - "Qualified lead rate dropped at the last 2 shows because we're attending the same circuit and encountering repeat attendees. Hypothesis: adding 2 new shows in adjacent verticals will increase net-new qualified leads by 25%."
  - "Tier 2 nurture reply rate declined from 12% to 6% over the last 3 shows. Hypothesis: nurture sequence fatigue — the same email templates have been used for 4 months. Refreshing copy and switching from resource-led to question-led approach will recover reply rates."
  - "Cost per meeting increased 40% because booth costs at {show X} rose while lead volume stayed flat. Hypothesis: downgrading from a 20x20 to a 10x10 booth at this show will reduce cost per meeting by 30% without significant lead volume loss."
  - "Pre-show outreach acceptance rate dropped from 25% to 10%. Hypothesis: subject line fatigue — testing a new subject line formula referencing a specific show session will improve open rates."
- If top hypothesis has risk = "high" (e.g., dropping a historically good show, changing booth size significantly), send Slack alert for human approval. Otherwise, proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment. Because trade shows are discrete events (not continuous traffic), experiments often span 2 shows:
  - **Show selection test**: Add a new show to the calendar, run with standard operations, compare metrics to established shows
  - **Booth messaging test**: Change the booth hook for the next show, compare demo-to-conversation rate vs the previous show at the same event (year-over-year) or vs the 4-show average
  - **Pre-show outreach test**: A/B split the target list for the next show, test two subject lines or messaging approaches
  - **Nurture sequence test**: Split leads from the next show into control (current sequence) and variant (new sequence). Use PostHog feature flags to route.
  - **Demo path test**: Track a new demo path at the next show (e.g., interactive vs. presentation style), compare meeting conversion rate
- Set experiment duration: minimum 2 shows or 8 weeks, whichever is longer
- Log experiment start in Attio: hypothesis, variants, success criteria, expected completion date

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run experiment evaluation: statistical significance (where sample sizes allow), practical significance, and secondary metric impact
- Decision:
  - **Adopt**: Winner improves the primary metric by >=5% with reasonable confidence. Update the playbook configuration. Log the change. Move to Phase 5.
  - **Iterate**: Promising direction but results are inconclusive (trade shows have inherently small sample sizes). Refine the hypothesis and test for 2 more shows.
  - **Revert**: Variant performed worse. Restore the control. Log the failure and the learning.
  - **Extend**: Insufficient data. Run for 2 more shows.
- Store the full evaluation in Attio: decision, confidence, reasoning, secondary metric impact

**Phase 5 — Report (weekly via n8n cron):**
- Generate weekly optimization brief:
  - Anomalies detected since last brief
  - Experiments in progress: status, preliminary data
  - Experiments completed: decisions and impact
  - Net metric change from all adopted experiments
  - Current distance from estimated local maximum
  - Upcoming shows and expected performance
  - Recommended focus for next week
- Post to Slack and store in Attio

### 3. Configure trade-show-specific guardrails

The `autonomous-optimization` drill has standard guardrails. Add these trade-show-specific constraints:

- **Show commitment guard**: Never cancel a confirmed show booking less than 6 weeks out. Cancellation fees and relationship damage outweigh most optimization gains.
- **Budget stability guard**: Never increase per-show investment by more than 30% without human approval. Booth upgrades, additional staff, and premium booth locations can escalate costs quickly.
- **Circuit consistency guard**: Maintain attendance at your top 3 performing shows for at least 2 consecutive years before considering removal. Annual attendees expect to see you, and absence signals weakness to competitors.
- **Nurture list fatigue guard**: Track unsubscribe rate on trade show nurture sequences. If unsubscribe rate exceeds 1.5% on any sequence, pause and review targeting and copy. Leads from in-person interactions tolerate less email than opt-in subscribers.
- **Maximum 1 active experiment per show**: Never test multiple variables at the same show. Clean attribution requires one change at a time. The exception: pre-show outreach A/B tests (split list) can run simultaneously with a booth messaging change because they are measured independently.
- **Competitive intelligence guard**: If the agent detects a major competitor withdrawing from a show, flag for human review — this may signal market intelligence worth acting on (the show is declining) or an opportunity (less competition for attendees).
- **Staff rotation guard**: Never send an entirely new booth team to a proven show. At least 1 experienced staff member must attend for continuity with repeat attendees and institutional knowledge.

### 4. Build show selection intelligence

Over 12 months and 8+ shows, the data enables predictive show selection:

- **Show scoring model**: Train a scoring model (in Claude via the Anthropic API) on historical data: show characteristics (size, industry, geography, cost, time of year) vs outcomes (qualified leads, meetings, pipeline, ROI). Use this to predict performance of candidate shows before committing budget.
- **Diminishing returns detection**: Track whether your qualified lead rate at repeat shows is declining year-over-year. If the same show produces 20% fewer net-new leads than last year, flag audience saturation — you may be reaching the same people repeatedly.
- **Adjacent market discovery**: Use show performance data to identify adjacent verticals where your ICP congregates. If your best show is in {vertical A}, search for similar shows in related verticals that share ICP characteristics.
- **Competitive positioning intelligence**: Track which shows your competitors attend, their booth investment level, and their messaging themes over time. Identify shows where you have the field to yourself vs shows where competitive density is high.

Feed all intelligence back into show selection scoring.

### 5. Build the convergence detection system

The optimization loop should detect when the trade show motion has reached its local maximum:

- Track the percentage improvement from each adopted experiment
- When 3 consecutive experiments produce <2% improvement on the primary metric (qualified leads per show):
  1. The motion is converging — most tactical levers have been optimized
  2. Reduce experimentation frequency to 1 experiment per quarter (maintenance mode)
  3. Maintain monitoring at current frequency (shows are discrete events, not continuous)
  4. Generate a convergence report: "The trade show motion is optimized at [current metrics]. Best-performing configuration: [show circuit, booth approach, demo path, nurture sequence, content strategy]. Further improvement requires strategic changes: entering new show circuits, expanding to international events, increasing booth investment for higher-traffic positions, or product changes that unlock new demo narratives."

**Human action required:** At convergence, review the report. Decide whether to:
- Accept the local maximum and keep the motion running in maintenance mode
- Expand to a new show circuit or geographic market (resets the optimization loop)
- Invest in a step-change (e.g., becoming a keynote sponsor, hosting a side event at a major show) that shifts the performance ceiling
- Reallocate trade show budget to higher-ROI motions if trade shows have plateaued below other channels

### 6. Sustain the motion over 12 months

Over a 12-month Durable run, the agent:

- Manages 8-12 trade shows with automated pre-show and post-show operations
- Runs 6-10 experiments across all trade show variables
- Generates 50+ weekly optimization briefs
- Produces quarterly motion reports with strategic recommendations
- Detects and responds to seasonal patterns (Q4 conference season, summer lulls, end-of-year budget cycles)
- Refreshes the show calendar annually based on performance data and market intelligence
- Identifies when the show circuit is saturating (declining net-new leads at repeat shows) and recommends circuit expansion

The play is durable when the agent can maintain >=100 qualified leads per quarter and cost per meeting at or below the Scalable baseline without human optimization effort.

## Time Estimate

- Monitoring and reporting setup (PostHog dashboards, n8n crons, alert configuration): 10 hours
- Autonomous optimization loop configuration: 8 hours
- Guardrail and convergence detection setup: 4 hours
- Show selection intelligence model: 6 hours
- Per-show agent-managed effort (targeting, enrichment, nurture, analysis, content): 10 hours x 10 shows = 100 hours
- Per-show human effort (booth staffing, travel): excluded (human hours)
- Experiment design and implementation: 5 hours x 8 experiments = 40 hours
- Weekly brief generation and review: 0.5 hours x 50 weeks = 25 hours
- Quarterly motion report generation and strategic review: 4 hours x 4 = 16 hours
- **Total: ~200 hours over 12 months** (split: ~150 hours agent, ~50 hours human review)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Pre-show enrichment + lead enrichment at scale | $495/mo Growth (10,000 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| Loops | Pre-show outreach + tiered nurture at volume | $49/mo (5,000 contacts) or higher tier based on list size — [loops.so/pricing](https://loops.so/pricing) |
| Loom | Personalized Tier 1 video follow-ups | $12.50/mo Business — [loom.com/pricing](https://www.loom.com/pricing) |
| PostHog | Full-funnel tracking, experiments, anomaly detection | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM, deal tracking, show calendar, experiment log | $29/user/mo Plus — [attio.com](https://attio.com) |
| n8n | Monitoring crons, optimization loop, automation pipelines | Self-hosted free or Cloud Pro EUR60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Descript | Demo clips + content repurposing | $24/mo Creator — [descript.com/pricing](https://www.descript.com/pricing) |
| Cal.com | Meeting booking CTA | Free tier — [cal.com/pricing](https://cal.com/pricing) |
| Anthropic API | Hypothesis generation + evaluation (Claude) | Usage-based ~$15-40/mo for this play — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost at Durable: $630-930/mo** (Clay Growth + Loops + Loom + Descript + n8n Pro + Anthropic API)

Note: Annual show-specific costs at Durable: $40,000-100,000+ (8-12 shows x $4,000-10,000 per show). The agent's job is to maximize pipeline per dollar across this portfolio.

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics across shows, diagnose anomalies, generate hypotheses, run experiments on show selection, booth execution, nurture sequences, and content strategy, evaluate results, auto-implement winners, and generate weekly optimization briefs
- `trade-show-performance-monitor` — continuous monitoring, post-show post-mortems, quarterly motion reports, cross-show comparison, and show selection intelligence that feeds data into the optimization loop
