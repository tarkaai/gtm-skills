---
name: usage-limit-sales-upsell-scalable
description: >
  Usage-Based Upsell — Scalable Automation. Automated expansion scoring pipeline
  combining usage, growth, engagement, and firmographic signals. A/B test outreach
  copy, timing, and offer structure. Scale to 50+ qualified accounts per month with
  expansion close rate sustained at 35%+.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product, Email, Direct"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: ">=35% expansion close rate for Tier 1 accounts and expansion ARR >=15% of base ARR across 50+ qualified accounts per month"
kpis: ["Expansion close rate by scoring tier", "Expansion ARR growth rate", "Scoring model accuracy (Tier 1 vs Tier 2 close rates)", "Outreach sequence conversion rate", "Average expansion deal size", "Pipeline velocity (signal to close)"]
slug: "usage-limit-sales-upsell"
install: "npx gtm-skills add product/upsell/usage-limit-sales-upsell"
drills:
  - ab-test-orchestrator
  - expansion-outreach-sequence
---

# Usage-Based Upsell — Scalable Automation

> **Stage:** Product -> Upsell | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Direct

## Outcomes

Find the 10x multiplier. Baseline proved the pipeline works for a controlled group. Scalable replaces manual qualification with an automated scoring model, adds A/B testing to find optimal outreach copy and timing, expands to all metered resources, and scales to 50+ qualified accounts per month while maintaining a 35%+ expansion close rate. The focus shifts from "does it work" to "what configuration maximizes expansion revenue per account."

## Leading Indicators

- Expansion scoring pipeline runs daily across all accounts and all metered resources
- Tier 1 accounts are identified automatically with no manual review needed
- At least 2 A/B tests running concurrently on different outreach variables
- Pipeline volume reaching 50+ qualified accounts per month
- Expansion ARR growing month over month
- Scoring model differentiation: Tier 1 close rate is at least 3x higher than Tier 2
- 90-day expansion retention exceeds 85% (upgrades are sticking)

## Instructions

### 1. Deploy the automated expansion scoring pipeline

Run the the play's scoring criteria drill in full automated mode:

1. Configure the four signal categories in the n8n scoring workflow:
   - Usage proximity (40% weight): limit percentage, multi-resource flags, velocity trends
   - Growth velocity (30% weight): user growth, project creation, billing page visits, pricing page views
   - Engagement depth (20% weight): DAU frequency, feature adoption breadth, session duration trends
   - Firmographic fit (10% weight): company size, funding, industry, tech stack (via Clay)
2. Set up the daily scoring cron (07:00 UTC, after detection runs at 06:00 UTC)
3. Configure automatic tier assignment: Tier 1 (score >= 65) creates deals and triggers outreach, Tier 2 (40-64) adds to watch list, Tier 3 (<40) routes to self-serve
4. Build the tier transition tracking: log when accounts move between tiers
5. Connect Clay for monthly firmographic enrichment refresh

Validate the scoring model against Baseline data: re-score the accounts from Baseline using the new model and confirm that accounts which closed deals in Baseline would have been classified as Tier 1. If not, adjust weights.

### 2. Expand resource coverage

At Baseline, the pipeline likely covered 1-2 resources. Now expand to every metered resource:

1. Audit all plan-limited resources in the product: seats, API calls, storage, projects, workflows, integrations, environments, team members, etc.
2. Add each resource to the detection configuration
3. Update outreach templates with resource-specific copy (API limit outreach reads differently than storage limit outreach)
4. Track per-resource conversion rates from the start — some resources will drive much higher expansion rates than others

### 3. Launch systematic A/B testing on outreach

Run the `ab-test-orchestrator` drill to test variations across the outreach sequence. Run these experiments sequentially:

**Experiment 1 — Subject line framing:**
- Control: Usage data lead ("Your {{resource_name}} usage this month")
- Variant A: Growth framing ("Your team is scaling — here is what is next")
- Variant B: Peer comparison ("How teams like yours handle {{resource_name}} limits")
- Success metric: open rate and reply rate
- Hypothesis: Growth framing outperforms usage data because it makes the recipient feel successful rather than constrained.

**Experiment 2 — Outreach timing:**
- Control: Outreach on Day 0 when account hits Tier 1 (immediate)
- Variant A: Wait 48 hours after Tier 1 classification (let urgency build)
- Variant B: Wait for next billing page visit after Tier 1 (behavioral trigger)
- Success metric: meeting booking rate
- Hypothesis: Behavioral trigger outperforms both fixed timings because it catches the decision-maker at the moment of intent.

**Experiment 3 — First touch content:**
- Control: Current 4-paragraph email with Cal.com CTA
- Variant A: 2-sentence email: "Your team has used {{pct_used}}% of {{resource_name}}. Want to discuss what comes next? [Calendar link]"
- Variant B: Loom-style: Send a short written walkthrough showing their usage dashboard screenshot with the upgrade path highlighted
- Success metric: reply rate and meeting booking rate
- Hypothesis: Brevity outperforms detail for the first touch because busy decision-makers scan before committing.

**Experiment 4 — Offer structure:**
- Control: Standard next-tier upgrade
- Variant A: Annual commitment discount ("Upgrade annual and save 20%")
- Variant B: Temporary limit extension ("I have extended your limit for 14 days — want to discuss the right long-term plan?")
- Variant C: Custom bundle ("Instead of the full next tier, here is a custom add-on for just {{resource_name}}")
- Success metric: close rate and average deal size
- Hypothesis: Temporary limit extension outperforms because it removes immediate pressure and creates a soft deadline for the conversation.

Use PostHog feature flags to allocate accounts to variants. Run each experiment for at least 50 qualified accounts per variant or 21 days, whichever comes last.

### 4. Build predictive expansion signals

Move from reactive (account is already at 85%) to predictive (account will be at 85% within 14 days). Add velocity-based triggers to the the play's scoring criteria:

- If consumption velocity projects a limit hit within 14 days, add +20 to the score regardless of current percentage
- If an account's MRR is growing (they added seats or upgraded partially), treat that as a positive expansion signal — they have already demonstrated willingness to pay more
- If multiple team members are hitting the same feature gate, that is a stronger signal than one person hitting it once
- If an account has been at 70-84% for 3+ weeks without upgrading, escalate to personal outreach — they may be stuck on a pricing objection

### 5. Implement sales routing by account segment

Differentiate the expansion motion by account value:

**Enterprise (MRR > $2,000):**
- Skip the email sequence entirely. Create an Attio task for the account owner with full context.
- Account owner sends a personal, fully custom email (not a template).
- Offer a 30-minute expansion strategy call, not a quick upsell.
- Include a written expansion proposal referencing their specific usage patterns.

**Mid-market (MRR $200-$2,000):**
- Run the standard 4-touch sequence with all personalization.
- Route meetings to the CSM or AE.
- Offer flexible options: tier upgrade, add-on, annual discount.

**SMB (MRR $100-$200):**
- Run the sequence but with a self-serve bias: CTA links to an in-product upgrade flow, not a meeting.
- Only escalate to a meeting if the account replies with questions.
- Test whether a simple in-app nudge is more effective than email for this segment.

### 6. Evaluate against threshold

After 2 months, measure against the pass threshold: at least 35% expansion close rate for Tier 1 accounts AND expansion ARR from closed deals is at least 15% of those accounts' base ARR, across 50+ qualified accounts per month.

Also evaluate:

- Scoring model accuracy: Tier 1 close rate vs. Tier 2 close rate (target 3x+ differential)
- A/B test results: which experiments produced statistically significant winners?
- Per-resource performance: which resources drive the highest expansion close rate and deal size?
- Pipeline velocity: is signal-to-close time decreasing as the system matures?
- Expansion quality: 90-day retention of expanded accounts should exceed 85%
- Revenue efficiency: expansion ARR per dollar spent on tooling
- Self-serve leakage: what percentage of Tier 1 accounts upgrade via self-serve before the outreach sequence reaches them? (This is a positive signal — the scoring model is identifying ready accounts.)

If PASS, proceed to Durable. If FAIL, focus on the highest-leverage experiment result and iterate. Common failure modes: scoring too loose (Tier 1 has too many accounts that are not truly ready), outreach fatigue (accounts receiving too many touches across multiple plays), or offer-market mismatch (the next tier is priced wrong for what customers need).

## Time Estimate

- 12 hours: deploy and validate the automated expansion scoring pipeline
- 8 hours: expand resource coverage and create resource-specific outreach copy
- 16 hours: design, implement, and run 4 A/B experiments (4 hours each)
- 8 hours: build predictive signals and velocity-based scoring
- 8 hours: implement segment-based routing (enterprise, mid-market, SMB)
- 10 hours: ongoing monitoring, experiment analysis, and iteration over 2 months
- 8 hours: evaluation, documentation, and Durable preparation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Scoring signals, cohorts, feature flags, experiments, funnels | Free up to 1M events/mo; paid from $0.00031/event — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM — expansion deals, pipeline, scoring storage, routing | Free up to 3 seats; from $29/seat/mo — [attio.com/pricing](https://attio.com/pricing) |
| Loops | Outreach email sequences with A/B variants | From $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Scoring pipeline, outreach orchestration, experiment routing | Free self-hosted; Cloud from EUR 24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Clay | Firmographic enrichment for scoring Category 4 | From $149/mo — [clay.com/pricing](https://clay.com/pricing) |
| Intercom | In-app messages for Touch 4 and SMB segment | Essential $29/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |
| Cal.com | Expansion meeting booking | Free for individuals; Team from $12/user/mo — [cal.com/pricing](https://cal.com/pricing) |

**Estimated play-specific cost: $250-500/mo** (Clay enrichment + increased Loops volume + n8n workflows)

## Drills Referenced

- the play's scoring criteria — automated 4-category scoring combining usage proximity, growth velocity, engagement depth, and firmographic fit to rank expansion opportunities
- `ab-test-orchestrator` — designs, runs, and evaluates A/B tests on outreach subject lines, timing, content format, and offer structure
- `expansion-outreach-sequence` — 4-touch personalized outreach cadence, expanded with resource-specific copy and segment-based routing
