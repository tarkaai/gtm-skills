---
name: linkedin-ads-lead-gen-forms
description: Create and manage LinkedIn Lead Gen Forms via the Marketing API to capture leads without a landing page
tool: LinkedIn
product: LinkedIn Ads
difficulty: Intermediate
---

# Create LinkedIn Lead Gen Forms

LinkedIn Lead Gen Forms let prospects submit their info directly inside the LinkedIn feed without leaving to a landing page. This reduces friction and typically converts 2-5x higher than landing-page-based campaigns. Critical for Problem-Aware audiences who are not yet motivated enough to visit an external page.

## Prerequisites
- LinkedIn Campaign Manager account with Marketing API access
- A campaign with LEAD_GENERATION objective already created (see `linkedin-ads-campaign-setup`)
- Privacy policy URL for form compliance

## Steps

1. **Create a Lead Gen Form via API.** Use the LinkedIn Marketing API:
   ```
   POST /v2/leadGenForms
   {
     "account": "urn:li:sponsoredAccount:<id>",
     "name": "Problem-Aware Lead Capture - Engineering Leaders",
     "headline": "Get the guide: 5 signs your deployment process is broken",
     "description": "See how teams like yours fixed their deploy pipeline.",
     "privacyPolicyUrl": "https://yoursite.com/privacy",
     "thankYouMessage": {
       "message": "Check your inbox for the guide.",
       "landingPageUrl": "https://yoursite.com/thank-you"
     },
     "questions": [
       {"predefinedField": "FIRST_NAME"},
       {"predefinedField": "LAST_NAME"},
       {"predefinedField": "EMAIL"},
       {"predefinedField": "JOB_TITLE"},
       {"predefinedField": "COMPANY_NAME"},
       {"predefinedField": "COMPANY_SIZE"}
     ]
   }
   ```
   Use predefined fields (auto-filled from LinkedIn profile) for maximum conversion. Only add custom questions if absolutely essential for qualification.

2. **Attach the form to a campaign.** Link the form to your Sponsored Content campaign via the ad creative:
   ```
   POST /v2/adCreatives
   {
     "campaign": "urn:li:sponsoredCampaign:<id>",
     "type": "SPONSORED_STATUS_UPDATE",
     "reference": "urn:li:ugcPost:<post-id>",
     "callToAction": {
       "action": "DOWNLOAD",
       "leadGenFormUrn": "urn:li:leadGenForm:<form-id>"
     }
   }
   ```

3. **Retrieve lead submissions via API.** Poll for new submissions or set up a webhook:
   ```
   GET /v2/leadGenFormResponses?q=owner&owner=urn:li:sponsoredAccount:<id>&leadGenForm=urn:li:leadGenForm:<form-id>
   ```
   Returns: submittedAt, form answers, and the person's LinkedIn profile URN.

4. **Automate lead routing.** Build an n8n workflow that polls the LinkedIn Lead Gen API every 15 minutes, extracts new submissions, creates contacts in Attio, and triggers a Loops welcome email within 5 minutes of submission. Fast response time matters: leads contacted within 5 minutes are 9x more likely to convert.

5. **A/B test form variants.** Create 2-3 forms with different headlines and question sets. Attach each to separate ads within the same campaign. Compare: submission rate, lead quality (do shorter forms produce worse leads?), and downstream conversion to meeting.

6. **Monitor form performance via API.** Pull form-level analytics:
   ```
   GET /v2/adAnalytics?q=statistics&pivots=LEAD_TYPE&campaigns=urn:li:sponsoredCampaign:<id>
   ```
   Key metrics: form open rate, form completion rate, cost per lead. If open rate is high but completion rate is low, reduce the number of questions.

## Error Handling
- **403 Forbidden**: Your API token lacks `rw_ads` scope. Re-authenticate with the correct permissions.
- **Empty responses**: Leads may take 1-2 hours to appear in the API after submission. Do not assume zero leads until 2+ hours have passed.
- **Duplicate leads**: Check email against existing Attio contacts before creating. Use the `attio-contacts` fundamental for deduplication logic.
