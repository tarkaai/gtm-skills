---
name: posthog-project-setup
description: Set up a PostHog project with proper configuration for GTM tracking
tool: PostHog
difficulty: Setup
---

# Set Up PostHog for GTM Tracking

## Prerequisites
- PostHog account (cloud or self-hosted)
- Access to your application codebase

## Steps

1. **Create a project.** Use the PostHog API or dashboard to create a new project named after your product. For separate staging/production environments, create one project per environment. Retrieve the project API key via `GET /api/organizations/<org-id>/projects/` or from project settings.

2. **Install the SDK.** Add PostHog to your application:
   - **Web:** `npm install posthog-js` and initialize at your app entry point:
     ```javascript
     posthog.init('<project-api-key>', { api_host: 'https://app.posthog.com' })
     ```
   - **Node:** `npm install posthog-node` and initialize with project API key.
   - **Python:** `pip install posthog` and set `posthog.project_api_key = '<key>'`.

3. **Configure autocapture.** PostHog autocaptures pageviews, form submissions, and interactions by default. To reduce noise, pass config options during init:
   ```javascript
   posthog.init('<key>', { autocapture: { dom_event_allowlist: ['submit'] } })
   ```
   Keep pageviews and form submissions enabled -- they power funnel analysis.

4. **Set up user identification.** Call `posthog.identify(userId)` after login with a stable user ID (not email). Pass user properties:
   ```javascript
   posthog.identify(userId, { plan: 'pro', signup_date: '2025-01-15', company: 'Acme', role: 'founder' })
   ```
   This links anonymous pre-signup activity to the identified user for full-journey visibility.

5. **Configure group analytics.** For B2B account-level analysis:
   ```javascript
   posthog.group('company', companyId, { name: 'Acme', plan: 'enterprise', employee_count: 150 })
   ```
   This enables analyzing behavior at the account level, not just per-user.

6. **Verify data flow.** Use the PostHog MCP `query_events` operation or the API (`GET /api/projects/<id>/events/?limit=10`) to confirm events are arriving. Verify pageviews and identify calls appear with correct user properties in the `properties` object.
