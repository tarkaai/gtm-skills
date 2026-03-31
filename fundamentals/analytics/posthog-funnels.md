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

1. **Define your funnel stages.** Map the user journey as a sequence of events. Example signup funnel: "page_viewed (pricing)" > "signup_started" > "signup_completed" > "onboarding_step_1" > "onboarding_complete". Each step should be a distinct, trackable event.

2. **Create a funnel insight.** In PostHog, go to Insights > New > Funnel. Add your events in order. Set the conversion window (how long users have to complete the funnel -- typically 7 days for signup flows, 30 days for sales processes).

3. **Analyze drop-off points.** PostHog shows the conversion rate between each step. Identify the biggest drop-off. If 80% start signup but only 40% complete it, the signup form is your bottleneck. Focus optimization effort on the step with the largest absolute drop.

4. **Break down by properties.** Use PostHog's breakdown feature to slice the funnel by: traffic source (organic vs paid vs outbound), device (desktop vs mobile), plan type, or geography. This reveals which segments convert best and which need attention.

5. **Compare time periods.** Use the date range selector to compare this week vs last week, or this month vs previous month. Look for improving or declining conversion rates at each stage. A declining step indicates something changed (new bug, UX change, market shift).

6. **Set up funnel alerts.** If a stage's conversion rate drops below a threshold, you want to know immediately. Use PostHog's alerting or connect to n8n (see `fundamentals/automation/n8n-crm-integration`) to trigger a Slack notification when funnel performance degrades.
