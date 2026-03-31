---
name: ugc-prompt-design
description: Design and deploy in-product prompts that trigger users to create content about the product at the right moment
category: Advocacy
tools:
  - Intercom
  - Loops
  - PostHog
  - Attio
fundamentals:
  - intercom-in-app-messages
  - intercom-product-tours
  - loops-sequences
  - posthog-custom-events
  - posthog-cohorts
  - attio-lists
---

# UGC Prompt Design

This drill designs the trigger points, messaging, and submission flow that convert product users into content creators. The goal is to ask users to share their experience at the moment when they have the most positive momentum — right after a success event — and make the creation process as frictionless as possible.

## Prerequisites

- PostHog tracking core product events (activation, feature usage, milestones)
- Intercom or equivalent in-app messaging configured
- Attio with contact records and power user scores (if available)
- A UGC submission endpoint (run `ugc-submission-webhook` fundamental first, or use a simple form)

## Steps

### 1. Identify the 3-5 trigger moments

Query PostHog to find events that correlate with positive sentiment and product investment. These are the moments when a user is most likely to say "yes" to creating content:

**High-signal triggers:**
- **First value moment:** user completes activation and sees their first result (e.g., first report generated, first automation run, first successful integration)
- **Usage milestone:** user crosses a round-number threshold (100th action, 1000th event, 6-month anniversary)
- **Team expansion:** user invites their 3rd+ team member (social proof that they trust the product)
- **Plan upgrade:** user upgrades to a higher tier (financial commitment = strong endorsement)
- **Support resolution:** user rates a support interaction 5/5 (they feel helped and grateful)

Using `posthog-cohorts`, create cohorts for each trigger:
- "Just activated (last 48 hours)"
- "Milestone reached this week"
- "Expanded team recently"
- "Recently upgraded"
- "Positive support resolution"

### 2. Design the prompt for each trigger

Each prompt follows this structure: context (why now), ask (what specifically), and ease (how simple it is).

**Post-activation prompt (Intercom in-app message):**
- Trigger: 24-48 hours after activation event
- Message: "You just [achieved first result]. Share how you set it up -- it takes 2 minutes and helps others discover [Product]."
- CTA: "Share my setup" -> opens a pre-filled form with their use case auto-detected from their event data
- Dismiss: "Maybe later" -> schedule a re-ask in 14 days

**Milestone prompt (Intercom in-app message):**
- Trigger: when user crosses a milestone threshold
- Message: "You've hit [N] [actions] with [Product]. That's impressive. Would you write a quick review or tip for other users?"
- CTA: "Write a quick tip" -> opens a lightweight form: one-line tip + optional longer story
- Dismiss: snooze for 30 days

**Team expansion prompt (Loops email):**
- Trigger: 3rd team member joins
- Message: "Your team is growing on [Product]. Teams like yours often have great stories. Would your team be open to sharing how you use [Product]?"
- CTA: "Tell our story" -> links to a case study questionnaire (5 questions)

**Upgrade prompt (Intercom in-app message):**
- Trigger: 7 days after upgrade (let them settle in)
- Message: "Thanks for upgrading to [Plan]. Would you share why you chose [Product]? A quick testimonial helps others make the same decision."
- CTA: "Share my experience" -> 3-field form: role, what you use it for, one sentence on why it works

**Support prompt (Loops transactional email):**
- Trigger: 24 hours after 5-star support rating
- Message: "Glad we could help. Would you share your experience on [G2/Capterra/Product Hunt]? It takes 60 seconds."
- CTA: "Leave a review" -> direct link to review platform with pre-filled product name

### 3. Build the submission forms

For each prompt, design the simplest possible submission path:

**Quick tip form (for milestones):**
- One text field: "What's your best tip for using [Product]?" (280 char limit)
- Optional: "Want to say more?" (expandable text area)
- Auto-populated: user name, email, account name, plan tier
- Submit -> POST to `ugc-submission-webhook` with `content_type: "tip"`

**Testimonial form (for upgrades):**
- Field 1: "Your role" (dropdown: founder, manager, IC, other)
- Field 2: "What do you use [Product] for?" (one line)
- Field 3: "Why does it work for you?" (one line)
- Auto-populated: user name, email, company
- Submit -> POST to `ugc-submission-webhook` with `content_type: "testimonial"`

**Case study questionnaire (for team expansion):**
- Q1: "What problem were you solving when you found [Product]?"
- Q2: "How does your team use it today?"
- Q3: "What changed after adopting [Product]?"
- Q4: "Any specific results you can share? (numbers are great)"
- Q5: "Would you be willing to be featured by name?"
- Submit -> POST to `ugc-submission-webhook` with `content_type: "case_study"`

### 4. Configure frequency capping

Using `posthog-custom-events`, track `ugc_prompt_shown` and `ugc_prompt_dismissed` events. Build frequency rules:

- Maximum 1 UGC prompt per user per 14 days (across all trigger types)
- If a user dismisses 2 prompts in a row, stop showing prompts for 60 days
- If a user submits content, stop prompts for 90 days (they already contributed)
- Never show UGC prompts to users with open support tickets or declining usage

Using `attio-lists`, maintain a "UGC Prompt Suppression" list for users in cooldown.

### 5. Track prompt performance

Fire PostHog events for the full prompt funnel:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `ugc_prompt_shown` | Prompt rendered to user | `trigger_type`, `prompt_variant`, `user_tier` |
| `ugc_prompt_clicked` | User clicks the CTA | `trigger_type`, `prompt_variant` |
| `ugc_prompt_dismissed` | User dismisses | `trigger_type`, `dismiss_count` |
| `ugc_form_started` | User opens submission form | `form_type`, `trigger_type` |
| `ugc_form_completed` | User submits content | `form_type`, `content_type`, `trigger_type` |
| `ugc_form_abandoned` | User opens form but does not submit within 10 min | `form_type`, `trigger_type`, `fields_completed` |

Build a PostHog funnel: `ugc_prompt_shown` -> `ugc_prompt_clicked` -> `ugc_form_started` -> `ugc_form_completed`

## Output

- 3-5 trigger-based UGC prompts deployed via Intercom and Loops
- Submission forms for tips, testimonials, and case studies
- Frequency capping rules preventing prompt fatigue
- Full PostHog event tracking for the prompt-to-submission funnel
- Attio suppression list for cooldown management

## Triggers

Run once at play setup. Re-run when adding new trigger moments or when prompt performance data suggests a redesign.
