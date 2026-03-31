---
name: in-app-review-request-baseline
description: >
  G2/Capterra Review Requests — Baseline Run. Instrument the full review request
  funnel in PostHog, automate review asks across 3 trigger types via Intercom and
  Loops, and sustain >=10 new reviews per month on G2 and Capterra combined.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=10 new reviews per month across G2 and Capterra combined"
kpis: ["Review ask show-to-click rate", "Review completion rate (click-to-submit)", "Average review rating", "Reviews per month by platform"]
slug: "in-app-review-request"
install: "npx gtm-skills add product/referrals/in-app-review-request"
drills:
  - posthog-gtm-events
  - directory-review-generation
  - nps-feedback-loop
---

# G2/Capterra Review Requests — Baseline Run

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Build always-on review request infrastructure that runs without manual intervention. Instrument the full ask-to-review funnel in PostHog. Deploy review prompts across 3 trigger types (milestone, NPS promoter, post-support) via Intercom in-app messages. Add email follow-up via Loops for users who clicked but did not complete the review. Route asks to both G2 and Capterra. Sustain >=10 new reviews per month across both platforms combined with an average rating of 4.0+.

## Leading Indicators

- PostHog funnel shows complete visibility: ask shown -> clicked -> submitted, with conversion rates at each step by trigger type
- All 3 trigger types are firing automatically (no manual sends required)
- Loops follow-up email reaches users who clicked the review link but did not submit within 48 hours
- G2 and Capterra both receive reviews (not all concentrated on one platform)
- Review candidate pipeline in Attio shows >=4 weeks of eligible users ahead of current ask rate
- NPS survey identifies promoters who are then routed into the review ask flow within 7 days

## Instructions

### 1. Instrument the review request event taxonomy

Run the `posthog-gtm-events` drill to set up comprehensive tracking for the review request lifecycle:

- `review_ask_shown`: prompt displayed. Properties: `trigger_type` (milestone/nps-promoter/support-resolved), `platform_target` (g2/capterra), `user_engagement_score`, `user_tenure_days`, `prompt_variant`
- `review_ask_clicked`: user clicked the review link. Properties: same as above plus `time_to_click_seconds`
- `review_ask_dismissed`: user closed the prompt. Properties: same as above plus `dismiss_action` (close/snooze/never-ask)
- `review_ask_snoozed`: user chose "remind me later." Properties: same as above
- `review_submitted`: new review detected on G2/Capterra. Properties: `platform`, `rating`, `word_count`, `trigger_type_attributed`, `time_from_ask_to_review_hours`
- `review_followup_sent`: Loops email sent to a user who clicked but did not submit. Properties: `platform_target`, `days_since_click`
- `review_followup_clicked`: user clicked the review link in the follow-up email

Build PostHog funnels:
- Primary funnel: `review_ask_shown` -> `review_ask_clicked` -> `review_submitted` (broken down by `trigger_type`)
- Follow-up funnel: `review_followup_sent` -> `review_followup_clicked` -> `review_submitted`
- Platform funnel: `review_submitted` broken down by `platform` (weekly trend)

Create a PostHog dashboard: "Review Request — Baseline" showing all three funnels plus a weekly review count trend.

### 2. Build the automated review ask system across 3 triggers

Run the `directory-review-generation` drill to configure the always-on review ask system. Adapt the drill for in-app delivery (not just email):

**Trigger 1 — Usage milestone:**
Configure an n8n workflow that fires when PostHog detects a milestone event (customize to your product: 100th action, 50th project, 30-day streak). The workflow:
1. Checks Attio: is the user eligible? (engagement score >=60, tenure >30 days, not in review cooldown, has not already reviewed)
2. If eligible: trigger an Intercom in-app message with the review ask
3. Alternate between G2 and Capterra as the target platform (odd-numbered asks go to G2, even to Capterra)
4. Log `review_ask_shown` in PostHog via event API
5. Update Attio: `last_review_ask_date`, increment `review_ask_count`

**Trigger 2 — NPS promoter:**
Run the `nps-feedback-loop` drill to deploy NPS surveys at product milestones via Intercom. When a user scores 9-10 (promoter):
1. Wait 24 hours (do not ask for a review in the same session as the NPS survey)
2. Check eligibility in Attio (same criteria as above)
3. If eligible: show a review ask via Intercom in-app message with copy that references their positive score: "You rated us a {score}/10 — would you share that feedback on {platform}? It helps teams like yours find the right tools."
4. Log events, update Attio

**Trigger 3 — Post-support resolution:**
Configure an n8n workflow triggered by Intercom conversation closure with CSAT 4-5:
1. Wait 48 hours (let the positive support experience settle)
2. Check eligibility in Attio
3. If eligible: trigger review ask via Intercom message referencing the support interaction: "Glad we could help with [topic]. If you have 3 minutes, a review on {platform} would mean a lot."
4. Log events, update Attio

**Cooldown rules (apply to all triggers):**
- Minimum 30 days between review asks per user
- Maximum 3 review asks total per user per year
- If user dismisses with "never ask," mark `review_ask_eligible: false` permanently
- If user snoozes, re-eligible after 60 days

### 3. Add email follow-up for incomplete reviews

Using Loops (from the `directory-review-generation` drill), create a single follow-up email for users who clicked the review link but did not submit a review within 48 hours:

```
Subject: Still thinking about that review?

Hi {first_name},

You clicked to review us on {platform} a couple of days ago — if you still have 3 minutes, here is the link again:

[Leave your review on {platform}] -> {review_url}

Even 2-3 sentences about what you like most helps other teams find us. No worries if reviews are not your thing.

Thanks,
{sender_name}
```

Configure via n8n:
1. After `review_ask_clicked`, start a 48-hour timer
2. Check if `review_submitted` fired for this user in that window
3. If not: trigger the Loops email
4. If review was submitted: cancel the email

### 4. Set up review monitoring on both platforms

Using the `directory-review-monitoring` fundamental from the `directory-review-generation` drill:

- Configure G2 review webhooks to post to your n8n instance when new reviews appear
- Configure Capterra API polling (daily) via n8n cron
- For each new review: match to Attio contact, update `reviewed_platform`, `review_rating`, `review_date`
- Fire `review_submitted` event in PostHog with all properties
- Remove the user from the review ask sequence
- Post new reviews to Slack with rating, platform, and excerpt
- For 4-5 star reviews: flag the user as a case study candidate in Attio
- For 1-2 star reviews: alert CS team immediately

### 5. Evaluate against threshold

After 4 weeks of always-on operation, measure:

- **Pass threshold:** >=10 new reviews per month across G2 and Capterra combined
- **If PASS:** Always-on review generation is working. Proceed to Scalable to add A/B testing, multi-variant prompts, and platform-specific optimization.
- **If FAIL but >=15 clicks/month:** Users are interested but not completing reviews. Investigate: is the G2/Capterra form too long? Add the Loops follow-up if not yet configured. Test linking to a simpler review format.
- **If FAIL and <15 clicks/month:** The prompts are not compelling or the trigger moments are wrong. Check which trigger type has the highest CTR. Double down on the best trigger, retire the worst.
- **If FAIL and <30 asks shown/month:** The eligible user pipeline is too small. Lower the engagement score threshold from 60 to 50, or reduce the cooldown from 30 to 21 days.

## Time Estimate

- 4 hours: PostHog event instrumentation and funnel/dashboard creation
- 4 hours: configure 3 trigger workflows in n8n with Intercom messaging
- 2 hours: NPS survey setup via Intercom (from `nps-feedback-loop` drill)
- 2 hours: Loops follow-up email and 48-hour timer workflow
- 2 hours: G2/Capterra webhook and API monitoring setup in n8n
- 2 hours: 2-week monitoring, evaluation, and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, dashboards, cohorts | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app review prompts, NPS surveys, support CSAT | Starter $29/seat/mo; Proactive Support add-on ~$99/mo ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Follow-up email for incomplete reviews | Starter: free up to 1,000 contacts; $49/mo up to 5,000 ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Trigger workflows, review monitoring, cooldown management | Self-hosted: free; Cloud: from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Candidate pipeline, review tracking, eligibility management | Free tier: 3 seats; Pro: $34/seat/mo ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific cost at this level:** $50-175/mo (Intercom proactive support add-on is the main cost; Loops and n8n Cloud optional)

## Drills Referenced

- `posthog-gtm-events` — establishes the review request event taxonomy and builds funnels/dashboards for full funnel visibility
- `directory-review-generation` — configures the automated review ask system with trigger workflows, platform monitoring, and candidate pipeline management
- `nps-feedback-loop` — deploys NPS surveys to identify promoters who are then routed into the review ask flow
