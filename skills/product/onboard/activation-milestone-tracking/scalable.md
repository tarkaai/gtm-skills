---
name: activation-milestone-tracking-scalable
description: >
  Activation Milestone Tracking — Scalable Automation. A/B test milestone
  variations across segments, build churn prevention from milestone data, and
  deploy upgrade prompts at activation moments. Target ≥45% activation rate
  sustained across 500+ monthly signups.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥45% activation rate sustained across 500+ monthly signups for 4 consecutive weeks"
kpis: ["Activation rate at scale", "Per-milestone completion rate by segment", "Experiment win rate", "Churn save rate", "Upgrade conversion rate"]
slug: "activation-milestone-tracking"
install: "npx gtm-skills add product/onboard/activation-milestone-tracking"
drills:
  - ab-test-orchestrator
  - churn-prevention
  - upgrade-prompt
---

# Activation Milestone Tracking — Scalable Automation

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Activation rate sustains ≥45% across 500+ monthly signups for 4 consecutive weeks. Systematic A/B testing runs on the highest-drop-off milestone each cycle. Churn prevention system detects users who activated but are declining, triggering retention interventions. Upgrade prompts fire at activation moments to capture expansion revenue. Per-segment milestone data enables different optimization strategies for different user types.

## Leading Indicators

- At least 1 A/B test running on a milestone variation at all times
- Experiment results reach statistical significance within 3 weeks (sufficient traffic per variant)
- Churn detection workflow identifies at-risk users before they go inactive for 14+ days
- Upgrade prompts fire at the value-moment milestone and produce measurable click-through
- Segment-specific activation rates are tracked and improving independently

## Instructions

### 1. Launch systematic milestone A/B testing

Run the `ab-test-orchestrator` drill to set up a continuous testing program on activation milestones. The process:

**Identify the test target:**
Query the PostHog milestone funnel from Baseline level. Find the milestone with the highest absolute drop-off (not highest percentage drop — the step losing the most users in absolute terms). This is your first test target.

**Design the experiment:**
Form a hypothesis following the drill's structure: "If we [change X at milestone N], then [milestone N completion rate] will increase by [Y percentage points], because [reasoning]."

Example hypotheses by milestone:
- Milestone 2 (configuration): "If we reduce the setup form from 8 fields to 3 required fields with the rest optional, completion rate will increase by 15 points, because shorter forms reduce abandonment on mobile."
- Milestone 3 (first core action): "If we add sample data that pre-populates the workspace, first-action rate will increase by 10 points, because users can explore value without investing setup effort."
- Milestone 4 (value moment): "If we show a results preview within 5 seconds instead of requiring a full workflow, value-moment rate will increase by 12 points, because instant feedback sustains motivation."

**Run the test:**
Use PostHog feature flags to split new signups 50/50 between control and variant. Set minimum sample size per variant (200 users or 14 days, whichever comes first). Track the primary metric (milestone completion rate) and secondary metric (downstream activation rate — winning a milestone should not hurt overall activation).

**Implement and iterate:**
When a test reaches significance: implement the winner permanently, document the result in Attio, and immediately start the next test on the new highest-drop-off milestone. Target: 2-3 completed experiments per month.

### 2. Build segment-specific milestone paths

Using PostHog cohorts from the Baseline dashboard, identify segments with significantly different activation patterns. Common segmentation dimensions:

- **Signup source:** Organic vs. paid vs. referral users may need different onboarding emphasis
- **Plan type:** Free users vs. trial users have different urgency levels
- **Company size:** Solo users vs. team accounts have different milestone paths
- **Use case:** If your product serves multiple use cases, the "first core action" differs

For each segment with activation rate >10 points below the overall rate, create a segment-specific test: different product tour content, different email sequence messaging, or different milestone ordering. Use PostHog feature flags to route segments to their optimized paths.

### 3. Deploy churn prevention from milestone data

Run the `churn-prevention` drill, using milestone data as the primary signal source. Configure these churn signals:

**Pre-activation churn signals (users who started but have not activated):**
- Completed Milestone 2 but stalled at Milestone 3 for 7+ days: High risk. Trigger personal outreach email with a calendar link.
- Completed Milestone 3 but no return session for 10+ days: Medium risk. Trigger Intercom in-app message on next login offering help.
- Completed only Milestone 1 after 14 days: Very high risk. Trigger winback email with an offer (extended trial, setup call, simplified path).

**Post-activation churn signals (users who activated but are declining):**
- Weekly active sessions dropped 50%+ vs. their 4-week average: Usage decline. Trigger Intercom message highlighting an unused feature.
- No login for 7+ days after being daily active: Gap signal. Trigger Loops email: "We noticed you have not been back — here is what is new since your last session."
- Visited pricing/cancellation page: Immediate risk. Create Attio task for account owner with full usage history.

**The n8n workflow runs daily:**
1. Query PostHog for users matching each churn signal
2. Score risk: sum of signal weights → low (20-40), medium (40-70), high (70+)
3. Route to appropriate intervention
4. Log intervention in Attio
5. Track outcome: re-engaged within 14 days yes/no

### 4. Set up upgrade prompts at activation moments

Run the `upgrade-prompt` drill, keyed to specific milestone triggers:

**Trigger 1: Value moment reached (Milestone 4)**
When a free/trial user reaches the value moment: Show an Intercom banner — "You just [achieved X]. Upgrade to [Plan] to [get more of this value]." This is the highest-intent moment for expansion.

**Trigger 2: Return power user (Milestone 5 repeated)**
When a user returns for their 5th session within 14 days: They are forming a habit. Show a subtle Intercom tooltip highlighting a paid feature relevant to their usage pattern.

**Trigger 3: Limit proximity**
When a user approaches a plan limit (storage, API calls, seats): Show a contextual message at the point of friction — not a generic modal, but a message tied to the specific limit they are hitting.

**Trigger 4: Team growth**
When a user invites 2+ teammates: This signals organizational adoption. Send a Loops email about team/enterprise features.

Track the full upgrade funnel: trigger fired → prompt shown → prompt clicked → upgrade started → upgrade completed. Report conversion rate by trigger type weekly.

### 5. Evaluate against threshold

Pass criteria:

- **≥45% activation rate** across 500+ monthly signups, sustained for 4 consecutive weeks.

If PASS: Scalable systems are working — A/B testing, churn prevention, and upgrade prompts all contribute to sustained performance. Proceed to Durable.

If FAIL on activation rate: Focus on the A/B testing pipeline. Are experiments producing wins? If experiments are inconclusive, test bigger changes (not copy tweaks — structural changes to the milestone flow).

If FAIL on scale: Activation rate held at lower volume but dropped at 500+. Investigate segment mix shift: are you attracting a different user profile at scale? Segment-specific paths may need adjustment.

## Time Estimate

- 15 hours: Set up A/B testing infrastructure and run first 2 experiments
- 10 hours: Build segment-specific milestone paths
- 15 hours: Configure churn prevention signals and interventions
- 10 hours: Deploy upgrade prompt system
- 5 hours: Dashboard updates and ongoing monitoring
- 5 hours: Threshold evaluation and iteration planning

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, funnels, cohorts | Free up to 1M events + 1M feature flag requests/month; paid ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app messages, product tours, upgrade prompts | Advanced plan $85/seat/mo recommended for workflows + proactive campaigns; Early-stage program up to 90% off ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Lifecycle emails, churn nudges, upgrade emails | Free up to 1,000 contacts; paid from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Daily churn detection, intervention routing, experiment monitoring | Community Edition free (self-hosted); Cloud from €24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated monthly cost at this level:** $150-400/mo (Intercom Advanced + Loops paid + n8n Cloud), plus PostHog usage if exceeding free tier.

## Drills Referenced

- `ab-test-orchestrator` — designs, runs, and analyzes A/B tests on milestone variations using PostHog feature flags
- `churn-prevention` — detects pre-activation and post-activation churn signals and triggers tiered interventions
- `upgrade-prompt` — deploys contextual upgrade prompts at activation moments and limit-proximity events
