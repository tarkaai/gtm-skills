---
name: intercom-fin-ai-agent
description: Configure Intercom Fin AI Agent as a contextual in-product coaching surface that answers questions and guides users based on help content and user context
tool: Intercom
difficulty: Config
---

# Configure Intercom Fin AI Agent

Fin is Intercom's native AI agent that lives inside the Messenger widget. It answers user questions using your help articles, product documentation, and custom content sources. For onboarding plays, Fin becomes the AI coaching surface — the always-available guide that responds to user questions and proactively suggests next steps.

## Prerequisites

- Intercom account on a plan that includes Fin AI (minimum Essential plan + Fin add-on)
- Help articles published in Intercom Help Center (see `intercom-help-articles`)
- User properties flowing into Intercom (see `intercom-user-properties`)

## Setup

### 1. Enable Fin and configure content sources

In Intercom Settings > Fin AI Agent > Content:

Via the Intercom API, manage Fin's content sources:

```
# List existing content sources
GET https://api.intercom.io/help_center/collections
Authorization: Bearer {INTERCOM_ACCESS_TOKEN}
```

Fin ingests from these source types:
- **Help Center articles**: Automatically indexed. Ensure articles are published and organized by collection.
- **Custom content snippets**: Short Q&A pairs for product-specific guidance not covered by articles. Create via the Intercom dashboard under Fin > Custom Answers.
- **External URLs**: Point Fin at product documentation, API docs, or changelog pages. Fin crawls and indexes these.
- **PDF/file uploads**: Upload onboarding guides, setup checklists, or feature documentation.

For the AI onboarding coach use case, ensure these content categories exist:
- Getting started / quickstart guides
- Feature-by-feature walkthroughs
- Common errors and troubleshooting
- Integration setup guides
- FAQ for each user persona

### 2. Configure Fin's behavior and persona

Set Fin's tone and behavior via Intercom Settings > Fin AI Agent > Basics:

- **Name**: Use a coach-like name ("Setup Guide", "Product Coach") rather than a generic bot name
- **Tone**: Set to "Friendly and encouraging" for onboarding contexts
- **Handoff behavior**: Configure when Fin passes to a human: (a) user explicitly asks for a person, (b) Fin confidence drops below 50% after 2 attempts, (c) user frustration signals (repeated questions, negative sentiment)
- **Follow-up questions**: Enable — Fin should ask clarifying questions when the user query is ambiguous

Via the API, configure Fin's settings:

```
# Update Fin AI Agent settings
PUT https://api.intercom.io/ai_agent/settings
Authorization: Bearer {INTERCOM_ACCESS_TOKEN}
Content-Type: application/json

{
  "enabled": true,
  "handoff_after_attempts": 2,
  "tone": "friendly",
  "follow_up_enabled": true,
  "proactive_suggestions_enabled": true
}
```

### 3. Set up audience targeting for onboarding users

Configure Fin to behave differently for onboarding users versus established users:

```javascript
// Update user properties to control Fin behavior
Intercom('update', {
  onboarding_stage: 'active',       // active | completed | stalled
  activation_reached: false,
  days_since_signup: 0,
  persona_type: 'team_lead'
});
```

Set Fin audience rules in Intercom:
- For users where `onboarding_stage = active`: Fin greets proactively with "Need help getting set up? Ask me anything about [product]."
- For users where `onboarding_stage = stalled` (no activity for 48h): Fin opens with "Looks like you haven't finished setting up. Want me to walk you through the next step?"
- For users where `onboarding_stage = completed`: Fin switches to standard support mode

### 4. Configure proactive Fin suggestions

Fin can proactively suggest help based on user context. Configure triggers:

```javascript
// Trigger contextual Fin suggestion when user lands on a complex page
Intercom('update', {
  current_page: 'integrations',
  last_action: 'viewed_integrations_page'
});

// Intercom Fin will use this context to proactively suggest relevant help articles
// Configure in Fin > Proactive Support: "When user views integrations page, suggest integration setup guide"
```

### 5. Track Fin interactions for coaching analytics

Forward Fin conversation data to PostHog for analysis:

```javascript
// Intercom fires events when Fin resolves or hands off
// Use the Intercom webhook to capture these in your backend:

// Webhook: conversation.closed (check if resolved by Fin)
// Payload includes: resolution_type (fin_resolved | human_resolved | unresolved)
// Forward to PostHog:
posthog.capture('ai_coach_interaction', {
  resolution_type: 'fin_resolved',
  topic: conversationTopic,
  turns: conversationTurnCount,
  persona_type: userPersona,
  onboarding_stage: userOnboardingStage
});
```

### 6. Build custom Fin answers for onboarding flows

For common onboarding questions that need precise, structured answers:

In Intercom > Fin > Custom Answers, create entries for:
- "How do I get started?" -> Step-by-step quickstart with deep links
- "What should I do next?" -> Context-aware response based on user's current onboarding_stage
- "How do I connect [integration]?" -> Integration-specific setup guide with direct link to setup page
- "I'm stuck" -> Diagnostic flow: "What were you trying to do?" -> route to specific help

Custom answers take priority over article-based answers when matched.

## Error Handling

- **Fin gives wrong answers**: Review Fin's "Unanswered" and "Incorrectly answered" queues in Intercom. Add custom answers for frequently wrong responses. Remove or update misleading help articles.
- **Fin loops without resolution**: Reduce `handoff_after_attempts` to 1 for complex topics. Add explicit handoff triggers for known difficult workflows.
- **Low Fin usage**: Check that Messenger is visible on onboarding pages. Verify the proactive greeting fires for new users. Test the greeting copy — "Ask me anything" outperforms "How can I help?"

## Pricing

Fin charges per resolution (a conversation Fin handles without human handoff):
- $0.99 per Fin resolution (as of 2025)
- No charge for conversations Fin hands off to humans
- Volume discounts available above 1,000 resolutions/month

Cost modeling:
- 100 onboarding users/month, 60% engage Fin, 2 conversations each, 70% Fin-resolved: ~84 resolutions = ~$83/month
- 500 users/month: ~420 resolutions = ~$416/month
- 1,000 users/month: ~840 resolutions = ~$832/month

## Tool Alternatives

- **Ada** (ada.cx): AI-powered customer support bot. Custom knowledge base. Enterprise pricing.
- **Forethought** (forethought.ai): AI agent for support automation. Starts at custom pricing.
- **CommandBar Copilot** (commandbar.com): In-app AI assistant with product-specific knowledge. Usage-based pricing starting ~$200/mo.
- **Plain** (plain.com): AI-first support with in-app widget. Starts at $39/seat/mo.
- **Gleap** (gleap.io): In-app support with AI bot. Starts at $49/mo.
