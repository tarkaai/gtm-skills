---
name: viral-loop-design-scalable
description: >
  Built-In Virality — Scalable Automation. Multiply viral volume by deploying referral surfaces
  across every high-intent moment, A/B testing mechanic variants, and adding gamification to
  sustain sharing behavior at scale.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "Viral coefficient ≥0.4 sustained at 500+ active users with 3+ viral surfaces deployed"
kpis: ["Viral coefficient (K)", "Invites sent per active user", "Invite-to-signup conversion rate", "Active referrer percentage", "Channel-level K"]
slug: "viral-loop-design"
install: "npx gtm-skills add product/referrals/viral-loop-design"
drills:
  - referral-channel-scaling
  - ab-test-orchestrator
  - gamification-system-design
---

# Built-In Virality — Scalable Automation

> **Stage:** Product → Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Viral acquisition scales from a single mechanic to a multi-surface system. Referral prompts appear at every high-intent moment in the product and lifecycle emails. A/B testing systematically optimizes invite copy, landing pages, and reward structures. Gamification sustains long-term sharing behavior. K >= 0.4 holds at 500+ active users across 3+ viral surfaces.

## Leading Indicators

- New viral surfaces produce incremental referral volume (not just redistribution from existing surfaces)
- A/B tests produce statistically significant winners that lift conversion at specific funnel steps
- Gamification mechanics increase repeat sharing (users who share more than once per month)
- Channel-level K identifies which sharing channels (email, link copy, Slack, social) drive the highest quality referrals
- Active referrer percentage (users who shared at least once in last 30 days / total active users) grows month-over-month

## Instructions

### 1. Deploy referral surfaces across every high-intent moment

Run the `referral-channel-scaling` drill. This deploys:

- **In-app contextual prompts**: Intercom messages triggered after milestone completion (first major workflow done), plan upgrades, and round-number usage milestones. Each prompt shows a 1-click share with pre-populated message.
- **Lifecycle email referral CTAs**: Referral sections injected into Day 7 post-signup email, monthly usage summary email, and plan renewal confirmation email via Loops sequences. Each CTA carries a `surface=email_{touchpoint_name}` tracking property.
- **Post-action social sharing**: When users generate shareable outputs (reports, exports, dashboards), present "Share with your team" with pre-populated messages for email, Slack, and LinkedIn. Shared links require signup to view fully.
- **Referral reminder cadence**: n8n automation that identifies users who shared 30+ days ago but not since. Sends a personalized Loops email: "You referred [name] last month. Know anyone else?" Rate limited to 1 reminder per user per 30 days.

Roll out each new surface behind PostHog feature flags at 50%. Keep surfaces with >3% share rate; retire surfaces below 1% after 4 weeks.

### 2. Run systematic A/B tests on the viral funnel

Run the `ab-test-orchestrator` drill. Test one variable at a time across the viral funnel:

**Invite step tests:**
- Invite copy variants (action-oriented vs. social proof vs. benefit-led)
- Share channel prominence (email first vs. link copy first vs. Slack first)
- Timing of invite prompt (immediate post-action vs. 1 hour delay vs. next session)

**Landing step tests:**
- Landing page layout (full preview vs. teaser with signup gate vs. interactive demo)
- Social proof elements (referrer's name visible vs. anonymous vs. "X people from your company")
- Signup friction (email-only vs. OAuth vs. magic link)

**Reward step tests:**
- Reward type (product credits vs. feature unlock vs. extended trial vs. swag)
- Reward timing (immediate on signup vs. on referee activation vs. tiered milestones)
- Two-sided vs. referrer-only incentives

Run each test for minimum 7 days or 100+ samples per variant. Use PostHog experiments for statistical significance. Log all test results in Attio. Apply winners immediately.

### 3. Add gamification to sustain sharing behavior

Run the `gamification-system-design` drill to create mechanics that reward sustained sharing:

- **Referral streaks**: Track consecutive months with at least one successful referral. Display streak count in-app. Award badges at 3, 6, and 12-month streaks.
- **Referrer leaderboard**: Weekly leaderboard of top referrers by referral signups. Scope to cohort (users who signed up the same month) to prevent permanent leaders from discouraging new referrers. Top 3 get featured in the product or community.
- **Referral tiers**: Bronze (1 referral), Silver (5), Gold (10), Platinum (25). Each tier unlocks escalating rewards (extended trial for friends, premium features, branded swag, lifetime discount). Display tier and progress in the product.
- **Milestone celebrations**: Intercom in-app message + Loops email when a user reaches a new tier. Include their referral count, who they referred, and how close they are to the next tier.

Instrument all gamification events in PostHog: `gamification_points_earned`, `gamification_streak_updated`, `gamification_badge_awarded`, `gamification_level_up`.

### 4. Monitor channel-level performance

Build a PostHog dashboard breaking K-factor down by:
- Viral surface (in-app prompt, lifecycle email, post-action share, reminder email)
- Share channel (email, link copy, Slack, LinkedIn, Twitter)
- User segment (new users <30 days, active 30-90 days, power users 90+ days)

Identify the highest-K surface/channel/segment combinations and double down. Identify the lowest-K combinations and investigate whether they can be improved or should be retired.

### 5. Evaluate against threshold

Measure over a 2-month period at 500+ active users:

```
K = (total invites sent / active user count) * (viral signups / total invite recipients)
```

**Pass threshold:** K >= 0.4 sustained at 500+ active users with 3+ viral surfaces deployed.

Also verify:
- Active referrer percentage >= 15% (at least 15% of active users shared in the last 30 days)
- At least 2 A/B tests produced statistically significant winners
- Gamification mechanics increased repeat-share rate by measurable amount vs. pre-gamification baseline
- No single referrer accounts for >10% of total referrals (healthy distribution)

If K >= 0.4, proceed to Durable. If K is below 0.4, focus on the lowest-converting funnel step across all surfaces and run targeted A/B tests there.

## Time Estimate

- 12 hours: referral channel scaling (deploy 4+ surfaces, feature flags, tracking)
- 16 hours: A/B test design, execution, and analysis (3-4 tests over 2 months)
- 12 hours: gamification system design and implementation
- 8 hours: channel-level monitoring dashboard and analysis
- 12 hours: ongoing measurement, optimization, and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, funnels, cohorts, dashboards | Free tier: 1M events/mo. Paid: usage-based from $0.00005/event. https://posthog.com/pricing |
| Intercom | In-app contextual referral prompts, milestone celebrations | Essential: $29/seat/mo. Advanced: $85/seat/mo. https://intercom.com/pricing |
| Loops | Lifecycle email referral CTAs, referral reminders, reward emails | Free tier: 1,000 contacts. Paid from $49/mo. https://loops.so/pricing |
| n8n | Referral reminder automation, surface rollout orchestration | Community (self-hosted): free. Cloud Starter: ~$20/mo. https://n8n.io/pricing |
| Attio | A/B test results logging, referrer tier tracking | Free tier available. Paid from $29/seat/mo. https://attio.com/pricing |

## Drills Referenced

- `referral-channel-scaling` — deploys referral surfaces across in-app prompts, lifecycle emails, post-action triggers, and reminder cadences
- `ab-test-orchestrator` — runs systematic A/B tests on invite copy, landing pages, reward structures, and timing
- `gamification-system-design` — designs streaks, badges, tiers, and leaderboards to sustain long-term sharing behavior
