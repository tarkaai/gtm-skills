---
name: google-ads-display-campaign
description: Create and configure Google Display Network campaigns for banner ads on industry sites and publications
tool: Google Ads
difficulty: Config
---

# Set Up a Google Display Network Campaign

## Prerequisites

- Google Ads account with API access enabled
- Conversion tracking configured (see `google-ads-conversion-tracking`)
- Banner creative assets in required sizes (see asset specifications below)
- Landing pages built and tracked

## Authentication

Use OAuth 2.0 with the Google Ads API. Required credentials: developer token, OAuth client ID/secret, refresh token, and customer ID.

## Steps

### 1. Create a Display campaign via API

```
POST /customers/{customer_id}/campaigns:mutate
{
  "operations": [{
    "create": {
      "name": "Display - Industry Sites - Q1 2026",
      "advertising_channel_type": "DISPLAY",
      "status": "PAUSED",
      "campaign_budget": "{budget_resource_name}",
      "bidding_strategy_type": "TARGET_CPA",
      "target_cpa": {
        "target_cpa_micros": 25000000
      }
    }
  }]
}
```

Start with `TARGET_CPA` if you have conversion data, otherwise use `MAXIMIZE_CONVERSIONS` for the learning period. Set campaign status to `PAUSED` until all ad groups and creatives are ready.

### 2. Configure placement targeting

Target specific industry sites and publications where your ICP reads:

**Managed placements (specific sites):**
```
POST /customers/{customer_id}/adGroupCriteria:mutate
{
  "operations": [{
    "create": {
      "ad_group": "{ad_group_resource}",
      "placement": {
        "url": "techcrunch.com"
      },
      "status": "ENABLED"
    }
  }]
}
```

**Topic targeting (broader reach):**
```
POST /customers/{customer_id}/adGroupCriteria:mutate
{
  "operations": [{
    "create": {
      "ad_group": "{ad_group_resource}",
      "topic": {
        "topic_constant": "topics/13"
      }
    }
  }]
}
```

Topic constants for B2B SaaS: `/Business & Industrial/Business Services` (13), `/Computers & Electronics/Software` (30), `/Internet & Telecom` (38).

**Custom intent audiences:**
```
POST /customers/{customer_id}/customAudiences:mutate
{
  "operations": [{
    "create": {
      "name": "Intent - DevOps Tools",
      "type": "AUTO",
      "members": [
        {"member_type": "KEYWORD", "keyword": "CI/CD pipeline tools"},
        {"member_type": "KEYWORD", "keyword": "deployment automation"},
        {"member_type": "URL", "url": "competitor-site.com"}
      ]
    }
  }]
}
```

### 3. Upload responsive display ads

Responsive display ads automatically adjust size and format to fit available placements:

```
POST /customers/{customer_id}/adGroupAds:mutate
{
  "operations": [{
    "create": {
      "ad_group": "{ad_group_resource}",
      "ad": {
        "responsive_display_ad": {
          "marketing_images": [
            {"asset": "{landscape_image_asset}"}
          ],
          "square_marketing_images": [
            {"asset": "{square_image_asset}"}
          ],
          "logos": [
            {"asset": "{logo_asset}"}
          ],
          "headlines": [
            {"text": "Cut Deploy Failures by 73%"},
            {"text": "Your Deploy Process Is Broken"},
            {"text": "500+ Teams Use This Playbook"}
          ],
          "descriptions": [
            {"text": "Free guide: the 5-step checklist used by leading engineering teams."},
            {"text": "Stop losing weekends to broken deploys. Get the fix."}
          ],
          "business_name": "Your Company",
          "call_to_action_type": "LEARN_MORE",
          "long_headline": {"text": "The Engineering Team's Guide to Zero-Downtime Deploys"}
        }
      }
    }
  }]
}
```

**Required image assets:**
- Landscape: 1200x628 (minimum 600x314)
- Square: 1200x1200 (minimum 300x300)
- Logo: 1200x1200 (minimum 128x128)
- Logo landscape: 1200x300 (optional but recommended)

Upload assets first via the AssetService:
```
POST /customers/{customer_id}/assets:mutate
{
  "operations": [{
    "create": {
      "name": "hero-banner-landscape",
      "type": "IMAGE",
      "image_asset": {
        "data": "{base64_encoded_image}"
      }
    }
  }]
}
```

### 4. Set frequency capping

Prevent ad fatigue by capping impressions per user:

```
"frequency_caps": [{
  "key": {
    "level": "AD_GROUP_AD",
    "event_type": "IMPRESSION",
    "time_unit": "WEEK"
  },
  "cap": 5
}]
```

Recommended caps: 5 impressions per user per week for awareness, 3 per week for retargeting.

### 5. Configure content exclusions

Protect brand safety by excluding low-quality placements:

```
POST /customers/{customer_id}/campaignCriteria:mutate
{
  "operations": [
    {"create": {"campaign": "{campaign}", "content_label": {"type": "SEXUALLY_SUGGESTIVE"}, "negative": true}},
    {"create": {"campaign": "{campaign}", "content_label": {"type": "BELOW_THE_FOLD"}, "negative": true}},
    {"create": {"campaign": "{campaign}", "placement": {"url": "parked-domains.com"}, "negative": true}}
  ]
}
```

Also exclude: mobile app placements (high accidental click rate), parked domains, and error pages. Add `mobileappcategory::69500` as a negative placement to exclude all mobile app inventory.

### 6. Launch and monitor

Set campaign status to `ENABLED`. Monitor via the GoogleAdsService.Search endpoint:

```
SELECT campaign.name, metrics.impressions, metrics.clicks, metrics.ctr,
       metrics.cost_micros, metrics.conversions, metrics.cost_per_conversion
FROM campaign
WHERE campaign.id = {campaign_id}
  AND segments.date DURING LAST_7_DAYS
```

Check placement reports to identify where ads actually appear. Exclude low-quality placements weekly:

```
SELECT detail_placement_view.display_name, detail_placement_view.target_url,
       metrics.impressions, metrics.clicks, metrics.conversions
FROM detail_placement_view
WHERE campaign.id = {campaign_id}
ORDER BY metrics.impressions DESC
```

## Error Handling

- `CAMPAIGN_BUDGET_NOT_FOUND`: Create the budget resource first via CampaignBudgetService
- `INVALID_IMAGE_SIZE`: Verify image meets minimum dimensions. Re-export at correct resolution.
- `POLICY_VIOLATION`: Review ad text for restricted terms. Google rejects ads with superlatives ("best"), misleading claims, or excessive capitalization.
- `BIDDING_STRATEGY_NOT_AVAILABLE`: Target CPA requires at least 15 conversions in the last 30 days. Fall back to Maximize Conversions.

## Tool Alternatives

- **Microsoft Advertising** (Bing Display): near-identical API structure, lower CPM, smaller but less competitive inventory
- **DV360 (Google Marketing Platform)**: programmatic display across premium exchanges; higher minimum spend ($10K+/mo), better brand safety controls, private marketplace deals with publishers
- **The Trade Desk**: independent DSP for programmatic display; transparent auction, cross-device targeting, strong reporting
- **Amazon DSP**: display ads on Amazon properties and partner sites; useful if ICP is Amazon-adjacent
- **AdRoll**: self-serve display retargeting; simpler than GDN, integrates with Shopify/HubSpot
