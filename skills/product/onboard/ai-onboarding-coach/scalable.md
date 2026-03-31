---
name: ai-onboarding-coach-scalable
description: >
  AI Onboarding Coach — Scalable Automation. Expand the AI coach to all personas with
  persona-specific coaching, automated content gap filling, and proactive struggle
  intervention. Pass threshold: >= 55% coach engagement AND >= 10pp activation lift
  sustained at 500+ monthly signups.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: ">= 55% engagement AND >= 10pp activation lift sustained at 500+ signups/month"
kpis: ["Coach engagement rate at scale", "Activation lift (coach vs no-coach)", "Coach resolution rate by persona", "Proactive suggestion CTR by trigger type", "Content gap fill rate", "Struggle intervention success rate"]
slug: "ai-onboarding-coach"
install: "npx gtm-skills add product/onboard/ai-onboarding-coach"
drills:
  - onboarding-persona-scaling
  - ab-test-orchestrator
---

# AI Onboarding Coach — Scalable Automation

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Scale the AI coaching surface to handle 500+ monthly signups across all personas without degradation in engagement or activation lift. Expand the coach from a general onboarding assistant to a persona-aware, struggle-detecting system that personalizes responses and proactively intervenes when users show signs of frustration or stagnation. Pass threshold: >= 55% coach engagement AND >= 10pp activation lift sustained at 500+ monthly signups with per-persona resolution rate >= 55%.

## Leading Indicators

- Coach engagement rate holds at >= 55% as monthly volume grows beyond 200 users (no volume-based degradation)
- Per-persona resolution rates are within 15 percentage points of each other (no persona is underserved by the knowledge base)
- Struggle intervention success rate >= 40% (users who receive a struggle-triggered coach suggestion recover and reach the next milestone)
- Content gap fill time drops below 48 hours (new unanswered patterns are detected and addressed within 2 business days)
- A/B test velocity reaches 2+ experiments per month on coach messaging, trigger timing, and suggestion formats
- Human handoff rate stays below 25% even as user volume scales

## Instructions

### 1. Expand the coach to all personas

Run the `onboarding-persona-scaling` drill to extend the coach's knowledge and behavior to every user persona:

1. **Persona-specific knowledge bases**: For each persona, create a content collection in Intercom Help Center with articles tailored to that persona's activation path. Example: "Developer Setup Guide" collection for technical builders, "Team Onboarding Guide" for team leads.

2. **Persona-aware Fin responses**: Configure Fin to use the `persona_type` user property when selecting answers. When a developer asks "How do I get started?", Fin should surface the API quickstart, not the GUI walkthrough. Implement this by tagging custom Fin answers with persona relevance.

3. **Persona-specific proactive triggers**: Adjust the n8n proactive suggestion engine to use persona-aware rules:
   - Technical builder stalled on integrations page -> suggest API docs and code examples
   - Team lead stalled on team setup -> suggest the team invite flow with a pre-written invite template
   - Solo creator stalled on project creation -> suggest starting from a template

4. **Persona-specific conversation flows**: Update the first-time greeting flow to detect persona and tailor the opening:
   - Developer: "Welcome! Want to start with the API quickstart or the integrations setup?"
   - Team lead: "Welcome! Let's get your team set up. How many people should we invite?"
   - Solo creator: "Welcome! Let's create your first [core object]. Start from scratch or use a template?"

5. **Track per-persona coach metrics**: Extend PostHog tracking to include `persona_type` on every coach event. Build per-persona funnels: `ai_coach_impression (persona=X)` -> `ai_coach_engaged (persona=X)` -> `activation_reached (persona=X)`. Identify which personas benefit most from the coach and which need more content investment.

### 2. Deploy struggle signal detection

Run the the struggle signal detection workflow (see instructions below) drill to build the behavioral detection layer that identifies struggling users in real-time:

1. Instrument struggle signals: error spikes, rage clicks, repeated failures, help-seeking behavior, abandoned setup flows
2. Compute per-user struggle scores every 6 hours
3. For moderate+ struggle users, extract the specific workflow they are stuck on and the failure mode

Connect struggle detection to the AI coach:
- When a user's struggle score crosses the "moderate" threshold, trigger a contextual coach intervention. The coach opens with: "I noticed you're having trouble with [stuck_workflow]. Here's how to fix [failure_mode]:" followed by step-by-step instructions and a deep link.
- When a user's struggle score crosses "severe", trigger a coach intervention AND flag the user for the human support team with full behavioral context from the struggle detection output.
- Track intervention outcomes: `struggle_intervention_shown` -> `struggle_intervention_engaged` -> `milestone_completed` (within 24 hours). Target >= 40% of struggle interventions resulting in the user progressing within 24 hours.

### 3. Run systematic coach experiments

Run the `ab-test-orchestrator` drill to test coach variations:

**Experiment 1 — Greeting format**: Test different first-time coach greetings:
- Variant A: Question-based ("What would you like to do first?")
- Variant B: Suggestion-based ("Here's your recommended first step: [action]")
- Variant C: Checklist-based ("You have 4 setup steps. Let's start with #1.")
- Measure: Coach engagement rate within the first session

**Experiment 2 — Proactive suggestion timing**: Test when to fire stuck triggers:
- Variant A: After 2 minutes on a setup page
- Variant B: After 3 minutes (current)
- Variant C: After 5 minutes
- Measure: Suggestion CTR and activation rate

**Experiment 3 — Coach response depth**: Test how much detail the coach provides:
- Variant A: Brief (1-2 sentence answer + deep link)
- Variant B: Detailed (step-by-step instructions + deep link)
- Variant C: Interactive (asks clarifying question first, then tailored response)
- Measure: Resolution rate and activation lift

**Experiment 4 — Struggle intervention format**: Test how the coach handles struggling users:
- Variant A: Proactive Fin message with fix instructions
- Variant B: Proactive Fin message offering to walk them through the fix
- Variant C: In-app banner with a "Need help?" CTA linking to a targeted help article
- Measure: Struggle intervention success rate (user progresses within 24h)

Run each experiment for >= 7 days with >= 100 users per variant. Implement winners immediately.

### 4. Evaluate at scale

After 2 months and 500+ total signups:

- **Coach engagement rate**: >= 55% across all personas (check per-persona rates — no persona below 40%)
- **Activation lift**: >= 10pp coach-engaged vs coach-ignored, sustained across the most recent 4 weekly cohorts
- **Resolution rate**: >= 60% overall, >= 55% per persona
- **Struggle intervention success rate**: >= 40%

Decision tree:
- **Pass (all thresholds met at scale):** Proceed to Durable. The coach works, scales, and helps across personas.
- **Engagement pass but lift declining:** The coach is popular but losing effectiveness. Move to Durable with priority on the autonomous optimization loop.
- **One persona failing:** Focus content and trigger investment on the underperforming persona. Extend Scalable for that persona only.
- **Fail at volume (metrics degrade above 300 users/month):** Fin resolution quality may be hitting limits. Investigate: Are there too many unique question patterns? Is the knowledge base too broad? Consider adding persona-specific Fin instances or routing complex questions to human support proactively.

## Time Estimate

- 12 hours: Persona-specific knowledge base expansion and Fin configuration
- 10 hours: Struggle signal detection deployment and coach integration
- 8 hours: A/B test design, setup, and analysis (4 experiments, 2 hours each)
- 8 hours: Per-persona proactive trigger configuration and testing
- 12 hours: Ongoing monitoring, content gap filling, and optimization (1.5 hours/week over 8 weeks)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom (Fin AI Agent) | Persona-aware AI coaching with proactive suggestions | $0.99/resolution; ~$300-600/mo at 500+ signups with 55%+ engagement |
| Loops | Lifecycle email sequences supplementing coach | ~$25-50/mo |

_CRM (Attio), automation (n8n), and PostHog are standard stack — not counted as play-specific costs._

## Drills Referenced

- `onboarding-persona-scaling` — extends the coach knowledge base, conversation flows, and proactive triggers to cover all user personas with persona-specific content and routing
- the struggle signal detection workflow (see instructions below) — builds the behavioral detection layer that identifies struggling users by error density, rage clicks, abandoned flows, and help-seeking behavior, then routes them to the AI coach with specific context
- `ab-test-orchestrator` — runs systematic A/B tests on coach greeting format, proactive suggestion timing, response depth, and struggle intervention format to find the optimal coach configuration at scale
