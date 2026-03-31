---
name: plg-sales-hybrid-baseline
description: >
  PLG + Sales-Assist Model — Baseline Run. First always-on automation: instrument
  full event tracking, compute per-user engagement scores for PQL identification,
  and deliver contextual upgrade prompts that sustain >=50% sales conversion on
  routed accounts.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Direct"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=50% sales conversion on routed accounts"
kpis: ["Sales-assist conversion rate", "Self-serve upgrade rate", "PQL volume per week", "MRR added from upgrades"]
slug: "plg-sales-hybrid"
install: "npx gtm-skills add product/upsell/plg-sales-hybrid"
drills:
  - posthog-gtm-events
  - engagement-score-computation
  - upgrade-prompt
---

# PLG + Sales-Assist Model — Baseline Run

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Direct

## Outcomes

Build the first always-on PLG-to-sales pipeline. Every active account is continuously scored for engagement. Accounts that cross PQL thresholds receive contextual upgrade prompts (self-serve) or get routed to sales (high-value). Target: >=50% of sales-routed accounts convert to paid or expanded plans within the 2-week evaluation window.

## Leading Indicators

- Engagement scores computing daily for all active accounts without errors
- PQL signals firing for 10+ distinct accounts per week
- Upgrade prompts showing a click-through rate above 5%
- At least 3 sales-routed accounts book meetings within the first week

## Instructions

### 1. Instrument full event tracking

Run the `posthog-gtm-events` drill to establish the PLG event taxonomy. Configure these play-specific events:

| Event | Trigger | Key Properties |
|-------|---------|----------------|
| `plg_signal_detected` | Account crosses a PQL threshold | `account_id`, `signal_type`, `signal_tier`, `plan_tier` |
| `plg_prompt_shown` | Upgrade prompt displayed | `account_id`, `route`, `prompt_variant`, `trigger_signal` |
| `plg_prompt_clicked` | User clicks upgrade CTA | `account_id`, `route`, `cta_type` |
| `plg_upgrade_completed` | Account upgrades or expands | `account_id`, `old_plan`, `new_plan`, `mrr_delta` |
| `plg_sales_handoff` | Account routed to sales | `account_id`, `pql_score`, `assigned_ae` |
| `plg_sales_converted` | Sales-routed account closes | `account_id`, `deal_value`, `days_to_close` |

Build PostHog funnels: `plg_signal_detected` -> `plg_prompt_shown` -> `plg_prompt_clicked` -> `plg_upgrade_completed` (self-serve path) and `plg_signal_detected` -> `plg_sales_handoff` -> `plg_sales_converted` (sales-assist path).

### 2. Deploy per-user engagement scoring

Run the `engagement-score-computation` drill. Configure the four scoring dimensions (frequency, breadth, depth, recency) using your product's core engagement events. The drill outputs a daily engagement score (0-100) per user, stored in Attio and available as PostHog cohorts.

Key configuration for this play:
- Set the PQL threshold at engagement score >= 60 combined with at least one Tier 1 signal (plan limit hit, feature gate, team growth)
- Create PostHog cohorts: `pql-self-serve` (score 40-64, standard plan eligible) and `pql-sales-assist` (score 65+ or enterprise signals)
- Wire the daily scoring pipeline to fire `plg_signal_detected` events when accounts cross the PQL threshold for the first time

### 3. Deploy contextual upgrade prompts

Run the `upgrade-prompt` drill. Configure prompts for the self-serve cohort and sales routing for the high-value cohort:

**Self-serve path (PQL score 40-64):**
- Intercom in-app messages triggered by the `pql-self-serve` cohort
- Message copy tied to the specific PQL signal: limit proximity gets "You have used X of Y -- upgrade for more", feature gate gets "Unlock {{feature}} on {{plan}}"
- One-click upgrade button linking directly to the billing page with the recommended plan pre-selected

**Sales-assist path (PQL score 65+):**
- Create an expansion deal in Attio with the PQL score, top signals, engagement score, and usage summary
- Assign to the account owner or round-robin AE
- Show an Intercom message: "Your usage suggests a custom plan might be a better fit. Want to chat with someone who can help?"
- Send a Loops email from the AE with a Cal.com booking link and personalized usage context

### 4. Evaluate against threshold

After 2 weeks of always-on operation, measure:

- **Primary metric:** Of accounts routed to sales-assist, what percentage converted (upgraded, expanded, or signed a deal)? Target: >=50%.
- **Secondary metrics:** Self-serve upgrade rate (target: >=15%), total MRR added, PQL signal accuracy (what % of flagged accounts took any upgrade action).

**Pass (>=50% sales conversion):** The routing and prompts work. Document the winning prompt variants and signal combinations. Proceed to Scalable.

**Fail (<50%):** Diagnose which path is underperforming. If self-serve is weak: the prompts are not compelling enough or the timing is wrong. If sales-assist is weak: the AE is not getting enough context, the handoff is too slow, or the wrong accounts are being routed. Fix the weakest link and re-run for another 2 weeks.

## Time Estimate

- 3 hours: event taxonomy setup and funnel configuration
- 4 hours: engagement scoring pipeline configuration and validation
- 5 hours: upgrade prompt configuration (self-serve + sales-assist paths)
- 4 hours: 2-week monitoring, analysis, and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts, engagement data | Free tier: 1M events/mo; paid: usage-based from $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app upgrade prompts and sales handoff messages | Essential: $29/seat/mo; Proactive Support add-on: $349/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Triggered upgrade emails from AE | Free: 1,000 contacts; paid from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Cal.com | Booking links for sales calls | Free tier available ([cal.com/pricing](https://cal.com/pricing)) |
| Attio | CRM for deal tracking and engagement score storage | Standard stack (excluded) |
| n8n | Engagement scoring pipeline and routing workflows | Standard stack (excluded) |

**Play-specific cost:** ~$50-100/mo (Loops paid plan if >1,000 contacts, Intercom Proactive Support if using advanced targeting)

## Drills Referenced

- `posthog-gtm-events` -- establish the PLG event taxonomy and build conversion funnels
- `engagement-score-computation` -- compute daily per-user engagement scores for PQL identification
- `upgrade-prompt` -- deliver contextual upgrade prompts and route high-value accounts to sales
