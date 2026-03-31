---
name: linkedin-thought-leader-ads-baseline
description: >
  Thought Leader Ads — Baseline Run. First always-on TLA campaigns with proper audience segmentation,
  conversion tracking, lead routing, and a 2-week cadence of post rotation. Validate that TLAs
  produce repeatable qualified leads at a sustainable cost per lead.
stage: "Marketing > ProblemAware"
motion: "LightweightPaid"
channels: "Paid, Social"
level: "Baseline Run"
time: "18 hours over 4 weeks"
outcome: ">=50,000 impressions and >=20 qualified leads from $2,000-3,000 budget over 4 weeks, with cost per qualified lead below $150"
kpis: ["Impressions", "Engagement rate", "CPC", "Cost per qualified lead", "Lead-to-meeting conversion rate", "Post rotation cadence"]
slug: "linkedin-thought-leader-ads"
install: "npx gtm-skills add marketing/problem-aware/linkedin-thought-leader-ads"
drills:
  - tla-campaign-build
  - paid-social-audience-builder
  - paid-social-lead-routing
---

# Thought Leader Ads — Baseline Run

> **Stage:** Marketing > ProblemAware | **Motion:** LightweightPaid | **Channels:** Paid, Social

## Outcomes

First always-on Thought Leader Ad campaigns. The agent builds multi-segment campaigns with proper conversion tracking and automated lead routing. The thought leader publishes organically on a regular cadence, and the best-performing posts are rotated into ad campaigns every 2 weeks. Leads flow automatically from LinkedIn through enrichment and scoring into CRM and email nurture. The goal is to prove that TLAs produce repeatable, qualified leads at a sustainable cost.

**Pass threshold:** >=50,000 impressions and >=20 qualified leads from $2,000-3,000 budget over 4 weeks, with cost per qualified lead below $150.

## Leading Indicators

- TLA engagement rate sustains above 1.5% across all campaigns
- CPC remains below $5 (target: $2-4 for Engagement objective TLAs)
- At least 2 audience segments produce qualified leads
- Lead quality: >=50% of leads score 70+ on ICP scoring (via Clay enrichment)
- Post rotation happens on schedule every 2 weeks (no single post runs as an ad for more than 3 weeks)
- Thought leader receives measurable increase in profile visits and connection requests vs pre-TLA baseline

## Instructions

### 1. Build Multi-Segment Campaigns

Run the `tla-campaign-build` drill:

1. Create two campaign groups (text/image TLAs and video TLAs if applicable)
2. Configure 3 audience segments using `paid-social-audience-builder`:
   - **Segment 1 -- Core ICP (tight):** Job function + Director+ seniority + target industry + company size 50-1,000. Budget share: 50%
   - **Segment 2 -- Adjacent ICP (broader):** Same seniority, broader industry or company size range. Budget share: 30%
   - **Segment 3 -- Website retargeting:** Visitors from last 90 days who did not convert (upload from PostHog as LinkedIn Matched Audience). Budget share: 20%
3. Configure exclusions: own employees, current customers (from Attio), competitors
4. Add 4-6 thought leader posts as ads (carry over the Smoke test winners plus 1-2 new posts)
5. Set daily budget: $75-100/day across all campaigns ($2,100-2,800 for 4 weeks)
6. Bidding: Maximum Delivery for the first 2 weeks, then evaluate switching to manual CPC

### 2. Install Full Conversion Tracking

As part of `tla-campaign-build`, set up the tracking layer:

1. Verify LinkedIn Insight Tag on all website pages
2. Create conversion actions in Campaign Manager: website visit, form submission, demo request
3. Configure PostHog events: `tla_click`, `tla_engagement`, `tla_conversion` with properties for post_id, thought_leader, audience_segment, campaign_id
4. Set up UTM parameters on all thought leader posts that contain links: `utm_source=linkedin&utm_medium=paid-social&utm_campaign=tla-baseline`
5. Build the PostHog funnel: `tla_impression > tla_click > page_view > form_submit > demo_booked`

### 3. Deploy Automated Lead Routing

Run the `paid-social-lead-routing` drill adapted for TLA:

Since TLAs do not support LinkedIn Lead Gen Forms, leads come through website conversions:

1. Build an n8n workflow triggered by PostHog `tla_conversion` webhook
2. Enrich each lead via Clay: company data, LinkedIn profile, ICP scoring
3. Create or update the contact in Attio with: `source: tla`, `campaign`, `thought_leader`, `post_id`, `lead_score`
4. If lead_score >= 70: add to Loops high-intent nurture sequence, create a deal in Attio, send Slack alert to sales
5. If lead_score < 70: add to Loops educational nurture sequence
6. Weekly: run a lead quality report comparing TLA leads against leads from other channels

### 4. Establish the Content-to-Ads Pipeline

Set up a repeating cycle that keeps fresh content flowing into campaigns:

**Week 1-2:**
- Thought leader publishes 3-4 organic posts
- Agent monitors organic performance daily

**Week 2 (end):**
- Agent runs `tla-post-selection` drill on the new posts
- Top performers are added to the TLA campaigns
- Worst-performing ads (lowest engagement rate or highest CPC) are paused
- Campaign always has 4-6 active ads

**Week 3-4:**
- Repeat the publish-measure-promote cycle
- After 4 weeks, every original Smoke test post should be retired and replaced with fresher content

### 5. Weekly Performance Review

Every Monday, review campaign performance manually (Durable level automates this):

1. Pull Campaign Manager data: impressions, engagement rate, CPC, conversions by ad and segment
2. Pull PostHog funnel data: TLA click-through to conversion rate
3. Pull Attio data: leads created, lead scores, meetings booked
4. Action:
   - Pause any ad with engagement rate below 1% or CPC above $8
   - Shift budget from underperforming segments to winners
   - If retargeting segment has CPA 50%+ lower than cold segments, increase its budget share
   - Flag any audience approaching frequency 5+ for audience refresh

### 6. Evaluate at 4 Weeks

Run the `threshold-engine` drill:

1. Total impressions (threshold: >=50,000)
2. Total qualified leads (threshold: >=20, where qualified = lead_score >= 70 in Attio)
3. Cost per qualified lead (threshold: below $150)
4. Engagement rate trend: is it stable, improving, or declining week over week?
5. Best-performing audience segment, thought leader (if multiple), and post format

**If PASS:** TLAs produce repeatable qualified leads. Proceed to Scalable with expanded budget, multiple thought leaders, and automated content rotation.

**If FAIL:** Diagnose:
- Low lead volume but good engagement: landing page or CTA is the bottleneck, not the ads. Optimize the conversion path.
- High CPC: audience may be over-targeted. Broaden to adjacent ICP or test different seniority levels.
- Low engagement: content is not resonating. Analyze which pain points drove the best Smoke results and double down.
- Unqualified leads: audience targeting is too broad. Tighten firmographic filters or improve ICP scoring in Clay.

## Time Estimate

- 4 hours: Campaign build (structure, targeting, tracking, lead routing)
- 2 hours: Initial post selection and campaign launch
- 8 hours: Weekly reviews and post rotation over 4 weeks (~2 hours/week)
- 2 hours: Content-to-ads pipeline management
- 2 hours: Final threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn Ads | TLA campaign management | Ad spend only ($2,000-3,000/mo) |
| PostHog | Analytics — funnel tracking, conversion attribution | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM — lead management, deal tracking | $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — lead scoring and company data | $149/mo (Starter) or $349/mo (Explorer) — [clay.com/pricing](https://www.clay.com/pricing) |
| Loops | Email — nurture sequences for TLA leads | $49/mo (Starter) — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Automation — lead routing workflows | $24/mo (Starter) — [n8n.io/pricing](https://n8n.io/pricing) |
| Taplio | LinkedIn analytics for post selection | $49/mo (Standard) — [taplio.com/pricing](https://taplio.com/pricing) |

**Estimated play-specific cost this level:** $2,000-3,000/mo ad spend + ~$300-500/mo tools (Clay, Loops, Taplio, n8n). Total: $2,300-3,500/mo.

## Drills Referenced

- `tla-campaign-build` — build and launch TLA campaigns with targeting, tracking, and CRM integration
- `paid-social-audience-builder` — build and refine audience segments on LinkedIn targeting problem-aware ICP prospects
- `paid-social-lead-routing` — route TLA-sourced leads through enrichment, scoring, CRM, and email nurture automatically
