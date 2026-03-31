---
name: cross-sell-segment-scaling
description: Scale cross-sell surfaces across multiple products, user segments, and channels with automated targeting and fatigue management
category: Revenue Ops
tools:
  - PostHog
  - Intercom
  - Loops
  - Attio
  - n8n
fundamentals:
  - posthog-feature-flags
  - posthog-cohorts
  - posthog-custom-events
  - intercom-in-app-messages
  - intercom-product-tours
  - loops-transactional
  - attio-deals
  - attio-custom-attributes
  - n8n-scheduling
  - n8n-workflow-basics
---

# Cross-Sell Segment Scaling

This drill takes a validated cross-sell surface (proven at Baseline for 1-2 products) and scales it across the full product catalog, multiple user segments, and coordinated in-app + email channels. The goal is 10x the cross-sell volume without proportional manual effort.

## Input

- Cross-sell catalog mapping completed (`cross-sell-catalog-mapping` drill)
- At least 1 product with validated discovery surfaces achieving >=15% CTR and >=10% activation
- PostHog tracking with all `addon_discovery_*` events flowing
- n8n workflow for trigger detection running daily
- Attio with cross-sell tracking attributes populated

## Steps

### 1. Expand the product catalog

Using the prioritized deployment order from `cross-sell-catalog-mapping`, build discovery surfaces for the next 3-5 products. For each product:

1. Define the trigger using the catalog mapping trigger thresholds
2. Create the PostHog cohort for triggered users using `posthog-cohorts`
3. Build 2 surface variants per product using `intercom-in-app-messages` and `intercom-product-tours`:
   - **Contextual tooltip**: Anchored to the UI element related to the trigger behavior
   - **Page banner**: Shown on a related settings or dashboard page
4. Set the PostHog feature flag using `posthog-feature-flags` to randomly assign triggered users to one variant
5. Instrument all events: `addon_discovery_impression`, `addon_discovery_clicked`, `addon_activation_started`, `addon_activated` with `surface_variant` property

### 2. Build segment-specific messaging

Not all users respond to the same message. Using `posthog-cohorts`, segment triggered users by:

- **Plan tier**: Free users see "Unlock with Pro" / Paid users see "Add to your plan"
- **Usage maturity**: New users (< 30 days) get educational messaging / Power users get efficiency messaging
- **Role**: Admins see team-value messaging / Individual users see personal-productivity messaging
- **Company size**: Solo users see simplicity / Team accounts see collaboration

For each segment, write variant copy that speaks to their specific context. Store the copy variants as Intercom message variants targeted by PostHog cohort.

### 3. Add the email fallback channel

Using `loops-transactional`, build a cross-sell email sequence for users who saw the in-app surface but did not engage:

**Email 1 (48 hours after in-app impression, no click):**
- Subject references their specific behavior: "You exported 47 reports this month"
- Body explains the cross-sell product in terms of their workflow
- CTA deep-links to the product activation page
- Properties: `addon_slug`, `trigger_behavior`, `surface_type=email`, `email_step=1`

**Email 2 (5 days after Email 1, no activation):**
- Social proof: "Teams like yours use [product] to save X hours per week"
- Include a customer quote or usage stat
- CTA: "Start your free trial" or "See what's included"
- Properties: `email_step=2`

**Suppression rules:**
- Do not send if user already activated the product
- Do not send if user dismissed the in-app surface 3+ times (fatigue)
- Maximum 1 cross-sell email per user per 14-day window across all products
- Do not overlap with other email sequences (onboarding, feature announcements)

Build the orchestration in n8n using `n8n-scheduling`:
1. Daily cron checks PostHog for users with impressions but no clicks in last 48 hours
2. Checks Attio for suppression flags using `attio-custom-attributes`
3. Enrolls eligible users in the Loops sequence
4. Logs the enrollment in Attio

### 4. Build the multi-product coordination layer

When a user qualifies for multiple cross-sell products simultaneously, you need a priority system. Using `n8n-workflow-basics`, build a prioritization workflow:

1. Query Attio for all cross-sell eligible products per user
2. Rank by: (trigger strength score) x (product revenue) x (recency of trigger)
3. Show only the top-ranked product per user per session
4. After a user adopts or permanently dismisses a product, promote the next-ranked product
5. Maximum 2 different cross-sell products shown per user per week

Store the priority queue in Attio using `attio-custom-attributes`:
- `cross_sell_priority_queue`: Ordered list of eligible products
- `cross_sell_active_product`: Currently displayed product
- `cross_sell_cooldown_until`: Timestamp for when next product can be shown

### 5. Build the fatigue management system

At scale, fatigue is the primary threat. Track and manage it:

**Per-user fatigue tracking** via `posthog-custom-events`:
- `cross_sell_fatigue_score`: Starts at 0, +1 per dismissal, +3 per "not interested" click, -2 per engaged click, reset on adoption
- When score reaches 5: suppress all cross-sell surfaces for 30 days
- When score reaches 10: suppress for 90 days and flag in Attio for manual review

**Per-product fatigue tracking:**
- If a product's dismissal rate exceeds 50% across all users for 7 consecutive days, auto-pause that product's surfaces
- Alert the team to review the trigger threshold or messaging

**Global cross-sell health:**
- Track the ratio of (total impressions) to (total activations) weekly
- If impression-to-activation ratio degrades by >30% WoW, the system is fatiguing users — reduce frequency

### 6. Scale the sales handoff

Using `attio-deals`, create expansion deals when:
- Account's total cross-sell opportunity exceeds $500/mo ARR
- Multiple users on the same account triggered for the same product
- Account is on enterprise plan or has custom pricing
- User who triggered is a decision-maker (admin role)

Enrich the deal with: trigger data, usage context, estimated revenue uplift, and which products the account already has. Assign to the account owner in Attio.

## Output

- Discovery surfaces live for 4-6 cross-sell products with variant testing
- Segment-specific messaging for plan tier, maturity, role, and company size
- Coordinated in-app + email cross-sell with suppression logic
- Multi-product priority system preventing surface overload
- Fatigue management with automatic suppression and alerting
- Sales handoff for high-value expansion opportunities

## Triggers

Run the full setup once. The n8n workflows run daily. Add new products as they become available. Re-run segment analysis quarterly as user base evolves.
