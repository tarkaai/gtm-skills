---
name: meddic-qualification-smoke
description: >
  MEDDIC Qualification System — Smoke Test. Manually apply MEDDIC scoring to 3-5 active enterprise
  deals, validate that structured element tracking improves deal visibility and surfaces risks
  that would otherwise be missed.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=2 deals with >=80% MEDDIC completeness in 1 week"
kpis: ["MEDDIC completeness score", "Elements per call", "Time to complete MEDDIC"]
slug: "meddic-qualification"
install: "npx gtm-skills add sales/connected/meddic-qualification"
drills:
  - threshold-engine
---

# MEDDIC Qualification System — Smoke Test

> **Stage:** Sales > Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Prove that structured MEDDIC scoring produces better deal visibility than gut-feel qualification. After 1 week, at least 2 deals should have all 6 MEDDIC elements assessed with 80%+ completeness (scores for every element, evidence captured, gaps identified). The smoke test validates that the framework fits your enterprise deal motion before investing in automation.

## Leading Indicators

- MEDDIC scorecard created in CRM with all 6 element fields populated for at least 1 deal within first 2 days
- Discovery call question guide generated and used on at least 1 call
- At least 1 deal risk surfaced by MEDDIC analysis that was not previously visible (e.g., no identified economic buyer, unclear decision process)
- Founder reports that MEDDIC-structured calls feel more focused and productive than unstructured calls

## Instructions

### 1. Set up MEDDIC infrastructure in your CRM

Run the the meddic scorecard setup workflow (see instructions below) drill. This creates 20+ custom attributes on the Deals object in Attio:
- Score fields (0-100) for each of the 6 MEDDIC elements: Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion
- Status fields for each element (e.g., Metrics: Quantified/Directional/Vague/Absent)
- Evidence fields to store key quotes and findings
- Composite score with weighted formula: (M * 0.15) + (EB * 0.20) + (DC * 0.15) + (DP * 0.15) + (IP * 0.20) + (C * 0.15)
- Pipeline stages: New Lead, MEDDIC Pre-Scored, Discovery Scheduled, MEDDIC Qualified, MEDDIC Needs Work, MEDDIC Disqualified
- PostHog tracking events for qualification milestones

Estimated time: 2 hours.

### 2. Select 3-5 active deals for MEDDIC scoring

From your existing pipeline in Attio, select 3-5 deals that are in the Connected stage — deals where you have had initial contact but have not yet fully qualified. Prioritize deals with upcoming calls scheduled so you can run MEDDIC discovery in real time.

For each deal, manually review everything you know and score each MEDDIC element 0-100 based on existing information. Set `meddic_assessment_source` to "Pre-call Enrichment" (even though this is manual — it establishes the baseline).

### 3. Run MEDDIC discovery calls

Run the the meddic discovery call workflow (see instructions below) drill for each selected deal that has a call scheduled:

1. The drill pulls the deal's current MEDDIC scores and identifies the weakest elements
2. It generates a tailored question guide targeting the gaps (e.g., if Economic Buyer score is below 50, it generates questions like "Who ultimately signs off on the budget for tools in this area?")
3. Ensure Fireflies is recording the call
4. After the call, run `call-transcript-meddic-extraction` to extract structured MEDDIC scores from the transcript
5. Update the deal record with post-call scores, evidence, and next steps

**Human action required:** You must be on the calls. The agent prepares questions and processes transcripts, but the founder runs the conversation.

For deals without calls scheduled this week, score them based on existing notes, emails, and prior conversations. Document what you know for each element and identify what is missing.

### 4. Assess MEDDIC completeness

After scoring all selected deals, evaluate completeness for each:
- A deal has 80%+ MEDDIC completeness when all 6 elements have scores above 0, at least 4 elements have evidence captured (not just estimated scores), and the weakest elements have documented next actions to address them
- A deal has 100% MEDDIC completeness when all 6 elements have scores, evidence, and status classifications

### 5. Evaluate against threshold

Run the `threshold-engine` drill to evaluate results against the pass threshold: >=2 deals with >=80% MEDDIC completeness in 1 week.

Also assess qualitatively:
- Did MEDDIC scoring surface any deal risks you did not previously see?
- Did the structured question guide improve your discovery calls?
- Are the scoring weights and rubrics appropriate for your deal motion, or do they need adjustment?

If PASS, proceed to Baseline. If FAIL, review: Were the deals too early-stage for MEDDIC scoring? Were the scoring rubrics unclear? Did you not have enough calls scheduled? Adjust and re-run.

## Time Estimate

- CRM setup (meddic-scorecard-setup): 2 hours
- Deal selection and initial scoring: 1 hour
- Discovery call prep and execution (2-3 calls): 3 hours
- Post-call scoring and analysis: 1.5 hours
- Threshold evaluation and documentation: 0.5 hours

**Total: ~8 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, MEDDIC custom attributes, pipeline stages | Standard stack (excluded from play budget) |
| PostHog | Event tracking for qualification milestones | Standard stack (excluded from play budget) |
| Fireflies.ai | Call transcription for MEDDIC extraction | Free plan: 800 min/mo. Pro: $10/user/mo annual. [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Cal.com | Meeting scheduling for discovery calls | Standard stack (excluded from play budget) |

**Play-specific cost: Free** (Fireflies free tier sufficient for Smoke volume)

## Drills Referenced

- the meddic scorecard setup workflow (see instructions below) — creates CRM infrastructure with all MEDDIC fields and pipeline stages
- the meddic discovery call workflow (see instructions below) — full discovery call lifecycle with element-targeted questions, transcript extraction, and CRM logging
- `threshold-engine` — evaluates results against pass/fail threshold and recommends next action
