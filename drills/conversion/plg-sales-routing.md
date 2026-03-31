---
name: plg-sales-routing
description: Score product-qualified leads in real time and route them to self-serve upgrade or sales-assist based on account value, complexity, and engagement signals
category: Conversion
tools:
  - PostHog
  - Attio
  - Intercom
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - attio-deals
  - attio-custom-attributes
  - attio-lists
  - attio-lead-scoring
  - intercom-in-app-messages
  - n8n-workflow-basics
  - n8n-triggers
---

# PLG Sales Routing

This drill builds the decision engine that determines whether a product-qualified lead (PQL) should self-serve their upgrade or be routed to a human sales conversation. The wrong routing destroys conversion: sending a $20/mo account to sales wastes rep time; letting a $5,000/mo prospect self-serve leaves money and context on the table.

## Input

- PostHog tracking product usage events per user and per account
- Attio CRM with account records, deal pipeline, and custom attributes
- Intercom configured for in-app messaging
- n8n instance for real-time routing workflows
- Defined plan tiers with pricing (self-serve tiers and enterprise/custom tiers)

## Steps

### 1. Define the PQL signal set

Using `posthog-custom-events`, identify the in-product behaviors that indicate upgrade readiness. PQLs are not the same as MQLs -- they have demonstrated value realization through product usage, not content engagement.

**Tier 1 signals (strong PQL indicators):**
- Hit a plan limit (seats, storage, API calls, projects)
- Attempted a premium feature behind a gate
- Invited 3+ teammates within 7 days
- Usage volume exceeds 2x the median for their plan tier
- Connected 2+ integrations

**Tier 2 signals (supporting indicators):**
- Active on 10+ of the last 14 days
- Used 5+ distinct product features in a week
- Exported data or created reports (power-user behavior)
- Visited the pricing page from within the product
- Engagement score above 70 (from `engagement-score-computation` drill)

Fire a `pql_signal_detected` event for each signal:

```javascript
posthog.capture('pql_signal_detected', {
  account_id: accountId,
  user_id: userId,
  signal_type: 'plan_limit_hit',
  signal_tier: 1,
  resource: 'seats',
  current_usage: 5,
  plan_limit: 5,
  plan_tier: 'starter'
});
```

### 2. Build the PQL scoring model

Using `posthog-cohorts`, compute a composite PQL score per account. The score combines product signals with account characteristics:

**Product signal score (0-60 points):**
- Each Tier 1 signal: +15 points (max 45)
- Each Tier 2 signal: +5 points (max 15)

**Account value score (0-40 points):**
- Current MRR >$200: +10
- Team size >5 users: +10
- Company size >50 employees (from enrichment): +10
- Industry match to ICP: +10

Threshold: PQL score >= 40 qualifies the account for routing evaluation.

### 3. Build the routing decision tree

Create an n8n workflow using `n8n-triggers` that fires whenever a `pql_signal_detected` event hits the threshold. The workflow implements this routing logic:

**Route to self-serve upgrade (PQL score 40-64):**
- Account MRR potential under $500/mo
- Upgrade path is a standard plan with published pricing
- No enterprise signals (small team, no custom requirements mentioned in support)
- Action: trigger contextual in-app upgrade prompt via Intercom, send upgrade email via Loops

**Route to sales-assist (PQL score 65+):**
- Account MRR potential $500+/mo OR
- Team size >10 OR
- Enterprise enrichment signals (large company, regulated industry) OR
- Account has asked about custom pricing, SSO, or SLA in support
- Action: create expansion deal in Attio, assign to AE, deliver warm intro via Intercom

**Route to sales-assist override (any score):**
- User explicitly requested a demo or "talk to sales" from within the product
- Action: immediate deal creation in Attio, Slack alert to on-call AE

### 4. Implement self-serve routing actions

For accounts routed to self-serve, use `intercom-in-app-messages` to show contextual upgrade prompts tied to the specific PQL signal:

- Plan limit hit: "You have used all {{limit}} {{resource}}. Upgrade to {{nextPlan}} for {{newLimit}}." Show a one-click upgrade button.
- Feature gate: "{{featureName}} is available on {{plan}}. Unlock it now." Show the feature benefit and price delta.
- Growth signal: "Your team is growing fast. {{nextPlan}} includes {{benefit}} -- ideal for teams your size." Show in a non-blocking banner.

Using `posthog-custom-events`, track prompt performance:

```javascript
posthog.capture('plg_upgrade_prompt_shown', {
  account_id: accountId,
  route: 'self_serve',
  pql_score: 52,
  trigger_signal: 'plan_limit_hit',
  prompt_variant: 'v1'
});
```

### 5. Implement sales-assist routing actions

For accounts routed to sales, use `attio-deals` to create an expansion deal:

1. Create deal: "PLG Expansion -- {{companyName}}"
2. Stage: "PQL Identified"
3. Estimated value: projected annual value based on usage trajectory
4. Context note: PQL score breakdown, top signals, current plan, usage data, engagement score
5. Assign to: round-robin AE or the existing account owner if one exists

Using `attio-lists`, add the account to a "PQL -- Sales Action Required" list.

Using `intercom-in-app-messages`, show a warm handoff message: "Based on how your team uses {{product}}, a custom plan might be a better fit. {{aeName}} from our team can help -- want me to set up a quick call?" with a booking link.

### 6. Handle the handoff moment

The transition from self-serve to sales-assisted must be seamless. Using `n8n-workflow-basics`, build the handoff workflow:

1. When a sales-routed account clicks the booking link or replies to the AE's email, capture the event
2. Enrich the AE's view: pull the account's full product usage history from PostHog, engagement score, PQL score breakdown, and support history from Intercom
3. Generate a one-page account brief and attach it to the Attio deal as a note
4. The AE walks into the call knowing exactly how the prospect uses the product, what triggered the PQL, and what upgrade path makes sense

### 7. Measure routing effectiveness

Track routing quality with `posthog-custom-events`:

```javascript
posthog.capture('plg_route_outcome', {
  account_id: accountId,
  route: 'self_serve',  // self_serve | sales_assist
  pql_score: 52,
  outcome: 'upgraded',  // upgraded | declined | no_action | rerouted_to_sales
  days_to_outcome: 3,
  revenue_delta: 50  // MRR change
});
```

Weekly metrics to track:
- **Self-serve route**: conversion rate (target: 15-25%), time to upgrade, MRR added
- **Sales-assist route**: meeting booked rate (target: 40-60%), close rate, deal cycle time, ACV
- **Mis-routes**: accounts that were self-serve routed but ended up needing sales (too complex), or sales-routed but self-served anyway (wasted rep time)

Use mis-route data to recalibrate the PQL score thresholds quarterly.

## Output

- Real-time PQL scoring per account based on product signals and account characteristics
- Automated routing: self-serve accounts get contextual upgrade prompts, high-value accounts get routed to sales with full context
- n8n workflow handling signal detection, scoring, routing, and handoff
- Attio deals created for sales-assisted accounts with PQL context attached
- Full funnel tracking from PQL signal through upgrade or deal close

## Triggers

Runs in real time via n8n webhook when PostHog fires `pql_signal_detected` events. Recalibrates PQL thresholds monthly based on conversion data. Full model review quarterly.
