---
name: admin-onboarding-flow-smoke
description: >
  Admin vs User Onboarding — Smoke Test. Separate admin workspace setup from end-user
  activation by classifying signups at entry and routing each role to a dedicated onboarding
  path. Validate that the split improves both admin setup completion and user activation rates
  over a single generic flow.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Smoke Test"
time: "6 hours setup + 7 days observation"
outcome: "≥60% admin workspace setup completion AND ≥50% end-user activation within 7 days, measured against a 10-20 user cohort"
kpis: ["Admin setup completion rate", "User activation rate", "Team invite rate", "Time to workspace ready (hours)", "Checklist step drop-off by step"]
slug: "admin-onboarding-flow"
install: "npx gtm-skills add product/onboard/admin-onboarding-flow"
drills:
  - admin-user-role-routing
  - workspace-setup-flow
  - onboarding-flow
  - threshold-engine
---

# Admin vs User Onboarding — Smoke Test

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Prove that splitting onboarding by role (admin vs user) produces measurably better setup completion and activation than a single generic onboarding flow. Pass threshold: ≥60% of admins complete workspace setup (billing + permissions + first team invite) AND ≥50% of invited end users reach activation within 7 days.

## Leading Indicators

- Admins reaching step 3 of the setup checklist within 24 hours of signup
- End users completing their first core action within 48 hours of invite acceptance
- Team invite rate: ≥40% of admins who complete workspace setup send at least one invite
- Checklist engagement: ≥70% of admins interact with the Intercom checklist in their first session
- Email open rate on setup sequence: ≥45%

## Instructions

### 1. Classify signups and build routing

Run the `admin-user-role-routing` drill to set up role classification at the point of signup. Configure:

- Classification signals: entry path (workspace creation vs invite link), role selection if your product captures it
- PostHog event: `user_role_classified` with properties `role`, `classification_method`, `workspace_id`
- PostHog person property: `user_role` set to "admin" or "user"
- PostHog feature flag: `onboarding-role-path` with variants "admin" and "user"
- Intercom user property: `user_role` pushed via JavaScript SDK

For the Smoke test, classification can be simple: anyone who creates a new workspace is an admin, anyone who accepts an invite link is a user. No ML or complex scoring needed.

### 2. Build the admin workspace setup flow

Run the `workspace-setup-flow` drill to create the admin onboarding path. Configure the Intercom Checklist with 6 setup steps: workspace creation, company profile, billing, permissions, integration connection, and first team invite. Set up auto-completion triggers for each step. Build the 5-email admin lifecycle sequence in Loops with behavioral skip logic.

For Smoke: use the simplest version of each step. Permissions can be a single "admin vs member" binary. Integration step can be optional. Focus on getting admins to billing + first team invite.

**Human action required:** Review the Intercom checklist copy and Loops email content before launching. Ensure the CTA links are correct and point to real product pages. Test the full flow yourself: create a test workspace, walk through every checklist step, verify PostHog events fire, verify emails arrive.

### 3. Build the end-user onboarding path

Run the `onboarding-flow` drill to create the user onboarding path. This is the path for team members who accept an invite. Configure Intercom Product Tours for their first session, focusing on the single most important workflow action. Build the Loops email sequence for invited users (different from the admin sequence -- these users do not need billing or permissions guidance).

For Smoke: keep the user path simple. One product tour (3-5 steps) guiding them to their first core action. One email sequence (3 emails: welcome, quickstart, check-in).

### 4. Launch to a small test cohort

Enable the `onboarding-role-path` PostHog feature flag for 10-20 new signups. Use PostHog's percentage rollout: set to 100% but only target users who sign up during the test window.

**Human action required:** Monitor the first 3-5 signups manually. Verify that admins see the setup checklist and users see the getting-started tour. Check PostHog Live Events to confirm `user_role_classified`, `admin_setup_step_completed`, and `activation_reached` events are firing correctly. Fix any broken flows before the remaining test cohort arrives.

### 5. Track and observe for 7 days

Monitor PostHog daily:
- Admin funnel: `workspace_created` → `billing_configured` → `first_team_invite_sent` → `workspace_ready`
- User funnel: `invite_accepted` → `first_core_action` → `activation_reached`
- Checklist engagement: which steps do admins complete first, where do they stall?
- Email engagement: which emails are opened, which CTAs are clicked?

Do not intervene or change the flows during the observation period unless something is completely broken.

### 6. Evaluate against threshold

Run the `threshold-engine` drill to measure results against the pass criteria:

- **Admin setup completion**: count of admins where `workspace_ready` = true / total admins in cohort. Target: ≥60%.
- **User activation rate**: count of users where `activation_reached` = true / total users in cohort. Target: ≥50%.
- **Team invite rate**: count of admins who sent ≥1 invite / count of admins who completed workspace setup. Track as leading indicator.

If PASS (both thresholds met): document what worked, note the biggest drop-off step in each path, proceed to Baseline.

If FAIL: identify which path underperformed. If admin setup is low, simplify the checklist (reduce steps, make some optional). If user activation is low, shorten the product tour or change the first suggested action. Re-run Smoke with fixes.

## Time Estimate

- 2 hours: role routing setup (classification logic, PostHog events, feature flag)
- 2 hours: workspace setup checklist and admin emails
- 1 hour: user onboarding path and emails
- 1 hour: testing, launch, and monitoring setup
- 7 days observation (passive, ~15 min/day checking PostHog)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, feature flags, funnels | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Intercom | Checklists, product tours, in-app messages | Starter: $39/seat/mo (https://www.intercom.com/pricing) |
| Loops | Lifecycle email sequences | Free tier: 1,000 contacts (https://loops.so/pricing) |
| n8n | Automation workflows (PostHog→Loops→Intercom) | Free self-hosted; Cloud: $24/mo (https://n8n.io/pricing) |

**Estimated monthly cost at Smoke:** Free (within free tiers for 10-20 users)

## Drills Referenced

- `admin-user-role-routing` — classifies signups as admin or user and routes to the correct onboarding path
- `workspace-setup-flow` — builds the admin workspace setup checklist, product tours, and email sequence
- `onboarding-flow` — builds the end-user onboarding path with product tours and email sequence
- `threshold-engine` — evaluates admin setup completion and user activation against pass thresholds
