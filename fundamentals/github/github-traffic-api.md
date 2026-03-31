---
name: github-traffic-api
description: Fetch repository traffic data (views, clones, referrers, paths) via GitHub API
tool: GitHub API
difficulty: Setup
---

# GitHub Traffic API

Retrieve repository traffic metrics including page views, unique visitors, clone counts, top referral sources, and popular content paths. GitHub only retains traffic data for 14 days, so this must run on a schedule to build historical records.

## Tools

| Tool | Method | Docs |
|------|--------|------|
| GitHub CLI (`gh`) | `gh api repos/{owner}/{repo}/traffic/*` | https://cli.github.com/ |
| GitHub REST API | `GET /repos/{owner}/{repo}/traffic/*` | https://docs.github.com/en/rest/metrics/traffic |
| GitLab API | No direct traffic API; use GitLab Analytics | https://docs.gitlab.com/ee/api/project_statistics.html |
| Bitbucket API | No direct traffic API; use Bitbucket Analytics | https://developer.atlassian.com/cloud/bitbucket/ |

## Authentication

Requires a token with `repo` scope (traffic data is only available to repo collaborators/owners).

## Endpoints

### Page Views (last 14 days)

```bash
gh api repos/<org>/<repo>/traffic/views
```

Response:
```json
{
  "count": 1250,
  "uniques": 487,
  "views": [
    { "timestamp": "2026-03-16T00:00:00Z", "count": 95, "uniques": 42 },
    { "timestamp": "2026-03-17T00:00:00Z", "count": 112, "uniques": 56 }
  ]
}
```

### Clones (last 14 days)

```bash
gh api repos/<org>/<repo>/traffic/clones
```

Response:
```json
{
  "count": 340,
  "uniques": 128,
  "clones": [
    { "timestamp": "2026-03-16T00:00:00Z", "count": 25, "uniques": 12 }
  ]
}
```

### Top Referral Sources

```bash
gh api repos/<org>/<repo>/traffic/popular/referrers
```

Response:
```json
[
  { "referrer": "google.com", "count": 280, "uniques": 150 },
  { "referrer": "twitter.com", "count": 95, "uniques": 62 }
]
```

### Popular Content Paths

```bash
gh api repos/<org>/<repo>/traffic/popular/paths
```

Response:
```json
[
  { "path": "/org/repo", "title": "org/repo: description", "count": 850, "uniques": 340 },
  { "path": "/org/repo/blob/main/README.md", "title": "README.md", "count": 410, "uniques": 200 }
]
```

### Star Count (current)

```bash
gh api repos/<org>/<repo> --jq '.stargazers_count'
```

### Star History (paginated)

```bash
gh api repos/<org>/<repo>/stargazers \
  -H "Accept: application/vnd.github.star+json" \
  --paginate --jq '.[].starred_at'
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `403 Must have push access` | Token user is not a collaborator | Add user as collaborator or use an org-level token |
| `404 Not Found` | Repo does not exist or is private without proper auth | Verify repo name and token scopes |

## Important Notes

- **14-day retention:** GitHub only stores traffic data for 14 days. To build historical data, run this on a daily or weekly schedule and persist results to your own datastore (PostHog, a database, or a JSON file in the repo).
- **Rate limits:** 60 requests/hour unauthenticated, 5,000/hour authenticated. Traffic endpoints are lightweight -- a daily cron is fine.
- **Unique counts:** "Uniques" are based on IP + user-agent, not GitHub accounts. They approximate real visitors but are not exact.
