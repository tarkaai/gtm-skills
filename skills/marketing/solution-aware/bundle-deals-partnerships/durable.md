---
name: bundle-deals-partnerships-durable
description: >
  Bundle Deal Partnerships — Durable Intelligence. Always-on AI agents monitor
  per-partner bundle performance, detect pricing decay and promotional fatigue,
  generate optimization hypotheses, run A/B experiments on landing pages and
  tier structures, and auto-implement winners. Weekly optimization briefs.
  Converges when successive experiments produce <2% improvement.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Durable Intelligence"
time: "180 hours over 6 months"
outcome: "Sustained or improving bundle deals and revenue over 6 months; page-to-deal CVR at or above Scalable peak; agents detect pricing decay, promotional fatigue, tier mismatch, and seasonal patterns, adapting automatically."
kpis: ["Bundle deals per quarter", "Page-to-deal conversion rate", "Revenue per bundle", "Experiment win rate", "Partner promotional effort score", "Bundle customer retention rate", "Pricing tier distribution shift"]
slug: "bundle-deals-partnerships"
install: "npx gtm-skills add marketing/solution-aware/bundle-deals-partnerships"
drills:
  - autonomous-optimization
  - bundle-performance-reporting
---

# Bundle Deal Partnerships — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Outcomes

An always-on optimization system that manages the bundle deal portfolio autonomously. The `autonomous-optimization` drill runs the core loop: detect metric anomalies across partners, pricing tiers, and landing page variants; generate improvement hypotheses; run A/B experiments on bundle pricing, landing page copy, CTA positioning, and tier structure; evaluate results; and auto-implement winners. Weekly optimization briefs summarize what changed and why. The system converges when successive experiments produce <2% improvement — the play has reached its local maximum.

Sustained or improving deal volume and revenue over 6 months. Page-to-deal conversion rate at or above the Scalable peak. The agent detects and adapts to pricing decay (a bundle's perceived value eroding as standalone prices change), promotional fatigue (a partner's audience stops responding to repeated bundle messaging), tier mismatch (customers consistently choosing only the lowest tier, indicating the higher tiers lack compelling differentiation), and seasonal patterns (budget cycles, conference seasons, end-of-quarter purchasing surges).

## Leading Indicators

- Anomaly detection fires within 24 hours of a metric shift (signal: monitoring is working)
- At least 1 experiment runs per 2-week period (signal: optimization loop is active)
- Experiment win rate ≥30% (signal: hypotheses are well-targeted)
- No bundle partner drops below 50% of their historical deal volume for 3+ consecutive weeks without a corrective action firing (signal: decay detection works)
- Weekly optimization brief posts on time every Friday (signal: reporting pipeline is stable)
- Time between anomaly detection and experiment launch <72 hours (signal: the loop is tight)
- Bundle portfolio maintains ≥8 active partners generating deals (signal: replacement pipeline keeps pace with partner churn)

## Instructions

### 1. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill configured for this play's specific metrics and levers:

**Monitor phase (daily via n8n cron):**
- Pull bundle KPIs from PostHog: page views, tier selections, deals completed, revenue, per-partner performance, landing page variant performance
- Compare last 2 weeks against 4-week rolling average
- Classify each metric as: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), or spike (>50% increase)
- Per-partner anomaly detection: flag any partner whose deals dropped >30% from their rolling average
- Per-tier anomaly detection: flag if any tier's selection rate shifts >15% in either direction over 4 weeks (signals pricing misalignment)
- Promotional balance check: flag any partner where traffic attribution is >80% from one side for 3+ consecutive weeks
- Revenue split accuracy: verify actual revenue collected matches the agreed split for each partner. Flag discrepancies >5%.
- If anomaly detected, trigger the Diagnose phase

**Diagnose phase (triggered by anomaly):**
- Gather context: which partners are affected, which tiers are underperforming, what landing page variants were active, when was the last pricing change, what is the partner's promotional cadence
- Pull 8-week per-partner and per-tier metric history from PostHog
- Run hypothesis generation with the anomaly data. Common hypotheses for this play:
  - "Partner X's audience is fatigued — same subscribers seeing bundle promotions for 3+ months without new angles. Prescribe: partner cooldown period or completely refreshed bundle positioning."
  - "Tier mismatch — 85% of customers select Starter tier. Prescribe: A/B test removing the Starter tier to push customers toward Growth, or A/B test adding more value to Growth to justify the price increase."
  - "Landing page conversion dropped — bundle traffic arrives but does not convert. Prescribe: A/B test new headline, value proposition framing, or social proof placement."
  - "Pricing decay — Partner Y raised their standalone price, making the bundle discount less compelling. Prescribe: renegotiate bundle pricing to maintain perceived savings."
  - "Seasonal effect — Q4 purchasing surge or January budget reset. Prescribe: adjust expectations; do not over-react or under-react."
  - "Partner Z stopped promoting — their traffic dropped to near-zero while the bundle page still converts when visited. Prescribe: re-engage partner with updated performance data and refreshed co-marketing assets."
  - "Bundle customer churn spike — 90-day retention dropped below 60%. Prescribe: investigate whether bundle customers are discount-seekers or product-fit mismatches. May need to adjust the target audience or add onboarding support."
- Store hypotheses in Attio. If risk = "high" (e.g., changing pricing for a top-3 partner's bundle, or retiring a bundle that generates >20% of total revenue), alert for human review.

**Experiment phase (triggered by hypothesis acceptance):**
- Design the experiment. For this play, the primary experiment types are:

  1. **Landing page A/B test**: Use PostHog feature flags to show different page variants to bundle traffic. Test headlines, social proof placement, CTA copy, and value proposition framing. Measure page-to-deal CVR per variant.
  2. **Pricing tier A/B test**: Test different discount levels or tier structures across similar partners. Example: Partner A gets 20% bundle discount, Partner B gets 25%. Compare deal volume and revenue. CAUTION: never show different prices to the same audience — split by partner, not by visitor.
  3. **CTA commitment test**: Test different CTA commitment levels across partners. Example: "Start free trial bundle" vs. "Get the bundle — 15% off" vs. "Book a bundle walkthrough." Measure conversion rate per CTA type.
  4. **Tier elimination test**: For bundles where >80% of deals are the lowest tier, test removing the lowest tier entirely (forcing the choice between Growth and Scale). Measure total deal volume and revenue impact.
  5. **Promotional channel test**: Test whether partner email promotion, in-product banner, or social media post drives the highest quality bundle traffic (measured by conversion rate, not just volume).
  6. **Bundle refresh test**: For a stale bundle (declining deals over 3+ months), test a complete refresh: new landing page design, updated pricing, and a limited-time bonus offer. Compare the refresh month against the prior 3-month average.

- Use PostHog experiments for landing page and CTA tests. For pricing and tier tests, track by partner and `utm_content` variant.
- Minimum experiment duration: 14 days or 50+ bundle page views per variant, whichever is longer.

**Evaluate phase (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run experiment evaluation:
  - **Adopt**: Winning variant becomes the new default for that bundle. Update the landing page or pricing. Log the change in Attio.
  - **Iterate**: Result was inconclusive or showed a promising direction. Generate a refined hypothesis and re-test.
  - **Revert**: Variant performed worse. Restore the control. Wait 14 days before testing the same variable.
  - **Extend**: Insufficient data (too few bundle page views in the test period). Keep the experiment running for another cycle.
- Store the full evaluation in Attio with decision, confidence level, and reasoning.

**Report phase (weekly, Friday 3pm via n8n cron):**
- Aggregate all optimization activity for the week
- Calculate net metric change from adopted experiments
- Generate the weekly optimization brief (see step 2)

### 2. Deploy play-specific monitoring and reporting

Run the `bundle-performance-reporting` drill to build the monitoring layer specific to this play:

**Bundle dashboard in PostHog:**
- Bundle page views by partner (bar chart, last 30 days)
- Deals completed by partner (bar chart, last 30 days)
- Page-to-deal CVR by partner (table, sorted descending)
- Revenue over time (trend line, last 90 days)
- Tier selection distribution (pie chart, last 30 days)
- Bundle funnel: page view → tier selected → CTA clicked → checkout started → deal completed
- Traffic source breakdown per partner (your channels vs. theirs)
- Average deal value by partner (table)
- Bundle customer retention cohort analysis (30, 60, 90 day retention by partner)
- Pricing tier migration tracker (are customers upgrading tiers over time?)

**Weekly bundle brief (automated, Friday 3pm):**
```
## Bundle Deals Weekly Brief — {date}

**This week**: {page_views} page views, {deals_completed} deals, ${revenue} revenue
**vs 4-week avg**: {change_pct}% {up/down}
**Active bundles**: {count} | **Avg deal value**: ${avg_deal_value}

### Top partners by revenue
1. {partner_1}: {deals} deals, ${revenue} ({cvr}% CVR)
2. {partner_2}: {deals} deals, ${revenue} ({cvr}% CVR)

### Tier distribution
- Starter: {pct}% | Growth: {pct}% | Scale: {pct}%
- Shift from last week: {direction and magnitude}

### Anomalies detected
- {partner/metric}: {description} — {hypothesis generated}

### Promotional balance
- Partners with >80% one-sided traffic: {list with ratios}
- Partners stopped promoting: {list}

### Experiments this week
- {experiment}: {status} — {result or ETA}

### Adopted changes
- {change}: {impact on metrics}

### Bundle customer health
- 90-day retention rate: {pct}%
- Churn signals: {count} bundle customers at risk

### Convergence status
{distance from local maximum estimate}
{recommended focus for next week}
```

**Per-partner bundle ROI tracking in Attio:**
- Total page views, deals, revenue, CVR, preferred tier, revenue split paid, traffic attribution, bundle health score, customer retention rate
- Updated weekly by n8n automation

**Performance alerts:**
- Partner's bundle deals drop to zero for 2 consecutive weeks → investigate promotion and landing page health
- New bundle generates first deal within 7 days → celebrate and fast-track promotional support
- Total weekly revenue drops below Scalable baseline for 2 consecutive weeks → trigger autonomous optimization investigation
- Tier distribution shifts >20% toward lowest tier over 4 weeks → flag pricing misalignment
- Bundle customer 30-day churn exceeds 40% → flag product-fit issue for human review

### 3. Manage bundle portfolio health

The agent autonomously manages the bundle portfolio:

- **Pricing decay detection**: Monitor each partner's standalone pricing page weekly (via web scrape or manual check). If a partner raises their standalone price, the bundle discount percentage effectively increases (more value for the customer) — no action needed. If a partner LOWERS their standalone price, the bundle becomes less compelling — the agent flags for immediate pricing renegotiation.
- **Promotional fatigue management**: If a partner's traffic contribution declines for 3 consecutive weeks, the agent sends refreshed co-marketing assets (new email copy, new social posts, updated performance data) via Loops. If traffic does not recover in 2 weeks, flag for a human re-engagement call.
- **Partner graduation**: Partners consistently generating >10 deals per month get escalated to deeper partnerships: co-developed features, exclusive bundle tiers, joint customer success programs. Log the recommendation in Attio for human review.
- **Partner replacement**: When a bundle is retired (fatigue, pricing decay, partner churn), the agent triggers `partner-prospect-research` to source a replacement. Maintain ≥8 active bundles at all times.
- **Seasonal adjustment**: The agent learns seasonal patterns (Q4 budget spending, January resets, conference season distractions) and adjusts deal volume expectations accordingly rather than flagging expected seasonal shifts as anomalies.
- **Bundle customer health**: Track bundle customer retention at 30, 60, and 90 days. If a partner's bundle customers churn at >2x the rate of standalone customers, the bundle may be attracting discount-seekers rather than product-fit buyers. The agent recommends: adjusting the target audience, reducing the discount, or adding onboarding support specific to bundle customers.

### 4. Guardrails

- **Maximum 1 active experiment per bundle at a time.** Never stack pricing tests with landing page tests on the same bundle.
- **Maximum 3 active experiments across the entire portfolio at a time.** Too many simultaneous experiments make attribution impossible.
- **Revert threshold**: If any bundle's deal volume drops >40% during an experiment period, auto-revert immediately.
- **Human approval required for:**
  - Pricing changes to any bundle generating >20% of total portfolio revenue
  - Retiring a partner that generates >15% of total deals
  - Any experiment the hypothesis generator flags as "high risk"
  - Proposing partnership escalation (co-developed features, exclusive tiers)
  - Revenue split renegotiation
- **Cooldown**: After a failed experiment, wait 14 days before testing the same variable on the same bundle.
- **Maximum 4 experiments per month across the portfolio.** If all 4 fail, pause optimization and flag for human strategic review.
- **Never retire more than 2 bundles in the same month** without human approval (prevents portfolio collapse).
- **Revenue protection**: Never change pricing for a bundle in a way that raises the price for existing bundle customers. Existing customers keep their rate; experiments apply to new customers only.

### 5. Convergence detection

The optimization loop runs continuously. It detects convergence when:
- 3 consecutive experiments produce <2% improvement in the primary metric (deals per quarter)
- The play has reached its local maximum

At convergence:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment frequency to 1 per month (maintenance mode)
3. Report: "Bundle deals has converged. Current performance: {metrics}. Top partners: {list}. Portfolio: {count} active bundles generating {deals}/quarter at ${revenue} average deal value. Further gains require strategic changes (product integrations that create bundled experiences rather than just bundled pricing, new partner categories, embedded partnerships where your product is part of the partner's offering) rather than tactical pricing/landing page optimization."

## Time Estimate

- Autonomous optimization setup: 20 hours
- Bundle performance reporting setup: 10 hours
- Initial monitoring and tuning (month 1): 20 hours
- Ongoing oversight (months 2-6, ~5 hours/month): 25 hours
- Experiment design and evaluation: 35 hours
- Bundle portfolio management: 30 hours
- Strategic reviews and course corrections: 40 hours

Total: ~180 hours over 6 months (heavily front-loaded; agent handles most ongoing work)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, experiments, anomaly detection, dashboards | Free up to 1M events; paid from $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Optimization loop orchestration, scheduling, alerts | Cloud Pro: ~EUR 60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Bundle CRM, experiment logs, ROI tracking | Plus: $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Anthropic Claude | Hypothesis generation, experiment evaluation, briefs | Sonnet 4 API: ~$15-30/mo at this usage ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Webflow | Bundle landing pages with A/B variants | CMS plan: $29/mo ([webflow.com/pricing](https://webflow.com/pricing)) |
| Loops | Partner re-engagement, bundle customer retargeting | Paid from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Stripe | Bundle checkout and revenue tracking | 2.9% + $0.30 per transaction ([stripe.com/pricing](https://stripe.com/pricing)) |
| Crossbeam | Ongoing partner account overlap analysis | Free tier for basic; Connector from ~$400/mo ([crossbeam.com/pricing](https://www.crossbeam.com/pricing)) |

**Estimated cost for this level: ~$200-400/mo** (n8n Pro + Attio Plus + Webflow CMS + Anthropic API + Loops required; Crossbeam and PostHog within free tiers for most usage)

## Drills Referenced

- `autonomous-optimization` — the core monitor → diagnose → experiment → evaluate → implement loop that finds the local maximum
- `bundle-performance-reporting` — per-partner dashboards, weekly briefs, ROI tracking, tier distribution analysis, and alerts specific to this play
