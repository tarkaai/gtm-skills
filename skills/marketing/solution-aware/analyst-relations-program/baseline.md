---
name: analyst-relations-program-baseline
description: >
  Analyst Relations Program — Baseline Run. Expand to 15-20 analysts, systematize briefing
  outreach, launch quarterly nurture cadence, and validate that analyst engagement produces
  report mentions and influenced deals over 10 weeks.
stage: "Marketing > SolutionAware"
motion: "PartnershipsWarmIntros"
channels: "Other"
level: "Baseline Run"
time: "30 hours over 10 weeks"
outcome: ">=6 briefings completed, >=1 analyst report mention or inclusion, and >=5 analyst-influenced deals identified within 10 weeks"
kpis: ["Briefing acceptance rate", "Briefings completed", "Report mentions", "Analyst-influenced deals", "Relationship score distribution"]
slug: "analyst-relations-program"
install: "npx gtm-skills add marketing/solution-aware/analyst-relations-program"
drills:
  - analyst-target-research
  - briefing-deck-preparation
  - analyst-relationship-nurture
  - threshold-engine
---

# Analyst Relations Program — Baseline Run

> **Stage:** Marketing > SolutionAware | **Motion:** PartnershipsWarmIntros | **Channels:** Other

## Outcomes

The first always-on analyst relations cadence. Briefing outreach is systematic, a quarterly nurture cadence keeps you top-of-mind, and you begin tracking the influence analysts have on your deal pipeline. The goal is proving that analyst engagement reliably produces report mentions and influences buyer decisions.

**Pass threshold:** >=6 briefings completed, >=1 analyst report mention or inclusion, and >=5 analyst-influenced deals identified within 10 weeks.

## Leading Indicators

- Briefing acceptance rate exceeds 40% across all tiers
- At least 1 analyst proactively mentions your company when contacted by buyers
- At least 1 analyst agrees to include you in upcoming research (even if not yet published)
- Quarterly update emails achieve >50% open rate (analysts are reading your updates)
- Sales team identifies at least 2 deals where the prospect mentioned analyst research during the buying process

## Instructions

### 1. Expand the Analyst List

Run the `analyst-target-research` drill at Baseline scale (15-20 analysts):

1. Retain all analysts from Smoke who engaged. Add new targets across all four tiers.
2. Include Tier 1 analysts now: Gartner Magic Quadrant leads, Forrester Wave leads for your category
3. Use `clay-enrichment-waterfall` for full contact enrichment: email, LinkedIn, firm, coverage area, recent publications
4. Re-score the full list with updated data. Reprioritize based on Smoke learnings (e.g., if Tier 3 independents were most responsive, weight them higher)
5. Push all analysts to Attio with: Relationship Type = "Analyst/Consultant", Analyst Tier, Priority, Coverage Area, Briefing Status

### 2. Systematize Briefing Outreach

Expand from ad-hoc requests to a structured pipeline:

1. Run the `briefing-deck-preparation` drill for each new Priority 1 and Priority 2 analyst
2. Create a briefing request template with personalization fields:
   - `{analyst_name}` — their name
   - `{recent_publication}` — reference to their latest relevant work
   - `{company_update}` — what is new since their last coverage of the space
   - `{specific_ask}` — what you want feedback on
3. Sequence the outreach: Priority 1 analysts first (week 1-2), Priority 2 (week 3-4), new Tier 1 (week 5-6)
4. For Tier 1 analysts at major firms: check if they offer vendor briefing request forms (Gartner and Forrester have formal processes). Use the form and follow up via email.
5. Track all requests in Attio: date sent, method, status (requested / scheduled / completed / declined / no response)
6. One follow-up per analyst (after 7 days). If no response after follow-up, mark as "cold" and try again next quarter with a different hook.

### 3. Launch Quarterly Nurture Cadence

Run the `analyst-relationship-nurture` drill:

1. Set up the quarterly update automation in n8n:
   - Trigger: first Monday of each quarter at 9am
   - Pull all analysts in Attio with Briefing Status = "Briefed"
   - Generate a personalized quarterly update email using Claude API: reference their coverage area, share 2-3 relevant updates (new customer, product launch, market data), close with offer for follow-up briefing
   - Route to Slack for human review before sending
2. Build milestone notification triggers: when a major event occurs (funding, product launch, significant customer win), auto-draft a note to relevant analysts
3. Track engagement: log all analyst opens, replies, and proactive outreach in Attio

### 4. Track Analyst-Influenced Pipeline

Connect analyst activity to deal outcomes:

1. Add an "Analyst Influenced" tag in Attio for deals where the prospect mentions analyst research
2. Train the sales team: during discovery calls, ask prospects what research they consulted. If they mention an analyst report, market guide, or advisor recommendation, tag the deal.
3. In PostHog, track: `analyst_briefing_completed`, `analyst_mention_detected`, `analyst_referral_received`, `deal_analyst_influenced`
4. Weekly: review Attio for any new analyst-influenced deals. Log the analyst, the research, and the deal value.

### 5. Prepare for Report Inclusion

For each analyst who expressed interest in including you:

1. Ask what data, metrics, and customer references they need
2. Prepare a detailed submission package: company overview, differentiation, customer metrics, competitive positioning
3. Provide customer references who have agreed to speak with analysts
4. Follow up on their timeline: when is the report expected? When do they need your input by?
5. Log all report inclusion activity in Attio with expected publication dates

### 6. Evaluate Against Threshold

Run the `threshold-engine` drill after 10 weeks:

1. Compile:
   - Briefings completed (threshold: >=6)
   - Report mentions or inclusions (threshold: >=1)
   - Analyst-influenced deals identified (threshold: >=5)
2. Analyze: which analyst tier produced the most value (briefings that led to mentions or referrals)?
3. Calculate: briefing-to-mention conversion rate, analyst-influenced pipeline value

**If PASS:** Analyst relations is producing measurable pipeline influence. Proceed to Scalable with automated monitoring and expanded nurture.

**If FAIL:** Diagnose:
- Low briefing count: outreach volume or quality is insufficient. Expand the list and improve one-pager quality.
- Briefings but no mentions: your positioning may not meet analyst criteria. Ask directly what you need to demonstrate.
- No influenced deals: sales team is not tracking. Reinforce the process or survey recent closed-won deals retrospectively.

## Time Estimate

- 4 hours: Analyst list expansion and re-scoring
- 6 hours: Briefing material preparation for 8-10 new analysts
- 4 hours: Briefing request outreach and follow-ups
- 6 hours: Conducting 6 briefings (30 min each + prep + follow-up)
- 4 hours: Quarterly nurture setup (n8n workflow, templates)
- 3 hours: Pipeline tracking setup and sales team training
- 3 hours: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Cal.com | Scheduling — analyst briefing booking | Free plan — [cal.com/pricing](https://cal.com/pricing) |
| Attio | CRM — analyst contacts, pipeline tracking, relationship scoring | $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — analyst contact research and scoring | $149/mo (Starter) — [clay.com/pricing](https://www.clay.com/pricing) |
| Loops | Email — quarterly nurture sequences | $49/mo (Starter) — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Analytics — analyst event tracking | Free up to 1M events — [posthog.com/pricing](https://posthog.com/pricing) |
| Claude API | Briefing document and update drafting | ~$15-25/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** Loops ~$49/mo for analyst nurture sequences. Other tools are standard stack or minimal.

## Drills Referenced

- `analyst-target-research` — expanded analyst list with enrichment and updated scoring
- `briefing-deck-preparation` — tailored one-pagers and agendas for each analyst briefing
- `analyst-relationship-nurture` — quarterly update cadence, milestone notifications, and engagement tracking
- `threshold-engine` — evaluate Baseline results against the pass threshold and recommend next action
