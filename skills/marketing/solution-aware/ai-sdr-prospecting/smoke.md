---
name: ai-sdr-prospecting-smoke
description: >
  AI SDR Prospecting — Smoke Test. Use AI agents to research 50 solution-aware
  prospects, generate personalized outreach hooks, and manually execute
  founder-sent email and LinkedIn outreach to validate that AI-researched
  personalization produces meetings within 1 week.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=2 meetings booked from 50 AI-researched prospects in 1 week"
kpis: ["Response rate", "Personalization accuracy", "Time to first reply"]
slug: "ai-sdr-prospecting"
install: "npx gtm-skills add marketing/solution-aware/ai-sdr-prospecting"
drills:
  - icp-definition
  - build-prospect-list
  - ai-prospect-research
  - threshold-engine
---

# AI SDR Prospecting — Smoke Test

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social

## Outcomes

The Smoke Test proves that AI-driven prospect research produces outreach personalization good enough to book meetings with solution-aware prospects. Success means at least 2 meetings booked from 50 AI-researched prospects within 1 week. No automation, no paid tools beyond free tiers. The founder executes outreach manually using AI-generated research briefs and personalization hooks.

## Leading Indicators

- AI research briefs that surface specific, verifiable facts about each prospect (not generic company descriptions)
- Personalization hooks that reference a real event, publication, or signal per prospect
- Positive email replies within 48 hours mentioning the personalized detail
- LinkedIn connection acceptance rate above 30%
- At least 1 reply that explicitly references the personalized opener ("Thanks for mentioning my post on...")

## Instructions

### 1. Define your ICP for AI SDR prospecting

Run the `icp-definition` drill. Document firmographic criteria (company size, industry, funding stage), buyer persona (title, seniority, department), top 3 pain points, and 3 triggering events that make outbound timely. Write disqualification criteria. For AI SDR prospecting specifically, add a section on what "solution-aware" means for your product: which alternative solutions are these prospects currently evaluating, and what specific gaps does your product fill versus those alternatives.

Output: a one-page ICP document and scoring criteria loaded into Clay.

### 2. Build a prospect list of 50 contacts

Run the `build-prospect-list` drill. Source contacts from Apollo matching your ICP. Import into Clay, run the enrichment waterfall to fill email addresses and LinkedIn URLs. Score each contact. Filter to the top 50 by score. Push to Attio with tags `play:ai-sdr-prospecting` and `level:smoke`.

Requirements per contact: verified email address, LinkedIn profile URL. Reject any contacts where email verification fails.

### 3. Run AI research on all 50 prospects

Run the `ai-prospect-research` drill. Configure Clay Claygent columns to generate:

- A research brief per prospect (company context, recent activity, pain signals, competitive context)
- A personalization hook (one-sentence opener referencing a specific fact)
- A pain hypothesis (what problem this prospect likely has)
- An outreach angle classification (trigger_event, competitive_displacement, pain_match, or content_connection)

Process in 2 batches of 25. After the first batch, manually verify the top 5 research briefs for factual accuracy. Check that the personalization hooks reference real events, not hallucinated ones. If accuracy is below 80%, revise the Claygent prompt and re-run.

### 4. Write outreach copy using AI research output

Using the AI research output, write two outreach channels:

**Email (3-step sequence, sent manually):**
- Email 1 (Day 1): Open with the `personalization_hook` from Clay. Follow with one sentence connecting their `pain_hypothesis` to your product. Soft question as CTA. Under 80 words total.
- Email 2 (Day 4): One proof point from a customer similar to the prospect. Reference the `outreach_angle` to frame it. Under 70 words.
- Email 3 (Day 7): Breakup email. Include Cal.com booking link. Under 60 words.

**LinkedIn (2-step, sent manually):**
- Connection request (Day 2): Reference the same fact from the `personalization_hook` but reworded for LinkedIn's 200-character limit.
- Follow-up message (Day 5, if connected): Ask a question about the pain area from `pain_hypothesis`. No pitch.

### 5. Execute outreach manually

**Human action required:** Send all emails from your personal email client. Send LinkedIn connection requests and messages manually. This is NOT automated. You are proving that AI-generated research produces better outreach than generic templates.

Follow this timing across 7 days:
- Day 1: Send Email 1 to all 50 prospects
- Day 2: Send LinkedIn connection requests to all 50
- Day 4: Send Email 2 to non-responders
- Day 5: Send LinkedIn follow-up to accepted connections
- Day 7: Send Email 3 (breakup) to remaining non-responders

Log every touchpoint in Attio immediately: channel, step, response, sentiment, and whether the prospect referenced the personalized detail.

### 6. Evaluate against threshold

Run the `threshold-engine` drill. Pull data from Attio. Count meetings booked. Compare against: **>=2 meetings booked from 50 AI-researched prospects in 1 week**.

- **PASS**: Proceed to Baseline. Document: which outreach angles produced the most replies, which personalization hooks resonated, and how AI research quality correlated with response rate.
- **FAIL**: Diagnose — was it research quality (hooks were generic or inaccurate), targeting (wrong ICP), or messaging (good research but poor copy)? Adjust and re-run Smoke.

Also record: AI research accuracy rate, reply rate by outreach angle, and qualitative notes on which personalization types performed best.

## Time Estimate

- ICP definition: 45 minutes
- List building and enrichment: 45 minutes
- AI research execution and quality review: 1.5 hours
- Outreach copy writing: 30 minutes
- Manual outreach execution across 7 days: 1.5 hours (15-20 min/day)
- Logging and evaluation: 1 hour

Total: ~6 hours of active work spread over 1 week.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | AI prospect research via Claygent + enrichment | Free tier: 100 credits/mo (https://www.clay.com/pricing) |
| Apollo | Contact sourcing | Free tier: 10,000 email credits/yr (https://www.apollo.io/pricing) |
| Attio | CRM for logging outreach and research notes | Free tier: 3 users (https://attio.com/pricing) |
| Cal.com | Booking link in breakup email | Free tier (https://cal.com/pricing) |
| PostHog | Event tracking for research quality metrics | Free tier: 1M events/mo (https://posthog.com/pricing) |

**Estimated play-specific cost: $0** (free tiers sufficient for Smoke)

## Drills Referenced

- `icp-definition` — define ideal customer profile with scoring criteria and solution-aware competitive context
- `build-prospect-list` — source, enrich, and qualify 50 contacts in Clay and push to Attio
- `ai-prospect-research` — run AI agents to generate per-prospect research briefs, personalization hooks, and outreach angles
- `threshold-engine` — evaluate pass/fail against >=2 meetings threshold
