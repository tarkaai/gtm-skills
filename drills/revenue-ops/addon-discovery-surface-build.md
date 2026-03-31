---
name: addon-discovery-surface-build
description: Build in-product surfaces that expose relevant add-ons to users based on usage context, with tracking and CRM routing
category: Revenue Ops
tools:
  - PostHog
  - Intercom
  - Loops
  - Attio
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - posthog-feature-flags
  - intercom-in-app-messages
  - intercom-product-tours
  - loops-transactional
  - attio-deals
  - attio-custom-attributes
  - n8n-triggers
  - n8n-workflow-basics
---

# Add-On Discovery Surface Build

This drill builds in-product surfaces that show users relevant add-ons and modules at the moment they are most likely to see value. The goal is contextual discovery — showing the right add-on to the right user at the right time — not a generic upsell banner.

## Input

- A catalog of add-ons, modules, or features available for cross-sell (names, descriptions, pricing, entry points)
- PostHog tracking installed with user-level usage data
- Intercom configured for in-app messaging
- Understanding of which usage patterns indicate readiness for each add-on

## Steps

### 1. Map add-ons to usage triggers

For each add-on in the catalog, define the usage behavior that signals a user would benefit from it. This is not guesswork — it requires data.

Using the `posthog-cohorts` fundamental, create two cohorts per add-on:
- **Adopters**: Users who already purchased or activated this add-on
- **Non-adopters**: Users who have not

Compare the two groups on behavioral dimensions: which features do adopters use before purchasing? What usage thresholds do they cross? How long have they been active?

Output a trigger map:

| Add-On | Trigger Behavior | Threshold | Timing Window |
|--------|-----------------|-----------|---------------|
| Reporting Module | Created 5+ custom views | 5 views in 14 days | After 3rd week of use |
| API Access | Used export 10+ times | 10 exports in 30 days | After 2nd month |
| Team Seats | Shared 3+ items with external emails | 3 shares in 7 days | After 1st collaboration event |
| Advanced Automations | Built 3+ manual workflows | 3 workflows created | After completing onboarding |

If you do not have enough historical data, start with product-intuition triggers and validate them within 30 days.

### 2. Build discovery events in PostHog

Using the `posthog-custom-events` fundamental, instrument the following events:

```javascript
// Fired when an add-on discovery surface renders for the user
posthog.capture('addon_discovery_impression', {
  addon_slug: 'reporting-module',
  surface_type: 'tooltip|banner|modal|sidebar|email',
  trigger_behavior: 'created_5_views',
  placement: 'dashboard_header',
  user_plan: currentPlan,
  days_since_signup: daysSinceSignup
});

// Fired when user clicks/engages with the discovery surface
posthog.capture('addon_discovery_clicked', {
  addon_slug: 'reporting-module',
  surface_type: 'tooltip',
  cta_text: 'Try Reporting',
  placement: 'dashboard_header'
});

// Fired when user starts the add-on activation or purchase flow
posthog.capture('addon_activation_started', {
  addon_slug: 'reporting-module',
  entry_point: 'discovery_surface',
  surface_type: 'tooltip'
});

// Fired when add-on is successfully activated or purchased
posthog.capture('addon_activated', {
  addon_slug: 'reporting-module',
  entry_point: 'discovery_surface',
  activation_method: 'self_serve|sales_assisted',
  revenue_delta: monthlyRevenueIncrease
});
```

### 3. Design contextual surfaces

For each trigger in the map, choose the surface type based on urgency and context:

**Tooltips** — low-friction, shown inline when the user is performing the trigger behavior. Example: user creates their 5th custom view, a tooltip appears on the views list: "Need charts and scheduled reports? The Reporting Module turns these views into dashboards."

Using `intercom-product-tours`, build a tooltip-based product tour that:
- Anchors to the UI element the user just interacted with
- Shows the add-on benefit in one sentence tied to what they are doing right now
- Includes a single CTA: "See what's included" or "Start free trial"
- Dismisses permanently once clicked or dismissed twice

**Banners** — medium-friction, shown at the top of a page related to the add-on. Example: a user on the free plan visits the integrations page for the 3rd time. A banner says: "Connect your tools with API Access — automate the exports you're doing manually."

Using `intercom-in-app-messages`, create a banner message:
- Targeted to the PostHog cohort matching the trigger behavior
- Shown only on the relevant page (not globally)
- Includes usage-specific copy: reference the user's actual behavior count
- Auto-dismisses after 7 days if not clicked

**Email nudges** — for users who triggered but did not engage with in-app surfaces. Using `loops-transactional`, send a single email 48 hours after the trigger fires if the user did not click the in-app surface:
- Subject: reference their specific behavior ("You've exported 12 reports this month")
- Body: explain the add-on benefit in terms of their workflow
- CTA: deep link directly to the add-on activation page
- Do not send more than one add-on email per user per 14-day window

### 4. Build the trigger detection workflow

Using `n8n-triggers` and `n8n-workflow-basics`, create an n8n workflow:

1. **Trigger**: Daily cron at 9am UTC
2. **Step 1**: Query PostHog for users who crossed a trigger threshold in the last 24 hours but have not seen the corresponding add-on discovery surface
3. **Step 2**: For each matched user, check if they already have the add-on (query Attio or your billing system)
4. **Step 3**: For eligible users, activate the discovery surface:
   - Set the PostHog feature flag for that user to show the in-app surface (using `posthog-feature-flags`)
   - If 48 hours pass without in-app engagement, enqueue the email nudge in Loops
5. **Step 4**: Log the discovery event in Attio using `attio-custom-attributes`: add-on shown, trigger reason, surface type, timestamp

### 5. Route high-value expansions to sales

Using `attio-deals`, create an expansion deal when:
- The account's potential add-on revenue exceeds a threshold (e.g., >$200/mo)
- The user is on an enterprise or team plan
- Multiple users on the same account triggered for the same add-on

Include in the deal: which add-on, which users triggered, what behavior triggered it, and the estimated revenue. This lets sales have a data-informed conversation.

### 6. Frequency and fatigue controls

Implement strict controls to prevent add-on discovery from becoming spam:
- Maximum 1 in-app surface per user per session
- Maximum 2 different add-ons shown per user per week
- If a user dismisses a surface twice, suppress that add-on for 30 days
- If a user dismisses 3 different add-on surfaces in a month, suppress all add-on discovery for 60 days
- Track `addon_discovery_dismissed` events and use them to build suppression cohorts in PostHog

## Output

- Trigger map: which behaviors signal readiness for each add-on
- PostHog events: impression, clicked, activation_started, activated, dismissed
- In-app surfaces (tooltips, banners) via Intercom targeted by PostHog cohorts
- Email nudges via Loops for users who did not engage in-app
- n8n workflow for daily trigger detection and surface activation
- Attio deal creation for high-value expansion opportunities
- Fatigue controls preventing over-exposure

## Triggers

Run the full setup once. The n8n workflow then runs daily. Re-run setup when adding new add-ons to the catalog or when trigger thresholds need recalibration (typically after 30 days of data).
