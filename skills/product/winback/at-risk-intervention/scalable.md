---
name: at-risk-intervention-scalable
description: >
  At-Risk User Intervention — Scalable Automation. Scale intervention to the full user base
  with segmented messaging, multi-channel sequencing, A/B tested copy, and automated
  channel rotation for non-responders.
stage: "Product > Winback"
motion: "LeadCaptureSurface"
channels: "Email, Product, Direct"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: "≥35% response rate AND ≥25% save rate at 500+ at-risk users/month"
kpis: ["Response rate", "Save rate", "Save rate by segment", "Channel efficiency", "Intervention reach"]
slug: "at-risk-intervention"
install: "npx gtm-skills add product/winback/at-risk-intervention"
drills:
  - ab-test-orchestrator
  - churn-prevention
  - churn-risk-scoring
---

# At-Risk User Intervention — Scalable Automation

> **Stage:** Product > Winback | **Motion:** LeadCaptureSurface | **Channels:** Email, Product, Direct

## Outcomes

Scale the Baseline intervention system to handle the full at-risk population without proportional effort increase. Add segmented messaging variants, multi-channel sequencing (if the first channel gets no response, try the next), A/B testing of intervention copy and timing, and automated channel rotation. The system should handle 500+ at-risk users per month with the same or better save rate as Baseline.

Pass threshold: **≥35% response rate AND ≥25% save rate at 500+ at-risk users processed per month**, sustained over 4 weeks.

## Leading Indicators

- Multi-channel sequences deliver interventions across 2+ channels per non-responding user
- A/B test results show statistically significant differences between message variants
- Save rate holds steady as the at-risk population scales (no degradation from volume)
- Channel rotation recovers users who ignored the first intervention channel

## Instructions

### 1. Segment the at-risk population

Extend the `churn-risk-scoring` drill's output with segmentation. Using PostHog cohorts, classify at-risk users by:

- **Usage pattern before decline:** Power users (daily, multi-feature) vs. light users (weekly, single-feature) vs. team admins vs. individual contributors
- **Churn signal type:** Usage decline (doing less) vs. feature abandonment (stopped a specific workflow) vs. billing signals (exploring cancellation) vs. team signals (removing members)
- **Account value:** High MRR vs. mid-tier vs. free/trial
- **Tenure:** First 30 days vs. 30-90 days vs. 90+ days

Store segment assignments as PostHog user properties so intervention triggers can use them.

### 2. Build segment-specific intervention variants

Extend the `churn-prevention` drill to create different message variants per segment:

- **Power users with usage decline:** "We noticed [specific feature] usage dropped. Here's what [similar company] does with it — [link to case study or template]." Tone: peer-level, value-focused. Channel: in-app first, then email.
- **Light users with feature abandonment:** "Most teams using [product] get the most value from [feature the user hasn't tried]. Here's a 2-minute setup guide." Tone: educational, low-pressure. Channel: email first (they're not in the app).
- **Billing signal users:** "Before you go — want to chat about what would make [product] worth it? 15 minutes, no pressure." Tone: direct, honest. Channel: email with calendar link, then personal if high-value.
- **Team signal users:** Route to personal outreach regardless of value. Team shrinkage is a high-confidence churn predictor. Include team usage data in the outreach brief.

Write 2 variants per segment for A/B testing (step 3).

### 3. Launch A/B tests on intervention messaging

Run the `ab-test-orchestrator` drill to test intervention variants. For each segment:

1. Create a PostHog feature flag that splits at-risk users in that segment between variant A and variant B
2. Variant A = current best-performing message from Baseline. Variant B = new variant written in step 2.
3. Primary metric: save rate (risk tier improved to low within 14 days)
4. Secondary metrics: response rate, time-to-response, 30-day retention of saved users
5. Run each test until 100+ users per variant or 3 weeks, whichever comes first
6. Adopt the winner, write a new challenger, repeat

Run tests sequentially (one segment at a time) to avoid interaction effects.

### 4. Build multi-channel intervention sequences

Extend the n8n intervention workflows to implement channel sequencing for non-responders:

- **Day 0:** Primary channel fires based on segment assignment (in-app or email)
- **Day 3 (if no engagement):** Secondary channel fires. If primary was in-app, send email. If primary was email, show in-app message.
- **Day 7 (if still no engagement AND high/critical risk):** Escalate to personal outreach via Attio task. Include both previous attempts and the user's specific risk data.
- **Day 14 (if no engagement across all channels):** Mark as "intervention exhausted." Do not re-intervene for 30 days. Log as `intervention_exhausted` event in PostHog.

Set a global cap: no user receives more than 4 intervention touches in a 30-day window.

### 5. Automate channel efficiency analysis

Build a weekly n8n workflow that calculates save rate and cost per save by channel:

1. Query PostHog for all `intervention_sent` and `intervention_saved` events in the past 7 days
2. Group by channel and segment
3. Calculate: response rate, save rate, median time-to-response, and cost per save (Intercom message cost + Loops email cost + estimated time cost for personal outreach)
4. If any channel's save rate drops below 15%, flag it for review — the channel may need message refresh or the segment assignment may be wrong
5. Store the analysis in Attio on the play's campaign record

### 6. Evaluate against threshold

After 4 weeks at scale, measure against the pass threshold:

- **Pass (≥35% response rate AND ≥25% save rate at 500+ users/month):** The system scales. Proceed to Durable.
- **Marginal (30-35% response at scale):** Check if degradation is from volume (too many generic messages) or segment (one segment dragging the average down). Fix the weak segment and re-measure.
- **Fail (<30% response at scale):** Scale back to Baseline volumes. Test whether the scoring model is producing too many false positives at higher volumes.

## Time Estimate

- 8 hours: Segment analysis and variant copywriting
- 10 hours: Build multi-channel sequencing workflows in n8n
- 8 hours: Set up A/B tests in PostHog
- 8 hours: Build channel efficiency analysis workflow
- 8 hours: Monitor, analyze test results, iterate on variants
- 8 hours: Evaluate and document winning configurations

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Cohorts, experiments, feature flags, event tracking | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app intervention messages, multi-channel sequences | $85/seat/mo Advanced (recommended for targeting rules); +$99/mo Proactive Support — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Triggered intervention emails at scale | $49/mo+ based on contact volume — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Multi-channel sequencing, scoring, analysis workflows | Self-hosted free; Cloud from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |

**Play-specific cost at Scalable:** ~$150-300/mo (Intercom Advanced + Proactive Support + Loops scaled tier)

## Drills Referenced

- `ab-test-orchestrator` — A/B test intervention message variants per segment with statistical rigor
- `churn-prevention` — extended with segment-specific message variants and multi-channel sequences
- `churn-risk-scoring` — extended with user segmentation for targeted interventions
