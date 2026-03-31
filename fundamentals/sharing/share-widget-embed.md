---
name: share-widget-embed
description: Build and embed in-product share buttons and share cards with channel-specific formatting
tool: Custom UI Component
difficulty: Config
---

# Share Widget Embed

Build the in-product UI component that users interact with to share content. This is the share button, the share modal/popover, and the channel-specific share actions (copy link, share to Twitter/X, share to LinkedIn, email, Slack).

## Approach

Deploy a reusable share widget component that can be attached to any shareable resource in the product. The widget handles: generating the share link (via `share-link-generation`), formatting content per channel, opening the share flow, and tracking interactions.

## Component Architecture

The share widget consists of:
1. **Share trigger button** — the "Share" button visible on shareable resources
2. **Share popover/modal** — displays share options when triggered
3. **Channel share actions** — each channel has its own share URL format
4. **Share preview** — shows the user what their share will look like

## Implementation

### 1. Share trigger button

Place the share button on every shareable resource surface:

```tsx
<ShareButton
  resourceType="dashboard"
  resourceId={dashboard.id}
  title={dashboard.title}
  description={`${dashboard.metricCount} metrics tracked`}
  metric={{ label: 'Total Revenue', value: '$142K' }}
/>
```

Placement guidelines:
- Dashboards/reports: top-right action bar, next to "Export" and "Print"
- Achievements/milestones: inline in the celebration modal, primary CTA
- Workspaces/projects: in the workspace header, secondary action
- Results/outputs: below the result, as a "Share this result" link

### 2. Share popover with channel options

When the user clicks "Share," display a popover with these options:

| Channel | Action | URL Format |
|---------|--------|-----------|
| **Copy Link** | Copy share URL to clipboard | `https://yourapp.com/s/{code}` |
| **Twitter/X** | Open Twitter compose with pre-filled text | `https://twitter.com/intent/tweet?text={encoded_text}&url={share_url}` |
| **LinkedIn** | Open LinkedIn share dialog | `https://www.linkedin.com/sharing/share-offsite/?url={share_url}` |
| **Email** | Open mailto with subject and body | `mailto:?subject={encoded_subject}&body={encoded_body}` |
| **Slack** | Copy formatted message for Slack | Rich-text with link preview |

### 3. Pre-generate share text per channel

Each channel needs different formatting:

**Twitter/X** (max 280 chars):
```
{achievement_text} {share_url} via @YourProduct
```
Example: "Just hit 10,000 page views this month on my dashboard. {share_url} via @YourProduct"

**LinkedIn** (professional tone, longer):
```
{professional_context}

{metric_highlight}

{share_url}

#YourProduct #{relevant_hashtag}
```

**Email**:
```
Subject: Check out {resource_title} on YourProduct
Body: I wanted to share {resource_description}. Take a look: {share_url}
```

### 4. Track all share widget interactions

Fire PostHog events at every step:

```javascript
// User clicks the share button
posthog.capture('share_widget_opened', {
  resource_type: 'dashboard',
  resource_id: 'abc-123',
  surface_location: 'dashboard_header'  // where in the UI the button was
});

// User selects a channel
posthog.capture('share_channel_selected', {
  resource_type: 'dashboard',
  resource_id: 'abc-123',
  channel: 'twitter'
});

// Share action completed (link copied, tweet window opened, etc.)
posthog.capture('share_action_completed', {
  resource_type: 'dashboard',
  resource_id: 'abc-123',
  channel: 'twitter'
});

// Share popover dismissed without sharing
posthog.capture('share_widget_dismissed', {
  resource_type: 'dashboard',
  resource_id: 'abc-123',
  time_open_ms: 3400
});
```

### 5. Native Web Share API fallback (mobile)

On mobile browsers that support `navigator.share()`, use the native share sheet instead of the custom popover:

```javascript
if (navigator.share) {
  await navigator.share({
    title: shareTitle,
    text: shareText,
    url: shareUrl
  });
  posthog.capture('share_action_completed', {
    resource_type, resource_id, channel: 'native_share'
  });
}
```

## Error Handling

- Share link generation fails: show "Copy link" with the direct resource URL as fallback, fire error event
- Clipboard API not available: show a text input with the URL pre-selected for manual copy
- Third-party share window blocked by popup blocker: fall back to opening in the current tab

## Verification

Test each channel:
1. Click share button — popover appears with all channel options
2. Copy link — clipboard contains the tracked share URL
3. Twitter — opens Twitter compose with correct text and URL
4. LinkedIn — opens LinkedIn share dialog with correct URL
5. Email — opens email client with correct subject and body
6. PostHog Live Events shows all share events firing correctly
