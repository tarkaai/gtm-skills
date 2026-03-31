---
name: registry-download-tracking
description: Query download/install counts from package registries via their public APIs
tool: Registry APIs (npm, PyPI, crates.io, NuGet, RubyGems)
difficulty: Setup
---

# Registry Download Tracking

Query download and install counts from package registries to measure SDK adoption over time. Each registry exposes download stats through a public API.

## Tools

| Registry | API Endpoint | Docs |
|----------|-------------|------|
| npm | `GET https://api.npmjs.org/downloads/point/{period}/{package}` | https://github.com/npm/registry/blob/main/docs/download-counts.md |
| PyPI | `GET https://pypistats.org/api/packages/{package}/recent` | https://pypistats.org/api/ |
| crates.io | `GET https://crates.io/api/v1/crates/{crate}` | https://crates.io/apidocs |
| NuGet | `GET https://api.nuget.org/v3/registration5-gz-semver2/{id}/index.json` | https://learn.microsoft.com/en-us/nuget/api/registration-base-url-resource |
| RubyGems | `GET https://rubygems.org/api/v1/gems/{gem}.json` | https://guides.rubygems.org/rubygems-org-api/ |
| Go (proxy) | `GET https://proxy.golang.org/{module}/@v/list` | https://proxy.golang.org/ |

## Authentication

All download count APIs are public and require no authentication.

## Instructions

### npm

```bash
# Downloads in the last 7 days
curl -s "https://api.npmjs.org/downloads/point/last-week/@org/package-name" | python3 -m json.tool

# Downloads in the last 30 days
curl -s "https://api.npmjs.org/downloads/point/last-month/@org/package-name" | python3 -m json.tool

# Daily downloads over a date range
curl -s "https://api.npmjs.org/downloads/range/2026-03-01:2026-03-30/@org/package-name" | python3 -m json.tool
```

Response: `{"downloads": 12345, "start": "2026-03-23", "end": "2026-03-30", "package": "@org/package-name"}`

### PyPI

```bash
# Recent downloads (last day, week, month)
curl -s "https://pypistats.org/api/packages/your-package/recent" | python3 -m json.tool

# Downloads by Python version
curl -s "https://pypistats.org/api/packages/your-package/python_minor?months=1" | python3 -m json.tool
```

Response: `{"data": {"last_day": 500, "last_week": 3200, "last_month": 14000}, "package": "your-package", "type": "recent_downloads"}`

### crates.io

```bash
# Crate metadata including total downloads
curl -s "https://crates.io/api/v1/crates/your-crate" -H "User-Agent: your-app" | python3 -m json.tool
```

Response includes `crate.downloads` (total) and `crate.recent_downloads` (last 90 days).

### RubyGems

```bash
# Gem info including download count
curl -s "https://rubygems.org/api/v1/gems/your-gem.json" | python3 -m json.tool

# Total downloads for all versions
curl -s "https://rubygems.org/api/v1/downloads/your-gem-1.0.0.json" | python3 -m json.tool
```

Response includes `downloads` (total for all versions) and `version_downloads` (current version).

### NuGet

```bash
# Package metadata (total downloads in catalog metadata)
curl -s "https://api.nuget.org/v3/registration5-gz-semver2/yourorg.packagename/index.json" \
  -H "Accept-Encoding: gzip" --compressed | python3 -m json.tool
```

## n8n Integration

Build an n8n workflow to collect all registry stats on a schedule:

1. HTTP Request nodes for each registry API
2. Parse download counts from each response
3. Send as PostHog events: `sdk_weekly_downloads` with properties `{registry, package_name, downloads_7d, downloads_30d}`
4. Store in Attio on the SDK campaign record

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `404 Not Found` | Package name typo or not yet indexed | Verify exact package name; new packages may take hours to appear in stats |
| Rate limiting | Too many requests | npm: 1000/min, PyPI: be polite, crates.io: requires User-Agent header |
