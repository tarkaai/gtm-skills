---
name: email-subject-testing-baseline
description: >
  Email Subject-Line A/B Testing — Baseline Run. Run weekly automated subject-line tests across
  all retention emails, targeting a 20% relative open-rate lift on tested emails over 2 weeks.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=20% relative open-rate lift on tested emails vs. pre-test baseline"
kpis: ["Open rate lift (relative %)", "Click rate", "Unsubscribe rate", "Tests completed per week"]
slug: "email-subject-testing"
install: "npx gtm-skills add product/retain/email-subject-testing"
drills:
  - email-subject-test-pipeline
  - posthog-gtm-events
  - email-subject-performance-monitor
  - threshold-engine
---

# Email Subject-Line A/B Testing — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Email

## Outcomes

Establish always-on subject-line testing across all retention email campaigns. Run at least 1 test per week. Achieve a >=20% relative open-rate lift (e.g., 25% baseline open rate -> 30% tested open rate) on emails that have been through the testing process. Build PostHog tracking and a monitoring dashboard.

## Leading Indicators

- PostHog events firing for every email send, open, click, and unsubscribe with test_id and variant properties
- Weekly subject-line performance dashboard showing open-rate trends
- At least 2 of the first 4 tests produce a clear winner (>3pp open-rate lift)
- Subject-line pattern library has 4+ documented results

## Instructions

### 1. Configure email event tracking

Run the `posthog-gtm-events` drill to set up a complete event taxonomy for email subject testing. Implement these events via an n8n workflow that listens to Loops webhooks and forwards to PostHog:

- `email_subject_test_sent` — properties: test_id, variant (A|B), email_id, email_type, subject_line, segment
- `email_subject_test_opened` — properties: test_id, variant, email_id, user_id
- `email_subject_test_clicked` — properties: test_id, variant, email_id, user_id, link_url
- `email_subject_test_unsubscribed` — properties: test_id, variant, email_id, user_id

Build PostHog funnels: sent -> opened -> clicked, filtered by test_id and variant. This gives you per-test conversion data.

### 2. Run weekly subject-line tests

Run the `email-subject-test-pipeline` drill once per week on a different retention email each time. Prioritize emails with:
- Highest send volume (tests need 200+ sends per variant for reliable data)
- Below-average open rate (most room for improvement)
- Direct retention impact (re-engagement, renewal, feature adoption)

Each test follows the pipeline: select email, generate variant, configure split in Loops, instrument PostHog tracking, evaluate after 48 hours, roll out winner.

### 3. Build the performance monitoring dashboard

Run the `email-subject-performance-monitor` drill to create:
- A PostHog dashboard showing open-rate trends across all retention emails
- Weekly automated performance briefs posted to Slack
- Anomaly detection for open-rate drops
- A subject-line pattern library logging every test result

### 4. Apply winning patterns to untested emails

After accumulating 4+ test results, identify which framing categories consistently win for which email types. Apply the winning patterns to emails that have not been tested yet. For example, if personalization consistently beats generic subjects for re-engagement emails, update all re-engagement email subjects to use personalization.

### 5. Evaluate against threshold

Run the `threshold-engine` drill at the end of 2 weeks. Pass criteria: emails that went through subject-line testing show a >=20% relative open-rate lift compared to their pre-test baseline open rates. If PASS, proceed to Scalable. If FAIL, analyze which email types are not responding to testing and focus tests on higher-volume, lower-performing emails.

## Time Estimate

- 4 hours: Set up PostHog event tracking and n8n webhook workflow
- 2 hours: Build PostHog dashboard and anomaly detection
- 8 hours: Run 2 subject-line tests (4 hours each including setup, monitoring, evaluation)
- 2 hours: Document patterns and apply winners to untested emails

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loops | Send A/B test emails, manage sequences | Starter $49/mo for 5,000 contacts, unlimited sends — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Track email events, build funnels and dashboards | Free up to 1M events/mo, 1M feature flag requests/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Webhook listener, event forwarding, weekly cron reports | Self-hosted free; Cloud from ~$24/mo — [n8n.io/pricing](https://n8n.io/pricing) |

**Estimated play-specific cost:** Loops Starter ~$49/mo

## Drills Referenced

- `email-subject-test-pipeline` — runs each individual subject-line A/B test end-to-end
- `posthog-gtm-events` — configures the event taxonomy for email tracking in PostHog
- `email-subject-performance-monitor` — builds the dashboard, anomaly alerts, and weekly performance briefs
- `threshold-engine` — evaluates pass/fail against the 20% relative open-rate lift threshold
