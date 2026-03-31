---
name: template-gallery-setup
description: Build a browseable template gallery with install-to-account functionality and engagement tracking
category: Product
tools:
  - PostHog
  - Intercom
  - n8n
fundamentals:
  - template-catalog-api
  - posthog-custom-events
  - posthog-funnels
  - intercom-in-app-messages
  - n8n-workflow-basics
---

# Template Gallery Setup

This drill builds a template gallery — a curated collection of pre-built configurations users can browse and install into their accounts. Templates reduce blank-slate friction by giving users a structured starting point they chose, rather than a generic empty state.

## Input

- Product with configurable objects (projects, pipelines, boards, workflows, dashboards, forms, etc.)
- At least 5 template ideas based on common use cases from your ICP
- PostHog installed with user identification
- Intercom installed for in-app guidance

## Steps

### 1. Audit your product's most common configurations

Before building templates, understand what successful users actually build:

1. Query your product database for the most-created object configurations across active accounts
2. Using `posthog-custom-events`, pull the top 10 object types by creation frequency
3. Cluster configurations by similarity — if 40% of users create a "Sales Pipeline" with 4-6 stages, that is a template candidate
4. Interview 5-10 power users or review support tickets asking "how do I set up X" — these are template opportunities

Target: 8-15 templates organized into 3-5 categories.

### 2. Design the template catalog

Run the `template-catalog-api` fundamental to build:
- The template data model with metadata, payload, and preview assets
- List/detail/install API endpoints
- Install tracking events

For each template, create:
1. **Name and description**: Action-oriented. "B2B Sales Pipeline" not "Pipeline Template #1"
2. **Category**: Group by use case or department (Sales, Marketing, Engineering, HR, Operations)
3. **Preview**: Screenshot or rendered preview showing what the installed template looks like
4. **Payload**: The actual configuration that gets created on install
5. **Setup time estimate**: How long until the user has a working version (most should be "Instant" or "Under 2 minutes")

### 3. Build the gallery UI in three surfaces

Templates should appear where users need them most:

**Surface 1 — Dedicated gallery page (/templates or /explore)**

Grid layout with:
- Category sidebar or filter tabs
- Search by name and tags
- Sort by popularity (install count) or newest
- Template cards showing: name, description, category, install count, preview thumbnail
- Click-through to detail page with full preview and "Use this template" CTA

Track with PostHog:
```javascript
posthog.capture('template_gallery_viewed', { surface: 'gallery_page', category_filter: selectedCategory });
posthog.capture('template_card_clicked', { template_id: id, surface: 'gallery_page', position: index });
```

**Surface 2 — Empty states**

When a user has zero objects of a given type, replace the empty state with:
- "Get started with a template" heading
- 3 most popular templates for that object type as cards
- "Browse all templates" link to the gallery page
- "Start from scratch" secondary option

Track:
```javascript
posthog.capture('empty_state_template_shown', { object_type: 'project', templates_shown: [id1, id2, id3] });
```

**Surface 3 — Onboarding flow**

Add a template selection step to your onboarding wizard:
- "What are you building?" with category options
- Show 2-3 top templates matching their selection
- "Use this template" installs and redirects to the populated object
- "I'll start from scratch" skips the step

Using `intercom-in-app-messages`, create a follow-up message for users who skipped templates during onboarding: "Did you know you can start with a template? Browse templates →" Show 48 hours after signup if the user has not created any objects.

### 4. Instrument the template funnel

Using `posthog-funnels`, build a funnel tracking the full template journey:

```
template_gallery_viewed → template_card_clicked → template_previewed → template_installed → template_object_edited
```

The critical conversion is `template_installed → template_object_edited` — this proves the user did not just install and abandon. Break the funnel down by:
- Template ID (which templates convert best)
- Surface (gallery vs. empty state vs. onboarding)
- User cohort (new vs. returning)

### 5. Build the template contribution pipeline

Templates should grow over time. Set up a pipeline for new templates:

1. Using `n8n-workflow-basics`, create a workflow that monitors for templates with high install counts but low edit rates (users install but do not customize — the template may need improvement)
2. Track template "forks" — when a user installs a template and then significantly modifies it, the modification pattern may be a better template
3. Build an internal submission form: team members can propose new templates by specifying use case, target persona, and payload

### 6. Set up template health monitoring

Using `posthog-custom-events`, track template health metrics:
- **Install-to-edit rate**: What percentage of users who install a template go on to edit it within 7 days? Below 30% means the template is not resonating.
- **Install-to-delete rate**: If users install and then delete within 24 hours, the template preview is misleading.
- **Time-to-first-edit**: How quickly after install does the user start customizing? Faster is better.

Build an n8n workflow that runs weekly, queries these metrics per template, and flags unhealthy templates (install-to-edit <30% or install-to-delete >20%).

## Output

- Template catalog with 8-15 templates across 3-5 categories
- Gallery page, empty-state integration, and onboarding step
- Full PostHog funnel tracking from gallery view to template edit
- Template health monitoring via n8n
- Contribution pipeline for ongoing template creation

## Triggers

Run once during play setup. Re-run when:
- Adding new product features that need templates
- Template health metrics flag underperforming templates
- New ICP segments need dedicated templates
