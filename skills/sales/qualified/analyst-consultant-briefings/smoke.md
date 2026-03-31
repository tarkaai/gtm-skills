---
name: analyst-consultant-briefings-smoke
description: >
  Analyst & Consultant Briefings — Smoke Test. Identify 5-10 niche analysts or consultants
  who influence your buyers, prepare tailored briefing documents, and secure at least 1
  intro meeting within 1 week. Validates that analysts in your space will take briefings.
stage: "Sales > Qualified"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: ">=1 analyst or consultant briefing meeting completed in 1 week"
kpis: ["Briefing requests sent", "Briefings scheduled", "Briefing acceptance rate", "Follow-up requests from analysts"]
slug: "analyst-consultant-briefings"
install: "npx gtm-skills add sales/qualified/analyst-consultant-briefings"
drills:
  - analyst-target-research
  - briefing-deck-preparation
  - threshold-engine
---

# Analyst & Consultant Briefings — Smoke Test

> **Stage:** Sales → Qualified | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Outcomes

Prove that industry analysts and consultants in your space will accept briefing requests, meet with you, and engage substantively enough to become a referral channel. At this level, everything is manual: you research analysts, prepare briefing materials, send outreach, and conduct meetings yourself. One completed briefing meeting is the signal that this channel works.

**Pass threshold:** >=1 analyst or consultant briefing meeting completed in 1 week.

## Leading Indicators

- Briefing request open rate (target: >=50% — if they are not opening, subject lines or targeting are wrong)
- Briefing request reply rate (target: >=25% — analysts who cover your space should respond)
- Time from outreach to scheduled meeting (target: <5 business days for Tier 3-4 analysts)
- Analyst engagement during the briefing (do they ask follow-up questions, or are they just being polite?)

## Instructions

### 1. Identify target analysts and consultants

Run the `analyst-target-research` drill to build your initial target list. At Smoke level, keep it focused: identify 5-10 analysts and consultants who directly cover your market category. Prioritize Tier 3 (independent consultants) and Tier 4 (thought-leader influencers) over Tier 1-2 (large firms) — they are faster to access and more likely to accept a first briefing.

Use Clay to enrich each analyst with email, LinkedIn URL, and recent publications. Score them on coverage relevance, buyer access, and accessibility. Export scored analysts to an Attio list called "Analyst Briefing Targets."

### 2. Research each analyst's recent work

For each target, read their 2-3 most recent publications, talks, or social media posts about your market. Note:
- The terminology they use for your category (match it exactly in your outreach)
- Their evaluation criteria or framework (if they publish one)
- Competitors they have covered or recommended
- Opinions they hold about where the market is heading

Store these notes on each analyst's Attio contact record. This context is essential for step 3.

### 3. Prepare briefing materials

Run the `briefing-deck-preparation` drill for your top 5 analysts. For each, generate:
- A tailored one-page briefing document using the Claude API, customized to the analyst's coverage area and terminology
- A 30-minute meeting agenda with 3 discussion topics relevant to the analyst's interests
- A short briefing request message (under 150 words) that references their recent work

**Human action required:** Review every briefing document before sending. Verify metrics are accurate and competitive positioning is defensible. Edit discussion topics to reflect what you genuinely want their perspective on.

### 4. Send briefing requests

**Human action required:** Send briefing requests personally — email or LinkedIn DM, depending on your relationship and the analyst's accessibility. Do NOT use automated sequences at Smoke level. Personalize each message.

For each request:
- Open with a reference to their specific recent work (proves you did homework)
- One sentence on what your company does using their terminology
- State the ask: 30 minutes to share your approach and get their perspective
- Include a Cal.com booking link
- Attach or link the briefing document

Log each outreach in Attio: date sent, channel used, analyst response status.

### 5. Conduct the briefing

**Human action required:** Conduct each briefing personally. Follow the prepared agenda:
- Minutes 0-2: Introductions, thank them for their time, set the context
- Minutes 2-10: Company overview and market positioning (use the briefing document as a guide, not a script)
- Minutes 10-18: Deep dive on your approach, product, or technical differentiation
- Minutes 18-25: Discussion on the prepared topics — ask for their perspective on market direction
- Minutes 25-28: Ask directly: "Who in your network would benefit from learning about what we are building?"
- Minutes 28-30: Next steps — offer to send updates quarterly, ask what format they prefer

Take notes during the call. If the analyst asks follow-up questions or requests additional materials, that is a strong engagement signal — log it in Attio.

### 6. Evaluate against threshold

Run the `threshold-engine` drill to evaluate: did you complete >=1 analyst briefing meeting?

If PASS: Document what worked (which analysts responded, what messaging resonated, which tier was most receptive). Proceed to Baseline.

If FAIL: Diagnose — was the issue low response rate (targeting or messaging problem), scheduling difficulty (need more lead time), or no analysts found in your space (market category may be too niche for formal analyst coverage — consider pivoting to consultant and influencer outreach)? Adjust and re-run.

## Time Estimate

- 1 hour: Analyst research, scoring, and list building (using `analyst-target-research` drill)
- 30 minutes: Briefing document preparation (using `briefing-deck-preparation` drill + human review)
- 30 minutes: Send 5 personalized briefing requests
- 30 minutes: Conduct 1 briefing meeting
- 30 minutes: Document findings, evaluate threshold, log outcomes

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Analyst enrichment and research | Launch $185/mo, Growth $495/mo — [clay.com](https://www.clay.com) |
| Attio | Store analyst records, track outreach | Free tier or existing plan — [attio.com](https://attio.com) |
| Cal.com | Schedule briefing meetings | Free tier (1 event type) — [cal.com/pricing](https://cal.com/pricing) |
| Claude API | Generate briefing documents | ~$0.03-0.05 per document (Sonnet 4.6) — [anthropic.com](https://console.anthropic.com) |

**Estimated play-specific cost:** Free (using free tiers + existing Clay plan) to ~$20 (if Clay credits needed for enrichment)

## Drills Referenced

- `analyst-target-research` — Identifies, enriches, and scores analysts who influence your buyers
- `briefing-deck-preparation` — Generates tailored briefing documents and meeting agendas per analyst
- `threshold-engine` — Evaluates results against the pass threshold
