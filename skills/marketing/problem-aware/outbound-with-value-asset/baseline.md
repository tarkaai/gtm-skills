---
name: outbound-with-value-asset-baseline
description: >
  Outbound With Value Asset — Baseline Run. Automate the asset-led outbound sequence
  using Instantly with a 3-step cadence, track engagement in PostHog, and validate
  that the play produces consistent replies at 200-500 prospect volume.
stage: "Marketing > ProblemAware"
motion: "OutboundFounderLed"
channels: "Email"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: ">=5 positive replies referencing the asset with >=3% reply rate over 2 weeks"
kpis: ["Asset link click rate", "Reply rate", "Asset-referencing reply rate", "Meeting rate"]
slug: "outbound-with-value-asset"
install: "npx gtm-skills add marketing/problem-aware/outbound-with-value-asset"
drills:
  - posthog-gtm-events
  - cold-email-sequence
---

# Outbound With Value Asset — Baseline Run

> **Stage:** Marketing > ProblemAware | **Motion:** OutboundFounderLed | **Channels:** Email

## Outcomes

Baseline validates that the asset-led outbound works consistently with automation. You move from the founder sending manually to a 3-step email sequence running through Instantly, with proper tracking. The asset is proven from Smoke — now you test whether automation preserves its effectiveness.

**Pass threshold:** >=5 positive replies referencing the asset AND >=3% overall reply rate over 2 weeks, sending to 200-500 prospects.

## Leading Indicators

- Asset link click rate holds at 15%+ (automation did not kill curiosity)
- First positive reply arrives within 3 days of campaign launch
- Reply rate at each sequence step: Email 1 (asset gift) generates 50%+ of total replies
- Negative reply rate stays below 5% of total sends
- At least 1 meeting booked from an asset-referencing reply

## Instructions

### 1. Set up the automated outreach sequence

Run the the value asset outreach sequence workflow (see instructions below) drill. This creates a 3-step email sequence in Instantly:

- **Email 1 (Day 0):** Gift the asset. No pitch, no meeting ask. Just the asset link with a personalized intro.
- **Email 2 (Day 4-5):** Follow up with a specific insight from the asset relevant to the prospect's situation.
- **Email 3 (Day 9-10):** Make the offer. Connect the asset's topic to your product. Include Cal.com booking link.

Configure Clay personalization variables: `personalization_line`, `pain_category`, and `asset_hook`. Map these to Instantly merge fields.

### 2. Warm up and configure sending infrastructure

Using the `cold-email-sequence` drill's sending setup steps:

- Verify all sending accounts have completed 2+ weeks of warmup via `instantly-warmup`
- Confirm SPF, DKIM, and DMARC records are configured
- Set daily send limits to 20-30 per account (founder-level volume, not SDR volume)
- Schedule sends for weekdays, 7:00am-9:30am in prospect timezone
- Disable open tracking; enable link tracking for the asset URL only

### 3. Configure event tracking

Run the `posthog-gtm-events` drill to establish the event taxonomy for this play. Implement these events:

- `value_asset_email_sent` — properties: step (1/2/3), prospect_id, campaign_id, asset_version
- `value_asset_link_clicked` — properties: asset_url, prospect_id
- `value_asset_reply_received` — properties: sentiment (positive/negative/neutral), references_asset (boolean), sequence_step
- `value_asset_meeting_booked` — properties: prospect_id, source_step

Connect Instantly webhooks to PostHog via n8n to fire events automatically. Connect reply detection to Attio to tag prospects: `asset-reply-positive`, `asset-engaged`, `opted-out`.

### 4. Load prospects and launch

Import 200-500 enriched prospects from your Clay table into Instantly. Verify:
- All personalization variables render correctly (spot-check 10 emails)
- The asset link works and loads in under 3 seconds
- Reply detection rules route positive, negative, and OOO replies correctly

Launch the campaign. Monitor daily for the first 3 days:
- Check deliverability (bounce rate should be <3%)
- Verify reply routing is working (test with a self-send)
- Confirm PostHog events are flowing

### 5. Monitor for 2 weeks and evaluate

Track the funnel daily in PostHog. After 2 weeks:

- Pull total sends, asset clicks, replies by sentiment, and meetings booked
- Calculate: reply rate (total positive replies / total sends), asset click rate (clicks / sends), asset-referencing reply rate (referencing replies / sends)
- Compare Email 1 vs Email 2 vs Email 3 reply contributions

Run the `threshold-engine` evaluation: >=5 positive replies referencing the asset AND >=3% reply rate.

**If PASS:** The automated sequence preserves the asset's effectiveness. Proceed to Scalable to add A/B testing, multi-segment assets, and higher volume.

**If FAIL:** Diagnose by funnel step:
- Low click rate on Email 1: Subject line or first line is not compelling. The personalization is weak.
- Clicks but no replies: The asset delivers value but does not prompt engagement. The Email 2 insight may be too generic.
- Replies on Email 1-2 but drop-off on Email 3: The transition from "helpful" to "pitch" is too abrupt. Soften Email 3 or add a step.
- High negative reply rate: Targeting is off. Tighten ICP or review if the asset topic resonates with this audience.

## Time Estimate

- Outreach sequence setup and Clay variables: 3 hours
- Sending infrastructure warmup verification: 1 hour
- PostHog event tracking configuration: 2 hours
- Prospect loading and campaign launch: 1.5 hours
- Daily monitoring (15 min/day x 10 days): 2.5 hours
- Evaluation and analysis: 2 hours
- **Total: ~12 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Cold email sequences with warmup | Growth: $30/mo annual ($37/mo monthly) — 5,000 emails, 1,000 leads ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Clay | Prospect enrichment and personalization | Launch: $185/mo — 2,500 credits, 15,000 actions ([clay.com/pricing](https://www.clay.com/pricing)) |
| Attio | CRM tracking and reply routing | Plus: $29/user/mo — enhanced email, no seat limits ([attio.com](https://attio.com)) |
| PostHog | Event tracking and funnel analysis | Free: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Workflow automation (Instantly->PostHog->Attio) | Starter: ~$24/mo (2,500 executions) ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated monthly cost: ~$270-300/mo** (Instantly Growth + Clay Launch + Attio Plus + n8n Starter)

## Drills Referenced

- the value asset outreach sequence workflow (see instructions below) — build and configure the 3-step asset-led email sequence
- `posthog-gtm-events` — set up event tracking for the full outreach funnel
- `cold-email-sequence` — sending infrastructure setup and warmup verification
