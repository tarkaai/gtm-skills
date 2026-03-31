---
name: executive-demo-smoke
description: >
  Executive-Focused Demo — Smoke Test. Run 3+ executive demos with manual
  persona-specific preparation. Validate that condensed, business-outcome-focused
  demos for C-level stakeholders produce next-step commitments at higher rates
  than generic feature walkthroughs.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=3 exec demos with >=70% next-step commitment within 1 week"
kpis: ["Exec demo-to-nextstep conversion", "Demo duration (target 15-20 min)", "Questions asked per demo", "Sentiment score"]
slug: "executive-demo"
install: "npx gtm-skills add sales/aligned/executive-demo"
drills:
  - bant-discovery-call
  - threshold-engine
---

# Executive-Focused Demo — Smoke Test

> **Stage:** Sales > Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

3 or more executive demos delivered within 1 week, with at least 70% resulting in a next-step commitment (follow-up meeting, proposal request, technical evaluation, or stakeholder introduction). Demos stay within 15-20 minutes. Executives ask strategic questions during the demo, confirming engagement.

## Leading Indicators

- Executive asks follow-up questions during the demo (>=3 questions = engaged)
- Executive references their own strategic priorities during the demo ("Yes, that is exactly what we are trying to solve")
- Executive requests materials to share with their team or board
- Executive proposes the next step themselves rather than waiting for you to ask
- Demo runs close to 15-20 minutes (not 5 minutes of disengagement, not 45 minutes of feature overload)

## Instructions

### 1. Identify executive demo opportunities

Review your Attio pipeline for deals that have C-level stakeholders (CEO, CFO, CTO, COO, CRO, VP+) as contacts. You need at least 3 scheduled or schedulable executive demos this week.

For each exec, manually research:
- Their LinkedIn profile: recent posts, stated priorities, role description
- Company news from the last 90 days: funding, product launches, leadership changes, earnings themes
- Their likely top 3 priorities based on role (CEO = growth/competitive advantage, CFO = margins/cash flow, CTO = technical debt/velocity, COO = efficiency/scale)

Store this research as an Attio note on the deal record.

### 2. Run discovery to understand exec-specific pain

If a prior discovery call exists with this account, run the `bant-discovery-call` drill on the transcript. Extract BANT scores and pain points with exact prospect quotes.

If no prior discovery exists, dedicate the first 5 minutes of the exec demo itself to strategic discovery:
- "What is the single biggest challenge your team is facing this quarter?"
- "If you could solve one thing before your next board meeting, what would it be?"
- "What does success look like for your organization in the next 12 months?"

These are strategic questions, not tactical ones. Executives do not answer "walk me through your current workflow."

### 3. Build a persona-specific demo prep document

For each executive demo, manually create a prep doc:

```
Executive: {name}, {title} ({persona: CEO/CFO/CTO/COO})
Company: {company}
Top 3 priorities: {from research}
Pains from discovery: {if available, with exact quotes}

Opening hook (30 seconds):
"{Exec name}, based on {specific priority or news item}, I want to show you
how companies like yours are {achieving business outcome}."

Demo flow (15-20 minutes total):
1. Strategic context (2 min): Frame the market problem in their language.
   - For CEO: "While your competitors are still doing X manually..."
   - For CFO: "The hidden cost of {pain} across your organization is..."
   - For CTO: "Your engineering team is spending {X hours} on {problem} instead of..."

2. Outcome 1 (5-7 min): Show the business outcome, not the feature.
   - What it solves: {pain from discovery or research}
   - ROI framing: {persona-specific — CEO gets market share, CFO gets payback}
   - Proof: "Companies like {peer company} saw {result} in {timeframe}"

3. Outcome 2 (5-7 min): Second business outcome.
   - What it solves: {second pain}
   - ROI framing: {persona-specific}

4. Summary and next step (3 min):
   - Total value recap in one sentence
   - Risk of inaction: "Every month without this costs you approximately {amount}"
   - Closing: Propose a specific next step appropriate to the persona
```

This is manual at Smoke level. The founder builds the prep doc and runs the demo.

### 4. Execute the executive demo

**Human action required:** Run the demo live. Follow the strict structure:

1. **Opening hook (30 sec):** Reference their specific priority. Establish relevance immediately. No small talk beyond 30 seconds.
2. **Strategic context (2 min):** Frame the market problem in executive language. No feature names. No technical jargon (unless CTO). Use phrases like "strategic advantage," "margin improvement," "risk reduction," "competitive positioning."
3. **Outcome 1 (5-7 min):** Show the product solving their top pain. Lead with the business outcome. Use the ROI framing appropriate to their persona. Include one peer proof point.
4. **Outcome 2 (5-7 min):** Second outcome tied to their second priority.
5. **Summary and close (3 min):** Recap total value. State cost of inaction. Propose specific next step. Ask: "What would you need to see to move this forward?"

Reserve 5 minutes at the end for Q&A. Executive questions are your strongest engagement signal.

### 5. Log results in Attio

After each demo, create an Attio note on the deal with:

- Date, exec name, exec title, exec persona (CEO/CFO/CTO/etc.)
- Demo duration in minutes
- Number of questions the exec asked
- Sentiment score (1-5: 1=disengaged, 3=neutral, 5=enthusiastic)
- Outcome: `next_step_committed`, `follow_up_needed`, or `no_interest`
- What the committed next step is (if applicable)
- Which ROI framing resonated most (what the exec reacted to)
- Any objections raised and how they were handled

### 6. Track events in PostHog

For each exec demo, fire PostHog events:

- `exec_demo_completed` with properties: `deal_id`, `exec_persona`, `outcome`, `duration_minutes`, `questions_asked`, `sentiment_score`
- `exec_nextstep_committed` if next step was committed, with property: `next_step_type` ("technical_eval", "proposal", "stakeholder_intro", "board_review", "other")

### 7. Evaluate against threshold

Run the `threshold-engine` drill after all demos are complete. The threshold engine checks:

- Primary: >=3 exec demos delivered within 1 week
- Primary: >=70% of exec demos yielded a next-step commitment
- Secondary: Average demo duration between 15-20 minutes
- Secondary: Average questions asked per demo >=3

If PASS, document which persona-specific approaches worked best and proceed to Baseline. If FAIL, diagnose:
- Low next-step rate but high engagement (questions asked, long duration): closing technique needs improvement, not the demo itself
- Short duration and few questions: exec was not engaged — the opening hook missed their priorities
- Exec talked about features instead of outcomes: you led with features — rewrite the demo flow to lead with business outcomes

## Time Estimate

- 1 hour per demo for exec research and prep doc creation: 3 hours
- 30 minutes per demo execution (15-20 min demo + 10 min buffer): 1.5 hours
- 20 minutes per demo for logging results: 1 hour
- 30 minutes for threshold evaluation: 0.5 hours
- 2 hours buffer for scheduling, rescheduling, and ad-hoc prep: 2 hours
- **Total: ~8 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM -- deal records, exec research notes, pipeline tracking | Free tier for up to 3 users; Plus $29/user/mo |
| PostHog | Analytics -- exec demo events and conversion tracking | Free tier includes 1M events/mo |
| Fireflies | Transcription -- discovery call recording (if available) | Free tier 800 min/mo; Pro $10/user/mo annually |
| Cal.com | Scheduling -- exec demo booking links | Free for 1 user; Teams $15/user/mo |

**Estimated play-specific cost at Smoke:** $0 (all tools have free tiers sufficient for 3-5 exec demos)

## Drills Referenced

- `bant-discovery-call` -- structured discovery questioning, transcript BANT extraction, CRM logging (used on prior discovery calls if available)
- `threshold-engine` -- evaluate exec demo results against pass/fail criteria
