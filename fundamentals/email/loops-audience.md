---
name: loops-audience
description: Set up and manage contact audiences in Loops for lifecycle email
tool: Loops
product: Loops
difficulty: Setup
---

# Manage Audiences in Loops

## Prerequisites
- Loops account connected to your app or website
- User data available (email, signup date, plan, usage data)

## Steps

1. **Set up contact properties via API.** Define custom properties that match your user data model using the Loops API:
   ```
   POST /api/v1/contacts/properties
   { "key": "plan_type", "type": "string" }
   ```
   Essential properties: plan_type (free, pro, enterprise), signup_date, last_active_date, company_name, user_role, onboarding_complete (boolean), and any product-specific properties.

2. **Import existing contacts via API.** If migrating from another email tool, import contacts:
   ```
   POST /api/v1/contacts/create
   { "email": "jane@acme.com", "firstName": "Jane", "plan_type": "pro", "signup_date": "2025-01-15" }
   ```
   Loops deduplicates on email address automatically, so re-imports are safe.

3. **Connect your app for real-time sync.** Use Loops' REST API or Node.js SDK to sync contacts in real-time. Send a contact update whenever a user signs up, changes plan, or hits a key product milestone:
   ```
   PUT /api/v1/contacts/update
   { "email": "jane@acme.com", "plan_type": "enterprise", "last_active_date": "2025-03-30" }
   ```

4. **Create segments.** Build segments using property filters via the Loops dashboard or API. Essential segments: Active Free Users (signed up >7 days, last active <3 days, plan=free), At-Risk Users (last active >14 days), Power Users (usage above 80th percentile), Trial Ending (trial_end_date within 3 days).

5. **Set up event tracking.** Send events from your app to Loops via API when users complete key actions:
   ```
   POST /api/v1/events/send
   { "email": "jane@acme.com", "eventName": "completed_onboarding" }
   ```
   Key events: `completed_onboarding`, `invited_teammate`, `created_first_project`, `hit_usage_limit`. These trigger automated sequences.

6. **Maintain list hygiene.** Review your audience monthly via the API. Archive contacts with no email activity in 90+ days to maintain deliverability. Loops provides engagement scores -- use them to identify and suppress disengaged contacts.
