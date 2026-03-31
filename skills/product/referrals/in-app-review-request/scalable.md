---
name: in-app-review-request-scalable
description: >
  G2/Capterra Review Requests — Scalable Automation. A/B test prompt copy, timing,
  and platform routing. Build multi-variant review asks personalized by engagement
  tier and trigger type. Scale to >=30 reviews per month with review velocity
  monitoring across both platforms.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=30 reviews per month across G2 and Capterra with average rating >=4.0 and no single trigger type producing >60% of reviews"
kpis: ["Review ask show-to-click rate by variant", "Review completion rate by trigger type", "Average review rating by platform", "Reviews per month by platform", "Trigger type distribution", "Ask fatigue rate (dismiss + never-ask)"]
slug: "in-app-review-request"
install: "npx gtm-skills add product/referrals/in-app-review-request"
drills:
  - ab-test-orchestrator
  - review-velocity-monitor
---

# G2/Capterra Review Requests — Scalable Automation

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Find the 10x multiplier for review generation. A/B test every element of the review ask — prompt copy, CTA wording, trigger timing, platform routing, engagement score thresholds — to find the highest-converting combination. Expand from 3 trigger types to 5+. Personalize the ask by engagement tier (different copy for power users vs. engaged users). Scale to >=30 reviews per month across G2 and Capterra with an average rating of 4.0+ and no single trigger type producing more than 60% of reviews (diversified pipeline). Deploy the review velocity monitor to track platform-level performance and ask channel effectiveness in real time.

## Leading Indicators

- A/B tests produce statistically significant winners within 2-3 week cycles
- At least 2 new trigger types added beyond the original 3 (expanding the ask surface)
- Ask fatigue metrics remain stable: dismiss rate <50%, "never ask" rate <8%
- Review velocity dashboard shows steady weekly increase, not spiky (pipeline is healthy)
- Both G2 and Capterra receive reviews each week (platform balance maintained)
- Follow-up email conversion rate improves with variant testing
- Review candidate pipeline depth stays >=6 weeks ahead of ask rate

## Instructions

### 1. Launch systematic A/B testing of review ask variants

Run the `ab-test-orchestrator` drill to test review prompt variations. Run one experiment at a time, each for minimum 7 days or 100+ impressions per variant.

**Experiment queue (run in this order):**

**Experiment 1 — Prompt copy:**
- Control: current best-performing copy from Baseline
- Variant A: Social proof copy: "Join {N} customers who have reviewed us on {platform}. It takes 3 minutes."
- Variant B: Reciprocity copy: "You have been using {product} for {tenure}. We would love to hear what you think — your review on {platform} helps us build what matters to you."
- Primary metric: show-to-click rate
- Secondary metric: review completion rate

**Experiment 2 — CTA wording:**
- Control: "Leave a review on {platform}"
- Variant A: "Share your experience (3 min)"
- Variant B: "Help other teams find us"
- Primary metric: show-to-click rate

**Experiment 3 — Trigger timing:**
- Control: show prompt immediately at the trigger moment
- Variant A: show prompt 2 hours after the trigger event (user has moved on from the milestone context)
- Variant B: show prompt at next session start after the trigger event (fresh session, not mid-workflow)
- Primary metric: review completion rate (not just clicks — does delayed timing produce more follow-through?)

**Experiment 4 — Engagement score threshold:**
- Control: eligible at engagement score >=60
- Variant A: eligible at score >=50 (wider pool, potentially lower quality)
- Variant B: eligible at score >=70 (narrower pool, potentially higher quality)
- Primary metric: review completion rate
- Secondary metric: average review rating (does quality degrade with a lower threshold?)

**Experiment 5 — Platform routing:**
- Control: alternate G2/Capterra per ask
- Variant A: route to whichever platform has fewer recent reviews (balance optimization)
- Variant B: always route to G2 first, then Capterra on second ask (if G2 is the higher-priority platform)
- Primary metric: review completion rate by platform

For each experiment, use PostHog feature flags to split traffic. Implement variants in Intercom (multiple message variants targeting the same audience rules). Log all experiment metadata in Attio.

### 2. Expand trigger types

Add 2+ new trigger types beyond the original 3 (milestone, NPS promoter, post-support):

**Trigger 4 — Usage streak:**
When a user has been active for 7+ consecutive days, they are in a habit formation window. Configure an n8n workflow:
1. PostHog fires a `usage_streak_7d` event
2. Check eligibility in Attio
3. If eligible: show review ask via Intercom with streak-specific copy: "7 days in a row with {product} — you are clearly getting value. Would you share your experience on {platform}?"

**Trigger 5 — Feature adoption breadth:**
When a user uses 5+ distinct features in a 14-day window (from `engagement-score-computation` breadth dimension), they are exploring the product deeply. Configure an n8n workflow:
1. PostHog fires a `feature_breadth_threshold` event when a user crosses the breadth threshold
2. Check eligibility
3. Show review ask with breadth-specific copy: "You have been exploring everything from {feature_1} to {feature_3}. What is your favorite so far? Share your take on {platform}."

**Trigger 6 — Collaboration milestone (if applicable):**
When a user invites their 3rd team member or shares their 5th asset, the product is embedded in their team's workflow. Show a review ask emphasizing team value.

### 3. Personalize asks by engagement tier

Instead of one prompt for all eligible users, tailor the ask by engagement tier (from `engagement-score-computation`):

**Power Users (score >=80):**
- More direct ask: "You are one of our most active users. Your review carries weight on {platform} — would you share your experience?"
- Offer to feature their review in your marketing (with permission)
- Route to G2 first (higher-value platform for B2B credibility)

**Engaged Users (score 60-79):**
- Standard ask: the winning variant from your A/B tests
- Alternate between G2 and Capterra
- Include the follow-up email for non-completers

**Rising Stars (score 40-59) — experimental:**
- Softer ask: "We noticed you have been using {product} for {tenure}. We would value your feedback — even a short review on {platform} helps."
- Only trigger for this tier if Experiment 4 (lower threshold) shows acceptable quality

### 4. Deploy review velocity monitoring

Run the `review-velocity-monitor` drill to build the real-time monitoring layer:

- Create the PostHog "Review Velocity & Attribution" dashboard with all 5 panels: velocity, ask-to-review funnel, rating trends, review-to-lead attribution, ask channel effectiveness
- Build the weekly automated velocity report via n8n (Monday 8am)
- Configure anomaly alerts: velocity stall (0 reviews in 14 days), rating drop (below 4.0), ask fatigue (CTR below 5%), negative review (1-2 stars)
- Maintain the review candidate pipeline in Attio with pipeline depth tracking

The velocity monitor provides the real-time feedback loop that tells you whether scaling changes are working or degrading.

### 5. Evaluate against threshold

After 2 months of scaled operation, measure:

- **Pass threshold:** >=30 reviews per month across G2 and Capterra, average rating >=4.0, no single trigger type producing >60% of reviews
- **If PASS:** The review machine is diversified and scaling. Proceed to Durable to hand optimization to the AI agent.
- **If 20-29 reviews/month:** Close but not there. Check which trigger types are underperforming and run targeted experiments to improve them. Check ask fatigue metrics — if dismiss rate is climbing, extend cooldowns.
- **If <20 reviews/month:** The 10x multiplier is not working. Diagnose: is the eligible user pool growing (new users reaching engagement threshold each month)? Are ask fatigue metrics rising (existing pool exhausted)? Is one trigger type dominating (not diversified enough)?
- **If average rating <4.0:** The engagement threshold may be too low. Increase the minimum score for review eligibility. Check if specific trigger types produce lower-rated reviews.
- **If >60% from one trigger:** The other triggers are underperforming. Run experiments specifically on the weak triggers or add new ones.

Document: winning A/B test results, final trigger type distribution, platform balance ratio, and candidate pipeline depth. This data feeds the Durable optimization agent.

## Time Estimate

- 15 hours: A/B test design, implementation, and analysis (5 experiments x 3 hours each)
- 10 hours: 2 new trigger type workflows (n8n + Intercom configuration)
- 8 hours: engagement tier personalization (3 tier-specific prompt variants + routing logic)
- 12 hours: review velocity monitor setup (PostHog dashboard + n8n weekly report + anomaly alerts)
- 10 hours: ongoing monitoring, experiment management, pipeline maintenance over 2 months
- 5 hours: final evaluation, documentation, and Durable handoff preparation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, funnels, dashboards, velocity tracking | Free tier: 1M events/mo; paid experiments: usage-based ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Multi-variant in-app review prompts, tier-based targeting | Starter $29/seat/mo + Proactive Support ~$99/mo ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Follow-up emails for non-completers, variant testing | $49/mo up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Trigger workflows, experiment routing, velocity reporting, anomaly alerts | Self-hosted: free; Cloud: from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Experiment logs, candidate pipeline, review tracking | Pro: $34/seat/mo ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific cost at this level:** $100-250/mo (Intercom Proactive Support + Loops are the main drivers; PostHog experiments may add usage-based costs at higher volume)

## Drills Referenced

- `ab-test-orchestrator` — designs, runs, and evaluates A/B experiments on prompt copy, CTA wording, timing, thresholds, and platform routing
- `review-velocity-monitor` — builds real-time dashboard, weekly velocity reports, anomaly alerts, and candidate pipeline health tracking
