---
name: ai-sdr-prospecting-baseline
description: >
  AI SDR Prospecting — Baseline Run. First always-on outreach automation using
  AI-researched personalization. Instantly sends AI-personalized email sequences,
  LinkedIn outreach runs in parallel, PostHog tracks the full funnel. Prove that
  AI SDR produces repeatable meetings at 200+ contacts over 2 weeks.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=2% meeting rate from 200 AI-personalized outreach contacts over 2 weeks"
kpis: ["Meeting rate", "Reply rate by outreach angle", "Cost per meeting", "AI research accuracy"]
slug: "ai-sdr-prospecting"
install: "npx gtm-skills add marketing/solution-aware/ai-sdr-prospecting"
drills:
  - ai-prospect-research
  - cold-email-sequence
  - linkedin-outreach
  - posthog-gtm-events
---

# AI SDR Prospecting — Baseline Run

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social

## Outcomes

Baseline proves that AI SDR prospecting is repeatable at 200+ contacts. AI agents research every prospect via Clay Claygent, generating personalized hooks that feed into Instantly email sequences and LinkedIn outreach. PostHog tracks the full funnel from research to reply to meeting. The meeting rate holds at >=2% over 2 weeks with AI-personalized outreach measurably outperforming generic templates.

## Leading Indicators

- AI research briefs completing at 80%+ accuracy rate (verified by spot-checking first 20)
- Instantly email deliverability above 95% (no domain reputation issues)
- Email open rate above 40% (subject lines working)
- Email reply rate above 4% (AI personalization resonating)
- LinkedIn connection acceptance above 25%
- Positive reply rate (meeting interest) above 2% within 7 days of first touch
- At least 1 reply per 50 contacts mentioning the personalized detail
- Cost per meeting below $75

## Instructions

### 1. Scale AI research to 200 prospects

Run the `ai-prospect-research` drill at 4x Smoke volume. Build a prospect list of 200 contacts using the same ICP validated in Smoke. Import into Clay and run the Claygent research columns:

1. Process in batches of 50. After the first batch, verify 10 research briefs for accuracy.
2. Track research quality in PostHog: log `ai_research_completed` events with properties `batch_size`, `quality_pass_rate`, `credits_used`.
3. Filter out any prospects where the research brief returned generic output (no specific facts found). These go to a "low-research" list for non-personalized outreach or discard.
4. Segment the 200 researched prospects by `outreach_angle`: trigger_event, competitive_displacement, pain_match, content_connection. This segmentation determines which email copy variant each prospect receives.

### 2. Build AI-personalized email sequences in Instantly

Run the `cold-email-sequence` drill with AI research variables. Create 4 campaign variants in Instantly, one per outreach angle:

**Trigger Event variant:**
- Email 1: Open with the `personalization_hook` referencing their trigger event. Connect it to the problem your product solves. Under 80 words.
- Email 2: Proof point from a similar customer who faced the same trigger. Under 70 words.
- Email 3: Breakup with Cal.com link. Under 60 words.

**Competitive Displacement variant:**
- Email 1: Open with `personalization_hook` referencing a gap in their current solution (without naming the competitor). Under 80 words.
- Email 2: One specific result from a customer who switched from that category. Under 70 words.
- Email 3: Breakup with Cal.com link. Under 60 words.

**Pain Match variant:**
- Email 1: Open with `personalization_hook` + `pain_hypothesis`. Under 80 words.
- Email 2: Data point quantifying the cost of the pain. Under 70 words.
- Email 3: Breakup with Cal.com link. Under 60 words.

**Content Connection variant:**
- Email 1: Reference the content the prospect published. Tie to a related insight. Under 80 words.
- Email 2: Share a relevant resource or case study. Under 70 words.
- Email 3: Breakup with Cal.com link. Under 60 words.

Map Clay merge fields (`personalization_hook`, `pain_hypothesis`, `similar_customer`, `proof_metric`) to Instantly variables. Set sending schedule: weekdays 7:30-9:30am in the prospect's timezone. Limit to 20 sends per day per sending account. Disable open tracking to reduce spam filter risk.

### 3. Launch LinkedIn outreach in parallel

Run the `linkedin-outreach` drill. Send connection requests to all 200 prospects with personalized notes derived from the `personalization_hook` (reworded to fit LinkedIn's 200-character limit). Follow the 3-message LinkedIn sequence:

- Connection request (Day 2 relative to Email 1)
- Thank-you message (Day 1 after accept): reference a shared interest from the research brief
- Value message (Day 5 after accept): ask about their current approach to the pain area from `pain_hypothesis`

Coordinate timing so LinkedIn and email touches do not overlap on the same day for any prospect.

### 4. Configure event tracking

Run the `posthog-gtm-events` drill to set up tracking for this play. Configure events:

- `ai_sdr_research_completed` — properties: prospect_id, outreach_angle, research_quality_score
- `ai_sdr_email_sent` — properties: campaign_id, outreach_angle, sequence_step, subject_variant
- `ai_sdr_email_replied` — properties: campaign_id, sentiment (positive/negative/neutral), sequence_step, mentioned_personalization (boolean)
- `ai_sdr_linkedin_connected` — properties: campaign_id, days_to_accept
- `ai_sdr_linkedin_replied` — properties: campaign_id, sentiment
- `ai_sdr_meeting_booked` — properties: source_channel, outreach_angle, research_quality_score

Connect Instantly webhooks to PostHog via n8n. Connect Attio deal stage changes to PostHog.

### 5. Execute and monitor for 2 weeks

Let the email sequences run in Instantly. Execute LinkedIn touches daily (15-20 min/day). Monitor:

- **Daily**: check Instantly for bounces, reply sentiment, and deliverability. If bounce rate exceeds 3%, pause and clean the list.
- **Day 5**: review reply rates by outreach angle. If any angle has 0 replies after 50+ sends, revise the copy for that variant.
- **Day 10**: interim evaluation. If overall reply rate is below 2%, investigate whether the issue is research quality (hooks too generic), deliverability (landing in spam), or targeting (wrong ICP segment).

Log every meeting booked in Attio with: source channel, outreach angle, and whether the prospect referenced the personalized detail.

### 6. Evaluate against threshold

Pull PostHog funnel data and Attio deal pipeline. Measure against: **>=2% meeting rate from 200 AI-personalized outreach contacts over 2 weeks**.

- **PASS**: Proceed to Scalable. Document: meeting rate by outreach angle, best-performing personalization types, AI research accuracy vs. meeting correlation, and cost per meeting.
- **FAIL**: Diagnose by checking each stage of the funnel:
  - Research quality low -> revise Claygent prompts, tighten ICP
  - Open rate low (<30%) -> fix subject lines or deliverability
  - Reply rate low but opens high -> copy issue, not research issue
  - Replies but no meetings -> CTA or offer problem
  Adjust and re-run Baseline.

Also record: A/B performance of outreach angle variants, cost per meeting by channel, and which research quality score ranges produced the best outcomes.

## Time Estimate

- AI research at 200 contacts (4 batches, review, quality control): 4 hours
- Email sequence setup in Instantly (4 variants, merge field mapping): 3 hours
- LinkedIn outreach setup and daily execution: 4 hours (20 min/day over 2 weeks)
- PostHog event tracking configuration: 2 hours
- Monitoring and mid-flight adjustments: 3 hours
- Evaluation and documentation: 2 hours

Total: ~18 hours over 2 weeks.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | AI research via Claygent + enrichment waterfall | Launch: $185/mo for 2,500 data credits (https://www.clay.com/pricing) |
| Instantly | Cold email sequencing (4 campaign variants) | Growth: $37/mo or $30/mo annual (https://instantly.ai/pricing) |
| Apollo | Contact sourcing at 200+ volume | Basic: $49/user/mo annual (https://www.apollo.io/pricing) |
| Attio | CRM deal tracking + research notes | Plus: $29/user/mo (https://attio.com/pricing) |
| PostHog | Event tracking + funnel analysis | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Cal.com | Meeting booking links | Free tier (https://cal.com/pricing) |

**Estimated play-specific cost: ~$270-330/mo** (Clay Launch + Instantly Growth + Apollo Basic)

## Drills Referenced

- `ai-prospect-research` — AI-driven per-prospect research generating personalization hooks, pain hypotheses, and outreach angles for all 200 contacts
- `cold-email-sequence` — build and launch 4 outreach-angle-specific email sequences in Instantly with AI-generated merge variables
- `linkedin-outreach` — parallel LinkedIn connection and messaging sequence using research brief context
- `posthog-gtm-events` — configure event taxonomy for tracking AI SDR funnel from research to meeting
