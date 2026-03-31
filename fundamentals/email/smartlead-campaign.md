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

1. **Create a new campaign.** In Smartlead, go to Campaigns > Create Campaign. Name it descriptively with audience and date context. Select your campaign type: "Email Only" for pure cold outreach or "Email + LinkedIn" for multi-channel.

2. **Upload your lead list.** Import your CSV with required fields: email, first_name, last_name, company. Smartlead supports custom fields for personalization -- add any enrichment data columns you want to reference in templates (company size, tech stack, recent news).

3. **Write your email sequence.** Add 3-4 email steps. Use Smartlead's template variables: {{first_name}}, {{company}}, and any custom fields. Each email should be under 100 words. Smartlead supports A/B variants per step -- add 2 variants for Step 1 to test subject lines.

4. **Configure sending schedule.** Set timezone-aware sending (Smartlead detects recipient timezone from location data). Send window: weekdays 8am-11am. Set inter-email delay to 60-90 seconds to mimic human sending patterns.

5. **Set daily limits.** Configure per-mailbox daily send limits (30-50 emails). Smartlead distributes sends across all connected accounts. Enable "Stop on reply" and "Stop on bounce" at the campaign level.

6. **Launch and monitor.** Activate the campaign and review analytics after 48 hours. Key metrics: delivery rate (>95%), open rate (>45%), reply rate (>3%). Smartlead surfaces these in the campaign dashboard with per-step breakdowns.
