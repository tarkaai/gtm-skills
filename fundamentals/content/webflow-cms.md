---
name: webflow-cms
description: Manage Webflow CMS collections for dynamic content via the Webflow API
tool: Webflow
product: Webflow
difficulty: Intermediate
---

# Manage Webflow CMS Collections

## Prerequisites
- Webflow site with CMS plan
- Webflow API token generated

## Steps

1. **Create a CMS collection via API.** Use the Webflow REST API:
   ```
   POST /v2/sites/<site-id>/collections
   { "displayName": "Blog Posts", "singularName": "Blog Post" }
   ```
   Common collections: Blog Posts, Case Studies, Testimonials, Team Members.

2. **Define collection fields via API.** Add fields to the collection:
   ```
   POST /v2/collections/<id>/fields
   { "type": "RichText", "displayName": "Body", "isRequired": true }
   ```
   Blog fields: Title (PlainText), Slug (auto), Body (RichText), Featured Image (ImageRef), Author (Reference), Published Date (Date), Category (Option).

3. **Add CMS items via API.** Create collection items programmatically:
   ```
   POST /v2/collections/<id>/items
   { "fieldData": { "name": "Post Title", "slug": "post-title", "body": "<p>Content...</p>" } }
   ```
   This is how an agent publishes content without manual editing.

4. **Set up dynamic SEO.** Bind meta title and description to collection fields so each page has unique SEO metadata. Configure via the collection template settings.

5. **Publish via API.** Webflow requires a publish action to make CMS changes live:
   ```
   POST /v2/sites/<site-id>/publish
   { "domains": ["your-domain.com"] }
   ```

6. **Automate content pipeline.** Build an n8n workflow: content approved in Airtable -> n8n creates Webflow CMS item via API -> publishes the site -> posts to social media. This removes manual publishing from the workflow.
