---
name: github-release-publish
description: Create a GitHub release with changelog, assets, and announcement body via CLI or API
tool: GitHub
product: CLI
difficulty: Setup
---

# GitHub Release Publish

Create tagged releases on GitHub to generate activity signals (shows in feeds, triggers watchers, improves SEO). Each release is an opportunity to re-engage stargazers and drive traffic back to the README CTA.

## Tools

| Tool | Method | Docs |
|------|--------|------|
| GitHub CLI (`gh`) | `gh release create` | https://cli.github.com/manual/gh_release_create |
| GitHub REST API | `POST /repos/{owner}/{repo}/releases` | https://docs.github.com/en/rest/releases/releases#create-a-release |
| GitLab API | `POST /projects/:id/releases` | https://docs.gitlab.com/ee/api/releases/ |
| Gitea API | `POST /repos/{owner}/{repo}/releases` | https://gitea.io/en-us/api/ |
| Bitbucket API | No native releases; use Downloads API | https://developer.atlassian.com/cloud/bitbucket/ |

## Authentication

Token needs `repo` scope (or `contents: write` for fine-grained tokens).

## Instructions

### Option A: GitHub CLI

```bash
gh release create v1.0.0 \
  --repo <org>/<repo> \
  --title "v1.0.0 - <Short description>" \
  --notes "## What's New

- Feature 1: <description>
- Feature 2: <description>

## Try it

\`\`\`bash
git clone https://github.com/<org>/<repo>.git
cd <repo> && npm install && npm start
\`\`\`

---

**Want [outcome]?** [Try <Product> free](https://yoursite.com/?utm_source=github&utm_medium=release&utm_campaign=<repo>-v1.0.0)" \
  --latest
```

To attach binary assets:

```bash
gh release create v1.0.0 ./dist/tool-linux-amd64 ./dist/tool-darwin-arm64 \
  --repo <org>/<repo> \
  --title "v1.0.0" \
  --notes-file CHANGELOG.md
```

### Option B: GitHub REST API

```bash
curl -X POST https://api.github.com/repos/<org>/<repo>/releases \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -d '{
    "tag_name": "v1.0.0",
    "name": "v1.0.0 - Short description",
    "body": "## What'\''s New\n\n- Feature 1\n- Feature 2\n\n---\n\n**Want [outcome]?** [Try Product free](https://yoursite.com/?utm_source=github&utm_medium=release&utm_campaign=repo-v1.0.0)",
    "draft": false,
    "prerelease": false,
    "make_latest": "true"
  }'
```

## Response Format

```json
{
  "id": 789012,
  "html_url": "https://github.com/org/repo/releases/tag/v1.0.0",
  "tag_name": "v1.0.0",
  "published_at": "2026-03-30T12:00:00Z"
}
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `422 Validation Failed` | Tag already exists as a release | Increment version or delete the existing release first |
| `422 tag_name not well-formed` | Invalid tag format | Use semver format: `v1.0.0` |

## Notes

- **CTA in release notes:** Every release body should include a CTA link with UTM parameters. Stargazers receive release notifications -- this is free re-engagement.
- **Cadence:** Publish releases at least monthly to keep the repo looking active. GitHub surfaces recently-active repos higher in search.
- **Auto-generate notes:** Use `gh release create --generate-notes` to auto-generate from merged PRs.
