---
name: competitive-objection-handling-smoke
description: >
  Competitive Objection Handling — Smoke Test. Handle 5 competitive objections manually using
  structured battlecard research and positioning frameworks. Validate that data-backed
  competitive responses maintain deal engagement better than improvised responses.
stage: "Sales > Aligned"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=3 of 5 competitive deals maintain engagement (next meeting booked or positive reply) within 1 week of competitive objection"
kpis: ["Competitive engagement retention rate", "Positioning framework selection accuracy", "Battlecard research quality", "Time from objection to structured response"]
slug: "competitive-objection-handling"
install: "npx gtm-skills add sales/aligned/competitive-objection-handling"
drills:
  - competitive-battlecard-assembly
  - competitive-objection-response
  - threshold-engine
---

# Competitive Objection Handling — Smoke Test

> **Stage:** Sales > Aligned | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Handle 5 competitive objections using structured battlecard research and positioning frameworks instead of improvised responses. Prove that data-backed competitive positioning maintains deal engagement at a higher rate than winging it. This is a manual test — the agent helps prepare battlecards and draft responses, the human delivers them.

## Leading Indicators

- Battlecard research completed for each competitor before responding (not after)
- Positioning framework selected based on objection type, not guesswork
- Trap questions asked during the call that surfaced competitor weaknesses organically
- Prospect acknowledged a differentiator or asked a follow-up question about it
- Follow-up email sent within 24 hours with positioning-aligned content

## Instructions

### 1. Identify 5 competitive deals in your pipeline

Review your current Attio pipeline for deals where a competitor has been mentioned or is suspected. Prioritize deals that are:
- In "Demo," "Proposal," or "Negotiation" stage
- Active (last activity within 7 days)
- High enough value to warrant competitive prep

If you don't have 5 deals with known competitors, include deals where you suspect competition based on: the prospect mentioned "evaluating options," the deal is stalling without clear reason, or the prospect asked feature-specific questions that sound like they're comparing.

Log each deal in Attio with:
- `competitor_mentioned`: the competitor name (or "suspected" if unconfirmed)
- `competitive_objection_type`: classify as `active_evaluation`, `incumbent_loyalty`, `feature_comparison`, `price_comparison`, `social_proof`, or `switching_cost`

### 2. Build battlecards for each competitor

Run the `competitive-battlecard-assembly` drill for each unique competitor across your 5 deals. For Smoke level, the drill runs in manual-assist mode:

- Query Attio for any historical deal data involving this competitor
- If you have 3+ deals with this competitor, the drill synthesizes patterns from those deals
- If fewer than 3, the drill uses Clay enrichment + web research to build an initial battlecard:
  - Scrape competitor's pricing page, features page, and recent changelog
  - Search for G2/Capterra comparisons
  - Search for competitor customer reviews mentioning strengths and weaknesses
  - Pull competitor company data (size, funding, tech stack)

Store each battlecard in Attio on the Competitor record. You should have:
- Their top 3 strengths (from buyer quotes or public reviews)
- Their top 3 weaknesses (from buyer quotes or public reviews)
- 3 trap questions that surface their gaps without naming them
- A pricing comparison (if pricing is public or known from past deals)

### 3. Prepare positioning responses for each deal

For each of the 5 deals, run the `competitive-objection-response` drill in preparation mode:

1. Pull the deal's pain data and decision criteria from Attio
2. Match the prospect's decision criteria against the battlecard's comparison dimensions
3. Identify the hinge criterion — where we have the biggest advantage that the prospect cares about
4. Generate a positioning response: verbal response, trap questions, follow-up email, and champion ammunition
5. Select a supporting asset to prepare (TCO comparison, feature matrix, customer case study, or migration guide)

**Human action required:** Review each generated response. Edit the verbal response to match your voice. Verify that comparison claims are factually accurate. Prepare the supporting asset if it doesn't exist yet.

### 4. Deliver the competitive response

**Human action required:** On your next call or in a follow-up email for each of the 5 deals:

1. **Acknowledge the competitor respectfully.** Never disparage. Say something like: "They've built a good product. The real question is which approach best solves {their top pain} for your specific situation."
2. **Ask the trap questions.** These are designed to surface the competitor's gaps naturally. Let the prospect discover the difference.
3. **Present the hinge criterion.** Focus the conversation on the dimension where you have the strongest advantage that aligns with their stated pain.
4. **Send the follow-up email within 24 hours.** Include the supporting asset. Lead with their pain, not features. End with a clear next step.

For each deal, log in Attio within 1 hour of delivery:
- Which positioning framework you used
- How the prospect responded (exact quote if possible)
- Whether the prospect engaged with the follow-up content
- The competitive outcome: `differentiated`, `partially_differentiated`, `lost_on_criteria`, or `too_early_to_tell`

### 5. Evaluate against threshold

Run the `threshold-engine` drill to evaluate results. The engine checks:
- Of the 5 competitive deals, how many maintained engagement (next meeting booked or positive reply) within 1 week of the competitive objection?
- Target: >= 3 out of 5

If **PASS**: Structured competitive positioning works better than improvised responses. You have validated the battlecard + framework approach. Proceed to Baseline to automate detection and response preparation.

If **FAIL**: Diagnose why:
- **Battlecard quality:** Were the competitor strengths/weaknesses accurate? If prospects contradicted your battlecard, the intel needs improvement.
- **Framework selection:** Did you pick the right positioning framework for the objection type? Review: was the hinge criterion actually what the prospect cared about?
- **Delivery:** Was the response delivered too late (> 48 hours after objection)? Timing matters in competitive deals.
- **Deal quality:** Were these deals already too far gone? The prospect may have already decided before your response.

Re-run with adjustments.

## Time Estimate

- Pipeline review and deal identification: 1 hour
- Battlecard research (5 competitors, some overlap): 2 hours
- Response preparation (5 deals x 20 min): 1.5 hours
- Competitive conversations/follow-ups (5 x 30 min avg): 2.5 hours
- Threshold evaluation: 1 hour
- **Total: ~8 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, competitor records, battlecard storage | Free tier (up to 3 users); Plus $29/user/mo |
| Clay | Competitor enrichment, web scraping for battlecard research | Free tier (100 credits); Launch $185/mo |
| Claude API (Anthropic) | Competitive positioning generation, battlecard synthesis | Sonnet: $3/$15 per M tokens; ~$0.20-0.50 per deal |
| Fireflies | Call recording and transcription | Free (800 min/mo); Pro $10/user/mo |
| PostHog | Track competitive outcomes | Free tier (1M events/mo) |

**Estimated play-specific cost at Smoke:** Free (all tools have free tiers sufficient for 5 deals)

## Drills Referenced

- `competitive-battlecard-assembly` — Research competitors, synthesize deal data and public intel into structured battlecards in Attio
- `competitive-objection-response` — Classify the objection, pull battlecard, generate positioning response, log outcome
- `threshold-engine` — Evaluate results against pass/fail criteria
