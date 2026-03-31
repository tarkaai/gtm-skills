---
name: feature-adoption-campaign-baseline
description: >
  Targeted Adoption Campaigns — Baseline Run. Always-on adoption campaign for one segment with
  automated delivery, A/B control group, and full funnel tracking in PostHog.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥30% adoption rate with ≥10pp lift over control group"
kpis: ["Feature adoption rate", "Lift vs. control", "Campaign engagement rate", "7-day feature retention"]
slug: "feature-adoption-campaign"
install: "npx gtm-skills add product/retain/feature-adoption-campaign"
drills:
  - posthog-gtm-events
  - activation-optimization
  - feature-adoption-monitor
---

# Targeted Adoption Campaigns — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

30% or more of the campaign group adopts the feature, with at least 10 percentage points lift over the control group. The campaign runs always-on via automation for 2 weeks. This proves the campaign effect is real (not just targeting already-interested users) and that automation can sustain it without manual intervention.

## Leading Indicators

- Control group adoption rate stays below 20% (validates the campaign is causing the lift, not organic discovery)
- Campaign engagement rate holds steady or increases over the 2 weeks (no message fatigue)
- Time-to-adoption decreasing week over week (the campaign is accelerating discovery)
- Session recordings show users completing the feature action without confusion after clicking the CTA

## Instructions

### 1. Set up full event tracking

Run the `posthog-gtm-events` drill to instrument comprehensive tracking for this campaign:

| Event | When Fired | Key Properties |
|-------|-----------|---------------|
| `adoption_campaign_impression` | User sees the in-app message | `segment`, `variant`, `channel` |
| `adoption_campaign_clicked` | User clicks the CTA | `segment`, `variant`, `channel` |
| `adoption_campaign_dismissed` | User dismisses the message | `segment`, `variant`, `channel` |
| `feature_first_used` | User performs the feature action for the first time | `feature`, `source` (organic vs. campaign) |
| `feature_retained_7d` | User performs the feature action again 7+ days after first use | `feature`, `first_use_source` |

Build a PostHog funnel: `adoption_campaign_impression` -> `adoption_campaign_clicked` -> `feature_first_used` -> `feature_retained_7d`. Break down by `variant` (campaign vs. control) and `segment`.

### 2. Launch with A/B control group

Using PostHog feature flags, split the target segment 50/50:
- **Treatment group:** Receives the in-app message and follow-up email from the Smoke test (refined based on Smoke learnings)
- **Control group:** Receives no campaign messaging but is tracked for organic feature adoption

This split is critical. Without a control group, you cannot distinguish campaign-driven adoption from organic adoption. Run both groups for the full 2 weeks before comparing.

Configure n8n to automatically enroll new users entering the target segment into one of the two groups (consistent assignment via PostHog feature flag).

### 3. Optimize the activation path

Run the `activation-optimization` drill focused specifically on the feature's activation flow. Analyze the PostHog funnel from Step 1:

- **Biggest drop: impression to click.** The message copy or placement is wrong. Rewrite the headline to focus on the user's specific pain point, not the feature capability.
- **Biggest drop: click to first use.** The feature has a UX problem. Check session recordings of users who clicked but did not complete the action. Simplify the feature's first-run experience.
- **Biggest drop: first use to retention.** The feature delivers weak value. Investigate whether the feature needs improvement (product issue, not campaign issue) or if users need guidance on advanced use cases.

Implement fixes and track whether the funnel improves in Week 2 vs. Week 1.

### 4. Configure automated monitoring

Run the `feature-adoption-monitor` drill to set up always-on monitoring:

- Daily check: how many users entered the treatment group today, how many adopted
- Stalled user detection: users who saw the campaign 3+ days ago but have not adopted — trigger a different message variant or a help offer
- Automated alerts: if adoption rate drops below 15% for 3 consecutive days, flag for investigation

### 5. Evaluate against threshold

At the end of 2 weeks, compare treatment vs. control:

- **Treatment adoption rate:** Count of `feature_first_used` events in treatment group / total treatment group size
- **Control adoption rate:** Same calculation for control group
- **Lift:** Treatment rate minus control rate

Pass criteria: treatment rate >=30% AND lift >=10 percentage points.

- **Pass:** The campaign reliably drives adoption above organic levels. Proceed to Scalable to expand across multiple segments.
- **Fail:** Diagnose which funnel step is weakest. If impression-to-click is the bottleneck, test different messaging. If click-to-adoption is the bottleneck, improve the feature's first-run experience. Re-run for another 2 weeks.

## Time Estimate

- 4 hours: Event taxonomy setup, funnel configuration, feature flag setup for A/B split
- 4 hours: Activation path analysis, session recording review, message refinement
- 4 hours: Feature adoption monitor setup, n8n automation for enrollment and stalled-user detection
- 4 hours: Week 1 and Week 2 analysis, threshold evaluation, documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, feature flags, session recordings | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app message delivery to treatment group | Included in existing plan — https://www.intercom.com/pricing |
| Loops | Follow-up email sequences | Free up to 1,000 contacts — https://loops.so/pricing |
| n8n | Automated enrollment, stalled-user detection | Free self-hosted — https://n8n.io/pricing |

**Play-specific cost:** ~$0-50/mo (PostHog may need paid tier if event volume exceeds free tier)

## Drills Referenced

- `posthog-gtm-events` — instrument the full campaign event taxonomy
- `activation-optimization` — identify and fix the biggest drop-off in the feature adoption funnel
- `feature-adoption-monitor` — always-on monitoring with stalled-user detection and alerts
