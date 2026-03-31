---
name: paid-reddit-ads-baseline
description: >
  Paid Reddit Ads — Baseline Run. Scale the proven Smoke campaign to always-on with $1,000-3,000/mo
  budget, full conversion tracking, and automated daily reporting.
stage: "Marketing > Problem Aware"
motion: "LightweightPaid"
channels: "Paid, Social"
level: "Baseline Run"
time: "8 hours setup + 14 days runtime"
outcome: "≥ 8 leads or ≥ 4 meetings over 14 days at CPA ≤ $150"
kpis: ["Click-through rate", "Cost per click", "Cost per acquisition", "Landing page conversion rate", "Lead quality (ICP match rate)"]
slug: "paid-reddit-ads"
install: "npx gtm-skills add marketing/problem-aware/paid-reddit-ads"
drills:
  - posthog-gtm-events
  - budget-allocation
---

# Paid Reddit Ads — Baseline Run

> **Stage:** Marketing -> Problem Aware | **Motion:** LightweightPaid | **Channels:** Paid, Social

## Outcomes

Prove that Reddit Ads produce leads consistently when run always-on. A passing Baseline demonstrates that the campaign sustains lead flow over 2 weeks with a cost per acquisition the business can tolerate. You need 8 leads or 4 meetings over 14 days with CPA at or below $150.

## Leading Indicators

- Stable or improving CTR over 14 days (no fatigue decay >20%)
- CPA within 120% of Smoke-level CPA by day 7
- At least 50% of leads pass ICP qualification in Attio
- Reddit CAPI events matching PostHog events within 15% (tracking reliability)

## Instructions

### 1. Set up full event tracking

Run the `posthog-gtm-events` drill to establish a complete event taxonomy for this play:

- `paid_reddit_ads_ad_click` — ad click (captured via UTM on landing page load)
- `paid_reddit_ads_page_view` — landing page view
- `paid_reddit_ads_form_focus` — user interacts with the form
- `paid_reddit_ads_lead_captured` — form submitted
- `paid_reddit_ads_lead_qualified` — lead matches ICP in Attio
- `paid_reddit_ads_meeting_booked` — meeting scheduled

Attach properties to every event: `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` (variant ID), `utm_term` (subreddit cluster), `rdt_cid` (Reddit click ID).

Configure the Reddit CAPI (via n8n) to fire server-side `Lead` events for every form submission, ensuring conversion data flows back to Reddit for optimization.

### 2. Build the performance monitoring system

Run the `reddit-ads-performance-monitor` drill to set up:

- Daily automated health checks via n8n (CPA spike, CTR decay, budget utilization, tracking gaps)
- PostHog dashboard with spend vs. leads, CPA trend, CTR by ad group, conversion funnel, and ad variant performance
- Weekly Attio campaign notes with performance summary
- Slack alerts for anomalies

This monitoring system runs for the duration of Baseline and carries forward to Scalable and Durable.

### 3. Optimize budget allocation

Run the `budget-allocation` drill. Using the Smoke test data as your baseline:

- Increase total budget to $1,000-3,000/mo ($70-100/day)
- Allocate 70% to the winning subreddit cluster from Smoke
- Allocate 30% to the secondary cluster for continued testing
- Set rebalancing triggers: if a cluster's CPA exceeds 150% of the other for 5+ days, shift 20% of its budget to the winner

**Human action required:** Approve the increased monthly budget.

### 4. Expand creative variants

Using the winning hook type from Smoke (data, question, or story), create 3 additional ad variants:

- Rotate in 1-2 new variants per week
- Pause any variant whose CTR drops below 50% of the top performer
- Test one new hook type per week (if data won at Smoke, test question variants at Baseline)
- Enable comments on all promoted posts and monitor daily

### 5. Run for 14 days with weekly optimization

**Week 1:**
- Launch expanded campaign with increased budget
- Monitor daily health checks. No creative changes in the first 5 days.
- Respond to promoted post comments within 4 hours during business hours.

**Week 2:**
- Review week 1 performance data
- Pause underperforming ad variants (CTR < 50% of best)
- Replace with new variants
- Rebalance budget between clusters if CPA differs significantly
- If any subreddit has CPA > 2x campaign average, remove it from targeting

### 6. Evaluate against threshold

Measure against: >= 8 leads or >= 4 meetings over 14 days at CPA <= $150.

Document the full Baseline report:

- Total spend and budget utilization
- Impressions, clicks, CTR, CPC by ad group and subreddit
- Leads and meetings by subreddit cluster
- CPA by cluster and overall
- ICP match rate (what % of leads are qualified)
- Best-performing ad variant and hook type
- Conversion funnel: click -> page view -> form focus -> lead -> qualified -> meeting
- Comparison to Smoke results

**PASS:** Reddit Ads are a repeatable lead source. Move to Scalable.
**FAIL:** If CPA is too high, test tighter subreddit targeting or stronger landing pages. If volume is too low, expand to more subreddits or add keyword targeting. If lead quality is poor, refine subreddit selection.

## Time Estimate

- Event tracking setup: 2 hours
- Performance monitoring setup: 2 hours
- Budget allocation analysis: 1 hour
- Creative expansion: 1 hour
- Weekly optimization (2 sessions): 1 hour
- Threshold evaluation and reporting: 1 hour

**Total active time: ~8 hours. Calendar time: 14 days.**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Reddit Ads | Ad platform | $1,000-3,000/mo ad spend. https://ads.reddit.com |
| PostHog | Analytics, dashboards, funnels | Free up to 1M events/mo. https://posthog.com/pricing |
| n8n | Automation (monitoring, CAPI, alerts) | Free self-hosted or $20/mo cloud. https://n8n.io/pricing |
| Attio | CRM for lead tracking and qualification | Free up to 3 users. https://attio.com/pricing |
| Webflow | Landing page hosting | $14-39/mo. https://webflow.com/pricing |

**Estimated monthly cost: $1,020-3,060 (primarily ad spend).**

## Drills Referenced

- `posthog-gtm-events` — full event taxonomy for tracking the Reddit Ads funnel
- `budget-allocation` — data-driven budget distribution across subreddit clusters
