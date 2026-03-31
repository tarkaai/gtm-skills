---
name: loom-analytics
description: Track video engagement data from Loom via API to prioritize follow-ups
tool: Loom
product: Loom
difficulty: Beginner
---

# Track Loom Video Analytics

## Prerequisites
- Loom account with shared videos
- Loom API access (Business plan)

## Steps

1. **Query video analytics via API.** Use the Loom API to retrieve engagement data for your videos:
   ```
   GET /v1/videos/<video-id>/analytics
   ```
   Returns: total views, unique viewers, average watch percentage, and viewer list.

2. **Check the viewer list.** The API returns who watched (by email if logged in) and how much they watched. This data is critical for sales follow-up prioritization.

3. **Prioritize follow-ups based on engagement.** A prospect who watched 90% of your demo is more interested than one who watched 10%. Build an n8n workflow that scores viewers by watch percentage and creates prioritized follow-up tasks in Attio.

4. **Set up view notifications.** Configure Loom webhooks to notify you in real-time when someone watches your video. Follow up within hours for maximum impact.

5. **Track CTA engagement.** If you added a CTA button (book a call, visit pricing), the API returns how many viewers engaged with it. Use this to measure video-to-meeting conversion rates.

6. **Sync to CRM and analytics.** Build an n8n workflow: Loom webhook (video viewed) -> Attio (update contact with "watched demo video" activity) -> PostHog (capture `video_viewed` event with properties: video_id, watch_percentage, viewer_email). This connects video engagement to your pipeline.
