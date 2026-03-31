---
name: analyst-relations-program-durable
description: >
  Analyst Relations Program — Durable Intelligence. Always-on AI agents autonomously optimize
  analyst targeting, briefing cadence, nurture content, and report inclusion strategy. The
  autonomous-optimization loop detects anomalies, generates hypotheses, runs experiments, and
  auto-implements winners. Weekly optimization briefs track convergence.
stage: "Marketing > SolutionAware"
motion: "PartnershipsWarmIntros"
channels: "Other"
level: "Durable Intelligence"
time: "160 hours over 12 months"
outcome: "Sustained >=25 analyst-influenced deals/quarter over 12 months, with <2% variance in successive optimization cycles indicating convergence at the local maximum"
kpis: ["Sustained analyst-influenced deals/quarter", "Autonomous experiment win rate", "Briefing-to-mention rate trend", "Nurture engagement rate trend", "Report inclusion rate", "Optimization convergence rate"]
slug: "analyst-relations-program"
install: "npx gtm-skills add marketing/solution-aware/analyst-relations-program"
drills:
  - autonomous-optimization
  - analyst-briefing-monitor
---

# Analyst Relations Program — Durable Intelligence

> **Stage:** Marketing > SolutionAware | **Motion:** PartnershipsWarmIntros | **Channels:** Other

## Outcomes

Always-on AI agents finding the local maximum. The analyst relations program runs autonomously: analyst lists refresh quarterly, nurture cadences adapt based on engagement data, briefing materials update with new metrics, and report cycle tracking anticipates deadlines. The `autonomous-optimization` drill runs the core loop: detect anomalies in analyst engagement KPIs, generate hypotheses, run experiments, evaluate results, and auto-implement winners. Weekly optimization briefs track convergence. The program converges when successive experiments produce <2% improvement.

**Pass threshold:** Sustained >=25 analyst-influenced deals/quarter over 12 months, with <2% variance in successive optimization cycles indicating convergence at the local maximum.

## Leading Indicators

- Autonomous optimization loop runs daily without manual intervention
- Weekly optimization briefs are generated and posted to Slack
- At least 2 experiments per month are initiated, evaluated, and decided
- Analyst nurture cadences operate autonomously: updates generated, reviewed, sent
- Analyst-influenced deals per quarter are stable or improving
- Convergence signal: last 3 experiments each produced <2% improvement
- 50%+ of tracked analysts are at relationship score >= 3 (established relationship)

## Instructions

### 1. Deploy Autonomous Optimization

Run the `autonomous-optimization` drill configured for the analyst relations program.

**Configure the optimization loop:**

**Phase 1 — Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check analyst relations KPIs:
  - Briefing acceptance rate (outreach effectiveness)
  - Briefing-to-mention conversion rate (briefing quality)
  - Nurture email open and reply rates (relationship health)
  - Analyst-influenced deals per week (pipeline impact)
  - Report inclusion rate (mentions per reports published in your category)
  - Proactive analyst outreach count (analysts reaching out to you)
- Compare last 4 weeks against 8-week rolling average (analyst relations moves slower than content or ads)
- Classify: normal (within +-10%), plateau (+-2% for 6+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context from Attio: current analyst list, relationship scores, recent briefings, nurture engagement, pending report deadlines
- Pull 12-week metric history from PostHog
- Run `hypothesis-generation` with anomaly data and context
- Example hypotheses:
  - "Briefing acceptance rate dropped from 45% to 25% this quarter. Hypothesis: briefing request emails are too generic — they do not reference the analyst's most recent publication. Test: refresh all request templates with Claude-generated personalization referencing the analyst's latest report."
  - "Analyst-influenced deals dropped 30% despite stable briefing volume. Hypothesis: sales team stopped asking the analyst research question during discovery. Test: add an automated prompt in the CRM deal stage to ask 'What research have you consulted?'"
  - "Nurture email reply rate declined from 15% to 5%. Hypothesis: quarterly updates have become formulaic. Test: replace the standard update format with a 'data insight' format — lead with one surprising metric relevant to the analyst's coverage area."
  - "Two Tier 1 analysts who previously mentioned us stopped engaging. Hypothesis: they shifted coverage to a sub-category we have not addressed. Test: schedule targeted re-briefings focused on the new sub-category with a custom one-pager."
- Store hypotheses in Attio. If risk = "high", alert human. If "low" or "medium", proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Implement the variant:
  - If testing nurture format: split the analyst list into control (current format) and variant (new format) for the next quarterly update
  - If testing briefing outreach: use the new template for the next 5 briefing requests while maintaining the old template for 5 others
  - If testing sales integration: implement the CRM prompt in half the sales team for 4 weeks
  - If testing re-briefing approach: use the new one-pager format for 3 stale relationships vs standard approach for 3 others
- Use `posthog-experiments` to create feature flags tracking control vs variant
- Set experiment duration: minimum 4 weeks (analyst relations has longer feedback loops)
- Log experiment in Attio with: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` to determine: Adopt, Iterate, Revert, or Extend
- If Adopt: update templates, processes, or integrations. Log the change.
- If Iterate: generate new hypothesis. Return to Phase 2.
- If Revert: restore previous approach. Log failure. Return to Phase 1.
- Store full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron):**
- Generate weekly optimization brief:
  - Anomalies detected this week
  - Experiments running, completed, decided
  - Net impact on analyst-influenced deals
  - Current distance from estimated local maximum
  - Analyst relationship portfolio health (score distribution)
  - Upcoming report deadlines and preparation status
  - Recommended focus for next week
- Post to Slack, store in Attio

### 2. Deploy Analyst Briefing Monitoring

Run the `analyst-briefing-monitor` drill at full scale:

1. Maintain the PostHog dashboard (briefing pipeline, report tracking, pipeline influence, relationship health)
2. Keep anomaly detection thresholds calibrated quarterly
3. Weekly and monthly automated reports continue generating
4. Monthly deep-dive includes: experiment results, report cycle updates, relationship score trends, competitive analyst coverage analysis

The reporting layer provides the data substrate the optimization loop reads.

### 3. Configure Optimization Guardrails

Apply the guardrails from the `autonomous-optimization` drill:

- **Rate limit:** Maximum 1 active experiment at a time on the analyst program
- **Revert threshold:** If analyst-influenced deals drop to zero for 6 consecutive weeks during an experiment, auto-revert
- **Human approval required for:**
  - Changes to how the company is positioned in briefings (messaging changes)
  - Providing new data or metrics to analysts that have not been approved for external sharing
  - Budget commitments (e.g., Gartner or Forrester paid programs)
  - Adding or removing Tier 1 analysts from the program
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment, wait 14 days before testing the same variable (analyst relations has slower cycles)
- **Maximum experiments per month:** 3 (lower than other plays due to longer feedback loops). If all 3 fail, pause and flag for human strategic review.

### 4. Autonomous Analyst Intelligence

At Durable level, the system proactively identifies opportunities:

1. **Publication monitoring:** n8n workflow scans for new publications from tracked analysts (via RSS feeds, Google Alerts, or Mention API). When a new report is published in your category, alert the team and draft a response (congratulations note, offer of updated briefing data).
2. **Category shift detection:** Track when analysts add or change category definitions. If your category is renamed or split, update briefing materials and outreach terminology.
3. **Competitive coverage tracking:** Monitor when competitors get analyst mentions. Draft proactive "alternative perspective" outreach to the same analysts.
4. **Report cycle prediction:** Based on historical publication dates, predict when the next refresh of each major report is likely. Auto-schedule re-briefing outreach 6 months before expected publication.
5. **New analyst detection:** Monitor for new analysts hired at tracked firms or independent analysts who start covering your space. Auto-add to Clay for enrichment and evaluation.

### 5. Monitor Convergence

Track the magnitude of improvement from each adopted experiment:

- If the last 3 consecutive experiments each produced <2% improvement:
  1. The analyst program is converged — current performance is near-optimal
  2. Reduce monitoring frequency from daily to weekly
  3. Reduce experiment frequency from 3/month to 1/month (maintenance mode)
  4. Generate a convergence report: "Analyst relations program optimized. Current analyst-influenced deals/quarter: [X]. Report inclusion rate: [Y]. Relationship health: [Z]% at score >= 3. Further gains require strategic changes (paid analyst programs like Gartner Peer Insights, Forrester TEI studies, or expanding to new analyst categories) rather than tactical optimization."

Post convergence report to Slack and store in Attio.

### 6. Handle Market and Category Shifts

The optimizer should detect external shifts:

- If a major analyst firm changes its category taxonomy: update all briefing materials and outreach to match the new terminology
- If a new analyst firm enters your space (e.g., a new research boutique): evaluate and add to the program
- If peer review platforms (G2, Capterra) become more influential than traditional analysts in your category: shift program emphasis
- If AI-powered research tools change how analysts work: adapt briefing format (e.g., structured data vs narrative one-pagers)

## Time Estimate

- 18 hours: Autonomous optimization setup (n8n workflows, PostHog experiments, guardrails)
- 8 hours: Analyst monitoring refinement and report cycle tracking
- 4 hours: Analyst intelligence automation (publication monitoring, competitive tracking)
- 80 hours: Ongoing optimization over 12 months (~1.5 hours/week)
- 15 hours: Monthly strategic reviews (12 reviews at 1.25 hours each)
- 20 hours: Briefing preparation and delivery (ongoing)
- 15 hours: Convergence analysis, category shift response, and adaptation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — analyst contacts, experiment logging, pipeline attribution | $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — quarterly analyst list refresh | $149/mo (Starter) — [clay.com/pricing](https://www.clay.com/pricing) |
| Loops | Email — automated analyst nurture sequences | $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Mention | Analyst publication and competitor monitoring | $41/mo (Solo) — [mention.com/pricing](https://mention.com/en/pricing/) |
| n8n | Automation — optimization loop, nurture, monitoring | $60/mo (Pro) — [n8n.io/pricing](https://n8n.io/pricing) |
| PostHog | Analytics — dashboards, experiments, anomaly detection | Free up to 1M events — [posthog.com/pricing](https://posthog.com/pricing) |
| Cal.com | Scheduling — analyst briefing booking | Free plan — [cal.com/pricing](https://cal.com/pricing) |
| Claude API | Briefing docs, nurture content, hypothesis generation, evaluation | ~$50-80/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** Loops ~$49/mo + Mention ~$41/mo = ~$90/mo play-specific. n8n, PostHog, Attio, Clay are standard stack.

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: detect anomalies in analyst relations KPIs, generate hypotheses (briefing template effectiveness, nurture format, sales integration, relationship re-engagement), run experiments, evaluate results, auto-implement winners. Weekly optimization briefs. Converges when successive experiments produce <2% improvement.
- `analyst-briefing-monitor` — continuous monitoring of briefing pipeline, report mentions, analyst-influenced pipeline, and relationship health. Provides the data layer the optimization loop reads from.
