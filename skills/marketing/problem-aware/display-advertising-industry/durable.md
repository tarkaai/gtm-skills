---
name: display-advertising-industry-durable
description: >
  Display Advertising — Durable Intelligence. Always-on AI agents continuously optimize display
  placements, creative rotation, audience targeting, and cross-platform budget allocation. The
  autonomous optimization loop detects metric anomalies, generates improvement hypotheses, runs
  A/B experiments, and auto-implements winners. Weekly optimization briefs track convergence
  toward the local maximum.
stage: "Marketing > ProblemAware"
motion: "LightweightPaid"
channels: "Paid"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained display efficiency and >=50 qualified leads/month over 12 months via AI-optimized placements, with <2% variance in successive optimization cycles indicating convergence at the local maximum"
kpis: ["Sustained monthly qualified leads", "Cost per qualified lead trend", "Autonomous experiment win rate", "Placement portfolio health", "Creative pipeline velocity", "Audience fatigue index", "Optimization convergence rate"]
slug: "display-advertising-industry"
install: "npx gtm-skills add Marketing/ProblemAware/display-advertising-industry"
drills:
  - autonomous-optimization
---

# Display Advertising — Durable Intelligence

> **Stage:** Marketing > ProblemAware | **Motion:** LightweightPaid | **Channels:** Paid

## Outcomes

Always-on AI agents finding the local maximum. The display advertising program runs itself: placement discovery and curation, creative generation and rotation, audience optimization, budget allocation, and performance reporting all execute autonomously. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in display KPIs, generate improvement hypotheses, run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs track convergence. The program converges when successive experiments produce <2% improvement -- at that point, display performance is near-optimal for the current market, audience, and competitive landscape.

**Pass threshold:** Sustained >=50 qualified leads/month and cost per qualified lead trending down or stable over 12 months, with <2% variance in successive optimization cycles indicating convergence at the local maximum.

## Leading Indicators

- Autonomous optimization loop runs daily without manual intervention
- Weekly optimization briefs are generated and posted to Slack
- At least 2 experiments per month are initiated, evaluated, and decided
- Creative pipeline operates autonomously: AI generates variants, human reviews, winners deploy, fatigued creatives retire
- Placement portfolio is self-curating: new high-quality sites discovered, low-quality sites auto-excluded
- Cost per qualified lead is stable or improving month over month
- Convergence signal: last 3 experiments produced <2% improvement each
- Audience fatigue index stays below threshold without manual intervention (auto-rotation handles it)

## Instructions

### 1. Deploy Autonomous Optimization

Run the `autonomous-optimization` drill configured for the display advertising program. This is the drill that makes Durable fundamentally different from Scalable.

**Configure the optimization loop:**

**Phase 1 -- Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check display program KPIs:
  - Cost per qualified lead (primary KPI)
  - CTR by campaign type (managed placements, custom intent, topic, retargeting, lookalike)
  - CPC by platform (GDN vs. Meta Audience Network)
  - Creative pipeline health (active variants, average creative age, fatigue rate)
  - Lead quality (% scoring 70+ on ICP scoring)
  - Placement quality (% of impressions on validated industry sites)
  - Audience frequency by segment
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +-10%), plateau (+-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 -- Diagnose (triggered by anomaly):**
- Gather context from Attio: current placement portfolio, audience segments, budget allocation, active creatives, campaign structure
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data and context
- Example hypotheses the system might generate:
  - "CPC increased 25% on GDN managed placements this week. Hypothesis: frequency on the top 5 placements has exceeded 6/week, indicating audience exhaustion on those sites. Test adding 10 new managed placements from the custom intent discovery pipeline to dilute frequency."
  - "CTR dropped from 0.22% to 0.14% across all campaigns. Hypothesis: the top 3 creatives have all been running for 5+ weeks and are fatigued. Test deploying the 5 fresh variants currently in the staging queue."
  - "Cost per qualified lead increased 30%. Hypothesis: Meta Audience Network retargeting audience has shrunk below 2,000 due to the 30-day window expiring. Test expanding the window to 60 days or adding GDN retargeting to supplement."
  - "Lead quality dropped from 55% to 35% ICP match. Hypothesis: the interest-based Meta audience is producing low-quality leads at high volume. Test pausing the interest audience and reallocating budget to managed placements and retargeting."
  - "GDN custom intent is outperforming managed placements by 40% on CPA. Hypothesis: the custom intent keywords are capturing higher-intent users who are actively researching the problem. Test expanding the custom intent keyword list and increasing its budget share."
- Store hypotheses in Attio. If risk = "high", alert human. If "low" or "medium", proceed.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
- Use `posthog-experiments` to create a feature flag splitting traffic between control and variant
- Implement the variant using the appropriate mechanism:
  - If testing placement changes: create a duplicate campaign with the modified placement list via Google Ads API
  - If testing creative changes: deploy new creatives in a parallel ad group and compare performance
  - If testing audience changes: create a duplicate campaign with the modified audience configuration
  - If testing budget allocation: split budget between current and proposed allocation
  - If testing cross-platform shift: reallocate budget between GDN and Meta
  - If testing bidding strategy: duplicate campaign with different bidding configuration
- Set experiment duration: minimum 7 days or 10,000+ impressions per variant, whichever is longer
- Log experiment in Attio with: hypothesis, start date, expected duration, success criteria

**Phase 4 -- Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` to determine: Adopt, Iterate, Revert, or Extend
- If Adopt: update live configuration, log the change, move to Phase 5
- If Iterate: generate new hypothesis building on this result, return to Phase 2
- If Revert: restore control configuration, log failure, return to Phase 1
- Store full evaluation in Attio

**Phase 5 -- Report (weekly via n8n cron):**
- Generate weekly optimization brief:
  - Anomalies detected this week
  - Experiments running, completed, decided
  - Net impact on cost per qualified lead and lead volume
  - Current distance from estimated local maximum
  - Placement portfolio health: sites added, excluded, total active
  - Creative pipeline health: variants in queue, average age, fatigue rate
  - Recommended focus for next week
- Post to Slack, store in Attio

### 2. Deploy Display Performance Reporting

Run the `autonomous-optimization` drill:

1. Build the PostHog display dashboard (8 panels: spend/reach trends, placement quality matrix, creative performance, audience segment comparison, conversion funnel, lead quality trend, cross-platform CPA trend, pipeline attribution)
2. Build Attio saved views (display-sourced contacts, display pipeline, display ROI by campaign)
3. Deploy the weekly automated report (n8n workflow every Monday)
4. Deploy the monthly ROI report (first Monday of each month)
5. Configure 5 real-time anomaly alerts (CPA spike, CTR collapse, zero conversions, budget runaway, lead quality drop)

The reporting layer provides the data substrate that the autonomous optimization loop reads. Without accurate reporting, the optimizer cannot generate meaningful hypotheses.

### 3. Configure Optimization Guardrails

Apply the guardrails from the `autonomous-optimization` drill to the display program:

- **Rate limit:** Maximum 1 active experiment at a time on the display program
- **Revert threshold:** If cost per qualified lead exceeds 2x the 4-week average during any experiment, auto-revert immediately
- **Human approval required for:**
  - Budget changes exceeding 20% of current monthly spend
  - Adding or removing an entire platform (GDN or Meta)
  - Changes to placement exclusion rules that affect more than 30% of impressions
  - Any change the hypothesis generator flags as "high risk"
  - Changes to landing page offers or CTAs
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review
- **Never optimize what isn't measured:** All display events must have PostHog tracking before experiments can target them. If a KPI lacks tracking, fix tracking first using the `posthog-gtm-events` drill

### 4. Autonomous Placement Curation

At Durable level, the placement portfolio should be self-maintaining:

1. **Discovery pipeline (weekly n8n workflow):**
   - Query GDN placement reports for sites discovered via custom intent and topic targeting
   - Score each new site: CTR, conversion rate, CPA, ICP match of leads from that site
   - If a discovered site produces 3+ conversions with CPA below target: auto-add to managed placement list
   - If a managed placement produces 1,000+ impressions with zero conversions for 2 consecutive weeks: auto-exclude

2. **Competitive placement monitoring (monthly):**
   - Use SEMrush or SimilarWeb API to check where competitors run display ads
   - Identify new competitor placements that are not in your portfolio
   - Queue them for testing in the next custom intent campaign

3. **Seasonal placement adjustment:**
   - Track placement performance by month over the year
   - Detect seasonal patterns (e.g., certain trade publications spike during conference season)
   - Auto-increase budget on seasonally strong placements and reduce on weak ones

### 5. Autonomous Creative Pipeline

At Durable level, the creative pipeline should operate with minimal human touch:

1. **AI generates creative batches** bi-weekly using the evolving creative playbook (templates updated based on experiment results)
2. **Human reviews** (15 min per batch) and approves copy
3. **Images produced** from approved concepts using brand templates
4. **Creatives deploy** to campaigns automatically
5. **Fatigue monitor auto-retires** underperforming creatives daily
6. **The optimization loop** continuously tests which creative templates, hook types, pain points, and image styles produce the best display results

Over time, the creative playbook evolves based on experimental data. The templates that produce the best-performing display ads get weighted more heavily in the generation pipeline.

### 6. Monitor Convergence

The optimization loop should detect when the display program has reached its local maximum:

- Track the magnitude of improvement from each adopted experiment
- If the last 3 consecutive experiments each produced <2% improvement:
  1. The program is converged -- current performance is near-optimal
  2. Reduce monitoring frequency from daily to weekly
  3. Reduce experiment frequency from 4/month to 1/month (maintenance mode)
  4. Generate a convergence report: "Display advertising program optimized. Current cost per qualified lead: $[X]. Monthly qualified leads: [Y]. Active placements: [Z]. Further gains require strategic changes (new placement categories, new audience markets, landing page redesign, or channel diversification) rather than tactical optimization."

Post the convergence report to Slack and store in Attio.

### 7. Handle Market and Platform Shifts

The display advertising landscape evolves: platform algorithm changes, cookie deprecation, new ad formats, competitive dynamics. The optimizer should detect shifts:

- If CPM increases across all GDN placements by >20%: Google may have changed auction dynamics. Test switching to Microsoft Advertising Display as a supplementary channel.
- If conversion rate drops despite stable CTR: landing page or offer fatigue. Alert for creative refresh on landing pages.
- If Meta Audience Network reach shrinks significantly: Meta may have reduced Audience Network inventory. Shift budget to GDN or explore DV360 for programmatic access.
- If a major competitor starts running heavy display on your top placements: frequency competition increases. Test new placements or shift to custom intent targeting to find users before they reach the contested sites.
- If Google announces new display format support (e.g., interactive HTML5 ads): evaluate and test. Early adopters of new formats often get lower CPMs.

In these cases: the optimizer flags the situation and recommends whether tactical optimization can address it or whether strategic human intervention is needed.

## Time Estimate

- 25 hours: Autonomous optimization setup (n8n workflows, PostHog experiments, guardrails, placement curation)
- 15 hours: Performance reporting dashboard, anomaly alerts, monthly ROI report
- 5 hours: Creative pipeline automation refinement
- 100 hours: Ongoing optimization over 12 months (~2 hours/week for monitoring, experiment design, evaluation)
- 15 hours: Monthly strategic reviews (12 reviews at ~1.25 hours each)
- 10 hours: Convergence analysis and maintenance mode transition
- 10 hours: Platform shift response and strategic adaptation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Ads (GDN) | Display campaigns — agent-optimized placements and audiences | Ad spend ($3,000-12,000/mo, agent-optimized) |
| Meta Ads (Audience Network) | Display campaigns — agent-optimized retargeting and lookalike | Ad spend ($2,000-8,000/mo, agent-optimized) |
| PostHog | Analytics — dashboards, experiments, anomaly detection, funnels | Free up to 1M events, then usage-based — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM — lead tracking, experiment logging, pipeline attribution | $29/user/mo (Plus) or $59/user/mo (Pro) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — lead scoring at scale | $349/mo (Explorer) or $699/mo (Pro) — [clay.com/pricing](https://www.clay.com/pricing) |
| Loops | Email — nurture sequences with A/B testing | $99/mo (Growth) — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Automation — optimization loop, creative pipeline, placement curation, reporting | $60/mo (Pro, 10K executions) — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | AI — creative generation, hypothesis generation, experiment evaluation | Usage-based, ~$50-100/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| Webflow | Landing pages | $29/mo (CMS) — [webflow.com/pricing](https://webflow.com/pricing) |

**Estimated play-specific cost this level:** $5,000-20,000/mo ad spend + ~$700-1,100/mo tools + ~$50-100/mo AI API. Total: $5,750-21,200/mo.

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: detect anomalies in display KPIs, generate hypotheses (placement saturation, creative fatigue, audience exhaustion, cross-platform CPA drift, lead quality decline), run experiments, evaluate results, auto-implement winners. Weekly optimization briefs. Converges when successive experiments produce <2% improvement.
- `autonomous-optimization` — comprehensive reporting on display advertising effectiveness: placement quality matrix, creative health, audience performance, and pipeline attribution dashboards, weekly and monthly automated reports, real-time anomaly alerts. Provides the data layer the optimization loop reads from.
