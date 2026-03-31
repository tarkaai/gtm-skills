---
name: ai-onboarding-coach-smoke
description: >
  AI Onboarding Coach — Smoke Test. Deploy an AI coaching surface inside the product
  that answers new user questions and proactively suggests next steps during onboarding.
  Test with 20-50 users. Pass threshold: >= 45% of test users engage the AI coach at
  least once during their first 7 days.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">= 45% of test cohort engage the AI coach at least once during onboarding"
kpis: ["Coach engagement rate", "Coach resolution rate", "Activation rate (coach-engaged vs control)", "Time to first coach interaction"]
slug: "ai-onboarding-coach"
install: "npx gtm-skills add product/onboard/ai-onboarding-coach"
drills:
  - onboarding-flow
  - ai-coach-conversation-design
  - threshold-engine
---

# AI Onboarding Coach — Smoke Test

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Deploy an AI coaching surface (Intercom Fin) inside the product that answers new user questions and proactively nudges users toward activation during onboarding. Run for 7 days with 20-50 new signups. Pass threshold: >= 45% of test users engage the AI coach at least once during their first 7 days.

## Leading Indicators

- At least 5 users initiate a conversation with the AI coach in the first 3 days (demand signal)
- Coach resolution rate >= 50% (Fin answers questions without human handoff)
- Users who engage the coach progress further through the onboarding funnel than those who do not (even directionally, exact lift measured at Baseline)
- Proactive coach suggestions get >= 10% click-through rate (users find the nudges relevant)
- Zero critical user complaints about the AI coach giving wrong or misleading answers

## Instructions

### 1. Ensure the onboarding flow and tracking are in place

Run the `onboarding-flow` drill to confirm your onboarding milestones are defined, PostHog funnel events are firing, and Intercom is installed with user properties synced. The AI coach layer sits on top of the existing onboarding flow — it supplements tours and emails with an interactive AI surface.

If your onboarding flow is already running, verify these PostHog events fire correctly: `signup_completed`, `milestone_N_completed` (for each onboarding step), `activation_reached`. Verify Intercom receives `persona_type`, `onboarding_stage`, and `days_since_signup` as user properties.

### 2. Design and deploy the AI coach

Run the `ai-coach-conversation-design` drill. For the smoke test, focus on the minimum viable coach:

1. **Knowledge base**: Audit your Intercom Help Center. Ensure articles exist for every onboarding step. Write custom Fin answers for the 10 most common onboarding questions (pull from Intercom conversation history or support tickets).

2. **Fin configuration**: Enable Intercom Fin on all product pages where onboarding happens. Set the greeting for new users: "Need help getting set up? Ask me anything." Configure handoff to human after 2 failed attempts.

3. **Proactive triggers**: Implement 2-3 stuck triggers only — fire a proactive coach suggestion when:
   - User encounters 3+ errors in 5 minutes
   - User has been on a setup page for > 3 minutes without completing the expected action
   - User returns for a second session without having progressed since their first session

4. **Tracking**: Instrument `ai_coach_impression`, `ai_coach_engaged`, `ai_coach_resolved` events in PostHog with `trigger_type` and `persona_type` properties.

Do NOT build the full proactive suggestion engine or n8n pipelines yet — those come at Baseline. For smoke, the coach is Fin with a good knowledge base plus 2-3 simple proactive triggers.

**Human action required:** Review all custom Fin answers before enabling for real users. Test every onboarding question manually — ask the coach as a test user and verify the answers are correct, specific, and include deep links to the right product pages. Enable the coach only after manual review passes.

### 3. Run the test for 7 days

Launch the coach for the next 20-50 new signups. During the test:

- Monitor PostHog Live Events daily to confirm coach events are firing
- Check Intercom Fin's "Unanswered" queue daily — if a question appears 3+ times unanswered, add a custom answer immediately
- Track any incorrect answers Fin gives and correct them same-day
- Do NOT change the proactive trigger rules mid-test — record observations for iteration

### 4. Evaluate against threshold

Run the `threshold-engine` drill with these criteria:

- **Primary**: >= 45% of test cohort users fired at least one `ai_coach_engaged` event during the 7-day window
- **Secondary (informational, not pass/fail)**: Coach resolution rate (Fin resolved without handoff), activation rate comparison (coach-engaged vs coach-ignored users)

Decision tree:
- **Pass (>= 45% engagement):** Proceed to Baseline. Document which triggers drove the most engagement, which questions were most common, and initial directional activation lift.
- **Marginal (30-44% engagement):** The coach exists but users are not finding or using it. Investigate: Is the Messenger widget visible? Is the greeting copy engaging? Are proactive triggers firing? Adjust and re-run with 20 more users.
- **Fail (< 30% engagement):** Users are either not seeing the coach or not finding it useful. Review: Are help articles comprehensive? Is Fin giving good answers? Does the product even have enough complexity to warrant a coach? Re-evaluate whether this play fits your product.

## Time Estimate

- 2 hours: Knowledge base audit and custom Fin answer creation
- 1.5 hours: Fin configuration, proactive trigger setup, and tracking instrumentation
- 0.5 hours: Manual review and testing of coach responses
- 2 hours: Daily monitoring over 7 days (15-20 min/day)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom (Fin AI Agent) | AI coaching surface — answers questions, proactive suggestions | $0.99/resolution; ~$10-30 for 20-50 user smoke test |
| PostHog | Coach analytics, funnel tracking, event capture | Free tier covers smoke test volume |

_CRM (Attio), automation (n8n), and PostHog are standard stack — not counted as play-specific costs._

## Drills Referenced

- `onboarding-flow` — confirms the onboarding milestones, product tours, email sequence, and funnel tracking are in place before layering the coach on top
- `ai-coach-conversation-design` — designs the coach knowledge base, Fin configuration, proactive triggers, conversation flows, and analytics instrumentation
- `threshold-engine` — measures coach engagement rate against the 45% threshold and recommends pass/iterate/fail
