---
name: engagement-scoring-scalable
description: >
  User Engagement Scoring — Scalable Automation. Connect engagement scores to automated
  interventions: re-engagement for declining users, expansion prompts for power users, and
  A/B-tested messaging per tier. Scale to 500+ scored users with maintained accuracy.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=70% churn prediction accuracy at 500+ scored users, with automated interventions producing >=15% re-engagement rate for At Risk users"
kpis: ["Churn prediction accuracy at scale (500+ users)", "Re-engagement rate (At Risk users returning to Casual+ within 14 days of intervention)", "Intervention coverage (% of tier-change events that trigger an automated action)", "False positive rate (% of At Risk flags that do not churn within 60 days)"]
slug: "engagement-scoring"
install: "npx gtm-skills add product/retain/engagement-scoring"
drills:
  - engagement-alert-routing
  - health-score-alerting
  - ab-test-orchestrator
---

# User Engagement Scoring — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Connect the engagement scoring pipeline to automated intervention systems. When a user's score drops, the system triggers the right response: in-app nudge for declining Engaged users, re-engagement email for At Risk users, personal outreach for high-value Dormant users, and expansion prompts for Power Users showing growth signals. Run A/B tests on intervention messaging to maximize re-engagement rates.

Scale the system to 500+ scored users while maintaining 70%+ churn prediction accuracy. The automated interventions should produce a 15%+ re-engagement rate: at least 15% of users flagged At Risk who receive an intervention return to Casual or higher engagement within 14 days.

## Leading Indicators

- Interventions fire within 4 hours of a tier-change detection
- In-app messages reach 60%+ of targeted users (measured by impression events)
- Re-engagement emails achieve 30%+ open rate and 10%+ click rate
- At least 2 A/B tests on intervention messaging have been run and evaluated
- Power User expansion prompts generate measurable upgrade or invite actions
- The scoring pipeline handles 500+ users without n8n workflow timeouts

## Instructions

### 1. Wire engagement scores to intervention routing

Run the `engagement-alert-routing` drill to connect tier-change events to the appropriate intervention channels:

1. Configure the n8n webhook that receives `engagement_tier_changed` events from the scoring pipeline
2. Implement the routing rules:
   - **Engaged -> Casual:** In-app nudge via Intercom highlighting the feature they stopped using (pull from breadth dimension data)
   - **Casual -> At Risk:** Re-engagement email via Loops with personalized content based on their highest-scoring dimension (lead with what they value most)
   - **At Risk -> Dormant:** If MRR > threshold, create Attio task for human outreach. If MRR < threshold, add to win-back email sequence.
   - **Any tier -> Power User:** In-app expansion prompt (invite teammates, explore advanced features, upgrade plan)
   - **Power User declining 2+ consecutive weeks:** Early warning alert to account owner before they drop tier
3. Implement rate limiting: maximum 1 in-app message per user per 7 days, maximum 1 email per user per 14 days

### 2. Build tier-specific health score alerting

Run the `health-score-alerting` drill adapted for per-user engagement scores:

1. Configure Tier 1 (automated nudge) for score drops from Engaged to Casual or when any dimension drops 15+ points in one week
2. Configure Tier 2 (outreach email) for score drops to At Risk or 3+ consecutive weeks in Casual with no improvement
3. Configure Tier 3 (human intervention) for score drops to Dormant or 20+ point drops in a single week on high-value accounts
4. Configure Tier 4 (expansion signal) for Power Users with rising breadth scores and approaching plan limits
5. Build the 14-day follow-up workflow that tracks whether each intervention produced re-engagement
6. Generate weekly intervention summary reports with recovery rates per tier

### 3. A/B test intervention messaging

Run the `ab-test-orchestrator` drill to test intervention effectiveness:

**Test 1: Re-engagement email subject lines**
- Control: "Need a hand with {{productName}}?"
- Variant A: "Your {{topFeature}} results are waiting"
- Variant B: "What {{similarUser}} discovered this week in {{productName}}"
- Measure: open rate, click rate, re-engagement within 7 days
- Run for 4 weeks or 100+ recipients per variant

**Test 2: In-app nudge positioning and content**
- Control: Generic "Welcome back" banner
- Variant A: Feature-specific deep link ("Pick up your {{lastProject}}")
- Variant B: Social proof ("{{teammateName}} just used {{feature}} -- check it out")
- Measure: click rate, subsequent session depth, 7-day retention
- Run for 4 weeks using PostHog feature flags

**Test 3: Intervention timing**
- Control: Trigger on tier change day
- Variant A: 48-hour delay after tier change (some users self-correct)
- Variant B: Trigger only after 2 consecutive days at the new lower tier
- Measure: re-engagement rate, false positive reduction
- Run for 4 weeks

After each test completes, implement the winning variant as the new default. Document the results.

### 4. Scale to 500+ users

As the scored user base grows:

1. Optimize the n8n scoring workflow for batch processing: query PostHog for all users in a single HogQL query rather than per-user queries
2. Add error handling: if PostHog API times out, retry with smaller batches. If Attio write fails, queue and retry.
3. Monitor pipeline execution time. If the workflow takes more than 30 minutes, add parallelization in n8n or split into sub-workflows by user cohort.
4. Verify score accuracy does not degrade at scale: re-run the back-test monthly

### 5. Evaluate against threshold

After 2 months, measure:

1. **Churn prediction accuracy at 500+ users:** Pull the back-test numbers. Target: 70%+ of churners were flagged At Risk or Dormant 14 days before churn.
2. **Re-engagement rate:** Of At Risk users who received an automated intervention, what percentage returned to Casual or higher within 14 days? Target: 15%+.
3. **Intervention coverage:** What percentage of tier-change events triggered an automated action? Target: 95%+ (exceptions: rate-limited users).

If all three pass, the scoring system is delivering measurable retention impact at scale. Proceed to Durable.

If any fail:
- Low churn accuracy: Review scoring model, consider adding new dimensions or adjusting weights
- Low re-engagement rate: Run more A/B tests on messaging, review intervention timing
- Low coverage: Debug the routing workflow for missed events or error states

## Time Estimate

- 12 hours: Wire engagement alert routing (step 1)
- 10 hours: Build health score alerting adapted for per-user scores (step 2)
- 20 hours: Design, run, and evaluate 3 A/B tests over 2 months (step 3)
- 8 hours: Scale optimization and monitoring (step 4)
- 10 hours: Ongoing monitoring, debugging, and threshold evaluation (step 5)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Scoring queries, cohorts, experiments, feature flags | Free tier: 1M events/mo. https://posthog.com/pricing |
| n8n | Scoring workflow, alert routing, A/B test orchestration | Free (self-hosted) or $20/mo (cloud). https://n8n.io/pricing |
| Attio | CRM for scores, tasks, intervention tracking | Free tier: 3 users. https://attio.com/pricing |
| Intercom | In-app messages for nudges and expansion prompts | Starter: ~$74/mo. https://www.intercom.com/pricing |
| Loops | Re-engagement emails and sequences | Free tier: 1,000 contacts. https://loops.so/pricing |

## Drills Referenced

- `engagement-alert-routing` -- routes tier-change events to the right intervention channel based on score severity and account value
- `health-score-alerting` -- tiered intervention system with automated nudges, emails, human routing, and expansion signals
- `ab-test-orchestrator` -- designs, runs, and evaluates A/B experiments on intervention messaging and timing
