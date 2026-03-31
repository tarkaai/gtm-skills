---
name: github-repo-setup
description: Scaffold a complete public GitHub sample repo with README CTA, analytics, topics SEO, and social preview
category: GitHub
tools:
  - GitHub CLI
  - PostHog
  - Loops
fundamentals:
  - github-repo-create
  - github-readme-optimization
  - github-topics-seo
  - github-social-preview
  - posthog-custom-events
---

# GitHub Repo Setup

End-to-end workflow to create and publish a GitHub sample or teaser repository optimized for developer discovery and lead capture. This drill produces a live public repo with analytics instrumented and CTA links tracked.

## Input

- **Sample concept:** What code sample or tool to publish (agent provides a concrete example or the human has a codebase ready)
- **ICP description:** Who should discover this repo (language, frameworks, problem domain)
- **Product CTA URL:** Where to send interested developers (signup page, demo booking link)
- **Cal.com booking link:** For high-touch CTA option

## Steps

### 1. Research the keyword landscape

Before creating anything, research what developers search for on GitHub:

```bash
# Find competing repos in this space
gh search repos "<problem domain keyword>" --limit 20 --json fullName,description,stargazersCount,repositoryTopics --sort stars
```

Record:
- Top 10 repos and their star counts (this is your competitive benchmark)
- Common topics used across top repos
- Gaps: problems mentioned in issues of existing repos that nobody has solved
- Naming patterns: how do top repos name themselves?

### 2. Create the repository

Run the `github-repo-create` fundamental:
- Name the repo with the primary keyword (e.g., `webhook-tester`, `api-mock-server`, not `cool-project-v2`)
- Description: verb-first, keyword-rich, under 350 characters
- License: MIT (lowest friction for developers evaluating your code)
- Topics: set 8-12 topics based on keyword research from Step 1

### 3. Write the README

Run the `github-readme-optimization` fundamental:
- Follow the exact section order: Title + Badges, Problem Statement, Quick Start, What It Does, Architecture, CTA Block, Contributing, License
- CTA links must include UTM parameters: `?utm_source=github&utm_medium=readme&utm_campaign=<repo-slug>`
- Quick Start must be copy-pasteable and tested

### 4. Add the sample code

Structure the repo for maximum developer trust:

```
<repo>/
  README.md          # Optimized per step 3
  LICENSE            # MIT
  CONTRIBUTING.md    # Brief contribution guidelines
  .github/
    social-preview.png  # 1280x640 branded image
  src/               # The actual sample code
  examples/          # Usage examples
  package.json       # (or equivalent for your language)
```

The code must:
- Run without errors from a fresh clone
- Include inline comments explaining non-obvious logic
- Use modern idioms for the target language/framework
- NOT require any paid services or API keys to run the basic example

### 5. Instrument analytics

Using the `posthog-custom-events` fundamental, add tracking to the sample if applicable (web-based samples). For all repos, set up external tracking:

- Add a PostHog pixel to any documentation site or landing page linked from the README
- Track these events from the landing page side:
  - `github_readme_cta_clicked` (when someone arrives via the UTM link)
  - `github_demo_booked` (when a GitHub-sourced visitor books a demo)
  - `github_signup_completed` (when a GitHub-sourced visitor signs up)

For the GitHub side, traffic is tracked via the GitHub Traffic API (see `github-traffic-api` fundamental) -- no instrumentation needed in the repo itself.

### 6. Set the social preview

Run the `github-social-preview` fundamental:
- Create a 1280x640 image showing: what the tool does (one line), a code snippet or terminal screenshot, your brand mark
- Upload via the repo settings page

**Human action required:** Upload the social preview image via GitHub repo settings.

### 7. Optimize topics for search

Run the `github-topics-seo` fundamental:
- Set the homepage URL to your product site with UTM parameters
- Verify the repo appears in GitHub search for your target keywords

## Output

- A live public GitHub repository with:
  - Keyword-optimized name, description, and topics
  - README with tested Quick Start and CTA block
  - Working sample code
  - Social preview image
  - Analytics instrumented on linked landing page
- All links tracked with UTM parameters

## Triggers

Run once per sample repo. Re-run when creating additional samples targeting different keywords or audiences.
