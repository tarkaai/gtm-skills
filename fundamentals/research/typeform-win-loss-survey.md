---
name: typeform-win-loss-survey
description: Create a structured win/loss survey in Typeform with branching logic for won vs lost deals
tool: Typeform
difficulty: Config
---

# Create Win/Loss Survey in Typeform

Build a Typeform survey specifically designed to capture structured win/loss feedback from recent buyers and lost prospects. This survey supplements live interviews and captures feedback from contacts who decline a call.

## Prerequisites

- Typeform account (Free tier: 10 responses/month; Basic: $25/mo for 100 responses)
- Understanding of your sales process stages
- List of top 3-5 competitors

## Steps

1. **Create the form via Typeform API.** Use the Typeform Create API to build the survey programmatically:
   ```
   POST https://api.typeform.com/forms
   Authorization: Bearer {TYPEFORM_API_KEY}
   ```
   Set the form title to "Help us improve — [Company Name] feedback" and workspace_id to your workspace.

2. **Add the branching opener.** First question: "Did you end up going with [Company Name]?" (Yes/No). This branches the entire survey into Won vs Lost paths. Use Typeform Logic Jumps to route respondents to different question sets.

3. **Build the Won path questions (5 questions max):**
   - "What was the primary reason you chose us?" (Multiple Choice: Product fit, Pricing, Team/support, Integration capabilities, Reputation, Other)
   - "Which alternatives did you seriously consider?" (Short Text)
   - "What almost stopped you from choosing us?" (Long Text)
   - "On a scale of 1-10, how would you rate your buying experience?" (Opinion Scale)
   - "What could we have done better during the sales process?" (Long Text)

4. **Build the Lost path questions (5 questions max):**
   - "What was the primary reason you chose a different solution?" (Multiple Choice: Price too high, Missing features, Better competitor, Timing/budget, Went with status quo, Other)
   - "Which solution did you go with?" (Short Text, with logic jump: if "Went with status quo" skip this)
   - "What would have changed your decision?" (Long Text)
   - "On a scale of 1-10, how would you rate your experience with our team?" (Opinion Scale)
   - "Is there anything else you'd like us to know?" (Long Text)

5. **Configure the thank-you screen.** Set a custom ending: "Thank you for your honest feedback. It directly shapes how we build and sell our product." Do not ask for anything else — the respondent already gave you their time.

6. **Set up the webhook for responses.** Use the Typeform Webhooks API to send completed responses to your n8n instance:
   ```
   PUT https://api.typeform.com/forms/{form_id}/webhooks/{tag}
   { "url": "https://your-n8n.com/webhook/typeform-winloss", "enabled": true }
   ```
   This triggers your insight extraction workflow automatically.

7. **Generate shareable links with hidden fields.** Use Typeform hidden fields to pre-populate deal context:
   ```
   https://your-typeform.typeform.com/winloss#deal_id={deal_id}&contact_name={name}&outcome={won|lost}&close_date={date}
   ```
   This lets your analysis pipeline link responses back to CRM deal records without asking the respondent redundant questions.

8. **Test the full flow.** Complete the survey yourself on both the Won and Lost paths. Verify logic jumps work, hidden fields pass through, and the webhook fires to n8n. Confirm the response appears in Typeform's Responses tab with all hidden field data intact.
