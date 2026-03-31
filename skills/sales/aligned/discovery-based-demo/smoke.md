---
name: discovery-based-demo-smoke
description: >
  Discovery-Based Demo — Smoke Test. Run 5 product demos that open with discovery
  questions to uncover pain, then tailor the demo to those pains in real time.
  Validate that pain-based demos produce next-step commitments at a higher rate
  than generic feature walkthroughs.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=3 out of 5 demos yield next-step commitment via pain-based customization in 1 week"
kpis: ["Demo-to-nextstep conversion", "Demo engagement score", "Pain coverage rate", "Questions asked per demo"]
slug: "discovery-based-demo"
install: "npx gtm-skills add sales/aligned/discovery-based-demo"
drills:
  - bant-discovery-call
  - threshold-engine
---

# Discovery-Based Demo — Smoke Test

> **Stage:** Sales > Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Outcomes

3 or more out of 5 demos result in a next-step commitment (technical evaluation, proposal request, or stakeholder introduction). Pain-based demos outperform your historical generic demo conversion rate by at least 30%.

## Leading Indicators

- Prospects ask follow-up questions during the demo (>=5 questions per demo = high engagement)
- Prospects reference their own pain during the demo ("Yes, that is exactly our problem")
- Prospect requests a recap or additional information after the demo
- Meeting runs past scheduled time because prospect wants to see more

## Instructions

### 1. Run discovery before every demo

For each of 5 scheduled demos, run the `bant-discovery-call` drill on the preceding discovery call. This produces BANT scores and extracts pain points with exact prospect quotes. If no separate discovery call exists, dedicate the first 10-15 minutes of the demo call itself to structured discovery.

Focus the discovery on:
- What is the prospect's current workflow for the problem your product solves
- Where does that workflow break down (specific pain)
- What is the cost of that pain (hours wasted, revenue lost, team frustration)
- Who else is affected by this pain

### 2. Build a pain-to-feature map for each demo

After discovery, manually create a simple document for each demo:

```
Prospect: {name}
Pain 1: "{exact quote}" -> Feature: {feature name} -> ROI: {estimate}
Pain 2: "{exact quote}" -> Feature: {feature name} -> ROI: {estimate}
Pain 3: "{exact quote}" -> Feature: {feature name} -> ROI: {estimate}
Demo order: Pain 1 feature first, then Pain 2, then Pain 3
Opening line: "You mentioned {pain 1} -- let me show you how we solve that."
```

This is manual at Smoke level. The agent assists with transcript analysis, but the founder builds the map.

### 3. Execute the discovery-based demo

**Human action required:** Run the demo live. Follow this structure:

1. **Recap (2 min):** Summarize what you heard in discovery. "Last time you told me about X, Y, and Z. Did I get that right?" This shows you listened and lets the prospect correct or add context.
2. **Pain 1 feature (8 min):** Show the feature that solves their top pain. Reference their exact words. Quantify the value. "You said you spend 10 hours a week on manual reports -- this automates that."
3. **Pain 2 feature (8 min):** Transition naturally. "You also mentioned X was a problem..." Show the relevant feature.
4. **Pain 3 feature (5 min):** Cover the third pain if time allows.
5. **Summary and next step (5 min):** Recap total value. Propose a specific next step. "Based on what we covered, I think the next step is [specific action]. Does that work?"

### 4. Log results in Attio

After each demo, log the outcome in Attio on the deal record. Create a note with:

- Date and duration of demo
- Pains addressed (which ones from discovery)
- Outcome: next_step_committed, follow_up_needed, or no_interest
- What the next step is (if committed)
- Number of questions the prospect asked
- Any objections raised

### 5. Track events in PostHog

For each demo, fire PostHog events:

- `demo_completed` with properties: `deal_id`, `outcome`, `pains_addressed` (count), `questions_asked` (count), `duration_minutes`, `discovery_method` ("separate_call" or "inline")
- `demo_nextstep` if next step was committed, with property: `next_step_type` ("technical_eval", "proposal", "stakeholder_intro", "other")

### 6. Evaluate against threshold

Run the `threshold-engine` drill after all 5 demos are complete. The threshold engine checks:

- Primary: >=3 out of 5 demos yielded a next-step commitment
- Secondary: Average questions asked per demo >=5 (engagement signal)
- Secondary: All 3 pains from discovery were addressed in each demo (pain coverage = 100%)

If PASS, document your pain-to-feature mapping process and proceed to Baseline. If FAIL, diagnose: was the problem discovery quality (not enough pain uncovered), demo execution (features shown did not match pains), or prospect fit (wrong ICP).

## Time Estimate

- 30 min per demo for discovery prep (review transcript, build pain-feature map): 2.5 hours
- 45 min per demo execution: 3.75 hours
- 15 min per demo for logging results: 1.25 hours
- 30 min for threshold evaluation: 0.5 hours
- **Total: ~8 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM -- deal records, notes, pipeline tracking | Free tier for up to 3 users; Plus $29/user/mo |
| PostHog | Analytics -- demo events and funnel tracking | Free tier includes 1M events/mo |
| Fireflies | Transcription -- discovery call recording and transcript | Free tier 800 min/mo; Pro $10/user/mo annually |
| Cal.com | Scheduling -- demo booking links | Free for 1 user; Teams $15/user/mo |

**Estimated play-specific cost at Smoke:** $0 (all tools have free tiers sufficient for 5 demos)

## Drills Referenced

- `bant-discovery-call` -- structured discovery questioning, transcript BANT extraction, CRM logging
- `threshold-engine` -- evaluate demo results against pass/fail criteria
