---
name: best-practices-content-pipeline
description: Research user behavior data, identify highest-value best practices and workflow patterns, and produce structured content cards for in-app and email delivery
category: Enablement
tools:
  - PostHog
  - Anthropic
  - Intercom
  - Ghost
fundamentals:
  - posthog-cohorts
  - posthog-session-recording
  - posthog-custom-events
  - ai-content-ghostwriting
  - intercom-help-articles
  - ghost-blog-publishing
---

# Best Practices Content Pipeline

This drill produces a library of best-practices content cards — short, actionable tips that teach users optimal workflows. Each card maps to a specific product behavior the user has not yet adopted. The content is structured for programmatic delivery via Intercom and Loops, not as a static knowledge base.

## Input

- PostHog instance with at least 30 days of product usage data
- Access to session recordings of power users (top 10% by usage volume)
- Product feature list with usage frequency data
- Brand voice guidelines (tone, reading level, terminology)

## Steps

### 1. Mine power-user behavior patterns

Using the `posthog-cohorts` fundamental, define a "power users" cohort: top 10% by session frequency and feature breadth (uses 5+ distinct features per week). Then use the `posthog-session-recording` fundamental to watch 20-30 session recordings from this cohort.

For each recording, document:
- Which features the power user combines in sequence (workflow patterns)
- Keyboard shortcuts or UI shortcuts the user employs
- Settings or configurations the user has customized
- Workarounds or non-obvious paths the user takes
- Any feature the user uses in a way that differs from the intended flow

Aggregate into a frequency table: which behavior patterns appear in 30%+ of power-user sessions? These are your best practices. Target 10-15 distinct patterns.

### 2. Rank practices by retention correlation

Using `posthog-custom-events`, cross-reference each identified behavior pattern with 30-day retention data:

For each pattern, query PostHog:
- What percentage of users who exhibit this pattern retain at 30 days?
- What percentage of users who do NOT exhibit this pattern retain at 30 days?
- What is the retention lift (difference between the two)?

Rank patterns by retention lift. The top 5-8 patterns with the highest retention correlation become your first batch of best-practices cards. A pattern that correlates with a 15pp retention lift is worth more than one with a 3pp lift.

### 3. Structure each content card

Each best practice becomes a content card with this schema:

```json
{
  "id": "bp-{sequential-number}",
  "title": "{Action verb} + {Specific outcome}",
  "hook": "{One sentence describing the benefit, under 80 characters}",
  "body": "{3-5 sentences: what the practice is, why it matters, how to do it}",
  "steps": [
    {"step": 1, "instruction": "{Exact UI action with element names}", "screenshot_tag": "[SCREENSHOT: {description}]"},
    {"step": 2, "instruction": "{Next action}", "screenshot_tag": "[SCREENSHOT: {description}]"}
  ],
  "cta_label": "{Action verb matching the first step}",
  "cta_deeplink": "{Product URL that opens the relevant screen}",
  "trigger_event": "{PostHog event indicating the user would benefit from this tip}",
  "exclude_event": "{PostHog event indicating the user already does this}",
  "retention_lift": "{Xpp}",
  "category": "workflow | shortcut | configuration | integration | advanced"
}
```

Rules:
- Maximum 3 steps per card. If the practice requires more, split into multiple cards.
- Every step names the exact UI element ("Click the **Filters** dropdown in the top toolbar").
- The `trigger_event` defines when to show this card (e.g., user completes a task the slow way).
- The `exclude_event` prevents showing the card to users who already follow the practice.
- The `cta_deeplink` opens the product at the exact screen where the user starts the practice.

### 4. Generate card content

Using the `ai-content-ghostwriting` fundamental, generate the body text for each card via the Anthropic API:

```
System prompt: "You are writing in-app best-practices tips for {PRODUCT}. Each tip must:
- Lead with the user benefit, not the feature name
- Be scannable in under 30 seconds
- Use active voice and second person ('you')
- Include specific numbers when possible ('saves ~2 minutes per task')
- Never use marketing language or superlatives
- Sound like a helpful teammate, not a product announcement
Target reading level: Grade 8."

User prompt: "Write a best-practice tip about: {BEHAVIOR_PATTERN}. The data shows users who do this retain {RETENTION_LIFT} better. Context: {SESSION_RECORDING_OBSERVATIONS}."
```

**Human action required:** Review each card for accuracy. Verify all UI element names match the current product. Test each deep link. Remove any tip that feels obvious to experienced users.

### 5. Publish to Intercom help center

Using the `intercom-help-articles` fundamental, create an article collection called "Best Practices" in your Intercom Help Center. Publish each card as a standalone article tagged with its category. This serves as the persistent reference library — users can browse all tips at any time.

### 6. Publish to knowledge base (web)

Using the `ghost-blog-publishing` fundamental, publish a "Best Practices" index page at `{yourdomain}/best-practices`. Each card links to a standalone page. Add structured data markup (HowTo schema) for SEO. Track views and engagement via PostHog.

### 7. Instrument content card tracking

Using `posthog-custom-events`, define these events:

| Event | When Fired | Key Properties |
|-------|-----------|---------------|
| `best_practice_shown` | Card displayed to user (any surface) | `card_id`, `category`, `surface` (in-app, email, web), `trigger_event` |
| `best_practice_clicked` | User clicks the CTA on the card | `card_id`, `category`, `surface` |
| `best_practice_completed` | User performs the behavior within 24h of seeing the card | `card_id`, `category`, `surface`, `time_to_complete_seconds` |
| `best_practice_dismissed` | User dismisses or closes the card | `card_id`, `category`, `surface` |

Build a PostHog funnel: `best_practice_shown` -> `best_practice_clicked` -> `best_practice_completed`. Break down by `card_id` and `surface` to identify which cards drive behavior change and which surface delivers them most effectively.

## Output

- 5-8 structured content cards ranked by retention lift
- Cards published in Intercom Help Center and on the web
- PostHog event taxonomy for tracking card engagement
- A funnel measuring shown -> clicked -> completed per card

## Triggers

Run this drill once at Smoke level to produce the initial card library. Re-run quarterly (or when product UI changes significantly) to update existing cards and add new ones based on fresh session recording analysis.
