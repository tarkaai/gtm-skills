---
name: technical-fit-objection-baseline
description: >
  Technical Fit Objection Handling — Baseline Run. Always-on technical gap assessment and proof
  delivery for every deal that encounters a technical objection. Automated tracking of objection
  types, response strategies, and resolution outcomes across the full pipeline.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct"
level: "Baseline Run"
time: "15 hours over 2 weeks"
outcome: "Technical objections assessed and responded to on >=80% of instances over 2 weeks with >=65% achieving resolution that advances the deal"
kpis: ["Objection resolution rate", "Gap assessment coverage (% of objections assessed)", "Technical proof effectiveness", "Roadmap commitment accuracy"]
slug: "technical-fit-objection"
install: "npx gtm-skills add sales/connected/technical-fit-objection"
drills:
  - technical-gap-assessment
  - technical-proof-library
  - posthog-gtm-events
---

# Technical Fit Objection Handling — Baseline Run

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct

## Outcomes

First always-on automation. Every technical objection that enters the pipeline gets a structured gap assessment and matched proof assets automatically. The agent detects technical objections from call transcripts and CRM notes, runs the gap assessment, retrieves relevant proof, and queues the response for the founder. Do results hold over time with higher volume?

**Pass threshold:** Technical objections assessed and responded to on >=80% of instances over 2 weeks with >=65% achieving resolution that advances the deal.

## Leading Indicators

- Gap assessments auto-generated within 4 hours of a technical objection being logged
- Proof assets matched and delivered for >=70% of identified gaps
- Response plans reviewed and sent by founder within 24 hours of generation
- Workaround acceptance rate holding at >=50%
- Roadmap commitment delivery tracking is active (no commitments going untracked)

## Instructions

### 1. Configure Event Tracking

Run the `posthog-gtm-events` drill to set up the technical objection event taxonomy in PostHog. Define these events:

- `tech_objection_raised` — properties: deal_id, company, objection_category (integration, security, performance, feature, architecture, migration), objection_quote, prospect_priority (must_have, nice_to_have)
- `tech_gap_assessment_completed` — properties: deal_id, total_requirements, gap_count, dealbreaker_count, fit_verdict
- `proof_asset_retrieved` — properties: deal_id, gap_type, asset_type, asset_id
- `proof_asset_delivered` — properties: deal_id, asset_id, delivery_method (call, email, chat)
- `tech_objection_resolved` — properties: deal_id, resolution_strategy, outcome (resolved, partially_resolved, unresolved, deal_lost), days_to_resolution
- `roadmap_commitment_made` — properties: deal_id, feature, committed_date, commitment_type (verbal, contractual)
- `workaround_demonstrated` — properties: deal_id, workaround_type, prospect_response (accepted, partially_accepted, rejected)

Connect PostHog to Attio via n8n webhook so deal stage changes fire events automatically.

### 2. Build the Technical Proof Library

Run the `technical-proof-library` drill to create the searchable proof asset catalog:

- Audit all existing technical documentation, benchmarks, architecture diagrams, and customer references
- Classify each asset by gap type and objection category
- Store the catalog in Attio as structured records
- Set up the retrieval workflow in n8n so proof assets can be fetched by gap type
- Establish baseline effectiveness scores (use Smoke test data if available)

**Human action required:** The founder must identify and catalog existing proof assets. The agent structures and indexes them, but the founder knows which case studies, benchmarks, and architecture docs exist.

### 3. Automate Gap Assessment on Every Technical Objection

Build an n8n workflow triggered when a technical objection is logged in Attio:

**Trigger:** Attio webhook when `tech_objection_raised` event fires or when a deal note is tagged with "technical objection."

**Step 1:** Pull all deal context from Attio — company, requirements, prior technical notes, tech stack data.

**Step 2:** Run the `technical-gap-assessment` drill automatically — extract requirements, match against capabilities, classify gaps, generate response plan.

**Step 3:** Query the proof library for assets matching each identified gap.

**Step 4:** Package the gap assessment + matched proof assets into a response brief and store as an Attio note on the deal.

**Step 5:** Notify the founder via Slack with a summary: "{Company} raised a {category} technical objection. Gap assessment complete: {verdict}. {gap_count} gaps found, {dealbreaker_count} dealbreakers. Response plan ready in Attio."

**Human action required:** The founder reviews the response plan and proof assets, then delivers the technical response to the prospect.

### 4. Track Objection Resolution Outcomes

After each technical response is delivered, track the outcome:

- When the prospect responds (via email, call, or meeting), log the resolution status in Attio
- Fire `tech_objection_resolved` event in PostHog with the resolution strategy and outcome
- If a roadmap commitment was made, create a tracking record with the committed date
- If a workaround was demonstrated, log the prospect's acceptance level

Build a simple Attio saved view: "Active Technical Objections" showing all deals with unresolved technical gaps, sorted by severity and days since objection.

### 5. Monitor and Evaluate Over 2 Weeks

Let the automated workflow run for 2 weeks. Monitor:
- Assessment coverage: what percentage of technical objections get a gap assessment within 4 hours?
- Resolution rate: what percentage of assessed objections reach resolution?
- Proof utilization: what percentage of gap assessments include matched proof assets?
- Time to resolution: how many days from objection raised to objection resolved?

Run the `threshold-engine` at the end of 2 weeks:
- Pass threshold: >=80% coverage AND >=65% resolution rate
- If PASS: proceed to Scalable
- If FAIL: diagnose whether the bottleneck is assessment quality (wrong gap classification), proof gaps (missing assets for common objection types), or response delay (founder not reviewing fast enough)

## Time Estimate

- 3 hours: Configure PostHog event tracking and Attio attributes
- 4 hours: Build and catalog the technical proof library
- 3 hours: Build n8n automation for gap assessment + proof retrieval + notification
- 3 hours: Monitor and respond to objections over 2 weeks (~15 min per objection)
- 2 hours: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal tracking, gap assessment storage, proof library, objection logging | $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — tech stack detection for proactive gap prediction | $185/mo (Launch) — [clay.com/pricing](https://www.clay.com/pricing) |
| Fireflies | Transcription — automated call transcript extraction | $10/user/mo (Pro, annual) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics — event tracking, funnel analysis | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Automation — gap assessment trigger, proof retrieval, notifications | $24/mo (Starter) or free self-hosted — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | AI — gap classification, response generation | Claude Sonnet 4.6: $3/$15 per 1M tokens — [claude.com/pricing](https://claude.com/pricing) |

**Estimated play-specific cost this level:** ~$25-50/mo incremental. Primary new cost: n8n Starter ($24/mo) if not already in stack. Anthropic API usage: ~$5-15/mo for 20-30 gap assessments.

## Drills Referenced

- `technical-gap-assessment` — assess prospect technical requirements against product capabilities, classify gaps, generate response strategies
- `technical-proof-library` — build and maintain the searchable library of proof assets, with retrieval workflow and effectiveness tracking
- `posthog-gtm-events` — define and implement the event taxonomy for tracking technical objections
