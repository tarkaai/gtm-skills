---
name: seat-expansion-triggers-scalable
description: >
  Team Growth Upsell — Scalable Automation. A/B test prompt variations,
  segment by account profile, and scale to 500+ prompted accounts while
  maintaining >=40% expansion rate.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=40% expansion rate at 500+ prompted accounts"
kpis: ["Seat expansion rate", "Prompt CTR by variant", "Seats added per conversion", "Revenue per prompt", "Segment expansion rates"]
slug: "seat-expansion-triggers"
install: "npx gtm-skills add product/upsell/seat-expansion-triggers"
drills:
  - ab-test-orchestrator
  - upgrade-prompt
  - seat-expansion-health-monitor
---

# Team Growth Upsell — Scalable Automation

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Scale the expansion system from 50 to 500+ prompted accounts per month while maintaining or improving conversion rates. Find the 10x multiplier through systematic A/B testing of prompt timing, copy, channel mix, and account segmentation. Pass threshold: >=40% expansion rate at 500+ prompted accounts over a 2-month period.

## Leading Indicators

- 500+ accounts enter the hot or warm expansion tiers per month (signal detection is casting a wide enough net)
- A/B test velocity: at least 2 experiments completed per month
- At least one experiment produces a statistically significant improvement
- Prompt fatigue rate stays below 60% dismissal rate (prompts are not wearing out)
- Expansion revenue per prompt increases week over week

## Instructions

### 1. Expand signal detection to warm tier

At Baseline, only hot-tier accounts (score >= 40) received prompts. Now extend prompt delivery to warm-tier accounts (score 20-39) with a lighter touch:

- Hot tier: continue with immediate multi-channel delivery (in-app + email)
- Warm tier: show in-app message only on next login, no email unless they do not log in for 48 hours

This expands the addressable pool. Monitor whether warm-tier conversion rates are acceptable (target: >=25% for warm, >=50% for hot, blended >=40%).

### 2. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill to test variations of the expansion prompt. Test one variable at a time. Priority order:

**Test 1 — Prompt timing (Week 1-2):**
- Control: deliver prompt immediately when account enters hot tier
- Variant: deliver prompt when the user who triggered the signal next performs an in-product action (contextual moment)
- Metric: expansion conversion rate
- Hypothesis: prompts delivered in the moment of need convert 10%+ better than immediate delivery

**Test 2 — CTA copy (Week 3-4):**
- Control: "Add seats now"
- Variant A: "Invite {{inviteeName}} to join" (personalized with the name from the blocked invite)
- Variant B: "Unlock team collaboration" (benefit-focused)
- Metric: prompt click-through rate and conversion rate
- Hypothesis: personalized CTAs with the colleague's name convert 15%+ better

**Test 3 — Prompt format (Week 5-6):**
- Control: Intercom modal (blocks the page)
- Variant: Intercom banner (non-blocking, persistent)
- Metric: expansion conversion rate and prompt dismissal rate
- Hypothesis: modals have higher immediate conversion but banners have lower fatigue over time

**Test 4 — Email vs in-app channel mix (Week 7-8):**
- Control: in-app message only
- Variant: in-app message + email sent 2 hours later
- Metric: expansion conversion rate
- Hypothesis: multi-channel delivery increases conversion by 8%+ for warm-tier accounts

Use PostHog feature flags to randomize accounts into control/variant groups. Run each test for 100+ accounts per variant or 14 days, whichever is longer.

### 3. Build segment-specific expansion paths

Run the `upgrade-prompt` drill to build differentiated expansion paths by account segment:

**By plan tier:**
- Free accounts: emphasize the team features they unlock by moving to a paid plan with more seats
- Starter accounts: show the per-seat price decrease at higher tiers (volume discount)
- Pro accounts: route to sales for enterprise seat licensing discussions

**By team size:**
- Solo users showing collaboration signals: "Bring your first teammate on board — teams of 2+ unlock shared workspaces"
- Teams of 2-5: "Your team is growing — add seats now before you hit your limit"
- Teams of 5+: "Manage your growing team with admin controls and team analytics" (upsell to a higher tier, not just more seats)

**By industry/use case (if data available):**
- Reference industry-specific collaboration patterns in prompt copy
- Include social proof from similar companies: "Teams like yours typically grow to {{avgTeamSize}} users within 3 months"

### 4. Deploy the health monitor

Run the `seat-expansion-health-monitor` drill to build the monitoring layer:

1. Create the PostHog "Seat Expansion Health" dashboard with all 6 panels
2. Configure anomaly alerts for conversion drops, signal spikes, and prompt fatigue
3. Enable the weekly health report automation in n8n
4. Review the first 2 weekly reports to calibrate alert thresholds

Use the health monitor data to prioritize which A/B tests to run next. If a specific prompt type has low conversion, test variations of that prompt first.

### 5. Evaluate against threshold

After 2 months, pull the comprehensive expansion data:

- Total accounts prompted: target 500+ over the 2-month period
- Blended conversion rate across all tiers and channels
- Conversion rate by tier (hot vs warm)
- Conversion rate by channel (in-app vs email vs multi-channel)
- Best-performing prompt variant from A/B tests
- Total seats added and additional MRR generated
- Revenue per prompt (total additional MRR / total prompts delivered)
- Prompt fatigue trend (are dismissal rates increasing?)

**Pass: >=40% expansion rate at 500+ prompted accounts.** Document the winning prompt variants, best-performing segments, and optimal channel mix. These become the configuration inputs for the Durable autonomous optimization loop. Proceed to Durable.

**Fail:** If conversion dropped below 40% at scale, identify whether it is a signal quality issue (warm-tier accounts are not as ready as hot) or a prompt quality issue (prompts are not compelling at scale). If signal quality: tighten warm-tier thresholds. If prompt quality: run more A/B tests focusing on the lowest-performing segments.

## Time Estimate

- 8 hours: extend signal detection to warm tier and configure differentiated routing
- 16 hours: design, launch, and analyze 4 A/B tests (4 hours each)
- 8 hours: build segment-specific expansion paths and prompt variants
- 8 hours: deploy the health monitor dashboard and weekly reporting
- 8 hours: weekly monitoring and optimization over the 2-month period
- 12 hours: final analysis, documentation, and Durable preparation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, A/B test experiments, funnel analysis, dashboards | Free tier: 1M events/mo; paid: $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Workflow automation for detection, delivery, and reporting | Self-hosted: free; Cloud: from EUR20/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Intercom | In-app expansion prompts with A/B variants | From $29/seat/mo; Proactive Support $349/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Expansion emails and follow-up sequences | $49/mo for 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |

**Play-specific cost:** ~$100-400/mo (Intercom Proactive Support add-on is the primary cost driver at scale)

## Drills Referenced

- `ab-test-orchestrator` — design and run A/B tests on prompt timing, copy, format, and channel mix
- `upgrade-prompt` — build segment-specific expansion paths by plan tier, team size, and use case
- `seat-expansion-health-monitor` — monitor expansion funnel health, generate weekly reports, alert on anomalies
