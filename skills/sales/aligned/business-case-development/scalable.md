---
name: business-case-development-scalable
description: >
  Business Case Development — Scalable Automation. Auto-generate business cases when deals
  reach Aligned stage with sufficient pain data. A/B test business case structures, executive
  framings, and delivery methods to find the highest-converting approach.
stage: "Sales > Aligned"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Scalable Automation"
time: "65 hours over 2 months"
outcome: "Business cases auto-generated for all qualifying deals; approval rate ≥65% of Baseline; time-to-approval ≤75% of Baseline"
kpis: ["Auto-generation coverage", "Executive approval rate", "Time-to-approval", "Enterprise win rate", "Deal size impact"]
slug: "business-case-development"
install: "npx gtm-skills add sales/aligned/business-case-development"
drills:
  - roi-auto-generation
  - ab-test-orchestrator
  - dashboard-builder
---

# Business Case Development — Scalable Automation

> **Stage:** Sales → Aligned | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Automatically generate business cases when deals reach the Aligned stage with sufficient pain data — no manual assembly required. The seller reviews and sends, but the building is fully automated. Maintain approval rate at least 65% of Baseline level. Reduce median time-to-approval to 75% of Baseline through A/B tested improvements in structure, framing, and delivery.

## Leading Indicators

- Auto-generation fires within 5 minutes of deal meeting qualification criteria
- Seller review-to-send time drops below 10 minutes (most cases need zero edits)
- A/B test variants produce statistically significant differences within 2 weeks
- Business case ROI projections correlate with actual deal outcomes at >70% accuracy
- Champions begin expecting business cases as a standard part of the process

## Instructions

### 1. Deploy auto-generation workflows

Run the `roi-auto-generation` drill to create n8n workflows that trigger automatically:

**Trigger conditions:**
- Attio deal stage changes to "Aligned" AND `pain_count >= 2` AND `pain_quantification_rate >= 0.5`
- OR: `pain_count` attribute updated on a deal already at Aligned stage (additional discovery completed)

**Auto-generation pipeline:**
1. Validate pain data readiness (`pain_to_price_ratio >= 3`)
2. Generate ROI model with sensitivity analysis
3. Map strategic alignment to known prospect initiatives
4. Generate persona-specific executive narratives for the identified Economic Buyer
5. Match risks to mitigation assets from the content library
6. Assemble the full business case document
7. Generate a standalone ROI calculator (Google Sheet)
8. Attach both artifacts to the Attio deal record
9. Notify the deal owner via Slack: "Business case auto-generated for {company}. ROI: {X}%, payback: {Y} months. Review and send: {link}"

**Rate limits:**
- Maximum 10 auto-generations per day (controls API costs)
- Skip generation if `business_case_status` already set (avoid duplicates)
- If `pain_to_price_ratio < 3`, skip and alert: "Weak ROI for {company}. Additional discovery recommended."

### 2. Generate stakeholder-specific business case versions

Build n8n workflows that auto-generate persona-tailored versions of the business case:

- **CFO version:** Lead with payback period, NPV, cost avoidance. Emphasize sensitivity analysis. Remove strategic narrative (CFOs want numbers).
- **CEO version:** Lead with strategic alignment and competitive positioning. Include ROI summary but emphasize market opportunity. Remove technical detail.
- **CTO version:** Lead with technical debt reduction, architecture simplification, integration efficiency. Include implementation timeline. Remove financial detail.

The seller selects which version(s) to send based on the identified approval chain. Store version metadata in Attio for effectiveness tracking.

### 3. Launch A/B testing on business case elements

Run the `ab-test-orchestrator` drill to set up experiments:

**Experiment 1: Business case structure**
- Control: Current template (exec summary → current state → solution → ROI → risk → recommendation)
- Variant: ROI-first structure (ROI summary → current state → solution → strategic alignment → risk → recommendation)
- Success metric: executive review rate within 7 days
- Minimum sample: 20 cases per variant

**Experiment 2: ROI presentation format**
- Control: Table with conservative/moderate/optimistic scenarios
- Variant: Single conservative number with "upside potential" callout
- Success metric: champion reports executive found ROI credible

**Experiment 3: Delivery method**
- Control: PDF attachment via email
- Variant: Interactive web page (via Qwilr) with embedded ROI calculator
- Success metric: time spent reviewing, sections viewed, approval rate

**Experiment 4: Risk section positioning**
- Control: Risks after ROI analysis
- Variant: Risks immediately after current state (address concerns before presenting solution)
- Success metric: objection count during executive review

Use PostHog feature flags to randomly assign deals to variants. Run each test for minimum 20 cases per variant before declaring a winner.

### 4. Build the business case effectiveness dashboard

Run the `dashboard-builder` drill to create a PostHog dashboard:

**Funnel panel:** `business_case_auto_generated` → `business_case_reviewed_by_seller` → `business_case_sent` → `champion_engaged` → `executive_review_scheduled` → `executive_approval_granted` → `deal_won`

**Trend panels:**
- Auto-generation volume and success rate (weekly)
- Approval rate by business case version (CFO/CEO/CTO)
- Median time-to-approval (rolling 4 weeks)
- A/B test variant performance comparison
- ROI projection accuracy (projected vs. actual deal outcome)

**Alert panels:**
- Approval rate drops >20% below Baseline → immediate alert
- Auto-generation failure rate >10% → infrastructure alert
- Seller review time exceeds 30 minutes → template quality alert

### 5. Scale volume and optimize

Increase coverage:
- Set auto-generation to trigger for ALL deals reaching Aligned with `pain_count >= 2` (remove manual gatekeeping)
- Build a "business case readiness score" that predicts which deals will benefit most: `readiness = (pain_count * 0.3) + (pain_to_price_ratio * 0.2) + (alignment_score * 0.2) + (stakeholder_coverage * 0.3)`. Prioritize high-readiness deals for immediate generation; queue low-readiness deals for discovery.

Optimize cost:
- Cache common industry benchmarks and strategic alignment patterns to reduce API calls
- Batch generate for deals entering Aligned on the same day
- Use Claude Haiku for draft generation, Sonnet for final quality pass

### 6. Set guardrails

- Approval rate must stay ≥65% of Baseline level. If it drops below for 2 consecutive weeks, pause auto-generation and investigate.
- Time-to-approval must not exceed Baseline median. If it increases, the auto-generated cases may be lower quality than manual ones.
- If seller edit rate exceeds 50% of auto-generated cases, the templates need calibration.
- Maximum API spend: $50/month on auto-generation (at ~$0.30/case, supports ~160 cases/month).

### 7. Evaluate at 2 months

Measure against threshold:
- Auto-generation coverage for all qualifying deals
- Approval rate ≥65% of Baseline
- Time-to-approval ≤75% of Baseline

If PASS: document winning A/B variants, lock in the best templates, proceed to Durable.
If FAIL: identify the weakest stage in the funnel. If generation quality is the issue, improve prompts. If delivery is the issue, test new formats. If approval is the issue, improve executive framing.

---

## Time Estimate

- 15 hours: building auto-generation workflows in n8n (trigger logic, API orchestration, Slack notifications)
- 10 hours: setting up persona-specific version generation and A/B test infrastructure
- 5 hours: building the effectiveness dashboard and alert system
- 20 hours: monitoring, analyzing A/B results, and iterating on templates over 2 months
- 15 hours: scaling, optimizing costs, and calibrating guardrails

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal triggers, stakeholder data, business case tracking | Standard stack (excluded) |
| PostHog | Analytics — funnel tracking, A/B testing, dashboards | Standard stack (excluded) |
| n8n | Automation — auto-generation workflows, alerts, scheduling | Standard stack (excluded) |
| Anthropic Claude API | Business case generation, ROI modeling, narrative creation | ~$15-50/mo at scale ([pricing](https://platform.claude.com/docs/en/about-claude/pricing)) |
| Clay | Stakeholder enrichment, initiative research | ~$150-400/mo at scale ([pricing](https://www.clay.com/pricing)) |
| Qwilr (optional) | Interactive business case delivery | ~$39-49/user/mo ([pricing](https://qwilr.com/pricing/)) |

**Estimated play-specific cost:** ~$150-500/mo (Clay enrichment + Claude API + optional Qwilr)

## Drills Referenced

- `roi-auto-generation` — n8n workflow that auto-generates ROI calculators and business cases when deals reach qualification thresholds
- `ab-test-orchestrator` — manages A/B experiments on business case structure, framing, and delivery methods
- `dashboard-builder` — creates PostHog dashboards for real-time business case effectiveness visibility
