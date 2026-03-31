---
name: winback-campaign-scalable
description: >
  Churned User Win-back — Scalable Automation. Scale winback to the full churned
  population with A/B tested offers, multi-channel sequencing (email + in-app + personal),
  automated segment expansion, and cohort-level retention tracking.
stage: "Product > Winback"
motion: "LeadCaptureSurface"
channels: "Email, Product"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: "≥12% reactivation rate at 500+ churned users processed per month"
kpis: ["Reactivation rate", "Reactivation rate by segment", "30-day retention of reactivated users", "Cost per reactivation", "Rechurn rate"]
slug: "winback-campaign"
install: "npx gtm-skills add product/winback/winback-campaign"
drills:
  - ab-test-orchestrator
  - winback-campaign
---

# Churned User Win-back — Scalable Automation

> **Stage:** Product > Winback | **Motion:** LeadCaptureSurface | **Channels:** Email, Product

## Outcomes

Scale the Baseline winback system to handle the full churned population without proportional effort increase. Add A/B testing of offers and messaging, multi-channel sequencing for non-responders, recency-based timing optimization, and automated retirement of underperforming segments. The system should process 500+ churned users per month with reactivation rates equal to or better than Baseline.

Pass threshold: **≥12% reactivation rate at 500+ churned users processed per month**, sustained over 4 consecutive weeks.

Note: The threshold drops from 15% (Baseline) to 12% at scale. This is intentional — at higher volume you are reaching further into the churned population (older churns, weaker signals), which naturally dilutes the rate. The absolute number of reactivations increases significantly.

## Leading Indicators

- A/B test results show statistically significant differences between offer variants
- Multi-channel sequences recover at least 20% of users who ignored the first email
- Segment-specific reactivation rates are stable as volume scales (no degradation from dilution)
- 30-day retention of reactivated users remains above 60%
- Cost per reactivation stays below 3x the cost of acquiring a new user

## Instructions

### 1. Launch A/B tests on winback offers and messaging

Run the `ab-test-orchestrator` drill to test variations of the winback experience. Test one variable at a time per segment:

**Round 1 — Offer type (4 weeks):**
For price churners: test discount (20% for 2 months) vs. plan downgrade (lower tier at reduced price) vs. extended trial (30 days free).
For feature churners: test "feature shipped" announcement vs. "feature shipped + free trial" vs. "feature shipped + personal walkthrough."
For inactive churners: test re-education email vs. case study vs. new onboarding flow invitation.

**Round 2 — Timing (4 weeks):**
Test when the first email fires: 14 days post-churn vs. 30 days vs. 45 days. Hypothesis: fresher churns respond better but may not have had time to miss the product.

**Round 3 — Subject line and sender (4 weeks):**
Test founder name vs. product name as sender. Test specific subject ("We built the feature you asked for") vs. curiosity subject ("Something changed since you left") vs. direct subject ("Come back — 30 days free").

For each test:
1. Create a PostHog feature flag splitting the segment 50/50
2. Run until 100+ users per variant or 3 weeks, whichever is first
3. Primary metric: reactivation rate. Secondary: 30-day retention, rechurn rate.
4. Adopt the winner, design a new challenger, repeat.

### 2. Build multi-channel winback sequences

Extend the Baseline email-only sequences with channel escalation for non-responders. Using the `winback-campaign` drill's multi-channel approach:

- **Day 0 (30 days post-churn):** Winback Email 1 fires via Loops (segment-specific, validated copy from Baseline A/B tests)
- **Day 7 (if no email engagement):** In-app message via Intercom if the user visits the site. Show a banner with the same offer but different framing.
- **Day 14 (if no engagement on email or in-app):** Winback Email 2 with social proof
- **Day 21 (if still no engagement):** Winback Email 3 with direct offer and expiration
- **Day 30 (if no engagement AND user is High Value):** Escalate to personal outreach via Attio task. Include all previous attempts and the user's churn data.
- **Day 45 (if no engagement across all channels):** Mark as "winback exhausted." Do not re-contact for 90 days. Log `winback_exhausted` event in PostHog.

Global cap: No churned user receives more than 5 winback touches in a 90-day window.

### 3. Expand and refine segments

Run the the winback offer personalization workflow (see instructions below) drill monthly to:

1. Enroll newly churned users into the appropriate segment
2. Re-evaluate stale segments: move users from "fresh" to "mid" to "stale" as time passes
3. Retire segments with <3% reactivation rate over 8+ weeks. Stop spending resources on them.
4. Create new micro-segments if data reveals a pattern. Example: if "inactive churners who used feature X" reactivate at 2x the rate of other inactive churners, split them into their own segment with tailored messaging.
5. Update offers based on product changes: if you shipped a new feature, check if any "missing feature" churners requested it and move them to a fresh outreach queue.

### 4. Track reactivated user quality

Reactivation without retention is wasted effort. Build these measurements:

- **30-day retention cohort:** What percentage of reactivated users are still active 30 days later? Segment by churn reason and offer type.
- **Rechurn rate:** What percentage of reactivated users churn again within 90 days? If >40%, the offers are attracting deal-seekers, not genuinely re-engaged users. Diagnose by offer type — discounts may drive high rechurn while feature announcements drive low rechurn.
- **Reactivated LTV:** Compare the 6-month LTV of reactivated users to the LTV of never-churned users. If reactivated LTV is <50% of normal LTV, the winback is recovering low-quality revenue.
- **Cost per reactivation:** (Email cost + Intercom cost + personal outreach time) / reactivations. Compare to customer acquisition cost (CAC). If cost per reactivation exceeds CAC, winback is less efficient than acquiring new customers.

### 5. Automate segment performance reporting

Build a weekly n8n workflow that:

1. Queries PostHog for all winback events in the past 7 days
2. Calculates reactivation rate, open rate, click rate, and cost per reactivation by segment
3. Flags segments that are underperforming (below 5% reactivation) or overperforming (above 20%)
4. Stores the report in Attio and sends a summary to the team
5. Automatically pauses sequences for segments that have been below 3% for 4+ consecutive weeks

### 6. Evaluate against threshold

After 4 weeks at scale, measure against the pass threshold:

- **Pass (≥12% reactivation at 500+ users/month):** The system scales. Note which segments, offers, and channels drive the most reactivations. Proceed to Durable.
- **Marginal (8-12% reactivation at scale):** Identify the weakest segment and either improve its messaging or retire it. Check if multi-channel sequences are adding incremental reactivations. Re-measure after 2 more weeks.
- **Fail (<8% reactivation at scale):** Scale is diluting quality. Tighten segment definitions: only target fresh churners (0-60 days) and segments with proven Baseline results. Re-test at lower volume.

## Time Estimate

- 10 hours: Design and launch A/B tests (3 rounds, setup + analysis)
- 10 hours: Build multi-channel sequencing workflows in n8n
- 8 hours: Expand segment definitions and monthly refresh automation
- 8 hours: Build reactivated user quality tracking (retention, rechurn, LTV)
- 6 hours: Automate segment performance reporting
- 8 hours: Monitor, analyze test results, iterate on offers and messaging

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, cohorts, retention analysis | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Loops | Automated winback sequences at scale | $49/mo+ based on contact volume — [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app welcome-back messages, multi-channel sequencing | $85/seat/mo Advanced; +$99/mo Proactive Support — [intercom.com/pricing](https://www.intercom.com/pricing) |
| n8n | Multi-channel sequencing, segment refresh, reporting workflows | Self-hosted free; Cloud from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | Segment data, high-value routing, campaign records | $29/seat/mo Plus — [attio.com/pricing](https://attio.com/pricing) |

**Play-specific cost at Scalable:** ~$150-350/mo (Intercom Advanced + Proactive Support + Loops scaled tier + Attio Plus)

## Drills Referenced

- `ab-test-orchestrator` — A/B test winback offers, timing, and messaging per segment with statistical rigor
- the winback offer personalization workflow (see instructions below) — monthly segment refresh, new micro-segments, offer updates based on product changes
- `winback-campaign` — multi-channel winback sequence templates and in-app welcome-back flows
