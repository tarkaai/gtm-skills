---
name: posthog-cohorts
description: Create user cohorts in PostHog for targeted analysis and action
tool: PostHog
product: PostHog
difficulty: Intermediate
---

# Create Cohorts in PostHog

## Prerequisites
- PostHog project with identified users and custom events
- User properties set (plan, signup_date, company)

## Steps

1. **Understand cohorts.** A cohort is a saved group of users defined by shared characteristics or behaviors. Use cohorts to: compare groups in insights, target users for feature flags, export lists for email campaigns, and track how different user segments behave over time.

2. **Create behavioral cohorts via API.** Use the PostHog API to create cohorts programmatically:
   ```
   POST /api/projects/<id>/cohorts/
   {
     "name": "Power Users",
     "groups": [{"properties": [{"key": "feature_used", "value": 10, "operator": "gte", "type": "behavioral"}]}]
   }
   ```
   Standard GTM cohorts: "Power Users" (key action 10+ times in 30 days), "At-Risk" (active 30 days ago, inactive last 14 days), "Activated" (completed onboarding within first 7 days).

3. **Create property-based cohorts.** Build cohorts from user properties: "Enterprise Accounts" (company.employee_count > 500), "Free Trial" (plan = "trial" AND days_since_signup < 14), "Outbound Leads" (source = "outbound"). These segment analysis by acquisition channel.

4. **Use cohorts in insights.** When building any PostHog insight (trend, funnel, retention), add a cohort filter or breakdown. Example: compare funnel conversion rates for "Outbound Leads" vs "Organic Signups" via HogQL:
   ```sql
   SELECT cohort, count() FROM events WHERE event = 'signup_completed' GROUP BY cohort
   ```

5. **Create retention cohorts.** Build retention analysis using cohorts: group users by signup week, then measure what percentage return in weeks 1, 2, 4, and 8. Use the PostHog MCP to run these queries and identify which signup cohorts retain best.

6. **Export cohorts for campaigns.** Use the PostHog API to export a cohort's user list (`GET /api/projects/<id>/cohorts/<cohort-id>/persons/`) and feed it into Loops for targeted email campaigns. Use n8n to automate this export-import flow at Scalable level.
