---
name: feature-spotlight-series-baseline
description: >
  Weekly Feature Spotlights — Baseline Run. Establish the spotlight as a recurring weekly series
  with structured event tracking, a content pipeline, and adoption measurement to prove the
  format holds over time.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 4 weeks"
outcome: "≥30% trial rate and ≥10% 7-day adoption rate sustained across 4 consecutive spotlights"
kpis: ["Per-spotlight trial rate", "7-day adoption rate", "Series engagement trend", "Feature coverage"]
slug: "feature-spotlight-series"
install: "npx gtm-skills add product/retain/feature-spotlight-series"
drills:
  - posthog-gtm-events
  - feature-adoption-monitor
---

# Weekly Feature Spotlights — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Trial rate of 30% or more and 7-day adoption rate of 10% or more, sustained across 4 consecutive weekly spotlights. This proves the spotlight format works as a recurring series — not just a one-shot message — and that the pipeline can identify features, produce content, deliver it, and drive sustained adoption week after week.

## Leading Indicators

- Weekly spotlight shipped on schedule (the pipeline is operational)
- Open rate stable or improving across the 4 spotlights (no engagement decay)
- Different features spotlighted each week with distinct target cohorts (the selection engine works)
- Users who tried a feature via spotlight still using it 7+ days later (adoption sticks)
- Drop-off funnel consistent: if the weakest step is always the same, you know what to fix

## Instructions

### 1. Instrument the full event taxonomy

Run the `posthog-gtm-events` drill to establish the spotlight series event tracking in PostHog. Define and instrument these events:

| Event | Trigger | Key Properties |
|-------|---------|---------------|
| `spotlight_delivered` | Spotlight shown in-app or email sent | `feature`, `channel` (email/in-app), `cohort_id`, `spotlight_week` |
| `spotlight_opened` | Email opened or in-app message rendered | `feature`, `channel` |
| `spotlight_clicked` | User clicks the CTA | `feature`, `channel` |
| `spotlight_feature_tried` | User performs the feature's core action for the first time | `feature`, `source` (spotlight) |
| `spotlight_feature_adopted` | User performs the feature action again 7+ days after first try | `feature`, `source` (spotlight) |

Build PostHog funnels:
- **Per-spotlight funnel**: `spotlight_delivered` -> `spotlight_opened` -> `spotlight_clicked` -> `spotlight_feature_tried` -> `spotlight_feature_adopted`
- **Channel comparison funnel**: Same funnel, broken down by `channel` property
- **Series trend**: Trial rate and adoption rate by `spotlight_week`, plotted as a line chart

### 2. Launch the weekly content pipeline

Run the the spotlight content pipeline workflow (see instructions below) drill to establish the recurring production and delivery system:

**Week 1 setup:**
1. Build the feature usage matrix in PostHog — query adoption rates for every trackable feature
2. Score and prioritize features by: low adoption + high retention correlation + sufficient target audience
3. Create the Spotlight Calendar in Attio with the next 4 features queued
4. Build the n8n workflow for the weekly cadence: Monday auto-select, Monday human review, Tuesday deliver

**Each subsequent week the pipeline runs:**
1. n8n queries PostHog for the feature usage matrix and selects the next feature
2. Agent drafts the spotlight content: benefit-led headline, 150-word body, screenshot/GIF, deep link
3. **Human action required:** Review and approve the feature selection, content, and targeting before delivery
4. n8n deploys the in-app message via Intercom and sends the email via Loops
5. The following Monday, n8n pulls 7-day results and logs them in Attio

Target the full eligible audience for each spotlight (not the 30-50 user Smoke group). For each feature, the audience is: active users who have not used this feature in the last 60 days.

### 3. Monitor per-feature adoption

Run the `feature-adoption-monitor` drill to track what happens after each spotlight:

- Build a per-feature adoption funnel: spotlight delivered -> tried -> adopted (used again 7+ days later)
- Track stalled users: users who clicked the spotlight but did not complete the feature action. These users expressed interest but hit friction. Configure a follow-up nudge via Intercom 48 hours after click with a more specific how-to or example.
- Log per-spotlight results in the Spotlight Calendar in Attio: feature, audience size, delivered count, open rate, CTR, trial rate, adoption rate

After 4 weeks, you have 4 data points showing whether the series format holds:
- Is trial rate consistently above 30%?
- Is adoption rate consistently above 10%?
- Is engagement trending stable or improving (not declining)?
- Are different features responding to the spotlight format?

### 4. Evaluate against threshold

Measure the 4-week results:

- **Pass (trial ≥30% AND adoption ≥10% for all 4 spotlights):** The series works as a recurring format. Proceed to Scalable to find the 10x multiplier through testing and automation.
- **Marginal pass (3 of 4 spotlights hit threshold):** Diagnose the underperformer. Was it the feature choice, the content, the audience, or the timing? Fix and run one more week to confirm.
- **Fail (<3 spotlights hit threshold):** Identify the pattern. Are all spotlights failing at the same funnel step? If delivery is fine but clicks are low, the content format needs work. If clicks are fine but trial is low, the features chosen have UX friction. If trial is fine but adoption is low, the features are interesting but not sticky. Fix the systemic issue and re-run 4 weeks.

## Time Estimate

- 4 hours: Event taxonomy setup, PostHog funnels, n8n weekly workflow configuration
- 2 hours: Feature usage matrix build, Spotlight Calendar creation, first 4 features queued
- 8 hours: Four weekly cycles of content production, review, delivery, and monitoring (2 hours/week)
- 2 hours: 4-week analysis, threshold evaluation, and series performance review

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts, feature usage analysis | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app spotlight delivery and follow-up nudges | Included in existing plan — https://www.intercom.com/pricing |
| Loops | Email spotlight delivery | Free up to 1,000 contacts; Starter $49/mo — https://loops.so/pricing |
| n8n | Weekly pipeline automation and scheduling | Free self-hosted; Cloud from $24/mo — https://n8n.io/pricing |
| Attio | Spotlight Calendar, per-feature results logging | From $0/mo (free tier) — https://attio.com/pricing |

**Play-specific cost:** ~$25-75/mo (Loops Starter if >1,000 contacts + n8n Cloud if not self-hosted)

## Drills Referenced

- `posthog-gtm-events` — establish the full spotlight event taxonomy and build conversion funnels
- the spotlight content pipeline workflow (see instructions below) — the weekly system for selecting features, producing content, and delivering spotlights
- `feature-adoption-monitor` — track per-feature adoption, detect stalled users, and measure spotlight impact
