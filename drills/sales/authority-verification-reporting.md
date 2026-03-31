---
name: authority-verification-reporting
description: Weekly reporting on authority verification coverage, accuracy, and deal impact across the pipeline
category: Sales
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - attio-deals
  - attio-reporting
  - n8n-workflow-basics
  - n8n-scheduling
---

# Authority Verification Reporting

This drill builds a weekly reporting cycle that tracks how effectively authority is being verified across the pipeline and the downstream impact on deal velocity and close rates. It surfaces deals where authority remains unverified and correlates verification timing with win/loss outcomes.

## Input

- Attio deals with `authority_verification_status` field populated (from `authority-discovery-call` or `stakeholder-enrichment-automation` drills)
- PostHog with authority verification events flowing
- At least 4 weeks of data for trend analysis

## Steps

### 1. Define authority verification metrics

Track these metrics in PostHog:

| Metric | Calculation | Target |
|--------|-------------|--------|
| Authority verification rate | Deals with status = verified / total active deals | >=80% |
| Time to authority verification | Days from deal creation to authority_verified_date | <14 days |
| Authority accuracy rate | Deals where verified authority holder signed the contract / total closed-won | >=90% |
| Multi-threading rate with EB | Deals where Economic Buyer has engagement_level = Active / total active deals | >=60% |
| Unverified deal aging | Count of deals >21 days old with authority_verification_status = unverified | 0 |

### 2. Build the authority verification dashboard

Using `posthog-dashboards`, create panels:

- **Verification funnel**: deal_created -> stakeholder_mapped -> authority_identified -> authority_verified -> deal_won
- **Verification rate trend**: Weekly authority verification rate over last 12 weeks
- **Time to verification distribution**: Histogram of days-to-verification across all deals
- **Authority accuracy**: For closed deals, did the verified authority holder actually sign? Track accuracy over time
- **Stale deals table**: Deals where authority is unverified and deal age >14 days, sorted by deal value descending

### 3. Build the weekly n8n report workflow

Using `n8n-scheduling`, create a Monday 7 AM workflow:

1. Query Attio for all active deals: pull `authority_verification_status`, `authority_verified_date`, `deal_value`, `deal_age`, `stakeholder_count`
2. Query PostHog for authority verification events in the last 7 days
3. Compute weekly metrics (see table above)
4. Compare to prior week and flag any metric that moved >10%
5. Generate the report using Claude:

```
## Authority Verification Weekly Report — Week of {date}

### Pipeline Coverage
- Active deals: {count}
- Authority verified: {count} ({%})
- Authority identified (not yet verified): {count}
- Authority unverified: {count}

### Velocity
- Avg time to verification: {days} (target: <14)
- Deals verified this week: {count}
- Deals stuck (unverified >21 days): {list with deal names and values}

### Accuracy
- Closed-won deals this month: {count}
- Verified EB signed: {count}/{total} ({%})
- Misclassified authority: {count} (detail what went wrong)

### Impact
- Win rate (authority verified): {%}
- Win rate (authority unverified): {%}
- Avg deal velocity (verified): {days}
- Avg deal velocity (unverified): {days}

### Recommendations
- {Specific actions for stuck deals}
- {Process improvements if accuracy is declining}
```

6. Post to Slack and store as an Attio note on the "Authority Verification" campaign record

### 4. Set up real-time alerts

Configure n8n alert branches:
- **Stale authority alert**: Deal passes 14 days without authority verified -> Slack alert to deal owner
- **High-value unverified alert**: Deal value >$50K and authority unverified -> escalation to founder
- **Misclassification alert**: A deal closes and the contract signer is NOT the person tagged as Economic Buyer -> flag for process review

### 5. Build the authority-to-close correlation model

After 12+ weeks of data, analyze the correlation:
1. Pull all closed deals from Attio with: authority_verified_date, deal_created_date, deal_closed_date, deal_outcome (won/lost)
2. Segment by: verified early (<7 days), verified late (7-21 days), verified very late (>21 days), never verified
3. Calculate win rate and deal velocity per segment
4. Use this data to set evidence-based targets for verification timing

This model feeds the `autonomous-optimization` drill at Durable level — it provides the baseline against which optimization experiments are measured.

## Output

- Weekly authority verification report posted to Slack
- Real-time alerts for stale or high-value unverified deals
- Authority-to-close correlation data for optimization
- Dashboard for pipeline review meetings

## Triggers

- Weekly: Full report generation (Mondays at 7 AM)
- Daily: Stale deal alert check
- On deal close: Accuracy validation check
