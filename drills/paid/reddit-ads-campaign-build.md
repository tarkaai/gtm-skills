---
name: reddit-ads-campaign-build
description: Build a complete Reddit Ads campaign from subreddit research through ad creative and conversion tracking
category: Paid
tools:
  - Reddit Ads API
  - PostHog
  - Webflow
fundamentals:
  - reddit-ads-campaign-setup
  - reddit-ads-audience-targeting
  - reddit-ads-creative
  - reddit-ads-conversion-tracking
  - subreddit-research
  - webflow-landing-pages
  - posthog-custom-events
---

# Reddit Ads Campaign Build

This drill builds a complete Reddit Ads campaign: from subreddit research to targeting configuration, ad creative, landing page, and conversion tracking. Designed for B2B SaaS targeting problem-aware prospects in specific Reddit communities.

## Input

- ICP definition: who you are targeting (job title, industry, pain points)
- Landing page offer: what value you are driving to (checklist, guide, demo, tool)
- Budget: daily budget in dollars (minimum $20/day recommended for meaningful data)
- Duration: campaign run time (minimum 7 days for Smoke, 14+ for Baseline)

## Steps

### 1. Research target subreddits

Run the `subreddit-research` fundamental to identify 10-15 candidate subreddits where your ICP participates. Score each by ICP fit, activity, engagement, accessibility, and competition. Select the top 8-10.

Organize selected subreddits into 2-3 clusters:

| Cluster | Subreddits | Theme |
|---|---|---|
| Core ICP | r/SaaS, r/startups, r/EntrepreneurRideAlong | Direct ICP match |
| Technical | r/devops, r/sysadmin, r/webdev | Technical practitioners with the problem |
| Adjacent | r/smallbusiness, r/marketing | Broader audience that may have the problem |

### 2. Build the landing page

Using the `webflow-landing-pages` fundamental, create a dedicated landing page for this campaign. Requirements:

- Headline matches the ad creative promise (consistency is critical for Reddit audiences)
- Content is ungated or optionally gated (free value accessible without email)
- Optional email capture for deeper content or notifications
- PostHog tracking installed (page view, scroll depth, form submit)
- Reddit Pixel installed (see step 4)
- UTM parameter capture implemented

**Human action required:** Review and approve the landing page before launching ads.

### 3. Configure conversion tracking

Using the `reddit-ads-conversion-tracking` fundamental:

1. Install the Reddit Pixel on the landing page
2. Set up `rdt_cid` click ID capture on landing page load
3. Configure standard events: `PageVisit` on page load, `Lead` on form submit
4. Set up server-side CAPI in n8n for form submissions
5. Verify tracking fires correctly using Reddit Pixel Helper and Event Testing

Using `posthog-custom-events`, fire parallel PostHog events:
- `paid_reddit_ads_page_view` on landing page load
- `paid_reddit_ads_lead_captured` on form submit
- Include properties: `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `rdt_cid`

### 4. Create the campaign structure

Using the `reddit-ads-campaign-setup` fundamental:

1. Create a campaign with objective `CONVERSIONS`, daily budget, and start/end dates
2. Create 2-3 ad groups, one per subreddit cluster (from step 1)
3. Set each ad group with appropriate subreddit targets, geo targeting (US/UK/CA unless specified otherwise), and CPC bidding
4. Start CPC bid at $2.00-3.00 for B2B subreddits. Adjust after 3 days of data.

### 5. Create ad creative

Using the `reddit-ads-creative` fundamental, create 3 ad variants per ad group:

- **Variant A — Data hook**: Lead with a specific statistic or research finding
- **Variant B — Question hook**: Ask a question that ICP prospects would answer "yes" to
- **Variant C — Story hook**: Share a specific result or case study outcome

Each ad includes:
- Headline (under 100 characters, Reddit-native tone)
- Body text (under 200 characters, value-first, no hard sell)
- Click URL with UTM parameters and `utm_content` set to the variant ID
- CTA button (`LEARN_MORE` for content, `SIGN_UP` for trial/demo)

Enable comments on promoted posts. Plan to monitor and respond to comments within 4 hours during business hours.

### 6. Review and launch

Before activating:
- Verify all UTM parameters are correct across all ad URLs
- Confirm Reddit Pixel fires on the landing page
- Confirm PostHog events fire alongside Reddit events
- Review ad creative for Reddit compliance (no misleading claims, landing page matches ad promise)
- Check audience size estimates for each ad group (target 50k-500k)

**Human action required:** Approve the campaign structure and budget, then activate the campaign.

### 7. Post-launch monitoring (first 48 hours)

- Monitor ad approval status (Reddit reviews all ads, 24-48 hour turnaround)
- Check that conversion events are flowing to Reddit and PostHog
- Respond to any comments on promoted posts
- Verify spend is tracking to budget (no overspend, no underspend from delivery issues)

## Output

- 1 campaign with 2-3 ad groups targeting different subreddit clusters
- 6-9 ad variants (3 per ad group) with Reddit-native creative
- 1 dedicated landing page with Reddit Pixel + PostHog tracking
- Server-side CAPI configured for form submissions
- UTM-tagged URLs for full attribution chain
