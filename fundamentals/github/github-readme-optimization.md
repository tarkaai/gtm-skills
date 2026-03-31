---
name: github-readme-optimization
description: Write and push a README.md structured for developer engagement and lead capture via CTA
tool: GitHub CLI / git
difficulty: Config
---

# GitHub README Optimization

Write a README.md that serves dual purposes: help developers use the sample/tool AND convert interested readers into leads. The README is the primary landing page for any GitHub repo.

## Tools

| Tool | Method | Docs |
|------|--------|------|
| GitHub CLI (`gh`) | Commit and push via git | https://cli.github.com/ |
| GitHub REST API | `PUT /repos/{owner}/{repo}/contents/{path}` | https://docs.github.com/en/rest/repos/contents |
| GitLab API | `PUT /projects/:id/repository/files/:file_path` | https://docs.gitlab.com/ee/api/repository_files.html |
| Gitea API | `PUT /repos/{owner}/{repo}/contents/{filepath}` | https://gitea.io/en-us/api/ |
| Bitbucket API | `POST /repositories/{workspace}/{repo_slug}/src` | https://developer.atlassian.com/cloud/bitbucket/rest/ |

## README Structure

Write the README in this exact order. Every section serves a specific conversion or engagement purpose:

### 1. Title + Badges (first fold)

```markdown
# <Repo Name>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/<org>/<repo>)](https://github.com/<org>/<repo>/stargazers)

<One sentence: what this does and who it's for.>
```

The title must include the primary search keyword. Badges provide social proof signals.

### 2. Problem Statement (3 sentences max)

Describe the pain this sample solves. Use the exact words your ICP uses to describe this problem. Do NOT mention your product here.

### 3. Quick Start (copy-pasteable)

```markdown
## Quick Start

\`\`\`bash
git clone https://github.com/<org>/<repo>.git
cd <repo>
npm install  # or pip install, cargo build, etc.
npm start
\`\`\`
```

Must be copy-pasteable and run without errors. Test it.

### 4. What It Does (feature list)

3-5 bullet points. Each bullet: what + why it matters. Example:
- "Streams webhook events to any HTTP endpoint -- so you can test integrations locally without deploying"

### 5. Architecture / How It Works (optional diagram)

If the sample is non-trivial, include a Mermaid diagram or ASCII art showing the data flow. Developers trust repos with visible architecture.

### 6. CTA Block (the conversion point)

```markdown
## Want [outcome your product delivers]?

This sample shows [X]. **[Product Name]** does this and more, automatically.

[**Try it free**](https://yoursite.com/?utm_source=github&utm_medium=readme&utm_campaign=<repo-name>) | [Book a demo](https://cal.com/yourteam/demo?utm_source=github&utm_medium=readme&utm_campaign=<repo-name>)
```

Rules for the CTA:
- Place it after the developer has seen value (never at the top)
- Use UTM parameters on every link for attribution
- Offer two paths: self-serve (try/signup) and high-touch (demo/call)
- Frame the CTA as an upgrade from the sample, not an unrelated pitch

### 7. Contributing + License

```markdown
## Contributing

PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT -- see [LICENSE](LICENSE).
```

Open-source license lowers friction. MIT is the safest default for samples.

## Instructions

1. Draft the README following the structure above
2. Write the content using the ICP's vocabulary (pull from customer interviews, support tickets, competitor docs)
3. Include UTM parameters on ALL links back to your site: `?utm_source=github&utm_medium=readme&utm_campaign=<repo-slug>`
4. Commit and push:

```bash
git add README.md
git commit -m "docs: add README with quick start and CTA"
git push origin main
```

Or via API:

```bash
curl -X PUT https://api.github.com/repos/<org>/<repo>/contents/README.md \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -d '{
    "message": "docs: add README with quick start and CTA",
    "content": "<base64-encoded-content>"
  }'
```

## Validation

- Render the README on GitHub and confirm all links work
- Confirm UTM parameters are present on every external link
- Confirm the Quick Start runs without errors on a clean machine
- Confirm the CTA is visible without excessive scrolling (within first 3 screen-heights)
