---
name: keyboard-shortcuts-promotion-scalable
description: >
  Power User Features — Scalable Automation. Roll out to all users, personalize hint
  delivery by persona and workflow pattern, A/B test hint copy and timing, and scale
  to >=500 users with >=25% shortcut ratio sustained over 2 months.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: ">=25% average shortcut ratio across 500+ active users sustained for 4+ consecutive weeks"
kpis: ["Shortcut ratio across entire user base", "Shortcut ratio by persona segment", "Hint conversion rate by variant", "Total time saved per week (aggregate)", "Retention lift (shortcut users vs non-shortcut users)"]
slug: "keyboard-shortcuts-promotion"
install: "npx gtm-skills add product/retain/keyboard-shortcuts-promotion"
drills:
  - ab-test-orchestrator
  - tooltip-targeting-automation
  - dashboard-builder
---

# Power User Features — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Shortcut promotion running for all eligible users across the entire user base. Personalized by persona and workflow pattern. Sustained average shortcut ratio of >=25% across 500+ active users for 4+ consecutive weeks. A/B testing producing measurable improvements to hint conversion rates.

## Leading Indicators

- Shortcut ratio climbing steadily as new user cohorts enter the promotion system
- A/B test variants producing statistically significant winners on hint conversion rate
- Persona-specific hint strategies showing differentiated adoption patterns
- Retention rate for users with shortcut ratio >25% is measurably higher than users with ratio <5%
- Aggregate time saved per week growing as user base scales
- Stalled-user interventions converting at least 10% of stalled users per cycle

## Instructions

### 1. Roll out to 100% and segment by persona

Remove the 50/50 feature flag from Baseline. Enable shortcut hints for all eligible users. Using the `tooltip-targeting-automation` drill, build persona-specific hint strategies:

**Technical builders:** Surface advanced shortcuts first (multi-key combinations, custom shortcuts). These users expect power-user features. Hint copy should emphasize speed: "0.5s vs 3s. Cmd+Shift+P every time."

**Team leads / managers:** Surface shortcuts related to navigation, search, and overview actions. These users move between contexts frequently. Hint copy should emphasize flow: "Stay in your flow. Cmd+K gets you anywhere without clicking."

**Casual / infrequent users:** Surface only the 2-3 most universal shortcuts (search, submit, undo). Do not overwhelm. Hint copy should emphasize simplicity: "One keystroke. That is all."

Using PostHog cohorts and Intercom user properties, assign each user a persona and deliver the corresponding hint strategy. The n8n daily pipeline handles the assignment and Intercom property updates.

### 2. A/B test hint copy and timing

Run the `ab-test-orchestrator` drill to systematically test variations:

**Test 1: Hint copy framing**
- Control: "Pro tip: Press Cmd+K to search instantly"
- Variant A: "Cmd+K. 3 seconds faster, every time." (quantified benefit)
- Variant B: "Your fastest colleagues all use Cmd+K" (social proof)
- Metric: hint-to-trial conversion rate
- Sample: 200+ per variant, 2 weeks

**Test 2: Hint timing**
- Control: Show hint immediately after mouse action
- Variant A: Show hint after the user performs the same mouse action 3+ times in a session (frustration signal)
- Variant B: Show hint at session start as a "tip of the day" before any action
- Metric: hint-to-habitual conversion rate (not just trial — habitual usage)
- Sample: 200+ per variant, 2 weeks

**Test 3: Hint format**
- Control: Tooltip near the clicked element
- Variant A: Subtle inline text appearing next to the element: "or press Cmd+K"
- Variant B: Brief animation showing the keyboard shortcut keys after the mouse action completes
- Metric: hint dismissal rate (lower is better) AND hint-to-trial conversion rate
- Sample: 200+ per variant, 2 weeks

Run tests sequentially (one at a time). Implement each winner before starting the next test. Log all results in PostHog and the weekly adoption report.

### 3. Build the "time saved" reinforcement surface

Create an in-product efficiency dashboard visible to each user showing their personal shortcut stats:

- Shortcuts learned: X / Y total
- Time saved this week: Z minutes
- Shortcut ratio trend (last 4 weeks as a sparkline)
- "Next shortcut to learn" with a try-it-now CTA

Instrument this surface with PostHog events:
```javascript
posthog.capture('efficiency_dashboard_viewed', {
  shortcuts_learned: count,
  time_saved_minutes: savedMinutes,
  shortcut_ratio: ratio
});
```

This reinforcement loop makes shortcut adoption feel like personal progress, increasing stickiness. Users who engage with their efficiency stats show 2-3x higher shortcut adoption rates.

**Human action required:** Review the efficiency dashboard design and copy before shipping. Ensure the "time saved" calculation is accurate and not inflated — users will lose trust if the numbers feel wrong.

### 4. Scale the stalled-user intervention system

Using the `dashboard-builder` drill's stalled-user detection, expand the interventions for scale:

- For **hint-ignored** users at scale: Instead of just a Loops email, build a 3-message drip sequence spaced 7 days apart. Message 1: GIF showing top shortcuts. Message 2: "Users who use shortcuts retain 40% longer" (if you have this data). Message 3: Link to an interactive shortcut tutorial. If all 3 fail, mark as permanently opted-out of shortcut promotion.
- For **plateaued** users at scale: Build a "shortcut challenge" — a weekly prompt to try one new shortcut. Track completion. Users who complete 4 weekly challenges graduate from the promotion system entirely.

### 5. Measure retention correlation

Using PostHog, build a critical analysis: does shortcut adoption actually improve retention?

Create two cohorts:
- `shortcut-adopters`: shortcut ratio >= 25% for 4+ weeks
- `shortcut-non-adopters`: shortcut ratio < 5% for 4+ weeks, despite being eligible

Compare:
- 30-day retention rate
- 60-day retention rate
- Session frequency (sessions per week)
- Feature breadth (distinct features used per week)

If shortcut adopters retain significantly better (10+ percentage point difference), this is the business case for continued investment. Surface this data in the weekly report.

**Important:** Correlation is not causation. Users who adopt shortcuts may simply be more engaged overall. But the correlation still justifies the promotion investment — if shortcut hints accelerate the behavior that correlated users already exhibit, the system is working.

### 6. Evaluate against threshold

After 2 months, measure:

**Pass threshold: >= 25% average shortcut ratio across 500+ active users, sustained for 4+ consecutive weeks.**

Also verify:
- A/B tests produced at least 1 statistically significant improvement
- Persona-specific strategies show differentiated adoption rates (not identical across segments)
- Retention correlation analysis is complete and documented
- Stalled-user system is processing and converting stalled users

If PASS: Document the complete system configuration (winning hint copy, timing, persona strategies, intervention sequences). Prepare for Durable handoff. The system should run with zero human intervention at this point.

If FAIL at <500 users but ratio is good: The system works but the eligible user pipeline is too narrow. Broaden eligibility criteria (reduce tenure requirement, lower session frequency threshold). Re-evaluate in 4 weeks.

If FAIL on ratio at 500+ users: The promotion is reaching users but not converting at scale. Analyze by persona — if one segment drags down the average, consider excluding that segment or building a fundamentally different approach for them. Re-run.

## Time Estimate

- 8 hours: persona segmentation, tooltip targeting automation, 100% rollout
- 12 hours: 3 sequential A/B tests (design, setup, monitoring, analysis)
- 8 hours: efficiency dashboard build, instrumentation, reinforcement surface
- 6 hours: stalled-user intervention expansion, shortcut challenge build
- 6 hours: retention correlation analysis, threshold evaluation, documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, cohorts, feature flags, dashboards, retention analysis | Free tier may be exceeded at 500+ users; Paid: $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Persona-targeted tooltips, product tours, in-app messages | Essential: $29/seat/mo; Proactive Support Plus: $349/mo for high-volume messaging ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Stalled-user drip sequences | Paid from $49/mo based on contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Daily persona assignment, stalled-user detection, weekly reporting | Self-hosted: free; Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated play-specific cost at this level:** $75-400/mo depending on Intercom plan and PostHog event volume

## Drills Referenced

- `ab-test-orchestrator` — systematic A/B testing of hint copy, timing, and format
- `tooltip-targeting-automation` — persona-specific tooltip delivery with usage-based targeting
- `dashboard-builder` — adoption funnel tracking, stalled-user interventions at scale, retention correlation analysis
