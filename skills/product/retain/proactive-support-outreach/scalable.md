---
name: proactive-support-outreach-scalable
description: >
  Proactive Support Outreach — Scalable Automation. Expand coverage to all struggle
  workflows, add multi-channel routing, and A/B test outreach variants for maximum resolution.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Email, Direct"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥45% engagement at 500+ users/month, ≥20pp retention lift"
kpis: ["Outreach engagement rate", "Resolution rate", "30-day retention lift", "Ticket deflection", "Workflow coverage"]
slug: "proactive-support-outreach"
install: "npx gtm-skills add product/retain/proactive-support-outreach"
drills:
  - ab-test-orchestrator
  - support-ticket-analysis
  - engagement-alert-routing
---

# Proactive Support Outreach — Scalable Automation

> **Stage:** Product → Retain | **Motion:** LeadCaptureSurface | **Channels:** Email, Direct

## Outcomes

Baseline proved the pipeline works for the top 5 struggle workflows. Scalable expands to all significant struggle patterns, adds sophisticated multi-channel routing, and runs systematic A/B tests to maximize resolution rates. The 10x multiplier comes from coverage breadth (catching every struggling user, not just common patterns) and outreach precision (the right message, right channel, right timing for each struggle type).

Success = at least 45% engagement rate sustained at 500+ users per month, AND at least 20pp retention lift vs. non-outreached users.

## Leading Indicators

- Workflow-to-help-resource mapping covers 90%+ of detected struggle patterns
- A/B tests producing statistically significant winners within 2-week cycles
- Resolution rate improving for previously low-resolution workflows
- Support ticket volume declining as proactive outreach absorbs common questions
- Time-to-resolution shortening as help content improves
- No increase in outreach fatigue signals (unsubscribes, dismissals, negative replies)

## Instructions

### 1. Expand struggle detection coverage

Review the `struggle-signal-detection` drill output from the last 4 weeks. Identify:

- **Uncovered workflows:** Struggle patterns where `primary_stuck_workflow` maps to a workflow with no help resource. Build help resources (articles, videos, deep links) for every workflow that appears 5+ times in the detection log.
- **New signal types:** Product areas generating struggle that the current detection does not capture. Common gaps: mobile-specific struggles, API integration errors, team administration confusion, billing/plan confusion. Add new PostHog events for any gaps found.
- **Detection threshold tuning:** Review false positive and false negative rates from the Baseline data. Adjust the scoring weights in the struggle query. If a signal type generates many false positives (e.g., rage clicks on a known-slow page that actually loads fine), reduce its weight or add exclusion rules.

Target: the struggle-to-help-resource mapping covers 90%+ of detected `primary_stuck_workflow` values (measured by volume, not unique workflow count).

### 2. Build support-informed outreach content

Run the `support-ticket-analysis` drill. Classify the last 90 days of Intercom tickets and extract:

- The most common questions by product area (these become proactive outreach content)
- Recurring confusion patterns (map these to new struggle signals if not already detected)
- Successful resolution approaches from support agents (adopt these as outreach message templates)
- Feature requests disguised as support tickets (route these to product feedback, not outreach)

For each high-volume support topic that matches a detected struggle workflow, create an outreach variant that uses the language and resolution steps that support agents found most effective. This is the difference between generic help content and content that actually resolves the problem.

### 3. Add multi-channel routing optimization

Run the `engagement-alert-routing` drill adapted for struggle tiers. Build sophisticated routing that considers:

- **Channel preference by workflow:** Some struggles are best resolved by an in-app message (visual/UI confusion) while others need an email with detailed steps (data formatting, API integration). Analyze which channel produces higher resolution rates for each workflow type and route accordingly.
- **Time-of-day optimization:** Analyze when outreached users are most likely to engage. Route in-app messages to display during the user's typical active hours. Send emails during the time window with highest open rates for their timezone.
- **Account value weighting:** Higher-MRR accounts get more channels simultaneously. A $5K/mo account showing severe struggle gets in-app + email + human outreach in parallel, not sequenced.
- **Re-detection escalation:** If a user is re-flagged for the same workflow within 14 days of previous outreach, the previous outreach did not work. Automatically escalate: try a different channel, offer a different fix, or route to human.

### 4. Run systematic A/B tests on outreach

Run the `ab-test-orchestrator` drill targeting these outreach variables:

**Test 1: Message framing**
- Control: "Quick tip for {workflow}" (proactive tip framing)
- Variant A: "New: easier {workflow}" (product update framing)
- Variant B: "{workflow} guide" (educational framing)
- Success metric: Engagement rate (click + action taken)
- Run for 2 weeks or 200+ users per variant

**Test 2: In-app message timing**
- Control: Display immediately on next login
- Variant A: Display after 30 seconds (user has oriented themselves)
- Variant B: Display only when user navigates to the relevant product area
- Success metric: Resolution rate (struggle score drops below 10 within 7 days)

**Test 3: Help content depth**
- Control: 2-3 sentence quick fix + help article link
- Variant A: Step-by-step walkthrough embedded in the message (no click required)
- Variant B: Video walkthrough thumbnail + play button
- Success metric: Self-serve resolution rate

**Test 4: Follow-up cadence**
- Control: Day 0 + Day 3 follow-up
- Variant A: Day 0 only (no follow-up)
- Variant B: Day 0 + Day 2 + Day 5
- Success metric: Resolution rate balanced against unsubscribe rate

After each test reaches significance, implement the winner and move to the next test. Log all test results with `posthog-custom-events` for the Durable level's optimization loop.

### 5. Scale human outreach for critical tier

For critical-tier users, build a structured outreach process:

1. The agent prepares a briefing for the account owner: user's struggle context, specific errors encountered, help resources they already tried, session recording link, recommended talking points
2. The account owner has a pre-written email they can personalize in under 2 minutes
3. If the account owner does not act within 24 hours, the agent sends an automated escalation email to the user with enhanced help content and a direct calendar booking link for a screen-share session
4. Track: time from detection to human contact, resolution outcome, user satisfaction

Target: 100% of critical-tier users receive human contact within 48 hours.

### 6. Evaluate against threshold

Measure against: ≥45% engagement at 500+ users/month AND ≥20pp retention lift.

Track weekly across all tiers and workflows:
- Total users flagged and outreached
- Engagement rate by tier, channel, and workflow
- Resolution rate by tier and workflow
- 30-day retention lift vs. non-outreached users
- Support ticket deflection (estimated tickets avoided)
- A/B test results and improvements adopted

If PASS: Proceed to Durable.
If FAIL on engagement at scale: The help content is not scaling — new workflows need better resources. Focus on the lowest-resolution workflows.
If FAIL on retention lift: Users are engaging but not retaining. The struggles may indicate product gaps that outreach cannot fix. Feed workflow-level resolution data to the product team as prioritized bug/UX fix requests.

## Time Estimate

- 10 hours: Expand struggle detection coverage and tune scoring
- 12 hours: Run support-ticket-analysis and build support-informed outreach content
- 10 hours: Build multi-channel routing optimization
- 20 hours: Design, run, and evaluate 4 A/B tests (5 hours each, staggered)
- 5 hours: Scale human outreach process
- 3 hours: Evaluate results and document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Struggle detection, A/B testing, funnels, session recordings | Free tier: 1M events/mo; Paid: from $0 — https://posthog.com/pricing |
| Intercom | In-app messages, support ticket analysis, contextual help | Starter: $74/mo; Pro varies — https://www.intercom.com/pricing |
| Loops | Triggered emails, follow-up sequences, A/B variants | Starter: $49/mo — https://loops.so/pricing |
| n8n | Routing logic, A/B test orchestration, scheduling | Cloud: from $24/mo — https://n8n.io/pricing |
| Attio | CRM records, human routing, task management | Free tier; Pro: $34/user/mo — https://attio.com/pricing |

## Drills Referenced

- `ab-test-orchestrator` — Run systematic A/B tests on outreach framing, timing, content depth, and follow-up cadence
- `support-ticket-analysis` — Extract support ticket patterns to build better outreach content and detect new struggle signals
- `engagement-alert-routing` — Multi-channel routing logic adapted for struggle tiers and workflow types
