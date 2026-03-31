---
name: usage-threshold-alerts-scalable
description: >
  Plan Limit Notifications — Scalable Automation. A/B test alert copy, timing, and channel
  routing across all resources and tiers. Expand to predictive alerts that fire before users
  feel friction. Scale to 500+ alerted accounts per month with upgrade rate sustained at 35%+.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥35% upgrade rate sustained across 500+ alerted accounts per month"
kpis: ["Upgrade rate from alerted users", "Alert click-through rate", "Revenue from alert-driven upgrades", "Upgrade retention (30-day)", "Alerts per resource type"]
slug: "usage-threshold-alerts"
install: "npx gtm-skills add product/upsell/usage-threshold-alerts"
drills:
  - ab-test-orchestrator
  - upgrade-prompt
  - usage-alert-delivery
---

# Plan Limit Notifications — Scalable Automation

> **Stage:** Product -> Upsell | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Find the 10x multiplier. Baseline proved the system works for a controlled group. Scalable expands it to every metered resource, adds A/B testing to find optimal alert copy and timing, and scales to 500+ alerted accounts per month while maintaining a 35%+ upgrade rate. The focus shifts from "does it work" to "what configuration maximizes upgrades per alert."

## Leading Indicators

- Alert system covers all metered resources (not just the original 1-2 from Baseline)
- At least 2 A/B tests running concurrently on different alert variables
- Alert volume reaching 500+ unique accounts per month
- Revenue from alert-driven upgrades growing month over month
- 30-day retention of alert-driven upgraders exceeds 80%
- Upgrade rate per urgency tier is tracked separately and all tiers are improving

## Instructions

### 1. Expand resource coverage

At Baseline, the system likely covered 1-2 resources. Now expand to every metered resource in the product. For each resource:

1. Verify PostHog tracks consumption events with account_id, current_count, and plan_limit
2. Add the resource to the plan cap mapping config in n8n
3. Test the detection query returns correct results for the new resource
4. Create resource-specific alert copy (alerts about API limits should read differently than alerts about seat limits)

Update the `usage-alert-delivery` drill's Intercom and Loops templates to support resource-specific copy. Use template variables: `{{resource_name}}`, `{{resource_description}}`, `{{what_happens_at_limit}}`, `{{next_tier_value}}`.

### 2. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill to test variations across the alert system. Run these experiments sequentially (one at a time per variable, to isolate effects):

**Experiment 1 — Alert timing:**
- Control: Alert at 85% consumed (current imminent threshold)
- Variant A: Alert at 75% consumed (earlier, more runway)
- Variant B: Alert at 90% consumed (later, more urgency)
- Success metric: upgrade conversion rate
- Hypothesis: Earlier alerts give users time to plan budgets, but later alerts create more urgency. Find the optimal trigger point.

**Experiment 2 — In-app message format:**
- Control: Top banner with usage stats and upgrade CTA
- Variant A: Contextual tooltip that appears when the user performs an action that consumes the limited resource
- Variant B: Sidebar widget showing a usage meter with real-time count
- Success metric: click-through rate and upgrade rate
- Hypothesis: Contextual placement (showing the alert at the moment of consumption) will outperform passive banners.

**Experiment 3 — Email copy strategy:**
- Control: Urgency-focused ("You're running out of {{resource}}")
- Variant A: Value-focused ("Here's what {{next_tier}} users do with unlimited {{resource}}")
- Variant B: Social proof ("Companies like yours upgraded when they hit this point — here's what changed")
- Success metric: email open rate, click rate, and upgrade rate
- Hypothesis: Value messaging outperforms urgency for lower tiers; urgency outperforms for critical tier.

**Experiment 4 — Channel routing:**
- Control: In-app message only
- Variant A: Email only
- Variant B: In-app + email (24h delay on email)
- Success metric: upgrade rate and user sentiment (support ticket volume)
- Hypothesis: Multi-channel outperforms single-channel but may increase fatigue.

Use PostHog feature flags to allocate users to variants. Run each experiment for at least 200 per variant or 14 days, whichever comes last.

### 3. Build predictive alerts

Move from reactive (alerting at a percentage threshold) to predictive (alerting based on consumption velocity). Run the `upgrade-prompt` drill to add velocity-based triggers:

- If an account's consumption rate projects them hitting the limit within 7 days, fire an imminent alert regardless of current percentage (catches accounts that spike usage late in billing period)
- If an account has been steadily increasing consumption for 3 consecutive months, fire a growth-signal alert: "Your team is growing — here's why {{next_tier}} is built for what you're doing"
- If an account hits multiple resource limits simultaneously, fire a comprehensive upgrade prompt instead of per-resource alerts

Use the `upgrade-prompt` drill's power-user behavior detection to identify accounts that have outgrown their plan even if they are not near any single limit. An account using every feature, near limits on 3 resources, and adding team members is ready for the next tier even if no single resource is at 85%.

### 4. Scale routing for high-value accounts

Expand the sales routing from Baseline. Using the `usage-alert-delivery` drill's high-value account logic:

- Lower the MRR threshold for sales routing as the team proves they can handle the volume
- Add Attio automation: when an expansion deal is created from a usage alert, auto-schedule a Cal.com meeting link in the email
- Build a weekly expansion pipeline review: all usage-triggered deals, their status, and conversion rate
- Track sales-assisted upgrade rate vs. self-serve upgrade rate for similar-MRR accounts to prove the ROI of sales involvement

### 5. Monitor at scale

Build a live operational view:
- Real-time alert volume (are spikes normal or a system issue?)
- Delivery success rate (are Intercom/Loops throttling?)
- Queue depth (are alerts backlogged?)
- Per-resource alert distribution (is one resource dominating?)

Set up n8n error handling: if the detection pipeline fails, send an immediate Slack alert to the ops team. A day without detection means a day where users hit limits without warning.

### 6. Evaluate against threshold

After 2 months, measure against the pass threshold: at least 35% upgrade rate sustained across 500+ alerted accounts per month.

Also evaluate:
- A/B test results: which experiments produced statistically significant winners?
- Revenue impact: total MRR increase attributable to the alert system (compare alert-driven upgrades vs. total upgrades)
- Per-resource performance: which resources drive the most upgrades? Which have the highest conversion rate?
- Upgrade quality: 30-day retention of alert-driven upgraders should exceed 80%. If it is below 75%, the alerts may be pressure-selling.
- Operational health: detection uptime, alert delivery rate, error rate

If PASS, proceed to Durable. If FAIL, focus on the highest-leverage experiment result and iterate. Common failure modes: alert fatigue (too many alerts per user), channel mismatch (emailing users who only respond to in-app), or upgrade friction (checkout flow drops users).

## Time Estimate

- 8 hours: expand resource coverage and update templates
- 16 hours: design, implement, and run 4 A/B experiments (4 hours each)
- 8 hours: build predictive alerts and velocity-based triggers
- 8 hours: scale sales routing and expansion pipeline
- 12 hours: ongoing monitoring, experiment analysis, and iteration over 2 months
- 8 hours: evaluation, documentation, and Durable preparation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Detection, cohorts, feature flags, experiments, funnels | Free up to 1M events/mo; paid from $0.00031/event — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app alerts with A/B variants | Essential $29/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |
| Loops | Email alerts and sequences with A/B variants | From $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Detection, routing, experiment orchestration | Free self-hosted; Cloud from EUR 24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | Expansion deals, sales routing, account data | Free up to 3 seats; from $29/seat/mo — [attio.com/pricing](https://attio.com/pricing) |

**Estimated play-specific cost: $100-300/mo** (increased Loops volume + Intercom messages + Attio expansion pipeline)

## Drills Referenced

- `ab-test-orchestrator` — designs, runs, and evaluates A/B tests on alert timing, copy, format, and channel routing
- `upgrade-prompt` — adds predictive triggers: velocity-based alerts, growth signals, and multi-resource upgrade prompts
- `usage-alert-delivery` — expanded with resource-specific templates, A/B variant support, and scaled sales routing
