---
name: best-practices-content-smoke
description: >
  In-App Best Practices — Smoke Test. Mine power-user behavior from session recordings,
  produce 5 best-practices content cards ranked by retention correlation, and deliver
  them manually to a test group of 20-50 users to validate engagement.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Content"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥35% of test group engages with at least one best-practice card (clicks CTA)"
kpis: ["Card click-through rate", "Card completion rate", "Retention lift signal"]
slug: "best-practices-content"
install: "npx gtm-skills add product/retain/best-practices-content"
drills:
  - threshold-engine
---

# In-App Best Practices — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Content

## Outcomes

35% or more of a 20-50 user test group engages with at least one best-practice card within 7 days. "Engages" means the user clicks the card's CTA (not just views it). This proves that contextual best-practices content drives measurable behavior change, not just impressions. A secondary signal: at least 2 users complete the recommended practice within 24 hours of seeing the card.

## Leading Indicators

- Card impression rate above 80% of the test group (the delivery mechanism works and users see the cards)
- Click-through rate per card above 20% (the hook copy is compelling enough to interrupt the workflow)
- At least 1 user completes the practice and returns to use it again within 7 days (the practice delivers real value)
- Dismissal rate below 40% (the cards are not perceived as intrusive)

## Instructions

### 1. Build the initial content card library

Run the the best practices content pipeline workflow (see instructions below) drill to produce 5 best-practices content cards:

1. Define a "power users" cohort in PostHog: top 10% by session frequency and feature breadth
2. Watch 20-30 session recordings from power users. Document behavior patterns that average users do not follow: workflow sequences, keyboard shortcuts, configuration choices, non-obvious feature combinations
3. For each pattern, query PostHog to measure the retention lift: compare 30-day retention of users who exhibit the pattern versus users who do not
4. Rank patterns by retention lift. Select the top 5 as your first content cards
5. Structure each card with: title (action verb + outcome), hook (under 80 characters), 2-3 steps with exact UI element names, CTA deep link, trigger event (when to show), exclude event (when not to show)
6. Generate card body text via the Anthropic API. Target: scannable in 30 seconds, benefit-led, Grade 8 reading level
7. Publish cards to Intercom Help Center and instrument PostHog tracking: `best_practice_shown`, `best_practice_clicked`, `best_practice_completed`, `best_practice_dismissed`

**Human action required:** Review each card for accuracy. Verify all UI element names match the current product. Test each deep link. Remove any tip that is obvious to experienced users. Approve the 5 cards for delivery.

### 2. Deliver to a test group

Select 20-50 active users who have been on the product for at least 7 days and who exhibit at least one `trigger_event` for the cards you created. Manually target them in Intercom with the relevant in-app messages. Do not automate delivery yet — this is a manual test.

Deliver one card per user per day, starting with the highest-retention-lift card. If a user is eligible for multiple cards, prioritize by retention lift.

### 3. Monitor for 7 days

Track daily in PostHog:
- How many users in the test group saw each card (`best_practice_shown`)
- How many clicked the CTA (`best_practice_clicked`)
- How many completed the practice (`best_practice_completed`)
- How many dismissed (`best_practice_dismissed`)
- Session recordings of users who clicked but did not complete — identify where they got stuck

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure against: 35% of test group clicked at least one card CTA within 7 days.

- **Pass (>=35%):** Best-practices content drives engagement. The content resonates and the delivery surface works. Proceed to Baseline to prove it holds with always-on automation.
- **Fail (<35%):** Diagnose: Were cards shown? (Check impression rate — if below 80%, the targeting or placement is wrong.) Did users see but dismiss? (Check dismissal rate — if above 50%, the hook copy needs rewriting.) Did users click but not complete? (The steps may be unclear or the deep link may be broken.) Fix the weakest step and re-run with a fresh test group.

## Time Estimate

- 2 hours: Session recording analysis, behavior pattern identification, retention lift queries
- 1.5 hours: Card content creation (structure, copy generation, review), Intercom Help Center publishing
- 0.5 hours: PostHog event instrumentation and test group selection
- 0.5 hours: Manual delivery setup in Intercom
- 0.5 hours: 7-day monitoring and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Session recordings, cohorts, custom events, retention queries | Free up to 1M events/mo and 5K recordings/mo — https://posthog.com/pricing |
| Intercom | In-app message delivery and Help Center hosting | Included in existing plan — https://www.intercom.com/pricing |
| Anthropic API | Card body text generation | ~$1-2 for 5 cards — https://www.anthropic.com/pricing |

**Play-specific cost:** Free (uses existing stack; Anthropic API cost negligible)

## Drills Referenced

- the best practices content pipeline workflow (see instructions below) — mine power-user behavior, produce structured content cards ranked by retention lift
- `threshold-engine` — evaluate 7-day engagement rate against the 35% threshold
