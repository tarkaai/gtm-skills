---
name: value-asset-refresh-pipeline
description: Continuously refresh, version, and create new value assets based on performance data and market changes
category: Content
tools:
  - Anthropic
  - Clay
  - PostHog
  - n8n
fundamentals:
  - ai-content-ghostwriting
  - anthropic-api-patterns
  - clay-claygent
  - posthog-custom-events
  - posthog-funnels
  - n8n-workflow-basics
  - n8n-scheduling
---

# Value Asset Refresh Pipeline

This drill keeps your value assets current and creates new ones based on what is working. Stale assets lose credibility. This pipeline detects when an asset needs updating and automates the refresh cycle.

## Input

- At least one live value asset with 4+ weeks of outreach data
- PostHog tracking on asset engagement (link clicks, page views, reply sentiment)
- Attio records showing which prospects engaged with which assets
- ICP definition and pain point research

## Steps

### 1. Build the asset performance dashboard

Using `posthog-custom-events` and `posthog-funnels`, create a PostHog insight that tracks per asset:

- **Click-through rate**: % of email recipients who clicked the asset link
- **Reply rate by step**: % of recipients who replied at each sequence step
- **Asset-referencing reply rate**: % of positive replies that specifically mention the asset content
- **Meeting conversion**: % of asset-clickers who eventually booked a meeting
- **Funnel**: email_sent -> link_clicked -> reply_received (positive) -> meeting_booked

Track these weekly. An asset is performing when its click-through rate is above 15% and its asset-referencing reply rate is above 3%.

### 2. Define refresh triggers

Set up an n8n workflow using `n8n-scheduling` that runs weekly and checks:

- **Performance decay**: Click-through rate has dropped 30%+ from its peak over 4 weeks. Cause: asset fatigue or market shift. Action: refresh the asset content.
- **Data staleness**: Asset contains data points older than 6 months. Action: update the data.
- **Competitive displacement**: A competitor published a similar or better asset (detected via `clay-claygent` monitoring competitor content). Action: differentiate or create a new asset.
- **ICP shift**: New pain points surfacing in prospect replies that the current asset does not address. Action: create a supplementary asset.

### 3. Execute the refresh workflow

When a trigger fires:

**For content refresh (same topic, updated data):**
1. Pull the current asset text
2. Use `clay-claygent` to research 20 companies for updated pain point data
3. Use `anthropic-api-patterns` to generate updated sections with new data
4. **Human action required:** Founder reviews updated draft, verifies data, approves
5. Publish updated asset at the same URL (preserves link equity)
6. Version the old asset (rename to `{slug}-v1`) for historical tracking
7. Log `value_asset_refreshed` event to PostHog with version number

**For new asset creation (different topic or format):**
1. Run the full `value-asset-creation` drill with the new pain point
2. Create a new campaign variant in Instantly that uses the new asset
3. A/B test new asset against current asset: split the next prospect batch 50/50
4. After 100 sends per variant, compare asset-referencing reply rates
5. Promote the winner; archive the loser

### 4. Build an asset library over time

After 3+ months, you will have multiple assets. Organize them:

- Tag each asset by ICP segment, pain point, and funnel stage
- In Clay, add an `assigned_asset` column that matches each prospect to the most relevant asset based on their `pain_category`
- Route different prospect segments to different assets automatically

### 5. Automate the quarterly asset review

Using `n8n-workflow-basics` and `n8n-scheduling`, create a quarterly workflow that:

1. Pulls performance data for all assets from PostHog
2. Ranks assets by meeting conversion rate
3. Flags assets below the performance threshold for refresh or retirement
4. Generates a brief via `anthropic-api-patterns` summarizing: top performer, worst performer, recommended new topics based on reply analysis
5. Posts the brief to Slack for founder review

## Output

- Weekly automated asset performance monitoring
- Triggered refresh workflows when assets decay
- A growing library of segmented value assets
- Quarterly asset performance reviews

## Triggers

Weekly automated monitoring runs via n8n. Refresh workflows trigger on performance decay. Quarterly reviews run on a fixed schedule. At Durable level, this drill feeds into the `autonomous-optimization` drill for continuous experimentation.
