---
name: template-catalog-api
description: CRUD operations for a template catalog that lets users browse and install pre-built configurations
tool: Product
product: Product API
difficulty: Config
---

# Template Catalog API

Build and manage a template catalog — a browseable collection of pre-built configurations, workflows, or content that users can install into their accounts with one action.

## When to Use

When your product supports templates, presets, or starter configurations that help users skip blank-slate friction. Templates differ from sample data: sample data shows what a populated account looks like, while templates are reusable starting points users intentionally choose.

## Instructions

### 1. Define the template data model

Each template needs:

```json
{
  "id": "template_crm_pipeline",
  "name": "B2B Sales Pipeline",
  "description": "A 5-stage pipeline for B2B SaaS sales: Lead → Qualified → Demo → Proposal → Closed.",
  "category": "sales",
  "tags": ["b2b", "saas", "pipeline"],
  "preview_image_url": "https://assets.example.com/templates/crm-pipeline.png",
  "popularity": 847,
  "created_at": "2026-01-10T00:00:00Z",
  "updated_at": "2026-03-15T00:00:00Z",
  "author": "product_team",
  "install_count": 847,
  "estimated_setup_time": "2 minutes",
  "payload": {
    "type": "pipeline",
    "stages": ["Lead", "Qualified", "Demo", "Proposal", "Closed"],
    "default_fields": ["company_name", "deal_value", "close_date", "owner"]
  }
}
```

### 2. Implement the catalog API

**List templates:**
```
GET /api/templates?category={category}&sort={popularity|newest}&page={page}
Response: { "templates": [...], "total": 24, "page": 1, "per_page": 12 }
```

**Get template detail:**
```
GET /api/templates/{template_id}
Response: { "template": { ... full template with payload ... } }
```

**Install template:**
```
POST /api/templates/{template_id}/install
Headers: Authorization: Bearer {user_token}
Body: { "account_id": "{account_id}", "customize": { "rename": "My Sales Pipeline" } }
Response: { "installed": true, "created_objects": ["pipeline_abc123"], "redirect_url": "/pipelines/abc123" }
```

The install endpoint should:
1. Read the template payload
2. Create the corresponding objects in the user's account
3. Tag installed objects with `_from_template: "{template_id}"` metadata
4. Increment the template's `install_count`
5. Return a redirect URL so the user lands directly in their new template

**Track template installs:**
```
POST /api/templates/{template_id}/install → also fires:
posthog.capture('template_installed', {
  template_id: templateId,
  template_name: 'B2B Sales Pipeline',
  category: 'sales',
  account_id: accountId,
  source: 'template_gallery'  // or 'onboarding_flow', 'empty_state'
});
```

### 3. Build the catalog frontend surface

Templates should appear in three product locations:

| Surface | When Shown | UX Pattern |
|---------|-----------|------------|
| **Template gallery page** | User navigates to /templates or /explore | Grid layout with category filters, search, and sort by popularity |
| **Empty state** | User has zero objects of a type (no projects, no pipelines) | Inline template suggestions: "Start with a template" with 3-4 top picks |
| **Onboarding flow** | During first-time setup | Step in the onboarding wizard: "Choose a template to get started" |

For each surface, track impressions:
```javascript
posthog.capture('template_gallery_viewed', {
  surface: 'template_gallery',  // or 'empty_state', 'onboarding_flow'
  templates_shown: ['template_crm_pipeline', 'template_marketing_board'],
  account_id: accountId
});
```

### 4. Implement template preview

Before installing, users should see what they will get. Options:
- **Screenshot/image**: Static preview image stored with the template
- **Interactive preview**: Read-only rendered version of the template in a modal
- **Description + object list**: Text describing what gets created ("Creates: 1 pipeline with 5 stages, 4 custom fields, 2 automation rules")

Track preview engagement:
```javascript
posthog.capture('template_previewed', {
  template_id: templateId,
  surface: 'template_gallery',
  time_spent_ms: previewDurationMs
});
```

### 5. Manage the catalog

Templates need ongoing maintenance:
- **Retire stale templates**: If a template has <10 installs after 90 days, archive it
- **Update templates**: When the product adds new features, update templates to showcase them
- **Track uninstalls**: If users frequently delete template-created objects within 24 hours, the template is misleading — investigate and fix

## Error Handling

- **Install conflict**: If the template creates objects that conflict with existing user data (e.g., duplicate pipeline names), append a suffix or prompt the user to rename.
- **Payload version mismatch**: If the template payload references features or fields that have been removed, skip those elements and log a warning. Never block the install entirely.
- **Missing assets**: If preview images fail to load, fall back to a generic category icon.

## Output

A functional template catalog with list, detail, preview, and install endpoints, integrated into three product surfaces, with PostHog tracking at every interaction point.
