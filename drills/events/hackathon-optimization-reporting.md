---
name: hackathon-optimization-reporting
description: Durable-level reporting that tracks autonomous optimization experiments, challenge design evolution, and developer community health for the hackathon series
category: Events
tools:
  - PostHog
  - n8n
  - Attio
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-experiments
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-reporting
  - attio-lists
  - hypothesis-generation
  - experiment-evaluation
---

# Hackathon Optimization Reporting

This drill generates the play-specific reporting layer for the hackathon series at Durable level. While `autonomous-optimization` handles the generic monitor-diagnose-experiment-evaluate loop, this drill produces hackathon-specific insights: challenge design evolution, developer community health, cross-hackathon A/B test results, and product adoption funnel analysis.

## Prerequisites

- Hackathon series running at Scalable level for at least 2 quarters (4+ completed hackathons)
- `autonomous-optimization` drill deployed and running
- `hackathon-performance-monitor` drill running and producing data
- PostHog with full hackathon funnel tracking
- Anthropic API key for insight generation

## Steps

### 1. Track experiment history and challenge evolution

Using `attio-lists`, maintain an "Optimization Experiment Log" with fields:

- Experiment name, hypothesis, start date, end date
- Variable tested: challenge_design / prize_structure / recruitment_channel / nurture_sequence / format / duration / support_model
- Control description, variant description
- Result: adopted / reverted / iterated / extended
- Impact: metric changed, magnitude, confidence level

Using `n8n-scheduling`, run a weekly workflow that:

1. Pulls all active and recently completed experiments from the log
2. For each active experiment, checks if it has reached the minimum sample size or duration
3. For completed experiments, summarizes the result and net impact
4. Generates a "Challenge Design Evolution" timeline showing how the hackathon format has changed over time due to adopted experiments

### 2. Build the developer community health report

Hackathons are unique among GTM plays because they build a durable developer community. Track community health metrics separately from pipeline metrics:

Using `posthog-custom-events` and `n8n-workflow-basics`:

- **Community size**: Total members in Discord/Slack, trend over time
- **Active ratio**: % of members who posted or reacted in the last 30 days (target: >15%)
- **Hackathon alumni retention**: % of past hackathon participants still active in the community (target: >30% at 6 months)
- **Organic project sharing**: Number of projects shared in the community that were NOT part of a hackathon (indicates the community has a life beyond events)
- **Help request resolution rate**: % of technical questions that get a community answer within 24 hours (target: >70%)
- **Community-to-customer pipeline**: Deals where the first touchpoint was community participation (not hackathon directly)

Generate a monthly community health report:

```
## Developer Community Health -- {Month Year}

### Size: {N} members (+{N} this month, +{X}% growth)
### Active Ratio: {X}% (target: >15%)
### Alumni Retention (6mo): {X}% (target: >30%)

### Engagement Breakdown
| Activity | Count | Trend |
|----------|-------|-------|
| Messages sent | {N} | {trend} |
| Projects shared | {N} | {trend} |
| Help requests | {N} | {trend} |
| Help requests resolved <24h | {N} ({X}%) | {trend} |

### Community-Sourced Pipeline: {N} deals, ${X} value
### Top Contributors This Month: {names}

### Health: {GREEN/YELLOW/RED}
{Assessment and recommendations}
```

### 3. Generate cross-hackathon A/B test insights

The autonomous optimization loop tests variables across hackathons. This step synthesizes cross-event learnings:

Using `hypothesis-generation` and `experiment-evaluation`:

1. After every 2 hackathons, compile all experiment results from the period
2. Group experiments by variable category (challenge design, prize structure, etc.)
3. Generate a synthesis report:

```
## Cross-Hackathon Optimization Insights -- {Period}

### Challenge Design Insights
- {Finding from experiments}: "{description}" -> {impact on registration, submission, or pipeline}
- {Finding}: ...

### Recruitment Insights
- {Finding from experiments}: "{description}" -> {impact}

### Nurture Insights
- {Finding}: ...

### Prize Structure Insights
- {Finding}: ...

### Meta-Learning
- Variables with highest optimization ROI: {list -- which variables had the biggest impact when changed?}
- Variables near convergence: {list -- where are experiments producing diminishing returns?}
- Unexplored variables: {list -- what has not been tested yet that could be high-impact?}
```

### 4. Product adoption funnel deep-dive

Hackathons generate a unique product adoption signal: developers who build something with your product during time pressure. Track post-hackathon product behavior:

Using `posthog-dashboards` and `posthog-custom-events`:

- **Hackathon-to-activation funnel**: hackathon_registered -> hackathon_submitted -> product_signup -> product_activated -> product_retained_30d -> product_paid
- **Feature adoption by hackathon theme**: Which product features get the most post-hackathon usage? Does this vary by challenge theme?
- **Time-to-paid**: Median days from hackathon to paid conversion, by tier
- **Cohort retention**: 30/60/90 day retention for hackathon-sourced users vs other acquisition channels

Generate a quarterly product adoption report comparing hackathon-sourced users to other channels.

### 5. Generate weekly optimization briefs

Using `n8n-scheduling` and the Anthropic API, generate a weekly brief specific to the hackathon play:

```
## Hackathon Optimization Brief -- Week of {date}

### Active Experiments
- {experiment_name}: Testing {variable}. Status: {running/evaluating}. {days remaining or preliminary results}

### Decisions Made This Week
- {experiment_name}: {adopted/reverted/iterated}. Net impact: {metric} changed by {amount}

### Funnel Health
| Stage | Current | Target | vs Average | Status |
|-------|---------|--------|------------|--------|
| Registration | {N} | {N} | {pct}% | {status} |
| Submission rate | {pct}% | 40% | {pct}% | {status} |
| Qualified leads | {N} | {N} | {pct}% | {status} |
| Product adoption (30d) | {pct}% | 25% | {pct}% | {status} |
| Paid conversion (60d) | {pct}% | 5% | {pct}% | {status} |

### Community Pulse
- Active ratio: {pct}%
- New members this week: {N}
- Notable activity: {any standout community events or contributions}

### Convergence Status
- Consecutive experiments with <2% improvement: {count}/3
- Variables converged: {list}
- Estimated distance from local maximum: {assessment}

### Recommended Focus Next Week
- {recommendation based on data}
```

Post to Slack and store in Attio.

## Output

- Weekly optimization briefs with hackathon-specific context
- Monthly developer community health reports
- Cross-hackathon A/B test synthesis reports
- Product adoption funnel analysis comparing hackathon-sourced users to other channels
- Challenge design evolution timeline

## Triggers

- Weekly optimization briefs: every Monday via n8n cron
- Community health reports: 1st of each month
- Cross-hackathon synthesis: after every 2 hackathons
- Product adoption report: quarterly
