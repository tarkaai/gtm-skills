---
name: fireflies-action-items
description: Extract action items, decisions, and follow-ups from meeting transcripts using Fireflies API
tool: Fireflies
product: Fireflies
difficulty: Intermediate
---

# Extract Action Items with Fireflies

## Prerequisites
- Fireflies account with meetings being transcribed
- n8n instance for automation (optional but recommended)

## Steps

1. **Retrieve transcripts via API.** After a meeting is transcribed, use the Fireflies GraphQL API to fetch the transcript and AI-generated sections:
   ```graphql
   query { transcript(id: "<transcript-id>") { title, action_items, decisions, questions, summary } }
   ```

2. **Extract action items.** Parse the `action_items` field from the API response. Each item includes the text and speaker. Review for accuracy -- AI extraction may miss nuanced action items or include false positives.

3. **Extract decisions and open questions.** Parse the `decisions` field for decisions made during the meeting and `questions` for unresolved questions that need follow-up.

4. **Push action items to CRM.** Use an n8n workflow to create tasks in Attio from extracted action items:
   - Trigger: Fireflies webhook (`BOOKING_COMPLETED`)
   - Parse: Extract action items from webhook payload
   - Create: Attio task for each action item, assigned to the deal owner

5. **Set up automatic notifications.** Configure Fireflies via API to email action items to relevant team members after each meeting. Or use n8n to route action items to Slack channels based on the meeting type.

6. **Search past meetings via API.** Use Fireflies' search API to find specific decisions across all meetings:
   ```graphql
   query { transcripts(search: "pricing decision") { title, date, action_items } }
   ```
   This retrieves decisions without re-watching recordings.
