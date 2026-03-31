---
name: intercom-in-app-messages
description: Create targeted in-app messages in Intercom for user engagement
tool: Intercom
difficulty: Intermediate
---

# Send In-App Messages with Intercom

## Prerequisites
- Intercom account with Messenger installed on your app
- User identification set up (passing user ID and properties to Intercom)

## Steps

1. **Choose your message type.** Intercom offers several in-app formats: Chat messages (appear in the Messenger widget), Posts (banner-style announcements), Tooltips (point at specific UI elements), and Custom Bots (interactive flows). Choose based on your goal: chat for support, posts for announcements, tooltips for feature education.

2. **Define your audience.** In Intercom, go to Messages > New Message. Set targeting rules using user properties and events. Example: show a feature announcement to users who signed up more than 7 days ago AND have not used the feature AND are on the Pro plan. Precise targeting prevents message fatigue.

3. **Write concise copy.** In-app messages should be under 50 words. Lead with the benefit, not the feature. Bad: "We added CSV export." Good: "Export your data in one click -- CSV export is live." Include a single clear CTA button (e.g., "Try it now") that links directly to the feature.

4. **Set display rules.** Configure when the message appears: on page load, after a delay (5-10 seconds), or when the user performs a specific action. Set frequency to "Show once" for announcements or "Show until dismissed" for important notifications. Never set messages to show on every visit.

5. **Schedule or trigger.** Choose between one-time send (for announcements) or ongoing (for behavior-triggered messages). Ongoing messages fire for every user who matches the audience criteria going forward -- useful for onboarding tips and feature discovery.

6. **Measure impact.** Track: impressions (how many saw it), clicks (how many engaged), and the downstream action (how many used the feature or completed the goal). If click rate is below 5%, revise the copy or targeting. Remove underperforming messages to reduce noise.
