---
name: meta-ads-lead-forms
description: Create and manage Meta Instant Forms (Lead Ads) via the Marketing API for in-feed lead capture
tool: Meta Ads
difficulty: Intermediate
---

# Create Meta Lead Ads (Instant Forms)

Meta Instant Forms capture lead info directly within the Facebook/Instagram feed. Like LinkedIn Lead Gen Forms, they eliminate landing page friction. Best for Problem-Aware audiences where you offer educational content (guides, reports, checklists) in exchange for contact info.

## Prerequisites
- Meta Business Manager with Marketing API access
- A campaign with OUTCOME_LEADS objective (see `meta-ads-campaign-setup`)
- Privacy policy URL
- Facebook Page linked to the ad account

## Steps

1. **Create an Instant Form via API.** Use the Marketing API:
   ```
   POST /<page-id>/leadgen_forms
   {
     "name": "Problem-Aware Lead Capture - DevOps Guide",
     "follow_up_action_url": "https://yoursite.com/thank-you",
     "privacy_policy": {"url": "https://yoursite.com/privacy"},
     "questions": [
       {"type": "EMAIL"},
       {"type": "FULL_NAME"},
       {"type": "JOB_TITLE"},
       {"type": "COMPANY_NAME"}
     ],
     "context_card": {
       "title": "Why download this guide?",
       "content": ["Based on data from 200+ teams", "5-minute read", "Actionable framework you can use today"],
       "style": "PARAGRAPH_STYLE"
     },
     "thank_you_page": {
       "title": "You're all set",
       "body": "Check your inbox for the guide. Want to discuss your specific situation?",
       "button_text": "Book a Call",
       "button_url": "https://cal.com/yourteam/discovery"
     }
   }
   ```
   Use the `context_card` to set expectations before the form — this improves lead quality by filtering out low-intent clicks.

2. **Attach the form to an ad.** Create an ad with the lead form:
   ```
   POST /act_<ad-account-id>/ads
   {
     "name": "DevOps Guide Lead Ad",
     "adset_id": "<id>",
     "creative": {
       "object_story_spec": {
         "page_id": "<page-id>",
         "link_data": {
           "message": "Still debugging deployments manually? 73% of teams we surveyed waste 10+ hours/week on preventable incidents.",
           "link": "https://yoursite.com",
           "call_to_action": {"type": "DOWNLOAD", "value": {"lead_gen_form_id": "<form-id>"}}
         }
       }
     }
   }
   ```

3. **Retrieve leads via API.** Poll for submissions:
   ```
   GET /<form-id>/leads?fields=created_time,field_data
   ```
   Or subscribe to real-time lead webhooks for instant notification.

4. **Set up real-time lead webhook.** Configure a webhook subscription for `leadgen` events on your page. Route to n8n which creates the Attio contact and fires the Loops nurture email within minutes.

5. **Use Higher Intent form type for qualification.** For higher-quality leads, set `form_type: "MORE_VOLUME"` (pre-filled, fast) or `"HIGHER_INTENT"` (adds a review screen before submission, reducing accidental submits by ~30% but improving lead quality).

6. **Monitor form analytics via API.**
   ```
   GET /<form-id>/insights
   ```
   Track: impressions, form opens, submissions, cost per lead. Compare Higher Intent vs More Volume forms.

## Error Handling
- **Lead data retention**: Meta deletes lead data after 90 days. Set up automated exports via n8n to your CRM immediately.
- **Webhook delays**: Webhooks can lag 2-5 minutes during high-traffic periods. Supplement with periodic API polling every 15 minutes.
- **Low match rate**: If using customer list audiences, hash emails with SHA-256 before upload. Match rates below 30% suggest data quality issues.
