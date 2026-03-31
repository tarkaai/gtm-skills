---
name: signup-friction-reduction
description: Systematically remove friction from a signup funnel by reducing fields, adding OAuth, fixing validation, and optimizing mobile
category: Onboarding
tools:
  - PostHog
  - Intercom
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-feature-flags
  - posthog-funnels
  - intercom-bots
  - n8n-triggers
  - n8n-workflow-basics
---

# Signup Friction Reduction

This drill takes the bottleneck identified by `signup-funnel-audit` and systematically removes friction. It produces a set of targeted changes — each wired with tracking — that reduce drop-off at the primary conversion bottleneck.

## Input

- Completed `signup-funnel-audit` output: baseline metrics, primary bottleneck, friction diagnosis
- PostHog project with signup events flowing
- Access to modify the signup form HTML/JS or the signup backend

## Steps

### 1. Prioritize friction fixes

Using the friction diagnosis from `signup-funnel-audit`, rank fixes by expected impact and implementation effort:

| Friction Type | Fix | Expected Impact | Effort |
|--------------|-----|----------------|--------|
| Too many fields | Remove non-essential fields, defer to post-signup | High | Low |
| No OAuth | Add Google/GitHub OAuth buttons above the form | High | Medium |
| Validation blocking | Switch to inline real-time validation (on blur, not on submit) | Medium | Low |
| Mobile friction | Make form full-width, increase tap targets, auto-focus first field | Medium | Low |
| Trust concern | Add trust signals next to form (customer count, security badge, "no credit card") | Medium | Low |
| Password complexity | Replace with magic link or passkey, or show password strength meter | Medium | Medium |
| Email verification blocking | Defer verification to after first value moment | High | Medium |

Select the top 2-3 fixes based on the highest expected impact with lowest effort.

### 2. Implement tracking for each change

Using `posthog-custom-events`, add events that measure each specific fix:

For field reduction:
```javascript
posthog.capture('signup_form_variant', {
  variant: 'reduced_fields',
  field_count: document.querySelectorAll('form input:not([type=hidden])').length
});
```

For OAuth addition:
```javascript
document.querySelector('.oauth-google').addEventListener('click', () => {
  posthog.capture('oauth_signup_started', { provider: 'google' });
});
document.querySelector('.oauth-github').addEventListener('click', () => {
  posthog.capture('oauth_signup_started', { provider: 'github' });
});
```

### 3. Deploy changes behind feature flags

Using `posthog-feature-flags`, gate each change behind a feature flag so you can roll out incrementally:

```
POST /api/projects/<id>/feature_flags/
{
  "key": "signup-reduced-fields",
  "name": "Signup: Reduced Fields",
  "filters": { "groups": [{"rollout_percentage": 50}] },
  "active": true
}
```

In the signup page code:
```javascript
if (posthog.isFeatureEnabled('signup-reduced-fields')) {
  // Hide non-essential fields (company name, phone, etc.)
  document.querySelectorAll('.optional-field').forEach(f => f.style.display = 'none');
}
```

### 4. Build automated monitoring

Using `n8n-triggers` and `n8n-workflow-basics`, create a workflow that:

1. Runs daily via cron
2. Queries PostHog for signup funnel metrics for each feature flag variant
3. Compares conversion rates: control vs treatment
4. If treatment conversion rate is >10% higher with >100 samples per variant, sends a Slack alert recommending full rollout
5. If treatment conversion rate is >10% lower, sends an alert recommending rollback

### 5. Set up Intercom help triggers

Using `intercom-bots`, configure targeted help for users who show friction signals:

- If a user has `signup_form_field_error` events >= 3, trigger a bot message: "Having trouble signing up? I can help — or try signing up with Google instead."
- If a user has been on the signup page for > 2 minutes without submitting, show a non-intrusive tooltip: "Need help? [Chat with us]"

### 6. Validate against baseline

After running each change for at least 7 days with 200+ users per variant:

1. Pull the signup funnel for each variant from PostHog
2. Compare to the baseline from `signup-funnel-audit`
3. Calculate the lift: `(new_CVR - baseline_CVR) / baseline_CVR * 100`
4. If positive and statistically significant: roll out to 100%
5. If negative: revert and try the next fix on the priority list

## Output

- 2-3 friction fixes deployed behind feature flags with per-variant tracking
- Automated daily monitoring comparing variant conversion rates
- Intercom help triggers for users showing friction
- Validation report showing lift vs baseline for each change
- Recommendation: which changes to keep, which to revert

## Triggers

Run once during Baseline setup. Re-run when new friction sources are identified by ongoing monitoring.
