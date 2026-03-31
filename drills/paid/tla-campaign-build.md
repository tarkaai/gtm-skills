---
name: tla-campaign-build
description: Build and launch a LinkedIn Thought Leader Ads campaign from selected posts with targeting, tracking, and lead routing
category: Paid
tools:
  - LinkedIn Ads
  - PostHog
  - n8n
  - Attio
fundamentals:
  - linkedin-ads-thought-leader-setup
  - linkedin-ads-audience-targeting
  - linkedin-ads-bidding
  - linkedin-ads-measurement
  - posthog-custom-events
  - n8n-triggers
  - n8n-crm-integration
  - attio-contacts
---

# TLA Campaign Build

This drill takes selected thought leader posts (from `tla-post-selection`) and builds them into live LinkedIn Thought Leader Ad campaigns with proper targeting, tracking, and CRM integration. It covers the full lifecycle from campaign creation through launch.

## Prerequisites

- 4-6 posts selected and approved by the thought leader (from `tla-post-selection` drill)
- Thought leader has granted TLA promotion permissions in Campaign Manager
- LinkedIn Campaign Manager with ad account and billing configured
- LinkedIn Insight Tag installed on your website
- PostHog tracking on all landing pages
- Attio CRM configured

## Input

- Post selection brief from `tla-post-selection` drill
- ICP targeting criteria (job titles, seniority, company size, industries)
- Monthly budget allocation for TLAs
- Landing page URLs (if posts drive to specific pages)

## Steps

### 1. Set Up Campaign Structure

Create two campaign groups in Campaign Manager -- one for text/image TLAs and one for video TLAs (different performance profiles warrant separate optimization):

**Campaign Group A -- Text & Image TLAs:**
Using `linkedin-ads-thought-leader-setup`, create the campaign:
- Objective: **Engagement** (recommended for TLAs -- delivers 2x lower CPC than Brand Awareness)
- Ad format: Single image ad
- Placement: LinkedIn feed only
- Add 3-4 text-only and image posts as separate ads

**Campaign Group B -- Video TLAs (if applicable):**
- Objective: **Brand Awareness** (video TLAs optimize better for impressions)
- Ad format: Video ad
- Placement: LinkedIn feed only
- Add 1-2 video posts as separate ads

### 2. Configure Audience Targeting

Using `linkedin-ads-audience-targeting`, build 2-3 audience segments per campaign:

**Segment 1 -- Core ICP (tight):**
- Job function + seniority (Director+) + industry + company size (50-1000)
- Target size: 20,000-80,000
- This segment gets 50% of the budget

**Segment 2 -- Adjacent ICP (broader):**
- Same seniority, broader industry or company size range
- Target size: 80,000-200,000
- This segment gets 30% of the budget

**Segment 3 -- Retargeting (if available):**
- Website visitors from the last 90 days who did not convert
- Upload via LinkedIn Matched Audiences from PostHog export
- This segment gets 20% of the budget

For all segments, configure exclusions:
- Your own company's employees
- Current customers (export from Attio using `attio-contacts`)
- Competitors' employees

### 3. Set Budget and Bidding

Using `linkedin-ads-bidding`:

- Start with **Maximum Delivery** (automated) bidding for the first 2 weeks
- Set daily budget per campaign: minimum $50/day for sufficient data (at $25 CPM, this yields ~2,000 impressions/day)
- After 2 weeks of data, evaluate whether to switch to manual CPC bidding
- If CPC is below $5 with automated bidding, keep automated
- If CPC exceeds $8, switch to manual bidding at your target CPC

Budget allocation across campaigns:
- Text/Image campaign: 70% of total TLA budget
- Video campaign: 30% of total TLA budget

### 4. Install Conversion Tracking

Using `linkedin-ads-measurement` and `posthog-custom-events`:

1. Verify LinkedIn Insight Tag fires on all landing pages
2. Set up conversion actions in LinkedIn Campaign Manager:
   - `tla_website_visit` -- landing page view from TLA traffic
   - `tla_form_submit` -- form submission on landing page
   - `tla_demo_request` -- demo/meeting request
3. Configure PostHog events for TLA-specific tracking:
   - `tla_click` with properties: `post_id`, `thought_leader`, `audience_segment`, `campaign_id`
   - `tla_engagement` with properties: `action_type` (like/comment/share), `post_id`
   - `tla_conversion` with properties: `conversion_type`, `post_id`, `audience_segment`
4. Set up UTM parameters for posts that link to your website:
   - `utm_source=linkedin&utm_medium=paid-social&utm_campaign=tla-[thought-leader-initials]&utm_content=[post-id]`

### 5. Build the CRM Attribution Workflow

Using `n8n-triggers` and `n8n-crm-integration`, create an n8n workflow:

1. **Trigger:** PostHog webhook fires on `tla_conversion` event
2. **Lookup:** Check if the lead email exists in Attio
3. **Create or update:** Using `attio-contacts`, create the contact with:
   - `source: tla`
   - `campaign: [campaign name]`
   - `thought_leader: [name]`
   - `post_id: [post identifier]`
   - `audience_segment: [segment name]`
4. **Log activity:** Create a note in Attio recording the TLA touchpoint
5. **Alert:** For high-value conversions (demo requests), send a Slack notification

### 6. Launch and Verify

1. Activate all campaigns
2. Wait 24 hours, then verify:
   - Ads are serving impressions (check Campaign Manager)
   - Insight Tag is capturing visits (check LinkedIn conversion tracking)
   - PostHog events are flowing (`tla_click`, `tla_engagement`)
   - n8n workflow is triggering on conversions
3. If any component is not working, pause campaigns and troubleshoot before spending further

### 7. First-Week Optimization

After 7 days of data:

1. Pull performance by individual ad (post): pause any ad with CTR below 0.5% (TLA benchmark is 1.5-3%)
2. Pull performance by audience segment: if one segment has CPC 2x higher than another, reduce its budget share
3. Check frequency: if any audience segment shows frequency above 3 in the first week, the audience is too small -- broaden it
4. Review social actions: posts generating comments and shares get organic amplification on top of paid reach -- note which posts trigger conversations

## Output

- 2 LinkedIn TLA campaigns live (text/image + video)
- 4-6 thought leader posts running as ads across 2-3 audience segments
- Conversion tracking configured in LinkedIn + PostHog
- CRM attribution workflow live in n8n
- First-week performance reviewed and underperformers paused

## Triggers

- Campaign launch: one-time setup
- First-week optimization: 7 days after launch
- Ongoing management: weekly review cadence
