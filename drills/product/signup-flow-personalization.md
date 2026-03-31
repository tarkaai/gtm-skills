---
name: signup-flow-personalization
description: Personalize the signup experience by traffic source, device, and user segment using feature flags and dynamic content
category: Product
tools:
  - PostHog
  - Intercom
  - n8n
  - Loops
fundamentals:
  - posthog-feature-flags
  - posthog-cohorts
  - posthog-experiments
  - posthog-custom-events
  - intercom-bots
  - loops-audience
  - n8n-workflow-basics
  - n8n-scheduling
---

# Signup Flow Personalization

This drill creates segment-specific signup experiences that adapt based on traffic source, device, referral context, and user behavior. Instead of one signup flow for everyone, it delivers the right flow to the right visitor — maximizing conversion across all segments simultaneously.

## Input

- Signup funnel with baseline metrics per segment (from `signup-funnel-audit` and `signup-friction-reduction`)
- PostHog feature flags and experiments configured
- At least 500 signups/month across identifiable segments
- Intercom installed on signup pages

## Steps

### 1. Identify high-value segments

Using `posthog-cohorts`, analyze signup conversion rates across these dimensions:

- **Traffic source**: organic search, paid ads, referral, direct, social
- **Device**: mobile, desktop, tablet
- **Referrer context**: pricing page visitor, blog reader, comparison page visitor, homepage
- **Geography**: top 5 countries by traffic
- **Time of day**: business hours vs off-hours

Find segments where conversion rate diverges significantly from the overall average. Segments converting >30% below average are personalization targets.

### 2. Design segment-specific flows

For each underperforming segment, design a tailored signup experience:

**Mobile visitors** (if mobile CVR < 60% of desktop CVR):
- Single-column layout, larger inputs (min 44px tap targets)
- OAuth buttons prominently displayed (most mobile users prefer OAuth)
- Reduce form to email-only, collect rest post-signup
- Auto-focus first field, use `inputmode` attributes for correct mobile keyboards

**Paid ad visitors** (if paid CVR < organic CVR):
- Match ad copy to signup page headline (message consistency)
- Include the specific value prop from the ad above the form
- Add "no credit card required" if applicable
- Reduce form fields to minimum (name + email)

**Blog/content visitors** (if content CVR < direct CVR):
- Show a different CTA: "Try it free" instead of "Sign up"
- Include a brief product demo or screenshot above the form
- Add social proof specific to the content topic they read
- Consider a softer entry: free tool or template before full signup

**Referral visitors** (visitors from partner links or word-of-mouth):
- Pre-fill referral source in hidden field
- Show "Referred by [source]" trust badge
- Offer an incentive if a referral program exists

### 3. Implement with feature flags

Using `posthog-feature-flags`, create multivariate flags that route visitors to the right experience:

```
POST /api/projects/<id>/feature_flags/
{
  "key": "signup-flow-variant",
  "name": "Signup Flow Personalization",
  "filters": {
    "groups": [
      {
        "properties": [{"key": "$device_type", "value": "Mobile"}],
        "variant": "mobile-optimized"
      },
      {
        "properties": [{"key": "utm_source", "value": ["google", "facebook", "linkedin"], "operator": "exact"}],
        "variant": "paid-landing"
      },
      {
        "properties": [{"key": "$referrer", "value": "/blog/", "operator": "icontains"}],
        "variant": "content-reader"
      }
    ],
    "multivariate": {
      "variants": [
        {"key": "mobile-optimized", "rollout_percentage": 100},
        {"key": "paid-landing", "rollout_percentage": 100},
        {"key": "content-reader", "rollout_percentage": 100},
        {"key": "default", "rollout_percentage": 100}
      ]
    }
  },
  "active": true
}
```

### 4. Track per-segment performance

Using `posthog-custom-events`, enrich signup events with the variant:

```javascript
const variant = posthog.getFeatureFlag('signup-flow-variant');
posthog.capture('signup_completed', {
  signup_flow_variant: variant,
  device_type: /Mobi/.test(navigator.userAgent) ? 'mobile' : 'desktop',
  utm_source: new URLSearchParams(window.location.search).get('utm_source')
});
```

Build per-variant funnels in PostHog using `posthog-experiments`:

```
POST /api/projects/<id>/experiments/
{
  "name": "Signup Personalization - Mobile",
  "feature_flag_key": "signup-flow-variant",
  "filters": {
    "events": [
      {"id": "signup_page_viewed"},
      {"id": "signup_form_submitted"},
      {"id": "signup_completed"}
    ]
  },
  "parameters": {
    "minimum_detectable_effect": 0.05
  }
}
```

### 5. Build segment nurture for partial signups

Using `loops-audience`, create segments of users who started but did not complete signup, broken down by variant:

- Mobile abandoned: send email with deep link back to a mobile-optimized signup page
- Paid abandoned: retarget with a simplified offer (reduce friction even further)
- Content abandoned: send the content piece they were reading plus a soft signup CTA

Using `n8n-workflow-basics` and `n8n-scheduling`, build a daily workflow that:
1. Queries PostHog for `signup_form_focused` events without a matching `signup_completed` in the last 24 hours
2. If the user provided an email (partial form fill), sends them to the appropriate Loops nurture segment
3. Logs recovery attempts in Attio

### 6. Scale winning variants

After each variant runs for 14+ days with 200+ conversions:

1. Compare per-segment CVR against the default flow
2. If the personalized variant wins: make it permanent for that segment
3. If it loses: revert and investigate — the segment hypothesis may be wrong
4. For segments with no significant difference: keep the default (simpler to maintain)

Using `intercom-bots`, add segment-specific help bots:
- Mobile: "Tap here to sign up with Google — it's faster on mobile"
- Paid: "Questions about [product]? Chat with us before signing up"

## Output

- Segment analysis showing which visitor types underperform
- 2-4 personalized signup variants deployed via feature flags
- Per-variant tracking and experiment configuration
- Partial-signup nurture sequences per segment
- Scaling recommendations: which variants to keep, which to retire

## Triggers

Run during Scalable level. Re-evaluate segments quarterly as traffic mix and product positioning change.
