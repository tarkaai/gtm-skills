---
name: stack-overflow-presence-durable
description: >
  Stack Overflow Presence — Durable Intelligence. Always-on AI agents find the local maximum
  of SO authority and lead generation. The autonomous-optimization loop monitors answer
  performance, generates improvement hypotheses, runs A/B experiments on answer strategies,
  evaluates results, and auto-implements winners. Weekly optimization briefs track convergence.
stage: "Marketing > SolutionAware"
motion: "CommunitiesForums"
channels: "Communities"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained answer volume and ≥15 qualified leads/quarter over 12 months via autonomous AI optimization of answer strategy, tag allocation, and referral capture"
kpis: ["Sustained weekly answer volume", "Answer quality trend (avg score)", "Quarterly qualified leads", "AI experiment win rate", "Reputation growth rate", "Referral conversion rate trend", "Cost per qualified lead trend"]
slug: "stack-overflow-presence"
install: "npx gtm-skills add CommunitiesForums/Marketing/SolutionAware/stack-overflow-presence"
drills:
  - autonomous-optimization
---
# Stack Overflow Presence — Durable Intelligence

> **Stage:** Marketing → SolutionAware | **Motion:** CommunitiesForums | **Channels:** Communities

## Overview
Stack Overflow Presence — Durable Intelligence. Always-on AI agents find the local maximum of SO authority and lead generation. The autonomous-optimization loop monitors answer performance, generates improvement hypotheses, runs A/B experiments on answer strategies, evaluates results, and auto-implements winners. Weekly optimization briefs track convergence.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained answer volume and ≥15 qualified leads/quarter over 12 months via autonomous AI optimization of answer strategy, tag allocation, and referral capture

---

## Budget

**Play-specific tools & costs**
- **Anthropic API (Claude):** ~$30-80/mo for answer drafting + optimization analysis
- **Syften:** $20-100/mo for real-time question detection
- **Agent compute costs:** Variable based on optimization loop frequency

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for this play's metrics. The optimization loop operates in five phases:

**Phase 1 — Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check this play's primary KPIs: weekly answer volume, average upvote score, acceptance rate, referral sessions, qualified leads
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within ±10%), plateau (±2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Pull the current answering configuration from Attio: active tags, answer volume per tag, AI prompt versions, link strategy, posting schedule
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data and SO-specific context
- Receive 3 ranked hypotheses. Examples of SO-specific hypotheses:
  - "Answer quality dropped because we expanded into tags outside core expertise. Test: restrict to top 5 tags for 2 weeks."
  - "Referral traffic declined because link format changed. Test: revert to inline documentation links vs. end-of-answer links."
  - "Acceptance rate plateaued because we answer questions too late. Test: reduce monitoring interval from 30min to 15min."
- Store hypotheses in Attio. If top hypothesis is high-risk, alert human and stop.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment using `posthog-experiments`: create a feature flag that splits the answering pipeline between control (current strategy) and variant (hypothesis change)
- Implementation examples:
  - Tag reallocation: route 50% of answer budget to variant tag set
  - Prompt change: use variant system prompt for 50% of drafted answers
  - Timing change: post variant answers at different times of day
- Minimum duration: 14 days or 50+ answers per variant, whichever is longer
- Log experiment start in Attio

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` with control vs. variant metrics
- Decision: Adopt (implement winner permanently), Iterate (refine hypothesis), Revert (restore control), or Extend (keep running)
- Store full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes
- Generate weekly optimization brief:
  - What changed and why
  - Net impact on primary KPIs
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

### 2. Deploy SO authority monitoring

Run the the so authority monitoring workflow (see instructions below) drill to maintain a live scorecard of:
- Reputation growth trajectory and per-tag ranking
- Answer performance trends (score distribution, acceptance patterns)
- Referral attribution from SO to pipeline
- Badge progress (tag badges signal deep authority)

The authority metrics feed directly into the autonomous optimization loop. When the optimization agent detects a reputation stall or quality drop, it generates hypotheses specific to SO's ecosystem (tag selection, answer timing, code quality, explanation depth).

### 3. Implement advanced optimization strategies

Beyond the standard optimization loop, configure these SO-specific experiments:

**Answer timing optimization:**
- Test posting at different times of day (questions answered within 1 hour of posting get 3x more visibility)
- Track time-from-question-posted-to-answer-posted vs. upvote score
- Find the optimal response window per tag

**Answer format A/B testing:**
- Test answer structures: code-first vs. explanation-first
- Test answer lengths: concise (150 words) vs. comprehensive (500 words)
- Test inclusion of diagrams/ASCII art for architecture questions
- Track which formats earn the most upvotes per tag

**Tag portfolio rebalancing:**
- Monthly: compute ROI per tag (qualified leads + reputation earned / time invested)
- Shift answer budget from low-ROI to high-ROI tags
- Test emerging tags quarterly (new frameworks, new tools)

**Referral funnel optimization:**
- A/B test documentation landing pages for top SO referral sources
- Optimize the SO profile bio and "About Me" section for click-through
- Test whether answers with links to open-source tools convert better than links to documentation

### 4. Detect convergence

The optimization loop runs indefinitely. However, it detects convergence — when successive experiments produce diminishing returns (<2% improvement for 3 consecutive experiments). At convergence:

1. The play has reached its local maximum for current market conditions
2. Reduce monitoring frequency from daily to weekly
3. Report: "Stack Overflow presence is optimized. Current performance: [metrics]. Further gains require strategic changes (new product capabilities, entering new technology categories, or major SO algorithm changes) rather than tactical optimization."
4. Continue monitoring for external disruptions (SO policy changes, competitor activity, tag ecosystem shifts) that could shift the local maximum

### 5. Maintain long-term sustainability

**Reputation protection:**
- Monitor for SO quality bans or rate-limit warnings
- Maintain a downvote rate below 5% across all answers
- If any moderator action occurs, pause all automated posting and investigate

**Community standing:**
- Earn tag badges (bronze, silver, gold) in primary tags — these signal permanent authority
- Contribute to tag wiki edits and documentation improvements (builds goodwill)
- Occasionally answer questions purely for community value (no lead gen angle)

**Market adaptation:**
- When new technologies emerge in your domain, proactively add those tags
- When a technology your ICP uses is deprecated, shift away from those tags
- Track Stack Overflow Trends (https://insights.stackoverflow.com/trends) for tag volume shifts

---

## KPIs to track
- Sustained weekly answer volume
- Answer quality trend (avg score)
- Quarterly qualified leads
- AI experiment win rate
- Reputation growth rate
- Referral conversion rate trend
- Cost per qualified lead trend

---

## Pass threshold
**Sustained answer volume and ≥15 qualified leads/quarter over 12 months via autonomous AI optimization of answer strategy, tag allocation, and referral capture**

This level runs continuously. Review monthly: what experiments ran, what improved, what to test next. The play is durable when it maintains performance with decreasing human oversight.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add CommunitiesForums/Marketing/SolutionAware/stack-overflow-presence`_
