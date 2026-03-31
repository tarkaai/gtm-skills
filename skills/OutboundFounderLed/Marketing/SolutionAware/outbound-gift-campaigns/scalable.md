---
name: outbound-gift-campaigns-scalable
description: >
  Outbound Gift Campaigns — Scalable Automation. Scale to 150 gifts per quarter with
  signal-triggered sending, AI-optimized gift selection, and structured A/B testing.
  Find the 10x multiplier through targeting precision and gift-type optimization.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Direct"
level: "Scalable Automation"
time: "40 hours over 3 months"
outcome: "≥ 20% response rate sustained at 150 gifts/quarter with cost per meeting ≤ $75"
kpis: ["Response rate", "Cost per meeting", "Pipeline generated", "A/B test win rate", "Meetings booked per month"]
slug: "outbound-gift-campaigns"
install: "npx gtm-skills add OutboundFounderLed/Marketing/SolutionAware/outbound-gift-campaigns"
drills:
  - gift-campaign-send
  - gift-ab-testing
  - signal-detection
  - enrich-and-score
---

# Outbound Gift Campaigns — Scalable Automation

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Direct

## Outcomes

Scale gift outreach from 50/month to 150/quarter (50/month sustained) without proportional effort increase, while introducing structured experimentation to find the optimal gift type, value, and personalization for each prospect segment. The 10x multiplier comes from three levers: (1) signal-triggered sending that targets only the highest-intent prospects, (2) AI gift selection that matches the right gift to the right person, and (3) A/B testing that continuously improves response rates.

At Scalable, the agent handles prospect sourcing, gift selection, sending, follow-up, and tracking autonomously. Human effort drops to reviewing weekly A/B test results and approving experiment designs.

## Leading Indicators

- Automated prospect pipeline producing 50+ qualified, signal-detected contacts per month from Clay
- Signal-triggered sends producing higher response rates than batch sends
- A/B tests producing at least 1 winning variant per quarter
- Cost per meeting trending down as gift selection improves
- No manual intervention needed for weekly gift sends (fully automated via n8n)

## Instructions

### 1. Automate prospect sourcing with signal detection

Run the `signal-detection` drill to configure Clay to automatically surface prospects showing buying signals relevant to your gift campaign:

- **Job changes:** New VP/Director/Head of {{buyer_persona}} in the last 90 days — they arrive with fresh budget, no vendor relationships, and a strong desire to make an impact in their new role. A thoughtful welcome gift is memorable.
- **Funding events:** Series A/B/C closed in last 90 days — celebration context makes a gift feel natural rather than transactional.
- **Hiring signals:** 3+ open roles in your product's domain — building a team signals budget and urgency.
- **Competitor signals:** Using a competing product and showing signs of dissatisfaction (support complaints, review site posts) — displacement opportunity where a gift differentiates you.
- **Content engagement:** Prospect engaged with your content (webinar attendee, whitepaper download, blog commenter) — already aware of you, a gift accelerates the relationship.

For each signal, Clay should:
1. Detect the signal via automated enrichment (weekly schedule)
2. Enrich the contact with email, LinkedIn, company data, and optionally mailing address
3. Push qualified contacts to Attio tagged with the signal type and `ready_for_gift_campaign`

Run the `enrich-and-score` drill to score each prospect. Priority for gifts: contacts with high firmographic fit + a recent signal + solution awareness. Only send gifts to prospects scoring 70+ on your ICP fit model.

### 2. Build automated weekly gift send workflow

In n8n, create a workflow that runs weekly:

1. Query Attio for all contacts tagged `ready_for_gift_campaign` that have not yet received a gift
2. Cap at 12-15 per week (to maintain personalization quality and spread follow-up workload)
3. For each contact, call the `gift-campaign-send` drill:
   a. Run AI gift selection with the prospect's enrichment data
   b. Map the selection to the gifting platform catalog
   c. Send the gift
   d. Log in Attio and PostHog
4. Trigger the follow-up automation (built in Baseline) for each sent gift
5. Generate a weekly send summary and post to Slack

The AI gift selection at Scalable level should be fully autonomous for contacts with confidence ≥ 0.7. Route low-confidence selections (< 0.7) to a Slack approval queue.

### 3. Run structured A/B tests

Run the `gift-ab-testing` drill. At Scalable volume (50/month), plan one test per month:

**Month 1 — Test gift type:**
- Control: $25 eGift card (recipient's choice via Tremendous)
- Treatment: $25 business book selected by AI based on prospect's role and signal

Split weekly sends 50/50. Measure response rate and cost per meeting over 30 days post-delivery.

**Month 2 — Test gift value:**
- Control: $25 eGift card
- Treatment: $50 eGift card

Does doubling the gift value produce a proportional increase in response rate? If $50 gifts produce 2x the meetings, they are equally cost-effective. If less than 2x, $25 is more efficient.

**Month 3 — Test personalization depth:**
- Control: Signal-personalized note ("Congrats on joining {{company}} as {{title}}")
- Treatment: Deep-research note that references a specific LinkedIn post, podcast appearance, or company initiative

Measure whether the deeper personalization justifies the extra enrichment cost and effort.

**Ongoing test cadence:** One new test per month. Only test one variable at a time. Each test needs ≥ 25 sends per variant over the test period. After each test:
- If treatment wins with statistical significance: adopt as the new default
- If no significant difference: keep the simpler/cheaper variant
- Document every test result in Attio and PostHog

### 4. Segment by signal type

Different buying signals warrant different gift strategies:

| Signal | Gift Strategy | Note Angle |
|--------|--------------|------------|
| Job change | Welcome gift — book or gourmet item | "Welcome to {{company}}. Thought this might help as you get started." |
| Funding | Celebration gift — premium eGift or curated box | "Congrats on the raise. Here's to building something great." |
| Hiring | Practical gift — Amazon/office eGift | "Building a {{function}} team? This might come in handy." |
| Competitor user | Differentiation gift — book on the category + a bold note | "You're using {{competitor}}. Here's a different perspective on solving {{problem}}." |
| Content engaged | Deepening gift — related resource or experience | "You attended our {{webinar}}. Thought you'd find this valuable too." |

Configure the AI gift selection prompt to weight these strategies based on the signal type.

### 5. Track unit economics and optimize

Track these metrics weekly in PostHog:

| Metric | Target | Calculation |
|--------|--------|-------------|
| Response rate | ≥ 20% | (all responses within 30 days) / gifts delivered |
| Cost per response | ≤ $75 | total gift spend / total responses |
| Cost per meeting | ≤ $75 | total gift spend / meetings booked |
| Pipeline per gift dollar | ≥ $5 | pipeline generated / total gift spend |
| Signal-triggered response rate | ≥ 25% | responses from signal-triggered sends / signal-triggered sends |
| AI selection acceptance rate | ≥ 85% | AI selections approved without override / total selections |

Scale volume only when metrics hold. If response rate drops below 15% as you increase volume, you are outrunning your qualified prospect pool — tighten ICP scoring.

**Pass threshold:** ≥ 20% response rate sustained at 150 gifts/quarter with cost per meeting ≤ $75.

If PASS: Proceed to Durable for autonomous optimization.
If FAIL: Diagnose by segment — which signal types are underperforming? Which gift types are failing? Which seniority levels are not responding? Fix the weakest segment and re-run.

## Time Estimate

- 8 hours: Signal detection and automated sourcing setup in Clay (one-time)
- 4 hours: Automated weekly send workflow in n8n (one-time)
- 4 hours: A/B test design and execution per test cycle (12 hours over 3 months)
- 2 hours/week: Monitor metrics, review test results, approve low-confidence selections (24 hours over 3 months)
- Total: ~40 hours over 3 months (12 hours one-time + 28 hours ongoing)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Tremendous | Send eGift cards (no platform fee) | Free — pay only gift face value. https://www.tremendous.com/pricing |
| Sendoso | Send physical gifts (alternative) | From ~$20,000/yr platform + per-send. https://www.sendoso.com/compare-plans |
| Clay | Signal detection, enrichment, scoring | From $149/mo (Explorer) to $349/mo (Pro). https://www.clay.com/pricing |
| Attio | CRM — contacts, campaigns, experiment logs | Free for small teams, Pro from $29/seat/mo. https://attio.com/pricing |
| PostHog | Event tracking, experiment analysis, dashboards | Free up to 1M events/mo. https://posthog.com/pricing |
| n8n | Automated weekly sends, webhook processing | Free (self-hosted) or from $24/mo. https://n8n.io/pricing |
| Instantly | Follow-up email sequences | From $30/mo. https://instantly.ai/pricing |
| Anthropic API | AI gift selection at scale | ~$1.50/mo for 50 selections. https://www.anthropic.com/pricing |

**Estimated total monthly cost at 50 gifts/month (eGift path):**
- Gifts: 50 x $25-50 = $1,250-$2,500
- Tools: ~$250/mo
- **Total: ~$1,500-$2,750/mo**

**Estimated total quarterly cost at 150 gifts/quarter:**
- Gifts: $3,750-$7,500
- Tools: ~$750
- **Total: ~$4,500-$8,250/quarter**

## Drills Referenced

- `gift-campaign-send` — Automated weekly AI-powered gift selection, sending, and CRM logging
- `gift-ab-testing` — Structured A/B tests on gift type, value, personalization, and timing
- `signal-detection` — Automated buying signal detection for priority targeting
- `enrich-and-score` — Score and prioritize prospects for gift outreach
