---
name: github-topics-seo
description: Optimize repository topics, description, and URL for GitHub search and Google indexing
tool: GitHub CLI
difficulty: Config
---

# GitHub Topics SEO

Optimize a repository's metadata so it ranks in GitHub search, GitHub Explore, and Google. GitHub repos are indexed by Google and rank well for developer-intent queries.

## Tools

| Tool | Method | Docs |
|------|--------|------|
| GitHub CLI (`gh`) | `gh repo edit` | https://cli.github.com/manual/gh_repo_edit |
| GitHub REST API | `PATCH /repos/{owner}/{repo}` + topics endpoint | https://docs.github.com/en/rest/repos/repos#update-a-repository |
| GitLab API | `PUT /projects/:id` with `topics` field | https://docs.gitlab.com/ee/api/projects.html#edit-project |

## Instructions

### 1. Research keywords

Before setting topics, research what your ICP searches for on GitHub:

```bash
# Search GitHub for repos in your space and note their topics
gh search repos "<your problem domain>" --limit 20 --json fullName,description,repositoryTopics
```

Also check:
- GitHub Explore trending topics: https://github.com/topics
- Google autocomplete for `github <your keyword>`
- npm/pip/crates download stats for related packages

Compile a list of 15-20 candidate topics ranked by search volume and relevance.

### 2. Set repository topics (max 20)

```bash
gh repo edit <org>/<repo> \
  --add-topic "topic-1" \
  --add-topic "topic-2" \
  --add-topic "topic-3"
```

Or via API (replaces all topics):

```bash
curl -X PUT https://api.github.com/repos/<org>/<repo>/topics \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"names": ["topic-1", "topic-2", "topic-3"]}'
```

**Topic selection rules:**
- Include 2-3 broad topics (e.g., `python`, `api`, `developer-tools`)
- Include 3-5 specific topics (e.g., `webhook-testing`, `local-tunnel`, `api-mocking`)
- Include 1-2 problem-oriented topics (e.g., `integration-testing`, `ci-cd`)
- Include your product name as a topic if it has brand recognition
- Never use more than 20 topics (GitHub hard limit)
- Use hyphens, not underscores; all lowercase

### 3. Optimize repository description

```bash
gh repo edit <org>/<repo> --description "<keyword-rich description, max 350 chars>"
```

The description should:
- Start with a verb (Build, Test, Monitor, Stream, Connect)
- Include the primary keyword in the first 10 words
- State the use case, not the technology
- End with the differentiation vs. alternatives

Example: "Stream webhook events to localhost for testing -- no tunnels, no config, works with any HTTP framework"

### 4. Set the homepage URL

```bash
gh repo edit <org>/<repo> --homepage "https://yoursite.com/?utm_source=github&utm_medium=repo_homepage&utm_campaign=<repo>"
```

This URL appears prominently in the repo header. Include UTM parameters.

### 5. Enable GitHub Pages (optional, for docs)

If the sample has documentation, enable GitHub Pages to get a `<org>.github.io/<repo>` URL. This creates an additional Google-indexable page.

```bash
gh api repos/<org>/<repo>/pages \
  -X POST \
  -f source='{"branch":"main","path":"/docs"}'
```

## Validation

After optimization, verify:

```bash
gh repo view <org>/<repo> --json description,homepageUrl,repositoryTopics
```

Check that the repo appears in GitHub search for target keywords:

```bash
gh search repos "<primary keyword>" --limit 10 --json fullName
```

## Notes

- **Re-optimize monthly:** As your repo gains stars and forks, it will rank higher. Re-research keywords and update topics as the competitive landscape changes.
- **Google indexing:** GitHub repos are crawled within 24-48 hours of creation. Description and README content are the primary ranking factors.
- **Featured topics:** Repos associated with "featured" topics on GitHub Explore get additional visibility.
