---
name: feature-adoption-campaign-scalable
description: >
  Targeted Adoption Campaigns — Scalable Automation. Expand the adoption campaign across 5+ user
  segments with per-segment messaging, multi-channel delivery, and systematic A/B testing.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥25% adoption rate sustained across 500+ users in 5+ segments"
kpis: ["Overall adoption rate", "Per-segment adoption rate", "Experiment win rate", "Segment reach", "7-day retention by segment"]
slug: "feature-adoption-campaign"
install: "npx gtm-skills add product/retain/feature-adoption-campaign"
drills:
  - adoption-campaign-segment-scaling
  - ab-test-orchestrator
  - usage-milestone-rewards
---

# Targeted Adoption Campaigns — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

25% or more overall adoption rate sustained across 500+ users spanning 5+ distinct segments. Each segment has its own messaging, channel, and success threshold. The 10x multiplier comes from segmentation: instead of one message to everyone, each user segment gets the message that resonates with their specific context.

## Leading Indicators

- New segments launching without requiring manual message creation (the segment-scaling workflow handles it)
- Per-segment adoption rates clustering above 20% (no single segment dragging the average down)
- A/B test velocity: at least 2 experiments completed per month with clear winners
- Milestone reward engagement rates above 30% (users interacting with adoption celebrations)
- Campaign exhaustion rate below 20% per segment (most users adopt before exhausting all campaign touches)

## Instructions

### 1. Scale across segments

Run the `adoption-campaign-segment-scaling` drill to expand from the single Baseline segment to 5+ segments:

- **Power users who never tried the feature** — highest likelihood, message emphasizes efficiency gain
- **Active users who tried once** — re-engagement angle, message shows advanced use cases
- **Recent signups** — discovery angle, message introduces the feature as the natural next step
- **Declining-usage users** — retention angle, message positions the feature as the reason to stay
- **Team admins** — multiplier angle, message shows team-wide impact of enabling the feature

For each segment, the drill creates:
1. A PostHog cohort defining the segment
2. A PostHog feature flag controlling campaign delivery for that segment
3. Per-segment in-app messages in Intercom with segment-specific copy
4. Per-segment email sequences in Loops with segment-specific content
5. An n8n workflow that enrolls users as they enter each segment and removes them when they adopt

Launch segments one at a time, one per week. Monitor each for 7 days before launching the next. If a segment's adoption rate is below 15% after 7 days, pause it and revise the messaging before continuing.

### 2. Run systematic experiments

Run the `ab-test-orchestrator` drill to test campaign variations across segments:

**Month 1 experiments:**
- Test message framing: benefit-led ("Save 2 hours/week") vs. social-proof-led ("Teams like yours use this") — run in the power-user segment
- Test channel priority: in-app first with email follow-up vs. email first with in-app follow-up — run in the recent-signups segment

**Month 2 experiments:**
- Test CTA specificity: generic ("Try it now") vs. personalized ("Set up your first [specific action]") — run across all segments
- Test timing: trigger on login vs. trigger after completing a related action — run in the active-users segment

For each experiment:
1. Form the hypothesis with expected impact
2. Calculate required sample size (minimum 200 per variant)
3. Set up the feature flag split in PostHog
4. Run for the calculated duration without peeking
5. Evaluate: adopt the winner, document the learning, move to the next experiment

### 3. Deploy milestone rewards

Run the `usage-milestone-rewards` drill to reinforce adoption after the initial conversion:

- **First use milestone:** In-app celebration when the user completes the feature action for the first time. Show a contextual message: "You just [completed the action]. Here's how to get even more out of it." Link to an advanced use case.
- **Repeat use milestone:** After 5 uses, send an email summarizing what the user accomplished with the feature. Include a comparison: "You've [outcome] 5 times — users who do this regularly see [quantified benefit]."
- **Power milestone:** After 20 uses, invite the user to share feedback or request advanced capabilities. These are your feature champions.

Milestones serve two purposes: they increase retention (users who celebrate milestones retain at higher rates) and they provide data on which users are most engaged with the feature (candidates for case studies, referrals, or beta testing).

### 4. Monitor and optimize segment performance

Review per-segment performance weekly using the PostHog dashboard from the Baseline level, now expanded with segment breakdowns:

| Metric | Action Threshold |
|--------|-----------------|
| Segment adoption rate <15% for 2 weeks | Pause segment, test new messaging angle |
| Segment dismissal rate >40% | Reduce message frequency, test subtler format |
| Segment exhaustion >50% | The segment is saturated — retire and replace with a new segment |
| Overall adoption rate declining | Check if a new segment is dragging the average — isolate and fix |
| Experiment win rate <25% | Hypotheses are too incremental — test bigger changes |

### 5. Evaluate against threshold

At the end of 2 months, calculate:
- Overall adoption rate across all segments (target: >=25%)
- Total users reached across all segments (target: 500+)
- Number of active segments with >=20% adoption (target: 5+)

- **Pass:** The campaign scales across segments without proportional effort. Each new segment launches via the established workflow. Proceed to Durable for autonomous optimization.
- **Fail:** Identify which segments are underperforming. If most segments work but 1-2 fail, retire those and add new ones. If most segments fail, the feature may need product improvements before the campaign can scale.

## Time Estimate

- 15 hours: Segment definition, cohort creation, per-segment message creation, feature flag setup
- 15 hours: A/B test design, execution, and analysis (4 experiments over 2 months)
- 10 hours: Milestone reward configuration and testing
- 10 hours: n8n workflow build for segment orchestration
- 10 hours: Weekly performance reviews, segment optimization, documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Cohorts, feature flags, experiments, funnels, dashboards | Free up to 1M events/mo; Growth from $0.00045/event — https://posthog.com/pricing |
| Intercom | Per-segment in-app messages and product tours | ~$75-300/mo depending on MAU — https://www.intercom.com/pricing |
| Loops | Per-segment email sequences | Starter $49/mo for 5,000 contacts — https://loops.so/pricing |
| n8n | Segment orchestration, enrollment automation | Free self-hosted; Cloud from $24/mo — https://n8n.io/pricing |

**Play-specific cost:** ~$100-400/mo (Intercom and Loops scale with user count)

## Drills Referenced

- `adoption-campaign-segment-scaling` — expand from one segment to 5+ with per-segment targeting and orchestration
- `ab-test-orchestrator` — run systematic experiments on messaging, channels, and timing
- `usage-milestone-rewards` — reinforce adoption with celebrations and progressive engagement
