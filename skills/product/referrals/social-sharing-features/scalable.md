---
name: social-sharing-features-scalable
description: >
  Built-In Social Sharing — Scalable Automation. Find the 10x multiplier for viral
  growth: A/B test share surfaces, content variants, and prompt timing. Expand
  sharing to all resource types. Integrate with referral rewards. Build the
  self-reinforcing viral loop where shares drive signups that create more sharers.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Social"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=15% share initiation rate AND K-factor >=0.10 AND >=100 viral signups per month"
kpis: ["Share initiation rate (all users)", "K-factor (4-week rolling)", "Viral signups per month", "Share link CTR by channel", "Revenue attributed to viral signups", "Cost per viral acquisition vs paid channels"]
slug: "social-sharing-features"
install: "npx gtm-skills add product/referrals/social-sharing-features"
drills:
  - ab-test-orchestrator
  - referral-program
---

# Built-In Social Sharing — Scalable Automation

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Social

## Outcomes

The viral sharing loop scales from a measurable signal to a significant acquisition channel. A/B testing systematically optimizes every component of the share funnel: button placement, prompt timing, content variants, OG card designs, and landing page conversion. Sharing expands to all shareable resource types. Referral rewards incentivize repeat sharing. After 2 months, at least 15% of active users share, the K-factor reaches 0.10+, and the viral loop generates 100+ signups per month at a cost per acquisition below paid channels.

## Leading Indicators

- A/B tests produce statistically significant winners within 2-week cycles
- Share initiation rate increases month-over-month as winning variants roll out
- Share content CTR increases as AI-generated content is optimized (new variants outperform control)
- Referral reward mechanism activates repeat sharing: sharers with rewards share 3x more than those without
- Channel-specific optimization produces differentiated CTR improvements (LinkedIn and Twitter respond to different strategies)
- Viral signups as a percentage of total new signups trends upward month over month
- Cost per viral acquisition is tracking below 50% of paid channel CPA

## Instructions

### 1. A/B test every component of the share funnel

Run the `ab-test-orchestrator` drill to systematically optimize the share funnel. Run these experiments sequentially (one at a time per the autonomous-optimization guardrails):

**Test 1 — Share button placement and design:**
- Control: current share button in the resource header
- Variant A: floating share button that follows scroll (always visible)
- Variant B: share button embedded inline after the resource's key metric/output
- Variant C: contextual "Share this result" link that appears only when the resource has impressive data
- Metric: share_widget_opened / share_surface_impression
- Duration: 2 weeks or 200+ impressions per variant

**Test 2 — Share prompt timing:**
- Control: show share prompt after user views the resource for 5 seconds
- Variant A: show prompt immediately after the user completes a milestone or workflow
- Variant B: show prompt on the second visit to the same resource (user returning = higher intent)
- Variant C: show prompt after a positive micro-interaction (export, favorite, or pin the resource)
- Metric: share_widget_opened / share prompt shown
- Duration: 2 weeks or 100+ prompts per variant

**Test 3 — Share content variants:**
- Control: static template-based share text
- Variant A: AI-generated metric-focused text ("I tracked 142K in revenue this month")
- Variant B: AI-generated question-hook text ("How do you track your revenue metrics?")
- Variant C: AI-generated narrative text ("Building in public: here's my dashboard for Q1")
- Metric: share_link_clicked / share_action_completed (CTR of shared links)
- Duration: 2 weeks or 50+ shares per variant

**Test 4 — OG card design:**
- Control: current branded OG card with resource title and metric
- Variant A: dark-mode OG card (stands out in light-themed social feeds)
- Variant B: OG card with the user's avatar and a social proof line ("used by 500+ teams")
- Variant C: OG card that shows a mini-preview of the actual resource (dashboard screenshot, chart thumbnail)
- Metric: share_link_clicked / share_action_completed
- Duration: 2 weeks or 50+ shares per variant

**Test 5 — Landing page for shared links:**
- Control: show the shared resource with a signup banner at the top
- Variant A: show a blurred preview with "Sign up to see the full [resource]" gate
- Variant B: show the full resource ungated with a persistent bottom bar: "Create your own — sign up free"
- Variant C: show the resource with inline CTAs at the data points: "Want this metric for your team?"
- Metric: share_referral_signup / share_link_clicked
- Duration: 2 weeks or 100+ link clicks per variant

Implement winners immediately after each test. Log results in Attio with hypothesis, variants, sample sizes, and decision.

### 2. Optimize share content generation

Run the the share content generator workflow (see instructions below) drill with enhanced optimization:

- Use the Baseline period's channel CTR data to weight content generation toward higher-performing channels
- For each channel, maintain 3 active content variants and rotate based on performance
- Train the AI content generation prompt on the top-performing share texts from the Baseline period (include examples of high-CTR shares in the prompt context)
- Implement a feedback loop: when a share link gets clicked, positively weight that content variant. When it gets no clicks after 48 hours, negatively weight it.
- Pre-generate share content for the top 100 most-shared resource types daily (reduce latency for popular resources)

### 3. Integrate referral rewards with sharing

Run the `referral-program` drill to add incentives to the viral sharing loop:

- Design a reward structure tied to sharing outcomes (not just shares, but outcomes):
  - Share a link: no reward (sharing itself should be frictionless, not transactional)
  - Shared link leads to a signup: sharer earns a credit or feature unlock
  - Referred user activates (completes first workflow): sharer earns a larger credit
  - Referred user upgrades to paid: sharer earns a significant credit (e.g., free month)
- Build the reward pipeline in n8n: `share_referral_activated` event triggers reward calculation and delivery
- Notify sharers at each stage via Loops transactional emails: "Someone clicked your link," "Your referral signed up," "You earned [reward]!"
- Add a "Your Shares" dashboard in-product: total shares, link clicks, signups, rewards earned
- Build a referral leaderboard: top sharers this month (anonymized counts unless user opts into public)
- Track: does the referral reward increase repeat sharing? Compare sharer behavior before and after first reward.

### 4. Expand sharing to all resource types

Extend the share surface to every shareable resource type in the product:

- Deploy share buttons on all resource types identified in the Smoke-level audit
- Configure resource-type-specific OG card templates (dashboards show chart previews, achievements show the milestone, templates show a usage screenshot)
- Configure resource-type-specific share text templates for each channel
- Track share volume and CTR per resource type. Prioritize optimization on the highest-volume types.

### 5. Build the scalable reporting layer

Create a weekly viral growth report that runs automatically via n8n:

- **Share funnel**: impression rate, initiation rate, completion rate, link CTR — with week-over-week trends
- **Viral metrics**: K-factor trend, viral signups count, viral activation count, viral revenue attribution
- **Channel performance**: share volume, CTR, and signup rate by channel (Twitter, LinkedIn, email, copy link, native share)
- **Resource performance**: share volume and conversion by resource type
- **Experiment log**: active tests, completed tests, cumulative improvement from winners
- **Referral rewards**: rewards issued, cost of rewards, LTV of referred users vs organic users
- **Efficiency**: cost per viral acquisition vs paid channel CPA

Post to Slack weekly. Store in Attio.

### 6. Evaluate against threshold

After 2 months, measure:

- **Share initiation rate**: share_widget_opened / unique active users with share button impressions. Target: >=15%.
- **K-factor**: (shares per active user per month) * (signups per share). Target: >=0.10.
- **Viral signups per month**: Target: >=100.

If PASS: the viral loop is a significant, scalable acquisition channel. Proceed to Durable.
If FAIL on initiation rate: users are not sharing enough. Review the A/B test results — did any test significantly move initiation? If not, the core share motivation may need product changes (make resources more impressive, add competitive elements, add social features).
If FAIL on K-factor: shares happen but do not convert. Focus optimization on the landing page conversion and OG card quality. The shared content may not be compelling enough to external visitors.
If FAIL on viral signups: traffic volume is too low. Consider adding more share surfaces, increasing prompt frequency (carefully), or adding sharing to email signatures and export files.

## Time Estimate

- 20 hours: A/B test design, implementation, and evaluation (5 tests over 2 months)
- 10 hours: share content generation optimization and variant tracking
- 10 hours: referral reward system build and integration
- 8 hours: expand sharing to all resource types
- 7 hours: reporting layer and weekly automation
- 5 hours: 2-month monitoring and evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, funnels, dashboards, cohorts | Usage-based: ~$0.00005/event beyond 1M free/mo; experiments included ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Share prompts, feature announcements, share celebration messages | Essential $29/seat/mo + Proactive Support $99/mo ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Referral notifications, reward emails, sharer re-engagement | Starter $49/mo up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Reward pipeline, reporting automation, content generation triggers | Self-hosted: free; Cloud: from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Share text generation, content variant optimization | Claude API: estimated $30-80/mo at scale ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Attio | Sharer records, experiment logs, referral tracking, report storage | Pro: $34/seat/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Vercel | OG image generation at scale | Pro: $20/mo ([vercel.com/pricing](https://vercel.com/pricing)) |

**Estimated play-specific cost at this level:** $200-450/mo (Intercom Proactive Support + Anthropic API + Attio Pro are main drivers)

## Drills Referenced

- `ab-test-orchestrator` — systematic A/B testing of share button placement, prompt timing, content variants, OG cards, and landing pages
- the share content generator workflow (see instructions below) — optimized AI-generated share content with variant tracking and performance-based rotation
- `referral-program` — referral reward mechanism integrated with the share viral loop
