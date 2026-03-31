---
name: user-generated-content-scalable
description: >
  UGC Campaign — Scalable Automation. Launch tiered creator incentives, monthly contests,
  and social proof loops to multiply UGC production. A/B test prompt copy, timing, and
  incentive structures. Scale amplification to 3+ channels. Find the 10x by making content
  creation self-reinforcing through recognition, rewards, and community visibility.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Referrals"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: ">=40 approved UGC pieces/month from >=15 unique creators with >=100 referral visits/month from UGC"
kpis: ["Monthly approved UGC pieces (target >=40)", "Monthly unique creators (target >=15)", "Repeat creator rate (target >=25%)", "Prompt-to-submission conversion rate (target >=6%)", "Monthly referral visits from UGC (target >=100)", "Referral signups attributed to UGC (target >=5/month)", "Contest participation rate (target >=5% of eligible users)"]
slug: "user-generated-content"
install: "npx gtm-skills add product/referrals/user-generated-content"
drills:
  - ab-test-orchestrator
  - dashboard-builder
---

# UGC Campaign — Scalable Automation

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Referrals

## Outcomes

Scale from a working UGC pipeline to a self-reinforcing content creation flywheel. The 10x comes from three multipliers: (1) tiered creator incentives that reward repeat contributions and create status motivation, (2) monthly contests that create urgency and friendly competition, and (3) social proof loops where seeing others' UGC motivates new creators. A/B test every element of the prompting and incentive system to find what drives the most and best content. Scale amplification across 3+ channels with automated formatting and scheduling.

Pass: >=40 approved UGC pieces per month from >=15 unique creators, with >=25% repeat creator rate, and >=100 referral visits per month from amplified UGC.
Fail: UGC volume does not scale beyond Baseline levels despite incentives, or repeat creator rate stays below 15%.

## Leading Indicators

- First monthly contest generates >=3x the weekly submission average during the contest window (contests create urgency)
- At least 3 creators reach the "Active Creator" tier (3+ submissions) within the first month (the tier system motivates repeat behavior)
- In-product UGC showcase drives at least 1 new first-time creator per week (social proof works as a flywheel)
- A/B tests on prompt copy produce a statistically significant winner within 4 weeks (there is optimization headroom)
- Referral visit volume from UGC grows month-over-month (amplification is compounding)
- Creator notification emails ("your content was featured") achieve >=60% open rate and >=10% lead to a new submission (the notification loop works)

## Instructions

### 1. Launch the creator incentive system

Run the the ugc incentive scaling workflow (see instructions below) drill. This deploys the full incentive framework:

**Creator tier system:**
Set up 3 tiers in Attio with automated promotion:
- **First-time Creator:** Entry on first approved submission. Reward: public thank-you + "Contributor" badge in product (via PostHog feature flag).
- **Active Creator (3+ approved pieces):** Reward: "Creator" badge visible to other users + featured spotlight in newsletter + 1 month free feature credit.
- **Featured Creator (5+ pieces, avg quality >=4.0):** Reward: permanent "Featured Creator" badge + co-marketing opportunity + direct product team access + annual swag.

The n8n workflow checks daily for users crossing tier thresholds, updates Attio, enables feature flags, sends congratulatory messages, and delivers rewards.

**Monthly themed contests:**
Launch the first contest in week 1. Theme examples: "Best workflow automation," "Most creative use case," "Video walkthrough challenge." The n8n workflow automates the lifecycle: announcement email + in-app banner on day 1, reminder on day 7, close submissions on day 14, AI moderation + human judging days 15-21, winner announcement on day 22. Prizes: featured blog post + $100 credit for the winner, social amplification for top 3, participation badge for all entrants.

**Social proof loops:**
Deploy in-product UGC showcase via Intercom: show recent approved UGC to non-creators, targeted by role and industry. Update UGC prompts to include community stats: "47 users shared their setup this month. Join them." Build a creator leaderboard (PostHog dashboard or in-product page) showing top creators this month.

### 2. Run systematic A/B tests on the UGC system

Run the `ab-test-orchestrator` drill to test one variable at a time. Prioritize by expected impact:

**Month 1 tests:**

1. **Prompt copy test:** On the post-activation prompt (highest volume trigger), test 2 CTA variants. Example: "Share your setup" vs "Write a quick tip -- it takes 60 seconds." Use PostHog feature flags to split traffic 50/50. Measure `ugc_form_completed` rate per variant. Run for 14 days or 500 prompt impressions per variant.

2. **Form length test:** Test the current form (3 fields) against a minimal form (1 field: just the tip text, everything else auto-populated). Measure submission completion rate AND approval rate (shorter forms may produce lower-quality content).

**Month 2 tests:**

3. **Trigger timing test:** On the milestone prompt, test showing it immediately when the milestone is hit vs 24 hours later. Measure conversion rate and content quality.

4. **Incentive test:** Test the "Contributor badge" reward against a "featured in newsletter" reward for first-time creators. Measure which drives more second submissions within 30 days.

5. **Social proof test:** Test UGC prompts with social proof ("47 users shared this month") against prompts without. Measure conversion rate.

For each test: form hypothesis, calculate sample size, run to significance, document results, implement winners.

### 3. Scale amplification to 3+ channels

Expand the the ugc amplification pipeline workflow (see instructions below) from Baseline:

**LinkedIn (2-3 UGC posts per week):**
Increase from 1 to 2-3 posts per week. Alternate between: full user stories, quick tips/quotes, and contest winner spotlights. Use creator tags for reach.

**Email newsletter (every edition):**
Add a permanent "Community spotlight" section. Feature 1 flagship UGC piece + 2-3 quick tips. Include a CTA: "Got a story? Submit yours."

**In-product (continuous):**
Expand Intercom UGC showcases to target multiple user segments. Show tutorials to users who haven't used that feature. Show testimonials near upgrade triggers. Show industry-specific case studies to users in that industry.

**Blog (2-4 UGC pieces/month):**
Publish the best tutorials and use cases as guest blog posts with full creator byline. These become SEO assets that compound over time.

**Community channels (ongoing):**
Share UGC in your Slack/Discord community with creator attribution. Pin the best pieces.

### 4. Deploy the UGC health monitor

Run the `dashboard-builder` drill to build always-on monitoring for the scaled system:

Configure the 8 health metrics: submission rate, approval rate, prompt conversion, creator diversity, repeat rate, amplification throughput, referral traffic, and content quality trend. Set healthy/warning/critical thresholds. Enable automated interventions for prompt fatigue, repeat rate stalls, amplification backlogs, and quality declines.

The health monitor runs daily via n8n and generates a weekly report with trends, creator spotlights, and recommendations.

### 5. Evaluate after 2 months

Review the `dashboard-builder` weekly reports and PostHog dashboards for the full 2-month period:

- Monthly approved UGC pieces (month 1 and month 2)
- Monthly unique creators
- Repeat creator rate (creators with 2+ submissions / total creators)
- Tier distribution: how many First-time, Active, Featured creators?
- Contest metrics: entries per contest, winner quality, post-contest submission bump
- A/B test results: how many ran, how many produced winners, cumulative improvement
- Amplification metrics per channel: impressions, clicks, referral visits, signups
- Cost: total tool costs + credits/rewards / total approved pieces = cost per UGC piece

- **PASS (>=40 pieces/month, >=15 creators, >=25% repeat rate, >=100 referral visits/month):** The UGC flywheel is spinning. The incentive system, contests, and social proof create self-reinforcing content creation. Document: winning prompt variants, best-performing incentives, highest-ROI amplification channels, and the creator tier distribution. Proceed to Durable.
- **MARGINAL (25-39 pieces/month or 10-14 creators or 15-24% repeat rate):** The system is working but not yet at the 10x multiplier. Check: Are contests driving sufficient participation? Are the tier rewards motivating? Which A/B tests showed the most headroom? Focus on the weakest multiplier and iterate. Stay at Scalable.
- **FAIL (volume flat vs Baseline despite incentives, or repeat rate <15%):** The incentive structure is not motivating content creation. Diagnose: Are users aware of the program? Is the user base engaged enough to create content? Are the rewards valuable to your users? Consider restructuring incentives (monetary rewards vs. status, different creator tiers) or pivoting to a more targeted approach (recruit 5-10 power users personally as a creator cohort).

## Time Estimate

- Creator incentive system setup: 8 hours
- Contest framework and first contest launch: 6 hours
- A/B test setup and management (4-5 tests over 2 months): 12 hours
- Amplification scaling (3+ channels): 6 hours
- Health monitor deployment: 4 hours
- Weekly monitoring and reporting: 1 hour/week x 8 weeks = 8 hours
- Evaluation and documentation: 4 hours
- Buffer: 2 hours
- Total: ~50 hours over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, A/B experiments, feature flags, cohorts | Free tier: 1M events/mo; paid ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | All automation: incentive workflows, contests, monitoring, amplification | Pro EUR60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | CRM: UGC Library, Contributors, creator tiers | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Intercom | In-app prompts, UGC showcases, contest banners | Essential $29/seat/mo annual ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Creator sequences, newsletter UGC features, contest emails | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Anthropic API | AI content moderation | Usage-based ~$3/1M input tokens ([anthropic.com/pricing](https://anthropic.com/pricing)) |

**Estimated monthly cost for Scalable:** $170-270/mo (n8n Pro + Attio Plus + Intercom + Loops; plus contest prizes ~$100/month)

## Drills Referenced

- the ugc incentive scaling workflow (see instructions below) — design and automate the 3-tier creator program, monthly contest framework, social proof loops, and reward delivery system that multiply UGC production
- `ab-test-orchestrator` — design, run, and analyze A/B tests on prompt copy, form length, trigger timing, incentive structures, and social proof elements using PostHog feature flags
- `dashboard-builder` — monitor 8 UGC health metrics daily with diagnostics, automated interventions for prompt fatigue and repeat rate stalls, and weekly health reports
