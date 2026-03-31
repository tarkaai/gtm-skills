---
name: technical-requirements-discovery-baseline
description: >
  Technical Requirements Discovery — Baseline Run. Run technical discovery on all qualified deals
  for 2 weeks with automated transcript extraction, fit scoring, and collateral matching to
  validate that the process is repeatable and predictive.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: "Technical discovery completed on >=80% of qualified opportunities over 2 weeks with technical fit scores predicting deal outcomes within 20% accuracy"
kpis: ["Technical discovery completion rate", "Technical fit prediction accuracy", "Time from qualification to technical assessment", "Collateral response rate", "Blocker resolution rate"]
slug: "technical-requirements-discovery"
install: "npx gtm-skills add sales/qualified/technical-requirements-discovery"
drills:
  - tech-stack-discovery
  - technical-discovery-call
  - posthog-gtm-events
  - threshold-engine
---

# Technical Requirements Discovery — Baseline Run

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Prove that technical discovery is repeatable and produces predictive signals. Over 2 weeks, >=80% of qualified deals should have technical discovery completed. The technical fit scores should correlate with actual deal outcomes: strong-fit deals progress faster, weak-fit deals stall or disqualify. The automated collateral matching should reduce time from discovery call to technical follow-up.

## Leading Indicators

- Technical discovery is happening within 48 hours of deal qualification (not getting delayed)
- Pre-call tech stack research accuracy is improving week-over-week as the agent calibrates
- Technical collateral follow-ups are sent within 24 hours of the discovery call (agent automation working)
- Deals flagged as "Needs SE Review" are getting solutions engineer calls scheduled within 1 week
- Technically disqualified deals are being removed from the pipeline rather than lingering

## Instructions

### 1. Standardize the technical discovery event taxonomy

Run the `posthog-gtm-events` drill to define technical discovery events. Create these events:
- `tech_stack_discovery_completed` — pre-call research done
- `tech_discovery_call_completed` — call happened and transcript extracted
- `tech_fit_score_applied` — scores written to CRM
- `tech_collateral_sent` — follow-up documents sent
- `tech_blocker_identified` — a deal-blocking requirement found
- `tech_blocker_resolved` — a previously identified blocker was resolved
- `tech_routing_changed` — deal moved to a new technical status

### 2. Run tech stack discovery on all new qualified deals

For every deal that enters "Qualified" stage in Attio during the 2-week period, immediately run the `tech-stack-discovery` drill. Target: research should complete within 24 hours of deal qualification.

The agent:
- Detects tech stack from public signals via Clay Claygent
- Predicts integration requirements and security posture
- Generates a call prep brief with priority questions
- Stores everything on the deal record in Attio

### 3. Conduct technical discovery calls

**Human action required:** For each researched deal, schedule a technical discovery call within 1 week of qualification. Use the `technical-discovery-call` drill:

1. Before each call: review the agent-generated call prep brief. Add any context from prior conversations.
2. Conduct the call with the prospect's technical stakeholder.
3. After the call: the agent extracts requirements from the Fireflies transcript, scores technical fit across 5 categories, and routes the deal.

Run the the technical fit scoring workflow (see instructions below) drill after each call to apply scores and determine routing.

### 4. Send matched technical collateral

After each technical discovery call, run the the technical collateral matching workflow (see instructions below) drill:
- The agent matches the prospect's specific requirements to your technical collateral catalog
- It generates a personalized follow-up email with relevant docs (API guides, security certs, integration docs, case studies)
- It flags collateral gaps where you lack documentation for a stated requirement

**Human action required:** Review the generated follow-up email and send it. Add any personal context. The goal is to send technical follow-up within 24 hours of the discovery call.

### 5. Build the technical objection library

As technical requirements accumulate across deals, catalog the patterns:
- Common integration demands and how to address each
- Security questionnaire answers (build a reusable master questionnaire)
- Architecture diagrams for common deployment scenarios
- FAQ answers for recurring technical concerns

Store this library as an Attio list called "Technical Objection Library" with fields: `objection_category`, `objection_text`, `response_text`, `supporting_collateral`, `frequency` (how many deals raised this).

### 6. Evaluate against threshold

Run the `threshold-engine` drill. Measure:
- Technical discovery completion rate: >=80% of qualified deals over 2 weeks
- Technical fit prediction accuracy: compare scores at time of scoring vs. deal outcomes for any deals that close during the period (target: within 20% accuracy)
- Time from qualification to technical assessment: target <=1 week
- Collateral follow-up speed: target <=24 hours after discovery call

If PASS, document the process as your standard technical discovery playbook and proceed to Scalable. If FAIL, diagnose:
- Low completion rate? Scheduling bottleneck — too many calls for the founder. Consider involving a solutions engineer earlier.
- Low prediction accuracy? The scoring rubric needs recalibration based on actual outcomes.
- Slow collateral follow-up? Collateral catalog is incomplete. Invest time filling gaps.

## Time Estimate

- Event taxonomy setup: 1 hour
- Tech stack research (agent runs per deal): 30 min/deal oversight, ~5-8 hours total
- Technical discovery calls (10-15 calls): 6-8 hours
- Collateral matching review and send: 2-3 hours
- Objection library building: 1-2 hours
- Threshold evaluation: 1 hour

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with technical scoring and routing | Plus $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Fireflies | Call recording and transcription | Pro $10/user/mo annual — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Cal.com | Discovery call scheduling | Free (1 user) — [cal.com/pricing](https://cal.com/pricing) |
| Clay | Tech stack enrichment via Claygent | Launch $185/mo — [clay.com/pricing](https://clay.com/pricing) |
| PostHog | Event tracking and funnels | Free (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API | Transcript analysis and requirement extraction | Sonnet 4.6: $3/$15 per 1M tokens — [claude.com/pricing](https://claude.com/pricing) |

**Estimated play-specific cost:** $40-60/mo (Fireflies Pro $10, Attio Plus $29 if exceeding free tier, Clay Claygent credits ~$10-20, Anthropic API ~$5-10 for 10-15 transcripts)

## Drills Referenced

- `tech-stack-discovery` — pre-call tech stack research from public signals
- `technical-discovery-call` — structured discovery call with transcript extraction
- the technical fit scoring workflow (see instructions below) — apply 5-category scoring rubric and route deals
- the technical collateral matching workflow (see instructions below) — match requirements to documentation and generate follow-up
- `posthog-gtm-events` — define and implement the technical discovery event taxonomy
- `threshold-engine` — evaluate results against pass threshold
