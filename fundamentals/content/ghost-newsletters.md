---
name: ghost-newsletters
description: Send email newsletters through Ghost's built-in newsletter feature via the Admin API
tool: Ghost
difficulty: Intermediate
---

# Send Ghost Newsletters

## Prerequisites
- Ghost instance with newsletter feature enabled
- Subscriber list with segmented members

## Steps

1. **Configure newsletter settings via API.** Use the Ghost Admin API to manage newsletter configuration:
   ```
   GET /ghost/api/admin/newsletters/
   PUT /ghost/api/admin/newsletters/<id>/
   { "newsletters": [{ "sender_name": "Your Name", "sender_email": "hello@company.com" }] }
   ```

2. **Create a newsletter post via API.** Create a post with email delivery enabled:
   ```
   POST /ghost/api/admin/posts/
   {
     "posts": [{
       "title": "Weekly Update: March 2025",
       "html": "<p>Newsletter content...</p>",
       "email_segment": "status:free",
       "newsletter": { "id": "<newsletter-id>" }
     }]
   }
   ```
   Choose recipient segment: all subscribers, free members, paid members, or a specific label.

3. **Write for email format.** Keep paragraphs short -- email renders differently than web. Ghost posts double as email content, so optimize for both.

4. **Send a test email.** Use the Ghost Admin API to send a test email before broadcasting to verify formatting, links, and images render correctly.

5. **Publish and send.** Update the post status to `published` with `email_only: true` or both web and email. Schedule for optimal send time (Tuesday-Thursday, 9-11am).

6. **Monitor analytics via API.** Query post analytics:
   ```
   GET /ghost/api/admin/posts/<id>/
   ```
   Check email open rates, click rates, and unsubscribes. Target: >40% open rate, >5% click rate, <0.5% unsubscribe rate.
