---
name: marketplace-template-creation
description: Research, create, and publish a free template or tool to 2-3 marketplaces as a lead-magnet with embedded CTAs and UTM tracking
category: Marketplaces
tools:
  - Notion
  - Gumroad
  - Figma
  - Airtable
  - Clay
  - Attio
fundamentals:
  - notion-template-publish
  - gumroad-product-publish
  - figma-community-publish
  - airtable-universe-publish
  - clay-claygent
  - attio-contacts
---

# Marketplace Template Creation

This drill walks through the end-to-end process of creating a free template or tool and publishing it to template marketplaces as a lead-magnet. The template is designed to attract your ICP, demonstrate your product's value, and drive them to your product via embedded CTAs.

## Input

- ICP definition (output from `icp-definition` drill) -- who your buyers are and what workflows they care about
- Your product's core value proposition -- what problem it solves
- A list of 2-3 target marketplaces (e.g., Notion Marketplace, Gumroad, Figma Community, Airtable Universe)

## Steps

### 1. Research high-demand template topics

Use Clay with the `clay-claygent` fundamental to identify what template topics your ICP searches for:

**Claygent prompt:**
```
For a {your_category} product targeting {your_ICP}, research the top template marketplaces (Notion, Figma, Airtable, Gumroad, Canva). For each marketplace:
1. What are the top 10 most-downloaded free templates in the {your_category} or adjacent categories?
2. What keywords do users search when looking for templates in this space?
3. What gaps exist -- popular search terms with few quality results?
Return a ranked list of template ideas with: topic, target marketplace, estimated demand (high/medium/low), and competition level (high/medium/low).
```

Prioritize: high demand + low competition topics. These represent underserved search terms where your template can rank quickly.

### 2. Design the template

Create a template that delivers standalone value while naturally leading users to your product:

**Template structure:**
- **Core utility:** The template must solve a real workflow problem on its own. A template that only works with your product is not a lead magnet -- it is a feature demo.
- **Embedded product context:** Include sections, comments, or notes that reference how your product extends or automates what the template does manually.
- **CTA placement:** Add 1-2 CTAs (not more) linking to your product with UTM parameters. Place them: (a) in the template's README/About section, and (b) at a natural "what's next" point in the workflow.
- **Sample data:** Populate with realistic sample data. Templates with sample data get 3-5x more downloads than empty ones.

**Template quality checklist:**
- [ ] Solves a specific workflow problem for the ICP
- [ ] Works standalone without requiring your product
- [ ] Includes sample data showing the template in action
- [ ] Has 1-2 CTAs with UTM-tracked links to your product
- [ ] Includes a brief "About" or "How to use" section
- [ ] Is visually clean and well-organized

### 3. Publish to the primary marketplace

Based on your ICP's preferred platform, publish to the best-fit marketplace first:

- **Notion users (PMs, ops, founders):** Use `notion-template-publish`
- **Design-oriented users (designers, marketers):** Use `figma-community-publish`
- **Data-oriented users (ops, analysts):** Use `airtable-universe-publish`
- **General audience or mixed:** Use `gumroad-product-publish` (supports any file type)

Follow the relevant fundamental for full publishing instructions. Key metadata for all:
- Title with primary keyword
- Description leading with the outcome the template delivers
- 3-5 tags matching search terms
- Cover image showing the template populated with sample data

### 4. Cross-publish to secondary marketplaces

Adapt the template for 1-2 additional marketplaces:
- If primary is Notion, create a simplified version for Gumroad (export as PDF + Notion link)
- If primary is Figma, create an Airtable version of any data/tracker components
- Gumroad can host any file type as a universal fallback

Adjust UTM parameters per marketplace: `utm_source={marketplace_name}`.

### 5. Log listings in CRM

Using the `attio-contacts` fundamental, create a campaign record in Attio for each marketplace listing:

Fields: `template_name`, `marketplace`, `listing_url`, `date_published`, `status` (pending_review / live / rejected), `downloads_at_publish` (0).

### 6. Promote the template

After publication, amplify initial downloads:
- Share the listing URL on your social channels (LinkedIn, Twitter/X) with a brief post explaining what the template does
- Post in relevant communities (Reddit, Slack groups, Discord servers) where your ICP gathers
- Add the template link to your product's resources page
- Include a mention in your next email newsletter

## Output

- 1 template published on 2-3 marketplaces
- All listings have UTM-tracked CTAs pointing to your product
- CRM records for each listing
- Initial promotion executed to drive early downloads

## Triggers

- Run once at Smoke level for the first template
- Run again at Scalable level when expanding the template portfolio
- Re-run when creating templates for new use cases or audiences
