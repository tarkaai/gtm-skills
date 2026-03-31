---
name: industry-reports-research-baseline
description: >
  Industry Reports & Research — Baseline Run. Produce 1-2 reports with proper event
  tracking, gated landing pages, automated email capture, and multi-channel distribution
  to validate repeatable lead generation from research content.
stage: "Marketing > ProblemAware"
motion: "FounderSocialContent"
channels: "Content, Social, Email"
level: "Baseline Run"
time: "25 hours over 4 weeks"
outcome: ">=100 downloads and >=8 qualified leads across 1-2 reports in 30 days"
kpis: ["Report downloads", "Landing page conversion rate", "Qualified leads from reports", "Social shares per report", "Download-to-lead conversion rate"]
slug: "industry-reports-research"
install: "npx gtm-skills add marketing/problem-aware/industry-reports-research"
drills:
  - industry-research-production
  - report-distribution-pipeline
  - posthog-gtm-events
  - threshold-engine
---

# Industry Reports & Research — Baseline Run

> **Stage:** Marketing > ProblemAware | **Motion:** FounderSocialContent | **Channels:** Content, Social, Email

## Outcomes

Baseline validates that report-driven lead generation is repeatable with proper infrastructure. You move from manual distribution to tracked, multi-channel distribution with event-level attribution. You also validate whether a second report topic performs similarly to the first, proving this is a motion rather than a one-off hit.

**Pass threshold:** >=100 total downloads and >=8 qualified leads (ICP-matching contacts who downloaded and either booked a meeting, replied to follow-up, or engaged in meaningful conversation) across 1-2 reports in 30 days.

## Leading Indicators

- Landing page conversion rate (visit to download) holds above 20% for gated or 40% for ungated
- First report crosses 50 downloads within 10 days of launch
- Social distribution generates at least 30% of total downloads (LinkedIn is a real channel, not just vanity)
- Email broadcast drives at least 20% of total downloads
- At least 3 qualified leads arrive in the first 2 weeks
- At least 2 backlinks from external sites within 30 days
- Organic search traffic to report pages begins within 3-4 weeks

## Instructions

### 1. Set up event tracking infrastructure

Run the `posthog-gtm-events` drill to implement the report event taxonomy in PostHog. Configure these events:

- `report_page_viewed` — properties: report_slug, source, utm_source, utm_campaign
- `report_form_started` — properties: report_slug (fires when download form receives focus)
- `report_downloaded` — properties: report_slug, email, company, title
- `report_shared` — properties: report_slug, platform
- `report_lead_qualified` — properties: report_slug, email, icp_score
- `report_meeting_booked` — properties: report_slug, lead_email, days_from_download

Build a PostHog funnel: page_viewed -> form_started -> downloaded -> lead_qualified -> meeting_booked. Break down by source to identify which distribution channels produce the highest-quality leads.

Connect n8n webhooks to sync PostHog events with Attio: when `report_downloaded` fires, create or update the contact in Attio with report attribution data. Tag the contact with `report-lead` and the specific report slug.

### 2. Produce the first report with gated access

Run the `industry-research-production` drill to produce your first report (or refine the Smoke report with additional data). At Baseline, increase rigor:

- **Data quality:** Minimum 50 survey responses or 100 enrichment data points. Include methodology section explaining sample size, collection method, and limitations.
- **Report depth:** 3,000-4,000 words with 5-8 findings. Each finding gets a chart, analysis, and actionable recommendation.
- **Gated landing page:** Build a landing page with a 2-field form (email + company name). Display the executive summary and 2 key charts ungated as a preview. The full PDF requires the form submission. Track form abandonment rate in PostHog.

**Human action required:** Founder reviews the final report for accuracy, voice, and surprise factor. The report must contain at least one finding that makes the reader say "I didn't expect that." Generic findings ("most companies plan to increase spending on X") do not generate shares or leads.

### 3. Distribute via multi-channel pipeline

Run the `report-distribution-pipeline` drill to execute the 4-week distribution calendar:

**Week 1 — Launch:**
- LinkedIn post with headline finding (founder posts personally)
- Email broadcast to subscriber list via Loops
- Blog companion post on Ghost with executive summary and embedded charts
- 2-3 community posts (relevant Slack groups, Reddit, Indie Hackers)

**Week 2 — Amplification:**
- LinkedIn carousel (top 5 findings as slides)
- Newsletter deep-dive on the most actionable finding
- Second LinkedIn post with a different finding angle

**Week 3 — Repurpose:**
- LinkedIn post with contrarian/myth-busting angle from the data
- Short-form video (founder explaining one key finding, 60-90 seconds)

**Week 4 — Long tail:**
- LinkedIn poll based on a finding
- Re-send email to non-openers with different subject line
- Roundup post quoting commenters from earlier posts

Track every distribution action: channel, date, content angle, engagement metrics, and attribution to downloads/leads.

### 4. Produce a second report (if time allows)

If the first report is launched by Week 1 and the distribution pipeline is running, use Weeks 3-4 to produce a second report on a different ICP pain point. This tests whether the motion is repeatable across topics, not just a one-off hit. Use the same data collection and production process.

### 5. Follow up with downloaders

Build a simple follow-up flow in n8n:
- **Day 3 after download:** Send a personal email from the founder: "Saw you downloaded our {report title}. Any findings surprise you? Happy to walk through how this applies to {company_name}."
- **Day 7 after download (if no reply):** Send a follow-up with one additional insight not in the report, plus a Cal.com booking link.
- Log all replies and meetings in Attio with `report-{slug}` attribution.

### 6. Evaluate against threshold

After 30 days, aggregate all data from PostHog and Attio. Run the `threshold-engine` drill to evaluate:

- Total downloads across all reports >= 100
- Qualified leads (ICP match + engagement signal) >= 8

**If PASS:** Report-driven lead gen is repeatable. Proceed to Scalable to add SEO optimization, A/B testing, and quarterly production cadence.

**If FAIL:** Diagnose:
- Downloads below 100: Distribution failed or the landing page is not converting. Check: landing page conversion rate (if below 15%, the page needs work), social engagement (if low, the hooks need work), email open rate (if low, the subject lines need work).
- Downloads above 100 but leads below 8: The report attracts readers but not buyers. The topic may be too broad, the data too generic, or the soft CTA too weak. Tighten the ICP focus, add more proprietary data, and make the CTA more specific to a pain point your product solves.
- One report worked, the second did not: The first topic was strong but the motion is not universal. Double down on the winning topic area and produce variations (e.g., same topic but different industry vertical or company size).

## Time Estimate

- PostHog event tracking setup: 3 hours
- First report production (data collection + analysis + writing): 10 hours
- Landing page and gated form setup: 2 hours
- Distribution pipeline execution (4 weeks): 6 hours
- Follow-up email sequence setup: 1.5 hours
- Monitoring and evaluation: 2.5 hours
- **Total: ~25 hours over 4 weeks** (optional second report adds ~10 hours)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Company enrichment and data collection | Launch: $185/mo — 2,500 credits ([clay.com/pricing](https://www.clay.com/pricing)) |
| Typeform / Tally | Survey for primary research | Typeform Basic: $25/mo — unlimited responses ([typeform.com/pricing](https://www.typeform.com/pricing)); Tally Free ([tally.so](https://tally.so)) |
| Ghost | Report landing page, blog, gated access | Starter: $9/mo ([ghost.org/pricing](https://ghost.org/pricing/)) |
| Loops | Email broadcasts to subscriber list | Free: 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| PostHog | Event tracking, funnels, attribution | Free: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Automation (PostHog->Attio sync, follow-ups) | Starter: ~$24/mo — 2,500 executions ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | CRM, lead tracking, report attribution | Plus: $29/user/mo ([attio.com](https://attio.com)) |
| Anthropic API | Report analysis and draft generation | ~$0.50-2.00 per report ([anthropic.com](https://www.anthropic.com)) |

**Estimated monthly cost: ~$250-280/mo** (Clay Launch + Ghost Starter + n8n Starter + Attio Plus)

## Drills Referenced

- `industry-research-production` — produce the report from data collection through publication
- `report-distribution-pipeline` — multi-channel distribution over 4 weeks
- `posthog-gtm-events` — set up the event taxonomy for report funnel tracking
- `threshold-engine` — evaluate results against the pass threshold
