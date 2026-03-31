---
name: collaboration-network-effects
description: Detect, measure, and amplify viral loops from collaboration features — optimize invite flows, sharing surfaces, and referral attribution to increase the viral coefficient
category: Product
tools:
  - PostHog
  - Intercom
  - Loops
  - n8n
  - Attio
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - posthog-cohorts
  - posthog-feature-flags
  - posthog-experiments
  - intercom-in-app-messages
  - loops-sequences
  - n8n-workflow-basics
  - n8n-triggers
  - attio-contacts
---

# Collaboration Network Effects

This drill finds the 10x multiplier in collaboration features. Instead of manually driving adoption, it identifies and amplifies the organic loops where users invite others, share content, and create network effects that grow usage without proportional effort. The output is a self-reinforcing system where every new collaborator increases the value for existing users.

## Input

- Collaboration event taxonomy instrumented (run `collaboration-instrumentation` first)
- At least 4 weeks of collaboration data showing invite, share, and co-editing patterns
- PostHog experiments enabled for A/B testing
- Intercom configured for in-app messaging
- Loops configured for lifecycle emails

## Steps

### 1. Map the existing viral loops

Using `posthog-funnels`, identify every path through which one user's action leads to another user's activation:

**Loop 1 — Invite loop:**
User A invites -> User B accepts -> User B gets value -> User B invites User C

Measure: What percentage of invited users eventually send their own invite? This is the invite propagation rate.

**Loop 2 — Share loop:**
User A shares content publicly -> Non-user views -> Non-user signs up -> New user creates own content -> New user shares

Measure: What percentage of share viewers convert to signups? What percentage of those signups eventually share?

**Loop 3 — Co-editing loop:**
User A starts a project -> Invites User B to co-edit -> User B discovers features through collaboration -> User B starts their own project -> User B invites User C

Measure: Do co-editing participants use more features than solo users? Do they create more content?

For each loop, compute the full cycle time (days from trigger to completion) and the conversion rate at each step.

### 2. Find the highest-leverage bottleneck

Using `posthog-cohorts`, identify where each loop breaks down:

- **Invite loop bottleneck options:** Low invite send rate (users never invite), low acceptance rate (invites ignored), low invitee activation rate (new users do not engage), low propagation rate (activated invitees do not re-invite)
- **Share loop bottleneck options:** Low share creation rate, low view-to-signup rate, low new-user-to-sharer rate
- **Co-editing loop bottleneck options:** Low co-editing initiation rate, low feature discovery during co-editing, low independent project creation rate

Rank bottlenecks by potential impact: `(current conversion rate) × (total volume at that step) × (estimated improvement potential)`. Start with the bottleneck that has the highest combined score.

### 3. Optimize the invite flow

For the invite loop, test improvements using `posthog-experiments` and `posthog-feature-flags`:

**Invite trigger timing:**
- Test prompting invites at the moment of highest value (after first success) vs. during onboarding vs. after 7 days
- Use PostHog feature flags to split users into timing cohorts

**Invite mechanism:**
- Test invite-by-email vs. shareable link vs. in-app invite panel
- Using `intercom-in-app-messages`, test different invite prompts: "Invite a teammate" vs. "Share this with your team" vs. "{User}'s project works better with teammates"

**Invite email optimization:**
- Using `loops-sequences`, A/B test invite email subject lines, sender (product vs. personal from inviter), and CTA copy
- Track `team_invite_accepted` rate per variant

**Post-acceptance onboarding:**
- Test whether invited users who land directly in the inviter's workspace (contextual onboarding) activate faster than those who go through standard onboarding
- Use `posthog-feature-flags` to route invited users to variant onboarding flows

### 4. Optimize sharing surfaces

For the share loop, use `intercom-in-app-messages` and `posthog-experiments`:

**Sharing prompts:**
- Test adding "Share" CTAs at content completion moments (after creating a report, finishing a project, reaching a milestone)
- Test different share scopes: default to public link vs. default to team-only
- Measure `content_shared` rate and downstream `shared_content_viewed` → signup conversion

**Share landing pages:**
- Test shared content landing pages: full content visible vs. partial content with signup gate vs. interactive preview
- The page must attribute signups back to the sharer for viral coefficient computation

**Social proof on shared content:**
- Test adding "Created with [Product]" badges on shared content
- Test adding collaboration activity indicators ("3 people edited this", "12 comments")

### 5. Build the amplification engine

Using `n8n-workflow-basics` and `n8n-triggers`, create automated amplification:

**For power collaborators (from `collaboration-instrumentation` cohort):**
- Using `intercom-in-app-messages`, surface a "Your content was viewed {N} times this week" notification
- If their shared content has high view-to-signup conversion, prompt them to share more: "Your last 3 shares brought in 5 new users"
- Using `loops-sequences`, send a monthly "collaboration impact" email showing their network effect contribution

**For solo users with team potential:**
- Detect solo users whose usage patterns match team users (multiple projects, high frequency, broad feature use)
- Using `intercom-in-app-messages`, show: "Teams who use [Product] together are {X}% more productive. Invite your first teammate."
- Using `posthog-cohorts`, track whether this nudge increases invite rates

**For stalled invites:**
- Using `n8n-triggers`, detect when `team_invite_sent` occurred but `team_invite_accepted` has not after 48 hours
- Trigger a reminder to the inviter: "Your invite to {name} is still pending. Want to resend?"
- Optionally trigger a second invite email to the invitee with different copy

### 6. Measure and iterate on the viral coefficient

Using `posthog-custom-events`, compute k-factor weekly and track which optimizations moved it:

```
k_invite = (invites_per_user_per_week) × (acceptance_rate) × (activation_rate)
k_share = (shares_per_user_per_week) × (view_to_signup_rate) × (activation_rate)
k_total = k_invite + k_share
```

Log as PostHog insight `Network Effect: Combined K-Factor (weekly)`. Tag each week's k-factor with which experiments were active, so you can attribute changes to specific optimizations.

Target progression:
- Smoke: Establish baseline k (typically 0.05-0.15)
- Baseline: k >= 0.2
- Scalable: k >= 0.4
- Durable: k >= 0.5 sustained (each user brings in half a new user over their lifetime)

### 7. Attribution and ROI tracking

Using `attio-contacts`, tag every user with their acquisition source:

- `acquisition_source`: organic, invite, shared_content, paid, direct
- `invited_by_user_id`: the user who invited them (if applicable)
- `shared_content_source_id`: the shared content that led to signup (if applicable)
- `network_depth`: how many invite/share hops from the original organic user (1 = directly invited, 2 = invited by an invitee, etc.)

This lets you compute: what percentage of your user base came through collaboration network effects? What is the lifetime value of users acquired through invites vs. shares vs. paid?

## Output

- Viral loop maps with conversion rates at each step
- Ranked bottleneck analysis showing highest-leverage improvement opportunities
- A/B test results for invite flow, sharing surfaces, and amplification messages
- Amplification engine running autonomously (power collaborator engagement, solo-to-team nudges, stalled invite recovery)
- Weekly k-factor tracking with experiment attribution
- Per-user network-effect attribution in Attio

## Triggers

- Viral loop analysis: run once at setup, refresh monthly
- Invite flow experiments: continuous (one at a time per the `ab-test-orchestrator` guardrails)
- Amplification engine: always-on via n8n triggers
- K-factor computation: weekly via n8n cron
- Attribution sync: daily via n8n cron
