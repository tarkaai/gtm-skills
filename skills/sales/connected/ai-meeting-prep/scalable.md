---
name: ai-meeting-prep-scalable
description: >
  AI-Powered Meeting Preparation — Scalable Automation. Brief generation adapts per meeting type using
  feedback data. Multi-meeting context chains briefs across a deal's lifecycle. Briefs incorporate
  prior call transcripts, evolving competitive intelligence, and historical outcome patterns. A/B
  testing on prompt variants and section ordering finds the 10x multiplier.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct"
level: "Scalable Automation"
time: "65 hours over 2 months"
outcome: "AI prep used in >=80% of calls with >=30% better outcomes vs non-prepped calls over 2 months"
kpis: ["AI prep adoption rate", "Call outcome improvement", "Prep time savings", "Brief quality score"]
slug: "ai-meeting-prep"
install: "npx gtm-skills add sales/connected/ai-meeting-prep"
drills:
  - dashboard-builder
  - demo-prep-automation
---

# AI-Powered Meeting Preparation — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

Find the 10x multiplier. At Baseline, the system generates a meeting brief for every call. At Scalable, the system gets smarter: briefs adapt to meeting type (discovery briefs differ from demo briefs differ from negotiation briefs), incorporate context from ALL prior calls in a deal (not just the most recent), and the brief generation prompts are A/B tested to find the highest-quality output. The brief quality monitor tracks adoption, quality, and outcome correlation at scale.

**Pass threshold:** AI prep used in >=80% of calls with >=30% better outcomes vs non-prepped calls over 2 months.

## Leading Indicators

- Brief adoption rate exceeds 80% of all scheduled meetings
- Brief usefulness scores improve month-over-month (prompt optimization is working)
- Meeting type-specific briefs score higher than generic briefs
- Multi-meeting context chains produce richer briefs for second and third calls
- A/B test variants show statistically significant quality differences
- Demo prep briefs (from `demo-prep-automation`) lead to more next-step commitments

## Instructions

### 1. Differentiate Briefs by Meeting Type

Modify the the account research brief workflow (see instructions below) drill to use meeting type-specific prompts:

**Discovery call briefs** emphasize:
- Hypothesized pain points ranked by likelihood (from enrichment signals)
- Open-ended discovery questions with follow-up quantification questions
- Industry-specific context the prospect expects the caller to know
- Minimal product talk tracks (discovery is for listening)

**Demo briefs** use the `demo-prep-automation` drill:
- Pain-to-feature mapping from prior discovery call transcripts
- Custom demo flow ordered by prospect's stated priorities
- ROI estimates tied to prospect's quantified pain
- Objection preparation based on competitive landscape
- Recap video script for post-demo follow-up

**Negotiation briefs** emphasize:
- Full deal history: every interaction, promise, and next step
- BANT/MEDDIC score with gaps flagged
- Competitive positioning and price objection responses
- Stakeholder map with each person's influence and sentiment
- Fallback positions and walk-away criteria

**Executive review briefs** emphasize:
- Business case summary (aggregate ROI, strategic value)
- Executive-level talking points (no feature-level detail)
- Risk mitigation plan for common exec concerns
- Implementation timeline and resource requirements

Update the n8n workflow to detect meeting type from the Cal.com event type or from the deal stage, and route to the appropriate prompt variant.

### 2. Build Multi-Meeting Context Chains

When generating a brief for a second or third meeting in a deal, the system should pull ALL prior context:

1. Query all Attio notes tagged `meeting-brief` and `brief-feedback` for this deal, ordered by date
2. Query all Fireflies transcripts for this deal
3. Build a context chain:
   - What was discussed in each prior meeting
   - What next steps were agreed
   - Which of those next steps were completed
   - What new information has surfaced since the last meeting
   - How the stakeholder map has evolved
4. Feed this chain into the brief generation prompt so the new brief references prior conversations: "In your last call, {contact} mentioned {pain}. Follow up on whether they have explored {solution} since then."

This context chaining is what makes the second brief dramatically more valuable than the first.

### 3. Deploy the Brief Quality Monitor

Run the `dashboard-builder` drill to create the measurement layer:

- Build the PostHog dashboard with 6 panels (generation volume, adoption rate, quality scores, data completeness, best/worst sections, outcome correlation)
- Configure alerts for quality drops, adoption drops, and data source failures
- Set up the weekly metrics report that posts to Slack every Monday
- Establish the baseline metrics that the Durable optimizer will attempt to improve

### 4. A/B Test Brief Prompts

Use PostHog feature flags to split brief generation between prompt variants:

**Test 1: Section ordering**
- Variant A: Current order (executive summary first, questions after)
- Variant B: Questions first, executive summary last (hypothesis: the caller looks at questions first anyway)
- Success metric: `overall_usefulness` score from feedback loop
- Minimum sample: 30 meetings per variant

**Test 2: Question depth**
- Variant A: 5-7 questions with rationale
- Variant B: 10-12 questions without rationale (more options, less explanation)
- Success metric: number of questions from the brief that appear in the transcript

**Test 3: Objection preparation detail**
- Variant A: 2-sentence responses per objection
- Variant B: Full framework response with diagnostic questions and follow-up email draft
- Success metric: objection handling success (next step committed despite objection raised)

Run tests sequentially (1 at a time per the autonomous-optimization guardrails). Minimum 2 weeks per test. Implement winners and start the next test.

### 5. Scale to All Team Members

If the founding team has expanded to include AEs or SDRs:
- Configure the n8n workflow to generate briefs for ALL team members' calendars (not just the founder's)
- Customize briefs per caller: include the caller's personal talking style, prior relationship with the account, and expertise areas
- Track adoption and quality scores per team member — some may need training on how to use the briefs effectively

### 6. Evaluate Against Threshold

After 2 months, measure:

**Adoption rate:** `meeting_brief_generated` count / total meetings. Target: >=80%.

**Outcome improvement:** Compare `next_step_committed` rate for AI-prepped calls vs all calls before the play started (historical baseline from Smoke). Target: >=30% better.

**Quality trend:** Brief usefulness scores should be stable or improving over the 2-month period.

If PASS: proceed to Durable. If FAIL: diagnose using the brief quality dashboard. Common failure modes:
- Low adoption (team not reading briefs): simplify briefs, send via email instead of Attio note
- Low quality (briefs too generic): enrich more data sources, improve prompts based on feedback
- No outcome lift (briefs accurate but not impactful): the brief may be providing information the caller already knows — focus on surfacing NON-obvious insights

## Time Estimate

- 10 hours: Differentiate brief prompts by meeting type (discovery, demo, negotiation, exec)
- 8 hours: Build multi-meeting context chain logic
- 6 hours: Deploy brief quality monitor (dashboard, alerts, weekly report)
- 12 hours: Design and run 3 A/B tests on brief prompts (4 hours per test)
- 5 hours: Scale to additional team members (calendar integration, customization)
- 20 hours: Ongoing monitoring and optimization over 2 months (~2.5 hours/week)
- 4 hours: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal context, brief storage, context chains | $29/user/mo (Plus) or $59/user/mo (Pro) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — account research at scale | $185/mo (Launch) or $495/mo (Growth for higher volume) — [clay.com/pricing](https://www.clay.com/pricing) |
| Anthropic API | AI — brief generation, feedback scoring, A/B variants | Usage-based, ~$5-15/mo at 100+ meetings — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| n8n | Automation — brief triggers, feedback loops, A/B routing | $60/mo (Pro, 10K executions) — [n8n.io/pricing](https://n8n.io/pricing) |
| Fireflies | Transcription — context chains and feedback loop | $19/seat/mo (Pro) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Loom | Video — demo recap recordings | $12.50/mo (Business) — [loom.com/pricing](https://www.loom.com/pricing) |
| Cal.com | Scheduling — meeting trigger source | Free (self-hosted) or $12/seat/mo — [cal.com/pricing](https://cal.com/pricing) |
| PostHog | Analytics — quality dashboard, A/B tests, funnels | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost this level:** ~$80-200/mo. Key incremental costs: n8n Pro ($60), Fireflies ($19/seat x team), Anthropic API (~$10-15), Loom ($12.50). Clay upgrade to Growth if volume exceeds Launch limits.

## Drills Referenced

- the account research brief workflow (see instructions below) — now with meeting type-specific prompts and multi-meeting context chains
- the call brief feedback loop workflow (see instructions below) — continuous quality scoring feeding prompt optimization
- `dashboard-builder` — dashboard, alerts, and weekly reports tracking brief quality and impact at scale
- `demo-prep-automation` — specialized brief generation for demo meetings: pain-to-feature mapping, custom demo flow, ROI estimates, recap assets
