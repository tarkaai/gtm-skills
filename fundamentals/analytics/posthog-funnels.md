---
name: posthog-funnels
description: Create conversion funnels in PostHog to find GTM bottlenecks
tool: PostHog
difficulty: Intermediate
---

# Build Conversion Funnels in PostHog

## Prerequisites
- PostHog project with events tracked at each funnel stage
- Clear definition of the conversion path you want to analyze

## Steps

1. **Define your funnel stages.** Map the user journey as a sequence of events. Example signup funnel: `page_viewed` (pricing) > `signup_started` > `signup_completed` > `onboarding_step_1` > `onboarding_complete`. Each step must be a distinct, trackable event.

2. **Create a funnel insight via API.** Use the PostHog API or MCP to create a funnel:
   ```
   POST /api/projects/<id>/insights/
   {
     "name": "Signup Funnel",
     "filters": {
       "insight": "FUNNELS",
       "events": [
         {"id": "page_viewed", "properties": [{"key": "$current_url", "value": "/pricing"}]},
         {"id": "signup_started"},
         {"id": "signup_completed"}
       ],
       "funnel_window_days": 7
     }
   }
   ```
   Set the conversion window: 7 days for signup flows, 30 days for sales processes.

3. **Analyze drop-off points.** PostHog returns conversion rates between each step. Identify the biggest drop-off. If 80% start signup but only 40% complete it, the signup form is the bottleneck. Focus optimization effort on the step with the largest absolute drop.

4. **Break down by properties.** Add breakdown parameters to slice the funnel by traffic source, device, plan type, or geography:
   ```
   "breakdown": "utm_source", "breakdown_type": "event"
   ```
   This reveals which segments convert best and which need attention.

5. **Compare time periods.** Use HogQL to compare funnel performance across periods:
   ```sql
   SELECT step, count() FROM funnel WHERE timestamp > now() - interval 7 day GROUP BY step
   ```
   Look for improving or declining conversion rates. A declining step indicates something changed (new bug, UX change, market shift).

6. **Set up funnel alerts.** Use n8n to build a scheduled workflow that queries funnel conversion rates via the PostHog API and triggers a Slack notification when a stage's conversion rate drops below your threshold. See `n8n-crm-integration` for the n8n-to-PostHog pattern.
