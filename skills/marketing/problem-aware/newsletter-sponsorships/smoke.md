---
name: newsletter-sponsorships-smoke
description: >
  Newsletter Sponsorship — Smoke Test. Book one paid blurb in one niche industry
  newsletter to test whether the audience generates clicks and at least one lead
  before committing recurring sponsorship budget.
stage: "Marketing > Problem Aware"
motion: "LightweightPaid"
channels: "Email"
level: "Smoke Test"
time: "4 hours over 2 weeks"
outcome: "≥ 20 clicks and ≥ 1 lead from a single paid newsletter placement"
kpis: ["Clicks from placement", "Leads from placement", "CPC", "CPL"]
slug: "newsletter-sponsorships"
install: "npx gtm-skills add marketing/problem-aware/newsletter-sponsorships"
drills:
  - newsletter-sponsor-research
  - newsletter-sponsor-booking
  - threshold-engine
---

# Newsletter Sponsorship — Smoke Test

> **Stage:** Marketing → Problem Aware | **Motion:** LightweightPaid | **Channels:** Email

## Outcomes

One paid sponsorship blurb placed in one niche industry newsletter. At least 20 clicks to your landing page and at least 1 lead (signup, demo request, or form submission) within 7 days of the newsletter send. This proves that paying for newsletter audience access produces measurable signal before you invest in a multi-newsletter sponsorship program.

## Leading Indicators

- Newsletter publisher responds to your inquiry within 5 business days (signal: their ad program is active and responsive)
- Placement cost is within $100-500 range for a niche B2B newsletter (signal: pricing is accessible for testing)
- Clicks arrive within 24 hours of newsletter send (signal: the audience is engaged and reads the newsletter promptly)
- Click-through rate on the blurb exceeds 0.5% of estimated newsletter audience (signal: copy and audience alignment is viable)

## Instructions

### 1. Research and select one newsletter to sponsor

Run the `newsletter-sponsor-research` drill with reduced scope: search newsletter advertising marketplaces (Paved, Beehiiv Ad Network, Letterhead) for 10 candidate newsletters in your ICP's industry vertical. Score each on audience overlap, size, engagement quality, and pricing efficiency.

Select the single best newsletter based on the highest ICP density score relative to cost. Prioritize newsletters with:
- 2,000-20,000 subscribers (large enough for signal, small enough for affordable testing)
- Published open rates above 30%
- Existing sponsor program (they already run ads, so the process is smooth)
- Placement cost of $100-500

### 2. Book the placement

Run the `newsletter-sponsor-booking` drill for your selected newsletter:

- Request the media kit and confirm pricing
- If the listed rate exceeds $500, negotiate a one-time test placement at a reduced rate
- Book a single placement in an upcoming issue
- Set up UTM tracking: `{landing_page}?utm_source={newsletter_slug}&utm_medium=paid-newsletter&utm_campaign=newsletter-sponsorships&utm_content={newsletter_slug}-smoke-v1`
- Write 3 blurb variants, select the best fit for the newsletter's tone
- Submit creative by the publisher's deadline

**Human action required:** Approve the placement cost and process payment. Review the blurb before submission to the publisher.

### 3. Prepare your landing page

Ensure the landing page receiving newsletter traffic:
- Has one clear CTA (demo request, free trial, or resource download)
- Loads in under 3 seconds on mobile (newsletter readers predominantly open on phones)
- Has PostHog tracking installed capturing `$pageview` with UTM parameters and `newsletter_sponsor_lead` on CTA completion
- Matches the promise made in the newsletter blurb (headline and CTA should be consistent)

### 4. Monitor results on send day

On the day the newsletter sends:
- Confirm with the publisher that the issue was sent
- Watch PostHog for incoming `$pageview` events where `utm_source` matches your newsletter
- Note click velocity: a burst within the first 2-4 hours indicates an engaged readership
- Monitor for `newsletter_sponsor_lead` events

### 5. Evaluate against threshold

Run the `threshold-engine` drill 7 days after the newsletter send. Measure:
- Total clicks: pageviews from this `utm_content` tag
- Total leads: `newsletter_sponsor_lead` events from this `utm_source`
- CPC: placement cost / total clicks
- CPL: placement cost / total leads

**Pass threshold: >= 20 clicks AND >= 1 lead**

- **Pass**: Document which newsletter, what blurb angle, and what CPC/CPL you achieved. Proceed to Baseline.
- **Marginal**: 10-19 clicks or 0 leads but strong click engagement. Test one more newsletter before deciding.
- **Fail**: <10 clicks. Diagnose: Was the newsletter audience wrong for your ICP? Was the blurb too generic? Was the newsletter too small? Try a different newsletter with better ICP alignment.

## Time Estimate

- Newsletter research and selection: 1.5 hours
- Booking and negotiation: 30 minutes (plus wait time for publisher response)
- Blurb writing and landing page prep: 1 hour
- Monitoring and evaluation: 1 hour (spread over 7 days)

Total: ~4 hours of active work over 2 weeks (including publisher response time and the 7-day measurement window)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Paved | Newsletter marketplace discovery | Free for advertisers ([paved.com](https://www.paved.com)) |
| Clay | Publisher research and enrichment | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Attio | CRM tracking for placements | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Click and lead tracking | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Anthropic Claude | Blurb copywriting | Pay-per-use, ~$0.10-0.50 per blurb ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Newsletter placement | Paid sponsorship | $100-500 for a single niche placement |

**Estimated cost for this level: $100-500** (the newsletter placement itself; all tools within free tiers)

## Drills Referenced

- `newsletter-sponsor-research` — find and rank newsletters for paid sponsorship based on ICP overlap and cost-efficiency
- `newsletter-sponsor-booking` — negotiate, book, write creative, set up tracking, and collect results for one placement
- `threshold-engine` — evaluate clicks and leads against the pass threshold
