---
name: intent-signal-tracking-scalable
description: >
  Intent Signal Tracking — Scalable Automation. Build real-time signal-to-outreach orchestration
  that automatically triggers personalized multi-channel sequences when intent scores cross
  thresholds. Add third-party intent sources, AI personalization, and A/B testing to scale
  volume 10x without proportional effort.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=200 high-intent accounts/month identified and >=3x conversion rate vs cold outreach over 2 months"
kpis: ["Intent accounts identified per month", "Median signal-to-outreach time", "Conversion rate by intent tier", "Intent score decay rate"]
slug: "intent-signal-tracking"
install: "npx gtm-skills add sales/qualified/intent-signal-tracking"
drills:
  - ab-test-orchestrator
  - follow-up-automation
---

# Intent Signal Tracking — Scalable Automation

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Outcomes

Build the 10x multiplier: real-time orchestration that automatically triggers personalized outreach within minutes of a Hot-tier signal, without manual intervention. Add third-party intent data (G2, Bombora), AI-generated personalization, and systematic A/B testing. Process >=200 high-intent accounts per month while maintaining >=3x conversion advantage over cold outreach.

## Leading Indicators

- Hot-tier accounts receive outreach within 30 minutes of signal detection (median)
- At least 3 signal sources are feeding the scoring model (website visitors + G2 + enrichment signals)
- AI personalization is generating unique first lines for each Hot-tier contact
- A/B tests are running with sufficient volume to reach statistical significance within 2 weeks
- Monthly intent account volume is trending up without proportional effort increase

## Instructions

### 1. Deploy real-time intent orchestration

Run the the intent orchestration workflow (see instructions below) drill to build the full automation pipeline:

- **Hot-tier instant outreach**: n8n workflow triggered by Attio webhook when any account crosses into Hot tier. The workflow retrieves the account's signals, generates personalized copy via Clay Claygent, adds the contact to the Hot-tier Instantly sequence, logs the action in PostHog, and notifies the founder via Slack. Target: signal to email in under 30 minutes.

- **Warm-tier daily batch**: n8n cron workflow at 9am that pulls all new Warm-tier accounts, generates batch personalizations, and adds to the Warm-tier sequence. Maximum 20 per day.

- **Score-change modifier**: n8n workflow that moves contacts between sequences when their intent score changes tier (e.g., Warm account that visits pricing page gets upgraded to Hot sequence immediately).

- **Reply routing**: n8n workflow that classifies Instantly replies by sentiment and routes positive replies to Attio deals, neutral replies to manual follow-up tasks, and negative replies to opt-out.

### 2. Add third-party intent sources

Expand beyond website visitors to third-party intent:

- **G2 Buyer Intent**: If you have a G2 paid profile, configure the G2 intent webhook to feed signals into your n8n pipeline. G2 signals for "alternatives" and "compare" pages are highest value — weight them at 20 points in your scoring model.

- **Bombora Company Surge** (if budget allows): At ~$30K/year, Bombora is only justified at Scalable level when monthly deal value exceeds $5K ACV. Configure the Bombora API to pull weekly surge reports for your top 10 topics. Feed surge scores into Clay for scoring.

- **Clay enrichment signals**: Expand your weekly enrichment refresh to check for: new funding rounds (Crunchbase via Clay), executive job changes (LinkedIn via Clay), competitor technology adoption (BuiltWith via Clay), and hiring velocity in your product domain.

Each new source feeds into the same Clay scoring table and the same n8n routing logic.

### 3. Launch A/B testing program

Run the `ab-test-orchestrator` drill to set up systematic experiments:

**Test 1 — AI personalization vs static templates** (weeks 1-3):
- Control: proven email templates from Baseline with static first lines
- Variant: Clay Claygent-generated personalized first lines referencing specific intent signals
- Primary metric: reply rate
- Sample size: 100+ per variant
- Expected: AI personalization improves reply rate by 3-5 percentage points

**Test 2 — Outreach timing** (weeks 3-5):
- Control: outreach within 30 minutes of signal
- Variant: outreach delayed to next business morning at 9am
- Primary metric: reply rate and meeting rate
- Test whether urgency outweighs optimal sending time

**Test 3 — Signal-specific messaging** (weeks 5-8):
- Control: generic intent-aware template
- Variant: signal-type-specific templates (different copy for pricing page visitors vs G2 researchers vs job-change signals)
- Primary metric: reply rate by signal type

Implement winning variants permanently after each test concludes.

### 4. Build multi-channel follow-up

Run the `follow-up-automation` drill to add automated follow-up triggers:

- If a Hot-tier email gets opened 3+ times with no reply, trigger a LinkedIn connection request + message via a manual task in Attio (LinkedIn automation is risky at scale — keep it semi-manual)
- If a Hot-tier contact visits your website again after receiving outreach, trigger an immediate follow-up email referencing the topic of the page they visited
- If a meeting is booked from intent outreach, trigger a pre-meeting research brief (pull company news, recent signals, LinkedIn activity)

### 5. Scale volume and monitor

Increase monthly throughput to 200+ intent accounts by:
- Upgrading RB2B to Pro+ ($149/mo) for higher identification volume
- Expanding target account list in Clay to 500+ companies
- Adding additional sending accounts in Instantly to support volume (stay under 50 emails/day per account)

Monitor the scoring model weekly: as volume increases, does Hot-tier still convert at 3x+ vs Cold? If the ratio drops below 2x, the model is degrading — tighten thresholds or adjust weights.

### 6. Evaluate against threshold

After 2 months, measure:
- Total high-intent accounts identified per month: target >=200
- Hot-tier conversion rate vs cold outreach conversion rate: target >=3x
- Median signal-to-outreach time for Hot accounts: target <30 minutes
- A/B test win rate: at least 1 of 3 tests produced a statistically significant improvement

If PASS, proceed to Durable. If FAIL, identify the bottleneck: insufficient signal volume, scoring accuracy degradation, or outreach copy fatigue.

## Time Estimate

- 12 hours: build intent orchestration workflows (Hot-tier, Warm-tier, score-change, reply routing)
- 6 hours: configure third-party intent sources (G2, optionally Bombora)
- 8 hours: set up A/B testing infrastructure and launch first test
- 6 hours: build multi-channel follow-up automation
- 16 hours: weekly monitoring and optimization over 8 weeks (2 hr/week)
- 12 hours: A/B test analysis, implementation, and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| RB2B Pro+ | Website visitor identification (scaled) | $149/mo |
| Clay Explorer | Intent scoring + AI enrichment | $149-349/mo |
| Instantly Growth | Email sequencing at scale | $77/mo (5,000 contacts) |
| PostHog | Analytics, funnels, A/B testing | Free tier or Scale $0+ |
| Attio | CRM and deal pipeline | Pro $29/user/mo |
| n8n | Workflow automation (4+ workflows) | Starter $24/mo or Pro $60/mo |
| G2 Buyer Intent | Third-party intent signals | Included in G2 paid profile |
| Bombora (optional) | Topic-level intent data | ~$30K/yr (only if ACV justifies) |

**Total play-specific cost: ~$200-500/mo** (excluding optional Bombora)

## Drills Referenced

- the intent orchestration workflow (see instructions below) — real-time signal-to-outreach pipeline with AI personalization
- `ab-test-orchestrator` — systematic A/B testing on personalization, timing, and messaging
- `follow-up-automation` — multi-channel follow-up triggered by engagement signals
