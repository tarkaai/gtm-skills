---
name: reseller-affiliate-program-scalable
description: >
  Reseller & Affiliate Program — Scalable Automation. Continuous recruitment
  pipeline, tiered commission structure, automated payout processing, and
  per-partner performance tracking across a portfolio of 30+ affiliates.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥30 active partners generating ≥25 partner-sourced paid conversions/quarter with ≥4x commission ROI, sustained for 2 consecutive quarters"
kpis: ["Active partner count", "Conversions per partner per month", "Commission ROI", "Partner activation rate", "Revenue per partner tier"]
slug: "reseller-affiliate-program"
install: "npx gtm-skills add marketing/solution-aware/reseller-affiliate-program"
drills:
  - partner-pipeline-automation
  - affiliate-performance-reporting
---

# Reseller & Affiliate Program — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Outcomes

A self-sustaining partner program with 30+ active affiliates/resellers generating at least 25 paid conversions per quarter at 4x+ commission ROI. Continuous recruitment feeds new partners into the pipeline. Automated onboarding, payout processing, and performance tracking manage the portfolio without proportional headcount. Tiered commissions incentivize top performers while maintaining unit economics. Sustained for 2 consecutive quarters to prove the channel scales.

## Leading Indicators

- Continuous recruitment pipeline produces ≥5 new qualified partners per month without manual sourcing (signal: recruitment automation works)
- Partner activation rate (onboarded → first referral within 30 days) holds above 40% as volume increases (signal: onboarding quality scales)
- Top 20% of partners generate >60% of total affiliate revenue (signal: healthy Pareto distribution — focus resources on star partners)
- Average commission ROI per partner stays above 3x as the portfolio grows (signal: partner quality isn't declining as you scale)
- Partner churn rate (active → dormant in 90 days) stays below 15%/quarter (signal: partners stay engaged over time)

## Instructions

### 1. Build the continuous partner pipeline

Run the `partner-pipeline-automation` drill adapted for the affiliate program:

**Recruitment automation (n8n workflow):**
- **Trigger**: Monthly cron (1st of each month)
- **Action 1**: Run Clay company search and people search for new candidates matching the qualifying criteria from Baseline. Exclude companies and contacts already in Attio.
- **Action 2**: Enrich and score new candidates automatically. Add qualified candidates (score ≥10/15) to Attio with status "Prospect."
- **Action 3**: Auto-enroll new prospects in the Instantly outreach sequence.
- **Action 4**: When prospects reply positively, update Attio status to "In Conversation" and create a deal in the Partnerships pipeline.

**Inbound partner applications (n8n workflow):**
- Build a partner application form (Tally or Typeform) linked from your website's /partners page.
- **Trigger**: Form submission webhook
- **Action 1**: Enrich the applicant with Clay. Score on audience overlap, size, and activity.
- **Action 2**: If score ≥10/15, auto-approve: create affiliate account, send onboarding kit, update Attio status to "Onboarding."
- **Action 3**: If score <10/15, hold for manual review. Send acknowledgment email.

**Partner referral program:**
- Ask top-performing partners to recruit other affiliates. Offer a bonus ($50-100) for each referred partner who generates their first paid conversion.

### 2. Implement tiered commissions

Upgrade from flat commission to a tiered structure that rewards high performers:

| Tier | Criteria | Commission Rate | Perks |
|------|----------|----------------|-------|
| Standard | All new partners | 15% recurring, 12 months | Basic onboarding kit, self-serve portal |
| Silver | ≥5 paid conversions/quarter | 20% recurring, 12 months | Dedicated Slack channel, monthly performance email |
| Gold | ≥15 paid conversions/quarter | 25% recurring, 12 months | Co-branded landing page, quarterly strategy call, early feature access |

Build an n8n workflow to auto-promote partners:
- **Trigger**: Monthly cron
- **Action 1**: Query Rewardful for each partner's conversions in the last 90 days
- **Action 2**: Compare against tier thresholds
- **Action 3**: If tier change needed, update commission rate in Rewardful and tier field in Attio
- **Action 4**: Send tier change notification email (congratulations for promotion; for demotion, offer tips to requalify)

### 3. Automate payout processing

Build an n8n workflow for monthly commission payouts:

- **Trigger**: Monthly cron (last business day of month)
- **Action 1**: Pull all approved commissions from Rewardful that have cleared the 30-day delay
- **Action 2**: Cross-reference with Attio: verify each partner is in "Active" status and has a valid payout method
- **Action 3**: Check for chargebacks and refunds — deduct clawed-back commissions
- **Action 4**: Process payouts via Rewardful's PayPal mass pay or Wise for international partners
- **Action 5**: Update Attio with payout amount, date, and cumulative earnings
- **Action 6**: Send payout confirmation emails via Loops with earnings summary and next-tier progress

**Human action required:** Review and approve the monthly payout batch before execution (total amount, any flagged anomalies). This is the only manual step.

### 4. Deploy per-partner performance tracking

Run the `affiliate-performance-reporting` drill:

- Build the PostHog dashboard: referrals by partner, revenue by partner, conversion rates, commission ROI, funnel by tier
- Create performance cohorts: star partners, volume drivers, declining partners, dormant partners
- Deploy the weekly automated brief: clicks, signups, conversions, revenue, ROI, partner health
- Set up alerts: partner drops >60% week-over-week, star partner achievement, total revenue below baseline

### 5. Scale partner enablement

Invest in the assets that help partners sell more effectively:

**Content library (automated via n8n):**
- Monthly: Generate fresh email blurbs and social posts using Claude, tailored to current product features and customer stories. Distribute to all active partners via Loops.
- Quarterly: Create a "Partner Newsletter" with program updates, top performer spotlights, new product features, and high-converting copy templates.

**Partner Slack/Discord community:**
- Create a private channel for active partners. Share tips, answer questions, and let partners learn from each other.
- Post weekly conversion tips and monthly performance leaderboards (opt-in).

**Crossbeam integration (if available):**
- Connect Crossbeam to identify partners with the highest account overlap with your target list. Prioritize these partners for co-selling motions (partner introduces you to a specific prospect they already work with).

### 6. Evaluate against threshold

After 2 quarters (6 months), measure:

- **Active partners**: Partners with ≥1 click in the last 30 days. Target: ≥30
- **Partner-sourced paid conversions**: Per quarter. Target: ≥25/quarter
- **Commission ROI**: Total affiliate revenue / total commissions paid. Target: ≥4x
- **Sustainability**: Both metrics met for 2 consecutive quarters

**Pass threshold: ≥30 active partners AND ≥25 conversions/quarter AND ≥4x commission ROI, sustained 2 quarters**

- **Pass**: The affiliate channel scales. Document the partner mix, tier distribution, and top-performing partner types. Proceed to Durable.
- **Marginal**: 20-29 partners or 15-24 conversions. Analyze: Is the bottleneck recruitment (not enough partners entering), activation (partners not promoting), or conversion (traffic not converting)? Each requires a different fix.
- **Fail**: <20 partners or <15 conversions after 2 quarters. Re-evaluate: Does the product category support an affiliate model? Some products (complex enterprise, long sales cycle, heavy services) convert better through referral partnerships than self-serve affiliate links.

## Time Estimate

- Continuous recruitment pipeline build: 15 hours
- Tiered commission implementation: 5 hours
- Payout automation: 5 hours
- Performance reporting setup: 10 hours
- Partner enablement assets: 10 hours
- Ongoing monitoring and optimization (3 months): 20 hours
- Strategic reviews and course corrections: 10 hours

Total: ~75 hours over 3 months (front-loaded; automation handles most ongoing work)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Rewardful | Affiliate tracking, commissions, payouts | Growth: $99/mo ([rewardful.com/pricing](https://www.rewardful.com/pricing)) |
| Clay | Continuous partner candidate sourcing | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Crossbeam | Partner account overlap mapping | Free tier for basic use; Connector from $400/mo ([crossbeam.com/pricing](https://www.crossbeam.com/pricing)) |
| n8n | Pipeline, onboarding, payout automation | Cloud Pro: ~$60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Partner CRM and pipeline management | Plus: $34/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Affiliate funnel analytics and dashboards | Free up to 1M events ([posthog.com/pricing](https://posthog.com/pricing)) |
| Instantly | Cold outreach to partner candidates | Growth: $30/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Loops | Partner onboarding and enablement sequences | Starter: $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Anthropic Claude | Copy generation, performance insights | ~$15-30/mo ([anthropic.com/pricing](https://anthropic.com/pricing)) |

**Estimated cost for this level: ~$240-470/mo** (Rewardful Growth + Clay + n8n required; Crossbeam optional but valuable at scale)

## Drills Referenced

- `partner-pipeline-automation` — continuous recruitment, automated outreach, scheduling, and partner lifecycle management
- `affiliate-performance-reporting` — per-partner dashboards, weekly briefs, ROI tracking, and alerts
