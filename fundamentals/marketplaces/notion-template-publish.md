---
name: notion-template-publish
description: Publish a Notion template to the Notion Marketplace with optimized metadata and tracking links
tool: Notion
product: Notion
difficulty: Setup
---

# Notion Template Publish

Publish a template to the Notion Marketplace so it appears in search and browse results. This fundamental covers creating the template, configuring marketplace metadata, and submitting for review.

## Prerequisites

- Notion account with a workspace containing the template you want to publish
- Notion Marketplace creator profile (set up at https://www.notion.com/marketplace)
- Template must be a complete, working Notion page or database system

## Instructions

### 1. Prepare the template page

Ensure the template is in a standalone Notion page (not nested inside a private workspace page that has other content). The template page should be self-contained -- all linked databases, views, and sub-pages must be within the template's page tree.

Add an "About" section at the top of the template with:
- What the template does (1-2 sentences)
- Who it is for (target user/role)
- How to get started (3-5 bullet steps)
- A CTA linking to your product: `[Get started with {ProductName}]({your-url}?utm_source=notion&utm_medium=marketplace&utm_campaign=template-{slug})`

### 2. Configure marketplace listing metadata

Via the Notion Marketplace creator dashboard (https://www.notion.com/marketplace):

**Title:** Include the primary use-case keyword. Example: "Startup OKR Tracker" not "My Template."

**Description (max 200 chars):** Lead with outcome. "Track quarterly OKRs across teams with automated progress rollups and weekly check-in reminders."

**Category:** Select the most specific category that matches the template's function (e.g., Project Management, Marketing, Engineering, Personal Productivity).

**Tags:** Add 3-5 tags matching search terms your ICP would use.

**Cover image:** 1200x630px PNG showing the template in use (not a blank state). Use a screenshot with sample data populated.

**Preview images:** 3-5 screenshots showing: (1) the main view, (2) a detail/form view, (3) a dashboard or summary view.

### 3. Set pricing

For lead-magnet use: set price to **Free** ($0). The goal is downloads and CTA clicks, not template revenue.

Notion takes 10% + $0.40 per paid transaction. For free templates, there are no fees.

### 4. Add UTM tracking to all outbound links

Every link inside the template that points to your product should include:
```
?utm_source=notion&utm_medium=marketplace&utm_campaign=template-{template-slug}
```

### 5. Submit for review

Click "Submit for review" in the marketplace dashboard. Notion reviews templates for quality, completeness, and policy compliance. Typical review time: 3-7 business days.

### 6. Verify publication

After approval, verify:
- Template appears in marketplace search for your target keywords
- All outbound links have correct UTM parameters
- Cover image and screenshots render correctly
- Template can be duplicated by a new user without errors

## Error Handling

- **Review rejected:** Check Notion's rejection email for specific feedback. Common issues: incomplete template, broken linked databases, misleading description, or policy violations (no external redirects in the template body itself -- CTAs must be clearly labeled).
- **Template not appearing in search:** Ensure your title and description contain the target keywords. Re-check category and tag selections. It may take 24-48 hours to be indexed after approval.
- **Broken links after duplication:** Any relational database links that reference pages outside the template tree will break when a user duplicates. Restructure to be self-contained.

## Pricing

- Notion Marketplace creator account: Free
- Free template listings: No fees
- Paid template listings: 10% + $0.40 per transaction; additional 1% FX fee for non-US creators
- Creator payout: Biweekly on Thursdays, minimum $20 balance
