---
name: instantly-campaign
description: Create and launch cold email campaigns in Instantly
tool: Instantly
difficulty: Intermediate
---

# Create a Campaign in Instantly

## Prerequisites
- Instantly account with connected, warmed sending accounts (see `instantly-account-setup`)
- Verified prospect list (see `clay-email-verification`)

## Steps

1. **Create a new campaign via API.** Use the Instantly REST API:
   ```
   POST /api/v1/campaign/create
   {
     "name": "Mar24 Series-A CTOs Pain-Point",
     "sending_accounts": ["dan@acmehq.com", "daniel@getacme.com"]
   }
   ```
   Name with context: "[Date] [Audience] [Angle]" for easy comparison across campaigns.

2. **Upload your lead list via API.** Import your verified contacts:
   ```
   POST /api/v1/lead/add
   {
     "campaign_id": "<campaign-id>",
     "leads": [
       {"email": "jane@co.com", "first_name": "Jane", "last_name": "Doe", "company_name": "Acme", "custom_vars": {"pain_point": "slow pipeline"}}
     ]
   }
   ```
   Required fields: email, first_name, last_name, company_name. Add custom fields for personalization.

3. **Write your email sequence.** Add 3-4 steps via the API. Step 1 (day 0): Short, personalized opener referencing something specific. Step 2 (day 3): Different angle, lead with value. Step 3 (day 7): Social proof or case study. Step 4 (day 14): Soft breakup. Keep each under 100 words. Use `{{firstName}}` and custom variables for personalization.

4. **Assign sending accounts.** Select 2-3 warmed sending accounts for the campaign in the campaign creation payload. Instantly rotates between them automatically, distributing volume evenly.

5. **Configure schedule via API.** Set sending window:
   ```
   PATCH /api/v1/campaign/<id>/schedule
   { "days": ["mon","tue","wed","thu","fri"], "start_hour": 8, "end_hour": 11, "timezone": "recipient", "daily_limit": 20 }
   ```
   Start with 20 sends/day total and ramp up after 3 days.

6. **Launch and monitor.** Activate the campaign via `POST /api/v1/campaign/<id>/activate`. Check deliverability stats after the first 50 sends via `GET /api/v1/campaign/<id>/analytics`. Open rate below 40% suggests deliverability issues. Reply rate below 2% suggests messaging issues.
