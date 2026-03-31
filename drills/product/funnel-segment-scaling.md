---
name: funnel-segment-scaling
description: Scale funnel optimizations across personas, cohorts, and traffic sources by building per-segment variants and automated routing
category: Product
tools:
  - PostHog
  - Intercom
  - n8n
  - Loops
fundamentals:
  - posthog-cohorts
  - posthog-feature-flags
  - posthog-funnels
  - posthog-custom-events
  - intercom-in-app-messages
  - loops-sequences
  - n8n-triggers
  - n8n-workflow-basics
---

# Funnel Segment Scaling

This drill takes a funnel optimization that works for the general population and scales it across multiple user segments. Each segment gets a tailored variant based on its specific friction patterns, traffic source expectations, and behavioral profile. The output is a system that routes users into the right funnel variant automatically based on their properties.

## Input

- A validated funnel optimization from `signup-friction-reduction` or `activation-optimization` (the "general winner")
- PostHog funnel data broken down by at least 3 dimensions (device, traffic source, user type)
- At least 500 users per segment per month (enough for per-segment experiments)
- Intercom and Loops configured for in-app and email engagement

## Steps

### 1. Identify high-leverage segments

Using the `posthog-cohorts` fundamental, create cohorts for each major user segment. Then use `posthog-funnels` to calculate funnel conversion rates per cohort.

Priority segments to analyze:
- **By acquisition source:** organic, paid, referral, direct — different expectations and intent levels
- **By device:** mobile vs desktop — different UI capabilities and attention spans
- **By user type:** individual vs team admin, free vs paid trial, new vs returning
- **By geography:** different markets may have different friction patterns (payment methods, language, trust signals)

Rank segments by: `(average_conversion - segment_conversion) * segment_volume`. This identifies segments where the biggest absolute gains are available.

### 2. Build per-segment funnel variants

For each of the top 3 underperforming segments, design a tailored funnel variant.

Using `posthog-feature-flags`, create a multi-variant feature flag that routes users based on their properties:

```
POST /api/projects/<id>/feature_flags/
{
  "key": "funnel-segment-variant",
  "name": "Funnel: Segment-Specific Variants",
  "filters": {
    "groups": [
      {
        "properties": [{"key": "utm_source", "value": "paid"}],
        "variant": "paid-optimized"
      },
      {
        "properties": [{"key": "$device_type", "value": "Mobile"}],
        "variant": "mobile-optimized"
      },
      {
        "properties": [{"key": "user_type", "value": "team_admin"}],
        "variant": "team-optimized"
      }
    ],
    "payloads": {
      "paid-optimized": {"show_social_proof": true, "reduce_fields": true, "highlight_roi": true},
      "mobile-optimized": {"single_column": true, "sticky_cta": true, "oauth_first": true},
      "team-optimized": {"show_team_features": true, "skip_personal_setup": true}
    }
  }
}
```

### 3. Configure segment-specific messaging

For each segment variant, set up contextual support:

Using the `intercom-in-app-messages` fundamental, create targeted messages:
- Paid traffic users: "You came from [ad topic]. Here is exactly how to get started with [the thing the ad promised]."
- Mobile users: "Complete setup on mobile in 2 minutes, or we will email you a link to finish on desktop."
- Team admins: "Setting up for your team? Skip personal setup — go straight to workspace configuration."

Using the `loops-sequences` fundamental, create per-segment onboarding email sequences:
- Each segment gets a welcome email that matches their entry context
- Follow-up emails address the specific friction points diagnosed for that segment

### 4. Track per-segment funnel performance

Using `posthog-custom-events`, emit segment routing events:

```javascript
posthog.capture('funnel_segment_routed', {
  segment: '{segment_name}',
  variant: '{variant_key}',
  funnel_step: 'entry'
});
```

Using `posthog-funnels`, create per-segment funnels that track each variant's conversion independently. Build a comparison dashboard showing all segments side by side with trend lines.

### 5. Automate segment expansion

Using `n8n-triggers` and `n8n-workflow-basics`, create an n8n workflow that:

1. Runs weekly via cron
2. Queries PostHog for segment-level funnel metrics
3. For any segment where conversion is still >20% below the best-performing segment, flags it for deeper diagnosis
4. For segments where the variant outperforms the general funnel by >10%, logs the win and recommends the variant become the default for that segment
5. For any new segment that grows above 100 users/week (previously too small to optimize), triggers a diagnosis workflow

### 6. Build cross-segment insights

After running per-segment variants for 4+ weeks, analyze cross-segment learnings:

- Which optimizations work across multiple segments? (Candidates for the general funnel)
- Which optimizations only work for specific segments? (Keep as segment-specific)
- Are there segments that resist optimization? (May need entirely different approaches — product changes, pricing changes, or de-prioritization)

Log insights in Attio and feed the top-performing cross-segment optimizations back into the general funnel.

## Output

- Feature flag routing users into segment-specific funnel variants
- Per-segment Intercom messages and Loops email sequences
- Segment-level funnel dashboards with independent tracking
- Weekly automated monitoring of segment performance
- Cross-segment insight report identifying universal vs segment-specific wins

## Triggers

Run once during Scalable setup. The weekly n8n monitoring runs continuously. Re-run the full setup when new significant segments emerge (new traffic source, new user type, new market).
