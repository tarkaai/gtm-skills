---
name: linkedin-ads-thought-leader-setup
description: Configure LinkedIn Thought Leader Ads to promote personal profile posts as sponsored content via Campaign Manager
tool: LinkedIn
product: LinkedIn Ads
difficulty: Config
---

# Set Up LinkedIn Thought Leader Ads

LinkedIn Thought Leader Ads (TLAs) promote organic posts from a personal LinkedIn profile as sponsored content. Unlike standard Sponsored Content that comes from a Company Page, TLAs appear in the feed as a personal post with a small "Promoted by [Company]" label. They achieve 2-5x higher CTR and 3-4x lower CPC than company-page ads because the feed treats them as person-to-person content.

## Prerequisites

- LinkedIn Campaign Manager account with an active ad account
- The thought leader (founder, exec, employee) must have a LinkedIn personal profile
- The thought leader must grant permission to promote their posts
- At least 3-5 organic posts published on the thought leader's profile to select from

## Steps

### 1. Grant Thought Leader Permissions

The thought leader must authorize your ad account to promote their posts:

1. In Campaign Manager, navigate to **Account Assets > Thought Leader Ads**
2. Search for the thought leader by name or LinkedIn profile URL
3. Send a permission request
4. The thought leader receives a LinkedIn notification and must click **Accept** in their Settings > Account Preferences > Thought Leader Ads section
5. Once accepted, their organic posts become available for promotion

**Important:** The thought leader must be a first-degree connection of the Company Page admin OR an employee of the company. Third-party influencers cannot be used unless they are listed as employees or explicitly grant access.

Permission is persistent -- once granted, all future posts from that person are eligible for promotion. The thought leader can revoke access at any time.

### 2. Select Posts for Promotion

In Campaign Manager, when creating a new Sponsored Content campaign:

1. Choose your campaign objective: **Brand Awareness** or **Engagement** (TLAs support these two objectives; Engagement is recommended for lower CPC)
2. At the ad creation step, select **Browse existing content**
3. Filter by the thought leader's name
4. Browse their organic posts -- you will see impressions, reactions, and comments for each
5. Select posts that meet these criteria:
   - Published within the last 365 days (LinkedIn limit)
   - Text-only, single image, video, or document/carousel format (all supported)
   - No third-party tags, polls, or "celebrating" posts (these are not eligible)
   - Posts with articles/newsletters are NOT eligible

**Content format restrictions:**
- Supported: text-only, single image, multi-image, native video, document/carousel
- NOT supported: polls, "celebrating an occasion" posts, reshares, article links, newsletter posts, posts with external links in the body (link-in-first-comment is fine)

### 3. Create the TLA Campaign via Campaign Manager

Since TLAs are not fully supported via the Marketing API for post selection (you must use Campaign Manager UI for the initial setup), the workflow is:

1. **Create Campaign Group:**
   ```
   POST /v2/adCampaignGroups
   {
     "account": "urn:li:sponsoredAccount:<id>",
     "name": "TLA - [Thought Leader Name] - [Quarter]",
     "status": "ACTIVE"
   }
   ```

2. **Create Campaign in Campaign Manager UI:**
   - Objective: Engagement (recommended) or Brand Awareness
   - Ad format: Single image ad (even for text-only TLAs, this is the format category)
   - Placement: LinkedIn feed only (audience network not supported for TLAs)
   - Budget: Set daily budget ($50-100/day minimum for meaningful data)
   - Schedule: Continuous or date-bounded
   - Bidding: Maximum Delivery (automated) to start

3. **Add the thought leader post as ad creative:**
   - Select "Use existing content" > filter by thought leader name
   - Select the chosen post
   - Preview -- the ad will show the original post with "Promoted by [Company]" label

4. **Configure targeting** per `linkedin-ads-audience-targeting` fundamental

**Human action required:** The initial campaign creation for TLAs requires Campaign Manager UI. Once the campaign is live, budget adjustments, targeting changes, and performance monitoring can be done via the Marketing API.

### 4. Run Multiple Posts as a Multi-Ad Campaign

Best practice for TLAs is to run 4-6 posts simultaneously in a single campaign:

1. Add multiple thought leader posts as separate ads within one campaign
2. LinkedIn will auto-optimize delivery toward the best-performing post
3. Separate image/text posts from video posts into different campaigns (they have different performance profiles)
4. Rotate posts every 2-4 weeks to avoid audience fatigue

### 5. Monitor and Manage via API

Once campaigns are live, use the Marketing API for ongoing management:

**Pull performance data:**
```
GET /v2/adAnalytics?campaigns=urn:li:sponsoredCampaign:<id>&dateRange.start.year=2026&dateRange.start.month=1&dateRange.start.day=1&timeGranularity=DAILY
```

Key TLA-specific metrics to track:
- **Engagement rate**: TLAs should achieve 1.5-3% (vs 0.3-0.5% for company ads)
- **CPC to landing page**: Target $2-5 (vs $8-15 for company ads)
- **Social actions** (likes, comments, shares): Track separately as these amplify organic reach
- **Follower gains**: TLAs drive profile follows which compound organic reach over time

**Adjust budget:**
```
PATCH /v2/adCampaigns/<id>
{
  "dailyBudget": {"amount": "150", "currencyCode": "USD"}
}
```

**Pause underperforming ads:**
```
PATCH /v2/adCreatives/<id>
{
  "status": "PAUSED"
}
```

### 6. Track Downstream Conversions

TLAs do not support LinkedIn Lead Gen Forms. Conversions must be tracked via:

1. LinkedIn Insight Tag on your website (for website visits and form submissions)
2. UTM parameters -- add UTMs to the thought leader's post link (if the post contains a link) or to the comment-link
3. PostHog tracking on landing pages to attribute TLA traffic

Set up conversion tracking per `linkedin-ads-measurement` fundamental.

## Error Handling

- **"Post not eligible"**: The post contains a poll, article, reshare, or celebration. Select a different post.
- **"Thought leader not found"**: They must be a 1st-degree connection of the Page admin or listed as an employee. Verify the connection.
- **"Permission pending"**: The thought leader has not accepted the request yet. Resend or have them check Settings > Account Preferences > Thought Leader Ads.
- **Low delivery**: TLAs compete in the same auction as all LinkedIn ads. If delivery is low, increase the daily budget or broaden the audience. Minimum recommended audience: 20,000.
- **Engagement not tracking**: Ensure the Insight Tag is installed. For posts without links, engagement is measured by social actions (likes, comments, shares) only.

## Pricing

- LinkedIn Thought Leader Ads use the same auction system as standard LinkedIn ads
- No additional premium for TLA format
- Typical CPM: $15-35 (lower than standard Sponsored Content due to higher engagement rates)
- Typical CPC: $2-5 (vs $8-15 for company-page Sponsored Content)
- Minimum daily budget: $10/day per campaign
- Recommended test budget: $50-100/day for 2 weeks ($700-1,400 test)
