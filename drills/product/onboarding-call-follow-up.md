---
name: onboarding-call-follow-up
description: Automate post-onboarding-call workflow -- transcript processing, action item extraction, CRM logging, follow-up emails, and activation tracking
category: Product
tools:
  - Fireflies
  - Attio
  - Loops
  - PostHog
  - n8n
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - attio-notes
  - attio-contacts
  - attio-custom-attributes
  - loops-transactional
  - posthog-custom-events
  - posthog-cohorts
  - n8n-triggers
  - n8n-workflow-basics
---

# Onboarding Call Follow-Up

This drill automates everything that happens after an onboarding call ends: processing the transcript, extracting action items, logging the call in the CRM, sending a follow-up email with a summary and next steps, and tracking whether the user reaches the activation milestone post-call. The goal is zero manual work after hanging up.

## Prerequisites

- Fireflies configured and auto-joining onboarding calls (see `fireflies-transcription`)
- Attio CRM with onboarding call custom attributes configured (see `onboarding-call-script` drill)
- Loops configured for transactional emails
- PostHog tracking the activation milestone event
- n8n instance running

## Steps

### 1. Trigger on call completion

Using `n8n-triggers`, create an n8n workflow that triggers when Fireflies completes a transcript. Fireflies sends a webhook when transcription finishes (typically 5-10 minutes after the call ends). Configure the webhook in Fireflies settings pointing to your n8n instance.

Filter: Only process transcripts where the meeting title contains "Onboarding" or matches the Cal.com event type name. Skip all other meetings.

### 2. Extract structured data from the transcript

Using `fireflies-action-items`, query the Fireflies GraphQL API for the completed transcript:

```graphql
query {
  transcript(id: "<transcript-id>") {
    title
    date
    duration
    summary
    action_items
    decisions
    questions
    attendees { name, email }
    sentences { text, speaker_name, start_time }
  }
}
```

Parse the response into a structured call record:

- **Summary:** The AI-generated meeting summary
- **Action items for the user:** Tasks the user committed to (e.g., "invite teammates", "import data", "complete setup step X")
- **Action items for your team:** Internal tasks (e.g., "fix bug user encountered", "add documentation for feature Y", "follow up on feature request Z")
- **Blockers identified:** Anything that prevented the user from reaching the activation milestone
- **Feature requests:** Product feedback captured during the call
- **Key quotes:** Verbatim quotes that indicate satisfaction, frustration, or expansion intent

### 3. Score the call

Apply the post-call scoring rubric from the `onboarding-call-script` drill. Using the transcript data, score:

- **Activation progress (1-3):** Check if the activation milestone event fired in PostHog during or immediately after the call. If yes = 3. If attempted but not completed = 2. If not attempted = 1.
- **Engagement level (1-3):** Estimate from transcript: count user's speaking turns vs host's. If user spoke >40% of the time = 3. 20-40% = 2. <20% = 1.
- **Feedback quality (1-3):** Count specific, actionable feedback items in the transcript. 3+ items = 3. 1-2 = 2. 0 = 1.
- **Expansion signal (1-3):** Search transcript for mentions of teammates, other departments, or team usage. Found = 3. Vague mention = 2. None = 1.

Fire the PostHog event using `posthog-custom-events`:
```
posthog.capture('onboarding_call_completed', {
  user_email: attendee_email,
  call_score: total_score,
  activation_during_call: boolean,
  expansion_signal: boolean,
  call_duration_minutes: duration,
  blockers_count: blockers.length,
  action_items_user: user_action_items.length,
  action_items_team: team_action_items.length
})
```

### 4. Log everything to CRM

Using `attio-notes` and `attio-custom-attributes`, update the contact record in Attio:

1. Create a structured note with the call summary, action items, blockers, and key quotes
2. Update custom attributes: `onboarding_call_completed` = true, `onboarding_call_date` = call date, `onboarding_call_score` = total score, `onboarding_call_activated` = whether activation milestone was reached
3. If team action items exist, create follow-up tasks in Attio assigned to the appropriate team members

### 5. Send the follow-up email

Using `loops-transactional`, send a personalized follow-up email within 1 hour of the call ending:

- **From:** The person who ran the call (personal address, not noreply)
- **Subject:** "Your onboarding call recap + next steps"
- **Body structure:**
  1. Thank the user for their time
  2. Recap what was covered (pulled from the summary)
  3. List the user's action items with deadlines
  4. If the activation milestone was not reached: include the specific next step with a direct link to complete it
  5. If the activation milestone was reached: congratulate them and suggest the next valuable feature
  6. Offer to answer questions via reply
  7. If expansion signal detected: include a team invitation link

The email content is generated from the transcript data, not a generic template. Each email references specific things discussed on the call.

### 6. Track post-call activation

Build an n8n workflow using `n8n-workflow-basics` that monitors whether the user reaches the activation milestone after the call:

1. After the call, start a 7-day monitoring window
2. Check PostHog daily (via `posthog-custom-events` query): did the user fire the activation milestone event?
3. **If activated within 48 hours:** Fire `onboarding_call_activation_fast` event. No further action needed.
4. **If not activated after 48 hours:** Send a nudge email via Loops: "Following up on our call -- still need to [specific action item]? Here is a direct link." Include a reply-to for help.
5. **If not activated after 7 days:** Fire `onboarding_call_activation_failed` event. Add to Attio list "Call Follow-Up - Not Activated" for manual review.
6. Update the Attio contact record with `days_to_activation_post_call` once activation occurs.

### 7. Aggregate team action items

Build a weekly n8n workflow that aggregates all internal action items from onboarding calls:

1. Pull all Attio notes from the past week tagged as onboarding call summaries
2. Group action items by category: bugs, feature requests, documentation gaps, other
3. Deduplicate (the same bug may surface in multiple calls)
4. Generate a weekly "Onboarding Call Insights" report:
   - Top 3 blockers this week (by frequency)
   - Top 3 feature requests (by frequency)
   - Net activation rate for users who took calls
   - Average call score trend
5. Post to Slack and store in Attio

## Output

- Automated transcript processing within minutes of call completion
- Structured call scoring and CRM logging with zero manual entry
- Personalized follow-up emails generated from transcript content
- 7-day activation monitoring with automated nudges
- Weekly aggregated insights report for product and onboarding teams
