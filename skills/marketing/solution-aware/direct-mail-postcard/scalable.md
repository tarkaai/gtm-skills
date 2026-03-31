---
name: direct-mail-postcard-scalable
description: >
  Direct Mail Postcards — Scalable Automation. Scale to 500-1000 postcards/month with
  automated A/B testing, signal-triggered sending, and multi-variant optimization.
  Find the 10x multiplier through targeting precision and copy optimization.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Other"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: "≥ 5% response rate sustained at 500-1000 postcards/month with cost per meeting ≤ $50"
kpis: ["Response rate", "Cost per meeting", "Pipeline generated", "A/B test win rate", "Meetings booked per month"]
slug: "direct-mail-postcard"
install: "npx gtm-skills add marketing/solution-aware/direct-mail-postcard"
drills:
  - postcard-campaign-send
  - postcard-ab-testing
  - signal-detection
  - enrich-and-score
---

# Direct Mail Postcards — Scalable Automation

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Other

## Outcomes

Scale direct mail from 100-200 to 500-1000 postcards per month without proportional effort increase. The 10x multiplier comes from three levers: (1) signal-triggered sending (only mail prospects showing buying signals), (2) A/B-tested copy that continuously improves, and (3) automated prospect sourcing that feeds the pipeline without manual list building.

## Leading Indicators

- Automated prospect pipeline producing 500+ verified-address contacts per month from Clay
- Signal-triggered sends producing higher response rates than batch sends
- A/B tests producing at least 1 winning variant per month
- Cost per meeting trending down over successive sends
- No manual intervention needed for weekly sends (fully automated via n8n)

## Instructions

### 1. Automate prospect sourcing with signal detection

Run the `signal-detection` drill to configure Clay to automatically surface prospects showing buying signals:

- **Job changes:** New VP/Director/Head of [your buyer persona] in the last 90 days — they arrive with fresh budget and no vendor relationships
- **Funding events:** Series A/B/C closed in last 90 days — new capital means new priorities
- **Hiring signals:** 3+ open roles in your product's domain — building a team, need tools
- **Competitor signals:** Adopted a competing product in the last 6 months — displacement opportunity

For each signal, Clay should:
1. Detect the signal via automated enrichment (daily or weekly schedule)
2. Enrich the contact with a mailing address via `clay-enrichment-waterfall`
3. Push verified contacts to Attio tagged with the signal type

Run the `enrich-and-score` drill to score each prospect. Priority for direct mail: contacts with high firmographic fit + a recent signal + a verified mailing address. Only send postcards to prospects scoring 70+.

### 2. Build automated weekly send workflow

In n8n, create a workflow that runs weekly (e.g., every Monday at 9am):

1. Query Attio for all contacts tagged `ready_for_direct_mail` that have not yet received a postcard
2. Verify all addresses via Lob's batch verification
3. Randomly assign each contact to an A/B test variant
4. Send postcards via Lob for each variant
5. Log all send data in Attio (postcard ID, variant, send date, expected delivery)
6. Fire PostHog events for each send

This workflow should handle 100-250 postcards per weekly batch without manual intervention. The digital follow-up sequence (built in Baseline) continues to run automatically.

### 3. Run structured A/B tests

Run the `postcard-ab-testing` drill. At Scalable volume (500+/month), you can run meaningful A/B tests:

**Month 1 — Test headline personalization:**
- Control: Generic industry-level headline
- Treatment: Pain-point-specific headline using data from Clay enrichment

**Month 2 — Test postcard size:**
- Control: 4x6 standard postcard ($0.77/piece)
- Treatment: 6x9 jumbo postcard (higher cost but more real estate)

**Ongoing test cadence:** One new test per send cycle (every 2-4 weeks). Only test one variable at a time. Each test needs at least 200 postcards per variant for reliable results.

After each test completes:
- If the treatment wins: update the default template and use the winner as the new control
- If no significant difference: keep the simpler/cheaper variant
- Document every test result in Attio and PostHog for the optimization history

### 4. Segment by signal type

Different buying signals deserve different postcard messaging:

- **Job change:** "Welcome to your new role. Here's how [product] helps [role] at [company size] companies hit the ground running."
- **Funding event:** "Congrats on the raise. [Product] helps [company stage] teams scale [function] without scaling headcount."
- **Hiring signal:** "Building a [function] team? [Product] gives each new hire the tools to be productive on day one."
- **Competitor user:** "[Competitor] does X. [Product] does X + Y + Z. Here's what 50 teams who switched saw."

Create a Lob template for each signal type. In the automated weekly send, assign the template based on the contact's signal tag in Attio.

### 5. Track unit economics and scale

Track these metrics weekly in PostHog:

| Metric | Target | Calculation |
|--------|--------|-------------|
| Response rate | ≥ 5% | (URL visits + meetings + replies) / postcards delivered |
| Cost per response | ≤ $20 | Total postcard cost / total responses |
| Cost per meeting | ≤ $50 | Total postcard cost / meetings booked |
| Pipeline per postcard | ≥ $10 | Total pipeline generated / postcards sent |
| Signal-triggered response rate | ≥ 8% | Responses from signal-triggered sends / signal-triggered sends |

If metrics hold as you scale from 200 to 500 to 1000/month, the channel is scalable. If response rate drops below 3% at higher volume, you are outrunning your addressable market — tighten ICP criteria.

**Pass threshold:** ≥ 5% response rate sustained at 500-1000 postcards/month with cost per meeting ≤ $50.

If PASS: Proceed to Durable for autonomous optimization.
If FAIL: Diagnose — are you sending to lower-quality prospects at scale (scoring issue)? Has messaging fatigued? Are follow-ups still running? Fix the weakest link and re-run.

## Time Estimate

- 8 hours: Signal detection and automated sourcing setup in Clay (one-time)
- 4 hours: Automated weekly send workflow in n8n (one-time)
- 4 hours: A/B test design and template creation per test cycle
- 2 hours/week: Monitor metrics, review test results, adjust (16 hours over 2 months)
- Total: ~40 hours over 2 months (16 hours one-time setup + 24 hours ongoing)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Lob | Print, mail, and track postcards at scale | $260/mo + $0.51/pc (Small Business) or $550/mo + $0.48/pc (Growth). https://www.lob.com/pricing |
| Clay | Signal detection, enrichment, address sourcing | From $149/mo (Explorer) to $349/mo (Pro). https://www.clay.com/pricing |
| Attio | CRM — contact management, campaign tracking | Free for small teams, Pro from $29/seat/mo. https://attio.com/pricing |
| PostHog | Event tracking, experiment analysis, dashboards | Free up to 1M events/mo. https://posthog.com/pricing |
| n8n | Automated weekly sends, webhook processing | Free (self-hosted) or from $24/mo (cloud). https://n8n.io/pricing |
| Instantly | Follow-up email sequences | From $30/mo. https://instantly.ai/pricing |

**Estimated total monthly cost at 500 postcards/month:**
- Lob Small Business: $260 + (500 x $0.51) = $515/mo
- Clay: ~$249/mo
- Other tools: ~$100/mo
- **Total: ~$850-$1000/mo**

## Drills Referenced

- `postcard-campaign-send` — Automated weekly batch sends via Lob API
- `postcard-ab-testing` — Structured A/B tests on copy, design, size, and targeting
- `signal-detection` — Automated buying signal detection for priority targeting
- `enrich-and-score` — Score and prioritize prospects for direct mail outreach
