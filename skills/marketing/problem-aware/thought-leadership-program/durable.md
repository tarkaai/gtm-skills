---
name: thought-leadership-program-durable
description: >
  Thought Leadership Program — Durable Intelligence. Always-on AI agents autonomously optimize
  content pillars, posting cadence, format mix, repurposing strategy, and speaking pipeline.
  The autonomous-optimization loop detects anomalies, generates hypotheses, runs experiments,
  and auto-implements winners. Weekly optimization briefs track convergence.
stage: "Marketing > ProblemAware"
motion: "FounderSocialContent"
channels: "Social, Content, Events"
level: "Durable Intelligence"
time: "160 hours over 12 months"
outcome: "Sustained >=50 qualified leads/quarter attributed to thought leadership, with <2% variance in successive optimization cycles indicating convergence at the local maximum"
kpis: ["Sustained leads/quarter", "Autonomous experiment win rate", "Content pillar health scores", "Repurposing efficiency trend", "Speaking ROI per event", "Optimization convergence rate"]
slug: "thought-leadership-program"
install: "npx gtm-skills add marketing/problem-aware/thought-leadership-program"
drills:
  - autonomous-optimization
  - thought-leadership-performance-monitor
---

# Thought Leadership Program — Durable Intelligence

> **Stage:** Marketing > ProblemAware | **Motion:** FounderSocialContent | **Channels:** Social, Content, Events

## Outcomes

Always-on AI agents finding the local maximum. The thought leadership program runs autonomously: content generation adapts based on performance data, pillar weights shift based on lead attribution, posting cadence adjusts to audience behavior, repurposing routes to highest-ROI formats, and the speaking pipeline targets events with the best lead yield. The `autonomous-optimization` drill runs the core loop: detect metric anomalies, generate improvement hypotheses, run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs track convergence. The program converges when successive experiments produce <2% improvement.

**Pass threshold:** Sustained >=50 qualified leads/quarter attributed to thought leadership, with <2% variance in successive optimization cycles indicating convergence at the local maximum.

## Leading Indicators

- Autonomous optimization loop runs daily without manual intervention
- Weekly optimization briefs are generated and posted to Slack
- At least 2 experiments per month are initiated, evaluated, and decided
- Content pipeline operates autonomously: drafts generated, founder reviews, posts scheduled, repurposed
- Content-attributed leads per quarter are stable or improving
- Convergence signal: last 3 experiments each produced <2% improvement
- Founder review time stays at or below 45 min/week despite increasing output

## Instructions

### 1. Deploy Autonomous Optimization

Run the `autonomous-optimization` drill configured for the thought leadership program.

**Configure the optimization loop:**

**Phase 1 — Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check thought leadership KPIs:
  - Average engagement rate by pillar (primary signal)
  - Content-attributed leads per week
  - Repurposing conversion rate (source posts -> derivative pieces -> leads)
  - Speaking pipeline health (submissions, acceptances, leads per event)
  - Audience growth rate (followers, newsletter subscribers)
  - Format performance (text vs carousel vs video vs document)
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +-10%), plateau (+-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context from Attio: current pillar weights, posting cadence, active formats, recent speaking events
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with anomaly data and context
- Example hypotheses:
  - "Engagement rate on 'engineering hiring' pillar dropped 25% this week. Hypothesis: audience saturation — 4 posts on this pillar in the last 2 weeks vs typical 2. Test reducing to 1 post/week on this pillar and increasing 'product architecture' pillar."
  - "Content-attributed leads dropped despite stable engagement. Hypothesis: CTA effectiveness declined — last 8 posts used 'comment below' CTA instead of 'DM me for the template' CTA. Test switching 50% of CTAs to direct DM asks."
  - "Video posts consistently get 40% fewer impressions than text posts but 3x more DMs. Hypothesis: video reaches fewer people but converts better. Test increasing video ratio from 1/5 to 2/5 posts."
  - "Speaking-attributed leads at conference X were 10x higher than conference Y despite similar audience sizes. Hypothesis: workshop format produces more leads than keynote. Test submitting only workshop proposals next quarter."
- Store hypotheses in Attio. If risk = "high", alert human. If "low" or "medium", proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Implement the variant:
  - If testing pillar weight: adjust the content generation prompt to shift topic distribution
  - If testing CTA types: alternate CTA styles across posts for 2 weeks, tag each post with CTA type
  - If testing formats: increase/decrease video or carousel ratio in the weekly batch
  - If testing posting cadence: shift schedule (e.g., 4 posts Tu-Fri vs 5 posts Mon-Fri)
  - If testing speaking strategy: submit proposals in the variant format to the next batch of CFPs
- Use `posthog-experiments` to create feature flags tracking control vs variant posts
- Set experiment duration: minimum 14 days or 10+ posts per variant, whichever is longer
- Log experiment in Attio with: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` to determine: Adopt, Iterate, Revert, or Extend
- If Adopt: update the content generation configuration, log the change, move to Phase 5
- If Iterate: generate new hypothesis building on this result, return to Phase 2
- If Revert: restore previous configuration, log failure, return to Phase 1
- Store full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron):**
- Generate weekly optimization brief:
  - Anomalies detected this week
  - Experiments running, completed, decided
  - Net impact on content-attributed leads
  - Current distance from estimated local maximum
  - Content pipeline health: posts in queue, pillar balance, founder review backlog
  - Speaking pipeline status: upcoming events, leads projected
  - Recommended focus for next week
- Post to Slack, store in Attio

### 2. Deploy Thought Leadership Performance Reporting

Run the `thought-leadership-performance-monitor` drill:

1. Maintain the 5-panel PostHog dashboard (content output, engagement, growth, attribution, speaking)
2. Keep the thought leadership event taxonomy current as new channels or formats are added
3. Ensure anomaly detection thresholds are recalibrated monthly based on the rolling 4-week average
4. Weekly automated reports continue generating via n8n
5. Monthly deep-dive reports include experiment results and optimization recommendations

The reporting layer provides the data substrate that the autonomous optimization loop reads. Without accurate reporting, the optimizer cannot generate meaningful hypotheses.

### 3. Configure Optimization Guardrails

Apply the guardrails from the `autonomous-optimization` drill:

- **Rate limit:** Maximum 1 active experiment at a time on the thought leadership program
- **Revert threshold:** If content-attributed leads drop to zero for 2 consecutive weeks during an experiment, auto-revert immediately
- **Human approval required for:**
  - Adding or retiring a content pillar
  - Changing the founder's voice profile
  - Increasing founder review time beyond 45 min/week
  - Changes to posting frequency that exceed +-2 posts/week
  - Speaking commitments requiring >1 day of preparation
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review

### 4. Autonomous Content Pipeline Evolution

At Durable level, the content pipeline self-improves:

1. **Pillar weights auto-adjust** weekly based on the trailing 4-week lead attribution data: pillars that produce more leads get more posts
2. **Format mix evolves** based on engagement-to-lead conversion rates, not just engagement
3. **Hook patterns are tested systematically**: the system rotates through hook types (personal story, data, contrarian, how-to) and tracks which converts best per pillar
4. **Repurposing routes optimize**: if blog posts from LinkedIn source produce more SEO traffic than Twitter threads, shift repurposing effort toward blog
5. **Voice profile updates quarterly**: re-run voice profiling on the latest top-performing posts and update the generation prompt
6. **Founder review becomes curation**: the AI generates high-quality drafts that require less editing over time as the voice model improves

### 5. Monitor Convergence

Track the magnitude of improvement from each adopted experiment:

- If the last 3 consecutive experiments each produced <2% improvement:
  1. The program is converged — current performance is near-optimal
  2. Reduce monitoring frequency from daily to weekly
  3. Reduce experiment frequency from 4/month to 1/month (maintenance mode)
  4. Generate a convergence report: "Thought leadership program optimized. Current leads/quarter: [X]. Engagement rate: [Y]. Further gains require strategic changes (new platforms, new content types, new audience segments, or product positioning changes) rather than tactical optimization."

Post the convergence report to Slack and store in Attio.

### 6. Handle Platform and Market Shifts

The optimizer should detect external shifts:

- If LinkedIn engagement drops across all content types by >20%: algorithm change. Test new post lengths, formats, or engagement strategies.
- If a competitor founder enters the same content space aggressively: competitive response needed. Test differentiating angles or content types the competitor is not using.
- If audience demographics shift (new ICP titles engaging, old ICP titles disengaging): audience evolution. Adjust pillar focus to match new audience needs.
- If a new platform emerges (Threads, Bluesky): evaluate whether the ICP is present. If yes, add as a distribution channel and test.

In these cases: the optimizer flags the situation and recommends whether tactical optimization can address it or whether strategic human intervention is needed.

## Time Estimate

- 20 hours: Autonomous optimization setup (n8n workflows, PostHog experiments, guardrails)
- 8 hours: Performance monitoring dashboard and event taxonomy refinement
- 4 hours: Content pipeline automation tuning
- 80 hours: Ongoing optimization over 12 months (~1.5 hours/week for monitoring, experiment design, evaluation)
- 24 hours: Speaking pipeline management (research, proposals, preparation)
- 12 hours: Monthly strategic reviews (12 reviews at 1 hour each)
- 12 hours: Convergence analysis, platform shift response, and adaptation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Taplio | LinkedIn scheduling + analytics + AI content engine | $49/mo (Standard) — [taplio.com/pricing](https://taplio.com/pricing) |
| Typefully | Twitter/X scheduling | $12/mo — [typefully.com](https://typefully.com) |
| Descript or Loom | Video content repurposing | ~$15-24/mo — [descript.com/pricing](https://www.descript.com/pricing) |
| PostHog | Analytics — dashboards, experiments, anomaly detection | Free up to 1M events — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Automation — optimization loop, content pipeline, reporting | $60/mo (Pro) — [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | CRM — lead tracking, experiment logging, pipeline attribution | $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — CFP research, media research, lead scoring | $149/mo (Starter) — [clay.com/pricing](https://www.clay.com/pricing) |
| Claude API | Content generation, hypothesis generation, experiment evaluation | ~$50-100/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** Taplio ~$49/mo + Typefully ~$12/mo + Descript ~$20/mo + Claude API ~$75/mo = ~$156/mo play-specific. n8n, PostHog, Attio, Clay are standard stack.

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: detect anomalies in thought leadership KPIs, generate hypotheses (pillar saturation, CTA effectiveness, format mix, posting cadence), run experiments, evaluate results, auto-implement winners. Weekly optimization briefs. Converges when successive experiments produce <2% improvement.
- `thought-leadership-performance-monitor` — continuous monitoring of content output, engagement, audience growth, content-to-pipeline attribution, and speaking ROI. Provides the data layer the optimization loop reads from.
