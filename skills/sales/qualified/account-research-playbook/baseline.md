---
name: account-research-playbook-baseline
description: >
  Account Research & Intelligence — Baseline Run. Batch-enrich 40+ accounts
  via Clay automation, generate AI-powered personalization hooks at scale,
  run always-on outreach sequences, and measure research-driven reply rates
  over 2 weeks.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Baseline Run"
time: "24 hours over 2 weeks"
outcome: ">=35% reply rate from researched outreach and >=2.5x faster progression to meetings over 2 weeks"
kpis: ["Reply rate by research depth", "Meeting rate (researched vs non-researched)", "Research time efficiency", "Signal-to-reply correlation"]
slug: "account-research-playbook"
install: "npx gtm-skills add sales/qualified/account-research-playbook"
drills:
  - cold-email-sequence
  - posthog-gtm-events
  - threshold-engine
---

# Account Research & Intelligence — Baseline Run

> **Stage:** Sales > Qualified | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Research 40+ accounts using batch Clay enrichment with automated firmographic, news, tech stack, and contact data. Generate AI-powered personalization hooks for each account. Run always-on email sequences via Instantly with research-informed messaging. Achieve >=35% reply rate from researched outreach and demonstrate that researched accounts progress to meetings >=2.5x faster than non-researched accounts over 2 weeks.

## Leading Indicators

- Clay enrichment hit rate >=80% across firmographics, funding, and contacts
- Personalization hooks generated for >=90% of enriched accounts (at least 2 hooks each)
- Per-account research time drops from 15-20 minutes (Smoke) to 2-3 minutes (batch automation)
- Open rates on personalized emails >=45% (vs <=25% for generic templates)
- Positive reply sentiment ratio >=60% of all replies

## Instructions

### 1. Set up event tracking

Run the `posthog-gtm-events` drill. Configure events for this play:

| Event | Properties | Trigger |
|-------|-----------|---------|
| `account_researched` | `company_domain`, `research_depth`, `signal_count`, `hook_count` | After enrichment completes |
| `outreach_sent` | `company_domain`, `channel`, `hook_type`, `personalized` | After email/LinkedIn sent |
| `outreach_replied` | `company_domain`, `hook_type`, `sentiment`, `research_depth` | After reply detected |
| `meeting_booked` | `company_domain`, `hook_type`, `research_depth`, `days_from_first_touch` | After meeting scheduled |

Connect PostHog to Attio via n8n webhook so deal stage changes sync automatically.

### 2. Batch-enrich target accounts

Run the the account research enrichment workflow (see instructions below) drill. Import your 40-50 target accounts into a Clay table and configure enrichment columns:

1. **Firmographics**: Clearbit > Apollo waterfall for company size, revenue, funding stage
2. **Funding events**: Crunchbase enrichment for last round amount, date, investors
3. **Tech stack**: BuiltWith detection, classified as complementary/competing/neutral
4. **News signals**: Claygent search for last 90 days of company news
5. **Contacts**: Find 3 people per company matching buyer personas, with verified emails
6. **Personalization hooks**: Claygent-generated 2 hooks per account with suggested first lines
7. **Priority score**: Formula column scoring accounts 0-100 based on signal strength

Push all enriched data to Attio. Create a dynamic list of high-priority accounts (score >=50).

Estimated cost: ~15-20 Clay credits per account. For 50 accounts: ~750-1,000 credits.

### 3. Build research-informed email sequences

Run the `cold-email-sequence` drill. Set up Instantly with:

**Sequence A (researched accounts, score >=50):**
- Email 1: Personalized first line from research hook + value proposition + CTA
- Email 2 (day 3): Follow-up referencing a different hook or signal
- Email 3 (day 7): Social proof from a similar company in their industry/stage

**Sequence B (researched accounts, score <50):**
- Email 1: Light personalization (industry + company size reference) + value proposition
- Email 2 (day 3): Case study relevant to their segment
- Email 3 (day 7): Direct ask with low-commitment CTA

**Sequence C (control — non-researched):**
- Standard template sequence with no account-specific personalization

Split: 20 accounts in Sequence A, 20 in Sequence B, 10 in Sequence C.

### 4. Configure research-to-messaging frameworks

For each signal type, define the messaging template:

| Signal | Framework | Example |
|--------|-----------|---------|
| Funding (last 30 days) | Congratulate + scale challenge + your solution | "Congrats on the Series B with {Investor}. As you scale {function}, {pain point} becomes critical..." |
| Executive hire (last 60 days) | Welcome + new priorities + relevant help | "Saw {Company} brought on {Name} as {Title}. New {function} leaders typically prioritize {pain point}..." |
| Tech stack (complementary) | Integration angle | "Noticed you're using {Tool}. Our customers who also use {Tool} typically {benefit}..." |
| Tech stack (competing) | Displacement angle | "Companies like {Similar Company} switched from {Competitor} to us because {differentiator}..." |
| Hiring signals | Team-building angle | "You're hiring {n} {roles} — as that team grows, {pain point} compounds. We help teams like yours..." |

### 5. Execute and monitor for 2 weeks

Launch all sequences. Monitor daily in PostHog and Instantly:

- **Days 1-3**: Check deliverability. If bounce rate >5%, pause and clean the list.
- **Days 3-7**: Check reply rates by sequence. If Sequence A reply rate is not outperforming Sequence C by at least 1.5x, review hook quality.
- **Days 7-14**: Check meeting booking rate. Track which hook types generate meetings, not just replies.

Log every reply sentiment: positive (interested, asking questions), neutral (polite decline), negative (annoyed, unsubscribe request).

### 6. Analyze signal effectiveness

After 2 weeks, build a signal effectiveness table:

| Signal Type | Outreach Sent | Replies | Reply Rate | Meetings | Meeting Rate |
|-------------|--------------|---------|------------|----------|-------------|
| Funding | {n} | {n} | {%} | {n} | {%} |
| Exec hire | {n} | {n} | {%} | {n} | {%} |
| Tech stack | {n} | {n} | {%} | {n} | {%} |
| News/launch | {n} | {n} | {%} | {n} | {%} |
| No research | {n} | {n} | {%} | {n} | {%} |

This table feeds your Scalable-level prioritization: invest more research time in high-converting signal types.

### 7. Evaluate against threshold

Run the `threshold-engine` drill. Measure:

- Researched outreach reply rate: target >=35%
- Researched accounts time-to-meeting vs non-researched: target >=2.5x faster
- Research time efficiency: total research hours / accounts researched (target: <5 min/account)

**PASS:** Reply rate >=35% AND researched accounts progress >=2.5x faster to meetings. Proceed to Scalable.

**FAIL:** Diagnose by sequence:
- Sequence A underperforms: hooks are weak or inaccurate. Improve Claygent prompts.
- Sequence B underperforms: light personalization is not sufficient. Increase research depth for all accounts.
- All sequences underperform: issue is targeting (ICP), not research. Re-run `icp-definition`.

## Time Estimate

- Event tracking setup: 2 hours
- Clay enrichment configuration and execution: 4 hours
- Sequence building and messaging frameworks: 4 hours
- Execution monitoring (daily, 30 min x 14 days): 7 hours
- Signal analysis and evaluation: 3 hours
- **Total: ~24 hours over 2 weeks** (4 hours active work, rest is monitoring)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Batch enrichment, Claygent research, tech stack, news signals | Launch: $185/month ([clay.com/pricing](https://www.clay.com/pricing)) |
| Instantly | Cold email sequencing with A/B variants | Growth: $37/month, Hypergrowth: $97/month ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Attio | CRM — store enriched data, track deals | Plus: $34/user/month ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Event tracking and funnel analysis | Free tier: 1M events/month ([posthog.com/pricing](https://posthog.com/pricing)) |
| Apollo | Contact sourcing (initial list) | Free tier or Basic: $49/user/month ([apollo.io/pricing](https://www.apollo.io/pricing)) |

**Estimated play-specific cost: ~$220-330/month** (Clay Launch + Instantly Growth/Hypergrowth)

## Drills Referenced

- the account research enrichment workflow (see instructions below) — batch Clay enrichment with automated hook generation
- `cold-email-sequence` — Instantly email sequences with research-informed messaging
- `posthog-gtm-events` — event tracking for research effectiveness measurement
- `threshold-engine` — evaluate reply rate and time-to-meeting against pass thresholds
