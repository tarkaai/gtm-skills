---
name: email-reengagement-inactive-baseline
description: >
  Inactive User Re-engagement — Baseline Run. Automate a 3-email reengagement
  sequence in Loops triggered by PostHog inactivity cohorts. First always-on
  automation. Prove the sequence sustains >=20% return rate over 2 weeks.
stage: "Product > Winback"
motion: "LeadCaptureSurface"
channels: "Email, Product"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: ">=20% return rate AND >=8% reactivation rate over 2 weeks"
kpis: ["Email open rate per step", "Click-through rate per step", "7-day return rate", "14-day reactivation rate", "Unsubscribe rate"]
slug: "email-reengagement-inactive"
install: "npx gtm-skills add product/winback/email-reengagement-inactive"
drills:
  - posthog-gtm-events
  - winback-campaign
  - onboarding-sequence-automation
---

# Inactive User Re-engagement — Baseline Run

> **Stage:** Product > Winback | **Motion:** LeadCaptureSurface | **Channels:** Email, Product

## Outcomes

An always-on 3-email reengagement sequence runs automatically whenever a user crosses the inactivity threshold. The sequence achieves >=20% return rate and >=8% reactivation rate (returned users who complete a meaningful product action) sustained over 2 weeks. This proves the approach works continuously, not just as a one-shot.

## Leading Indicators

- Sequence entry rate matches inactivity cohort growth (no sync gaps between PostHog and Loops)
- Email open rate >=25% on Email 1 (first 48 hours after send)
- Click-through rate >=4% on at least one email step
- Unsubscribe rate below 0.5% per email step
- At least 1 returned user per day by the end of week 1

## Instructions

### 1. Set up the reengagement event taxonomy

Run the `posthog-gtm-events` drill to define the full event set for reengagement tracking:

- `reengagement_qualified` — user crossed the inactivity threshold (14 days no login, was previously active). Properties: `user_id`, `email`, `days_inactive`, `last_active_date`, `most_used_feature`, `plan_type`.
- `reengagement_sequence_entered` — user was added to the Loops reengagement sequence. Properties: `user_id`, `sequence_id`, `cohort` (14-30d, 30-60d).
- `reengagement_email_sent` — each email step sent. Properties: `user_id`, `step_number`, `subject_line`, `cohort`.
- `reengagement_email_opened` — email opened. Properties: `user_id`, `step_number`.
- `reengagement_email_clicked` — CTA clicked. Properties: `user_id`, `step_number`, `cta_url`.
- `reengagement_user_returned` — user logged in after being in a sequence. Properties: `user_id`, `days_to_return`, `returning_step` (which email they were on when they returned).
- `reengagement_user_reactivated` — returned user completed a meaningful product action within 14 days. Properties: `user_id`, `action_name`, `days_to_reactivate`.

Build PostHog funnels:
- Full funnel: `qualified` -> `sequence_entered` -> `email_opened` (any) -> `email_clicked` (any) -> `user_returned` -> `user_reactivated`
- Per-step funnels: `email_sent (step N)` -> `email_opened (step N)` -> `email_clicked (step N)` for each of 3 steps

### 2. Build the reengagement sequence

Run the `winback-campaign` drill to design the 3-email sequence segmented by inactivity duration:

**For 14-30 day inactive users (recent lapse):**
- Email 1 (day 0 of sequence): "What you missed" — highlight 2-3 product updates or new features since their last login. CTA: deep-link to their most-used feature.
- Email 2 (day 3): Social proof — share a specific result from a user in their segment. "Users like you are getting [outcome] with [feature]." CTA: link to a relevant case study or feature page.
- Email 3 (day 7): Direct ask — "Is [Product] still right for you?" Include a 1-click survey: (a) I'm coming back, (b) I switched to something else, (c) I don't need this anymore. CTA for option (a): deep-link to product. Replies from (b) and (c) feed into product intelligence.

**For 30-60 day inactive users (extended lapse):**
- Email 1 (day 0): Re-introduce the product. Assume they have forgotten the value. Lead with the single biggest improvement since they left. CTA: "See what's new" landing page.
- Email 2 (day 4): Offer a personal walkthrough or screen share. "We'd love 15 minutes to show you what's changed." CTA: Cal.com booking link.
- Email 3 (day 10): Final attempt with an incentive. Offer an extended trial of a paid feature, a data export if they want to leave cleanly, or a personal note from the founder. CTA: reactivate or export.

Using `loops-sequences`, build both sequences in Loops with the content, timing, and conditional branches defined above. Set exit conditions: user returns (logs in) at any point exits the sequence.

### 3. Wire the automation

Using `n8n-triggers`, create a workflow that:
1. Runs daily: queries PostHog for users who crossed the 14-day inactivity threshold today
2. Enriches each user with their `most_used_feature` and `plan_type` from PostHog person properties
3. Assigns users to the correct sequence variant based on `days_inactive` (14-30 or 30-60)
4. Pushes users to Loops via the `loops-audience` fundamental with the appropriate contact properties
5. Triggers the correct Loops sequence

**Human action required:** Review the first 10 users who enter the sequence. Verify the personalization variables render correctly in Loops and that the deep-links point to the right product pages. Approve for continuous operation.

### 4. Monitor delivery and early signals

Check daily for the first week:
- Are users entering the sequence? (compare `reengagement_qualified` count vs `reengagement_sequence_entered` count)
- Are emails being delivered? (check Loops delivery stats)
- What is the open rate on Email 1? (should be >25% within 48 hours)
- Any unsubscribes above 0.3% per step? (if so, review subject line and frequency)

### 5. Evaluate against threshold

After 2 weeks of always-on operation, measure:
- Primary: 7-day return rate >=20% across both cohorts combined
- Primary: 14-day reactivation rate >=8% (returned users who did something meaningful)
- Secondary: open rate, click rate, unsubscribe rate per step per cohort

If PASS: document the winning sequence, note which cohort and step performed best. Proceed to Scalable.
If FAIL: diagnose per-step performance. If Email 1 open rate is low, test new subject lines. If click rate is low, revise CTAs. If returns happen but reactivation is low, the product re-entry experience needs work (add an Intercom welcome-back message). Stay at Baseline and re-evaluate after another 2-week cycle.

## Time Estimate

- 3 hours: Set up PostHog event taxonomy and funnels
- 4 hours: Design and build the 2 sequence variants in Loops
- 2 hours: Build the n8n automation workflow and test
- 1 hour: Human review of first batch
- 2 hours (after 2 weeks): Pull results, analyze per-step performance, document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Cohort detection, event tracking, funnel analysis | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Automated reengagement sequences (2 variants, 3 steps each) | $49/mo for up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Daily cohort detection workflow, PostHog-to-Loops sync | Self-hosted free; Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated play-specific cost:** $49-73/mo (Loops + n8n Cloud)

## Drills Referenced

- `posthog-gtm-events` — define the reengagement event taxonomy and build PostHog funnels for per-step tracking
- `winback-campaign` — design the 3-email sequence content, timing, and segmentation by inactivity cohort
- `onboarding-sequence-automation` — wire the Loops sequences to n8n triggers so the system runs always-on
