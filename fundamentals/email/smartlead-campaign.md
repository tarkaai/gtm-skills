---
name: smartlead-campaign
description: Create and manage cold email campaigns in Smartlead
tool: Smartlead
difficulty: Intermediate
---

# Create a Campaign in Smartlead

## Prerequisites
- Smartlead account with connected sending accounts
- Verified prospect list with email addresses
- Smartlead MCP server connected (if using agent automation)

## Steps

1. **Create a new campaign via API.** Use the Smartlead REST API or MCP:
   ```
   POST /api/v1/campaigns/create
   { "name": "Q1 Series-A CTOs", "campaign_type": "email_only" }
   ```
   Name descriptively with audience and date context. Campaign types: "email_only" for pure cold outreach, "email_linkedin" for multi-channel.

2. **Upload your lead list via API.** Import contacts:
   ```
   POST /api/v1/campaigns/<id>/leads
   {
     "leads": [{"email": "jane@co.com", "first_name": "Jane", "last_name": "Doe", "company": "Acme", "custom_fields": {"tech_stack": "AWS"}}]
   }
   ```
   Required fields: email, first_name, last_name, company. Add custom fields for personalization.

3. **Write your email sequence.** Add 3-4 email steps via the API. Use Smartlead template variables: `{{first_name}}`, `{{company}}`, and custom fields. Each email should be under 100 words. Add 2 variants for Step 1 to A/B test subject lines.

4. **Configure sending schedule.** Set timezone-aware sending via API parameters. Send window: weekdays 8am-11am. Set inter-email delay to 60-90 seconds to mimic human sending patterns.

5. **Set daily limits.** Configure per-mailbox daily send limits (30-50 emails) via the API. Smartlead distributes sends across all connected accounts. Enable "stop_on_reply" and "stop_on_bounce" in campaign settings.

6. **Launch and monitor.** Activate via `POST /api/v1/campaigns/<id>/activate` and pull analytics after 48 hours via `GET /api/v1/campaigns/<id>/analytics`. Key benchmarks: delivery rate (>95%), open rate (>45%), reply rate (>3%).
