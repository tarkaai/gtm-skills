---
name: competitive-objection-handling-baseline
description: >
  Competitive Objection Handling — Baseline Run. Automate competitive detection in call
  transcripts and emails, auto-pull battlecards when competitors are detected, and track
  positioning effectiveness per competitor over 2 weeks of always-on operation.
stage: "Sales > Aligned"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: ">=45% competitive win rate and >=80% of competitive deals with response delivered within 4 hours of detection over 2 weeks"
kpis: ["Competitive win rate", "Time to competitive response", "Detection accuracy", "Positioning framework effectiveness by competitor"]
slug: "competitive-objection-handling"
install: "npx gtm-skills add sales/aligned/competitive-objection-handling"
drills:
  - competitive-detection-automation
  - competitive-objection-response
  - posthog-gtm-events
---

# Competitive Objection Handling — Baseline Run

> **Stage:** Sales > Aligned | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Automate the detection of competitor mentions in sales calls and emails so no competitive signal goes unnoticed. When a competitor is detected, auto-pull the battlecard and draft a positioning response within 2 hours of call end. Achieve >= 45% competitive win rate and >= 80% of competitive deals with a structured response delivered within 4 hours of detection. This proves the always-on detection + response pipeline works before scaling.

## Leading Indicators

- Fireflies transcripts processing and triggering competitive scans within 30 minutes of call end
- Competitive detection firing for >= 90% of calls where a competitor was mentioned (verified by seller review)
- Battlecard auto-pulled and response drafted before the seller's next prep session
- False positive rate below 15% (non-competitive deals flagged as competitive)
- Positioning responses reviewed and delivered within 4 hours of detection for >= 80% of deals

## Instructions

### 1. Deploy the competitive detection pipeline

Run the `competitive-detection-automation` drill to configure the always-on detection system:

**Fireflies webhook setup:**
Create an n8n workflow triggered by Fireflies transcript completion. When a new transcript is available:
1. Fetch the full transcript
2. Match to a deal in Attio by attendee email or calendar event
3. Run keyword scan for known competitor names (from Attio Competitors object)
4. Run semantic scan via Claude for indirect competitor references ("another vendor," "what we're using now," "evaluating options")
5. If competitor detected: classify objection type, severity, and risk level
6. Route: low/medium risk -> queue response. High/critical risk -> Slack alert + immediate response queue

**Email detection:**
Set up a parallel n8n workflow triggered by Attio email activity webhooks. Scan incoming emails for competitor mentions using the same keyword + semantic approach. Feed into the same routing logic.

**Human action required:** Test the pipeline end-to-end with 2-3 real calls before going live. Verify: Fireflies captures the transcript, the webhook fires, the competitive scan runs, and the correct competitor is identified. Check for false positives and false negatives.

### 2. Configure PostHog event tracking

Run the `posthog-gtm-events` drill to set up the event taxonomy for competitive handling:

- `competitor_detected` — fires when a competitor is identified in a transcript or email. Properties: deal_id, competitor_name, detection_source, competitive_objection_type, severity, time_to_detection_minutes
- `competitive_objection_handled` — fires when the positioning response is delivered. Properties: deal_id, competitor_name, positioning_framework, outcome, severity, hinge_criterion, days_to_resolution, battlecard_version_used
- `competitive_positioning_generated` — fires when the AI generates a response. Properties: deal_id, competitor_name, framework, risk_assessment
- `competitive_deal_closed` — fires when a competitive deal reaches won or lost. Properties: deal_id, competitor_name, outcome, deciding_factor

Set up a PostHog funnel: `competitor_detected` -> `competitive_positioning_generated` -> `competitive_objection_handled` -> `competitive_deal_closed`

### 3. Validate detection accuracy

For the first 2 weeks, manually verify every detection result:

For each call where the system detected a competitor:
- **True positive:** Competitor was actually mentioned. Good.
- **False positive:** No competitor was mentioned. Tune the detection prompt to reduce false signals.

For each call where the system did NOT detect a competitor:
- **True negative:** No competitor was present. Good.
- **False negative:** A competitor was mentioned but missed. Add the competitor name to the keyword list and tune the semantic scan.

Calculate after 2 weeks:
- **Precision:** True positives / (true positives + false positives). Target: >= 0.85
- **Recall:** True positives / (true positives + false negatives). Target: >= 0.90

If below target, adjust the detection prompts and keyword lists.

### 4. Handle competitive objections with always-on support

For each detected competitive objection, run the `competitive-objection-response` drill:

1. Auto-pull the battlecard for the detected competitor
2. Generate a positioning response using the deal's pain data + battlecard intelligence
3. Notify the seller via Slack with: competitor name, objection type, severity, draft response, and battlecard link

**Human action required:** Review the generated positioning response before delivery. Verify factual accuracy, edit for your voice, and deliver on the next call or via follow-up email. Log the outcome in Attio.

The goal at Baseline is to handle every competitive objection with a data-backed response within 4 hours of detection. The agent does the research and drafting; you do the delivery and judgment.

### 5. Update battlecards from outcomes

After each competitive interaction, the outcome data feeds back into the battlecard:
- Won deals: strengthen the "When We Win" section with the latest winning approach
- Lost deals: strengthen the "When We Lose" section with the latest loss patterns
- New objection types or competitor claims: add to battlecard

Configure an n8n workflow to auto-refresh battlecards weekly (from the `competitive-battlecard-assembly` drill).

### 6. Evaluate against threshold

After 2 weeks, measure:
- What is the competitive win rate? (Target: >= 45%)
- What percentage of competitive deals received a structured response within 4 hours? (Target: >= 80%)
- What is the detection accuracy (precision and recall)?
- Which positioning frameworks are working per competitor?

If **PASS**: The automated detection + response pipeline is working. Proceed to Scalable to add A/B testing on positioning frameworks and scale battlecard intelligence.

If **FAIL**: Diagnose:
- **Low win rate:** Review which competitors you're losing to and why. Are battlecards accurate? Is the positioning framework appropriate for the objection type?
- **Slow response time:** Is the detection pipeline running reliably? Check n8n execution logs for failures or delays.
- **Low detection accuracy:** Tune the semantic scan prompt. Add competitor aliases and product names to keyword lists.

## Time Estimate

- Detection pipeline setup and testing: 4 hours
- PostHog event configuration: 2 hours
- Detection validation (2 weeks of reviews): 3 hours
- Competitive calls and response delivery (~10 competitive interactions): 5 hours
- Battlecard maintenance: 2 hours
- Weekly review and threshold evaluation: 4 hours
- **Total: ~20 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, competitor records, battlecards | Plus $29/user/mo |
| Fireflies | Auto-transcribe sales calls for competitive detection | Pro $10/user/mo (annual); Business $19/user/mo |
| Claude API (Anthropic) | Competitive scan, positioning generation, battlecard synthesis | Sonnet: $3/$15 per M tokens; ~$0.30-0.80 per call |
| PostHog | Event tracking, funnels, competitive analytics | Free tier (1M events/mo) |
| n8n | Webhook automation (Fireflies -> detection -> CRM -> response) | Starter $24/mo; Pro $60/mo |
| Clay | Competitor enrichment for battlecard updates | Launch $185/mo |

**Estimated play-specific cost at Baseline:** ~$75-150/mo (Fireflies Pro + n8n Starter + Claude API usage). CRM and PostHog on free tiers for small teams.

## Drills Referenced

- `competitive-detection-automation` — Always-on monitoring of call transcripts and emails for competitor mentions with automated classification and routing
- `competitive-objection-response` — Pull battlecard, generate positioning response, log outcome
- `posthog-gtm-events` — Define and implement the event taxonomy for competitive tracking
