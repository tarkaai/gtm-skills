---
name: posthog-project-setup
description: Set up a PostHog project with proper configuration for GTM tracking
tool: PostHog
difficulty: Setup
---

# Set Up PostHog for GTM Tracking

## Prerequisites
- PostHog account (cloud or self-hosted)
- Access to your website or application codebase

## Steps

1. **Create a project.** In PostHog, create a new project named after your product. If you have separate staging and production environments, create one project per environment. Copy the project API key from Settings > Project > API Key.

2. **Install the SDK.** Add PostHog to your application. For web: install `posthog-js` via npm and initialize with your API key and instance URL. For backend: install the Python or Node SDK. Place initialization code at your app's entry point so it loads on every page.

3. **Configure autocapture.** PostHog autocaptures clicks, page views, and form submissions by default. Review autocapture settings and disable any events you do not need (reduces noise). Keep page views and form submissions enabled as they power your funnel analysis.

4. **Set up user identification.** Call `posthog.identify(userId)` after login with a stable user ID (not email). Pass user properties: plan, signup_date, company, role. This links anonymous pre-signup activity to the identified user, giving you full-journey visibility.

5. **Configure group analytics.** If you sell to companies, set up group analytics: `posthog.group('company', companyId, { name, plan, employee_count })`. This lets you analyze behavior at the account level, not just the individual level.

6. **Verify data flow.** After deploying, visit your site and check PostHog's Live Events tab. You should see page views and identify calls appearing in real-time. Verify user properties are attached correctly by clicking into an event and inspecting the properties panel.
