---
name: github-repo-create
description: Create a public GitHub repository with description, topics, and initial structure via CLI or API
tool: GitHub CLI
difficulty: Setup
---

# GitHub Repo Create

Create a new public repository on GitHub with proper metadata configured for discoverability.

## Tools

| Tool | Method | Docs |
|------|--------|------|
| GitHub CLI (`gh`) | `gh repo create` | https://cli.github.com/manual/gh_repo_create |
| GitHub REST API | `POST /user/repos` | https://docs.github.com/en/rest/repos/repos#create-a-repository-for-the-authenticated-user |
| GitLab API | `POST /projects` | https://docs.gitlab.com/ee/api/projects.html#create-project |
| Gitea API | `POST /user/repos` | https://gitea.io/en-us/api/ |
| Bitbucket API | `POST /repositories/{workspace}/{repo_slug}` | https://developer.atlassian.com/cloud/bitbucket/rest/api-group-repositories/ |

## Authentication

- **GitHub CLI:** `gh auth login` — uses OAuth device flow or a personal access token
- **GitHub API:** Pass `Authorization: Bearer <PAT>` header. Token needs `repo` scope (or `public_repo` for public repos only)

## Instructions

### Option A: GitHub CLI (preferred)

```bash
gh repo create <org>/<repo-name> \
  --public \
  --description "<one-line summary that includes primary keyword>" \
  --license MIT \
  --clone
```

After creation, add topics:

```bash
gh repo edit <org>/<repo-name> --add-topic "<topic1>" --add-topic "<topic2>"
```

### Option B: GitHub REST API

```bash
curl -X POST https://api.github.com/user/repos \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "<repo-name>",
    "description": "<one-line summary>",
    "private": false,
    "auto_init": true,
    "license_template": "mit",
    "has_issues": true,
    "has_projects": false,
    "has_wiki": false
  }'
```

Then set topics:

```bash
curl -X PUT https://api.github.com/repos/<org>/<repo-name>/topics \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"names": ["topic1", "topic2", "topic3"]}'
```

## Response Format (API)

```json
{
  "id": 123456,
  "full_name": "org/repo-name",
  "html_url": "https://github.com/org/repo-name",
  "clone_url": "https://github.com/org/repo-name.git",
  "default_branch": "main"
}
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `422 name already exists` | Repo with that name exists under the org | Choose a different name or delete the existing repo first |
| `401 Bad credentials` | Token expired or invalid | Re-authenticate with `gh auth login` or refresh PAT |
| `403 forbidden` | Token lacks `repo` scope | Create a new token with correct scopes |

## Validation

After creation, verify the repo is accessible and metadata is set:

```bash
gh repo view <org>/<repo-name> --json name,description,url,repositoryTopics
```
