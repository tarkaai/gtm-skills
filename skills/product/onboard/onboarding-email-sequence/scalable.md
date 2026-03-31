---
name: onboarding-email-sequence-scalable
description: >
  Onboarding email sequence — Scalable Automation. A/B test email content,
  segment sequences by user type, and build parallel tracks that optimize
  activation rate at 10x signup volume.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Email"
level: "Scalable Automation"
time: "30 hours over 2 months"
outcome: "Activation rate >= 30% at day 7 sustained over 2 months, with winning A/B variants deployed across all segments"
kpis: ["Activation rate at day 7 by segment", "A/B test win rate", "Time to activation by segment", "Email-to-activation conversion by email step", "Sequence completion rate", "Activation rate trend (weekly)"]
slug: "onboarding-email-sequence"
install: "npx gtm-skills add product/onboard/onboarding-email-sequence"
drills:
  - ab-test-orchestrator
  - activation-optimization
  - threshold-engine
---

# Onboarding Email Sequence — Scalable Automation

> **Stage:** Product > Onboard | **Motion:** Lead Capture Surface | **Channels:** Email

## Outcomes

Scale the onboarding email sequence to handle all signups with segment-specific tracks and continuous A/B testing. Instead of one sequence for everyone, build parallel sequences tailored to user type, plan, or signup source. Run systematic tests on subject lines, send timing, email content, and CTA placement. Sustain activation rate >= 30% at day 7 over 2 months while handling 10x the volume of Baseline.

## Leading Indicators

- First A/B test reaches statistical significance within 2 weeks of launch
- At least 2 segments show meaningfully different activation rates (validating the need for segmentation)
- Winning variants improve open rate or click rate by >= 10% relative over the control
- Activation rate trend is flat or increasing week over week (not degrading as volume grows)
- No deliverability issues: bounce rate < 2%, spam complaint rate < 0.1%

## Instructions

### 1. Segment users into onboarding tracks

Using PostHog cohorts and Loops audience segments, split new signups into 2-4 tracks based on the dimension that most affects their onboarding path. Common segmentation axes:

- **By use case / intent:** If your product serves multiple use cases, each use case has a different activation action. Ask during signup (one question: "What are you trying to accomplish?") or infer from first actions.
- **By plan type:** Free vs trial vs paid users have different urgency levels and feature access.
- **By signup source:** Users from different channels (organic, paid, referral, product hunt) have different context and expectations.
- **By company size / role:** Solo users vs team leads need different onboarding paths.

For each segment, customize:
- The activation metric (may differ by use case)
- Email content (use case examples, social proof from similar companies)
- CTA links (point to the specific feature relevant to their track)
- Timing (trial users need faster cadence due to expiration deadline)

Create separate Loops sequences for each track. In n8n, add a routing step after enrollment that assigns users to the correct sequence based on their PostHog properties.

### 2. Run systematic A/B tests on email content

Run the `ab-test-orchestrator` drill for each test. Test one variable at a time across the full sequence. Prioritize tests by expected impact:

**Test 1 — Subject lines (weeks 1-2):**
For Email 1, test two subject line approaches: direct ("Here's your quickstart guide") vs curiosity ("The one thing to do first in [Product]"). Measure open rate. Apply the winning pattern to all emails.

**Test 2 — CTA placement and copy (weeks 3-4):**
For Emails 2-4, test CTA at top of email vs bottom. Test action-oriented CTA ("Create your first project") vs benefit-oriented CTA ("See your first results in 2 minutes"). Measure click rate.

**Test 3 — Send timing (weeks 5-6):**
Test Email 2 at 12 hours vs 24 hours after signup. Test Email 3 at 36 hours vs 72 hours. Measure activation rate (not just open rate — earlier may get fewer opens but drive more activation).

**Test 4 — Email length and format (weeks 7-8):**
Test short (50 words, one link) vs medium (150 words, one screenshot, one link) for Emails 2-4. Measure click-through to activation.

For each test:
- Use Loops A/B testing for broadcast-style tests, or PostHog feature flags routed through n8n for behavioral tests
- Require minimum 200 users per variant before declaring a winner
- Document hypothesis, result, and confidence level
- Apply the winning variant permanently before starting the next test

### 3. Optimize activation bottlenecks

Run the `activation-optimization` drill in parallel with A/B testing. While email tests improve the sequence itself, activation optimization improves what happens AFTER the click:

1. Build a PostHog funnel from `email_clicked` to `activation_reached` broken down by email step
2. Identify which email step has the highest click rate but lowest post-click activation rate — this is where the product experience fails to deliver on the email's promise
3. For that step: either fix the product flow (reduce friction between click and activation action) or rewrite the email CTA to set more accurate expectations

Focus on the single biggest bottleneck. A 10% improvement at the worst step beats 2% improvements everywhere.

### 4. Build weekly performance reporting

Create an automated weekly report (n8n scheduled workflow) that includes:

- Activation rate for each segment (treatment vs control)
- Activation rate trend over time (is it improving, stable, or declining?)
- Per-email metrics: open rate, click rate, click-to-activation rate for each of the 7 emails
- Active A/B test status: current sample size, estimated days to significance, preliminary results (do NOT act on preliminary results)
- Deliverability health: bounce rate, spam complaints, unsubscribes

Post the report to Slack or email every Monday morning.

### 5. Handle volume scaling

As signup volume increases, monitor for:

- **Deliverability degradation:** If open rates drop across all emails, check domain reputation and sending volume ramp. Loops handles warm-up automatically, but sudden volume spikes can trigger spam filters.
- **Webhook throughput:** If n8n workflows start queuing, increase execution limits or batch-process enrollments.
- **Sequence stacking:** If your product has a free trial with expiration, trial users who have not activated by day 5 need a more aggressive cadence. Create an "urgent" variant of the sequence for trial users in the final 48 hours.

### 6. Evaluate at month 2

Run the `threshold-engine` drill with these criteria:

- **Activation rate >= 30% at day 7** for the best-performing segment
- **Activation rate sustained** — weekly activation rate does not drop more than 5 percentage points from the peak over the 2-month period
- **A/B testing cadence:** At least 4 tests completed with 2+ winning variants deployed
- **Segmentation validated:** At least 2 segments show statistically different activation rates

If PASS: Proceed to Durable for autonomous optimization.
If FAIL on activation rate: Focus all effort on the single weakest email step (lowest click-to-activation rate) and run a focused test round.
If FAIL on sustained performance: Investigate if message fatigue is setting in. Refresh email content or test reducing the sequence to fewer emails.

## Time Estimate

- 6 hours: Build segmented sequences and routing logic in Loops and n8n
- 8 hours: Design, launch, and analyze 4 A/B tests (2 hours each)
- 4 hours: Activation optimization analysis and product fixes
- 4 hours: Set up weekly reporting automation
- 8 hours: Weekly monitoring and iteration over 2 months (1 hour/week)

Total: ~30 hours spread over 2 months.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loops | Segmented email sequences, A/B testing, delivery | $49/mo (unlimited emails). Higher tiers for larger contact lists. [Pricing](https://loops.so/pricing) |
| PostHog | Event tracking, funnels, cohorts, feature flags for A/B tests | Free up to 1M events/mo. Usage-based beyond. [Pricing](https://posthog.com/pricing) |
| n8n | Workflow automation, routing, weekly reporting | Cloud from €24/mo (Starter) or €60/mo (Pro, 10K executions). Free self-hosted. [Pricing](https://n8n.io/pricing/) |
| Cal.com | Booking links in help-offer emails | Free for 1 user. [Pricing](https://cal.com/pricing) |

**Estimated monthly cost: $49-110/mo** (Loops $49 + n8n €24-60. PostHog and Cal.com free tier for most volumes.)

## Drills Referenced

- `ab-test-orchestrator` — designs, runs, and analyzes A/B tests on email subject lines, content, timing, and CTAs
- `activation-optimization` — finds the biggest activation bottleneck and systematically removes friction
- `threshold-engine` — evaluates activation rate, sustainability, and test velocity against pass/fail criteria
