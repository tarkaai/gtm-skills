---
name: user-conference-annual-durable
description: >
  Annual User Conference -- Durable Intelligence. Always-on AI agents continuously
  monitor the conference program funnel across years, detect metric anomalies
  in promotion effectiveness, attendee engagement, and pipeline generation.
  Agents generate improvement hypotheses, run experiments on promotion strategy,
  session format, content repurposing, and follow-up approaches, then auto-implement
  winners. Weekly optimization briefs during active periods. Year-over-year
  convergence when successive experiments produce less than 2% improvement.
stage: "Marketing > ProductAware"
motion: "MicroEvents"
channels: "Events"
level: "Durable Intelligence"
time: "160 hours over 12 months"
outcome: ">=15% YoY attendance growth, >=50 expansion meetings per conference, sustained NPS >=50, agents detect degradation and auto-correct. Convergence when 3 consecutive experiments produce <2% improvement."
kpis: ["YoY attendance growth rate", "Expansion meetings per conference", "NPS trend", "Cost per expansion meeting trend", "Content engagement per derivative", "Experiment win rate", "Time to convergence"]
slug: "user-conference-annual"
install: "npx gtm-skills add marketing/product-aware/user-conference-annual"
drills:
  - autonomous-optimization
  - conference-performance-monitor
---

# Annual User Conference -- Durable Intelligence

> **Stage:** Marketing -> Product Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Sustain or improve conference program performance year over year without manual optimization effort
- Detect and respond to metric degradation (promotion fatigue, content staleness, attendee satisfaction drop) before they become critical
- Continuously experiment on every lever: promotion channels, session formats, speaker mix, content repurposing strategy, follow-up sequences, pricing, and scheduling
- Find the local maximum -- the best achievable conference performance given your market, audience size, and competitive landscape
- Generate weekly optimization briefs during active periods (promotion window + 60 days post-event) that summarize what changed, why, and what to try next
- Converge: when 3 consecutive experiments produce <2% improvement, the program is optimized at its current ceiling

## Leading Indicators

- Anomaly detection fires within 48 hours of any metric moving >15% from its rolling benchmark
- At least 1 experiment running at all times during active periods (promotion + post-conference)
- Experiment win rate >30% (enough wins to drive measurable improvement year over year)
- Weekly optimization briefs generated on schedule during active periods with actionable recommendations
- No metric declines for 2+ consecutive conference cycles without an experiment addressing it
- Year-over-year improvements in at least 3 of: registrations, show rate, meetings booked, NPS, cost per meeting

## Instructions

### 1. Deploy continuous conference program monitoring

Run the `conference-performance-monitor` drill to build the always-on monitoring layer for the annual conference program:

**Promotion-period monitoring (10-16 weeks before the event):**
- Weekly registration health checks: compare current registration count against the week-by-week target curve. The target curve is calibrated from prior year data and adjusted for audience growth.
- Channel effectiveness tracking: registrations per channel per week. If any channel's contribution drops >25% vs. prior year at the same promotion stage, fire an alert: "Channel [X] underperforming at week [N] of promotion -- investigate fatigue or deliverability."
- Partner co-promotion tracking: monitor registrations driven by each partner's promotion. If a partner's contribution is below the agreed target at the halfway point, alert for re-engagement or substitution.
- Registration quality monitoring: track the customer-to-prospect ratio among registrants. If net new prospects drop below 30% of registrations, fire alert: "Registration skewing too heavily toward existing customers -- expand outreach."

**Event-day monitoring:**
- Real-time attendance tracking: fire alerts if session attendance drops below 50% of registrations at any point during the event.
- Engagement density tracking: questions, poll responses, and chat messages per attendee per session. Compare to prior year benchmarks.
- Technical health monitoring: if stream quality degrades (for virtual) or platform issues arise, alert the ops team immediately.

**Post-conference monitoring (60 days):**
- Nurture sequence performance: open rates, reply rates, and meeting conversion rates by tier. Compare to prior year.
- Content derivative performance: engagement metrics per content piece type (clips, blog posts, LinkedIn posts, email sequences). Identify which content types drive the most downstream registrations and meetings.
- Pipeline attribution: track deals created, advanced, and closed from conference-sourced leads on a rolling 90-day window.
- Satellite event performance: registrations, attendance, and meetings from replay events. Compare cost-effectiveness to main event.

**Year-over-year trend analysis:**
- After each conference cycle completes (event + 90-day pipeline window), generate a full year-over-year comparison report
- Track multi-year trends: Is the conference program growing, plateauing, or declining? At what rate?
- Segment trends by: promotion channel, attendee type (customer vs. prospect), session type, content derivative type

### 2. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the annual conference program:

**Phase 1 -- Monitor (runs on schedule appropriate to the conference lifecycle):**

The conference program has distinct phases with different monitoring cadences:
- **Off-season (months 4-8 post-conference)**: Weekly monitoring of content derivative performance and pipeline attribution. Low activity period -- focus on data collection and strategic planning.
- **Pre-promotion (months 8-10)**: Bi-weekly monitoring. Agent analyzes prior year data, identifies the highest-impact improvement areas, and generates initial hypotheses for this year's experiments.
- **Active promotion (10-16 weeks before event)**: Daily monitoring. Registration velocity, channel effectiveness, email performance.
- **Event week**: Real-time monitoring.
- **Post-conference (60 days)**: Daily monitoring. Nurture performance, content derivative performance, meeting conversion.

At each monitoring check:
- Pull the conference program KPIs from PostHog
- Compare against: (a) the time-matched benchmark from prior year, (b) the pre-set target for this year, (c) the 3-year rolling average (if available)
- Classify each metric: **normal** (within +/-10% of benchmark), **outperforming** (>15% above benchmark), **underperforming** (>15% below benchmark), **critical** (>30% below benchmark)
- If underperforming or critical: trigger Phase 2

**Phase 2 -- Diagnose (triggered by anomaly):**

Gather context for hypothesis generation:
- Pull the current conference configuration from Attio: promotion channel mix, email sequences, session lineup, speaker roster, pricing, registration incentive, content repurposing schedule
- Pull the metric history: this year's trajectory vs. prior year at the same stage
- Pull qualitative signals: feedback survey themes, attendee comments, support ticket mentions of the conference
- Pull external context: competing events in the same window, industry news, macroeconomic factors

Run `hypothesis-generation` with the anomaly data + context. Receive 3 ranked hypotheses. Examples of conference-specific hypotheses:

- "Registration velocity is 20% below last year at week -6. Hypothesis: the theme is too similar to last year's and audience feels 'been there, done that.' Changing the conference subtitle and lead sessions to emphasize a new angle will increase registrations by 15%."
- "Partner-driven registrations are 40% below target. Hypothesis: partner promotion materials are not compelling enough. Providing partners with pre-written email copy, social graphics, and a unique discount code will increase partner-driven registrations by 30%."
- "Tier 1 follow-up reply rate dropped from 25% to 12% vs. last year. Hypothesis: the follow-up email is too generic. Adding account-specific context (their current plan, usage stats, relevant new features) will increase reply rate by 10 percentage points."
- "Content derivative engagement is declining -- LinkedIn post engagement dropped 35% vs. last year's clips. Hypothesis: video clips are saturating the audience. Testing carousel posts with data visualizations from session content will increase engagement by 20%."

If the top hypothesis has risk = "high" (e.g., changing the conference date or switching from virtual to in-person), send alert for human approval. Otherwise, proceed.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**

Design and implement the experiment. Conference experiments differ from webinar experiments because you typically have 1 main event per year, so experiments must be designed carefully:

**Within-conference experiments (can test within a single event cycle):**
- Promotion A/B tests: email subject lines, send timing, registration page variants, ad creative. Split audiences and measure conversion.
- Follow-up A/B tests: email copy, CTA variants, send timing, personalization depth. Split attendee tiers and measure reply and meeting rates.
- Content repurposing tests: clip format (60s vs. 2min), blog post length, LinkedIn post style (video vs. carousel vs. text), email sequence length. Measure engagement per variant.
- Satellite event tests: different replay session selections, different timing, different promotion approaches.

**Between-conference experiments (test across years):**
- Session format changes: this year add workshops, measure engagement vs. prior year's presentations. Next year test panels vs. workshops.
- Pricing model changes: this year free, next year paid. Measure registration volume, show rate, and attendee quality.
- Timing changes: this year Tuesday-Wednesday, next year Wednesday-Thursday. Measure show rate.
- Scope changes: add a second day, add a virtual component to in-person, add regional satellite events.

For each experiment:
- Set success criteria before running
- Set minimum sample size (for within-event tests) or define the comparison methodology (for between-year tests)
- Log experiment start in Attio with: hypothesis, variants, success criteria, expected duration
- Implement the variant using the appropriate drill or fundamental

**Phase 4 -- Evaluate (triggered by experiment completion):**

Pull experiment results from PostHog. Run `experiment-evaluation`:

- **Adopt**: Winner improves primary metric with 95% confidence (within-event tests) or shows meaningful improvement vs. prior year (between-year tests). Update the conference playbook. Log the change.
- **Iterate**: Promising direction but not conclusive. Refine the hypothesis. Test again in the next promotion wave or at the next event.
- **Revert**: Variant performed worse. Restore the control approach. Log the failure and the learning.
- **Extend**: Insufficient data. Continue the experiment into the next phase (e.g., extend a promotion test into the post-event follow-up window).

Store the full evaluation (decision, confidence, reasoning) in Attio on the conference record.

**Phase 5 -- Report (weekly during active periods):**

Generate weekly optimization briefs during active periods (promotion + 60 days post-event):

- Anomalies detected this week
- Experiments in progress (status, preliminary data)
- Experiments completed (decisions, impact)
- Net metric change from adopted experiments vs. prior year
- Distance from estimated local maximum
- Recommended focus for next week

During off-season, generate monthly program health reports:
- Content derivative performance (which pieces are still driving engagement?)
- Pipeline attribution updates (deals closing from conference leads)
- Competitive landscape changes (new competing events, market shifts)
- Early recommendations for next year's conference

Post all reports to Slack and store in Attio.

### 3. Configure conference-specific guardrails

The `autonomous-optimization` drill has standard guardrails. Add these conference-specific constraints:

- **Theme stability guard**: Once the conference theme is announced (week -10), do not change it. Experiments on messaging angle and emphasis are fine, but the core theme stays fixed. Changing it mid-promotion confuses the audience.
- **Speaker commitment guard**: Any experiment that requires adding, removing, or rescheduling a speaker must be planned 4+ weeks in advance. Speakers are humans with calendars, not variables.
- **Budget guard**: Never increase total conference spend by more than 30% vs. prior year without human approval. This includes venue upgrades, paid promotion increases, and new tool costs.
- **Audience fatigue guard**: Track email unsubscribe rate on conference promotional emails. If any send exceeds 1.5% unsubscribe rate, immediately pause that channel and review targeting. Conference promotion should not damage your email list health.
- **Promotion frequency guard**: Maximum 1 email per week to any individual during the promotion window. Maximum 3 LinkedIn posts per week about the conference. Over-promotion hurts brand perception.
- **Follow-up intensity guard**: Maximum 4 follow-up emails per attendee in the 14-day post-conference window. Maximum 6 total touches including satellite event invites.
- **One experiment per variable**: Never test multiple variables simultaneously on the same audience segment. Clean attribution requires isolation.

### 4. Build the convergence detection system

Track the percentage improvement from each adopted experiment. The conference program converges differently than recurring plays because you have fewer data points (1 main event per year):

**Within-cycle convergence**: When all within-event experiments (promotion, follow-up, content) for a single conference cycle produce <2% improvement over the prior year's benchmarks, the tactical optimization for that cycle is converging.

**Cross-cycle convergence**: When 2 consecutive annual conferences show <2% improvement on primary metrics (attendance, meetings, NPS) despite active experimentation:

1. The conference program has reached its local maximum
2. Reduce experiment volume to 1-2 strategic experiments per cycle
3. Generate a convergence report:

"This conference program is optimized at [current metrics]. The best-performing configuration is: [theme approach, session format mix, promotion channel mix, follow-up strategy, content repurposing approach, pricing model]. Further improvement requires strategic changes: expanding to a second event per year, adding an in-person component, entering new geographic markets, or targeting a new audience segment beyond current ICP."

**Human action required:** At convergence, review the report. Decide whether to:
- Accept the local maximum and maintain the conference in steady-state mode
- Invest in a strategic shift: add an in-person day, expand to a second annual event, co-brand with a major partner
- Expand the target audience: bring in adjacent personas (developers, executives, partners) who are not in the current ICP

### 5. Sustain the conference program over 12 months

Over a 12-month Durable cycle, the agent:

- Manages the full conference lifecycle: planning (months 1-3), promotion (months 4-6), event execution (month 7), post-event follow-up and content repurposing (months 7-9), pipeline attribution and analysis (months 7-12), next-year planning (months 10-12)
- Runs 6-12 within-cycle experiments across promotion, follow-up, and content variables
- Generates 20+ weekly optimization briefs during active periods
- Generates 4-6 monthly program health reports during off-season
- Produces 1 comprehensive year-over-year conference ROI report
- Maintains the content repurposing pipeline year-round: conference derivative content should drive engagement for 6+ months post-event
- Identifies strategic opportunities for the next cycle: new audience segments, format changes, partnership expansions

The play is durable when the agent can maintain or improve conference metrics (attendance growth >=15% YoY, meetings >=50, NPS >=50) without human optimization effort beyond content delivery and strategic decisions.

## Time Estimate

- Conference performance monitoring setup (PostHog dashboards, n8n cron jobs, alert configuration): 10 hours
- Autonomous optimization loop configuration: 8 hours
- Guardrail and convergence detection setup: 4 hours
- Pre-conference planning and promotion (agent-managed): 30 hours
- Conference execution (human content delivery + agent logistics): 8 hours
- Post-conference follow-up and content repurposing (agent-managed): 20 hours
- Satellite events (2-3 events, agent-managed promotion and follow-up): 10 hours
- Experiment design, implementation, and evaluation: 6 hours x 10 experiments = 60 hours (split across the year)
- Weekly brief generation and review during active periods: 1 hour x 30 weeks = 30 hours
- Monthly program health reports: 2 hours x 6 months = 12 hours
- Year-over-year analysis and next-year planning: 8 hours
- **Total: ~160 hours over 12 months** (split: ~110 hours agent, ~50 hours human)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Riverside | Conference recording + production | $29/mo Pro (4K, 15hr transcription) -- [riverside.com/pricing](https://riverside.com/pricing) |
| Loops | Email invites, reminders, nurture, content sequences | $49/mo (5,000 contacts) or $79/mo (10,000) -- [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Event tracking, funnels, experiments, anomaly detection | Free tier: 1M events/mo -- [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM, registrant tracking, deal creation, reporting | $29/user/mo Plus -- [attio.com](https://attio.com) |
| n8n | Monitoring crons, optimization loop, follow-up automation | Self-hosted free or Cloud Pro EUR60/mo -- [n8n.io/pricing](https://n8n.io/pricing) |
| Clay | Prospect sourcing for conference invites | $185/mo Launch (2,500 credits) -- [clay.com/pricing](https://www.clay.com/pricing) |
| Descript | Recording clips + content repurposing | $24/mo Creator -- [descript.com/pricing](https://www.descript.com/pricing) |
| Loom | Personalized follow-up clips | $12.50/mo Business -- [loom.com/pricing](https://www.loom.com/pricing) |
| Cal.com | Expansion call booking CTA | Free tier -- [cal.com/pricing](https://cal.com/pricing) |
| Luma | Event registration and management | Free -- [lu.ma](https://lu.ma) |
| Anthropic API | Hypothesis generation + evaluation (Claude) | Usage-based ~$15-30/mo during active periods -- [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost at Durable: $370-650/mo** (all tools above + Anthropic API usage; costs concentrated in active months, lower during off-season)

## Drills Referenced

- `autonomous-optimization` -- the core always-on loop: monitor conference metrics across the full lifecycle, diagnose anomalies in promotion, engagement, and pipeline generation, generate hypotheses, run experiments on promotion strategy, session format, content repurposing, and follow-up approaches, evaluate results, auto-implement winners, and generate weekly optimization briefs
- `conference-performance-monitor` -- continuous monitoring of the conference program funnel, promotion-period health checks, post-conference analysis, year-over-year trend tracking, and pipeline attribution that feeds data into the optimization loop
