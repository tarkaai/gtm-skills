---
name: figma-community-publish
description: Publish a design template or UI kit to Figma Community with optimized metadata and CTA links
tool: Figma
product: Figma
difficulty: Setup
---

# Figma Community Publish

Publish a Figma file (template, UI kit, design system, or component library) to Figma Community so it appears in search and browse results. Figma Community is free for both creators and users.

## Prerequisites

- Figma account (free or paid)
- Figma Community profile configured (https://www.figma.com/community)
- A complete, well-organized Figma file to publish

## Instructions

### 1. Prepare the Figma file

Ensure the file is publication-ready:
- **Clean page structure:** Use named pages (e.g., "Cover", "Templates", "Components", "How to Use")
- **Cover frame:** Create a 1920x960px frame on the first page. This becomes the Community thumbnail. Include: template name, a visual preview, and your product branding.
- **Documentation page:** Add a page with usage instructions, what's included, and a CTA: "Built by {ProductName} -- get the full platform at {your-url}?utm_source=figma&utm_medium=community&utm_campaign=template-{slug}"
- **Sample data:** Populate all templates with realistic sample data. Empty templates get fewer duplicates.

### 2. Publish to Community

1. Open the file in Figma
2. Click the dropdown arrow next to the file name in the toolbar
3. Select "Publish to Community"
4. Fill in the publish dialog:

**Title:** Include your primary keyword. "Startup Dashboard UI Kit" not "My Design File."

**Description:** 2-3 paragraphs:
- Paragraph 1: What the template contains and who it is for
- Paragraph 2: What's included (number of screens, components, variants)
- Paragraph 3: CTA with UTM-tracked link to your product

**Tags:** Add 5-8 tags matching search terms. Examples: "dashboard", "ui-kit", "startup", "saas", "admin-panel", "figma-template".

**Thumbnail:** Uses the cover frame from step 1.

5. Click "Publish"

### 3. Add UTM-tracked links inside the file

On the documentation/cover page, add text with a hyperlink:
```
{your-url}?utm_source=figma&utm_medium=community&utm_campaign=template-{slug}
```

Figma supports clickable links in text layers -- users who duplicate the file will have these links in their copy.

### 4. Monitor performance

Figma Community shows public stats on the template page:
- **Duplicates:** Number of times users copied the file (primary metric)
- **Likes:** Community appreciation signal
- **Comments:** Engagement and feedback

Check these manually or use the `marketplace-analytics-scraping` fundamental for automated collection.

### 5. Update published files

To push updates to a published Community file:
1. Make changes in the original file
2. Click the dropdown > "Publish update to Community"
3. Add a changelog note describing what changed

Updates re-surface the template in "Recently updated" feeds.

## Error Handling

- **Publish button not available:** Ensure you have a Community profile set up and the file is not inside an organization that restricts Community publishing.
- **Low discoverability:** Check that tags match high-volume search terms in your category. Add more descriptive keywords to the title and description.
- **Comments requesting changes:** Respond to Community comments within 48 hours. Engagement signals boost visibility.

## Pricing

- Figma Community publishing: Free
- Figma Starter plan: Free (up to 3 projects)
- Figma Professional: $15/editor/month billed monthly ([figma.com/pricing](https://www.figma.com/pricing))
- All Community downloads: Free for users
