---
name: google-ads-display-audiences
description: Build and manage audience segments for Google Display Network campaigns via the Google Ads API
tool: Google Ads
difficulty: Intermediate
---

# Build Google Display Network Audience Segments

## Prerequisites
- Google Ads account with API access
- Active Display campaign (see `google-ads-display-campaign`)
- For remarketing: Google Ads tag installed on website
- For customer match: hashed email list (SHA-256)

## Audience Types

GDN offers five audience targeting mechanisms. Use them in combination for layered targeting.

### 1. In-Market Audiences

People actively researching or comparing products in a category. Highest purchase intent on GDN.

**Query available in-market audiences:**
```
SELECT
  user_interest.user_interest_id,
  user_interest.name,
  user_interest.availabilities
FROM user_interest
WHERE user_interest.taxonomy_type = IN_MARKET
```

**Attach to an ad group:**
```
POST /customers/<id>/adGroupCriteria:mutate
{
  "operations": [{
    "create": {
      "ad_group": "<ad-group-resource>",
      "user_interest": {
        "user_interest_category": "userInterestConstants/<in-market-id>"
      }
    }
  }]
}
```

Key B2B in-market categories: Business Software, CRM Software, Project Management Software, HR Software, Accounting Software, Cloud Computing Services, Web Design & Development Services. Search the taxonomy for your product category.

### 2. Affinity Audiences

People with long-term interests in broad topics. Lower intent than in-market but larger reach.

**Query affinity audiences:**
```
SELECT
  user_interest.user_interest_id,
  user_interest.name
FROM user_interest
WHERE user_interest.taxonomy_type = AFFINITY
```

Use affinity audiences for awareness at the top of the display funnel. Layer with demographics (job title proxies via detailed demographics) to narrow.

### 3. Custom Audiences

Build audiences from keywords, URLs, and apps that your ideal customers interact with.

**Create a custom audience:**
```
POST /customers/<id>/customAudiences:mutate
{
  "operations": [{
    "create": {
      "name": "SaaS Decision Makers - Custom",
      "type": "AUTO",
      "members": [
        { "member_type": "KEYWORD", "keyword": "CRM software comparison" },
        { "member_type": "KEYWORD", "keyword": "best project management tool" },
        { "member_type": "URL", "url": "g2.com/categories/crm" },
        { "member_type": "URL", "url": "capterra.com/crm-software" },
        { "member_type": "URL", "url": "competitor-domain.com" }
      ]
    }
  }]
}
```

Custom audiences are the most powerful GDN targeting for B2B. Include:
- Keywords your ICP searches (from your search ads data)
- URLs of competitor websites, review sites, and industry publications
- Apps your ICP uses (competitor apps, industry tools)

### 4. Remarketing Audiences

Re-engage people who visited your website. Requires the Google Ads remarketing tag or Google Analytics 4 integration.

**Create a remarketing list:**
```
POST /customers/<id>/userLists:mutate
{
  "operations": [{
    "create": {
      "name": "Pricing Page Visitors - 30 days",
      "type": "RULE_BASED",
      "rule_based_user_list": {
        "prepopulation_status": "REQUESTED",
        "flexible_rule_user_list": {
          "inclusive_rule_operator": "AND",
          "inclusive_operands": [{
            "rule": {
              "rule_item_groups": [{
                "rule_items": [{
                  "name": "url__",
                  "string_rule_item": {
                    "operator": "CONTAINS",
                    "value": "/pricing"
                  }
                }]
              }]
            }
          }]
        },
        "membership_life_span": 30
      }
    }
  }]
}
```

Build tiered remarketing lists by intent:
- **High intent (7-day window):** Visited pricing, started signup, or viewed demo page
- **Medium intent (30-day window):** Visited product pages, read 2+ blog posts
- **Low intent (90-day window):** Any site visit, single page view

Always create an exclusion list for existing customers to avoid wasting budget.

### 5. Similar/Lookalike Audiences

Google auto-generates "similar to" audiences based on your remarketing lists and customer match lists. These appear automatically in your audience library once the source list has enough members (typically 100+).

**Attach a similar audience:**
```
POST /customers/<id>/adGroupCriteria:mutate
{
  "operations": [{
    "create": {
      "ad_group": "<ad-group-resource>",
      "user_list": {
        "user_list": "customers/<id>/userLists/<similar-list-id>"
      }
    }
  }]
}
```

Note: Google has been phasing out similar audiences in favor of optimized targeting. If similar audiences are unavailable, use custom audiences built from your customer data (competitor URLs, industry keywords) as an alternative.

## Audience Layering

Combine audience types for precise targeting:
- **In-market + demographics:** Target people in-market for your category who are also in senior management roles
- **Custom audience + placement exclusions:** Target people who browse competitor sites while excluding low-quality placements
- **Remarketing + exclusion:** Retarget site visitors but exclude those who already converted

**Set audience targeting mode:**
```
POST /customers/<id>/adGroups:mutate
{
  "operations": [{
    "update": {
      "resource_name": "<ad-group-resource>",
      "targeting_setting": {
        "target_restrictions": [{
          "targeting_dimension": "AUDIENCE",
          "bid_only": false
        }]
      }
    }
  }]
}
```
`bid_only: false` = targeting (only show ads to this audience). `bid_only: true` = observation (show to everyone, bid higher for this audience). Use targeting mode for GDN campaigns to control spend.

## Error Handling

- **"USER_LIST_NOT_ELIGIBLE":** The remarketing list has fewer than 100 users. Wait for more traffic or broaden the list criteria.
- **"CUSTOMER_MATCH_NOT_ALLOWED":** Account must meet Google's customer match eligibility requirements (good payment history, 90+ day account age, $50,000+ total spend).
- **"USER_INTEREST_NOT_FOUND":** In-market and affinity categories change. Query the full taxonomy periodically and update references.
