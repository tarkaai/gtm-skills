---
name: freemium-model-scalable
description: >
  Freemium Tier Strategy — Scalable Automation. Systematically A/B test upgrade prompts, deploy
  progressive feature gating, and build a freemium conversion health report to sustain >=6%
  free-to-paid conversion at 500+ free users per month.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=6% free-to-paid conversion sustained at 500+ free users/month"
kpis: ["Free signups", "Free-to-paid rate", "Median days to upgrade", "Segment conversion rates", "Prompt CTR by trigger type"]
slug: "freemium-model"
install: "npx gtm-skills add product/onboard/freemium-model"
drills:
  - ab-test-orchestrator
  - feature-readiness-gating
---

# Freemium Tier Strategy — Scalable Automation

> **Stage:** Product -> Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The freemium conversion system scales to 500+ free users per month without proportional effort. A/B testing systematically improves prompt copy, placement, timing, and segmentation. Progressive feature gating replaces blunt plan limits with behavior-based disclosure that creates upgrade motivation at the right moment. A weekly health report monitors the entire pipeline and surfaces which segments, triggers, and surfaces convert best. The conversion rate holds at 6%+ despite the larger, more diverse user base.

## Leading Indicators

- At least 2 A/B tests completed per month with statistically significant results
- Progressive feature gating deployed: users unlock features based on readiness signals, not just plan tier
- Conversion rate stable or improving across at least 3 consecutive weekly health reports
- Prompt fatigue rate below 15% of active free users
- At least 3 distinct conversion segments identified (e.g., limit-driven, feature-driven, time-driven) with per-segment conversion data
- Free user activation rate (signup to first value action) exceeds 65%

## Instructions

### 1. Launch systematic A/B testing on upgrade surfaces

Run the `ab-test-orchestrator` drill to test variations of the upgrade experience. Run tests in this priority order (highest expected impact first):

**Test 1 — Upgrade prompt copy at limit proximity:**
- Hypothesis: "If we show the user's actual usage trajectory ('You'll hit your project limit in 3 days at this rate') instead of the static count ('You've used 4 of 5 projects'), then prompt-to-upgrade CTR will increase by 5pp, because velocity framing creates urgency while static framing does not."
- Control: current static limit message
- Variant: velocity-based message with projected hit date
- Primary metric: `upgrade_prompt_clicked` / `upgrade_prompt_shown`
- Sample size: 200 per variant, ~2 weeks at current volume

**Test 2 — Feature gate presentation:**
- Hypothesis: "If we show a 30-second preview of the gated feature in action (screenshot or short video) instead of a text description, then gate-to-upgrade rate will increase by 3pp, because seeing the feature working reduces the imagination gap."
- Control: text description of the gated feature
- Variant: visual preview with usage example
- Primary metric: `upgrade_completed` where trigger = `feature_gate_hit`

**Test 3 — Upgrade email timing:**
- Hypothesis: "If we send the upgrade email 4 hours after a limit encounter instead of 24 hours, then email-to-upgrade rate will increase by 2pp, because the pain is freshest immediately after hitting the wall."
- Control: 24-hour delay
- Variant: 4-hour delay
- Primary metric: `upgrade_completed` from email-sourced clicks

**Test 4 — Pricing page plan emphasis:**
- Hypothesis: "If we visually highlight the plan one tier above the user's free plan (anchoring) instead of showing all plans equally, then pricing page conversion will increase by 4pp, because choice overload is reduced."
- Control: all plans displayed equally
- Variant: recommended plan highlighted with 'Most popular' badge

For each test, use PostHog feature flags for traffic splitting (50/50). Run each test to planned sample size before evaluating. Never run 2 tests on the same upgrade surface simultaneously. Document every result (hypothesis, variants, sample size, outcome, confidence, decision) in Attio.

### 2. Deploy progressive feature gating

Run the `feature-readiness-gating` drill to replace the blunt free/paid boundary with behavior-based feature disclosure:

- Map all features into four tiers: Core (available immediately on free), Intermediate (unlocked after demonstrating Core mastery), Advanced (requires Intermediate usage + paid plan), Power (paid plan + extended usage)
- For each feature, define specific readiness signals: "Created 3+ projects AND completed 1 workflow" unlocks template access; "Used templates 5+ times AND invited a teammate" unlocks automation rules
- Implement PostHog feature flags gated by readiness cohorts: `tier-intermediate-features`, `tier-advanced-features`
- Build Intercom unlock messages: when a free user reaches a new readiness tier, celebrate the unlock and show what they just gained access to
- For Advanced and Power features (paid-only), show a "teased" locked state: the feature is visible but grayed out, with a tooltip showing the unlock condition AND the plan required

The key insight: progressive gating creates a series of small wins on the free tier that build habit and investment. By the time users encounter the paid gate, they have already built workflows and habits that make upgrading feel like a natural next step rather than a paywall.

### 3. Build the freemium conversion health report

Run the the freemium conversion health report workflow (see instructions below) drill to deploy weekly monitoring of the full pipeline:

- Build the PostHog dashboard: free-to-paid funnel (overall), conversion by trigger type, cohort progression velocity, revenue from conversions, prompt fatigue index, free user pool health
- Define free user health metric: activation state (inactive/activated/habitual/power-free), prompt history, conversion probability score
- Create dynamic cohorts: `free-activated`, `free-upgrade-ready`, `free-prompt-fatigued`, `free-at-risk`
- Schedule the weekly n8n workflow (Monday 08:00): pull funnel data, per-trigger breakdown, revenue attribution, anomaly check. Generate the report via Claude and post to Slack.
- Deploy daily degradation detection: flag any trigger type where conversion rate drops >20% vs. 4-week average. Flag if prompt-fatigued cohort exceeds 15% of active free users.

The health report becomes the feedback loop for the A/B testing program. Each weekly report identifies the weakest point in the funnel, which becomes the next test hypothesis.

### 4. Scale to 500+ free users per month

As volume increases, conversion dynamics change. Larger user bases are more diverse and include users with weaker intent. To maintain 6%+ conversion at scale:

- **Segment the free user pool**: not all free users are equal. Segment by signup source (organic vs. referral vs. paid), company size, and activation velocity. Run separate funnels per segment to identify which segments convert best and which need different treatment.
- **Adjust prompt frequency by segment**: high-activation users who are approaching limits get more prompts (they are ready). Low-activation users who have not reached the value moment get fewer prompts (they need onboarding help, not upgrade pressure).
- **Build a prompt suppression system**: if a user dismisses 3+ upgrade prompts in 14 days, suppress all in-app prompts for that user for 14 days. Switch to email-only at reduced frequency. Reactivate in-app prompts only when the user triggers a new limit event.
- **Route different segments to different upgrade paths**: self-serve checkout for individual users, sales-assisted for teams of 5+, enterprise contact for companies in the target ICP with 100+ employees.

### 5. Evaluate against threshold

After 2 months of always-on operation at 500+ free users/month:

- Free-to-paid rate across all users: >=6%
- Free-to-paid rate per segment: identify top and bottom segments
- Experiment velocity: at least 4 tests completed in 2 months
- Prompt fatigue: <15% of active free users fatigued

If PASS: the system converts at scale with systematic improvement. Proceed to Durable.

If FAIL, diagnose:
- Conversion dropped as volume grew: segment analysis will show which new user segments convert poorly. Build targeted onboarding or different upgrade paths for those segments.
- A/B tests not producing wins: test bigger changes (different value props, restructured pricing, new gated features) rather than incremental copy tweaks.
- Prompt fatigue rising: reduce prompt frequency, diversify surfaces (email, in-app, push), or improve prompt relevance.

## Time Estimate

- 12 hours: set up and run 4 A/B tests over 2 months (3 hours each: hypothesis, setup, monitoring, analysis)
- 16 hours: deploy progressive feature gating (tier mapping, flag setup, Intercom messages, n8n workflow)
- 12 hours: build health report (dashboard, weekly n8n workflow, degradation detection, cohort setup)
- 8 hours: segment analysis and prompt suppression system
- 8 hours: ongoing monitoring, weekly report review, experiment planning (1 hour/week for 8 weeks)
- 4 hours: threshold evaluation, documentation, segment-specific diagnosis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnels, feature flags, experiments, cohorts, dashboards | Free up to 1M events/mo; paid from $0/mo + usage -- [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app upgrade prompts, feature gate messages, unlock celebrations | Essential $29/seat/mo -- [intercom.com/pricing](https://intercom.com/pricing) |
| Loops | Upgrade emails, segment-based sequences | $49/mo for 5,000 contacts -- [loops.so/pricing](https://loops.so/pricing) |
| Attio | CRM records, deal tracking, experiment logs | Free up to 3 seats -- [attio.com/pricing](https://attio.com/pricing) |
| n8n | Health report workflow, degradation detection, prompt routing | Free self-hosted; cloud from $24/mo -- [n8n.io/pricing](https://n8n.io/pricing) |
| Stripe | Checkout sessions, subscription management | 2.9% + $0.30 per transaction -- [stripe.com/pricing](https://stripe.com/pricing) |
| Anthropic API (Claude) | Weekly health report generation | ~$10-20/mo -- [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost: ~$120-250/mo** (Intercom + Loops + n8n + Anthropic; PostHog and Attio free tiers may be sufficient depending on volume)

## Drills Referenced

- `ab-test-orchestrator` -- designs, runs, and evaluates A/B tests on upgrade prompts, gate presentations, email timing, and pricing page layout
- `feature-readiness-gating` -- deploys progressive feature disclosure based on behavior signals, creating a series of small wins before the paid gate
- the freemium conversion health report workflow (see instructions below) -- weekly monitoring of the full free-to-paid pipeline with degradation detection, cohort analysis, and revenue attribution
