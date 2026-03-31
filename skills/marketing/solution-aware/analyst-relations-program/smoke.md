---
name: analyst-relations-program-smoke
description: >
  Analyst Relations Program — Smoke Test. Research and prioritize 10-15 analysts covering your
  category, prepare tailored briefing documents, request briefings, and validate that analyst
  engagement produces at least 2 completed briefings and constructive positioning feedback.
stage: "Marketing > SolutionAware"
motion: "PartnershipsWarmIntros"
channels: "Other"
level: "Smoke Test"
time: "12 hours over 3 weeks"
outcome: ">=5 briefing requests sent, >=2 briefings completed, and actionable positioning feedback received from at least 1 analyst within 3 weeks"
kpis: ["Briefing requests sent", "Briefing acceptance rate", "Briefings completed", "Positioning feedback quality", "Warm paths identified"]
slug: "analyst-relations-program"
install: "npx gtm-skills add marketing/solution-aware/analyst-relations-program"
drills:
  - analyst-target-research
  - briefing-deck-preparation
  - threshold-engine
---

# Analyst Relations Program — Smoke Test

> **Stage:** Marketing > SolutionAware | **Motion:** PartnershipsWarmIntros | **Channels:** Other

## Outcomes

Prove that industry analysts are reachable and interested in your category positioning. At this level, the agent researches analysts, prepares briefing materials, and the founder requests and conducts briefings personally. No automation, no nurture cadences. The goal is signal: can you get analysts to take a briefing and do they provide useful feedback on your positioning?

**Pass threshold:** >=5 briefing requests sent, >=2 briefings completed, and actionable positioning feedback received from at least 1 analyst within 3 weeks.

## Leading Indicators

- At least 3 of 5 briefing requests get a response (positive or redirect) within 10 days
- At least 1 analyst asks follow-up questions during the briefing (indicates genuine interest)
- At least 1 analyst provides specific positioning feedback: how you compare to competitors, what category they would place you in, or what criteria their clients use
- At least 1 warm path exists (mutual connection, customer relationship, or prior interaction)
- Analyst does not reject the briefing for lack of category relevance (validation that you are targeting the right analysts)

## Instructions

### 1. Map the Analyst Landscape

Run the `analyst-target-research` drill at Smoke scale (10-15 analysts):

1. Use the `analyst-landscape-mapping` fundamental to identify analysts across four tiers:
   - **Tier 1 — Major firm analysts:** Gartner, Forrester, IDC analysts who write Magic Quadrants, Waves, or MarketScapes covering your category
   - **Tier 2 — Boutique research firms:** Smaller firms (451 Research, Constellation Research, EMA) with focused coverage
   - **Tier 3 — Independent consultants:** Solo practitioners who advise enterprises on purchasing decisions in your space
   - **Tier 4 — Thought-leader influencers:** People with large followings who influence buyer perception but are not traditional analysts (former Gartner analysts, industry bloggers with advisory businesses)
2. For each analyst, capture: name, firm, coverage area, LinkedIn URL, email, 2-3 recent publications relevant to your space
3. Use `clay-scoring` to score and prioritize: coverage match (40%), buyer access (30%), accessibility (20%), recency of relevant publication (10%)
4. Select top 5-7 analysts for briefing outreach. Focus on Tier 2-3 for Smoke — they are more accessible than Tier 1 and respond faster.

### 2. Identify Warm Paths

Before cold-requesting briefings, check for warm connections:

1. Search Attio for contacts at each analyst's firm or who have mentioned the analyst
2. Check LinkedIn for mutual connections
3. Ask existing customers if they have relationships with any of the target analysts
4. If a warm path exists, request an introduction instead of cold outreach

Log all warm paths in Attio notes on the analyst contact record.

### 3. Prepare Briefing Materials

Run the `briefing-deck-preparation` drill for each target analyst:

1. Use the `briefing-document-creation` fundamental to create a tailored one-pager for each analyst:
   - Use the analyst's published frameworks and terminology (e.g., if a Gartner analyst, align to their Magic Quadrant criteria)
   - Lead with the problem you solve, not your product features
   - Include 2-3 customer proof points with specific metrics
   - Close with what you are asking: "We would like to brief you on our approach to [category] and get your perspective on our positioning"
2. Prepare a 15-20 minute briefing agenda:
   - 5 min: company overview and market context
   - 5 min: differentiated approach and key metrics
   - 5 min: customer evidence
   - 5 min: questions for the analyst (positioning feedback, market dynamics, what they are hearing from buyers)
3. Set up a Cal.com booking link for the briefing using the `calcom-booking-links` fundamental: 30-minute slot, business hours, with buffer time

### 4. Request Briefings

**Human action required:** The founder sends briefing requests personally:

1. For each analyst, send a personalized email or LinkedIn message:
   - Reference their specific recent publication and why it is relevant
   - Explain what you do in one sentence using their terminology
   - State the ask clearly: "I would value 30 minutes to brief you on [topic] and get your perspective"
   - Attach or link the tailored one-pager
   - Include the Cal.com booking link
2. Send 5-7 requests over 1 week (not all at once)
3. If using a warm introduction: have the connector make the intro, then follow up with the briefing one-pager within 24 hours
4. Log every request in Attio: analyst name, date sent, method (email/LinkedIn/warm intro), status

### 5. Conduct Briefings

**Human action required:** The founder leads each briefing:

1. Follow the prepared agenda but allow for conversation — analysts often redirect to what interests them
2. Take detailed notes on:
   - How the analyst categorizes your space
   - Which competitors they mention and how they position them
   - What criteria their clients use to evaluate solutions like yours
   - Specific feedback on your positioning, messaging, or market approach
   - Whether they would be open to including you in future research
3. Ask explicitly: "What would we need to demonstrate to be included in your next [report/wave/quadrant]?"
4. After the briefing, send a thank-you email within 24 hours with any follow-up materials requested

### 6. Evaluate Against Threshold

Run the `threshold-engine` drill:

1. After 3 weeks, compile:
   - Briefing requests sent (threshold: >=5)
   - Briefings completed (threshold: >=2)
   - Actionable positioning feedback received (threshold: at least 1 analyst provided specific, useful feedback)
2. Assess feedback quality: Did you learn how analysts think about your category? Do you now know what criteria matter for inclusion in reports?
3. Calculate: acceptance rate (completed / sent)

**If PASS:** Analysts are reachable and engaged. You have initial relationships and positioning intelligence. Proceed to Baseline with systematic outreach and nurture.

**If FAIL:** Diagnose:
- No responses: you may be targeting the wrong tier. Try more accessible analysts (Tier 3-4 independents). Or your one-pager is not compelling — ask a friendly industry contact to review it.
- Briefings but no useful feedback: you may be pitching instead of briefing. Analysts want to learn about the market, not hear a sales pitch. Lead with data and ask more questions.
- Category mismatch: analysts say you do not fit their coverage. Revisit your category definition and target different analysts.

## Time Estimate

- 4 hours: Analyst landscape research and scoring
- 2 hours: Warm path identification
- 3 hours: Briefing material preparation (one-pager and agenda per analyst)
- 1 hour: Briefing request emails
- 2 hours: Conducting 2 briefings (30 min each + prep + follow-up)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn | Analyst research and outreach | Free — [linkedin.com](https://linkedin.com) |
| Attio | CRM — analyst contacts and briefing tracking | Free plan or $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Cal.com | Scheduling — briefing booking links | Free plan — [cal.com/pricing](https://cal.com/pricing) |
| Clay | Enrichment — analyst contact research | $149/mo (Starter) — [clay.com/pricing](https://www.clay.com/pricing) |
| Claude API | Briefing document drafting | ~$5-10 — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** Free. Clay and Claude API usage minimal; Cal.com has a free tier.

## Drills Referenced

- `analyst-target-research` — identify, research, and prioritize analysts across four tiers using Clay enrichment and scoring
- `briefing-deck-preparation` — prepare analyst-specific briefing documents, meeting agendas, and booking links
- `threshold-engine` — evaluate Smoke test results against the pass threshold and recommend next action
