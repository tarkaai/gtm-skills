---
name: ai-coach-conversation-design
description: Design the AI onboarding coach's knowledge base, contextual triggers, proactive suggestions, and conversation flows that guide users from signup to activation
category: Product
tools:
  - Intercom
  - PostHog
  - Anthropic
  - n8n
fundamentals:
  - intercom-fin-ai-agent
  - intercom-help-articles
  - intercom-user-properties
  - intercom-checklists
  - posthog-custom-events
  - posthog-cohorts
  - posthog-user-path-analysis
  - anthropic-api-patterns
  - n8n-triggers
  - n8n-workflow-basics
---

# AI Coach Conversation Design

This drill designs and deploys the AI coaching layer that guides users through onboarding. The coach is an always-available AI agent inside the product that combines Intercom Fin (for question answering) with contextual proactive suggestions (for nudging users toward activation). The drill covers: building the knowledge base, configuring contextual triggers, designing proactive suggestion logic, and instrumenting coach analytics.

This is distinct from `onboarding-flow` (which builds the static tour/email sequence) and `onboarding-personalization` (which routes users to persona-specific tours). The AI coach is the reactive + proactive intelligence layer that sits alongside those flows and responds to what users actually do.

## Input

- A defined activation metric per persona (from `onboarding-personalization` or `activation-optimization`)
- Help articles covering product setup, features, and troubleshooting (from `intercom-help-articles`)
- PostHog tracking active with onboarding events (from `posthog-gtm-events` or the play's Baseline tracking)
- Intercom Fin enabled (from `intercom-fin-ai-agent` fundamental)

## Steps

### 1. Audit and structure the knowledge base

The AI coach is only as good as the content it draws from. Audit your Intercom Help Center:

1. Map every onboarding step to a help article. For each milestone in your onboarding flow, there must be a dedicated article covering: what the step is, why it matters, exact instructions to complete it, common errors and fixes, and a video or screenshot walkthrough.
2. Organize articles into onboarding-specific collections: "Getting Started", "Account Setup", "Integrations", "Team Setup", "First Workflow", "Troubleshooting".
3. For each persona (from `onboarding-personalization`), tag articles with persona relevance so Fin can prioritize persona-appropriate content.

Quality check: For every article, ask "Could a confused new user follow these instructions and complete the step without asking a human?" If no, rewrite the article until the answer is yes.

Create custom Fin answers for the top 20 onboarding questions. Pull these from:
- Intercom conversation history: filter by tags "onboarding", "setup", "getting started" and extract the 20 most frequent question patterns
- PostHog: identify the pages/features where `help_docs_visited` or `intercom_messenger_opened` events concentrate

Each custom answer must include:
- The exact question pattern (and 3-5 variations)
- A structured answer with step-by-step instructions
- A deep link into the app to the relevant page/action
- A follow-up question: "Did that help? What are you trying to do next?"

### 2. Design contextual trigger rules

The proactive coach layer surfaces help BEFORE the user asks. Define trigger rules based on PostHog behavioral signals:

**Stuck triggers** (user is trying but failing):
| Signal | Detection | Coach Action |
|--------|-----------|-------------|
| Error spike | 3+ `error_displayed` events in 5 minutes | Open Fin with: "Looks like something went wrong. Here's how to fix [error_type]..." |
| Repeated retry | Same action attempted 3+ times without success | Open Fin with: "Need help with [action_name]? Here's a quick walkthrough." |
| Rage click | PostHog `$rageclick` event on a page | Open Fin with: "That button can be tricky. Try [alternative action] instead." |
| Long dwell on setup page | >3 minutes on a setup page without completing the expected action | Open Fin with: "Setting up [feature]? Here's the quickest way to do it." |

**Stall triggers** (user stopped progressing):
| Signal | Detection | Coach Action |
|--------|-----------|-------------|
| Milestone gap | 24+ hours between milestone N and milestone N+1 | Show in-app message: "You're [X%] through setup. Next step: [milestone N+1 action]." |
| Session without progress | User logs in but does not advance any onboarding metric | Open Fin proactively: "Welcome back! Shall I help you finish [current step]?" |
| Abandoned setup flow | Started setup wizard but closed before completion | On next session, open Fin: "You were setting up [feature]. Want to pick up where you left off?" |

**Discovery triggers** (user could benefit from a feature they have not found):
| Signal | Detection | Coach Action |
|--------|-----------|-------------|
| Manual workaround | User performing a multi-step sequence that a feature automates | Open Fin: "Tip: You can do this in one step with [feature]. Want me to show you?" |
| Feature gate approach | User navigating toward a feature area but not entering | Show tooltip: "[Feature] can help you [benefit]. Try it." |
| Post-activation exploration | User completed activation and is browsing | Open Fin: "Now that you're set up, here are 3 features that [persona_type] users love." |

### 3. Build the proactive suggestion engine

Using `n8n-triggers` and `n8n-workflow-basics`, build the backend logic for proactive suggestions:

1. **Real-time trigger pipeline**: Set up PostHog webhooks for key events (`error_displayed`, `$rageclick`, `action_abandoned`, `milestone_completed`). Each webhook fires an n8n workflow.

2. **Context assembly**: When a trigger fires, the n8n workflow gathers context:
   - Pull the user's current onboarding state from Intercom (`intercom-user-properties`)
   - Pull the user's recent event history from PostHog (last 20 events)
   - Identify which onboarding step the user is on (from milestone tracking)
   - Check if the user has already received a proactive suggestion in the last 2 hours (rate limit)

3. **Suggestion generation**: For stuck triggers, select the pre-written help content for that specific error/feature. For discovery triggers, use the `anthropic-api-patterns` fundamental to generate a personalized suggestion:

   ```json
   {
     "prompt": "The user is a {persona_type} on onboarding step {current_step}. They just {trigger_action}. They have not yet discovered {undiscovered_feature}. Write a 1-sentence proactive suggestion that connects their current action to {undiscovered_feature}. Be specific and actionable. Include a deep link.",
     "model": "claude-sonnet-4-20250514",
     "max_tokens": 150
   }
   ```

4. **Delivery**: Push the suggestion to Intercom as an in-app message targeting that specific user. Use `intercom-in-app-messages` with a user ID filter and a 2-hour expiry.

5. **Rate limiting**: Maximum 1 proactive suggestion per 2 hours per user. Maximum 3 per day. Never interrupt a user who is actively completing a workflow (check: no events in last 30 seconds = OK to suggest).

### 4. Design the coach conversation flows

For the interactive AI coach (Fin), design conversation patterns for key onboarding scenarios:

**Flow A — First-time greeting**:
```
Trigger: User's first session after signup
Fin: "Welcome to [Product]! I'm here to help you get set up. What would you like to do first?"
Options: [Start the quickstart guide] [Connect an integration] [Invite my team] [Just explore]
Each option -> deep link to relevant setup page + launch the matching Intercom Checklist
```

**Flow B — Stuck user rescue**:
```
Trigger: Stuck trigger detected (errors, retries, rage clicks)
Fin: "It looks like [specific situation]. Here's what usually works: [step-by-step fix]."
Follow-up: "Did that solve it?"
  Yes -> "Great! Your next step is [next milestone]. Want me to walk you through it?"
  No -> "Let me connect you with someone who can help." -> handoff to human with full context
```

**Flow C — Progress celebration + next step**:
```
Trigger: User completes a milestone
Fin: "Nice — you just [completed action]. You're [X%] through setup."
"Next recommended step for [persona_type] users: [next action]. [Deep link]"
```

**Flow D — Return visit re-engagement**:
```
Trigger: User returns after 24+ hour gap during onboarding
Fin: "Welcome back! Last time you [last completed action]. Ready to continue with [next step]?"
[Continue setup] -> deep link to next step
[Start over] -> deep link to checklist
[Ask a question] -> open Fin chat
```

### 5. Instrument coach analytics

Using `posthog-custom-events`, track every coach interaction:

| Event | Properties | Purpose |
|-------|-----------|---------|
| `ai_coach_impression` | `trigger_type`, `suggestion_content`, `persona_type`, `onboarding_step` | Coach appeared to user |
| `ai_coach_engaged` | `trigger_type`, `engagement_type` (clicked/dismissed/asked_followup), `persona_type` | User interacted with coach |
| `ai_coach_resolved` | `trigger_type`, `resolution_type` (self_serve/fin_resolved/human_handoff), `turns`, `persona_type` | Conversation completed |
| `ai_coach_to_activation` | `trigger_type`, `time_to_activation_hours`, `coach_interactions_count`, `persona_type` | User who engaged coach reached activation |

Build a PostHog funnel: `ai_coach_impression` -> `ai_coach_engaged` -> `ai_coach_resolved` -> `activation_reached`. This measures whether the coach actually helps users activate.

Using `posthog-cohorts`, create comparison cohorts:
- "Coach-engaged users" (1+ `ai_coach_engaged` events during onboarding)
- "Coach-ignored users" (0 `ai_coach_engaged` events during onboarding)
- Compare activation rates between the two groups

### 6. Build the coach performance dashboard

Create a PostHog dashboard with:
- **Coach engagement rate**: % of onboarding users who interact with the coach at least once
- **Coach resolution rate**: % of coach conversations resolved without human handoff
- **Coach-to-activation lift**: Activation rate of coach-engaged vs coach-ignored users
- **Top coach queries**: Most common questions asked to the coach (from Intercom Fin analytics)
- **Proactive suggestion CTR**: % of proactive suggestions that users click/engage with
- **Coach interaction by onboarding step**: Heatmap showing where users engage the coach most

## Output

- Structured knowledge base in Intercom with onboarding-specific articles and custom Fin answers
- Contextual trigger rules for proactive suggestions (stuck, stall, discovery)
- n8n workflows for real-time proactive suggestion delivery
- 4 conversation flow templates for key onboarding scenarios
- Full analytics instrumentation tracking coach engagement, resolution, and activation lift
- Performance dashboard measuring coach effectiveness

## Triggers

Run once at play setup for initial design. Re-run monthly to update knowledge base, refine trigger thresholds based on analytics, and add new custom answers for emerging question patterns.
