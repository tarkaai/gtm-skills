---
name: exec-demo-prep
description: Generate personalized executive demo preparation docs with persona-specific ROI narratives, strategic talking points, and company-tailored content
category: Sales
tools:
  - Clay
  - Anthropic
  - Attio
  - Fireflies
fundamentals:
  - exec-research-enrichment
  - roi-narrative-generation
  - roi-model-generation
  - stakeholder-role-classification
  - call-transcript-bant-extraction
  - fireflies-transcription
  - attio-notes
  - attio-deals
  - attio-contacts
---

# Executive Demo Prep

This drill takes a scheduled executive demo and produces a complete preparation package: executive research, persona-specific ROI narrative, strategic talking points, and a structured 15-20 minute demo flow. Designed for demos with C-level stakeholders where the conversation must be strategic, not tactical.

## Input

- Scheduled executive demo (from Cal.com booking or manual scheduling)
- Executive contact in Attio (name, title, company)
- Optional: Discovery call transcript from Fireflies (if a prior discovery call occurred with the exec or their team)
- Product feature catalog and case study library (stored in Attio or a markdown file)

## Steps

### 1. Identify the executive persona

Pull the executive's Attio contact record using `attio-contacts`. Classify their role using `stakeholder-role-classification`:

- **CEO/Founder**: Economic Buyer with strategic focus. Lead with competitive advantage and growth.
- **CFO/VP Finance**: Economic Buyer with financial focus. Lead with payback period and risk mitigation.
- **CTO/VP Engineering**: Influencer or Economic Buyer. Lead with architecture, technical debt, and engineering velocity.
- **COO/VP Operations**: Influencer. Lead with operational efficiency and scale readiness.
- **CRO/VP Sales**: Champion or Economic Buyer. Lead with pipeline velocity and rep productivity.

Store the persona classification on the contact record for reuse.

### 2. Research the executive

Run `exec-research-enrichment` to pull:
- Executive's stated priorities (from LinkedIn, conference talks, interviews)
- Recent company news (last 90 days)
- Earnings call themes (if public)
- Competitive landscape
- Pain signals (hiring patterns, Glassdoor, public complaints)

If a prior discovery call exists, run `fireflies-transcription` to get the transcript, then `call-transcript-bant-extraction` to extract pain points and BANT scores. Merge discovery data with enrichment data -- discovery data takes priority where both exist.

### 3. Generate the persona-specific ROI narrative

Run `roi-narrative-generation` with the exec persona, pain data, and company context. If an `roi-model-generation` output exists for this deal, feed it into the narrative generator for quantitative backing.

The ROI narrative produces:
- Opening hook tied to the exec's top priority
- Value narrative in persona-appropriate language
- Key numbers framed for the persona
- Peer proof point from a similar company
- Risk framing (cost of inaction)
- Closing question

### 4. Build the exec demo prep document

Using the research, ROI narrative, and pain data, generate the structured prep doc via Claude:

```
## Executive Demo Prep -- {Company Name}
### Exec: {Name}, {Title} ({Persona})
### Date: {demo_date}
### Duration: 15-20 minutes

### Pre-Demo Intelligence
- Exec priorities: {priorities from research}
- Recent company news: {key news items}
- Pain signals: {enrichment + discovery pains}
- BANT assessment: B:{score} A:{score} N:{score} T:{score}

### Opening Hook (30 seconds)
{roi_narrative.opening_hook}

Say: "{Exec name}, based on {specific priority or news item}, I want to show you how companies like yours are {achieving outcome}."

### Strategic Context (2 minutes)
- Frame the market problem in exec language (not feature language)
- Reference their competitive landscape: "{competitor} is doing X, your peers are moving toward Y"
- Connect your product to their stated strategic priorities

### Value Demonstration (8-10 minutes)
Show OUTCOMES, not features. For each pain:

#### Outcome 1: {Pain-linked business outcome}
- Business impact: {roi_narrative.key_numbers[0]}
- Show: {specific workflow or dashboard that demonstrates the outcome}
- Say: "{roi_narrative.value_narrative segment}"
- Peer proof: {roi_narrative.peer_proof}

#### Outcome 2: {Pain-linked business outcome}
- Business impact: {roi_narrative.key_numbers[1]}
- Show: {specific workflow or dashboard}
- Say: {talking point linked to exec priorities}

### ROI Summary (2 minutes)
- Total value: {roi_narrative.key_numbers summary}
- Payback: {payback period}
- Risk of inaction: {roi_narrative.risk_framing}
- Slides talking points: {roi_narrative.slides_talking_points}

### Next Steps (2-3 minutes)
- Proposed next step: {based on BANT and persona}
- If CEO: "What would you need to see to move this forward?"
- If CFO: "Shall I put together the full business case with your numbers?"
- If CTO: "Would a technical deep-dive with your team be useful?"
- Closing question: {roi_narrative.closing_question}

### Risk Factors & Objection Prep
- Likely objections based on persona: {persona-specific objection predictions}
- Competitive comparison points: {if competitor was mentioned in research}
- BANT gaps to probe: {any low BANT dimensions}

### Q&A Prep
Executives ask strategic questions. Prepare for:
- "How does this integrate with our {existing system from tech stack}?"
- "What's the implementation timeline and resource requirement?"
- "Who else in our industry uses this?"
- "What happens if this doesn't deliver the projected ROI?"
```

Store the full prep doc as an Attio note on the deal using `attio-notes`.

### 5. Prepare multi-exec alignment (when multiple execs attend)

If the demo has multiple executive attendees (detected from Cal.com booking):

1. Run steps 1-3 for each executive attendee
2. Identify conflicting priorities (e.g., CEO wants growth investment, CFO wants cost cutting)
3. Build a unified demo flow that addresses each exec's top concern:
   - Open with the most senior exec's priority
   - Transition to each other exec's concern with explicit callouts: "And {CFO name}, from a financial perspective..."
   - Close with a next step that involves all attendees

### 6. Track demo prep quality

Fire PostHog events:

```json
{
  "event": "exec_demo_prep_generated",
  "properties": {
    "deal_id": "...",
    "exec_persona": "CEO",
    "research_depth": "full|partial|persona_only",
    "roi_narrative_generated": true,
    "discovery_data_available": true,
    "multi_exec": false,
    "prep_generation_time_seconds": 45
  }
}
```

## Output

- Complete exec demo prep document stored in Attio
- Persona-specific ROI narrative with opening hook, key numbers, and closing question
- Executive research summary (priorities, news, competitive context)
- Multi-exec alignment plan (if applicable)
- PostHog tracking events

## Triggers

- Run when an executive demo is scheduled (Cal.com webhook for bookings with exec-level attendees)
- Re-run if new discovery data becomes available before the demo
- Re-run if the demo is rescheduled (exec priorities may have changed)
