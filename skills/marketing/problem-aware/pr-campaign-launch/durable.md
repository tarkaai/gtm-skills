---
name: pr-campaign-launch-durable
description: >
  PR Campaign Launch — Durable Intelligence. Always-on AI agents autonomously optimize pitch
  angles, outlet targeting, source request responses, and media relationship cadences. The
  autonomous-optimization loop detects anomalies, generates hypotheses, runs experiments, and
  auto-implements winners. Weekly optimization briefs track convergence.
stage: "Marketing > ProblemAware"
motion: "PREarnedMentions"
channels: "Other, Social"
level: "Durable Intelligence"
time: "170 hours over 12 months"
outcome: "Sustained >=50 qualified leads/quarter from earned media, with <2% variance in successive optimization cycles indicating convergence at the local maximum"
kpis: ["Sustained PR-attributed leads/quarter", "Autonomous experiment win rate", "Pitch-to-placement rate trend", "Source request win rate trend", "Media relationship health score", "Optimization convergence rate"]
slug: "pr-campaign-launch"
install: "npx gtm-skills add marketing/problem-aware/pr-campaign-launch"
drills:
  - autonomous-optimization
  - pr-performance-monitor
---

# PR Campaign Launch — Durable Intelligence

> **Stage:** Marketing > ProblemAware | **Motion:** PREarnedMentions | **Channels:** Other, Social

## Outcomes

Always-on AI agents finding the local maximum. The PR program runs autonomously: media list refreshes monthly, pitch angles evolve based on placement data, source request responses draft automatically, journalist relationships are nurtured on cadence, and every placement is tracked through to pipeline. The `autonomous-optimization` drill runs the core loop: detect anomalies in PR KPIs, generate hypotheses, run experiments, evaluate results, and auto-implement winners. Weekly optimization briefs track convergence. The program converges when successive experiments produce <2% improvement.

**Pass threshold:** Sustained >=50 qualified leads/quarter from earned media, with <2% variance in successive optimization cycles indicating convergence at the local maximum.

## Leading Indicators

- Autonomous optimization loop runs daily without manual intervention
- Weekly optimization briefs are generated and posted to Slack
- At least 2 experiments per month are initiated, evaluated, and decided
- Source request pipeline operates autonomously: detection, evaluation, draft, approval, submission
- PR-attributed leads per quarter are stable or improving
- Convergence signal: last 3 experiments each produced <2% improvement
- Journalist relationship scores trending upward across the portfolio

## Instructions

### 1. Deploy Autonomous Optimization

Run the `autonomous-optimization` drill configured for the PR program.

**Configure the optimization loop:**

**Phase 1 — Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check PR program KPIs:
  - Pitch-to-reply rate (primary outreach signal)
  - Reply-to-placement rate (pitch quality signal)
  - Placements per week (output volume)
  - Referral traffic per placement (placement quality signal)
  - PR-attributed leads per week (pipeline impact)
  - Source request win rate (reactive PR effectiveness)
  - Brand mention sentiment (reputation signal)
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +-10%), plateau (+-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context from Attio: current pitch angles in rotation, journalist relationship scores, recent campaign performance, source request topics
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with anomaly data and context
- Example hypotheses:
  - "Pitch-to-reply rate dropped 30% this month. Hypothesis: the lead pitch angle ('AI cost reduction data') has been used for 3 consecutive campaigns and journalists have seen the story. Test a new angle: 'contrarian take on [industry trend]' with fresh data."
  - "Placements are up but referral traffic per placement is down 40%. Hypothesis: recent placements have been in Tier 3 outlets with lower ICP readership. Test shifting 50% of outreach effort back to Tier 1 and 2 outlets."
  - "Source request win rate dropped from 25% to 10%. Hypothesis: response turnaround time increased from 2 hours to 8 hours as volume grew. Test: prioritize only relevance-score >= 4 requests and respond within 2 hours."
  - "Competitor coverage spiked 3x this month. Hypothesis: competitor launched a funding round. Test: proactive 'alternative perspective' pitch to every journalist who covered the competitor."
- Store hypotheses in Attio. If risk = "high", alert human. If "low" or "medium", proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Implement the variant:
  - If testing pitch angles: split the next campaign into control (current angle) and variant (new angle), same target list split randomly
  - If testing outlet tier mix: allocate the next 20 pitches with the new tier distribution
  - If testing source request prioritization: apply the new filter for 2 weeks and compare win rate
  - If testing reactive pitching: run the competitor response campaign alongside the regular campaign
- Use `posthog-experiments` to create feature flags tracking control vs variant
- Set experiment duration: minimum 14 days or 20+ pitches per variant, whichever is longer
- Log experiment in Attio with: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` to determine: Adopt, Iterate, Revert, or Extend
- If Adopt: update the PR playbook and pitch templates. Log the change.
- If Iterate: generate new hypothesis. Return to Phase 2.
- If Revert: restore previous approach. Log failure. Return to Phase 1.
- Store full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron):**
- Generate weekly optimization brief:
  - Anomalies detected this week
  - Experiments running, completed, decided
  - Net impact on PR-attributed leads
  - Current distance from estimated local maximum
  - Media relationship portfolio health
  - Source request pipeline status
  - Recommended focus for next week
- Post to Slack, store in Attio

### 2. Deploy PR Performance Reporting

Run the `pr-performance-monitor` drill at full scale:

1. Maintain the 5-panel PostHog dashboard (outreach pipeline, placements, referral traffic, attribution, relationships)
2. Keep anomaly detection thresholds recalibrated monthly
3. Weekly and monthly automated reports continue generating
4. Monthly deep-dive includes experiment results and optimization recommendations
5. Quarterly share-of-voice analysis: brand mentions vs competitor mentions

The reporting layer provides the data substrate the optimization loop reads.

### 3. Configure Optimization Guardrails

Apply the guardrails from the `autonomous-optimization` drill:

- **Rate limit:** Maximum 1 active experiment at a time on the PR program
- **Revert threshold:** If PR-attributed leads drop to zero for 3 consecutive weeks during an experiment, auto-revert
- **Human approval required for:**
  - Changing the embargo policy
  - Pitching a Tier 1 outlet with an unproven angle
  - Budget changes exceeding 20% of monthly tool spend
  - Any change affecting 50%+ of active media relationships
  - Changes the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review

### 4. Autonomous Media Relationship Evolution

At Durable level, journalist relationships self-maintain:

1. **Quarterly nurture emails** send automatically via the `analyst-relationship-nurture` pattern: share 2-3 relevant updates with each journalist based on their beat
2. **Relationship scoring auto-updates** in Attio based on: pitches sent, replies received, placements published, social interactions
3. **Stale relationship detection:** If a Tier 1 journalist has not engaged in 2 quarters, auto-generate a re-engagement pitch with a fresh angle
4. **New journalist detection:** When a new journalist starts covering your space (detected via Mention API), auto-add to Clay for enrichment and evaluation

### 5. Monitor Convergence

Track the magnitude of improvement from each adopted experiment:

- If the last 3 consecutive experiments each produced <2% improvement:
  1. The PR program is converged — current performance is near-optimal
  2. Reduce monitoring frequency from daily to weekly
  3. Reduce experiment frequency from 4/month to 1/month (maintenance mode)
  4. Generate a convergence report: "PR program optimized. Current PR-attributed leads/quarter: [X]. Pitch-to-placement rate: [Y]. Further gains require strategic changes (new markets, new product categories, executive hiring for spokesperson diversity, or paid media amplification of earned coverage) rather than tactical optimization."

Post convergence report to Slack and store in Attio.

### 6. Handle Market and Media Shifts

The optimizer should detect external shifts:

- If overall media coverage of your category declines: the topic may be saturated. Test adjacent topic angles or new journalist beats.
- If a major publication shuts down or changes coverage focus: redistribute effort to replacement outlets.
- If AI-generated press releases flood journalist inboxes: differentiate by offering exclusive data, customer access, or in-person meetings.
- If new media platforms emerge (podcasts, newsletters, video): evaluate and test as new placement channels.

## Time Estimate

- 20 hours: Autonomous optimization setup (n8n workflows, PostHog experiments, guardrails)
- 10 hours: PR performance reporting refinement and quarterly share-of-voice analysis
- 5 hours: Media relationship automation tuning
- 90 hours: Ongoing optimization over 12 months (~1.75 hours/week for monitoring, experiments, reactive PR)
- 15 hours: Monthly strategic reviews (12 reviews at ~1.25 hours each)
- 15 hours: Campaign execution and pitch quality maintenance
- 15 hours: Convergence analysis, market shift response, and adaptation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Sequenced media outreach with inbox rotation | $77/mo (Hypergrowth) — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Mention | Brand and competitor monitoring (annual) | $41/mo (Solo) — [mention.com/pricing](https://mention.com/en/pricing/) |
| Qwoted | Source request monitoring (Pro) | $99/mo — [qwoted.com](https://www.qwoted.com) |
| PR Newswire | Press release distribution (occasional) | $300-1,000/release — [prnewswire.com](https://www.prnewswire.com) |
| PostHog | Analytics — dashboards, experiments, anomaly detection | Free up to 1M events — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Automation — optimization loop, opportunity detection, reporting | $60/mo (Pro) — [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | CRM — media contacts, experiment logging, pipeline attribution | $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — monthly media list refresh | $149/mo (Starter) — [clay.com/pricing](https://www.clay.com/pricing) |
| Claude API | Pitch generation, hypothesis generation, experiment evaluation | ~$50-100/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** Instantly ~$77/mo + Mention ~$41/mo + Qwoted ~$99/mo + PR Newswire ~$100/mo amortized = ~$317/mo play-specific. n8n, PostHog, Attio, Clay are standard stack.

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: detect anomalies in PR KPIs, generate hypotheses (pitch angle fatigue, outlet tier mix, source request prioritization, competitor response), run experiments, evaluate results, auto-implement winners. Weekly optimization briefs. Converges when successive experiments produce <2% improvement.
- `pr-performance-monitor` — continuous monitoring of outreach pipeline, placements, referral traffic, placement-to-pipeline attribution, and media relationship health. Provides the data layer the optimization loop reads from.
