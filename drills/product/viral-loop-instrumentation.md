---
name: viral-loop-instrumentation
description: Instrument the complete viral funnel in PostHog — from trigger action through share, landing, signup, and activation — with cohort and funnel analysis
category: Product
tools:
  - PostHog
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - posthog-cohorts
  - posthog-feature-flags
  - posthog-dashboards
  - n8n-triggers
  - n8n-workflow-basics
---

# Viral Loop Instrumentation

This drill sets up comprehensive PostHog tracking for a viral loop mechanic so every step of the viral funnel is measurable and attributable.

## Input

- Viral mechanic specification (output of `viral-mechanic-design` drill)
- PostHog project with SDK installed
- n8n instance for webhook processing

## Steps

### 1. Define the viral event taxonomy

Using `posthog-custom-events`, implement these events at each stage of the viral loop:

**Trigger stage** (user performs the viral action):
```javascript
posthog.capture('viral_trigger_action', {
  mechanic: 'invite_to_collaborate',  // or 'share_to_show', 'use_to_expose'
  trigger_type: 'workspace_created',   // the specific product action
  user_id: currentUser.id,
  referral_code: currentUser.referralCode
});
```

**Share stage** (product generates and user distributes the artifact):
```javascript
posthog.capture('viral_share_initiated', {
  mechanic: 'invite_to_collaborate',
  share_channel: 'email',         // email, link_copy, slack, twitter, linkedin
  recipients_count: 3,            // number of people invited/shared with
  referral_code: currentUser.referralCode,
  artifact_type: 'workspace_invite'  // invite, report_link, embed_widget
});
```

**Landing stage** (non-user arrives via the shared artifact):
```javascript
posthog.capture('viral_landing_viewed', {
  referral_code: urlParams.ref,
  referrer_id: urlParams.referrer,
  mechanic: urlParams.mechanic,
  artifact_type: urlParams.artifact,
  landing_variant: 'v1'
});
```

**Signup stage** (non-user creates an account):
```javascript
posthog.capture('viral_signup_completed', {
  referral_code: urlParams.ref,
  referrer_id: urlParams.referrer,
  mechanic: urlParams.mechanic,
  signup_method: 'email'  // email, google_oauth, sso
});
```

**Activation stage** (new user reaches the product's activation metric):
```javascript
posthog.capture('viral_referee_activated', {
  referral_code: originalReferralCode,
  referrer_id: originalReferrerId,
  mechanic: originalMechanic,
  days_to_activate: daysSinceSignup
});
```

**Loop-close stage** (new user performs their own viral trigger action):
```javascript
posthog.capture('viral_loop_closed', {
  original_referrer_id: originalReferrerId,
  generation: referralGeneration + 1,  // tracks viral chain depth
  mechanic: mechanic
});
```

### 2. Build the viral funnel

Using `posthog-funnels`, create a funnel insight:

```
viral_trigger_action -> viral_share_initiated -> viral_landing_viewed -> viral_signup_completed -> viral_referee_activated -> viral_loop_closed
```

Save as "Viral Loop Funnel — [Mechanic Name]". Break down by:
- `share_channel` (which channels convert best)
- `mechanic` (if running multiple viral mechanics)
- Cohort week (is the funnel improving over time)

### 3. Create viral cohorts

Using `posthog-cohorts`, create these cohorts:

- **Active referrers**: users who triggered `viral_share_initiated` in the last 30 days
- **Viral signups**: users whose signup included a `referral_code`
- **Loop closers**: users who triggered `viral_loop_closed` (virally acquired users who then referred others)
- **Dormant referrers**: users who shared 30+ days ago but not since, AND are still active in the product

### 4. Build the viral coefficient dashboard

Using `posthog-dashboards`, create "Viral Metrics Dashboard" with:

**Card 1 — Viral Coefficient (K)**:
- Formula: (viral_share_initiated SUM of recipients_count) / (count of active users) * (viral_signup_completed / viral_landing_viewed)
- Display as: line chart, weekly, last 12 weeks
- Target line at K = 0.3 (Smoke), K = 0.5 (Baseline)

**Card 2 — Viral Funnel Conversion**:
- Funnel from trigger to loop-close
- Display as: funnel chart with conversion rates between each step

**Card 3 — Invite Volume**:
- Count of `viral_share_initiated` events per week
- Break down by `share_channel`

**Card 4 — Time to Activation (Viral Signups)**:
- Distribution of `days_to_activate` for viral signups
- Compare against non-viral signup activation time

**Card 5 — Viral Chain Depth**:
- Distribution of `generation` values from `viral_loop_closed`
- Shows how many levels deep viral chains propagate

### 5. Set up attribution webhooks

Using `n8n-triggers`, create a workflow that fires on `viral_signup_completed`:

1. Receive the PostHog webhook with referral_code and referrer_id
2. Look up the referrer in CRM (Attio)
3. Increment the referrer's `referral_count` property
4. If a reward threshold is met, trigger the reward fulfillment
5. Log the attribution in Attio as a note on both the referrer and referee records

Using `n8n-workflow-basics`, create a weekly aggregation workflow:

1. Query PostHog for the week's viral metrics
2. Calculate K, invite volume, conversion rate, activation rate
3. Compare to previous week
4. Post summary to Slack or store in Attio

## Output

- Complete PostHog event schema tracking every stage of the viral loop
- Viral funnel insight with channel and cohort breakdowns
- 4 viral cohorts for targeting and analysis
- Viral Metrics Dashboard with K-factor, funnel, and chain depth
- n8n attribution webhook and weekly summary automation

## Triggers

Run once when entering Baseline level. Update the event schema if the viral mechanic changes. The weekly summary automation runs continuously from Baseline onward.
