---
name: shortcut-discovery-promotion
description: Surface keyboard shortcuts via contextual in-app nudges, command palette prompts, and progressive shortcut education tied to user workflow patterns
category: Enablement
tools:
  - PostHog
  - Intercom
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - posthog-feature-flags
  - intercom-in-app-messages
  - intercom-product-tours
  - n8n-workflow-basics
  - n8n-triggers
---

# Shortcut Discovery Promotion

This drill builds the in-product system that teaches users keyboard shortcuts at the moment they are most useful. Instead of dumping a shortcut cheat sheet on users, it observes how they work and surfaces relevant shortcuts contextually — when the user performs an action the slow way, the system shows them the fast way.

## Input

- Product with keyboard shortcuts or power-user features already implemented
- PostHog tracking user interactions (clicks, navigation, feature usage)
- Intercom configured with Messenger on the product
- A mapping of mouse actions to their keyboard shortcut equivalents

## Steps

### 1. Build the shortcut action map

Create a reference mapping every promotable shortcut to its mouse-path equivalent. Structure:

```json
{
  "shortcuts": [
    {
      "id": "cmd-k-search",
      "keys": "Cmd+K",
      "mouse_path": "click_search_bar",
      "context_page": "/dashboard",
      "category": "navigation",
      "efficiency_gain": "3-5 seconds per use",
      "priority": 1
    },
    {
      "id": "cmd-enter-submit",
      "keys": "Cmd+Enter",
      "mouse_path": "click_submit_button",
      "context_page": "*",
      "category": "action",
      "efficiency_gain": "1-2 seconds per use",
      "priority": 2
    }
  ]
}
```

Rank shortcuts by: frequency of the mouse-path action (higher frequency = higher priority for promotion) multiplied by efficiency gain. The top 5-8 shortcuts should cover 80% of the time savings.

### 2. Instrument shortcut tracking events

Using `posthog-custom-events`, add events for both the mouse path and the shortcut path for every promotable action:

```javascript
// Track when user does it the slow way
posthog.capture('action_via_mouse', {
  action_id: 'search',
  shortcut_equivalent: 'cmd-k',
  page: window.location.pathname
});

// Track when user does it the fast way
posthog.capture('action_via_shortcut', {
  action_id: 'search',
  shortcut_key: 'cmd-k',
  page: window.location.pathname
});

// Track when a shortcut hint is shown
posthog.capture('shortcut_hint_shown', {
  shortcut_id: 'cmd-k-search',
  trigger_type: 'contextual',  // or 'tooltip', 'tour', 'nudge'
  page: window.location.pathname
});

// Track when user tries a shortcut after seeing a hint
posthog.capture('shortcut_hint_converted', {
  shortcut_id: 'cmd-k-search',
  time_since_hint_seconds: timeDelta,
  page: window.location.pathname
});
```

### 3. Create shortcut-readiness cohorts

Using `posthog-cohorts`, define who is ready to learn shortcuts:

- **shortcut-ready-beginner**: Completed onboarding, used 3+ core features via mouse in last 7 days, has NOT used any keyboard shortcuts. These users know the product but not the shortcuts.
- **shortcut-ready-intermediate**: Uses 1-2 shortcuts already, performs 5+ other actions via mouse that have shortcut equivalents. These users are open to shortcuts but do not know them all.
- **shortcut-ready-power**: Uses 5+ shortcuts, still performs some actions via mouse. Show them the remaining shortcuts they have not discovered.
- **shortcut-dormant**: Was shown shortcut hints 3+ times, has not adopted any. Stop showing hints to avoid annoyance. Try a different approach (command palette, settings page) or wait 30 days before re-engaging.

### 4. Build contextual shortcut hints

Using `intercom-in-app-messages`, create tooltip-style messages that appear immediately after a user performs an action via mouse that has a shortcut equivalent:

- **Trigger**: User is in a `shortcut-ready-*` cohort AND just performed `action_via_mouse` for an action with a shortcut equivalent
- **Message**: "Pro tip: Press `{shortcut_key}` to do this instantly." Keep it under 15 words.
- **Display**: Tooltip pointing at the element the user just clicked. Show for 5 seconds, then auto-dismiss. No blocking modal.
- **Frequency cap**: Maximum 1 shortcut hint per session. Maximum 3 per week. Never show the same shortcut hint twice if the user dismissed it.
- **CTA**: No button needed. The hint itself is the education. Optionally include "See all shortcuts" linking to a keyboard shortcut reference.

Using `posthog-feature-flags`, gate the hint system behind a feature flag (`shortcut-hints-enabled`) so you can control rollout percentage and disable instantly if users report annoyance.

### 5. Build the command palette promotion flow

For products with a command palette (Cmd+K / Ctrl+K), build a specific promotion sequence using `intercom-product-tours`:

**Tour: "Meet your command palette"** (3 steps, triggered once for shortcut-ready-beginner users):

1. Step 1: Highlight the search bar. "Everything you need is one keystroke away. Press Cmd+K to open the command palette."
2. Step 2: Interactive — user must press Cmd+K. "Try it now. Type any action, page, or setting."
3. Step 3: "You just saved 5 seconds. The command palette works everywhere. Use it anytime."

Set the tour to trigger on the user's 5th session (they know the product, ready for efficiency tips).

### 6. Build the progressive shortcut education sequence

Using `n8n-workflow-basics`, create a workflow that graduates users through shortcut tiers:

1. Query PostHog daily for users in each shortcut-readiness cohort
2. For `shortcut-ready-beginner`: enable contextual hints for the top 3 highest-priority shortcuts only
3. For `shortcut-ready-intermediate`: enable hints for the next 3 shortcuts (ones they do not use yet)
4. For `shortcut-ready-power`: enable hints for remaining shortcuts plus advanced combinations
5. For `shortcut-dormant`: disable all hints, set a 30-day cooldown flag in Intercom

Using `n8n-triggers`, trigger cohort re-evaluation when a user adopts a new shortcut (fires `action_via_shortcut` for a shortcut they have never used before). This moves them to the next tier and unlocks new hints.

### 7. Build the shortcut reference surface

Create an in-product keyboard shortcut reference accessible via:
- A "?" keystroke (standard convention)
- A help menu item
- The command palette search

Track access to this reference:
```javascript
posthog.capture('shortcut_reference_opened', {
  trigger: 'keystroke' // or 'menu', 'command_palette', 'tooltip_link'
});
```

This serves as both an education tool and a signal — users who open it voluntarily are highly engaged.

## Output

- Shortcut action map linking mouse paths to keyboard equivalents
- PostHog events tracking both mouse and shortcut usage patterns
- Shortcut-readiness cohorts segmenting users by adoption level
- Contextual shortcut hints via Intercom tooltips with frequency caps
- Command palette product tour for first-time discovery
- Progressive education pipeline graduating users through shortcut tiers
- In-product shortcut reference surface

## Triggers

The n8n cohort evaluation runs daily. Contextual hints fire in real-time based on user actions. The command palette tour triggers once per eligible user. Re-run the full setup when adding new shortcuts to the product.
