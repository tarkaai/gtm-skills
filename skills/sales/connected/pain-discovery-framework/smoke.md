---
name: pain-discovery-framework-smoke
description: >
  Pain Discovery Framework — Smoke Test. Run 3 structured discovery calls with manual prep
  and note-taking to validate that you can consistently surface and quantify prospect pain
  points at >= 5x product cost.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Smoke Test"
time: "7 hours over 1 week"
outcome: ">=3 quantified pain points per prospect for >=3 prospects with total pain >=5x product cost in 1 week"
kpis: ["Pain points per prospect", "Quantification rate", "Pain-to-price ratio", "Discovery call quality"]
slug: "pain-discovery-framework"
install: "npx gtm-skills add sales/connected/pain-discovery-framework"
drills:
  - pain-discovery-call-prep
  - threshold-engine
---

# Pain Discovery Framework — Smoke Test

> **Stage:** Sales > Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

Run 3 structured discovery calls and extract >= 3 quantified pain points per prospect. Each prospect's total quantified pain must exceed 5x your product's annual price. This proves you can consistently uncover pain that justifies your price before investing in automation.

## Leading Indicators

- Call prep documents generated with >= 4 hypothesized pains per prospect
- Prospect talk-time ratio >= 70% during discovery calls
- At least 2 pains per call reach "explored" or "quantified" depth
- Prospects volunteer dollar figures or time estimates without prompting

## Instructions

### 1. Define your pain discovery ICP

Before scheduling calls, clarify which prospects are likely to have quantifiable pain your product solves. Document:
- Company size range (headcount and revenue) where the pain is large enough to matter
- Job titles of people who experience the pain daily and can describe it
- Industries or verticals where the pain is acute
- Trigger events that make the pain urgent (hiring, funding, compliance deadlines)

### 2. Schedule 3 discovery calls

Identify 3 prospects from your existing pipeline or network who match the ICP and have agreed to a conversation. Book 45-minute calls using Cal.com. These should be net-new discovery conversations, not demos or follow-ups.

### 3. Prepare for each call

Run the `pain-discovery-call-prep` drill for each scheduled call. The drill:
- Pulls deal context from Attio
- Enriches the prospect company via Clay (firmographics, recent news, job postings)
- Generates 5 hypothesized pain areas with tailored discovery questions
- Produces a structured call prep document with question guide and call structure
- Stores the prep as an Attio note and verifies Fireflies recording

Review the call prep document before each call. Internalize the top 3 pain hypotheses and their discovery questions. Do not read from the script — use it as a guide.

### 4. Execute the discovery calls

**Human action required:** Conduct the 3 discovery calls. Follow these rules:

- **Listen 70%, talk 30%.** Your job is to ask questions and shut up.
- **Never pitch.** This is discovery, not a demo. If the prospect asks about your product, say "I want to make sure I understand your situation first — we can cover that next time."
- **Go deep on pain.** When a pain surfaces, probe: "Tell me more about that." / "How often does that happen?" / "What does that cost you?" / "What have you tried?" / "What happens if you don't solve it this quarter?"
- **Quantify everything.** Push for numbers: "How many hours per week?" / "How many people are affected?" / "What's the revenue impact?" / "What are you spending on the current workaround?"
- **Capture exact quotes.** Write down the prospect's exact words. These power the business case later.
- **Follow the energy.** If the prospect lights up about a pain, go deeper there even if it wasn't in your prep.

### 5. Log results after each call

Within 1 hour of each call, manually log the following in Attio as a note on the deal:

```markdown
## Discovery Call Results — {date}
### Prospect: {company} / {contact name, title}

### Pains Discovered
| # | Pain | Category | Depth | Estimated Annual Cost | Key Quote |
|---|------|----------|-------|----------------------|-----------|
| 1 | {description} | {operational/financial/strategic/technical/compliance} | {surface/explored/quantified} | ${estimate or "TBD"} | "{exact quote}" |

### Totals
- Pain count: {n}
- Quantified pains: {n with dollar estimates}
- Total quantified pain: ${sum}
- Pain-to-price ratio: {total / annual product price}x

### Urgency Signals
- {any quotes about timeline or urgency}

### Gaps to Explore Next
- {areas not covered, surface-level pains needing deeper probe}
```

### 6. Evaluate against threshold

Run the `threshold-engine` drill to evaluate your results. The threshold engine checks:
- Did you complete >= 3 discovery calls?
- Did each call surface >= 3 quantified pain points?
- Does total quantified pain per prospect exceed 5x product cost?

If **PASS**: You have validated that structured pain discovery consistently surfaces quantifiable pain. Proceed to Baseline to automate transcription and extraction.

If **FAIL**: Diagnose why. Common causes:
- **Low pain count:** Your questions are too surface-level. Add more "tell me more" follow-ups.
- **Low quantification:** Prospects described pain but didn't give numbers. Add more "what does that cost you" probes.
- **Low pain-to-price ratio:** The prospects may not be ICP-fit, or the pains are real but small. Tighten your ICP.

Re-run the Smoke test with adjustments.

## Time Estimate

- Call prep (3 calls x 45 min): 2.25 hours
- Discovery calls (3 x 45 min): 2.25 hours
- Post-call logging (3 x 30 min): 1.5 hours
- Threshold evaluation: 1 hour
- **Total: ~7 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — store deal records, pain data, call notes | Free tier (up to 3 users); Plus $29/user/mo |
| Cal.com | Schedule discovery calls | Free tier (1 user); Teams $15/user/mo |
| Clay | Prospect enrichment for call prep | Free tier (100 credits); Launch $185/mo |
| Fireflies | Record and transcribe calls | Free (800 min/mo); Pro $10/user/mo (annual) |
| PostHog | Track discovery metrics | Free tier (1M events/mo) |
| Claude API | Generate pain hypotheses for call prep | Sonnet: $3/$15 per M input/output tokens |

**Estimated play-specific cost at Smoke:** Free (all tools have free tiers sufficient for 3 calls)

## Drills Referenced

- `pain-discovery-call-prep` — Research the prospect, generate tailored pain questions, verify recording
- `threshold-engine` — Evaluate results against pass/fail criteria
