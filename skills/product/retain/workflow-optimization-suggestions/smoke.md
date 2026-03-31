---
name: workflow-optimization-suggestions-smoke
description: >
  AI Workflow Recommendations — Smoke Test. Analyze 10-20 users' behavior patterns manually with PostHog
  and Claude to generate and deliver workflow optimization suggestions. Validate that users act on
  AI-generated recommendations before investing in always-on automation.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥30% suggestion acceptance rate from 10-20 users in 7 days"
kpis: ["Suggestion acceptance rate", "Time-to-adopt (days from delivery to first use)", "User efficiency change (workflow time before vs. after)"]
slug: "workflow-optimization-suggestions"
install: "npx gtm-skills add product/retain/workflow-optimization-suggestions"
drills:
  - workflow-behavior-analysis
---

# AI Workflow Recommendations — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Prove that users will act on AI-generated workflow improvement suggestions. At least 30% of users who receive a suggestion adopt it within 7 days. This validates the core premise: users find value in proactive optimization recommendations based on their actual behavior.

## Leading Indicators

- Users view the suggestion (not just receive it) — targeting 70%+ view rate for in-app delivery
- Users click the CTA in the suggestion — targeting 30%+ click rate among viewers
- At least 1 user provides unsolicited positive feedback about a suggestion
- No users report the suggestions as annoying, irrelevant, or intrusive

## Instructions

### 1. Instrument workflow events in PostHog

Run the `workflow-behavior-analysis` drill, step 1 only (define the workflow event taxonomy). Ensure your product tracks:

- `workflow_started` and `workflow_completed` with `{workflow_type, duration_seconds}`
- `feature_used` with `{feature_name}`
- At least 1 friction signal: `action_undone`, `error_encountered`, or `same_action_repeated`

If events are missing, add them to your product code. Wait 3-5 days for data to accumulate before proceeding.

### 2. Identify your test cohort

In PostHog, find 10-20 users who:
- Have been active for 14+ days (enough behavior data)
- Log in at least 3x per week (will see in-app suggestions)
- Are NOT power users (have room to improve)
- Use at least 1 core workflow regularly

Create a PostHog cohort named `workflow-suggestion-smoke-test` with these users.

### 3. Analyze behavior and generate suggestions

Run the `workflow-behavior-analysis` drill for the smoke cohort:

1. Build the power user benchmark (step 2) — even at smoke level you need a baseline comparison
2. For each of the 10-20 users, run the path analysis (step 3) to identify their workflow inefficiencies
3. Generate AI suggestions for each user (step 5) using Claude. At smoke level, do this manually: run the `ai-workflow-recommendation` API call for each user with their specific behavior data
4. Review each suggestion for quality before delivery. Discard any that feel generic or irrelevant. Each user should have 1-3 specific, actionable suggestions.

**Human action required:** Review all generated suggestions. The AI may produce suggestions that reference features incorrectly or misunderstand the user's context. Edit or reject any that would not make sense to the user.

### 4. Deliver suggestions via Intercom

Run the the workflow suggestion delivery workflow (see instructions below) drill to deliver suggestions:

1. For this smoke test, use Intercom in-app messages only (no email, no bots)
2. Create 1 Intercom in-app post per suggestion, targeted to the specific user by user ID
3. Use this format:
   - Headline: the benefit (e.g., "Save 5 minutes every time you export")
   - Body: 1-2 sentences explaining the suggestion with the quantified benefit
   - CTA: "Try it now" linking to the relevant feature
4. Set display to "show once" and trigger on next session start
5. Log a `suggestion_delivered` event in PostHog for each user with `{suggestion_id, suggestion_category, suggestion_text}`

### 5. Track acceptance over 7 days

Using PostHog, monitor for 7 days:

- `suggestion_delivered` — did the message display?
- Whether the user performed the suggested action within 7 days of delivery (manual check: query PostHog for the specific action event after the delivery timestamp)
- Calculate acceptance rate: users who adopted / users who were delivered

### 6. Evaluate against threshold

**Pass threshold: ≥30% suggestion acceptance rate**

Count: of the 10-20 users who received suggestions, how many performed the suggested action at least once within 7 days?

If PASS (≥30%): Document which suggestion categories (efficiency, discovery, automation) had the highest acceptance. Note the top 3 performing suggestions for reuse at Baseline. Proceed to Baseline.

If FAIL (<30%): Diagnose. Were suggestions irrelevant (wrong feature for the user's workflow)? Were they timed poorly (user did not see them)? Were they too complex (user saw but did not act)? Fix the identified issue and re-run with a fresh cohort.

## Time Estimate

- 2 hours: instrument events and wait for data (may span 3-5 days)
- 1 hour: identify cohort and build power user benchmark
- 1.5 hours: run behavior analysis and generate suggestions for 10-20 users
- 0.5 hours: review suggestions, create Intercom messages
- 1 hour: monitor and evaluate over 7 days (15 min/day spot checks)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Track user behavior, path analysis, event logging | Free tier: 1M events/month ([posthog.com/pricing](https://posthog.com/pricing)) |
| Anthropic Claude API | Generate personalized workflow suggestions | ~$0.10 for 20 users at Sonnet 4.6 ($3/$15 per 1M tokens) ([claude.com/pricing](https://claude.com/pricing)) |
| Intercom | Deliver in-app suggestion messages | From $29/seat/month, includes in-app messaging ([intercom.com/pricing](https://www.intercom.com/pricing)) |

**Estimated Smoke cost: Free** (within PostHog free tier, minimal API usage, assumes existing Intercom seat)

## Drills Referenced

- `workflow-behavior-analysis` — analyze user behavior patterns, build power user benchmark, generate AI suggestions
- the workflow suggestion delivery workflow (see instructions below) — deliver suggestions via Intercom in-app messages, track acceptance
