---
name: referral-channel-scaling
description: Expand referral surfaces across in-app prompts, lifecycle emails, post-action triggers, and social sharing to multiply referral volume without proportional effort
category: Advocacy
tools:
  - Intercom
  - Loops
  - PostHog
  - n8n
  - Attio
fundamentals:
  - intercom-in-app-messages
  - intercom-product-tours
  - loops-sequences
  - loops-transactional
  - posthog-custom-events
  - posthog-cohorts
  - posthog-feature-flags
  - n8n-workflow-basics
  - n8n-triggers
  - attio-lists
---

# Referral Channel Scaling

This drill multiplies referral volume by deploying referral surfaces across every high-intent moment in the product and communication channels. Instead of a single "refer a friend" page, the referral ask appears contextually at moments of delight, habit formation, and social proof -- each instrumented and measurable independently.

## Prerequisites

- Referral program running at Baseline level for at least 2 weeks with proven conversion
- PostHog tracking core referral events (link shared, clicked, signup, activation, reward)
- Intercom and Loops configured with referral messaging templates
- A unique referral link per user already implemented

## Steps

### 1. Audit existing referral surfaces

Query PostHog for `referral_link_shared` events. Group by the `surface` property (or add it if missing). Calculate share rate and conversion rate per surface. Identify the current top-performing surface and the surfaces with zero or minimal activity. This baseline tells you where new surfaces will have the most incremental impact.

### 2. Deploy in-app contextual prompts

Using `intercom-in-app-messages`, create referral prompts triggered by product success moments:

**Post-milestone prompt**: When a user completes their first major workflow (defined by your activation metric), show: "You just [achieved X]. Know someone who needs this?" with a one-click referral share button.

**Post-upgrade prompt**: After a user upgrades their plan, show: "Welcome to [Plan]. Share [product] with a colleague and you both get [reward]."

**Usage milestone prompt**: When a user crosses a round-number milestone (100th document, 50th report, etc.), show: "You've reached [milestone]. Your referral link: [link]."

Using `posthog-feature-flags`, roll out each new prompt to 50% of eligible users first. Measure referral rate (prompts shown vs. links shared) for each. Keep prompts with >3% share rate; retire prompts below 1%.

### 3. Build lifecycle email referral touchpoints

Using `loops-sequences`, inject referral CTAs into existing lifecycle emails at strategic points:

- **Day 7 post-signup email**: If the user has activated, append a referral section at the bottom: "Enjoying [product]? Share with a friend."
- **Monthly usage summary email**: Include a section showing the user's impact (features used, time saved) with "Share your results" CTA that opens a pre-populated referral message.
- **Plan renewal confirmation email**: After successful renewal, include: "Thanks for staying. Refer a colleague and get [reward]."

Using `posthog-custom-events`, track `referral_email_cta_shown` and `referral_email_cta_clicked` for each touchpoint. Each email referral CTA should carry a `surface=email_{touchpoint_name}` property on the resulting referral link.

### 4. Implement post-action social sharing

Using `posthog-custom-events`, identify shareable product outputs: reports generated, dashboards created, exports completed, achievements unlocked. At each of these output moments, present a share mechanic:

- "Share this [output] with your team" -- generates a link that requires sign-up to view
- Pre-populated share text for email, Slack, and LinkedIn
- Each share link carries the referrer's unique referral code as a query parameter

Using `n8n-triggers`, fire a workflow when a shared output link gets its first click. The workflow enriches the visitor via `attio-lists` and starts the referee onboarding sequence.

### 5. Build the referral reminder cadence

Using `n8n-workflow-basics`, create an automation that identifies users who have shared at least once but not in 30+ days:

1. Query PostHog for users with `referral_link_shared` events, last occurrence >30 days ago
2. Filter to users still active (session in last 7 days)
3. Send a personalized Loops email: "You referred [name] last month. They're loving [product]. Know anyone else?" Include their current referral count and next reward tier.

Rate limit: maximum 1 referral reminder per user per 30 days.

### 6. Measure channel-level performance

Using `posthog-cohorts`, create a "Referral Surface Performance" dashboard showing:

| Surface | Prompts Shown | Links Shared | Share Rate | Referee Signups | Conversion Rate | Cost per Referral |
|---------|--------------|--------------|------------|-----------------|-----------------|-------------------|

Rank surfaces by total referral signups (volume) and by conversion rate (quality). Allocate optimization effort to the highest-volume surfaces first. Retire surfaces with <0.5% share rate after 4 weeks.

## Output

- 3+ in-app contextual referral prompts deployed at success moments
- Referral CTAs injected into 3+ lifecycle email touchpoints
- Post-action social sharing mechanic on shareable product outputs
- 30-day referral reminder automation for lapsed referrers
- Channel-level performance dashboard showing share rate and conversion per surface

## Triggers

Run this drill once when entering Scalable level. Re-run quarterly to add new surfaces based on product changes and to retire underperforming ones.
