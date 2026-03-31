---
name: airtable-universe-publish
description: Publish a base template to Airtable Universe with optimized description and CTA links
tool: Airtable
difficulty: Setup
---

# Airtable Universe Publish

Publish an Airtable base to Airtable Universe so other users can discover and copy it. Airtable Universe is free for both creators and users.

## Prerequisites

- Airtable account (free or paid)
- A complete, well-structured Airtable base to publish
- Airtable Universe creator profile

## Instructions

### 1. Prepare the base for publication

Ensure the base is self-contained and useful out of the box:
- **Sample data:** Populate tables with 5-15 realistic sample records. Empty bases get fewer copies.
- **Views:** Create 3-5 named views (grid, kanban, calendar, gallery) that demonstrate different ways to use the base.
- **Automations:** If the base includes automations, document them in a "README" table or a long-text field.
- **CTA field:** Add a single-select or long-text field at the top of the main table with a note: "Built by {ProductName}. Get the full platform: {your-url}?utm_source=airtable&utm_medium=universe&utm_campaign=template-{slug}"

### 2. Set up Universe profile

Navigate to Airtable Universe (https://www.airtable.com/universe):
1. Click "Publish and manage" at the bottom of the categories menu
2. Complete your public profile: display name, bio, avatar, and a link to your product website
3. Click "Start publishing"

### 3. Publish the base

1. Open the base you want to publish
2. Click "Publish and manage" in the Universe menu
3. Click "Update base" then confirm "Publish base contents"
4. Fill in listing metadata:

**Title:** Include the primary use-case keyword. "Content Calendar for Marketing Teams" not "My Base."

**Description:** 3-4 paragraphs:
- What the base does and who benefits
- What tables, views, and automations are included
- How to get started (copy the base, fill in your data, customize views)
- CTA: "Get the full {ProductName} platform at {url}?utm_source=airtable&utm_medium=universe&utm_campaign=template-{slug}"

**Category:** Select the best-fit category from Airtable's predefined list.

### 4. Add UTM tracking

All links in the base description and inside the base itself that point to your product should include:
```
?utm_source=airtable&utm_medium=universe&utm_campaign=template-{slug}
```

### 5. Monitor performance

Airtable Universe displays a public "copies" count on each base page. Track this weekly:
- Use the `marketplace-analytics-scraping` fundamental for automated collection
- Or log manually into PostHog as a `marketplace_weekly_metrics` event

## Error Handling

- **Base not appearing after publish:** Allow 24-48 hours for indexing. Ensure your Universe profile is complete.
- **Low copies:** Improve title keywords, add more screenshots to the description, and populate more sample data.
- **Linked tables breaking on copy:** Ensure all inter-table links are within the same base. Cross-base links will break for users who copy.

## Pricing

- Airtable Universe publishing: Free
- Airtable Free plan: Unlimited bases, 1,000 records per base, 1GB attachments
- Airtable Team plan: $20/seat/month billed annually ([airtable.com/pricing](https://airtable.com/pricing))
- All Universe copies: Free for users
