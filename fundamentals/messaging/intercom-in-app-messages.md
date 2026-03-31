---
name: intercom-in-app-messages
description: Create targeted in-app messages in Intercom for user engagement
tool: Intercom
product: Intercom
difficulty: Intermediate
---

# Send In-App Messages with Intercom

## Prerequisites
- Intercom account with Messenger installed on your app
- User identification set up (passing user ID and properties to Intercom)

## Steps

1. **Choose your message type.** Intercom offers several in-app formats: Chat messages (appear in the Messenger widget), Posts (banner-style announcements), Tooltips (point at specific UI elements), and Custom Bots (interactive flows). Choose based on your goal: chat for support, posts for announcements, tooltips for feature education.

2. **Define your audience via API.** Use the Intercom REST API to create targeted messages:
   ```
   POST /messages
   {
     "message_type": "inapp",
     "body": "Export your data in one step -- CSV export is live.",
     "from": {"type": "admin", "id": "<admin-id>"},
     "to": {"type": "user", "user_id": "<user-id>"}
   }
   ```
   For audience-wide messages, configure targeting rules using user properties and events: e.g., signed up >7 days ago AND has not used the feature AND plan = "pro".

3. **Write concise copy.** In-app messages should be under 50 words. Lead with the benefit, not the feature. Bad: "We added CSV export." Good: "Export your data in one step -- CSV export is live." Include a single clear CTA that links directly to the feature.

4. **Set display rules.** Configure when the message appears: on page load, after a delay (5-10 seconds), or when the user performs a specific action. Set frequency to "show_once" for announcements or "show_until_dismissed" for important notifications.

5. **Schedule or trigger.** Choose between one-time send (announcements) or ongoing (behavior-triggered). Ongoing messages fire for every user matching audience criteria going forward -- useful for onboarding tips and feature discovery.

6. **Measure impact via API.** Query message metrics: `GET /messages/<id>/stats`. Track impressions, engagement rate, and downstream actions. If engagement rate is below 5%, revise the copy or targeting. Remove underperforming messages via `DELETE /messages/<id>`.
