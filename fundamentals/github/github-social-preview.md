---
name: github-social-preview
description: Upload a custom social preview image (Open Graph) for a GitHub repository
tool: GitHub API
difficulty: Setup
---

# GitHub Social Preview

Set a custom social preview image (Open Graph / Twitter Card) for a repository. This image appears when the repo URL is shared on Twitter/X, LinkedIn, Slack, Discord, and anywhere that unfurls Open Graph tags. A branded image dramatically increases click-through rates vs. the default GitHub preview.

## Tools

| Tool | Method | Docs |
|------|--------|------|
| GitHub REST API | `PATCH /repos/{owner}/{repo}` (via web upload) | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview |
| GitHub CLI + API | Upload via settings page or API workaround | N/A (no direct API for image upload) |

## Image Specifications

- **Dimensions:** 1280x640px (2:1 aspect ratio)
- **Format:** PNG or JPEG
- **Max file size:** 1MB
- **Safe area:** Keep text within center 1000x500px (edges get cropped on some platforms)

## Image Content Rules

The social preview must communicate in 2 seconds:
1. **What it does** -- one line of text (e.g., "Stream webhooks to localhost")
2. **Visual context** -- a code snippet, architecture diagram, or terminal screenshot
3. **Brand** -- your logo in the corner (small, not dominant)
4. Do NOT include GitHub stars count (it goes stale)
5. Do NOT include version numbers (goes stale)
6. Use high contrast text (white on dark or dark on light) for readability at small sizes

## Instructions

### Option A: GitHub Web UI (simplest)

**Human action required:** Go to `https://github.com/<org>/<repo>/settings`, scroll to "Social preview", click "Edit", upload the image.

### Option B: Automated via GitHub API

GitHub does not provide a direct API endpoint for social preview upload. Workaround using the GraphQL API:

```bash
# First, upload the image and get the URL
# This requires using the GitHub web upload mechanism or a presigned URL approach

# Alternative: Use a GitHub Action to automate this
# .github/workflows/update-social-preview.yml
```

For automation, the most reliable approach is to store the image in the repo at `.github/social-preview.png` and use a GitHub Action that uploads it via a headless browser or the internal API.

### Option C: Generate programmatically

Use a tool like `@vercel/og` or `satori` to generate the image from a template:

```bash
# Install the generator
npm install @vercel/og

# Generate from template (custom script)
node generate-social-preview.js \
  --title "Stream webhooks to localhost" \
  --subtitle "No tunnels. No config." \
  --output social-preview.png
```

## Validation

After setting the preview, verify it renders correctly:

1. Use the Facebook Sharing Debugger: `https://developers.facebook.com/tools/debug/?q=https://github.com/<org>/<repo>`
2. Use the Twitter Card Validator: `https://cards-dev.twitter.com/validator` (paste repo URL)
3. Paste the repo URL in a Slack DM to yourself and confirm the preview looks correct

## Notes

- **Cache busting:** Social platforms cache OG images aggressively. After updating, use the Facebook debugger "Scrape Again" button and wait 24-48 hours for other platforms to refresh.
- **Impact:** A branded social preview can increase link click-through rates by 2-3x when the repo URL is shared on social media or in Slack/Discord communities.
