---
name: signup-funnel-audit
description: Instrument and audit a self-serve signup funnel to identify conversion drop-offs, friction points, and baseline metrics
category: Onboarding
tools:
  - PostHog
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - posthog-session-recording
  - posthog-user-path-analysis
---

# Signup Funnel Audit

This drill produces a complete audit of a self-serve signup funnel: every step instrumented, every drop-off quantified, and every friction point identified. The output is a prioritized list of conversion bottlenecks with baseline metrics.

## Input

- The signup flow URL(s): landing page, signup form, email verification, initial setup
- PostHog project with SDK installed on all signup pages
- At least 100 signups in the last 30 days (or best available data)

## Steps

### 1. Define the signup funnel events

Using `posthog-custom-events`, ensure every step in the signup flow fires a distinct event:

| Event | Trigger | Key Properties |
|-------|---------|----------------|
| `signup_page_viewed` | User lands on the signup page | `referrer`, `utm_source`, `utm_medium`, `utm_campaign`, `device_type` |
| `signup_form_focused` | User focuses the first form field | `field_name`, `device_type` |
| `signup_form_field_completed` | User completes a form field (on blur with value) | `field_name`, `field_position`, `device_type` |
| `signup_form_field_error` | Validation error shown on a field | `field_name`, `error_type` (e.g., invalid_email, password_too_short) |
| `signup_form_submitted` | User clicks the submit button | `field_count_filled`, `time_on_form_seconds`, `device_type` |
| `signup_form_error` | Server-side error after submission | `error_type` (e.g., email_taken, rate_limited, server_error) |
| `signup_completed` | Account successfully created | `signup_method` (email, google, github), `time_to_complete_seconds`, `device_type` |
| `email_verification_sent` | Verification email dispatched | `signup_method` |
| `email_verification_completed` | User clicks verification link | `time_to_verify_seconds` |
| `initial_setup_started` | User begins post-signup setup | `device_type` |
| `initial_setup_completed` | User finishes post-signup setup | `steps_completed`, `time_to_complete_seconds` |

Implement field-level tracking with this pattern:

```javascript
document.querySelectorAll('form input, form select').forEach(field => {
  field.addEventListener('blur', function() {
    if (this.value) {
      posthog.capture('signup_form_field_completed', {
        field_name: this.name,
        field_position: Array.from(this.form.elements).indexOf(this),
        device_type: /Mobi/.test(navigator.userAgent) ? 'mobile' : 'desktop'
      });
    }
  });
});
```

### 2. Build the signup funnel in PostHog

Using `posthog-funnels`, create the primary signup funnel:

```
POST /api/projects/<id>/insights/
{
  "name": "Signup Funnel - Full",
  "filters": {
    "insight": "FUNNELS",
    "events": [
      {"id": "signup_page_viewed"},
      {"id": "signup_form_focused"},
      {"id": "signup_form_submitted"},
      {"id": "signup_completed"},
      {"id": "email_verification_completed"},
      {"id": "initial_setup_completed"}
    ],
    "funnel_window_days": 7
  }
}
```

Break down by:
- `utm_source` — which traffic sources convert best
- `device_type` — mobile vs desktop conversion
- `signup_method` — email vs OAuth completion rates

### 3. Identify the primary bottleneck

Pull the funnel data and find the step with the largest absolute drop-off. Rank all steps by:

1. **Absolute drop-off**: how many users are lost at this step
2. **Relative drop-off**: what percentage of users reaching this step fail to proceed

The step with the highest absolute drop-off is the primary bottleneck. This is where optimization effort should focus first.

### 4. Diagnose friction with session recordings

Using `posthog-session-recording`, pull recordings of users who dropped off at the primary bottleneck:

```
GET /api/projects/<id>/session_recordings/?events=[{"id":"signup_form_focused"}]&date_from=-14d
```

Filter for sessions where `signup_form_focused` fired but `signup_form_submitted` did not. Watch 15-20 recordings and categorize the friction:

- **Form confusion**: user fills fields in wrong order, re-enters data, or hovers over labels
- **Validation blocking**: user hits errors repeatedly on a specific field
- **Distraction**: user scrolls away from form, opens other tabs, or leaves
- **Mobile friction**: form does not render properly, keyboard covers fields, or tapping is imprecise
- **Trust concern**: user pauses at password or credit card fields, reads privacy policy, then leaves

### 5. Analyze signup paths

Using `posthog-user-path-analysis`, examine the paths users take before reaching the signup page and the paths within the signup flow:

- Which pages do converting users visit before signing up?
- Do users who visit the pricing page first convert at a higher rate?
- What is the median number of page views before signup?
- Do users who sign up via OAuth complete at a higher rate than email signups?

### 6. Establish baseline metrics

Record the following baseline metrics with dates:

| Metric | Definition | Baseline Value | Date |
|--------|-----------|---------------|------|
| Signup page CVR | `signup_completed / signup_page_viewed` | | |
| Form start rate | `signup_form_focused / signup_page_viewed` | | |
| Form completion rate | `signup_form_submitted / signup_form_focused` | | |
| Form success rate | `signup_completed / signup_form_submitted` | | |
| Email verification rate | `email_verification_completed / signup_completed` | | |
| Setup completion rate | `initial_setup_completed / signup_completed` | | |
| Median time to complete signup | Time from `signup_page_viewed` to `signup_completed` | | |
| Mobile CVR vs Desktop CVR | Signup CVR broken down by device_type | | |

Store baselines in Attio as a campaign record note.

## Output

- Full signup funnel instrumented with field-level tracking
- PostHog funnel showing conversion rates at each step
- Prioritized bottleneck list (ordered by absolute drop-off)
- Session recording playlist of drop-off behavior at the primary bottleneck
- Baseline metric table with values and dates
- Friction diagnosis categorization from session recording review

## Triggers

Run once during Smoke test. Re-run whenever the signup flow changes (new fields, new design, new OAuth providers).
