---
name: ai-personalization-scalable
description: >
  AI Product Personalization — Scalable Automation. Move from static segment rules to
  dynamic per-user personalization with A/B testing and LLM-generated content at 500+ users.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: ">=45% engagement at 500+ users AND dynamic personalization outperforms static by >=5pp"
kpis: ["Personalization engagement rate at scale", "Dynamic vs static engagement lift", "14-day retention rate", "Feature adoption breadth (personalized users)", "LLM email open rate"]
slug: "ai-personalization"
install: "npx gtm-skills add product/retain/ai-personalization"
drills:
  - ab-test-orchestrator
  - personalization-scaling-pipeline
  - churn-prevention
---

# AI Product Personalization — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Personalization engagement rate holds at 45% or higher across 500+ active users. Dynamic per-user variant selection outperforms static segment-based personalization by at least 5 percentage points. LLM-generated email personalization achieves open rates at least equal to the segment-specific template emails. Churn prevention interventions successfully re-engage at least 20% of at-risk personalized users.

## Leading Indicators

- Per-user feature vectors computed daily for all active users
- Dynamic variant selection engine processing 80%+ of sessions
- At least 2 A/B experiments launched and concluded within the first month
- LLM-generated emails pass human quality review (first 50 emails)
- Churn detection workflow identifies at-risk users within 48 hours of usage decline
- No single segment's engagement rate drops below 30% as scale increases

## Instructions

### 1. Launch systematic personalization experiments

Run the `ab-test-orchestrator` drill to test personalization variants systematically:

1. **Experiment 1 — Dashboard personalization:** Test the current segment-based dashboard layout (control) against 2 new variant layouts informed by engagement score and primary workflow data. Hypothesis: "If we adapt the dashboard based on engagement score + workflow rather than segment alone, engagement rate will increase by 5pp because users at different engagement levels need different content density."
2. **Experiment 2 — CTA personalization:** Test segment-based CTAs (control) against dynamic CTAs selected by the activation + plan + engagement combination. Hypothesis: "If we select CTAs based on activation status and engagement score rather than segment alone, CTA click-through will increase by 8pp because the CTA matches the user's current journey stage."
3. **Experiment 3 — Message timing:** Test fixed-schedule Intercom messages (control) against session-behavior-triggered messages. Hypothesis: "If we trigger messages when the user shows a specific behavior pattern (e.g., browsing without acting for 3+ minutes) rather than on a fixed schedule, engagement rate will increase by 10pp because the message arrives at the moment of need."

For each experiment:
- Calculate sample size (minimum 200 per variant)
- Set up PostHog feature flags for variant assignment
- Define primary and secondary metrics
- Set guardrail: if any variant's dismissal rate exceeds 50%, auto-pause
- Document hypothesis, start date, and expected duration in Attio

### 2. Build the dynamic personalization engine

Run the `personalization-scaling-pipeline` drill to move from static rules to dynamic per-user adaptation:

1. **Compute per-user feature vectors** daily: engagement score, behavior segment, primary workflow, feature breadth, collaboration intensity, session recency, personalization engagement rate, activation status, plan type
2. **Deploy the dynamic variant selection engine** in n8n: when a session starts, pull the user's feature vector, apply dynamic selection rules, set PostHog feature flag overrides
3. **Implement the selection logic:** combine segment + engagement score + activation status + recency to pick the best variant for each surface. The rules from the drill give the full decision tree.
4. **Split traffic:** 50% dynamic selection, 50% static segment selection (this IS Experiment 1 from above — run them together)
5. **Log every selection** as `personalization_dynamic_variant_selected` with full context for later analysis

### 3. Scale email personalization with LLM generation

From the `personalization-scaling-pipeline` drill, implement the LLM email pipeline:

1. Build an n8n workflow triggered weekly per user
2. Pull each user's feature vector and recent product activity from PostHog
3. Call the Anthropic Claude API (Haiku 4.5 for cost efficiency) with the structured prompt from the drill — generates an 80-word personalized paragraph referencing specific user behavior
4. Inject the paragraph into a Loops transactional email template
5. Track with `personalization_email_dynamic_sent`, `personalization_email_dynamic_opened`, `personalization_email_dynamic_clicked`

**Human action required:** Review the first 50 LLM-generated emails before enabling full batch. Set up a Slack notification in n8n that posts 5 sample emails daily for ongoing quality spot-checks.

**Guardrail:** If LLM generation fails for a user (API error, content filter), fall back to the segment-specific template email. Log `personalization_email_llm_fallback` events. If fallback rate exceeds 5%, investigate prompt or API issues.

### 4. Integrate churn prevention with personalization

Run the `churn-prevention` drill integrated with the personalization system:

1. Configure churn signal detection: usage decline >50% vs user's own 4-week average, feature abandonment, login gap >7 days, billing page visits
2. Score at-risk users and route to tiered interventions:
   - Low risk: personalized Intercom message highlighting the feature they used most (pull from `primary_workflow`)
   - Medium risk: personalized Loops email with a specific re-engagement hook based on their segment
   - High risk: Attio task for account owner with user's engagement score history and risk signals
3. Track intervention outcomes: `churn_intervention_sent`, `churn_intervention_reengaged`, `churn_intervention_churned`
4. Feed outcomes back into the personalization engine: if a user re-engages after intervention, their personalization surfaces should acknowledge the return (e.g., "Welcome back — here's what's new since your last visit")

### 5. Monitor scale health

Build a PostHog dashboard: "Personalization at Scale" with:
- Total personalized users (target: 500+)
- Engagement rate trend: dynamic vs static
- Per-experiment status: running, concluded, winner implemented
- LLM email performance: volume, open rate, click rate, fallback rate
- Churn intervention pipeline: identified, intervened, re-engaged, churned
- Per-segment engagement rates at current scale

Set n8n alerts for:
- Overall engagement rate drops below 40%
- Any single segment drops below 25%
- Dynamic variant selection engine processes fewer than 80% of sessions
- LLM email fallback rate exceeds 5%

### 6. Evaluate against threshold

At the end of month 2:
- Primary: engagement rate >= 45% at 500+ users
- Primary: dynamic personalization outperforms static by >= 5pp
- Secondary: LLM email open rate >= segment-template open rate
- Secondary: churn intervention re-engagement rate >= 20%
- Guard: no segment below 30% engagement

If PASS, proceed to Durable. If FAIL:
- If engagement dropped at scale: review the dynamic selection rules. The feature vector may need recalibration for the broader user population.
- If dynamic does not beat static: the dynamic rules are not capturing meaningful variation. Simplify to fewer, higher-signal features.
- If LLM emails underperform: review the prompt. It may be generating generic content. Add more specific user data to the prompt context.

## Time Estimate

- 10 hours: A/B test design, setup, monitoring, and analysis (3 experiments)
- 15 hours: dynamic variant selection engine build and deployment
- 10 hours: LLM email pipeline build, testing, and human review
- 8 hours: churn prevention integration with personalization
- 4 hours: dashboard build, alert configuration, and monitoring
- 3 hours: final evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, experiments, feature flags, cohorts | Free 1M events/mo. Paid: ~$0.00005/event. At 500 users: likely $50-150/mo. [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app messages, product tours, churn interventions | Advanced: $85/seat/mo. Proactive Support add-on: $349/mo. [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Segment + LLM-personalized email sequences | $49-79/mo depending on contact volume. [loops.so/pricing](https://loops.so/pricing) |
| Anthropic Claude API | LLM content generation for personalized emails | Haiku 4.5: $1/MTok input, $5/MTok output. At 500 users/week: ~$5-15/mo. [claude.com/pricing](https://claude.com/pricing) |
| n8n | Automation pipelines (segmentation, scoring, variant selection, emails) | Cloud: $24-60/mo depending on execution volume. [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | CRM for scores, segments, experiment tracking, churn tasks | $29/seat/mo. [attio.com/pricing](https://attio.com/pricing) |

**Estimated play-specific cost at Scalable:** $200-500/mo (Intercom Advanced + Proactive Support + Loops + Claude API + n8n)

## Drills Referenced

- `ab-test-orchestrator` — design, run, and analyze 3 personalization experiments
- `personalization-scaling-pipeline` — build dynamic per-user variant selection and LLM email generation
- `churn-prevention` — detect at-risk users and trigger personalized retention interventions
