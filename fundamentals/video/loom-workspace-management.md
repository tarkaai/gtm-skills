---
name: loom-workspace-management
description: Organize, tag, and manage a Loom video library at scale via the Loom API for structured tutorial collections
tool: Loom
product: Loom
difficulty: Config
---

# Manage Loom Video Library via API

Manage a structured video tutorial library in Loom using the API. Create folders, tag videos by topic and persona, and maintain an organized catalog that other drills can query programmatically.

## Prerequisites

- Loom Business plan (API access required)
- Loom API key generated from Workspace Settings > Developer
- Base URL: `https://api.loom.com/v1`

## Steps

### 1. Authenticate with the Loom API

All requests require an API key in the Authorization header:

```
Authorization: Bearer loom_api_key_xxxxxxxx
```

Test authentication:
```
GET /v1/me
```
Returns workspace name, user ID, and plan details. If 401, regenerate the API key.

### 2. Create a folder structure for tutorials

Organize videos into folders that map to your product's feature areas:

```
POST /v1/folders
Content-Type: application/json

{
  "name": "Tutorials - Getting Started",
  "description": "First-session tutorials for new users"
}
```

Recommended folder structure:
- `Tutorials - Getting Started` (signup to first value)
- `Tutorials - Core Workflows` (primary use cases)
- `Tutorials - Advanced Features` (power user capabilities)
- `Tutorials - Integrations` (connecting third-party tools)
- `Tutorials - Troubleshooting` (common issues and fixes)

### 3. List and organize existing videos

Retrieve all workspace videos:
```
GET /v1/videos?limit=100&offset=0
```

Returns: `id`, `title`, `created_at`, `duration`, `view_count`, `folder_id`.

Move videos into the correct folder:
```
PATCH /v1/videos/{video-id}
Content-Type: application/json

{
  "folder_id": "folder-id-here",
  "title": "[Tutorial] How to create your first project",
  "description": "2-minute walkthrough of project creation for new users. Persona: all."
}
```

### 4. Apply a naming convention

Standardize video titles for programmatic access:

```
[Tutorial] {Action verb} {feature/workflow} - {persona if targeted}
```

Examples:
- `[Tutorial] Create your first project`
- `[Tutorial] Import data from CSV - Data Analyst`
- `[Tutorial] Set up Slack integration - Admin`
- `[Tutorial] Build a custom report - Power User`

The `[Tutorial]` prefix lets you filter tutorial videos from internal recordings, demos, and other content.

### 5. Retrieve video embed data

For each tutorial, get the embed URL for in-app or email use:
```
GET /v1/videos/{video-id}
```

Returns `share_url` (for linking) and `embed_url` (for iframe embedding). The GIF thumbnail URL follows the pattern:
```
https://cdn.loom.com/sessions/thumbnails/{video-id}-with-play.gif
```

### 6. Bulk-query video analytics

For library-wide performance reporting:
```
GET /v1/videos?folder_id={folder-id}&limit=100
```

For each video in the response, check `view_count` and `average_watch_percentage`. Videos with <20% average watch percentage need hooks rewritten. Videos with 0 views in 30 days should be archived or promoted.

## Error Handling

- `404` on video endpoints: video was deleted or ID is wrong. Remove from your catalog.
- `429` rate limit: Loom API allows 100 requests/minute. Add 1-second delays between bulk operations.
- `403` on folder operations: user lacks workspace admin role. Escalate permissions.
