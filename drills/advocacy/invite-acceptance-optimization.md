---
name: invite-acceptance-optimization
description: Optimize the invite-to-acceptance funnel by improving email deliverability, reducing signup friction, and personalizing the invited user onboarding experience
category: Advocacy
tools:
  - PostHog
  - Loops
  - Intercom
  - n8n
fundamentals:
  - posthog-funnels
  - posthog-cohorts
  - posthog-custom-events
  - loops-transactional
  - loops-sequences
  - intercom-product-tours
  - intercom-in-app-messages
  - n8n-scheduling
  - n8n-workflow-basics
---

# Invite Acceptance Optimization

This drill systematically improves the conversion rate from invite_sent to invite_accepted. An invite mechanism is only as good as its acceptance rate — a 40% acceptance rate means 60% of your viral potential is wasted. This drill targets each drop-off point in the acceptance funnel.

## Input

- Invite mechanism live with at least 50 invitations sent (from `invite-flow-setup` drill)
- PostHog funnel data showing: invite_sent, invite_email_delivered, invite_link_clicked, invite_accepted, invited_user_first_action
- Loops configured for invite and reminder emails
- Intercom configured for in-app messaging

## Steps

### 1. Diagnose the acceptance funnel

Using `posthog-funnels`, pull the invite funnel for the last 30 days. Calculate conversion at each step:

| Step | Metric | Benchmark |
|------|--------|-----------|
| invite_sent -> invite_email_delivered | Email deliverability | Should be >95%. If below, email validation issue. |
| invite_email_delivered -> invite_link_clicked | Email open + click | Should be >50%. If below, email copy or subject line issue. |
| invite_link_clicked -> invite_accepted | Signup completion | Should be >60%. If below, signup friction issue. |
| invite_accepted -> invited_user_first_action | Activation | Should be >70%. If below, onboarding issue. |

Using `posthog-cohorts`, segment by:
- Invitee domain match (same company vs external)
- Inviter role (admin vs member)
- Entry point of original invite
- Time of day/week invite was sent
- Whether a personal message was included

Identify the biggest drop-off step and the segment with the worst conversion. Focus all optimization effort there.

### 2. Optimize email deliverability (if delivered < 95%)

Check Loops delivery metrics. Common failures:
- **Bounced emails**: Implement email validation before sending. Use Loops webhook to catch bounces and notify the inviter immediately.
- **Spam-filtered**: Ensure the invite email uses a recognized sender domain, minimal HTML, no spam trigger words. Test with mail-tester.com.
- **Typos**: Add a "Did you mean {{suggestedEmail}}?" check for common domain typos (gmial.com, outllok.com).

### 3. Optimize email engagement (if clicked < 50%)

Using `loops-transactional`, test these email improvements:

**Subject line variants to test:**
- A: "{{inviterName}} invited you to {{teamName}}"
- B: "{{inviterName}} wants to work with you on {{productName}}"
- C: "Join {{inviterName}}'s team — {{specificContext}}"

**Email body improvements:**
- Lead with the inviter's personal message (social proof from someone they know)
- Show what the team is working on (specific resource names, not generic descriptions)
- Make the accept button massive and colored — it should be the only visual focal point
- Remove all navigation links except the accept button and an unsubscribe link
- Add the inviter's avatar/photo for visual recognition

**Reminder sequence via `loops-sequences`:**
- Hour 4: No separate email. Just ensure the original is optimized.
- Day 2: "{{inviterName}} is waiting for you to join {{teamName}}." Shorter, more urgent.
- Day 5: "Last chance — {{inviterName}}'s invite to {{teamName}} expires in 9 days." Scarcity.
- Day 12: "Your invite expires tomorrow." Final urgency.

Track each reminder separately: `invite_reminder_sent` with step number and `invite_reminder_clicked`.

### 4. Optimize signup completion (if accepted < 60%)

The signup flow for invited users must be different from organic signup. Invited users already have social proof and context — do not waste it:

**Reduce form fields:**
- Email: pre-filled from the invite link (read-only)
- Name: one field, required
- Password: one field, no confirmation field (use show/hide toggle)
- Everything else: collect later, not at signup

**Pre-fill context:**
- Show the inviter's name and avatar: "{{inviterName}} invited you"
- Show what they will see after signup: "You'll join {{teamName}} and see {{resourceName}}"
- Show the team: avatars of existing team members

**Remove blockers:**
- No credit card required for invited users
- No email verification step (the invite link IS the verification)
- No onboarding questionnaire — skip straight to the team workspace

Track with `posthog-custom-events`:
```javascript
posthog.capture('invite_signup_form_viewed', { account_id, invite_id });
posthog.capture('invite_signup_form_started', { account_id, invite_id, field: 'name' });
posthog.capture('invite_signup_form_error', { account_id, invite_id, field: 'password', error: 'too_short' });
posthog.capture('invite_signup_completed', { account_id, invite_id, time_to_complete_seconds });
```

### 5. Optimize invited user activation (if first_action < 70%)

Invited users need a different onboarding from organic users. They already know someone on the platform and have a specific context for why they were invited.

Using `intercom-product-tours`, build an invited-user tour:
- Step 1: "Welcome! {{inviterName}} invited you to collaborate on {{resourceName}}." Show the resource.
- Step 2: Point to the core collaborative action: comment, edit, share, or whatever the product's team value is.
- Step 3: "Need help? {{inviterName}} is already here." Show how to message or @mention their inviter.
- Do NOT show generic onboarding steps (profile setup, settings, etc.) — defer those until after the first collaborative action.

Using `intercom-in-app-messages`, trigger contextual help:
- If the invited user has not taken an action 30 minutes after accepting, show: "Not sure where to start? {{inviterName}} shared {{resourceName}} with you — start there."
- If the invited user completes their first action, show: "Nice! You and {{inviterName}} are now collaborating. Invite more teammates to keep the momentum going." (This seeds the viral loop.)

### 6. Build the optimization feedback loop

Using `n8n-scheduling`, create a weekly report workflow:

1. Pull the invite funnel metrics from PostHog
2. Compare to last week and to benchmark targets
3. Identify the worst-performing step and segment
4. Generate a summary: "Invite acceptance rate: {{rate}}%. Biggest drop-off: {{step}} ({{conversionRate}}%). Worst segment: {{segment}}. Suggested focus: {{recommendation}}."
5. Post to Slack or store in Attio

This report runs every Monday at 9 AM and provides the data needed to prioritize the next optimization experiment.

## Output

- Diagnosed invite funnel with conversion rates at every step
- Optimized invite email with personalization and reminder sequence
- Frictionless signup flow for invited users (pre-filled, minimal fields)
- Invited-user-specific onboarding tour (context-aware, not generic)
- Weekly optimization report identifying the next improvement opportunity

## Triggers

Run after the invite mechanism has generated 50+ invitations (typically Baseline level). Re-run monthly to identify new optimization opportunities as volume and user mix change.
