---
name: public-sharing-scalable
description: >
  Branded Public Sharing — Scalable Automation. Deploy share surfaces at every
  high-intent product moment, run systematic A/B tests on share page design
  and CTA variants, and scale to 500+ active sharers.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Social"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=30% share rate at 500+ active users AND >=5% viewer-to-signup conversion maintained"
kpis: ["Public share rate at scale", "Share page views per share", "CTA click-through rate", "Viewer-to-signup conversion", "Viral coefficient", "Share-acquired user activation rate"]
slug: "public-sharing"
install: "npx gtm-skills add product/referrals/public-sharing"
drills:
  - referral-channel-scaling
  - ab-test-orchestrator
---

# Branded Public Sharing — Scalable Automation

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Social

## Outcomes

Public sharing runs at scale: 500+ users actively sharing, with a share rate of 30% or higher across the full user base. Viewer-to-signup conversion holds at 5% or higher. Multiple share surfaces are deployed across the product, each instrumented and measurable independently. The 10x multiplier: instead of one "share publicly" button, every product output is a potential share surface.

## Leading Indicators

- Share surfaces deployed at 3+ product moments (not just one button)
- Each share surface has a measurable share rate and conversion rate in PostHog
- A/B tests running continuously with 1-2 experiments active per 2-week cycle
- Viral coefficient above 0.2 (some share-acquired users are creating their own shares)
- Share-acquired user activation rate within 80% of organic user activation rate

## Instructions

### 1. Deploy share surfaces across the product

Run the `referral-channel-scaling` drill adapted for public sharing:

**In-product share surfaces** — deploy contextual "share publicly" prompts at every high-intent output moment:

| Product Moment | Share Surface | Prompt Copy | PostHog Event |
|----------------|---------------|-------------|---------------|
| Content creation complete | "Share publicly" button on completion screen | "Share this with the world" | `share_surface_creation_complete` |
| Export/download action | "Share a live version instead" option | "Let people interact with it, not just view a PDF" | `share_surface_export` |
| Milestone reached (10th project, etc.) | Achievement modal with share CTA | "You hit [milestone]. Show it off." | `share_surface_milestone` |
| Template usage | "Share your customized version" after template edit | "Others want to see how you made this yours" | `share_surface_template` |
| Collaboration invite | "Or share publicly" as alternative to private invite | "Anyone can view, no login needed" | `share_surface_collab` |

**Lifecycle email share surfaces** — inject share CTAs into existing Loops sequences:
- Weekly/monthly usage summary email: "Your top [content] this week — share it publicly?"
- Feature update email: "New: [feature]. Here is what others are sharing with it."
- Re-engagement email for lapsed users: "Your [content] is still getting views. Update it?"

**Social sharing mechanics** — optimize the distribution side:
- Add platform-specific share buttons on the share confirmation page: LinkedIn, Twitter/X, email, Slack, copy-link
- Pre-populate share text with a hook: "[User's content title] — made with [Product]. [link]"
- Generate platform-optimized preview images (square for Instagram/LinkedIn, 2:1 for Twitter)

Track each share surface independently with a `surface` property on all share events. After 4 weeks, rank surfaces by volume (shares initiated) and quality (viewer-to-signup conversion). Keep surfaces with >3% share rate; retire surfaces below 1%.

### 2. Run systematic A/B tests

Run the `ab-test-orchestrator` drill to test the highest-leverage variables:

**Test 1 — Share page CTA design (weeks 1-3):**
- Control: current CTA button
- Variant A: sticky bottom bar with CTA + product screenshot
- Variant B: inline CTA after content with "See how this was made" copy
- Variant C: floating badge in corner with product logo
- Primary metric: CTA click-through rate
- Secondary metric: signup completion rate
- Sample: minimum 200 share page views per variant

**Test 2 — Share page value proposition (weeks 3-5):**
- Control: "Made with [Product]"
- Variant A: "Create yours free in 2 minutes"
- Variant B: "[X users] are building with [Product]" (social proof)
- Variant C: "See how [content type] was made" (curiosity)
- Primary metric: CTA click-through rate
- Secondary metric: bounce rate

**Test 3 — Share prompt timing (weeks 5-7):**
- Control: prompt after content creation
- Variant A: prompt 24 hours after creation (content has "settled")
- Variant B: prompt after 3rd content creation (proven commitment)
- Variant C: prompt after first viewer interaction on a share page (social proof trigger)
- Primary metric: share initiation rate
- Secondary metric: share completion rate

**Test 4 — Incentive structure (weeks 7-9):**
- Control: current incentive
- Variant A: tiered rewards (1 share = badge, 5 = feature unlock, 10 = free month)
- Variant B: social recognition (top sharers featured on product homepage)
- Variant C: no explicit incentive (rely on intrinsic motivation)
- Primary metric: share rate
- Secondary metric: share-acquired user quality (activation rate)

After each test: implement the winner, document the result, and feed learnings into the next test hypothesis.

### 3. Build the viral loop measurement

Measure the viral loop end-to-end in PostHog:

1. **K-factor calculation:** For every 100 existing users, how many new users are acquired through public shares? Track: shares per user * viewers per share * signup rate per viewer = K-factor.
2. **Second-generation shares:** Track share-acquired users who go on to create their own public shares. This is the compounding mechanic. If K > 0.3, each new user brings in ~0.3 additional users, which compounds.
3. **Time-to-share for acquired users:** How long after signup does a share-acquired user create their first public share? If this is shorter than organic users, the viral loop is self-reinforcing.
4. **Share page SEO value:** Track organic search impressions and clicks on share pages via Google Search Console. Shared pages may accumulate long-tail search traffic over time, creating an evergreen acquisition channel.

Build a PostHog dashboard: "Public Sharing Viral Loop" with panels for K-factor trend, second-generation shares, time-to-share by acquisition source, and share page organic traffic.

### 4. Evaluate at scale

After 2 months, measure against threshold:

- **Primary:** >=30% share rate across 500+ active users
- **Secondary:** >=5% viewer-to-signup conversion maintained at scale
- **Viral:** Viral coefficient (K-factor) above 0.2
- **Quality:** Share-acquired user 30-day retention within 80% of organic user retention

If PASS: Document the winning share surfaces, CTA variants, prompt timing, and incentive structure. The play is ready for autonomous optimization. Proceed to Durable.

If FAIL: Identify the binding constraint. If share rate is below threshold, focus on share surface deployment and prompt optimization. If conversion is below threshold, focus on share page CTA and signup flow. If viral coefficient is below 0.2, focus on activating share-acquired users to share themselves. Run one more 4-week optimization cycle before reassessing.

## Time Estimate

- 12 hours: share surface deployment (5 in-product surfaces + 3 email surfaces)
- 24 hours: A/B test design, implementation, monitoring, and analysis (4 tests x 6 hours each)
- 8 hours: viral loop measurement setup and dashboard build
- 8 hours: social sharing mechanics (platform-specific previews, share text, buttons)
- 4 hours: weekly analysis and optimization (2 hours/week for 2 months = 16 hours, but 12 hours are absorbed into A/B test work)
- 4 hours: scale evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, funnels, dashboards | Free tier: 1M events/mo; Growth: $0.00045/event — https://posthog.com/pricing |
| Intercom | In-app share prompts across surfaces | ~$75-300/mo depending on MAU — https://www.intercom.com/pricing |
| Loops | Lifecycle email share CTAs | Included in standard stack |
| n8n | Workflow automation for share tracking | Included in standard stack |

**Play-specific cost:** Intercom ~$75-300/mo (for in-app messaging at scale). PostHog may exceed free tier at 500+ users with intensive experimentation — estimate $50-100/mo for additional events.

## Drills Referenced

- `referral-channel-scaling` — deploys share surfaces across every high-intent product moment and lifecycle email, with independent tracking per surface
- `ab-test-orchestrator` — designs, runs, and evaluates A/B tests on share page CTA, value proposition, prompt timing, and incentive structure
