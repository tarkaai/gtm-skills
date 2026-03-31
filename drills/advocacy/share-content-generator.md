---
name: share-content-generator
description: Auto-generate shareable content (preview cards, share text, hashtags) from product data for each share channel
category: Advocacy
tools:
  - Anthropic
  - PostHog
  - n8n
fundamentals:
  - og-meta-generation
  - posthog-custom-events
  - n8n-workflow-basics
---

# Share Content Generator

This drill auto-generates share-ready content for each shareable resource and channel. Instead of the user writing their own share text, the product pre-generates compelling, channel-appropriate copy and visuals that the user can share with one click. Higher-quality share content drives higher click-through rates on shared links.

## Prerequisites

- Share link system deployed (run `social-share-surface-build` first)
- Product data accessible for the shareable resource (title, metrics, user info)
- Anthropic API key for text generation

## Steps

### 1. Define share content templates per resource type

For each shareable resource, create content templates per channel:

**Achievement shares:**
- Twitter/X: `"{achievement_description} {metric_value} {share_url} via @YourProduct"` (max 260 chars to leave room for link)
- LinkedIn: `"Milestone: {achievement_description}\n\n{context_paragraph}\n\n{share_url}\n\n#YourProduct #{industry_hashtag}"`
- Email subject: `"I just hit {metric_value} on YourProduct"`

**Dashboard/report shares:**
- Twitter/X: `"My {report_period} {report_type} — {headline_metric}: {metric_value} {share_url}"`
- LinkedIn: `"{professional_insight_about_the_data}\n\nBuilt with @YourProduct\n\n{share_url}"`
- Email subject: `"Take a look at my {report_type}"`

**Template/configuration shares:**
- Twitter/X: `"Free {template_type} template for {use_case}: {share_url} via @YourProduct"`
- LinkedIn: `"I built a {template_type} for {use_case} — sharing it publicly.\n\n{share_url}"`

### 2. Build the content generation pipeline

Using `n8n-workflow-basics`, create a workflow triggered when a share link is generated:

1. Receive the share link creation event (resource type, resource ID, channel)
2. Fetch the resource data from your product API (title, metrics, user name, etc.)
3. For simple templates (achievements, metrics): apply string interpolation
4. For complex content (professional LinkedIn posts): call Anthropic API with a prompt:

```
Generate a {channel} post for sharing a {resource_type}.

Context:
- Resource: {resource_title}
- Key metric: {metric_label}: {metric_value}
- User: {user_name}
- Product: YourProduct

Rules:
- {channel-specific rules: character limit, tone, hashtag policy}
- Do not use exclamation marks or superlatives
- Focus on the metric or result, not on the product itself
- Make it sound like the user wrote it, not the product's marketing team
```

5. Store the generated content alongside the share link
6. Return the content with the share link response

### 3. Generate dynamic OG images per resource

Using `og-meta-generation`, generate a unique OG image for each shared resource:

1. Extract the headline data from the resource (title, top metric, user avatar)
2. Call the `/api/og` endpoint with the extracted parameters
3. Cache the generated image URL in the share link record
4. Set the meta tags on the shared resource page to use the cached OG image

The OG image should make the share link preview visually distinctive in a social feed. Avoid generic product branding — show the user's specific data or achievement.

### 4. A/B test share content variants

Track which share content variants produce higher click-through rates:

Using `posthog-custom-events`, include the content variant in share events:

```javascript
posthog.capture('share_action_completed', {
  resource_type: 'achievement',
  channel: 'twitter',
  content_variant: 'metric_focused',  // vs 'narrative', 'question_hook', etc.
  share_text_length: 142
});
```

Compare: `share_link_clicked` rate by `content_variant` and `channel`. After 100+ shares per variant, adopt the winner and generate a new challenger.

### 5. Handle edge cases

- Resource has no metrics: generate content focused on the resource type and user context
- User has no public profile: omit the "Shared by" line, use product branding only
- Content generation fails (API error): fall back to the static template version
- User edits the share text: track `share_text_edited` event and compare CTR of edited vs auto-generated

## Output

- Auto-generated share text for each (resource type, channel) combination
- Dynamic OG images reflecting each shared resource's specific data
- Content variant tracking for continuous optimization
- Fallback templates for when generation fails

## Triggers

Runs on every share link creation. The content generation should complete in <2 seconds so the share popover loads quickly. Pre-generate content for popular resources during off-peak hours.
