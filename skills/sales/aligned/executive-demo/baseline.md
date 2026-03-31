---
name: executive-demo-baseline
description: >
  Executive-Focused Demo — Baseline Run. Scale to 10-15 exec demos over 2 weeks
  with automated persona-specific demo prep, structured follow-up sequences, and
  continuous tracking. First always-on automation: agent generates exec research
  briefs, ROI narratives, and demo prep docs from enrichment data and discovery
  transcripts.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Baseline Run"
time: "22 hours over 2 weeks"
outcome: ">=75% exec demo-to-nextstep conversion and >=30% faster close time for exec-engaged deals over 2 weeks"
kpis: ["Exec demo-to-nextstep conversion", "Deal velocity (exec vs non-exec)", "Close rate (exec vs non-exec)", "Exec satisfaction score"]
slug: "executive-demo"
install: "npx gtm-skills add sales/aligned/executive-demo"
drills:
  - exec-demo-prep
  - posthog-gtm-events
  - follow-up-automation
---

# Executive-Focused Demo — Baseline Run

> **Stage:** Sales > Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

75% or more of exec demos result in a next-step commitment. Deals with exec engagement close at least 30% faster than deals without. Automated demo prep reduces founder preparation time by at least 50% compared to Smoke level manual research. 10-15 exec demos delivered over 2 weeks.

## Leading Indicators

- Exec demo prep docs are generated within 30 minutes of demo scheduling
- Persona-specific ROI narratives are consistently rated as accurate by the founder before demos
- Follow-up emails sent within 2 hours of every exec demo
- Executives who receive persona-specific demos ask more strategic questions (>=5 per demo)
- Exec-engaged deals move to the next pipeline stage faster than non-exec deals
- Follow-up materials (exec summary, business case snippet) are opened and forwarded

## Instructions

### 1. Configure automated exec demo prep

Run the `exec-demo-prep` drill to set up the automation pipeline. When an executive demo is scheduled:

1. The agent pulls exec contact data from Attio and runs `exec-research-enrichment` to gather priorities, news, and competitive context
2. If a prior discovery call exists, the agent runs BANT extraction on the Fireflies transcript
3. The agent classifies the exec persona (CEO/CFO/CTO/COO) and selects the appropriate ROI framing
4. The agent runs `roi-narrative-generation` to produce persona-specific talking points: opening hook, value narrative, key numbers, peer proof, risk framing, and closing question
5. The agent assembles the full exec demo prep document and stores it as an Attio note on the deal

**Human action required:** Review each auto-generated exec demo prep doc before the demo. Verify the exec research is current, the ROI numbers are defensible, and the opening hook is authentic. The agent does the research; the founder makes the judgment calls.

### 2. Build exec persona demo templates

Create demo templates in Attio for the top 4 exec personas. Each template includes:

**CEO template:**
- Default framing: growth, competitive advantage, market positioning
- ROI language: market share, revenue acceleration, first-mover advantage
- Common questions: "How does this fit our strategic roadmap?" "What is the competitive advantage?"
- Objection prep: "We have other priorities" -> connect product to their stated priority

**CFO template:**
- Default framing: payback period, cost avoidance, margin improvement, risk mitigation
- ROI language: NPV, IRR, payback months, cost per employee saved
- Common questions: "What is the total cost of ownership?" "What is the implementation risk?"
- Objection prep: "Budget is tight" -> show cost of inaction exceeds investment

**CTO template:**
- Default framing: technical debt reduction, engineering velocity, architecture simplification
- ROI language: developer-hours saved, incident reduction, deployment frequency
- Common questions: "How does this integrate with our stack?" "What is the security posture?"
- Objection prep: "We could build this internally" -> show build-vs-buy math

**COO/CRO template:**
- Default framing: operational efficiency, process standardization, team productivity
- ROI language: hours saved per rep, process cycle time reduction, scale without proportional headcount
- Common questions: "How does this scale with our team?" "What is the training overhead?"
- Objection prep: "Our team is resistant to change" -> show adoption path and quick wins

The agent personalizes each template with exec-specific research and discovery data. Templates reduce prep time while maintaining personalization.

### 3. Set up PostHog tracking for the exec demo funnel

Run the `posthog-gtm-events` drill to configure event tracking for the complete pipeline:

- `exec_demo_prep_generated` -- fired when the agent creates a prep doc
- `exec_demo_scheduled` -- fired when Cal.com booking is confirmed (with exec persona)
- `exec_demo_completed` -- fired after each demo with outcome, persona, questions, sentiment, duration
- `exec_followup_sent` -- fired when follow-up email and exec summary are sent
- `exec_nextstep_committed` -- fired when exec agrees to next step
- `exec_proposal_requested` -- fired when exec requests pricing/proposal
- `exec_deal_accelerated` -- fired when deal velocity increases post-exec engagement

Connect PostHog to Attio via n8n webhook so deal stage changes and exec engagement events are tracked automatically.

Build a PostHog comparison insight: "Deal velocity: exec-engaged vs all deals" -- measure average days from qualified to closed-won, split by whether the deal had at least one exec demo.

### 4. Execute demos and send automated follow-ups

**Human action required:** Run each exec demo live using the auto-generated prep doc.

Run the `follow-up-automation` drill configured for exec demo follow-ups:

1. **Within 2 hours of exec demo:** Agent generates and sends a follow-up email with:
   - Executive summary (3 bullet points matching the persona's priorities)
   - Key ROI numbers from the demo (persona-specific framing)
   - One peer proof point
   - Cal.com link for the next meeting
   - If the exec mentioned other stakeholders: a one-page internal summary they can forward

2. **If exec asked about specific topics during demo** (detected from Fireflies transcript): Agent appends relevant case studies or technical documentation to the follow-up.

3. **If no next step committed within 48 hours:** Agent drafts a nudge email referencing the cost of inaction discussed in the demo.

4. **If multiple execs are involved in the deal:** Agent generates an alignment summary showing which exec cares about what, and proposes a joint next step.

### 5. Monitor exec engagement impact on deal velocity

Track two cohorts in PostHog:
- **Exec-engaged deals:** Deals with at least one `exec_demo_completed` event
- **Non-exec deals:** Deals in the same pipeline without exec engagement

Compare weekly:
- Average days from qualified to proposal
- Average days from proposal to closed-won
- Close rate
- Average deal size

### 6. Evaluate over 2 weeks

After 2 weeks with 10-15 exec demos completed:
- Primary: >=75% of exec demos resulted in next-step commitment
- Primary: Exec-engaged deals close >=30% faster than non-exec deals
- Secondary: Exec demo prep time <20 minutes per demo (down from 60 min at Smoke)
- Secondary: Follow-up emails sent within 2 hours for 100% of demos
- Secondary: Average exec questions per demo >=5

If PASS, proceed to Scalable. If FAIL, diagnose:
- Low next-step rate but high engagement: closing technique or follow-up needs work
- Low engagement (few questions, short demos): persona classification is wrong or ROI framing missed the exec's actual priorities
- No deal velocity impact: exec demos are happening too late in the deal cycle; move them earlier
- Low prep doc quality: enrichment data is stale or persona templates need tuning

## Time Estimate

- 4 hours: initial setup (exec-demo-prep automation, PostHog events, follow-up workflows, persona templates)
- 10 hours: execute 10-15 exec demos (30-45 min each including prep review)
- 3 hours: review auto-generated prep docs (15 min each)
- 2 hours: review follow-up outputs and deal velocity data
- 2 hours: weekly funnel review and threshold evaluation
- 1 hour: iterate on persona templates based on results
- **Total: ~22 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM -- deal records, exec research notes, persona templates, pipeline | Free (3 users); Plus $29/user/mo |
| PostHog | Analytics -- exec demo funnel, deal velocity comparison | Free tier (1M events/mo) |
| Fireflies | Transcription -- discovery and exec demo call recording | Pro $10/user/mo (annual); Business $19/user/mo for API access |
| Cal.com | Scheduling -- exec demo booking links | Free (1 user); Teams $15/user/mo |
| Clay | Enrichment -- exec research, company intelligence | Explorer $149/mo (2,400 credits); Growth $349/mo |
| n8n | Automation -- exec demo prep pipeline, follow-up workflows | Free (self-hosted); Starter $24/mo cloud |
| Anthropic API | AI -- persona classification, ROI narrative generation, prep doc creation | ~$0.50-2.00 per exec demo prep (Claude Sonnet) |

**Estimated play-specific cost at Baseline:** ~$100-200/mo (Fireflies Pro + Clay Explorer + n8n Starter + Anthropic API usage)

## Drills Referenced

- `exec-demo-prep` -- auto-generate persona-specific exec demo prep docs with research, ROI narratives, and strategic talking points
- `posthog-gtm-events` -- configure event tracking for the exec demo funnel and deal velocity measurement
- `follow-up-automation` -- automated post-demo follow-up with persona-specific executive summaries and materials
