---
name: docs-platform-publishing
description: Create, update, and publish documentation pages via docs platform APIs (Mintlify, GitBook, ReadMe, Docusaurus, Fumadocs)
tool: Mintlify
product: Docs
difficulty: Setup
---

# Docs Platform Publishing

Programmatically create, update, and publish documentation pages on a docs platform. This fundamental covers the five most common docs platforms used by developer-facing companies.

## Option 1: Mintlify (Git-based)

Mintlify docs are Markdown/MDX files in a Git repository. Publishing is a git push.

**Setup:**
- Docs live in a GitHub repo (e.g., `docs/` directory or dedicated repo)
- `mint.json` at the root defines navigation, theme, and metadata
- Mintlify deploys automatically on push to the configured branch

**Create a page:**
```bash
# Create the MDX file with frontmatter
cat > docs/guides/getting-started.mdx << 'EOF'
---
title: "Getting Started"
description: "Set up your first integration in under 5 minutes"
sidebarTitle: "Getting Started"
---

# Getting Started

Content here...
EOF
```

**Update navigation in mint.json:**
```json
{
  "navigation": [
    {
      "group": "Guides",
      "pages": ["guides/getting-started", "guides/authentication"]
    }
  ]
}
```

**Publish:**
```bash
git add docs/guides/getting-started.mdx mint.json
git commit -m "Add getting started guide"
git push origin main
```

Mintlify auto-deploys within 60 seconds of push.

**SEO metadata:** Set in frontmatter: `title`, `description`, `og:image`. Mintlify auto-generates sitemaps and OG tags.

## Option 2: GitBook (API)

**Authentication:**
```
Authorization: Bearer {GITBOOK_API_TOKEN}
Base URL: https://api.gitbook.com/v1
```

**Create a page:**
```
POST /spaces/{space_id}/content/pages
{
  "title": "Getting Started",
  "description": "Set up your first integration in under 5 minutes",
  "document": {
    "nodes": [
      {
        "type": "heading-1",
        "nodes": [{"type": "text", "value": "Getting Started"}]
      },
      {
        "type": "paragraph",
        "nodes": [{"type": "text", "value": "Content here..."}]
      }
    ]
  }
}
```

**Update a page:**
```
PUT /spaces/{space_id}/content/pages/{page_id}
```

**Publish changes:**
```
POST /spaces/{space_id}/change-requests/{change_request_id}/merge
```

## Option 3: ReadMe (API)

**Authentication:**
```
Authorization: Basic {base64(API_KEY:)}
Base URL: https://dash.readme.com/api/v1
```

**Create a doc:**
```
POST /docs
{
  "title": "Getting Started",
  "category": "{category_id}",
  "body": "# Getting Started\n\nContent in Markdown...",
  "hidden": false,
  "type": "basic"
}
```

**Update a doc:**
```
PUT /docs/{slug}
{
  "body": "Updated Markdown content..."
}
```

**List categories:**
```
GET /categories
```

## Option 4: Docusaurus (Git-based)

Docusaurus docs are Markdown files in a Git repository with a static site build step.

**Create a page:**
```bash
cat > docs/guides/getting-started.md << 'EOF'
---
id: getting-started
title: Getting Started
sidebar_label: Getting Started
sidebar_position: 1
description: Set up your first integration in under 5 minutes
keywords: [setup, quickstart, integration]
---

# Getting Started

Content here...
EOF
```

**Update sidebar (sidebars.js):**
```javascript
module.exports = {
  docs: [
    {
      type: 'category',
      label: 'Guides',
      items: ['guides/getting-started', 'guides/authentication'],
    },
  ],
};
```

**Build and deploy:**
```bash
npm run build
# Deploy via Vercel, Netlify, or GitHub Pages
git add . && git commit -m "Add getting started guide" && git push
```

## Option 5: Fumadocs (Git-based, Next.js)

Fumadocs is a Next.js-based docs framework using MDX files.

**Create a page:**
```bash
cat > content/docs/guides/getting-started.mdx << 'EOF'
---
title: Getting Started
description: Set up your first integration in under 5 minutes
---

# Getting Started

Content here...
EOF
```

**Update meta.json for navigation:**
```json
{
  "title": "Guides",
  "pages": ["getting-started", "authentication"]
}
```

**Publish:**
```bash
git add content/docs/guides/getting-started.mdx
git commit -m "Add getting started guide"
git push origin main
```

## Error Handling

- **Git push rejected:** Pull latest, rebase, push again
- **API 401:** Regenerate API token. Check scopes include write access.
- **API 404 on page update:** Verify the page/slug exists. Use list endpoints first.
- **Build failure (Docusaurus/Fumadocs):** Check MDX syntax errors. Run `npm run build` locally before pushing.
- **Sitemap not updating:** Force sitemap regeneration by clearing build cache and redeploying
