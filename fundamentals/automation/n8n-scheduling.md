---
name: n8n-scheduling
description: Build scheduled n8n workflows for recurring GTM tasks
tool: n8n
product: n8n
difficulty: Beginner
---

# Schedule Recurring Workflows in n8n

## Prerequisites
- n8n instance running
- Clear definition of the recurring task and its frequency

## Steps

1. **Add a Schedule Trigger node.** Create a new workflow and add the Schedule Trigger as the first node. This trigger fires at the interval you configure, with no external event needed.

2. **Configure the schedule.** Use n8n's visual schedule builder or cron expressions. Common GTM schedules: Hourly lead sync ("0 * * * *"), Daily morning report ("0 9 * * 1-5"), Weekly pipeline review ("0 9 * * 1"), Monthly metrics export ("0 9 1 * *"). Always set the timezone to your business timezone.

3. **Build daily lead sync.** A common pattern: Schedule Trigger (daily 8am) > HTTP Request (fetch new leads from Clay table via API) > IF node (filter already-synced leads) > Attio node (create new contacts) > Slack node (notify team of new leads). This ensures your CRM stays current.

4. **Build weekly reporting.** Schedule Trigger (Monday 9am) > HTTP Request (pull campaign metrics from Instantly) > HTTP Request (pull pipeline data from Attio) > Code node (calculate key metrics: leads generated, meetings booked, pipeline value) > Slack/Email node (send formatted report).

5. **Build monthly cleanup.** Schedule Trigger (1st of month) > Attio API (find stale deals with no activity in 30+ days) > Slack node (alert owners to update or close stale deals). This keeps your pipeline accurate without manual auditing.

6. **Handle execution windows.** If a scheduled workflow takes longer than its interval (e.g., a sync that runs hourly but takes 90 minutes), enable "Do not start if previous execution is still running" in workflow settings. This prevents overlapping runs and duplicate data.
