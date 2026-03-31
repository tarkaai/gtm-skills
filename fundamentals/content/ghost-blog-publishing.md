---
name: ghost-blog-publishing
description: Create and publish blog content on Ghost CMS via the Admin API
tool: Ghost
product: Ghost
difficulty: Intermediate
---

# Publish Blog Posts on Ghost

## Prerequisites
- Ghost instance with Admin API access
- Admin API key generated (Ghost Admin > Integrations > Custom Integration)

## Steps

1. **Create a post via Admin API.** Use the Ghost Admin API to create posts programmatically:
   ```
   POST /ghost/api/admin/posts/
   {
     "posts": [{
       "title": "Cold Email Best Practices for 2025",
       "html": "<p>Content here...</p>",
       "status": "draft",
       "tags": [{"name": "outbound"}, {"name": "email"}],
       "feature_image": "https://cdn.example.com/image.jpg"
     }]
   }
   ```
   Write content in HTML or use Ghost's Mobiledoc format. Structure with H2/H3 headings, short paragraphs, and images.

2. **Set SEO metadata via API.** Include meta fields in the post creation:
   ```json
   { "meta_title": "Cold Email Best Practices (under 60 chars)", "meta_description": "Learn the cold email...(under 155 chars)", "slug": "cold-email-best-practices" }
   ```

3. **Add tags and author.** Include tags for categorization and set the correct author in the API payload. Tags help with site navigation and internal linking.

4. **Preview before publishing.** Use the `status: "draft"` flag to create the post as a draft first. Retrieve via `GET /ghost/api/admin/posts/<id>/` to verify formatting.

5. **Publish via API.** Update the post status to publish immediately or schedule:
   ```
   PUT /ghost/api/admin/posts/<id>/
   { "posts": [{ "status": "published", "published_at": "2025-04-01T09:00:00Z" }] }
   ```

6. **Automate distribution.** After publishing, use n8n to automatically share the post: post to LinkedIn via API, send to newsletter subscribers via Loops, and capture the URL for email outreach campaigns.
