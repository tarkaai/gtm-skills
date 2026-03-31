---
name: loops-audience
description: Set up and manage contact audiences in Loops for lifecycle email
tool: Loops
difficulty: Setup
---

# Manage Audiences in Loops

## Prerequisites
- Loops account connected to your app or website
- User data available (email, signup date, plan, usage data)

## Steps

1. **Set up your contact properties.** In Loops, go to Audience > Properties and define custom properties that match your user data model: plan_type (free, pro, enterprise), signup_date, last_active_date, company_name, user_role, onboarding_complete (boolean), and any product-specific properties.

2. **Import existing contacts.** If migrating from another email tool, import your contacts via CSV. Map columns to Loops properties. Loops deduplicates on email address automatically, so re-imports are safe.

3. **Connect your app.** Use Loops' API or Node.js SDK to sync contacts in real-time. Send a contact update whenever a user signs up, changes plan, or hits a key product milestone. This keeps Loops data fresh for targeting.

4. **Create segments.** Build segments using property filters. Essential segments: Active Free Users (signed up >7 days, last active <3 days, plan=free), At-Risk Users (last active >14 days), Power Users (usage above 80th percentile), Trial Ending (trial_end_date within 3 days).

5. **Set up event tracking.** Send events from your app to Loops when users complete key actions: "completed_onboarding", "invited_teammate", "created_first_project", "hit_usage_limit". These events trigger automated sequences.

6. **Maintain list hygiene.** Review your audience monthly. Archive contacts with no email activity in 90+ days to maintain deliverability. Loops provides engagement scores -- use them to identify and suppress disengaged contacts.
