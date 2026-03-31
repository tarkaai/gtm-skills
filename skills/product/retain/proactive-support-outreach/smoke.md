---
name: proactive-support-outreach-smoke
description: >
  Proactive Support Outreach — Smoke Test. Detect users showing signs of struggle
  and reach out with contextual help before they file a ticket or churn.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Email, Direct"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥40% of outreached users engage with the help"
kpis: ["Outreach engagement rate", "Struggle detection count", "Resolution rate"]
slug: "proactive-support-outreach"
install: "npx gtm-skills add product/retain/proactive-support-outreach"
drills:
  - threshold-engine
---

# Proactive Support Outreach — Smoke Test

> **Stage:** Product → Retain | **Motion:** LeadCaptureSurface | **Channels:** Email, Direct

## Outcomes

Prove that you can detect users struggling with your product and send help that they actually find useful. At this level, the agent identifies struggling users from PostHog data, you manually send contextual help, and you measure whether the help lands.

Success = at least 40% of users you reach out to engage with the help (click the link, reply, watch the video, or take the suggested action).

## Leading Indicators

- Struggle signals appearing in PostHog data (errors, rage clicks, abandoned flows)
- Users responding positively to outreach ("thanks, that fixed it")
- Struggle scores dropping after outreach (user got unstuck)
- No negative reactions (users not marking outreach as spam or complaining about surveillance)

## Instructions

### 1. Instrument struggle signals in PostHog

Run the the struggle signal detection workflow (see instructions below) drill Steps 1-2 only. You are not building the full automated pipeline yet. Instead, manually run the struggle scoring query against your PostHog instance to get a list of users with struggle scores.

Minimum events you need tracked before proceeding:
- `error_displayed` (or your equivalent user-facing error event)
- `$rageclick` (PostHog auto-captures this with session recording enabled)
- `action_abandoned` (or equivalent flow abandonment event)
- `help_docs_visited` (or equivalent help-seeking event)

If any of these events are not tracked, instrument them first. This is the prerequisite for the entire play.

### 2. Manually identify 10-20 struggling users

Run the struggle scoring query from the struggle signal detection workflow (see instructions below) Step 2. Pick 10-20 users with scores above 25 (moderate tier or above). For each user:

1. Review their PostHog session recordings to understand what they were trying to do
2. Identify the specific workflow they are stuck on
3. Note the error messages or failure patterns they encountered
4. Check whether they have an open Intercom support ticket (if yes, skip them — help through the existing ticket instead)

Document each user's struggle context in a simple table: person_id, stuck workflow, failure mode, suggested fix.

### 3. Send contextual help manually

For each identified user, send a brief, specific message through Intercom or email. The message MUST:

- Reference what they were trying to accomplish (not that you saw them struggle)
- Provide the specific fix or next step for their situation
- Include a direct link to the relevant help article or product area
- Be framed as a proactive tip, not a support response

Example: "Quick tip for CSV imports: dates need to be in YYYY-MM-DD format. Here's the full guide: [link]. If you hit any other issues, reply here and I'll help."

Do NOT send: "Hi! We noticed you might be having some trouble. Let us know if we can help!" This is useless.

**Human action required:** Review each message before sending. Ensure the tone is helpful and specific, not creepy or surveillance-like. Send each message manually through Intercom or as a direct email.

### 4. Track responses and resolution

Log each outreach and its outcome:
- Did the user engage? (clicked link, replied, took action)
- Did their struggle resolve? (check PostHog — did the error/abandonment pattern stop?)
- Did they respond positively, neutrally, or negatively?
- How long after outreach did they re-engage with the product?

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure against: ≥40% of outreached users engage with the help. Count as engaged: clicked help link, replied to message, watched video, completed the previously-stuck workflow within 48 hours of outreach.

If PASS: The signal is real — struggling users respond to contextual help. Proceed to Baseline.
If FAIL: Either the struggle detection is picking up false positives, or the help content is not specific enough. Review session recordings of non-responders to understand why.

## Time Estimate

- 1 hour: Verify PostHog events are tracked, run struggle scoring query
- 1.5 hours: Review session recordings for 10-20 users, document struggle context
- 1 hour: Write and send contextual help messages
- 0.5 hours: Track responses over 3-5 days
- 1 hour: Evaluate results and document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Session recordings + event queries for struggle detection | Free tier: 5K sessions/mo; Paid: $0.005/session — https://posthog.com/pricing |

## Drills Referenced

- the struggle signal detection workflow (see instructions below) — Detect and score users showing signs of product struggle (Steps 1-2 only at this level)
- `threshold-engine` — Evaluate pass/fail against the 40% engagement threshold
