---
name: account-research-playbook-scalable
description: >
  Account Research & Intelligence — Scalable Automation. Deploy an always-on
  n8n pipeline that auto-researches every new target account, generates AI-powered
  briefs, and feeds 200+ accounts/month into research-informed outreach sequences
  with A/B testing across signal types.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: ">=80% research automation and >=35% reply rate maintained over 2 months"
kpis: ["Research automation rate", "Research accuracy", "Reply rate by research type", "Time savings vs manual"]
slug: "account-research-playbook"
install: "npx gtm-skills add sales/qualified/account-research-playbook"
drills:
  - ab-test-orchestrator
  - tool-sync-workflow
  - signal-detection
---

# Account Research & Intelligence — Scalable Automation

> **Stage:** Sales > Qualified | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Deploy an always-on n8n pipeline that automatically researches every account added to the target list: enriches via Clay, searches for news and signals, detects tech stack, identifies contacts, generates AI-powered account briefs with personalization hooks, and pushes everything to Attio. Scale from 40 accounts (Baseline) to 200+ accounts per month. Maintain >=35% reply rate while automating >=80% of the research process. Run A/B tests on signal types and messaging frameworks to find the 10x research-to-revenue multiplier.

## Leading Indicators

- Automated pipeline processes new accounts within 5 minutes of list addition
- >=80% of enrichment columns return data (hit rate)
- AI-generated briefs pass human accuracy check >=90% of the time
- Research time per account drops to <1 minute (fully automated)
- Signal-based account scoring predicts reply probability with >=65% accuracy
- A/B tests produce statistically significant winners within 2 weeks

## Instructions

### 1. Deploy the automated research pipeline

Run the the account research automation workflow (see instructions below) drill. Build an n8n workflow with:

**Trigger:** Attio webhook fires when a company is added to the "Target Accounts" list.

**Enrichment chain:**
1. Send domain to Clay API — triggers template table enrichment (firmographics, funding, tech stack, news, contacts)
2. Poll Clay for completion (max 120 seconds)
3. Parse results: extract firmographics, classify tech stack, score news signals, rank contacts
4. Query Attio for any prior interaction history
5. Send enriched data to Anthropic API — generate account brief with 3 personalization hooks and recommended entry point
6. Write everything to Attio: update company record, create brief note, update contact records
7. Notify via Slack: "Account researched: {Company} — Priority: {score} — Top signal: {signal}"

**Refresh workflow:** Weekly cron re-enriches pipeline accounts with briefs older than 30 days.

**Scoring feedback loop:** When deals progress (reply > meeting > proposal), log which signals were present. This data trains the account scoring model.

### 2. Build signal-based prioritization

Run the `signal-detection` drill. Configure Clay to monitor for real-time buying signals across your target account list:

| Signal | Source | Refresh | Score |
|--------|--------|---------|-------|
| Funding in last 30 days | Crunchbase via Clay | Daily | +30 |
| Executive hire (buyer persona role) | LinkedIn via Clay | Weekly | +25 |
| 3+ relevant job postings | Job boards via Claygent | Weekly | +20 |
| Uses complementary tech | BuiltWith via Clay | Monthly | +15 |
| Uses competing tech | BuiltWith via Clay | Monthly | +15 |
| Company news (product launch, partnership) | Claygent news search | Weekly | +15 |
| Engaged with competitor content | LinkedIn via Claygent | Bi-weekly | +10 |

When a high-score signal fires (composite score jumps by >=20 points), n8n triggers an immediate pipeline refresh: re-generate the account brief with the new signal as the top hook and move the account to the front of the outreach queue.

### 3. Connect the full tool stack

Run the `tool-sync-workflow` drill. Build n8n sync workflows:

- **Clay > Attio**: Enrichment results push to CRM company and contact records
- **Instantly > Attio**: Email opens, replies, and bounces sync to contact activity
- **Attio > PostHog**: Deal stage changes fire PostHog events for funnel tracking
- **PostHog > Attio**: Research effectiveness metrics surface on company records
- **LinkedIn activity > Attio**: Connection accepts and message replies logged

Ensure zero data silos: every touchpoint is tracked across the full stack.

### 4. Launch A/B testing on research variables

Run the `ab-test-orchestrator` drill. Design experiments to find what matters most:

**Experiment 1 — Hook type effectiveness:**
- Variant A: Lead with funding signal
- Variant B: Lead with tech stack signal
- Variant C: Lead with executive hire signal
- Minimum 50 sends per variant. Measure reply rate.

**Experiment 2 — Research depth:**
- Variant A: Full research (firmographics + news + tech + contacts + AI brief)
- Variant B: Light research (firmographics + contacts only)
- Minimum 75 sends per variant. Measure reply rate and meeting rate.

**Experiment 3 — Brief-generated vs framework messaging:**
- Variant A: Use AI-generated first lines from the account brief
- Variant B: Use framework templates (signal type + standard messaging)
- Minimum 50 sends per variant. Measure reply rate and positive sentiment rate.

Run experiments sequentially. Implement winners. Each winning variant becomes the new default for the next experiment cycle.

### 5. Scale to 200+ accounts per month

With automation handling research and A/B tests identifying winning approaches:

- **Week 1-2**: Pipeline 50 accounts. Verify automation reliability (error rate <5%).
- **Week 3-4**: Scale to 100 accounts. Monitor Clay credit consumption vs budget.
- **Month 2**: Scale to 200+ accounts. Optimize enrichment costs by skipping low-value columns for low-score accounts (tiered enrichment: high-priority accounts get full research, low-priority get firmographics only).

Track cost per researched account: target <$2/account at scale (Clay credits + API costs).

### 6. Build the research quality dashboard

Track in PostHog:

- **Automation rate**: % of accounts auto-researched vs manual (target >=80%)
- **Enrichment hit rate**: % of enrichment columns returning data (target >=80%)
- **Brief accuracy**: sampled human review of AI briefs (target >=90% accurate)
- **Reply rate by research depth**: full vs light vs none
- **Signal-to-meeting correlation**: which signals predict meetings (not just replies)
- **Cost per meeting**: total research costs / meetings generated

### 7. Evaluate against threshold

After 2 months, measure:

- Research automation rate: target >=80%
- Reply rate on researched outreach: target >=35% (sustained, not just initial burst)
- A/B test learnings implemented: at least 3 winning variants adopted

**PASS:** >=80% automation AND >=35% sustained reply rate. Proceed to Durable.

**FAIL:** Diagnose:
- Automation rate low: enrichment errors, API failures, or pipeline gaps. Review n8n execution logs.
- Reply rate dropping: message fatigue, signal staleness, or market shift. Review signal decay data.
- Costs too high: optimize tiered enrichment. Skip full research for low-score accounts.

## Time Estimate

- Automation pipeline setup: 12 hours
- Signal detection configuration: 6 hours
- Tool sync workflows: 8 hours
- A/B test design and setup: 6 hours
- Monitoring and optimization (weekly, 2h x 8 weeks): 16 hours
- Scale-up and cost optimization: 8 hours
- Evaluation and documentation: 4 hours
- **Total: ~70 hours over 2 months** (front-loaded in weeks 1-2)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Batch enrichment, Claygent, signal detection, tech stack | Growth: $495/month for 40,000 actions ([clay.com/pricing](https://www.clay.com/pricing)) |
| Instantly | Email sequencing at scale, A/B testing | Hypergrowth: $97/month for 100K emails ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Anthropic API | Account brief generation (Claude Sonnet) | ~$0.03/brief, ~$6/month at 200 accounts ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Attio | CRM — enriched records, deal tracking | Plus: $34/user/month ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Event tracking, funnels, experiments | Free tier: 1M events/month ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Automation workflows (research pipeline, syncs) | Starter: $24/month or self-hosted free ([n8n.io/pricing](https://n8n.io/pricing)) |
| LinkedIn Sales Navigator | Contact research, signal monitoring | Core: $99.99/month ([linkedin.com/sales](https://business.linkedin.com/sales-solutions/compare-plans)) |

**Estimated play-specific cost: ~$600-730/month** (Clay Growth + Instantly Hypergrowth + LinkedIn Sales Nav + Anthropic API)

## Drills Referenced

- the account research automation workflow (see instructions below) — n8n pipeline that auto-researches accounts on arrival and generates AI briefs
- `ab-test-orchestrator` — design and run A/B experiments on hook types, research depth, and messaging
- `tool-sync-workflow` — connect Clay, Instantly, Attio, PostHog, and LinkedIn into zero-silo data flow
- `signal-detection` — monitor for real-time buying signals and trigger research refreshes
