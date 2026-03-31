---
name: authority-verification-baseline
description: >
  Authority Verification — Baseline Run. Automate stakeholder enrichment on every new qualified deal
  so org charts are pre-built and authority roles are pre-classified before the first call. Verify
  authority is confirmed in >=80% of deals over 2 weeks with always-on tracking.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Baseline Run"
time: "15 hours over 2 weeks"
outcome: "Authority verified in >=80% of active deals over 2 weeks with automated enrichment triggering on every new deal"
kpis: ["Authority verification rate", "Time to authority confirmation", "Economic Buyer engagement rate", "Stakeholder auto-enrichment success rate", "Deal velocity (verified vs. unverified)"]
slug: "authority-verification"
install: "npx gtm-skills add sales/qualified/authority-verification"
drills:
  - stakeholder-enrichment-automation
  - posthog-gtm-events
  - threshold-engine
---

# Authority Verification — Baseline Run

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Authority verification runs continuously on every new qualified deal without manual enrichment work. When a deal enters the Qualified stage, the agent auto-enriches the org chart, pre-classifies stakeholders, and flags deals where no Economic Buyer is identified. The founder's discovery calls are focused on authority confirmation (not discovery from scratch), reducing time-to-verification to under 7 days. Authority should be verified in >=80% of active deals.

## Leading Indicators

- Auto-enrichment is firing on every new deal (check n8n execution logs for failures)
- Pre-call stakeholder maps are reducing discovery call prep time by 50%+ compared to Smoke
- Time from deal creation to authority verification is trending downward
- Deals with verified authority are advancing faster than unverified deals (this correlation validates the play)

## Instructions

### 1. Deploy stakeholder enrichment automation

Run the `stakeholder-enrichment-automation` drill to build an n8n workflow that triggers when a deal moves to Qualified stage in Attio:

1. Configure an Attio webhook (or 30-minute poll) for new deals entering Qualified stage
2. For each triggered deal, the workflow calls Clay to run org chart research: find 15-20 people at Director+ level across relevant departments
3. Each person is classified by Claude using `stakeholder-role-classification`: Economic Buyer, Champion, Influencer, Blocker, End User, or Gatekeeper
4. Classified stakeholders are written to Attio as Person records linked to the deal, with `stakeholder_role`, `stakeholder_confidence`, `stakeholder_sentiment` (default: Unknown), and `engagement_level` (default: No Contact)
5. A summary note is generated and attached to the deal: who was found, what roles were assigned, what gaps exist (no Economic Buyer, single-threaded risk)
6. The deal is flagged `stakeholder_mapped: true` with `stakeholder_map_date`

Verify the workflow by creating a test deal and confirming the full enrichment runs end-to-end.

### 2. Configure event tracking

Run the `posthog-gtm-events` drill to set up PostHog events for this play:

| Event | Properties | Source |
|-------|-----------|--------|
| `authority_deal_enriched` | deal_id, stakeholder_count, roles_found | n8n workflow |
| `authority_call_completed` | deal_id, person_id, authority_status | authority-discovery-call drill |
| `authority_verified` | deal_id, economic_buyer_id, verification_method | Attio field update |
| `authority_eb_engaged` | deal_id, economic_buyer_id, engagement_type | Email/meeting event |

Build a PostHog funnel: `deal_qualified` -> `authority_deal_enriched` -> `authority_call_completed` -> `authority_verified` -> `deal_advanced`.

### 3. Run authority discovery calls on enriched deals

For each deal with a pre-built stakeholder map, run the the authority discovery call workflow (see instructions below) drill. The key difference from Smoke: you now start with a map instead of building one from scratch.

1. Review the auto-generated stakeholder map — the agent has already identified likely Economic Buyers
2. For high-confidence EB classifications (title = CEO, VP with P&L ownership at <50 employees), consider authority verified without a call. Set `authority_verification_status: verified` and `verification_method: enrichment`.
3. For medium/low-confidence classifications, schedule a discovery call. The pre-call question generation now focuses specifically on confirming the EB, not discovering the org chart.
4. **Human action required:** Conduct 3-5 calls per week. Use the authority extraction prompt on each transcript. Update Attio with verification status.
5. For deals where the call reveals the EB is someone other than the current contact, create a task: "Get introduction to {EB name} via {Champion name}."

### 4. Monitor for 2 weeks

Track daily:
- How many new deals were auto-enriched? (Check n8n execution log)
- How many enrichments failed? (Clay returned 0 people, API errors)
- What is the current authority verification rate across all active deals?
- Are verified deals advancing faster than unverified deals?

Fix issues as they surface: if Clay enrichment consistently fails for a company type (very small, very private), document the fallback procedure (manual research using `stakeholder-research` drill).

### 5. Evaluate against threshold

Run the `threshold-engine` drill to evaluate: authority verified in >=80% of active deals over 2 weeks with automated enrichment triggering on every new deal.

Measure:
- Authority verification rate (target: >=80%)
- Auto-enrichment trigger rate (target: 100% of new Qualified deals)
- Average time to verification (target: <7 days)
- Deal velocity difference: verified vs. unverified deals

If PASS, proceed to Scalable. If FAIL, diagnose: is enrichment failing (Clay issue)? Are classifications inaccurate (role misidentification)? Are calls not happening fast enough (scheduling bottleneck)?

## Time Estimate

- n8n workflow build and testing: 4 hours
- PostHog event setup: 1 hour
- Discovery calls (3-5/week for 2 weeks, at 30 min each): 3-5 hours
- Daily monitoring and troubleshooting: 3 hours (15 min/day for 14 days)
- Threshold evaluation: 30 minutes

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with stakeholder fields and deal tracking | Free tier (up to 3 users) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Automated org chart enrichment | Launch plan $185/mo (~15 credits per company) — [clay.com/pricing](https://clay.com/pricing) |
| n8n | Automation workflows for enrichment triggers | Free (self-hosted) or Starter $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Fireflies | Call transcription for authority extraction | Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Event tracking and funnel analysis | Free (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic Claude | Stakeholder classification | Pay-per-use ~$3/MTok input — [anthropic.com/pricing](https://anthropic.com/pricing) |

**Estimated play-specific cost:** $50-100/mo (Clay credits are the main variable; n8n and PostHog fit free tiers at baseline volume)

## Drills Referenced

- `stakeholder-enrichment-automation` — n8n workflow that auto-enriches org charts and classifies stakeholders when deals enter Qualified
- the authority discovery call workflow (see instructions below) — structured call focused on confirming authority, now with pre-built stakeholder maps
- `posthog-gtm-events` — event taxonomy and tracking setup for authority verification funnel
- `threshold-engine` — evaluate results and determine pass/fail for level progression
