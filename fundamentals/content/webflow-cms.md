---
name: webflow-cms
description: Set up and manage Webflow CMS collections for dynamic content like blog posts, case studies, and team pages.
tool: Webflow
difficulty: Config
---

# Manage Webflow CMS Collections

### Step-by-step
1. In Webflow, go to CMS > Collections > New Collection.
2. Define the collection: name it (e.g., 'Blog Posts', 'Case Studies', 'Testimonials') and add fields.
3. Common fields for a blog: Title (plain text), Slug (auto-generated), Body (rich text), Featured Image (image), Author (reference to Authors collection), Published Date (date), and Category (option or reference).
4. For case studies: add Company Name, Logo, Industry, Challenge, Solution, Results, and a Pull Quote field.
5. Create a CMS template page: design how each item in the collection will look. Use dynamic elements bound to collection fields.
6. Create a collection list page: design the listing page (e.g., /blog) with cards showing each item's title, excerpt, and image.
7. Add CMS items: go to the collection and create entries. Fill in all fields and publish.
8. Set up dynamic SEO: bind meta title and description to collection fields so each page has unique SEO metadata.
9. Add filtering and search: use Webflow's collection list filters to let users browse by category or tag.
10. Publish changes: Webflow requires a publish action to make CMS changes live. Review changes in the staging preview before publishing.
