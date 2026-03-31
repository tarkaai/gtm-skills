---
name: viral-mechanic-design
description: Design a product-native viral mechanic (invite, share, collaborate) that creates a loop where usage by one user exposes the product to non-users
category: Product
tools:
  - PostHog
  - Intercom
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - intercom-in-app-messages
---

# Viral Mechanic Design

This drill produces a specification for one product-native viral mechanic — a feature where using the product inherently exposes it to non-users, creating an acquisition loop without paid spend. The output is a mechanic spec an agent or engineer can implement.

## Input

- Product with active users (minimum 100 MAU to observe natural sharing patterns)
- PostHog tracking installed with core product events
- Knowledge of which product actions produce outputs visible to non-users

## Steps

### 1. Identify natural sharing moments

Query PostHog using `posthog-cohorts` to find users who already share product outputs organically. Look for events that involve external parties: emails sent from the product, links generated, exports created, invitations sent, collaborative sessions started, public pages published.

Rank these by frequency and by downstream conversion (did the external party sign up?). If no organic sharing exists yet, identify the 3 product actions whose outputs would be most valuable to a non-user seeing them for the first time.

### 2. Select the viral mechanic type

Choose ONE mechanic from these proven patterns:

**Invite-to-collaborate**: The product works better with teammates. The user needs to invite others to get full value. Examples: project management (invite team), shared docs (invite editors), team messaging (invite colleagues).
- Viral trigger: user creates a shared workspace or project
- Exposure: invitee receives an email or link requiring signup to participate
- Viral coefficient driver: number of invitees per inviter

**Share-to-show**: The product generates outputs worth sharing. The user shares results, reports, or achievements with their network. Examples: analytics dashboards (share reports), design tools (share previews), fitness apps (share achievements).
- Viral trigger: user generates a shareable output
- Exposure: viewer sees a branded preview page requiring signup to create their own
- Viral coefficient driver: reach of each shared output

**Use-to-expose**: Normal product usage passively exposes the product to non-users. Examples: email signatures (powered-by branding), embedded widgets (data from product), collaborative forms (recipient sees product branding).
- Viral trigger: user performs a core action that touches an external party
- Exposure: external party sees the product name and value in context
- Viral coefficient driver: volume of external-facing actions per user

Select the mechanic with the highest natural frequency of the trigger action AND the most compelling reason for the external party to sign up.

### 3. Design the viral loop

Document the complete loop as a sequence:

```
Step 1: User performs [trigger action]
Step 2: Product generates [shareable artifact] with [branding + CTA]
Step 3: Non-user receives/sees [artifact] via [channel: email/link/embed]
Step 4: Non-user lands on [conversion surface: signup wall, preview page, invite acceptance]
Step 5: Non-user signs up (completes loop)
Step 6: New user performs [trigger action] (loop repeats)
```

For each step, specify:
- What the user sees (UI element, notification, prompt)
- What data flows between steps (referral ID, invite token, UTM parameters)
- What PostHog events fire (see viral-loop-instrumentation drill)
- What friction exists and how to minimize it

### 4. Define the invite/share UX

Using `intercom-in-app-messages`, design the prompt that encourages the viral action. Rules:

- Trigger the prompt at the moment of highest motivation (immediately after the user creates value, not before)
- Make the viral action 1-click: pre-populate the message, auto-generate the link, default to the most common sharing channel
- Show social proof: "12 of your teammates are already here" or "Your report was viewed 47 times"
- Never gate core product functionality behind the viral action — the user must get value first, then be prompted to share

### 5. Design the landing experience for non-users

The non-user who clicks the shared link or invite must land on a page that:

- Shows the shared artifact (report, workspace, output) with enough value to demonstrate the product
- Requires signup to interact, reply, or create their own
- Pre-fills context from the referral (inviter's name, workspace name, shared content)
- Tracks the referral chain: `posthog-custom-events` with `referrer_id`, `invite_token`, `source_mechanic`

### 6. Calculate expected viral coefficient

Estimate the viral coefficient (K) using:

```
K = invitations_per_user * conversion_rate_per_invitation
```

Use PostHog data to estimate:
- `invitations_per_user`: average number of external parties exposed per active user per month
- `conversion_rate_per_invitation`: percentage of exposed non-users who sign up

Target K >= 0.3 for Smoke test. If estimated K < 0.1, reconsider the mechanic — the trigger action may be too infrequent or the conversion surface too weak.

## Output

- Viral mechanic specification document: mechanic type, trigger action, loop diagram, UX spec
- PostHog event schema for the viral funnel
- Intercom in-app message configuration for the viral prompt
- Expected viral coefficient estimate with assumptions

## Triggers

Run once at Smoke level to design the initial mechanic. Re-run at Scalable level when adding additional mechanic types.
