---
name: intercom-user-properties
description: Configure user properties in Intercom for targeted messaging
tool: Intercom
difficulty: Setup
---

# Set Up User Properties in Intercom

## Prerequisites
- Intercom account with Messenger installed
- Access to your application's user data model

## Steps

1. **Identify key properties.** Define the user properties that drive your messaging segmentation. Essential properties: plan_type, signup_date, last_active_date, company_name, company_size, role, onboarding_complete, feature_usage_count, trial_end_date, source (how they found you).

2. **Send properties via SDK.** When initializing Intercom in your app, pass user properties in the boot call. For the JavaScript SDK: `Intercom('boot', { app_id: 'xxx', user_id: userId, email: email, plan: 'pro', company: { id: companyId, name: companyName, plan: 'enterprise' } })`. Update properties on change with `Intercom('update', { properties })`.

3. **Create custom attributes.** In Intercom, go to Settings > People Data > Custom Attributes. Define attributes that are not automatically captured: "activation_score", "nps_response", "primary_use_case", "referral_count". These enable precise message targeting.

4. **Send events for behavior tracking.** Use `Intercom('trackEvent', 'event-name', { metadata })` to send user actions to Intercom. Track: feature first use, upgrade initiated, support ticket created, invite sent. Events can trigger automated messages and bot flows.

5. **Segment users with properties.** Build segments combining properties and events. Examples: "Trial users ending in 3 days" (plan=trial AND trial_end_date within 3 days), "Power users not on paid plan" (feature_usage > 50 AND plan=free), "At-risk enterprise" (company.plan=enterprise AND last_active > 14 days ago).

6. **Keep properties in sync.** Properties must stay current to avoid sending wrong messages. Use server-side API calls to update Intercom whenever user data changes in your backend. A user who upgrades to Pro must have their plan property updated before they see Pro-targeted messages.
