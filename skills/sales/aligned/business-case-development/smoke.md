---
name: business-case-development-smoke
description: >
  Business Case Development — Smoke Test. Manually co-create business cases for 5+ aligned
  deals using discovery pain data, an ROI model, and strategic alignment to validate that
  champion-ready business cases accelerate executive approval.
stage: "Sales > Aligned"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Smoke Test"
time: "7 hours over 1 week"
outcome: "≥5 business cases delivered with ≥60% securing executive review within 7 days"
kpis: ["Business case completion rate", "Executive review rate", "Time to executive review", "Deal stage progression"]
slug: "business-case-development"
install: "npx gtm-skills add sales/aligned/business-case-development"
drills:
  - threshold-engine
---

# Business Case Development — Smoke Test

> **Stage:** Sales → Aligned | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Deliver champion-ready business cases for at least 5 aligned deals within 1 week. At least 60% of those business cases must result in an executive review being scheduled within 7 days of delivery. This proves that co-created business cases accelerate internal approval compared to leaving the champion to build the case alone.

## Leading Indicators

- Champion responds within 48 hours confirming the business case is useful
- Champion shares the document with at least 1 additional stakeholder
- Champion asks clarifying questions about ROI assumptions (signals engagement, not doubt)
- Executive review meeting is scheduled within 5 business days

## Instructions

### 1. Identify 5-8 deals that need business cases

Query Attio for deals at the Aligned stage where the prospect has indicated they need internal approval. Filter for deals with:
- At least 1 completed discovery call with transcript
- At least 2 quantified pains (from prior `pain-discovery-call` work or extracted now)
- An identified champion contact

If fewer than 5 deals qualify, run `call-transcript-pain-extraction` on recent discovery transcripts to populate pain data for additional deals.

### 2. Run the business-case-assembly drill for each deal

For each qualifying deal, run the the business case assembly workflow (see instructions below) drill. This orchestrates:
- Pain extraction and quantification (if not already done)
- Stakeholder role classification (identify the Economic Buyer and Champion)
- Strategic alignment mapping (connect your product to their known initiatives)
- ROI model generation (conservative 3-year projection with sensitivity analysis)
- Business case document generation (champion-ready, using their own words)

At Smoke level, run each step manually with the agent assisting. Review every output before proceeding to the next step. This is validation, not automation.

**Human action required:** Review each generated business case before sending. Verify:
- Prospect quotes are accurate and in context
- Dollar estimates are defensible (not inflated)
- Strategic alignment claims map to real initiatives the prospect mentioned
- The document reads as if the champion wrote it, not your marketing team

### 3. Deliver business cases to champions

For each reviewed business case:
- Send via email with a cover note: "Based on our conversations, I put together a summary of what we discussed and what solving these challenges could look like for [Company]. Feel free to use this internally — I wrote it from your team's perspective."
- Attach both the full business case document and the standalone ROI calculator (spreadsheet format) so the champion can adjust inputs
- Log delivery in Attio: set `business_case_status = "sent"`, `business_case_date = today`

### 4. Track responses and outcomes

For each delivered business case, track in Attio:
- `champion_responded`: true/false (within 48 hours)
- `champion_shared_internally`: true/false (champion forwarded or referenced sharing)
- `executive_review_scheduled`: true/false
- `executive_review_date`: date if scheduled
- `days_to_executive_review`: calculated from send date

Fire PostHog events for each milestone:
```
business_case_sent → business_case_champion_engaged → executive_review_scheduled → executive_approval_granted
```

### 5. Evaluate against threshold

Run the `threshold-engine` drill to check:
- **Primary threshold:** ≥5 business cases delivered AND ≥60% have executive review scheduled within 7 days
- **Secondary signals:** Average time-to-review, champion engagement rate, any business cases that led to deal stage advancement

If PASS: document which business case elements champions found most valuable (ask them). Note which sections executives focused on. Proceed to Baseline.

If FAIL: diagnose the failure mode:
- If business cases were delivered but champions did not engage → the document may not be useful or the champion relationship is weak
- If champions engaged but executive review was not scheduled → the business case may lack the right executive framing or the deal is not truly at Aligned stage
- Iterate on the failing element and re-run Smoke

---

## Time Estimate

- 1 hour: identifying qualifying deals and pulling data from Attio
- 4 hours: running business-case-assembly for 5 deals (agent-assisted, ~45 min each)
- 1 hour: human review and editing of generated business cases
- 1 hour: delivery, tracking setup, and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, pain data, stakeholder tracking | Standard stack (excluded) |
| PostHog | Event tracking — business case funnel metrics | Standard stack (excluded) |
| Anthropic Claude API | Pain extraction, ROI generation, business case generation | ~$0.10-0.30 per business case at Sonnet tier ([pricing](https://platform.claude.com/docs/en/about-claude/pricing)) |
| Fireflies | Call transcript source | Standard stack or ~$19/mo starter ([pricing](https://fireflies.ai/pricing)) |

**Estimated play-specific cost:** Free (Claude API costs negligible at 5 cases)

## Drills Referenced

- the business case assembly workflow (see instructions below) — orchestrates pain extraction, ROI modeling, strategic alignment, and document generation into a single workflow
- `threshold-engine` — evaluates business case delivery and approval metrics against pass/fail criteria
