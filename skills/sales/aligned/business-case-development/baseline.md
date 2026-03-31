---
name: business-case-development-baseline
description: >
  Business Case Development — Baseline Run. Systematize business case creation across 15-25
  enterprise deals over 2 weeks with template libraries, ROI calculators, and executive
  objection playbooks, maintaining ≥65% approval rate.
stage: "Sales > Aligned"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥80% of enterprise deals at Aligned stage have business cases delivered; ≥65% approval rate"
kpis: ["Business case coverage rate", "Executive approval rate", "Median time-to-approval", "Win rate with vs. without business case"]
slug: "business-case-development"
install: "npx gtm-skills add sales/aligned/business-case-development"
drills:
  - roi-calculator-build
  - stakeholder-map-assembly
  - posthog-gtm-events
---

# Business Case Development — Baseline Run

> **Stage:** Sales → Aligned | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Deliver business cases for at least 80% of enterprise deals at the Aligned stage over 2 weeks. Maintain a 65%+ executive approval rate. Establish a repeatable process with templates, ROI calculators, and executive objection libraries that any deal can use.

## Leading Indicators

- Business case assembly time drops below 30 minutes per deal (from ~45 min at Smoke)
- Champions request business case materials proactively (before being offered)
- Executive review meetings are scheduled within 5 days of delivery
- Deals with business cases advance to Proposed stage faster than those without
- ROI calculator is opened and inputs adjusted by the prospect (signals engagement)

## Instructions

### 1. Set up business case event tracking

Run the `posthog-gtm-events` drill to configure a complete event taxonomy for business case development. Define these events:

```
business_case_assembly_started
business_case_pain_validated
business_case_roi_generated
business_case_alignment_mapped
business_case_assembled
business_case_sent
business_case_champion_engaged
business_case_shared_internally
executive_review_scheduled
executive_approval_granted
executive_approval_denied
business_case_objection_raised
```

Attach standard properties: `deal_id`, `company_size_tier`, `industry`, `roi_percentage`, `alignment_score`, `champion_role`, `economic_buyer_persona`.

### 2. Build the stakeholder map for all active deals

Run the `stakeholder-map-assembly` drill on every deal at the Aligned stage. For each deal, produce:
- Buying committee map with role classifications (Economic Buyer, Champion, Influencer, Blocker)
- Influence scores per stakeholder
- Gap report: missing roles that need to be identified before the business case can succeed

Prioritize deals where the Economic Buyer is identified — these have the highest approval probability.

### 3. Build ROI calculators for each deal

Run the `roi-calculator-build` drill for each deal with sufficient pain data (`pain_count >= 2`, `pain_to_price_ratio >= 3`):
- Generate a prospect-specific ROI model
- Format as a Google Sheet with adjustable inputs (so prospects can modify assumptions)
- Include conservative/moderate/optimistic scenarios
- Validate that payback period is < 12 months (flag if longer)

For deals where pain data is insufficient, recommend an additional discovery call before building the ROI calculator.

### 4. Assemble business cases at volume

Run the the business case assembly workflow (see instructions below) drill for each qualifying deal. At Baseline level, the agent handles most of the assembly with the seller reviewing before delivery.

Build reusable artifacts:
- **Industry-specific templates:** After completing 3+ cases in the same industry, extract common sections (industry benchmarks, typical pain categories, regulatory drivers) into reusable templates
- **Executive objection library:** Track every objection raised during or after business case review. For each objection, store: the objection text, the persona who raised it, the response that worked, and the outcome. After 10+ objections, the library becomes a competitive asset.
- **Strategic alignment patterns:** Map which strategic initiatives appear most frequently across prospects and which alignment narratives resonate most with each executive persona

**Human action required:** Review each business case before delivery. At Baseline, the review should focus on accuracy and tone rather than structure (the structure is now templated).

### 5. Track outcomes and build the effectiveness baseline

For every business case delivered, track the full lifecycle in PostHog and Attio:
- Time from assembly start to delivery
- Time from delivery to champion engagement
- Time from champion engagement to executive review
- Executive review outcome (approved, denied, additional info requested)
- Objections raised and how they were resolved
- Whether the deal ultimately closed and at what size

Compute baseline metrics after 2 weeks:
- Approval rate (target: ≥65%)
- Median time-to-approval
- Win rate for deals with business case vs. without
- Average deal size with business case vs. without

### 6. Evaluate against threshold

At the end of 2 weeks, evaluate:
- **Primary threshold:** ≥80% of Aligned deals have business cases AND ≥65% approval rate
- **Secondary metrics:** time-to-approval trending down, deal size impact positive

If PASS: document the template library, objection library, and effectiveness baseline. Proceed to Scalable.

If FAIL: diagnose:
- Coverage < 80% → bottleneck is likely pain data insufficiency or stakeholder gaps. Run more discovery calls.
- Approval < 65% → analyze rejection reasons. Common causes: ROI not credible (need better pain quantification), wrong executive framing (need better persona targeting), missing risk mitigations (need more proof points).

---

## Time Estimate

- 3 hours: stakeholder mapping and event tracking setup
- 10 hours: business case assembly for 15-25 deals (agent handles assembly, seller reviews)
- 3 hours: building template library and objection library from patterns
- 2 hours: outcome tracking, baseline computation, threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, stakeholder maps, business case tracking | Standard stack (excluded) |
| PostHog | Event tracking — approval funnel, effectiveness metrics | Standard stack (excluded) |
| n8n | Automation — event routing, reminder workflows | Standard stack (excluded) |
| Anthropic Claude API | Pain extraction, ROI generation, business case generation | ~$2-6/mo at 15-25 cases ([pricing](https://platform.claude.com/docs/en/about-claude/pricing)) |
| Clay | Stakeholder enrichment for buying committee maps | ~$50-150/mo ([pricing](https://www.clay.com/pricing)) |

**Estimated play-specific cost:** ~$50-150/mo (primarily Clay for stakeholder enrichment)

## Drills Referenced

- the business case assembly workflow (see instructions below) — end-to-end business case creation from pain data through document delivery
- `roi-calculator-build` — generates prospect-specific ROI calculators with adjustable inputs
- `stakeholder-map-assembly` — maps buying committee roles, influence scores, and engagement gaps
- `posthog-gtm-events` — configures event taxonomy for tracking business case lifecycle metrics
