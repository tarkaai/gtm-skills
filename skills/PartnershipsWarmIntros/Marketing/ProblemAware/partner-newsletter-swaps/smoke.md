---
name: partner-newsletter-swaps-smoke
description: >
  Partner Newsletter Swaps — Smoke Test. Exchange dedicated emails with one complementary
  company's newsletter to prove that list swaps generate subscriber growth and qualified
  leads from a problem-aware audience.
stage: "Marketing > ProblemAware"
motion: "PartnershipsWarmIntros"
channels: "Email"
level: "Smoke Test"
time: "8 hours over 2 weeks"
outcome: ">=1 completed list swap and >=50 new subscribers with >=2 leads in 3 weeks"
kpis: ["Partner response rate", "Swap click-through rate", "New subscribers from swap", "Leads generated"]
slug: "partner-newsletter-swaps"
install: "npx gtm-skills add PartnershipsWarmIntros/Marketing/ProblemAware/partner-newsletter-swaps"
drills:
  - partner-prospect-research
  - list-swap-email-copy
  - threshold-engine
---
# Partner Newsletter Swaps — Smoke Test

> **Stage:** Marketing > ProblemAware | **Motion:** PartnershipsWarmIntros | **Channels:** Email

## Outcomes
- Complete at least 1 full list swap (you send their email to your list, they send yours to theirs)
- Generate >=50 new subscribers from the partner's list
- Generate >=2 leads (meeting booked or signup) from swap-sourced traffic
- Prove that a complementary company's audience responds to your value proposition

## Leading Indicators
- Partner accepts the swap proposal within 5 business days of outreach
- Partner's newsletter score >=14/20 from audit (audience overlap, size, engagement, co-marketing friendliness)
- Swap email variant click-through rate >=2% on the partner's send
- Landing page visitors from swap UTMs show >=30-second average session duration in PostHog

## Instructions

### 1. Research and qualify 10 partner candidates

Run the `partner-prospect-research` drill. Configure it with:
- **Target count:** 10 qualified partners
- **Minimum audience size:** 1,000 subscribers
- **Filter criteria:** Complementary products (not competitors), same buyer persona as your ICP, active newsletter (published within last 2 weeks)

The drill uses `clay-company-search` to source candidates, `clay-enrichment-waterfall` to enrich contacts, `partner-newsletter-audit` to score each newsletter (1-5 on audience overlap, audience size, engagement quality, co-marketing friendliness), and `crossbeam-account-mapping` to find overlapping target accounts.

Output: Ranked list of 10 partners in Attio with newsletter scores, subscriber estimates, and contact info for the partnerships/marketing lead.

### 2. Select the top partner and propose the swap

From the ranked list, select the partner with the highest newsletter score. Verify:
- Their newsletter published in the last 7 days (active)
- They already feature partner content or recommendations (co-marketing friendly)
- You have a mutual connection or warm path to the contact

**Human action required:** Send a personalized outreach message to the top partner proposing a list swap. Include: what your newsletter covers, your subscriber count, why the audiences are complementary, and a specific proposed timeline (swap emails within 2 weeks). Use a warm intro if available. Log the outreach in Attio with status "Proposed".

If no response within 5 business days, move to the next partner on the list.

### 3. Write and exchange swap emails

Once a partner agrees, run the `list-swap-email-copy` drill. This drill:
1. Sets up PostHog tracking for swap UTM parameters (`utm_source={partner_slug}&utm_medium=list-swap&utm_campaign=list-swaps-adjacent-startups&utm_content={variant_id}`)
2. Generates 3 email variants (curiosity, data-driven, story-driven) using `list-swap-email-authoring`
3. Selects the best variant matching the partner's tone and audience
4. Delivers the email to the partner with tracked CTA link and assets
5. Coordinates the reciprocal email (partner sends their email to you for your list)
6. Schedules simultaneous send (both emails go out same week)
7. Monitors results for 7 days post-send

**Human action required:** Review and approve both emails before send. Verify the partner's email to your list is relevant and not harmful to your subscriber relationship. Reject and request revision if quality is insufficient.

### 4. Monitor swap performance for 7 days

After both emails send, monitor daily in PostHog:
- `pageview` events where `utm_medium = list-swap` (traffic from partner's send)
- `list_swap_click` events (CTA conversions on your landing page)
- `list_swap_meeting_booked` events (leads generated)
- New subscriber count in your email tool (Loops audience growth)

Also track reciprocal performance: how did your list respond to the partner's email? Log opens, clicks, and unsubscribes. This reciprocity data determines whether the partner will want to swap again.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure:
- **>=1 completed list swap:** Both emails sent on time, both parties honored commitment
- **>=50 new subscribers:** Unique new subscribers acquired from swap traffic
- **>=2 leads:** Meetings booked or signups from swap-sourced visitors

If PASS: The channel works. Your value proposition resonates with this partner's audience. Proceed to Baseline to systematize across multiple partners.

If FAIL but close (e.g., 30+ subscribers, 1 lead): Analyze which email variant performed best, whether the partner's audience truly matched your ICP, and whether the landing page converted. Try one more swap with a different partner before abandoning.

If FAIL completely (<10 subscribers, 0 leads): The audience overlap may be insufficient, or the email copy missed the mark. Review the partner's newsletter audit score. If score was low, try a higher-scoring partner. If score was high but results were poor, revisit your value proposition for this audience segment.

---

## Time Estimate
- Partner research and qualification: 3 hours
- Outreach and negotiation: 1 hour (plus wait time)
- Email writing and coordination: 2 hours
- Monitoring and evaluation: 2 hours

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Partner research and enrichment | Free tier: 100 credits/mo. Pro: $149/mo (https://www.clay.com/pricing) |
| Attio | CRM for partner tracking | Free tier: 3 users. Plus: $34/user/mo (https://attio.com/pricing) |
| PostHog | Swap traffic tracking and analytics | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Loops | Send reciprocal email to your list | Free tier: 1,000 contacts (https://loops.so/pricing) |
| Crossbeam | Account overlap mapping | Free tier available (https://www.crossbeam.com/pricing) |

**Estimated play-specific cost:** Free (all tools within free tier at smoke scale)

## Drills Referenced
- `partner-prospect-research` — find, audit, and rank newsletter partners by audience fit
- `list-swap-email-copy` — write, track, and coordinate the swap email exchange
- `threshold-engine` — evaluate results against pass/fail criteria
