---
name: loops-broadcasts
description: Send one-time broadcast emails to segments in Loops
tool: Loops
difficulty: Beginner
---

# Send Broadcast Emails in Loops

## Prerequisites
- Loops audience with segments defined (see `loops-audience`)
- Email content written and reviewed

## Steps

1. **Understand when to use broadcasts.** Broadcasts are one-time sends to a segment. Use them for: product announcements, feature launches, monthly newsletters, event invitations, and company updates. Do not use broadcasts for recurring automated emails -- use sequences instead.

2. **Create a broadcast via API.** Use the Loops API to create and configure a broadcast targeting a specific segment. Never send to your entire audience -- always target a specific segment (e.g., "Active Pro Users" for a Pro-only feature announcement).

3. **Write the email.** Structure the broadcast content: keep it focused on one topic or CTA. Subject line should be specific and curiosity-driven. Preview text should complement (not repeat) the subject line. Body should be scannable with clear sections.

4. **Preview and test.** Send a test email to yourself using the Loops API test endpoint. Verify all links work, personalization variables render correctly ({{firstName}}, {{planName}}), and the email displays properly.

5. **Schedule strategically.** Schedule broadcasts for Tuesday-Thursday, 9am-11am in your primary audience timezone. Avoid Mondays (inbox overload) and Fridays (low engagement). Set a specific send date and time.

6. **Review performance via API.** After 48 hours, pull broadcast metrics via the Loops API. Benchmarks: open rate (target >30% for engaged segments), click rate (target >3%), unsubscribe rate (should be <0.5%). High unsubscribe rate signals poor targeting -- tighten your segment next time.
