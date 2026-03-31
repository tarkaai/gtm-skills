---
name: freemium-feature-upsell-scalable
description: >
  Freemium to Paid Conversion — Scalable Automation. Systematic A/B testing across prompt
  copy, timing, surface, and trigger thresholds. Segment-specific conversion paths. Scale
  the system to handle the full free user base without proportional effort increase.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: "≥8% conversion rate sustained at 500+ prompted free users per month with per-trigger rates within 20% of Baseline levels"
kpis: ["Free-to-paid rate at scale", "Conversion by trigger type", "Revenue per conversion", "Prompt fatigue rate", "Experiment win rate", "Segment-specific conversion rates"]
slug: "freemium-feature-upsell"
install: "npx gtm-skills add product/upsell/freemium-feature-upsell"
drills:
  - ab-test-orchestrator
  - usage-threshold-detection
  - gate-conversion-health-report
---

# Freemium to Paid Conversion — Scalable Automation

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Maintain the 8% overall free-to-paid conversion rate while scaling to 500+ prompted free users per month. Per-trigger conversion rates should stay within 20% of Baseline levels (limit proximity >=8%, feature gate >=5%, growth signal >=4%, time-based >=2.5%). The 10x multiplier comes from: (1) testing prompt variants to find what converts best per segment, (2) expanding the trigger surface area to reach more free users earlier in their lifecycle, and (3) building segment-specific conversion paths so a solo developer and a team lead get different upgrade experiences.

## Leading Indicators

- Experiment velocity: at least 2 A/B tests running per month across the conversion system
- Experiment win rate: at least 30% of tests produce a statistically significant winner (below 30% means hypotheses are poorly targeted)
- Segment coverage: percentage of active free users who have been exposed to at least one upgrade prompt in the last 30 days. Target: 60%+ (up from the Baseline level's smaller exposed pool)
- New trigger types producing measurable conversion (the trigger surface area is expanding)
- Prompt fatigue rate remaining below 15% despite higher prompt volume (suppression rules are scaling)

## Instructions

### 1. Launch systematic variant testing

Run the `ab-test-orchestrator` drill to set up a structured experimentation program across the freemium conversion funnel. Test one variable at a time per trigger type:

**Copy variants (test first, highest expected impact):**
- Limit proximity: test loss-aversion framing ("You will lose access to 3 projects when you hit the limit") vs. gain framing ("Upgrade to unlock unlimited projects")
- Feature gate: test social proof ("12,000 teams use this feature") vs. outcome framing ("Teams using this feature ship 40% faster")
- Growth signal: test team-centric ("Your team needs Pro") vs. data-centric ("Your usage grew 150% this month — Pro scales with you")

**Timing variants (test second):**
- Test showing the limit prompt at 70% vs. 85% vs. 95% consumed. Earlier = more time to decide but lower urgency. Later = higher urgency but less time.
- Test feature gate prompts at first encounter vs. third encounter (is curiosity enough, or does repeated exposure build more intent?)
- Test email follow-up timing: 24h vs. 48h vs. 72h after the in-app prompt

**Surface variants (test third):**
- Test in-app banner vs. in-app modal vs. inline tooltip for limit prompts
- Test full-screen locked state vs. blurred preview vs. sample output for feature gates
- Test email-only vs. email + in-app for time-based triggers

Use PostHog feature flags with multivariate flags for each experiment. Run each test for minimum 7 days or until 200+ samples per variant. Never stack experiments on the same trigger type simultaneously.

### 2. Expand trigger surface area

Run the `usage-threshold-detection` drill with expanded scope to reach more free users earlier:

- **Velocity-based triggers**: Not just current usage vs. limit, but acceleration of usage. A free user whose project count went from 10 to 25 in a week (on a 50-project limit) is higher intent than one who has been at 40 for months.
- **Behavioral proximity triggers**: Free user attempted an action that requires a paid feature but did not formally hit a feature gate. Example: tried to export data (paid feature) by clicking a "Download CSV" button that is not gated but leads to a soft upsell.
- **Peer comparison triggers**: Free users whose usage pattern matches the profile of users who historically upgraded. "Users like you typically upgrade within 2 weeks."
- **Re-engagement triggers**: Previously active free users who went dormant for 14+ days and just returned. Show a "Welcome back — here is what is new in Pro" message.

For each new trigger, deploy behind a feature flag, measure for 7 days, evaluate conversion rate vs. the established triggers. Keep triggers that convert at >=50% of the best-performing trigger. Remove triggers that convert below 2%.

### 3. Build segment-specific conversion paths

Different free user personas convert for different reasons. Build distinct paths:

**Solo users (1 seat, individual use):**
- Primary trigger: feature gates on power features (automations, API access, advanced analytics)
- Upgrade message: focused on personal productivity and capability
- CTA: "Upgrade to Pro" with one-click Stripe checkout
- Email: case study of a solo user who upgraded and achieved a specific outcome

**Team leads (2+ seats invited, collaborative usage):**
- Primary trigger: seat limits and team features (permissions, shared workspaces, team analytics)
- Upgrade message: focused on team efficiency and management visibility
- CTA: "Upgrade your team to Pro" with a seat-count selector
- Email: ROI calculator showing time saved per team member on Pro vs. Free

**Power-free users (advanced feature usage, API calls, integrations):**
- Primary trigger: API rate limits, integration limits, export limits
- Upgrade message: focused on removing technical constraints
- CTA: "Remove limits" with a direct link to the plan that addresses their specific constraint
- Email: technical comparison of Free vs. Pro capabilities for their usage pattern

Implement segment detection using PostHog cohorts. Route each segment to its conversion path via the n8n workflow from the `usage-threshold-detection` drill.

### 4. Generate weekly performance reports

Run the `gate-conversion-health-report` drill configured for the full freemium conversion system (not just feature gates):

The weekly report covers:
- Per-trigger conversion rates vs. 4-week average (detect decay early)
- Per-segment conversion rates (which persona is converting, which is not)
- Experiment outcomes: what was tested, what won, cumulative lift from adopted variants
- Prompt fatigue metrics by segment (power-free users may fatigue faster than occasional users)
- Revenue attribution: total MRR from free-to-paid conversions, broken down by trigger and segment
- Free user pool health: is the pool growing (new signups > conversions + churn) or shrinking

### 5. Optimize checkout and pricing presentation

Based on experiment results and funnel analysis, optimize the conversion endpoint:

- If checkout abandonment is high, test a simplified inline checkout modal (Stripe Checkout embedded in-app) vs. redirect to pricing page
- If users are converting to the cheapest plan and churning within 30 days, test presenting the mid-tier plan as default with the features the user actually needs highlighted
- If trial-to-paid conversion is low, test 7-day vs. 14-day trial durations. Shorter trials create urgency; longer trials allow deeper engagement. Test both.

### 6. Evaluate against threshold

Measure at the end of 2 months:

- **Scale metric**: 500+ free users prompted per month (the system is reaching enough of the free user base)
- **Conversion metric**: Overall >=8% prompted-to-paid. Per-trigger rates within 20% of Baseline.
- **Efficiency metric**: No proportional increase in manual effort despite higher volume (all new triggers and segments are automated)
- **Health metric**: Prompt fatigue rate <15%. Free user pool not shrinking.
- **Revenue metric**: Total MRR from free-to-paid conversions trending upward month-over-month

**Pass:** The system scales. Conversion rate holds. Revenue grows. Proceed to Durable for autonomous optimization.

**Fail:**
- If conversion rate dropped at scale: segment-specific paths are not working. Check which segment is underperforming and whether the messaging resonates with that persona.
- If fatigue rate is high: too many triggers are overlapping. Implement a global prompt budget: maximum N upgrade interactions per user per month across ALL trigger types, and prioritize by expected conversion rate.
- If the free user pool is shrinking: signups are declining or conversion is faster than acquisition. This is actually good (efficient conversion) unless it means the free tier is no longer attractive.

## Time Estimate

- 10 hours: A/B test setup — design experiments for copy, timing, and surface variants across trigger types
- 10 hours: Expand trigger surface area — velocity triggers, behavioral proximity, peer comparison, re-engagement
- 10 hours: Segment-specific conversion paths — cohort creation, routing logic, per-segment prompts and emails
- 8 hours: Weekly report automation, checkout optimization experiments
- 12 hours: Ongoing experiment management, monitoring, and threshold evaluation over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, funnels, cohorts, dashboards | Growth from $0.00045/event — https://posthog.com/pricing |
| Intercom | In-app prompts, segment-specific messages, feature gate UX | ~$75-300/mo at scale — https://www.intercom.com/pricing |
| Loops | Segment-specific email sequences, follow-up variants | Starter $49/mo — https://loops.so/pricing |
| n8n | Trigger detection, segment routing, experiment orchestration | Free self-hosted; Cloud from $24/mo — https://n8n.io/pricing |
| Attio | Revenue attribution, deal tracking, segment CRM data | Free tier — https://attio.com/pricing |

**Play-specific cost:** ~$150-400/mo (Intercom at scale + Loops + PostHog Growth tier)

## Drills Referenced

- `ab-test-orchestrator` — design and run systematic experiments across prompt copy, timing, surface type, and trigger thresholds with PostHog feature flags
- `usage-threshold-detection` — expand the trigger surface with velocity-based, behavioral proximity, peer comparison, and re-engagement triggers
- `gate-conversion-health-report` — weekly performance report covering per-trigger conversion, per-segment metrics, experiment outcomes, and revenue attribution
