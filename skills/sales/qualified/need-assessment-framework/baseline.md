---
name: need-assessment-framework-baseline
description: >
  Need Assessment Framework — Baseline Run. First always-on need assessment with automated outreach
  feeding discovery calls, structured need scoring after every call, and continuous tracking of
  which need profiles predict deal progression. Proves need assessment works repeatably over 2 weeks.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Email, Direct"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=80% of opportunities have completed need assessments over 2 weeks with need score predicting deal progression within 15% accuracy"
kpis: ["Need assessment completion rate", "Need score correlation with deal progression", "Disqualification rate", "Deal velocity by need tier", "Hypothesis accuracy (pre-call vs post-call delta)"]
slug: "need-assessment-framework"
install: "npx gtm-skills add sales/qualified/need-assessment-framework"
drills:
  - cold-email-sequence
  - linkedin-outreach
  - enrich-and-score
  - posthog-gtm-events
---

# Need Assessment Framework — Baseline Run

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Outcomes

Prove that need assessment works repeatably with automated outreach feeding the top of the funnel. Over 2 weeks, assess 30+ prospects through discovery calls and achieve >=80% completion rate on all opportunities. The need scoring model should produce consistent, actionable results — High Need deals should be progressing through your pipeline while Low Need prospects are correctly filtered out. Need scores should predict deal progression (demo acceptance, proposal delivery) within 15% accuracy.

## Leading Indicators

- Reply rate on cold outreach is >=5% (enough to fill the discovery call pipeline)
- Discovery calls are being scheduled at 3+ per week
- Need scores from discovery calls are distributed across the spectrum (not clustering)
- Need-to-product mapping is clear: for each Critical need identified, there is a specific product capability that addresses it
- High Need prospects (score >=15) are requesting demos at a higher rate than Medium Need prospects (12-14)
- The same 2-3 need categories keep appearing as Critical across multiple prospects — this validates your core value proposition

## Instructions

### 1. Scale the prospect list and enrich for need signals

Run the `enrich-and-score` drill to build a list of 80-120 prospects. Use Clay's enrichment waterfall to populate need-relevant signals for each prospect:

- **Job posting signals:** Active listings mentioning pain points related to your need categories (e.g., hiring for roles that your product automates suggests "reducing manual work" need)
- **Tech stack signals:** Current tools from BuiltWith/Wappalyzer — gaps in their stack that your product fills indicate unmet needs
- **Growth signals:** Headcount growth, funding rounds, new office openings suggest scaling needs
- **Industry signals:** Regulatory changes, market shifts, or competitive pressure creating urgency

For each prospect, generate a pre-call need hypothesis: which of your 5-7 need categories are likely relevant based on enrichment data. Push scored prospects to Attio with hypothesis scores.

### 2. Build the need-to-product mapping

Document exactly how each need category maps to specific product capabilities and customer outcomes. For each need category:

- What product feature or workflow addresses this need?
- What is the typical before/after scenario?
- What outcome can you promise (time saved, error reduction, cost savings)?
- What existing customer's story best illustrates this need being solved?

Store this mapping in Attio campaign notes. It feeds the discovery call question bank and post-call follow-up content.

### 3. Launch cold email sequences

Run the `cold-email-sequence` drill to set up a 4-step email sequence in Instantly. Personalize the first line using need-relevant signals from Clay:

- For prospects with strong scaling signals: lead with "scaling without adding headcount" angle
- For prospects with tech stack gaps: reference their current tools and the friction you eliminate
- For prospects with relevant job postings: reference the role they are hiring for and how your product reduces that need

Set up A/B testing on subject lines (2 variants minimum). Configure Instantly to detect positive replies and route them to Attio as hot leads.

### 4. Launch LinkedIn outreach in parallel

Run the `linkedin-outreach` drill to set up connection requests + follow-up messages. Focus LinkedIn messages on need validation: ask about their biggest operational challenge or what they would automate first if they could. These responses provide pre-call need intelligence even before a formal discovery call.

### 5. Configure qualification tracking

Run the `posthog-gtm-events` drill to set up event tracking for the need assessment funnel:

- `need_outreach_sent` — cold email or LinkedIn message sent
- `need_reply_received` — positive reply detected
- `need_discovery_scheduled` — call booked via Cal.com
- `need_assessment_completed` — call held and scored
- `need_qualified` — total score >=12, >=2 Critical needs
- `need_nurture` — close to threshold, added to nurture
- `need_disqualified` — total score well below threshold

Connect PostHog to Attio via n8n webhook so deal stage changes fire the corresponding events.

### 6. Run discovery calls and score

**Human action required:** Conduct discovery calls as they get booked from outreach replies.

For each call, run the the need discovery call workflow (see instructions below) drill:
1. Pre-call: review enrichment data and need hypothesis, generate tailored questions focused on unexplored or uncertain categories
2. During the call: probe each need category for severity, business impact, prior solution attempts, and urgency
3. Post-call: extract need signals from Fireflies transcript using the call transcript need extraction workflow (see instructions below), assign per-category severity scores, update Attio
4. Route: move deal to the correct pipeline stage based on total score and Critical need count

Track the delta between pre-enrichment hypothesis scores and post-call scores for each prospect. This calibrates your enrichment model.

### 7. Analyze need patterns by segment

After 2 weeks, analyze:
- Which ICP segments have the highest average need scores?
- Which need category combinations appear most often in High Need prospects?
- Do certain need profiles correlate with faster deal velocity?
- Are there need categories that never score Critical? Consider dropping them or redefining them.

### 8. Evaluate against threshold

Measure against: >=80% of opportunities have completed need assessments over 2 weeks with need score predicting deal progression within 15% accuracy.

If PASS (>=80% completion, prediction accuracy within 15%), proceed to Scalable. Document:
- The validated need categories and scoring rubric
- Need patterns by ICP segment
- The need-to-product mapping
- Hypothesis accuracy baseline (average pre-call vs post-call delta)

If FAIL, diagnose:
- Low completion rate: scheduling bottleneck — automate booking reminders or increase outreach volume
- Low prediction accuracy: either enrichment signals are weak predictors of actual needs, or the scoring rubric does not align with deal outcomes — recalibrate after reviewing closed deals
- One need tier dominates (>80% High or >80% Low): scoring threshold or ICP targeting needs adjustment

## Time Estimate

- Prospect enrichment and list building: 3 hours
- Need-to-product mapping: 1.5 hours
- Cold email sequence setup: 1.5 hours
- LinkedIn outreach setup: 1 hour
- PostHog event tracking: 1 hour
- Discovery calls (12-15 calls at 25 min each): 5-6 hours
- Post-call scoring and CRM logging: 2 hours
- Pattern analysis and calibration: 1 hour

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with need assessment pipeline | Free tier or Plus $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Instantly | Cold email sequences | Growth $47/mo — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Clay | Prospect enrichment with need signals | Launch $185/mo — [clay.com/pricing](https://clay.com/pricing) |
| Fireflies | Call transcription for need extraction | Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Need assessment funnel tracking | Free (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| Cal.com | Discovery call booking | Free — [cal.com/pricing](https://cal.com/pricing) |
| Anthropic API | LLM need extraction from transcripts | ~$3/MTok input (Sonnet) — [docs.anthropic.com/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |

**Estimated play-specific cost:** ~$250-280/mo (Instantly $47 + Clay $185 + Fireflies $18 + Anthropic ~$5-10)

## Drills Referenced

- `cold-email-sequence` — 4-step cold email sequence in Instantly with need-signal-personalized copy
- `linkedin-outreach` — parallel LinkedIn connection + message sequence for need validation
- the need discovery call workflow (see instructions below) — structured need discovery call lifecycle with LLM-based need extraction
- `enrich-and-score` — Clay enrichment with need-relevant signal scoring
- `posthog-gtm-events` — event tracking for the full need assessment funnel
