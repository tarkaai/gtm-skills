---
name: intercom-user-properties
description: Configure user properties in Intercom for targeted messaging
tool: Intercom
product: Intercom
difficulty: Setup
---

# Set Up User Properties in Intercom

## Prerequisites
- Intercom account with Messenger installed
- Access to your application's user data model

## Steps

1. **Identify key properties.** Define the user properties that drive your messaging segmentation. Essential properties: plan_type, signup_date, last_active_date, company_name, company_size, role, onboarding_complete, feature_usage_count, trial_end_date, source.

2. **Send properties via SDK.** When initializing Intercom in your app, pass user properties in the boot call:
   ```javascript
   Intercom('boot', {
     app_id: 'xxx',
     user_id: userId,
     email: email,
     plan: 'pro',
     company: { id: companyId, name: companyName, plan: 'enterprise' }
   })
   ```
   Update properties on change with `Intercom('update', { plan: 'enterprise' })`.

3. **Create custom attributes via API.** Use the Intercom API to define attributes not automatically captured:
   ```
   POST /data_attributes
   { "name": "activation_score", "model": "contact", "data_type": "integer", "description": "User activation score 0-100" }
   ```
   Key custom attributes: activation_score, nps_response, primary_use_case, referral_count.

4. **Send events for behavior tracking.** Use the SDK or API to track user actions:
   ```javascript
   Intercom('trackEvent', 'feature_first_used', { feature_name: 'csv_export' })
   ```
   Track: feature first use, upgrade initiated, support ticket created, invite sent. Events trigger automated messages and bot flows.

5. **Segment users with properties.** Build segments combining properties and events. Examples: "Trial users ending in 3 days" (plan=trial AND trial_end_date within 3 days), "Power users not on paid plan" (feature_usage > 50 AND plan=free), "At-risk enterprise" (company.plan=enterprise AND last_active > 14 days ago).

6. **Keep properties in sync.** Use server-side API calls to update Intercom whenever user data changes:
   ```
   PUT /contacts/<id>
   { "custom_attributes": { "plan_type": "enterprise" } }
   ```
   A user who upgrades must have their plan property updated before they see plan-targeted messages.
