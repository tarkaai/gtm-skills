---
name: technical-proof-library
description: Build and maintain a searchable library of technical proof assets (benchmarks, architecture diagrams, customer references, workaround demos) organized by objection type
category: Demos
tools:
  - Attio
  - Anthropic
  - n8n
  - PostHog
fundamentals:
  - attio-deals
  - attio-notes
  - attio-custom-attributes
  - competitive-intel-aggregation
  - n8n-workflow-basics
  - n8n-scheduling
  - posthog-custom-events
---

# Technical Proof Library

This drill builds a structured, searchable library of technical proof assets that the agent can retrieve instantly when a technical objection is raised. Instead of scrambling to find the right benchmark or architecture diagram during a call, the agent matches the objection to the best available proof and delivers it within minutes.

## Input

- Attio CRM with deal records containing technical objection data
- Existing technical documentation, benchmarks, and case studies
- Historical deal outcomes showing which proof assets influenced resolution

## Steps

### 1. Define the proof asset taxonomy

Create a structured schema for technical proof assets. Each asset maps to one or more gap types:

```json
{
  "proof_assets": [
    {
      "id": "proof-001",
      "title": "API Performance Benchmarks — 99.9% uptime over 12 months",
      "type": "benchmark_data",
      "gap_categories": ["performance", "infrastructure"],
      "objection_types": ["uptime_concern", "scalability_question", "performance_doubt"],
      "format": "pdf",
      "url_or_path": "https://docs.example.com/benchmarks/uptime-2025",
      "customer_reference": "Acme Corp (similar size, similar use case)",
      "effectiveness_score": 0.78,
      "times_used": 14,
      "times_resolved_objection": 11,
      "last_updated": "2026-02-15",
      "stale_after_days": 90
    }
  ]
}
```

### 2. Catalog existing proof assets

Audit all existing technical materials. For each asset, classify:
- **Benchmark data:** Performance metrics, uptime stats, load test results, comparison benchmarks
- **Architecture diagrams:** System architecture, integration patterns, data flow diagrams, security architecture
- **Customer references:** Named customers who solved a similar technical challenge, with permission to reference
- **Live demos:** Pre-built demos showing specific capabilities or workarounds
- **Documentation:** Technical docs, API references, security whitepapers, compliance certificates
- **Case studies:** Written accounts of technical implementations at similar companies

Store the catalog as Attio records (create a custom "Proof Assets" object) or as structured notes.

### 3. Build the retrieval workflow

Create an n8n workflow that, given a technical objection, retrieves the most relevant proof:

**Trigger:** Webhook from the `technical-gap-assessment` drill or manual API call with `{ "gap_type": "...", "objection_category": "...", "prospect_industry": "...", "prospect_size": "..." }`

**Step 1:** Query Attio for proof assets matching the gap type and objection category.

**Step 2:** Rank by: (a) effectiveness_score (highest first), (b) relevance to prospect industry and size, (c) recency (prefer recently updated assets).

**Step 3:** Return the top 3 proof assets with links and recommended delivery method:
- If on a live call: share the link in chat or screenshare
- If follow-up: attach to the post-call email
- If pre-call prep: include in the call brief

**Step 4:** Fire PostHog event:
```json
{
  "event": "proof_asset_retrieved",
  "properties": {
    "deal_id": "...",
    "gap_type": "performance",
    "objection_type": "scalability_question",
    "asset_id": "proof-001",
    "asset_type": "benchmark_data",
    "delivery_method": "follow_up_email"
  }
}
```

### 4. Track proof asset effectiveness

After each use, track whether the proof asset helped resolve the objection:

When a technical objection that received a proof asset is later marked `resolved` in Attio, fire:
```json
{
  "event": "proof_asset_outcome",
  "properties": {
    "asset_id": "proof-001",
    "deal_id": "...",
    "objection_resolved": true,
    "days_to_resolution": 3
  }
}
```

Weekly, recalculate `effectiveness_score` for each asset:
`effectiveness_score = times_resolved_objection / times_used`

Assets with score below 0.3 after 10+ uses should be flagged for review or replacement.

### 5. Identify proof gaps

Weekly, query Attio for technical objections where no matching proof asset existed:
- Log these as "proof gaps" — objection types that need new assets
- Rank by frequency: if the same gap type appears 3+ times without proof, it is a priority
- Generate a task to create the missing proof asset

Send a weekly Slack summary:
```
## Proof Library Health — Week of {date}
- Total assets: {n}
- Assets used this week: {n}
- Average effectiveness: {score}
- Proof gaps identified: {n} (top gap: {type} — appeared {n} times with no matching asset)
- Stale assets (>90 days without update): {n}
```

### 6. Set up asset refresh schedule

Create an n8n cron (monthly) that checks each proof asset's `last_updated` against `stale_after_days`:
- If stale: ping the asset owner (via Slack or email) to refresh
- If a benchmark, re-run the benchmark or pull updated metrics
- If a customer reference, verify the customer is still referenceable and the data is current

## Output

- Structured, searchable proof library in Attio
- Instant retrieval of relevant proof assets when an objection is raised
- Effectiveness tracking per asset
- Gap identification for missing proof types
- Automated staleness alerts and refresh reminders

## Triggers

- **Retrieval:** On-demand via n8n webhook when a gap assessment produces a gap, or when a technical objection is raised on a call
- **Tracking:** Automated via Attio webhook when objection status changes
- **Health check:** Weekly cron via n8n
- **Refresh:** Monthly cron via n8n
