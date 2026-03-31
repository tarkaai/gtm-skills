---
name: proactive-outreach-pipeline
description: Send contextual, struggle-aware help to users before they ask — routing in-app tips, targeted emails, or human outreach based on struggle tier and context
category: Support
tools:
  - Intercom
  - Loops
  - n8n
  - Attio
  - PostHog
  - Anthropic
fundamentals:
  - intercom-in-app-messages
  - intercom-help-articles
  - loops-transactional
  - loops-sequences
  - n8n-workflow-basics
  - n8n-triggers
  - attio-notes
  - attio-lists
  - posthog-custom-events
  - posthog-cohorts
---

# Proactive Outreach Pipeline

This drill takes struggle signals from `struggle-signal-detection` and delivers contextual help to users BEFORE they file a support ticket, complain, or churn. The intervention is specific to what the user is struggling with — not a generic "how's it going?" check-in.

The key principle: the outreach must demonstrate that you understand what the user is trying to do and provide the exact help they need. Vague "let us know if you need anything" messages are worse than no message at all — they signal that you do not actually know what is wrong.

## Input

- Webhook payload from `struggle-signal-detection` containing: person_id, struggle_score, struggle_tier, primary_stuck_workflow, failure_mode, help_docs_searched, has_support_ticket, sessions_with_struggle
- Attio account data (plan, account owner, lifecycle stage, previous outreach history)
- Intercom configured for in-app messaging and help article deep links
- Loops configured for triggered emails
- Anthropic API key for message personalization

## Steps

### 1. Enrich the struggle context

When the n8n webhook receives a struggle alert, pull additional context:

Using `attio-lists`, check:
- Account plan tier and MRR
- Account age (days since signup)
- Previous proactive outreach history (when was the last outreach, what type, did they engage?)
- Account owner assignment

Using `posthog-cohorts`, check:
- Which product features the user has successfully used (to understand their skill level)
- Whether the user completed onboarding
- Whether the user is on a trial or paid plan

This context shapes both the message content and the delivery channel.

### 2. Generate the contextual help content

Using `n8n-workflow-basics`, build the content generation step. For each struggling user, the agent composes help that is specific to their struggle:

**Map struggle workflows to help resources:**

Maintain a lookup table in n8n (or Attio) that maps `primary_stuck_workflow` values to:
- The relevant help article URL (from Intercom help center)
- A 2-3 sentence explanation of the most common fix
- A direct deep link to the product area where the fix is applied
- A video/gif walkthrough URL if available

Example mapping:
```json
{
  "data-import": {
    "help_article": "/help/importing-data",
    "quick_fix": "Most CSV import errors come from date formatting. Use YYYY-MM-DD format and ensure every row has an email column.",
    "deep_link": "/settings/import?format=csv",
    "video": "/tutorials/csv-import-walkthrough"
  },
  "integration-setup": {
    "help_article": "/help/integrations",
    "quick_fix": "Check that your API key has read+write permissions. The most common error is using a read-only key.",
    "deep_link": "/settings/integrations",
    "video": "/tutorials/integration-setup"
  }
}
```

For struggle contexts that do not have a pre-mapped resource, use the Anthropic API to generate a contextual help message based on the error messages and failure mode. Prompt:

```
You are a product support agent. A user is struggling with {primary_stuck_workflow}.
They have encountered these errors: {error_messages}.
They searched for help on: {help_docs_searched}.
Their failure mode is: {failure_mode}.

Write a 2-3 sentence help message that:
1. Acknowledges what they are trying to do (not that they are struggling)
2. Provides the specific fix or next step
3. Links to the relevant help resource

Tone: helpful, direct, not apologetic. Do not say "I noticed you're having trouble."
Instead, frame as a proactive tip: "Quick tip for {workflow}..."
```

### 3. Route to the right channel based on tier

Build routing logic in n8n:

**Moderate tier (score 26-50):**
- Primary channel: In-app message via Intercom
- Message type: Contextual tooltip or banner that appears on their next visit to the product area where they struggled
- Content: The quick fix text + help article link
- Fallback: If user does not log in within 48 hours, send an email via Loops

**Severe tier (score 51-75):**
- Primary channel: In-app message + email via Loops
- In-app: More prominent message with the specific fix, deep link, and video walkthrough
- Email template: "Quick tip for [workflow]" — contains the contextual help, a direct product link, and a reply-to that routes to the account owner
- If user does not engage within 72 hours: escalate to human outreach

**Critical tier (score 76+):**
- Primary channel: All three — in-app message + email + human outreach
- In-app: Prominent banner with one-click "Get help now" that opens a pre-filled support chat
- Email: Personal email from account owner with specific context about what the user is trying to accomplish
- Human: Create Attio task for account owner with full struggle context, recommended talking points, and a 24-hour deadline

### 4. Build in-app message templates

Using the `intercom-in-app-messages` fundamental, create targeted messages:

**Template: struggle-contextual-tip (Moderate tier)**
- Trigger: User visits the product area matching their `primary_stuck_workflow`
- Format: Subtle tooltip or inline banner
- Content: "Quick tip: {quick_fix_text} [See the full guide →]({help_article_url})"
- Display: Once per struggle detection. Dismiss on click or after 30 seconds.
- Do NOT mention that you detected their struggle. Frame as a proactive product tip.

**Template: struggle-detailed-help (Severe tier)**
- Trigger: User logs in (any page)
- Format: Card-style message with dismiss button
- Content: "Getting {workflow_name} set up? Here's the fastest path: {quick_fix_text} [Watch the walkthrough →]({video_url}) [Go to {workflow_name} →]({deep_link})"
- Display: On first login after detection. Dismiss on click.

**Template: struggle-urgent-help (Critical tier)**
- Trigger: User logs in (any page)
- Format: Prominent banner with CTA button
- Content: "Need a hand with {workflow_name}? Our team can walk you through it. [Get help now →]" (CTA opens Intercom chat with pre-filled context)
- Display: On every login until the user engages or their struggle score drops.

Using `intercom-help-articles`, ensure the linked help articles exist and are up to date. If the `struggle-signal-detection` drill flags a workflow with no corresponding help article, create a task to write one.

### 5. Build email templates

Using the `loops-transactional` fundamental, create email templates:

**Template: proactive-tip-email (for Moderate tier fallback and Severe tier)**
- From: noreply@ with reply-to set to account owner's email
- Subject: "Quick tip for {workflow_name} in {product_name}"
- Body: Short and specific. The contextual help content from Step 2. A direct link to the product area. A link to the help article. A human-signed sign-off (account owner name).
- Do NOT include: "We noticed you're struggling" / "It looks like you're having trouble" / any language that signals surveillance.

**Template: proactive-personal-email (for Critical tier)**
- From: Account owner's email address (sent via Loops with their authenticated sender)
- Subject: "{workflow_name} setup — quick pointer"
- Body: Written as a brief personal note. Reference the specific workflow. Provide the fix in 1-2 sentences. Offer a 15-minute call with a calendar link. Signed by account owner.

Using `loops-sequences`, build a 2-email follow-up sequence for users who do not engage with the first outreach:
- Day 0: Primary outreach (template above)
- Day 3: Follow-up with an alternative approach to their stuck workflow. "If {original_fix} didn't work, try {alternative_approach}."
- No Day 7 email. If two outreach attempts fail, stop. The user either resolved it themselves or the outreach is not relevant.

### 6. Build human routing for critical tier

Using `attio-lists`, maintain a "Struggling Users — Needs Human" list. When routing rules determine human outreach is needed:

1. Add the user to the list with full context: struggle score, stuck workflow, failure mode, error messages, sessions with struggle, help docs searched, previous outreach attempts
2. Using `attio-notes`, create a note on the user's record with a pre-drafted outreach email the account owner can personalize
3. Create an Attio task assigned to the account owner with a 24-hour deadline
4. If the account owner does not act within 48 hours, escalate (create a task for the CS lead)

### 7. Enforce cooldowns and rate limits

Prevent outreach fatigue:

- **Per-user cooldown:** Maximum 1 proactive outreach per user per 14 days. If a user is re-flagged within 14 days of previous outreach, do not send another message. Instead, log the repeat struggle signal and escalate one tier (moderate becomes severe treatment).
- **Channel cooldown:** Do not send an in-app message AND an email on the same day. Stagger: in-app on Day 0, email on Day 1 if no engagement.
- **Suppress if support ticket open:** If the user has an open Intercom conversation, suppress all proactive outreach. Enrich the existing ticket instead.
- **Suppress during onboarding:** If the user signed up less than 48 hours ago and is on an onboarding sequence, suppress proactive outreach. Onboarding emails should handle early confusion.

### 8. Track outreach outcomes

Using `posthog-custom-events`, track the full lifecycle:

```javascript
// When outreach is sent
posthog.capture('proactive_outreach_sent', {
  person_id: userId,
  struggle_tier: 'severe',
  outreach_channel: 'in_app',  // in_app | email | human
  stuck_workflow: 'data-import',
  struggle_score: 68
});

// When user engages with outreach
posthog.capture('proactive_outreach_engaged', {
  person_id: userId,
  outreach_channel: 'in_app',
  engagement_type: 'clicked_help_link',  // clicked_help_link | watched_video | replied_email | booked_call | opened_chat
  time_to_engage_hours: 2.5
});

// When user resolves their struggle after outreach
posthog.capture('proactive_outreach_resolved', {
  person_id: userId,
  stuck_workflow: 'data-import',
  resolution_type: 'self_serve',  // self_serve | support_assisted | call_assisted
  days_to_resolve: 1,
  struggle_score_before: 68,
  struggle_score_after: 5
});

// When user churns despite outreach
posthog.capture('proactive_outreach_failed', {
  person_id: userId,
  stuck_workflow: 'data-import',
  days_to_churn: 14,
  outreach_attempts: 2
});
```

Calculate weekly:
- **Outreach reach:** Percentage of moderate+ users who received outreach within 6 hours of detection
- **Engagement rate by channel:** Percentage who interacted with the outreach, broken down by in-app vs email vs human
- **Resolution rate:** Percentage whose struggle score dropped below 10 within 7 days of outreach
- **Save rate:** Of users who were on a churn trajectory (severe/critical tier), percentage who retained 30 days after outreach
- **Self-serve uplift:** Percentage who resolved via the help link/article without needing human support

## Output

- n8n routing workflow that processes struggle alerts and dispatches contextual help
- Three Intercom in-app message templates (moderate, severe, critical)
- Two Loops email templates and a 2-email follow-up sequence
- Attio task creation for critical-tier human outreach
- Cooldown and rate-limiting logic to prevent outreach fatigue
- Outreach outcome tracking in PostHog

## Triggers

Fires automatically when `struggle-signal-detection` sends a webhook. Runs for each individual user flagged at moderate tier or above. Respects a 14-day per-user cooldown.
