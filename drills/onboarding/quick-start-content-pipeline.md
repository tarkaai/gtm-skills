---
name: quick-start-content-pipeline
description: Build a concise, scannable quick-start guide with structured steps, deploy it in-app via Intercom and via Loops email, and instrument completion tracking
category: Onboarding
tools:
  - Intercom
  - Loops
  - PostHog
  - Ghost
fundamentals:
  - intercom-help-articles
  - intercom-in-app-messages
  - loops-sequences
  - posthog-custom-events
  - ghost-blog-publishing
---

# Quick-Start Content Pipeline

This drill produces a complete quick-start guide: the content itself, the in-app and email delivery surfaces, and the tracking instrumentation. The guide must be scannable (under 5 minutes to read), action-oriented (every section ends with a specific user action), and multi-surface (accessible in-app, via email, and on the web).

## Input

- Product's activation metric (from `onboarding-sequence-design` or `activation-optimization`)
- 3-5 onboarding milestones from signup to activation
- Product screenshots or screen-recording capability
- Brand voice guidelines (tone, reading level, terminology)

## Steps

### 1. Define the guide structure

Map the guide to your onboarding milestones. Each milestone becomes one guide section. Target 3-5 sections total. Each section follows this template:

```
## Section N: {Action verb} + {Object}
**Time:** {X minutes}
**What you'll do:** {One sentence describing the outcome}

1. {Step 1 — specific instruction with UI element names}
2. {Step 2 — specific instruction}
3. {Step 3 — specific instruction}

**You'll know it worked when:** {Observable confirmation — what the user sees on screen}
```

Rules:
- Maximum 3 steps per section. If a section needs more than 3 steps, break it into two sections.
- Every step references a specific UI element by name ("Click the **New Project** button in the top-right corner").
- Never use vague instructions like "configure your settings" or "set up your account." Name the exact fields and values.
- Include the expected time per section. Total guide time must be under 5 minutes.

### 2. Write the guide content

Using the section template from Step 1, write the complete guide. Include:

**Header:**
- Title: "Get started with [Product] in 5 minutes"
- Subtitle: "Follow these {N} steps to {activation outcome}"
- Progress indicator: "Step 1 of {N}"

**Per-section content:**
- A brief (1-2 sentence) explanation of why this step matters
- Numbered steps with exact UI references
- A screenshot or GIF placeholder tag: `[SCREENSHOT: {description of what to capture}]`
- A confirmation statement: "You'll know it worked when you see {specific UI feedback}"

**Footer:**
- "What's next?" section pointing to 2-3 advanced features
- Help link: "Stuck? [Chat with us](intercom-link) or [email support](mailto:support@...)"
- Feedback hook: "Was this guide helpful? [Yes] [No]" (tracked as PostHog events)

### 3. Deploy the guide in-app via Intercom

Using the `intercom-help-articles` fundamental, create the guide as an Intercom Help Center article:

1. Create the article in the "Getting Started" collection
2. Set visibility: all users (or specific segments if you have persona-based guides)
3. Add the article to the Intercom Messenger home screen as a pinned card
4. Title the Messenger card: "Quick Start Guide — {N} steps, {X} minutes"

Using the `intercom-in-app-messages` fundamental, create a targeted message that surfaces the guide to new users:

- Trigger: user's first session (no `guide_viewed` event exists for this user)
- Format: banner at top of screen or tooltip pointing to the help icon
- Copy: "New here? Follow our 5-minute quick-start guide to get set up."
- CTA: opens the Help Center article
- Dismiss: once dismissed, do not show again

### 4. Deploy the guide via email

Using the `loops-sequences` fundamental, add the guide to the onboarding email sequence:

- **Email 2** (24 hours after signup, if user has not reached Milestone 2): include the full guide content inline (not as a link to an external page). Subject: "[Product] — your 5-minute quick-start guide"
- Make the guide the body of the email with clear step numbering
- Each step's CTA links directly into the product at the relevant screen (deep links, not dashboard links)
- Include a "View in browser" link to the web version

### 5. Deploy the guide on the web

Using the `ghost-blog-publishing` fundamental (or your CMS), publish the guide as a standalone web page:

- URL: `{yourdomain}/quick-start` or `{yourdomain}/docs/quick-start`
- Include the same content as the in-app and email versions
- Add schema markup for "HowTo" structured data (helps with SEO)
- Include PostHog tracking for page views, scroll depth, and time on page

### 6. Instrument completion tracking

Using `posthog-custom-events`, add these events:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `guide_viewed` | User opens the guide (any surface) | `surface` (in-app, email, web), `user_id`, `days_since_signup` |
| `guide_step_completed` | User completes a guide section | `step_number`, `step_name`, `surface`, `time_spent_seconds` |
| `guide_completed` | User completes all guide sections | `surface`, `total_time_seconds`, `days_since_signup` |
| `guide_abandoned` | User opens guide but does not complete within 24 hours | `last_step_completed`, `surface` |
| `guide_feedback` | User clicks the "Was this helpful?" response | `response` (yes/no), `surface` |

Build a PostHog funnel: `guide_viewed` -> `guide_step_completed (step 1)` -> ... -> `guide_completed`. Break down by `surface` to identify which delivery channel drives the highest completion rate.

### 7. Test end-to-end

Before launching:

1. Open the in-app guide as a new user. Verify every step is accurate and every screenshot matches the current UI.
2. Receive the email version. Verify deep links open the correct product screens.
3. View the web version. Verify PostHog events fire on view, step completion, and feedback.
4. Complete the full guide. Verify `guide_completed` fires and the user's activation metric is tracked.
5. If any step is inaccurate, unclear, or broken, fix before launch.

## Output

- A complete quick-start guide (3-5 sections, under 5 minutes)
- Guide deployed on 3 surfaces: Intercom help article, Loops email sequence, web page
- PostHog events tracking guide views, step completions, abandonment, and feedback
- A funnel showing guide completion rates by delivery surface

## Triggers

Run once during play setup (Smoke level). Update the guide content when the product UI changes significantly or when guide completion data reveals a problematic step.
