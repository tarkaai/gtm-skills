---
name: ai-onboarding-coach-baseline
description: >
  AI Onboarding Coach — Baseline Run. Run the AI coach always-on for all new signups
  with full proactive suggestion engine, coach-vs-control A/B test, and detailed
  analytics. Pass threshold: >= 55% coach engagement AND >= 10pp activation lift
  for coach-engaged users over control group.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "20 hours over 3 weeks"
outcome: ">= 55% coach engagement AND >= 10pp activation lift over control"
kpis: ["Coach engagement rate", "Activation lift (coach vs control)", "Coach resolution rate", "Time to activation (coach-engaged)", "Proactive suggestion CTR"]
slug: "ai-onboarding-coach"
install: "npx gtm-skills add product/onboard/ai-onboarding-coach"
drills:
  - posthog-gtm-events
  - ai-coach-conversation-design
  - activation-optimization
---

# AI Onboarding Coach — Baseline Run

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Run the AI coaching surface always-on for all new signups. Deploy the full proactive suggestion engine via n8n. Run a controlled A/B test: 50% of new users get the AI coach, 50% get the standard onboarding flow without the coach. Measure whether the coach produces a statistically significant activation lift. Pass threshold: >= 55% coach engagement rate in the treatment group AND >= 10 percentage point activation lift for coach-engaged users vs the control group.

## Leading Indicators

- Coach engagement rate reaches 55% within the first week of always-on deployment
- Proactive suggestion click-through rate holds at >= 8% (validates the trigger rules from Smoke)
- Coach resolution rate holds at >= 60% at scale (no quality degradation as volume increases)
- Time to activation for coach-engaged users is measurably shorter than control (even before the full 3-week evaluation)
- Fin unanswered query volume does not spike — knowledge base covers the new user volume
- Human handoff rate stays below 35%

## Instructions

### 1. Instrument detailed coach analytics

Run the `posthog-gtm-events` drill to set up granular tracking for the coach:

Events to configure:
- `ai_coach_impression` — coach appeared (proactive suggestion shown or Fin greeting displayed). Properties: `trigger_type` (greeting/stuck/stall/discovery), `onboarding_step`, `persona_type`
- `ai_coach_engaged` — user interacted with the coach (clicked suggestion, typed a question, followed a deep link). Properties: `trigger_type`, `engagement_type` (click/question/deep_link), `persona_type`
- `ai_coach_resolved` — coach conversation completed. Properties: `resolution_type` (fin_resolved/human_handoff/abandoned), `turns`, `topic`, `persona_type`
- `ai_coach_suggestion_shown` — proactive suggestion surfaced. Properties: `suggestion_type` (stuck/stall/discovery), `suggestion_content_id`, `onboarding_step`
- `ai_coach_suggestion_clicked` — user clicked a proactive suggestion. Properties: `suggestion_type`, `suggestion_content_id`
- `ai_coach_suggestion_dismissed` — user dismissed a proactive suggestion. Properties: `suggestion_type`, `suggestion_content_id`

Build PostHog funnels:
- `signup_completed` -> `ai_coach_impression` -> `ai_coach_engaged` -> `activation_reached`
- `ai_coach_suggestion_shown` -> `ai_coach_suggestion_clicked` -> `activation_reached`

### 2. Deploy the full AI coach with proactive engine

Run the `ai-coach-conversation-design` drill at full scope:

1. **Expand the knowledge base**: Based on Smoke test data, add custom Fin answers for every question pattern that appeared 2+ times. Fill any content gaps identified during the Smoke monitoring.

2. **Build the proactive suggestion engine**: Deploy the n8n pipeline from the drill. Configure all three trigger categories:
   - **Stuck triggers**: Error spikes, repeated retries, rage clicks, long dwell on setup pages
   - **Stall triggers**: Milestone gaps (24h+), sessions without progress, abandoned setup flows
   - **Discovery triggers**: Post-activation feature suggestions based on persona

3. **Set up the A/B test**: Create a PostHog feature flag `ai-onboarding-coach-enabled` with 50/50 split:
   - **Treatment (50%)**: Full AI coach — Fin enabled, proactive suggestions active, contextual triggers firing
   - **Control (50%)**: Standard onboarding only — product tours, email sequence, checklists, but NO AI coach surface
   - Assign at signup so users stay in the same group for their entire onboarding

4. **Ensure the control group still gets standard onboarding**: The control must receive the same onboarding tours, emails, and checklists as before. The ONLY difference is the AI coach layer. This isolates the coach's incremental value.

### 3. Run the A/B test and optimize

Run the test for a minimum of 3 weeks or until 100+ users per group complete the 7-day onboarding window, whichever is longer.

During the test, run the `activation-optimization` drill on the treatment group only:
- Analyze the PostHog coach funnel to find where users drop off after coach engagement
- If coach resolution rate drops below 55%, immediately audit Fin's unanswered queue and add missing content
- If proactive suggestion CTR drops below 5%, reduce suggestion frequency or refresh copy
- Track which proactive trigger types drive the highest activation rates and concentrate on those

Weekly analysis:
- Compare activation rates: treatment vs control
- Compare time to activation: treatment vs control
- Compute coach engagement rate within the treatment group
- Review top unanswered coach queries and fill gaps

### 4. Evaluate against threshold

Measure at the end of the test period:

- **Coach engagement rate**: >= 55% of treatment group users engaged the coach at least once. This proves users find the coach accessible and relevant.
- **Activation lift**: Treatment group activation rate >= 10 percentage points above control group. This proves the coach causes higher activation, not just correlates with it.

Decision tree:
- **Pass (both thresholds met):** Proceed to Scalable. Document: which trigger types drive highest activation lift, most common coach queries, resolution rate by topic, and the measured activation lift with confidence interval.
- **Partial pass (engagement met but lift < 10pp):** The coach is used but is not moving the needle on activation. Investigate: Are coach answers leading to action? Do responses include deep links and clear next steps? The coach may be answering questions but not motivating behavior change. Iterate on response quality and proactive suggestion targeting.
- **Partial pass (lift met but engagement < 55%):** The coach helps those who use it, but most users do not find it. Investigate: Is the Messenger widget prominent enough? Are proactive triggers firing reliably? Is the greeting copy compelling? Increase coach visibility and re-test.
- **Fail (neither met):** Re-examine whether the coach knowledge base is comprehensive enough, whether proactive triggers fire at the right moments, and whether the product's onboarding has enough complexity to benefit from an AI coach.

## Time Estimate

- 4 hours: Detailed analytics instrumentation and funnel setup
- 6 hours: Full proactive suggestion engine deployment (n8n pipelines, trigger configuration)
- 2 hours: A/B test setup and validation
- 2 hours: Knowledge base expansion from Smoke learnings
- 6 hours: Weekly monitoring and optimization over 3 weeks (2 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom (Fin AI Agent) | AI coaching surface — answers questions, proactive nudges | $0.99/resolution; ~$80-200/mo at 100-200 onboarding users |
| Loops | Lifecycle email sequences for control group onboarding | Free tier or ~$25/mo |

_CRM (Attio), automation (n8n), and PostHog are standard stack — not counted as play-specific costs._

## Drills Referenced

- `posthog-gtm-events` — sets up the detailed event schema for coach impressions, engagements, resolutions, and proactive suggestion tracking
- `ai-coach-conversation-design` — deploys the full coach: expanded knowledge base, n8n proactive suggestion engine, all trigger categories, and conversation flows
- `activation-optimization` — identifies activation funnel drop-offs in the treatment group and systematically improves the coach's ability to convert engagement into activation
