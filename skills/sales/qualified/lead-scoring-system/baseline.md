---
name: lead-scoring-system-baseline
description: >
  Lead Scoring System — Baseline Run. Deploy automated scoring pipeline that enriches and scores
  100 leads in real-time, integrates PostHog intent signals, and validates Hot >=3x Cold conversion over 2 weeks.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "Hot leads convert at >=3x rate vs Cold leads over 2 weeks"
kpis: ["Meeting rate by tier", "Score accuracy (predicted tier vs actual outcome)", "False negative rate", "Time to first contact by tier"]
slug: "lead-scoring-system"
install: "npx gtm-skills add sales/qualified/lead-scoring-system"
drills:
  - lead-score-automation
  - posthog-gtm-events
  - enrich-and-score
---

# Lead Scoring System — Baseline Run

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Outcomes

Automated scoring pipeline processes 100 leads over 2 weeks. Hot-tier leads (>=80) convert to meetings at >=3x the rate of Cold-tier leads (<50). Scoring runs in real-time: new leads are enriched, scored, and tiered within minutes of entering Attio.

## Leading Indicators

- New leads receive scores within 5 minutes of CRM entry (automation latency)
- Intent scores update in real-time when PostHog detects website behavior
- Score distribution remains balanced (15-25% Hot, not inflating over time)
- Hot leads are contacted within 24 hours of scoring (speed-to-lead)

## Instructions

### 1. Set up event tracking

Run the `posthog-gtm-events` drill. Configure PostHog events specific to lead scoring:

- `lead_scored` — fired when a lead receives a score (properties: fit_score, intent_score, lead_score, lead_tier, scoring_method)
- `lead_tier_changed` — fired when a lead's tier changes due to new signals (properties: old_tier, new_tier, trigger_event)
- `meeting_booked` — with `lead_tier` and `lead_score` properties for conversion tracking
- `outreach_sent` — with `lead_tier` for speed-to-lead tracking

Build a PostHog funnel: `lead_scored` -> `outreach_sent` -> `outreach_replied` -> `meeting_booked`, broken down by `lead_tier`.

### 2. Expand enrichment coverage

Run the `enrich-and-score` drill. Set up a Clay table with enrichment waterfalls for 100 leads:

- Firmographics: company size, industry, revenue, funding stage (Clearbit -> People Data Labs -> Crunchbase)
- Contact fit: title, seniority, department (LinkedIn -> Apollo)
- Intent signals: funding events, job postings, tech stack (see `clay-intent-signals` fundamental)

Expand the scoring model from Smoke: add 2-3 new fit attributes (tech stack overlap, revenue range) and 2-3 new intent signals (funding recency, relevant job postings, competitor tool usage). Update point values based on Smoke learnings.

### 3. Deploy the automated scoring pipeline

Run the `lead-score-automation` drill. Build 3 n8n workflows:

**Workflow 1 — New lead scoring:**
- Trigger: new person created in Attio (webhook)
- Action: push to Clay for enrichment -> compute fit score -> pull PostHog intent data -> compute intent score -> assign composite + tier -> write to Attio -> log `lead_scored` event

**Workflow 2 — Intent signal re-scoring:**
- Trigger: PostHog webhook for high-value events (pricing_page_viewed, demo_form_submitted, content_downloaded)
- Action: look up person in Attio -> recalculate intent score -> update composite + tier -> fire `lead_tier_changed` if tier changed

**Workflow 3 — Score decay:**
- Trigger: daily cron at 6 AM
- Action: query leads with `last_scored` > 14 days and `intent_score` > 0 -> reduce intent score by 50% -> recalculate composite + tier -> update Attio

### 4. Configure outreach priority rules

In Attio, set up prioritized outreach based on lead tier:

- Hot leads (>=80): contact within 24 hours. Create a Slack notification to the founder when a new Hot lead is scored.
- Warm leads (50-79): contact within 3 business days.
- Cold leads (<50): add to a low-priority nurture queue or skip.

### 5. Execute outreach for 2 weeks

**Human action required:** Follow the tier-based priority rules. Contact Hot leads first, then Warm, then Cold. Use the same outreach approach for all tiers (this isolates scoring quality from messaging differences). Log all touchpoints in Attio.

### 6. Investigate false negatives

After week 1, query Attio for leads that scored Cold but booked meetings or replied positively. For each false negative:

- What signals did the model miss? (e.g., the lead had a buying signal not in the model)
- Should a new criterion be added?
- Were the point values miscalibrated?

Document findings and queue model updates for after the 2-week evaluation.

### 7. Evaluate against threshold

After 2 weeks, compute:
- Meeting rate by tier (Hot, Warm, Cold)
- **Pass:** Hot tier meeting rate >= 3x Cold tier meeting rate
- Score accuracy: % of Hot leads that engaged vs % of Cold leads that did not
- False negative rate: % of Cold leads that converted (target: <10%)

If PASS: document the automated scoring model, enrichment waterfall, and n8n workflows. Proceed to Scalable.

If FAIL: diagnose — is the issue fit criteria (wrong companies), intent signals (wrong behaviors), or automation (scoring delays, enrichment gaps)? Fix the weakest link and re-run Baseline for another 2 weeks.

## Time Estimate

- Event tracking setup: 2 hours
- Enrichment expansion: 3 hours
- Automated scoring pipeline (3 workflows): 5 hours
- Outreach priority configuration: 1 hour
- Monitoring and false negative analysis: 3 hours
- Evaluation: 2 hours
- Total: ~16 hours over 2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — lead records, scores, outreach logging | Standard stack (excluded) |
| PostHog | Analytics — intent signals, scoring events, conversion funnels | Standard stack (excluded) |
| n8n | Automation — scoring pipeline, decay cron, re-scoring | Standard stack (excluded) |
| Clay | Enrichment — firmographics, intent signals | Starter: $134/mo for 24K credits ([clay.com/pricing](https://www.clay.com/pricing)) |
| Instantly | Cold email — outreach execution | Growth: $37/mo for 5K emails ([instantly.ai/pricing](https://instantly.ai/pricing)) |

**Play-specific cost: ~$170/mo** (Clay Starter + Instantly Growth)

## Drills Referenced

- `lead-score-automation` — builds the 3 n8n workflows for real-time scoring, intent re-scoring, and decay
- `posthog-gtm-events` — sets up the event taxonomy for scoring and conversion tracking
- `enrich-and-score` — expands Clay enrichment waterfalls and scoring formulas for 100 leads
