---
name: pain-discovery-framework-baseline
description: >
  Pain Discovery Framework — Baseline Run. Automate transcript-to-pain extraction
  with AI. Run always-on after every discovery call: transcribe, extract pains, quantify
  in dollars, log to CRM, and route deals by pain quality.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: ">=70% of prospects with >=4 quantified pains totaling >=10x product cost over 2 weeks"
kpis: ["Quantified pain per prospect", "Pain-to-price ratio", "Pain validation rate", "Business case conversion rate"]
slug: "pain-discovery-framework"
install: "npx gtm-skills add sales/connected/pain-discovery-framework"
drills:
  - pain-discovery-call
  - posthog-gtm-events
---

# Pain Discovery Framework — Baseline Run

> **Stage:** Sales > Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

Automate the post-call pain extraction pipeline so every discovery call automatically produces structured pain data in your CRM. Achieve >= 70% of prospects with >= 4 quantified pains totaling >= 10x product cost. This proves the automation works reliably before scaling volume.

## Leading Indicators

- Fireflies transcripts processing within 15 minutes of call end
- Pain extraction completing automatically for >= 90% of calls
- Average pain count per call trending upward from Smoke baseline
- Pain quantification accuracy validated by caller review (>= 80% agreement)
- Deals with pain data progressing faster through pipeline than deals without

## Instructions

### 1. Set up the automated extraction pipeline

Configure the always-on pipeline that fires after every discovery call:

**Fireflies webhook setup:**
Create an n8n workflow triggered by Fireflies transcript completion. When a new transcript is available:
1. Match the transcript to a deal in Attio by meeting attendee email or calendar event
2. Verify the transcript has >= 200 words of prospect speech
3. If matched and valid, trigger the `pain-discovery-call` drill

**Human action required:** Test the webhook end-to-end with a real call before going live. Verify: Fireflies captures the transcript, the webhook fires, the drill runs, and pain data appears in Attio.

### 2. Configure PostHog event tracking

Run the `posthog-gtm-events` drill to set up the event taxonomy for pain discovery. Configure these events:

- `pain_discovery_call_scheduled` — fires when a Cal.com booking is created for a discovery call
- `pain_discovery_call_completed` — fires after pain extraction, includes: pain_count, total_quantified_pain, pain_to_price_ratio, quantification_rate, discovery_depth_score
- `pain_extraction_completed` — fires for each individual pain extracted, includes: category, severity, estimated_annual_cost, confidence
- `business_case_generated` — fires when a business case is auto-generated from pain data

Set up a PostHog funnel: `call_scheduled` -> `call_completed` -> `pain_extraction_completed` -> `business_case_generated` -> `deal_advanced`

### 3. Validate extraction accuracy

For the first 5 calls, manually review the AI-extracted pain data against your own notes:

For each call, compare:
- Did the AI find all the pains you heard? (Recall)
- Are the AI-identified pains real, not hallucinated? (Precision)
- Are the dollar estimates reasonable? (Accuracy)
- Are the supporting quotes actual transcript text? (Fidelity)

Calculate:
- **Recall:** Pains you noted that the AI also found / total pains you noted
- **Precision:** AI pains that are real / total AI-extracted pains
- **Accuracy:** Estimates within 50% of your manual estimate / total estimates

Target: Recall >= 0.8, Precision >= 0.9, Accuracy >= 0.7.

If below target, adjust the extraction prompt in `call-transcript-pain-extraction`. Common fixes:
- Low recall: Add industry-specific pain vocabulary to the prompt
- Low precision: Tighten the confidence threshold (reject pains below 0.6)
- Low accuracy: Add more enrichment data to the quantification context

### 4. Run 10+ discovery calls over 2 weeks

**Human action required:** Continue conducting discovery calls. The call prep and post-call extraction are now automated. Your job:

- Review the auto-generated call prep before each call
- Conduct the discovery call following the Smoke test rules
- After the call, review the auto-extracted pain data within 24 hours
- Correct any errors (edit pain records in Attio) — this improves future extraction

### 5. Set up CRM pain views

Configure Attio views for pipeline management:

- **"High-Pain Prospects"** list: filter deals where pain_to_price_ratio >= 10x
- **"Needs Deeper Discovery"** list: filter deals where quantification_rate < 0.5
- **"Business Case Ready"** list: filter deals where pain_count >= 4 AND quantification_rate >= 0.7
- Sort all deal views by total_quantified_pain descending — your highest-pain prospects get attention first

### 6. Evaluate against threshold

After 2 weeks, measure:
- What percentage of prospects have >= 4 quantified pains?
- What percentage have total pain >= 10x product cost?
- What is the average pain-to-price ratio?
- How many business cases were generated?

If **PASS** (>= 70% of prospects meet criteria): The automated pipeline is working. Proceed to Scalable to find cross-prospect patterns and scale question optimization.

If **FAIL**: Diagnose:
- **Low pain count per call:** Improve call prep hypotheses or add follow-up call workflow
- **Low quantification:** Improve the quantification prompt or add more enrichment data
- **Low pain-to-price:** Tighten ICP or revisit pricing

## Time Estimate

- Pipeline setup and testing: 4 hours
- PostHog event configuration: 2 hours
- Validation of first 5 calls (review + correction): 3 hours
- 10 discovery calls (45 min each): 7.5 hours
- CRM view configuration: 1.5 hours
- Threshold evaluation: 2 hours
- **Total: ~20 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, pain data, pipeline views | Plus $29/user/mo |
| Fireflies | Auto-transcribe discovery calls | Pro $10/user/mo (annual); Business $19/user/mo |
| Claude API (Anthropic) | Pain extraction + quantification | Sonnet: $3/$15 per M tokens; ~$0.10-0.30 per call |
| PostHog | Event tracking, funnels, analytics | Free tier (1M events/mo) |
| n8n | Webhook automation (Fireflies -> extraction -> CRM) | Starter $24/mo; Pro $60/mo |
| Cal.com | Discovery call scheduling | Free (1 user); Teams $15/user/mo |
| Clay | Prospect enrichment for call prep | Launch $185/mo |

**Estimated play-specific cost at Baseline:** ~$50-100/mo (Fireflies Pro + n8n Starter + Claude API usage). CRM, PostHog, Cal.com on free tiers for small teams.

## Drills Referenced

- `pain-discovery-call` — Full post-call lifecycle: transcribe, extract pains, quantify, score, log to CRM
- `posthog-gtm-events` — Define and implement the event taxonomy for pain discovery tracking
