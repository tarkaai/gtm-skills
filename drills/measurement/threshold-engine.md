---
name: threshold-engine
description: Define pass/fail thresholds and guardrails for every GTM play to enforce data-driven progression
category: Measurement
tools:
  - PostHog
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - n8n-triggers
  - n8n-workflow-basics
---

# Threshold Engine

This drill builds the system that decides whether a GTM play passed or failed at each level. Every play has a threshold — a measurable outcome that must be hit before progressing to the next level. The threshold engine checks results against these criteria and recommends the next action.

## Prerequisites

- PostHog tracking events from the play being measured (run `posthog-gtm-events` drill first)
- n8n instance for automated checking
- Clear understanding of the play's expected outcomes at each level

## Steps

### 1. Define thresholds per play level

Every play at every level needs a pass/fail threshold. Framework:

- **Smoke (manual, small scale)**: Did it work at all? Example: "2+ meetings from 20 cold emails" or "5+ signups from first landing page."
- **Baseline (tool-assisted, medium scale)**: Is it repeatable? Example: "10+ meetings from 100 cold emails with <$50 cost per meeting."
- **Scalable (automated, large scale)**: Does it scale profitably? Example: "50+ meetings/month with CPA below $40 and no manual intervention."
- **Durable (self-optimizing)**: Does it sustain? Example: "Maintains 50+ meetings/month for 3 consecutive months with CPA trending down."

Thresholds must be specific numbers, not vague goals. "Good response rate" is not a threshold. "12%+ reply rate" is.

### 2. Implement threshold checks in PostHog

Using `posthog-funnels`, create saved insights for each threshold. For a cold email play at Smoke level:

- Query: emails sent in last 14 days where source = "cold-email-sequence"
- Funnel: email_sent -> email_opened -> email_replied -> meeting_booked
- Threshold check: meeting_booked count >= 2

Save each insight with a clear name: "[Play Name] - [Level] - Threshold Check"

### 3. Build automated threshold checking

Using the `n8n-triggers` fundamental, create a workflow that runs at the end of each play's evaluation period. The workflow:

1. Queries PostHog for the relevant metrics
2. Compares results against the threshold
3. Generates a pass/fail verdict with the specific numbers
4. Sends the result to the team (Slack, email, or Attio note)

Using `n8n-workflow-basics`, handle edge cases: insufficient data (not enough time or volume to judge), partial pass (some metrics hit but others missed), and external factors (holiday weeks, product outage).

### 4. Define guardrails

Guardrails are "never exceed" limits that protect against damage even when a play is performing well:

- **Budget guardrail**: Never spend more than 120% of allocated budget
- **Volume guardrail**: Never send more than X emails/day to protect domain reputation
- **Quality guardrail**: If negative reply rate exceeds 5%, pause and review messaging
- **Compliance guardrail**: Unsubscribe rate above 1% triggers immediate pause

Guardrails fire n8n alerts using `n8n-triggers` and can automatically pause campaigns when breached.

### 5. Build the progression decision tree

When a threshold check completes, the engine recommends one of four actions:

- **Pass -> Advance**: Metrics exceeded threshold. Move to the next level. Document what worked.
- **Marginal Pass -> Optimize**: Metrics barely met threshold. Stay at current level, optimize, and re-check in one more cycle.
- **Fail -> Iterate**: Metrics missed threshold. Diagnose why (messaging, targeting, timing, offer), make changes, and re-run at the same level.
- **Hard Fail -> Pivot**: Metrics dramatically missed threshold after 2+ attempts. The play may not work for your market. Try a different play.

### 6. Track threshold results over time

Using `posthog-custom-events`, log every threshold check result as an event: play name, level, metrics achieved, threshold target, and verdict. Over time, this builds a dataset showing which plays work for your business and at which levels. This data informs future play selection and budget allocation.
