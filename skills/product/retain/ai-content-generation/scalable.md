---
name: ai-content-generation-scalable
description: >
  AI Content Assistant — Scalable Automation. Run systematic A/B tests on prompts and UX,
  build churn prevention around AI content usage signals, and configure expansion triggers
  to achieve 10x adoption without proportional effort.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=35% AI content adoption sustained at 500+ active users with acceptance rate >=60%"
kpis: ["AI content adoption rate at scale (>=35% at 500+ users)", "Acceptance rate (>=60%)", "Churn save rate (at-risk AI users re-engaged / at-risk AI users identified)", "Expansion trigger conversion (upgrade prompts shown to AI power users -> upgrades completed)", "Experiment velocity (A/B tests completed per month)"]
slug: "ai-content-generation"
install: "npx gtm-skills add product/retain/ai-content-generation"
drills:
  - ab-test-orchestrator
  - churn-prevention
  - upgrade-prompt
---

# AI Content Assistant — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Find the 10x multiplier: scale AI content adoption from a proven baseline to 500+ active users without proportional manual effort. Run systematic experiments on content quality, UX, and user segmentation. Build automated churn prevention that uses AI content usage drop-off as an early warning signal. Configure expansion triggers for AI power users.

Pass threshold: >=35% AI content adoption sustained at 500+ active users, AND acceptance rate >=60%.

## Leading Indicators

- At least 2 A/B tests completed per month with statistically significant results
- Content quality (acceptance rate) improves or holds steady as user base grows -- no quality degradation at scale
- Churn prevention interventions achieve >=20% save rate for at-risk AI content users
- At least 1 prompt optimization experiment per content type completed in the first month
- Expansion triggers show >=5% conversion rate (upgrade prompt shown -> upgrade completed)
- AI content non-adopters receiving re-targeting messages adopt at >=10% rate

## Instructions

### 1. Launch systematic content quality testing

Run the `ab-test-orchestrator` drill in combination with the the ai content prompt optimization workflow (see instructions below) drill to systematically improve output quality:

**Month 1 experiment plan:**
1. Identify the 3 content types with the highest generation volume from Baseline data
2. For each, run the the ai content prompt optimization workflow (see instructions below) drill to analyze rejection patterns and generate improvement hypotheses
3. Pick the top hypothesis for the highest-volume content type. Design and launch the first prompt A/B test:
   - Control: current system prompt
   - Variant: modified system prompt based on the hypothesis
   - Primary metric: clean acceptance rate (accepted without edits / total generated)
   - Secondary metrics: regeneration rate, edit rate, generation time
   - Minimum 100 generations per variant, minimum 7 days
4. Evaluate results using `experiment-evaluation`. If the variant wins, deploy the new prompt. If not, move to the next hypothesis.

**Month 2 experiment plan:**
1. Run prompt optimization for the remaining 2 high-volume content types
2. Test UX variations using PostHog feature flags:
   - Template-first vs blank-prompt-first entry point
   - Showing example outputs before generation vs not
   - One-click regenerate with suggested prompt modifications vs manual re-prompting
3. Run each UX test for minimum 14 days at 50/50 split

Track cumulative improvement: maintain a log of every experiment, its result, and the net impact on acceptance rate. Target: >=5pp acceptance rate improvement from Baseline by end of month 2.

### 2. Build AI-content-aware churn prevention

Run the `churn-prevention` drill with AI content-specific signals:

**Define AI content churn signals:**
- **Usage cliff**: User generated 5+ pieces of AI content in week N, then 0 in week N+1 (sudden drop)
- **Quality frustration**: 3+ rejections or regenerations in a single session (the AI is not meeting their needs)
- **Acceptance decline**: User's personal acceptance rate dropped from >=60% to <30% over 2 weeks (content quality degraded for their use case)
- **Feature abandonment**: User who was a regular AI content user (5+ generations per week for 3+ weeks) has not generated in 14+ days

**Build the detection workflow in n8n:**
1. Daily cron queries PostHog for users matching each signal
2. Score each user: usage cliff = 30 points, quality frustration = 25 points, acceptance decline = 20 points, feature abandonment = 40 points. Signals stack.
3. Route by score:
   - **Score 20-40 (low risk)**: Trigger an Intercom in-app message when they next visit the content creation area: "We've improved [content type] generation -- want to try again?" Link to the improved content type.
   - **Score 40-70 (medium risk)**: Send a Loops email with tips on getting better output: specific prompt examples, recommended content types, link to templates. Frame it as "Get more from AI content" not "We noticed you stopped using it."
   - **Score 70+ (high risk)**: Create an Attio task for product team review. Include the user's generation history, rejection reasons, and specific signals that triggered the alert.

### 3. Configure expansion triggers for AI power users

Run the `upgrade-prompt` drill targeting AI content power users:

**Identify expansion candidates:**
Using PostHog cohorts, define AI Power Users: 10+ generations per week, acceptance rate >=70%, used 3+ content types. These users are getting significant value from the AI feature.

**Design expansion prompts based on usage patterns:**
- **Generation limit approaching**: If the user's plan has a generation cap, trigger an in-app message at 80% usage: "You've generated [X] pieces of content this month. Upgrade to [plan] for unlimited AI generations." Show the specific number and what they would lose.
- **Team collaboration signal**: If the user generates content that gets shared or viewed by teammates, trigger: "Your AI content is being used by [N] teammates. Upgrade to team AI access so everyone can generate."
- **Advanced feature gate**: If the user attempts an advanced content type (e.g., long-form, multi-section) that is plan-gated, show the gate with a preview of what the output would look like.

**Measure expansion trigger effectiveness:**
Track `expansion_prompt_shown -> expansion_prompt_clicked -> upgrade_started -> upgrade_completed` as a PostHog funnel. Target >=5% end-to-end conversion. If below 5%, test different trigger thresholds, copy, or timing.

### 4. Scale non-adopter re-targeting

For users who have never tried AI content despite being active in content creation:

1. Using PostHog cohorts, identify active content creators who have never fired `ai_content_prompt_submitted`
2. Segment by content creation volume: high-volume creators get higher priority (more value from AI assistance)
3. Deploy a monthly re-targeting campaign via Intercom: contextual tooltip when they are actively creating content manually: "Want to speed this up? Try AI-assisted writing." Show next to their content editor.
4. Track conversion from tooltip shown to first AI generation. If >=10% adoption from re-targeting, maintain the campaign. If <10%, test different triggers (e.g., after the user spends 5+ minutes writing, or after they publish 3+ pieces in a week).

### 5. Evaluate against threshold

At the end of 2 months, measure:

1. **Adoption at scale**: Distinct users with >=1 AI content generation in trailing 14 days / total active users, with total active users >=500. Target: >=35%.
2. **Acceptance rate**: Total accepted / total generated, trailing 30 days. Target: >=60%.
3. **Churn save rate**: At-risk AI users who re-engaged within 14 days of intervention / total at-risk AI users identified. Track but no hard threshold.
4. **Experiment velocity**: Number of completed A/B tests (prompt or UX). Target: >=4 in 2 months.

If PASS: proceed to Durable. If adoption PASS but acceptance FAIL: content quality is not scaling. Focus prompt optimization on the content types dragging down the average. If adoption FAIL: discovery and re-targeting need more work. Analyze which user segments have the lowest adoption and design segment-specific interventions.

## Time Estimate

- 15 hours: Prompt optimization experiments -- analysis, hypothesis, A/B tests, evaluation (step 1)
- 12 hours: UX experiments -- design, implement, evaluate (step 1)
- 10 hours: Churn prevention -- signal definition, n8n workflow, intervention design (step 2)
- 8 hours: Expansion triggers -- cohort definition, prompt design, funnel tracking (step 3)
- 8 hours: Non-adopter re-targeting -- segmentation, campaign, measurement (step 4)
- 7 hours: Ongoing monitoring, evaluation, iteration (step 5)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, funnels, cohorts, dashboards | Free tier: 1M events/mo. https://posthog.com/pricing |
| n8n | Daily churn detection workflow, expansion trigger automation | Free (self-hosted) or $20/mo (cloud). https://n8n.io/pricing |
| Intercom | In-app messages, tooltips, expansion prompts | Starter: ~$39/seat/mo. https://www.intercom.com/pricing |
| Loops | Re-engagement emails, churn intervention emails | Free tier: 1,000 contacts. https://loops.so/pricing |
| Attio | Churn risk logging, experiment audit trail | Free tier: 3 users. https://attio.com/pricing |
| Anthropic API | Hypothesis generation for prompt experiments | Pay-per-use: ~$3/MTok input, ~$15/MTok output (Claude Sonnet). https://www.anthropic.com/pricing |

## Drills Referenced

- `ab-test-orchestrator` -- framework for running rigorous A/B tests on prompts and UX with proper sample sizing and statistical evaluation
- the ai content prompt optimization workflow (see instructions below) -- analyzes rejection patterns, generates prompt improvement hypotheses, and runs prompt A/B tests
- `churn-prevention` -- detects AI content usage drop-off signals and triggers tiered re-engagement interventions
- `upgrade-prompt` -- configures expansion triggers for AI power users based on usage patterns and plan limits
