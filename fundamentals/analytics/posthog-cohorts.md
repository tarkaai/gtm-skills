---
name: posthog-cohorts
description: Create user cohorts in PostHog for targeted analysis and action
tool: PostHog
difficulty: Intermediate
---

# Create Cohorts in PostHog

## Prerequisites
- PostHog project with identified users and custom events
- User properties set (plan, signup_date, company)

## Steps

1. **Understand cohorts.** A cohort is a saved group of users defined by shared characteristics or behaviors. Use cohorts to: compare groups in insights, target users for feature flags, export lists for email campaigns, and track how different user segments behave over time.

2. **Create behavioral cohorts.** In PostHog, go to People > Cohorts > New Cohort. Build cohorts based on actions: "Power Users" (performed key action 10+ times in last 30 days), "At-Risk" (was active 30 days ago but not in last 14 days), "Activated" (completed onboarding within first 7 days).

3. **Create property-based cohorts.** Build cohorts from user properties: "Enterprise Accounts" (company.employee_count > 500), "Free Trial" (plan = "trial" AND days_since_signup < 14), "Outbound Leads" (source = "outbound"). These are useful for segmenting analysis by acquisition channel.

4. **Use cohorts in insights.** When building any PostHog insight (trend, funnel, retention), add a cohort filter or breakdown. Example: compare funnel conversion rates for "Outbound Leads" vs "Organic Signups" to see which channel produces higher-quality users.

5. **Create retention cohorts.** Build a retention analysis using cohorts: group users by signup week, then measure what percentage return in weeks 1, 2, 4, and 8. This reveals whether your retention is improving over time and which signup cohorts retained best.

6. **Export cohorts for campaigns.** Export a cohort's email list and import it into Loops for targeted email campaigns. Example: export your "At-Risk" cohort weekly and trigger a re-engagement sequence. Use n8n to automate this export-import flow at Scalable level.
