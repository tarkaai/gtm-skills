---
name: sdk-registry-distribution
description: Distribute an SDK across multiple registries with automated download tracking and conversion funnels
category: SDK
tools:
  - PostHog
  - n8n
  - Attio
  - GitHub CLI
fundamentals:
  - registry-download-tracking
  - posthog-custom-events
  - posthog-funnels
  - n8n-workflow-basics
  - n8n-scheduling
  - attio-notes
  - attio-custom-attributes
  - github-release-publish
---

# SDK Registry Distribution

This drill establishes always-on tracking and distribution management for SDKs published across multiple package registries. It builds the measurement infrastructure that proves SDKs drive signups and tracks adoption over time.

## Input

- At least 1 SDK published via the `sdk-package-scaffold` drill
- PostHog tracking installed on your docs site and product
- n8n instance for scheduled data collection
- Attio CRM for logging SDK-sourced leads

## Steps

### 1. Configure the download tracking pipeline

Using `n8n-scheduling` and `n8n-workflow-basics`, build an n8n workflow that runs weekly (Monday 7am):

For each published SDK, use `registry-download-tracking` to query:
- npm: `https://api.npmjs.org/downloads/point/last-week/@org/package-name`
- PyPI: `https://pypistats.org/api/packages/your-package/recent`
- crates.io: `https://crates.io/api/v1/crates/your-crate`
- RubyGems: `https://rubygems.org/api/v1/gems/your-gem.json`
- NuGet, Go: respective APIs

For each response, extract:
- Downloads in the last 7 days
- Downloads in the last 30 days
- Total downloads (all time)

Send to PostHog as `sdk_weekly_downloads` events:
```json
{
  "event": "sdk_weekly_downloads",
  "properties": {
    "registry": "npm",
    "package_name": "@org/sdk-node",
    "language": "typescript",
    "downloads_7d": 1234,
    "downloads_30d": 5678,
    "downloads_total": 45000,
    "week_start": "2026-03-23"
  }
}
```

### 2. Build the full-funnel conversion tracking

Using `posthog-custom-events` and `posthog-funnels`, instrument the SDK-to-revenue funnel:

**Events to track:**

| Event | Trigger | Properties |
|-------|---------|-----------|
| `sdk_weekly_downloads` | n8n weekly collection | `registry`, `language`, `downloads_7d` |
| `sdk_docs_visit` | Visit to SDK docs page | `language`, `referrer`, `utm_source` |
| `sdk_readme_cta_clicked` | Arrival via registry README UTM | `registry`, `language` |
| `sdk_signup_completed` | Signup from SDK-sourced session | `registry`, `language` |
| `sdk_api_key_created` | First API key by SDK-sourced user | `registry`, `language` |
| `sdk_first_api_call` | First successful API call via SDK | `language`, `sdk_version` |

**Funnels to create:**

1. **Discovery funnel:** `sdk_weekly_downloads` -> `sdk_readme_cta_clicked` -> `sdk_signup_completed`
   (Break down by `registry`)
2. **Activation funnel:** `sdk_signup_completed` -> `sdk_api_key_created` -> `sdk_first_api_call`
   (Break down by `language`)

### 3. Set up release cadence automation

Using `github-release-publish`, establish a release workflow:

1. When merging to main, automatically generate a changelog from commit messages
2. Tag releases following semver (patch for fixes, minor for features, major for breaking)
3. Every release body includes a CTA with UTM: `utm_source=github&utm_medium=release&utm_campaign={language}-sdk-v{version}`
4. n8n workflow triggers on new GitHub release webhook -> posts to Slack announcing the new version

### 4. Log SDK-sourced leads in CRM

Using `attio-custom-attributes`, add SDK-specific fields to your contact/company records:
- `sdk_source_registry` (npm, PyPI, etc.)
- `sdk_source_language` (typescript, python, etc.)
- `sdk_signup_date`

Using `attio-notes`, when a new signup arrives with `utm_source` matching a registry:
1. Create or update the contact in Attio
2. Set `sdk_source_registry` and `sdk_source_language`
3. Add a note: "Signed up via {registry} SDK README CTA on {date}"

### 5. Generate weekly SDK distribution report

The n8n workflow assembles a weekly summary:

```
SDK Distribution Report -- Week of {date}

Downloads (7-day):
  npm @org/sdk-node:    {count} ({change}% vs last week)
  PyPI your-sdk:        {count} ({change}%)
  crates.io your-crate: {count} ({change}%)

Conversion:
  README CTA clicks: {count}
  Signups from SDKs: {count}
  API keys created:  {count}

Top registry by signups: {registry}
```

Post to Slack and store in Attio.

## Output

- Weekly automated download count collection from all registries
- Full-funnel PostHog tracking: downloads -> docs visit -> CTA click -> signup -> activation
- Automated release cadence with conversion-tracked release notes
- SDK-sourced leads tagged in CRM
- Weekly distribution report

## Triggers

- Download collection: weekly via n8n cron
- Conversion tracking: always-on (PostHog events fire in real time)
- Release automation: triggered by GitHub tag push
- Report: weekly, aggregated from all sources
