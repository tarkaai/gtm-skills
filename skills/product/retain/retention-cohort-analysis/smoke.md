---
name: retention-cohort-analysis-smoke
description: >
  Retention Cohort Analytics — Smoke Test. Run a single cohort retention extraction, generate
  10 structured insights from the data, and validate that cohort analysis surfaces actionable
  retention patterns your team did not already know.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "10 cohort analyses with 3+ novel insights"
kpis: ["Cohorts analyzed", "Divergent cohorts identified", "Novel insights generated"]
slug: "retention-cohort-analysis"
install: "npx gtm-skills add product/retain/retention-cohort-analysis"
drills:
  - cohort-retention-extraction
  - cohort-insight-generation
  - threshold-engine
---

# Retention Cohort Analytics — Smoke Test

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Prove the concept: can you extract retention data by cohort from PostHog, identify divergent cohorts, and generate insights your team did not already have? No automation, no always-on. A single agent run that produces a structured retention analysis and validates that cohort-level data reveals patterns invisible in aggregate metrics.

Pass threshold: 10 cohort analyses completed with at least 3 novel insights (insights the team was not already aware of and that map to a specific intervention).

## Leading Indicators

- PostHog retention query returns data for 8+ weekly cohorts (data coverage is sufficient)
- At least 2 cohorts are flagged as divergent from the population baseline (the data is not uniform — there are patterns to find)
- Insight generation produces hypotheses with "high" or "medium" confidence (the data supports root-cause analysis, not just speculation)

## Instructions

### 1. Verify PostHog data readiness

Confirm your PostHog project has at least 8 weeks of tracked user events. Run a data coverage check via PostHog API or MCP:

```
SELECT
  dateTrunc('week', person.created_at) AS signup_week,
  count(distinct distinct_id) AS users
FROM events
WHERE person.created_at > now() - interval 12 week
GROUP BY signup_week
ORDER BY signup_week
```

You need at least 8 weekly cohorts with 20+ users each. If fewer than 8 cohorts meet the minimum, wait until more data accumulates or lower the cohort threshold to 10 users (accept noisier results).

### 2. Choose your retention event

Decide which event signals a retained user. Options in order of preference:

1. **Core feature event** (e.g., `project_created`, `report_generated`, `message_sent`) — best signal of real engagement
2. **Session event** (e.g., `session_started`, `$pageview`) — acceptable floor if core features are not instrumented
3. **Login event** — weakest signal; users who log in but do nothing are not truly retained

Document your choice. This becomes the standard retention event for all future runs.

### 3. Run cohort retention extraction

Execute the `cohort-retention-extraction` drill with these parameters:
- Cohort dimension: signup week
- Retention event: your chosen event from step 2
- Time window: 12 weeks (or maximum available)
- Retention intervals: Week 1 through Week 8

The drill produces a structured JSON with cohort survival data, population baseline, and divergent cohort flags.

**Human action required:** Review the extraction output. Check that the cohort sizes are reasonable and the retention percentages are plausible for your product. If Week 1 retention is >90% or <10% for most cohorts, your retention event may be too broad or too narrow — adjust and re-run.

### 4. Generate insights from the cohort data

Run the `cohort-insight-generation` drill on the extraction output. The drill classifies divergent cohorts by pattern (activation gap, habit failure, value plateau, consistent outperformer), investigates root causes using PostHog user path analysis, and generates ranked hypotheses with intervention recommendations.

Review the output. For each insight, answer:
- Is this something the team already knew? (If yes, it does not count toward the 3 novel insights threshold)
- Is the intervention recommendation specific enough for an agent to execute? (If not, refine it)
- Does the confidence level match the data strength? (Reject insights based on <20 users as low-confidence)

### 5. Evaluate against threshold

Run the `threshold-engine` drill to verify:
- **Quantity check:** Did you analyze 10+ cohorts? Count the cohorts in the extraction output.
- **Quality check:** Did you generate 3+ novel insights? Count insights marked as novel (not previously known to the team).
- **Actionability check:** Does each novel insight have a specific, executable intervention recommendation?

If PASS (10+ cohorts, 3+ novel insights), document the findings and proceed to Baseline. If FAIL:
- If <10 cohorts: wait for more data or switch to a broader retention event
- If <3 novel insights: run the extraction with additional cohort dimensions (acquisition channel, plan type) to find patterns signup-week alone does not reveal

### 6. Document findings

Record in Attio:
- Total cohorts analyzed
- Population baseline retention curve (Week 1 through Week 8)
- Divergent cohorts and their patterns
- Top 3-5 insights ranked by priority score
- Recommended next steps for Baseline

## Time Estimate

- 1 hour: verify PostHog data readiness and choose retention event
- 1.5 hours: run cohort retention extraction and review output
- 1.5 hours: run insight generation and evaluate hypotheses
- 0.5 hours: threshold evaluation and documentation
- 0.5 hours: document findings and plan Baseline

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Retention data extraction, cohort queries, user path analysis | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API (Claude) | Hypothesis generation from cohort data | ~$0.50-2.00 for a single analysis run — [anthropic.com/pricing](https://anthropic.com/pricing) |

**Estimated cost for Smoke: Free** (PostHog free tier + <$2 in API calls)

## Drills Referenced

- `cohort-retention-extraction` — extracts cohort survival data from PostHog, computes population baseline, and flags divergent cohorts
- `cohort-insight-generation` — analyzes divergent cohorts, generates root-cause hypotheses, and produces ranked intervention recommendations
- `threshold-engine` — evaluates whether the analysis meets the pass threshold (10 cohorts, 3+ novel insights)
