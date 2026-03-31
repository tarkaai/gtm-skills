---
name: ai-sdr-prospecting-scalable
description: >
  AI SDR Prospecting — Scalable Automation. Scale AI-researched outreach to
  1,000 contacts/week with full automation: n8n orchestrates Clay research,
  Instantly email sequences, and LinkedIn outreach. Intent signals feed the
  prospect pipeline continuously. A/B test outreach angles, personalization
  depth, and timing. Maintain >=1.6% meeting rate at 5-10x Baseline volume.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: ">=1.6% meeting rate at 1,000 contacts/week sustained over 3 months"
kpis: ["Weekly volume", "Meeting rate", "Cost per meeting", "Outreach angle conversion by segment", "AI research quality at scale"]
slug: "ai-sdr-prospecting"
install: "npx gtm-skills add marketing/solution-aware/ai-sdr-prospecting"
drills:
  - intent-signal-automation
  - follow-up-automation
  - tool-sync-workflow
  - ab-test-orchestrator
---

# AI SDR Prospecting — Scalable Automation

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social

## Outcomes

Scalable is the 10x multiplier. Move from 200 contacts in 2 weeks to 1,000 contacts per week without proportional effort. n8n orchestrates the full pipeline: intent signals trigger prospect discovery, Clay runs AI research automatically, Instantly sends personalized sequences, and LinkedIn outreach runs in parallel. A/B testing identifies winning outreach angles, personalization approaches, and timing. The meeting rate holds within 20% of Baseline (>=1.6%) at 5-10x volume.

## Leading Indicators

- Automated prospect pipeline producing 250+ new AI-researched contacts per week
- AI research quality staying above 75% accuracy at scale (spot-checked weekly)
- Email deliverability above 95% across all sending accounts
- Meeting rate stable within 20% of Baseline benchmark week-over-week
- A/B tests producing statistically significant winners within 2-week cycles
- Cost per meeting declining month-over-month as winning variants compound
- Intent-signal-sourced prospects converting at 2x+ rate versus cold-sourced
- Cross-channel suppression working (no prospect receives email and LinkedIn on the same day)

## Instructions

### 1. Deploy intent signal automation for continuous prospect discovery

Run the `intent-signal-automation` drill to build always-on n8n workflows that replace manual list building:

1. **Website visitor workflow**: Configure RB2B or Koala to identify website visitors. n8n webhook receives visitor data, filters for high-intent pages (pricing, case studies, docs), sends to Clay for intent scoring. Hot-tier visitors (score 70+) auto-enter the AI research pipeline. Warm-tier visitors (40-69) go to a watch list.
2. **Third-party intent workflow**: Connect G2 buyer intent or Bombora signals via n8n. Companies researching your category or competitors trigger automatic Clay enrichment and scoring.
3. **Enrichment refresh workflow**: Weekly n8n cron refreshes contextual signals (funding, hiring, tech changes) for all accounts in the target list. Score changes trigger re-routing: accounts that moved from cold to warm/hot enter the outreach queue.

Combine intent-sourced prospects with Apollo-sourced lists to maintain 1,000+ contacts per week. Tag each contact with source type (`intent_website`, `intent_g2`, `cold_sourced`) for attribution analysis.

### 2. Automate AI research at scale

Build an n8n workflow that runs the `ai-prospect-research` drill automatically:

1. **Trigger**: new contact added to the "Research Queue" Attio list (via intent signals or batch import)
2. **Clay HTTP POST**: send contact data to Clay table for Claygent research (research_brief, personalization_hook, pain_hypothesis, outreach_angle)
3. **Wait 60 seconds** for Clay enrichment to complete
4. **Clay HTTP GET**: retrieve research results
5. **Quality filter**: if `research_quality_score` < 50, move to "Low Research" Attio list (these get a generic but still segmented sequence). If >= 50, proceed.
6. **Route by outreach_angle**: send to the appropriate Instantly campaign variant
7. **Log**: fire PostHog `ai_sdr_research_completed` event with quality metrics

Process 50-100 contacts per batch via n8n. Set rate limits to avoid Clay API throttling. Monitor Claygent credit consumption weekly.

### 3. Build automated cross-channel follow-ups

Run the `follow-up-automation` drill to create n8n workflows for:

- **Email opened 3+ times, no reply**: Bump to LinkedIn follow-up with a message referencing the email topic. Wait 48 hours after last open.
- **LinkedIn connection accepted**: Trigger the LinkedIn message sequence. Adjust the next email step to reference the connection: "Great connecting on LinkedIn..."
- **Positive reply on any channel**: Stop all automation for that prospect. Create Attio deal at "Interested" stage. Notify founder via Slack with the research brief attached for call prep.
- **Meeting booked**: Cancel remaining sequence steps across both channels. Update Attio deal to "Meeting Booked". Confirm via Cal.com.
- **Negative reply**: Stop all outreach. Tag in Attio as "Not Interested" with the reason extracted from the reply. Add to suppression list.

### 4. Connect all tools via sync workflows

Run the `tool-sync-workflow` drill to build n8n sync workflows:

- Clay research output -> Attio contact notes and custom attributes
- Instantly reply events -> Attio deal creation (positive) or contact tagging (negative)
- LinkedIn automation events -> Attio contact record updates
- All events -> PostHog for unified funnel tracking
- Attio deal stage changes -> PostHog for pipeline attribution

Ensure no data is siloed. Every prospect interaction across email and LinkedIn is visible in both Attio and PostHog.

### 5. Launch A/B testing across the pipeline

Run the `ab-test-orchestrator` drill. Design experiments at each stage:

**Research-level experiments:**
- Claygent prompt variants: test different research questions to see which produce higher-quality hooks
- Personalization depth: test detailed research briefs (3-4 facts) vs. single-fact hooks

**Email experiments (via Instantly A/B):**
- Outreach angle performance: compare trigger_event vs. competitive_displacement vs. pain_match conversion rates
- Subject line variants per outreach angle
- First-line personalization vs. third-line personalization placement
- Send timing: 7:30am vs. 10am vs. 2pm in prospect timezone

**LinkedIn experiments:**
- Connection note: research-based vs. mutual-interest-based vs. question-based
- Follow-up timing: Day 1 after accept vs. Day 3 after accept

Use PostHog feature flags to randomly assign prospects to variants. Run each test for minimum 100 prospects per variant. Declare winner at 95% confidence. Implement winner and start next test. Log all experiments in Attio as campaign notes.

### 6. Scale volume to 1,000 contacts/week

Ramp volume gradually over 3 months:
- Month 1: 500 contacts/week (validate automation pipeline, fix integration bugs)
- Month 2: 750 contacts/week (start A/B testing, optimize winning angles)
- Month 3: 1,000 contacts/week (full scale, compound winning variants)

Scale infrastructure in parallel:
- Add Instantly sending accounts as needed (maintain 20 emails/day per account limit)
- Increase Clay data credits if approaching monthly limit
- Add LinkedIn automation capacity if acceptance rates support it (never exceed 20 connection requests/day)

Monitor guardrails daily in PostHog:
- Meeting rate must stay within 20% of Baseline benchmark
- Email bounce rate must stay below 3%
- Negative reply rate must stay below 5%
- If any guardrail is breached, pause volume increase and diagnose

### 7. Monitor and evaluate over 3 months

Track weekly in PostHog dashboards:
- Total prospects in pipeline by source (intent vs. cold)
- AI research quality score distribution
- Meeting rate by outreach angle, prospect tier, and source type
- Cost per meeting trending (total tool spend / meetings booked)
- A/B test results and cumulative wins

**Pass threshold: >=1.6% meeting rate at 1,000 contacts/week sustained over 3 months.**

- **PASS**: Document the complete automated pipeline, winning outreach angles, optimal personalization approach, and intent signal ROI. Proceed to Durable.
- **FAIL**: Identify the bottleneck:
  - If AI research quality degraded at scale -> refine Claygent prompts, tighten source data
  - If deliverability dropped -> reduce volume per sending account, rotate domains
  - If intent signals not producing better conversions -> re-evaluate signal scoring model
  - If cost per meeting rose -> identify which scaling step caused efficiency loss
  Fix and re-run at current volume until stable.

## Time Estimate

- Intent signal automation setup: 8 hours
- AI research automation in n8n: 6 hours
- Follow-up automation and tool sync: 8 hours
- A/B test design and setup: 6 hours
- LinkedIn outreach management: 12 hours (30 min/day over 3 months for monitoring)
- Weekly monitoring, analysis, and optimization: 18 hours (1.5 hrs/week)
- Volume scaling and infrastructure management: 8 hours
- Evaluation and documentation: 4 hours
- Buffer for debugging automation issues: 5 hours

Total: ~75 hours over 3 months.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | AI research via Claygent at scale + enrichment | Growth: $495/mo for scaled credits (https://www.clay.com/pricing) |
| Instantly | Cold email sequencing (multiple campaign variants) | Hypergrowth: $97/mo for 100K emails (https://instantly.ai/pricing) |
| Apollo | Contact sourcing at volume | Professional: $79/user/mo annual (https://www.apollo.io/pricing) |
| Dripify | LinkedIn automation sequences | Pro: $59/user/mo annual (https://dripify.com/pricing) |
| LinkedIn Sales Navigator | Prospecting + advanced search | Core: $99.99/mo or $79.99/mo annual (https://business.linkedin.com/sales-solutions) |
| RB2B / Koala | Website visitor identification | RB2B: Free tier or $99/mo; Koala: $99/mo (https://www.rb2b.com/pricing) |
| n8n | Orchestration of full pipeline | Starter: $20/mo (https://n8n.io/pricing) |
| Attio | CRM + pipeline tracking | Plus: $29/user/mo (https://attio.com/pricing) |
| PostHog | Analytics + experiments + funnels | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Cal.com | Meeting booking | Free tier (https://cal.com/pricing) |

**Estimated play-specific cost: ~$830-1,050/mo** (Clay Growth + Instantly Hypergrowth + Apollo Pro + Dripify + Sales Nav + RB2B/Koala)

## Drills Referenced

- `intent-signal-automation` — always-on n8n workflows collecting website visitor, G2, and enrichment signals to feed the prospect pipeline continuously
- `follow-up-automation` — automated cross-channel follow-ups that respond to email opens, LinkedIn accepts, and positive/negative replies
- `tool-sync-workflow` — n8n sync workflows connecting Clay, Instantly, LinkedIn automation, Attio, and PostHog into a single data flow
- `ab-test-orchestrator` — A/B testing framework for research prompts, outreach angles, email copy, LinkedIn messages, and timing
