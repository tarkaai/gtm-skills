---
name: technical-deep-dive-demo-smoke
description: >
  Technical Deep-Dive Demo — Smoke Test. Run 5 technical deep-dive demos with engineer/architect
  stakeholders to validate that prospect-tailored technical content (architecture, APIs, security,
  integrations) drives advancement to POC or proposal stage.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: "Technical demos completed on ≥5 opportunities in 1 week with ≥60% advancing to POC or proposal"
kpis: ["Technical demo completion rate", "Demo-to-POC conversion rate", "Technical stakeholder engagement score", "Technical blockers identified per demo"]
slug: "technical-deep-dive-demo"
install: "npx gtm-skills add sales/connected/technical-deep-dive-demo"
drills:
  - threshold-engine
---
# Technical Deep-Dive Demo — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Outcomes
Complete technical deep-dive demos on at least 5 connected opportunities in 1 week. At least 60% of those demos must advance the deal to POC or proposal stage. Each demo must cover architecture, live API calls, at least one integration relevant to the prospect's stack, and a security review.

## Leading Indicators
- Technical stakeholders (engineer, architect, CTO) confirm attendance before the demo
- Prospect shares specific technical requirements or questions in advance
- Discovery notes contain at least 2 technical pain points or integration requirements
- Prospect's tech stack is detectable via Clay enrichment

## Instructions

### 1. Select 5-8 connected opportunities with technical stakeholders
Query Attio for deals at Connected stage where at least one contact has a technical title (Engineer, Architect, CTO, VP Engineering, DevOps, SRE). Filter to deals where a discovery call has been completed (check for Fireflies transcript or Attio notes tagged `discovery`).

**Human action required:** Review the list and select 5-8 opportunities where a technical deep-dive is the appropriate next step. Exclude deals where the buyer is non-technical and no technical evaluator has been identified.

### 2. Run the the account research brief workflow (see instructions below) drill for each opportunity
For each selected deal, run the the account research brief workflow (see instructions below) drill with `meeting_type: "technical_deep_dive"`. This pulls CRM context, enriches the account via Clay, incorporates prior discovery call transcripts from Fireflies, and generates a structured meeting brief with technical talking points.

Review the output. Verify that the brief includes:
- The prospect's tech stack
- Technical requirements from discovery
- Attendee profiles with role classifications
- Recommended technical topics based on their architecture

### 3. Run the the technical demo content assembly workflow (see instructions below) drill for each opportunity
For each deal, run the the technical demo content assembly workflow (see instructions below) drill. This detects the prospect's tech stack, generates a structured demo script with ordered modules (architecture, API walkthrough, integration demo, security review), prepares live API call payloads, generates integration code targeting their actual tools, and assembles a technical follow-up package.

Review each demo script. Verify:
- Live API calls reference real product endpoints
- Integration code targets tools detected in their stack (not generic examples)
- Module ordering reflects the attendee profiles (architect-heavy = architecture first; engineer-heavy = API first)
- Anticipated questions have substantive answers, not placeholder text

### 4. Execute the technical demos

**Human action required:** Deliver each technical demo following the generated script. During the demo:
- Execute the live API calls prepared in step 3
- Show integration code on screen and walk through it line by line
- Invite technical questions throughout (do not save them for the end)
- For each question asked, note whether the prepared answer was sufficient or if a follow-up is needed
- At the end, ask: "What technical questions remain?" and "Do you see any technical blockers to moving forward?"

After each demo, log the outcome in Attio:
- Outcome: `poc_requested`, `proposal_requested`, `follow_up_needed`, or `no_interest`
- Technical blockers identified (list each one)
- Number of technical questions asked
- Which demo modules generated the most engagement
- Duration in minutes

### 5. Send the technical follow-up package
After each demo, send the prospect-specific technical package assembled in step 3 (API docs, integration guide, architecture diagram, security documentation, code samples). Store the sent package as an Attio note on the deal.

### 6. Evaluate against threshold
Run the `threshold-engine` drill to measure results against the pass threshold. The threshold engine pulls demo completion events and outcome data from Attio, compares against the target (5 demos completed, 60% advancing), and returns PASS or FAIL.

If PASS, proceed to Baseline. If FAIL, analyze which step broke:
- If demos were not scheduled: targeting problem (wrong deals or missing technical stakeholders)
- If demos happened but did not advance: content problem (demo script did not address actual pain) or audience problem (wrong attendees in the room)
- If technical blockers killed advancement: product gap (log the blockers for product team review)

---

## Time Estimate
- Account research and demo prep: 4 hours (30-45 min per opportunity)
- Demo execution: 3 hours (30-40 min per demo)
- Follow-up and evaluation: 1 hour

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, contact management, notes | Free (up to 3 users); Plus $29/user/mo |
| Clay | Tech stack detection and account enrichment | Launch $185/mo (2,500 credits) |
| Fireflies | Discovery call transcription | Free (800 min/mo); Pro $10/user/mo annual |
| Anthropic Claude API | Demo script generation via `technical-demo-script-generation` | Sonnet 4.6: $3/$15 per 1M tokens (~$0.50/demo) |
| Cal.com | Scheduling technical demos | Free (1 user); Teams $15/user/mo |

**Play-specific cost:** Free (uses free tiers of Attio, Fireflies, Cal.com; Claude API cost negligible at ~$2.50 total for 5 demos)

## Drills Referenced
- the account research brief workflow (see instructions below) — assembles account intelligence and generates a structured meeting brief from CRM data, Clay enrichment, and prior call transcripts
- the technical demo content assembly workflow (see instructions below) — generates prospect-customized demo script with live API calls, integration code, architecture talking points, and technical follow-up package
- `threshold-engine` — evaluates play results against the pass threshold and recommends next action
