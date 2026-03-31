---
name: breakup-reengagement-monitor
description: Track breakup email re-engagement rates, message fatigue decay, and signal-to-reply attribution over time
category: Measurement
tools:
  - PostHog
  - n8n
  - Attio
  - Instantly
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-reporting
  - instantly-tracking
---

# Breakup Re-engagement Monitor

This drill builds the monitoring layer specific to breakup email sequences. Breakup emails have unique dynamics that general email dashboards miss: the prospect pool is finite (only prospects who completed a prior sequence), message fatigue decays differently (you cannot keep sending breakups to the same people), and the signal-vs-no-signal segmentation produces different performance curves.

## Prerequisites

- Breakup email campaigns running in Instantly with PostHog event tracking configured
- At least 4 weeks of breakup send data
- Attio records tagged with breakup sequence metadata
- n8n instance for scheduled reporting

## Steps

### 1. Define breakup-specific metrics

Standard email metrics (open rate, reply rate) are insufficient for breakup sequences. Track these breakup-specific metrics:

- **Re-engagement rate:** Positive replies / breakup emails sent. This is the primary metric. A "positive reply" means the prospect expressed interest, asked a question, or requested the low-friction asset — not just an auto-reply or "remove me."
- **Signal lift:** Re-engagement rate for signal-detected prospects vs. no-signal prospects. Measures whether signal-based personalization justifies the enrichment cost.
- **Latent interest ratio:** Prospects who replied to the breakup but NOT to any prior sequence email. These are people the breakup uniquely recovered — the play's core value.
- **Asset conversion rate:** Of prospects who replied "send it" to Email 2, how many booked a meeting within 14 days? Measures whether the low-friction asset actually converts.
- **Pool depletion rate:** How quickly you are exhausting the available silent-prospect pool. If you send 200 breakups/month and only 100 new prospects go silent/month, the pool shrinks and the play has a natural ceiling.
- **Fatigue decay curve:** Reply rate over successive breakup campaigns to the same ICP segment. Breakup messaging decays faster than cold email because prospects in the same network talk ("everyone is getting these breakup emails from Company X").

### 2. Build the PostHog dashboard

Using the `posthog-dashboards` fundamental, create a dashboard named "Breakup Email Sequences — Performance":

**Panel 1 — Weekly re-engagement rate trend:**
- Line chart, 12-week rolling window
- Series 1: Signal-detected re-engagement rate
- Series 2: No-signal re-engagement rate
- Series 3: Blended re-engagement rate
- Reference line at the Scalable-level pass threshold

**Panel 2 — Funnel: Breakup to meeting:**
- Funnel chart: `breakup_sent` -> `breakup_opened` -> `breakup_replied_positive` -> `asset_requested` -> `meeting_booked`
- Segmented by signal vs. no-signal

**Panel 3 — Pool health:**
- Stacked area chart showing: total silent prospects available, breakups sent this period, prospects re-engaged, prospects permanently exhausted (sent breakup, no reply, will not be contacted again)
- This shows the play's sustainability ceiling

**Panel 4 — Message variant performance:**
- Table: each breakup email variant (subject line + body angle) with send count, open rate, reply rate, and days active
- Sorted by reply rate descending
- Highlight variants where reply rate dropped >30% from peak (fatigue signal)

**Panel 5 — Signal type attribution:**
- Bar chart: re-engagement rate broken down by signal type (job change, funding, hiring, content engagement, no signal)
- Shows which signals are worth detecting

**Panel 6 — Cost efficiency:**
- Line chart: cost per re-engaged prospect over time (Clay enrichment + Instantly sends / positive replies)
- Compare to cost per cold lead from initial outbound

### 3. Configure automated alerts

Using the `n8n-scheduling` fundamental, create alert workflows:

- **Re-engagement rate drop:** If blended rate falls below 70% of the 4-week average for 2 consecutive weeks, trigger a review. Send Slack notification with the specific decline and which segment (signal vs. no-signal) is responsible.
- **Pool depletion warning:** If available silent prospects drops below 2 months of send volume at current rates, alert that the play needs fresh prospect inflow or volume reduction.
- **Variant fatigue trigger:** If any variant's reply rate drops below 50% of its peak over a 30-day window, flag it for rotation or retirement.
- **Bounce/complaint spike:** If bounce rate exceeds 2% or unsubscribe rate exceeds 0.5% on any breakup campaign, pause the campaign and alert.

### 4. Build the weekly breakup performance report

Using the `n8n-workflow-basics` fundamental, create an n8n workflow that runs every Friday:

1. Pull the last 7 days of breakup events from PostHog
2. Calculate: breakups sent, re-engagement rate (blended and by segment), meetings booked from breakup replies, pool size remaining, active variant performance
3. Compare to prior 4-week average and to the Scalable baseline
4. Generate a one-paragraph summary: "This week: [X] breakups sent, [Y]% re-engagement rate ([up/down] from [Z]% average). [N] meetings booked. Signal-detected prospects converted at [A]% vs [B]% for no-signal. Pool health: [C] months of prospects remaining at current volume."
5. Append actionable recommendation: "Continue as-is" / "Rotate variant [X] — reply rate decayed" / "Reduce volume — pool depleting faster than inflow" / "Increase signal-detection coverage — signal lift is [X]x"
6. Post to Slack and log in Attio

### 5. Track attribution through the pipeline

Use the `attio-reporting` fundamental to track breakup-originated deals separately:

- Tag every deal created from a breakup reply with `source: breakup-email-sequences` and `breakup_variant: [variant ID]`
- Track these deals through the pipeline: meeting -> proposal -> closed-won/lost
- Calculate breakup-specific metrics: average deal size from breakup-recovered prospects, close rate, and time-to-close compared to fresh outbound prospects
- This data feeds back into the `autonomous-optimization` drill to determine whether the play is worth continued investment

## Output

- PostHog dashboard with 6 breakup-specific panels
- n8n alert workflows for re-engagement drops, pool depletion, variant fatigue, and compliance
- Weekly automated performance report delivered to Slack
- Pipeline attribution for breakup-originated deals in Attio
