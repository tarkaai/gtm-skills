---
name: reddit-ads-reporting
description: Pull campaign performance metrics from Reddit Ads API for reporting and optimization
tool: Reddit Ads API
difficulty: Setup
---

# Reddit Ads — Reporting

Pull campaign, ad group, and ad-level performance metrics from the Reddit Ads API. Use this data for performance dashboards, automated optimization decisions, and budget reallocation.

## Endpoints

### Campaign-Level Metrics

```
GET https://ads-api.reddit.com/api/v3/accounts/{account_id}/campaigns/{campaign_id}/reports
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "start_date": "2026-04-01",
  "end_date": "2026-04-07",
  "group_by": ["DATE"],
  "metrics": ["impressions", "clicks", "spend_micro", "ecpc_micro", "ecpm_micro", "ctr", "conversions", "conversion_rate", "cost_per_conversion_micro"]
}
```

### Ad Group-Level Metrics

```
GET https://ads-api.reddit.com/api/v3/accounts/{account_id}/campaigns/{campaign_id}/adgroups/{adgroup_id}/reports
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "start_date": "2026-04-01",
  "end_date": "2026-04-07",
  "group_by": ["DATE"],
  "metrics": ["impressions", "clicks", "spend_micro", "ecpc_micro", "ctr", "conversions"]
}
```

### Ad-Level Metrics

```
GET https://ads-api.reddit.com/api/v3/accounts/{account_id}/campaigns/{campaign_id}/adgroups/{adgroup_id}/ads/{ad_id}/reports
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "start_date": "2026-04-01",
  "end_date": "2026-04-07",
  "group_by": ["DATE"],
  "metrics": ["impressions", "clicks", "spend_micro", "ecpc_micro", "ctr"]
}
```

## Available Metrics

| Metric | Description | Unit |
|---|---|---|
| `impressions` | Number of times ads were shown | Integer |
| `clicks` | Number of ad clicks | Integer |
| `ctr` | Click-through rate (clicks / impressions) | Decimal (0.025 = 2.5%) |
| `spend_micro` | Total spend | Microdollars (divide by 1,000,000 for dollars) |
| `ecpc_micro` | Effective cost per click | Microdollars |
| `ecpm_micro` | Effective cost per 1000 impressions | Microdollars |
| `conversions` | Number of conversion events tracked | Integer |
| `conversion_rate` | Conversions / clicks | Decimal |
| `cost_per_conversion_micro` | Spend / conversions | Microdollars |
| `video_views` | Video view count (video ads only) | Integer |
| `video_view_rate` | Views / impressions (video ads only) | Decimal |
| `video_completions` | Full video views (video ads only) | Integer |

## Group By Dimensions

Available `group_by` options:
- `DATE` — daily breakdown
- `CAMPAIGN` — group by campaign
- `ADGROUP` — group by ad group
- `AD` — group by individual ad
- `SUBREDDIT` — group by targeted subreddit (critical for optimization)
- `DEVICE` — group by desktop/mobile/tablet
- `COUNTRY` — group by geo

Combine dimensions: `"group_by": ["DATE", "SUBREDDIT"]` gives daily metrics per subreddit.

## Python Reporting Script

```python
import requests
from datetime import datetime, timedelta

class RedditAdsReporter:
    BASE_URL = "https://ads-api.reddit.com/api/v3"

    def __init__(self, access_token):
        self.token = access_token

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    def get_campaign_report(self, account_id, campaign_id, days=7):
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        url = f"{self.BASE_URL}/accounts/{account_id}/campaigns/{campaign_id}/reports"
        payload = {
            "start_date": start_date,
            "end_date": end_date,
            "group_by": ["DATE"],
            "metrics": [
                "impressions", "clicks", "spend_micro", "ecpc_micro",
                "ctr", "conversions", "cost_per_conversion_micro"
            ]
        }
        resp = requests.get(url, json=payload, headers=self._headers())
        return resp.json()

    def get_subreddit_breakdown(self, account_id, campaign_id, days=7):
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        url = f"{self.BASE_URL}/accounts/{account_id}/campaigns/{campaign_id}/reports"
        payload = {
            "start_date": start_date,
            "end_date": end_date,
            "group_by": ["SUBREDDIT"],
            "metrics": [
                "impressions", "clicks", "spend_micro", "ctr",
                "conversions", "cost_per_conversion_micro"
            ]
        }
        resp = requests.get(url, json=payload, headers=self._headers())
        return resp.json()

    def calculate_roas(self, report_data, avg_deal_value):
        """Calculate return on ad spend given average deal value per conversion."""
        total_spend = sum(r["spend_micro"] for r in report_data) / 1_000_000
        total_conversions = sum(r["conversions"] for r in report_data)
        revenue = total_conversions * avg_deal_value
        return revenue / total_spend if total_spend > 0 else 0
```

## n8n Reporting Workflow

Build an n8n workflow that runs daily:

1. **HTTP Request node**: Pull Reddit Ads report for last 7 days, grouped by DATE
2. **Function node**: Calculate derived metrics (CPA in dollars, ROAS, week-over-week change)
3. **IF node**: Check if CPA exceeds 150% of target or CTR dropped below 0.3%
4. **Slack node (alert path)**: Send alert with underperforming metrics
5. **PostHog node (logging path)**: Log daily metrics as PostHog events for dashboard
6. **Attio node**: Update campaign record with latest performance data

Schedule: daily at 09:00 UTC, so the team sees yesterday's performance first thing.

## Key Benchmarks (B2B SaaS)

| Metric | Below Average | Average | Good | Excellent |
|---|---|---|---|---|
| CTR | <0.3% | 0.3-0.5% | 0.5-1.0% | >1.0% |
| CPC | >$4.00 | $2.00-4.00 | $1.00-2.00 | <$1.00 |
| CPM | >$12.00 | $6.00-12.00 | $3.50-6.00 | <$3.50 |
| Conversion Rate | <1% | 1-3% | 3-5% | >5% |
| CPA (lead) | >$100 | $50-100 | $25-50 | <$25 |

Reddit CPCs average 42% lower than Facebook and 60% lower than LinkedIn for B2B audiences. However, volume is lower, so budget accordingly.

## Error Handling

- **400 Bad Request**: Invalid date range (start after end) or unsupported metric name. Check spelling against available metrics list.
- **404 Not Found**: Campaign/ad group/ad does not exist or was deleted.
- **429 Rate Limited**: Cache report results. Pull daily reports once per day, not on every dashboard load.
- **Empty results**: Campaign has not spent yet or date range has no data. Check campaign status is ACTIVE.
