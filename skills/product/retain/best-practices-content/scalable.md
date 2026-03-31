---
name: best-practices-content-scalable
description: >
  In-App Best Practices — Scalable Automation. Personalize best-practices delivery
  across 5+ behavioral personas and product maturity tiers, systematically A/B test
  content variants, and expand the card library to 15+ cards serving 500+ users.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Content"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥30% engagement rate sustained across 500+ users in 5+ personas with ≥5pp retention lift"
kpis: ["Overall engagement rate", "Per-persona engagement rate", "Experiment win rate", "Card library size", "Retention lift by persona"]
slug: "best-practices-content"
install: "npx gtm-skills add product/retain/best-practices-content"
drills:
  - best-practices-personalization
  - ab-test-orchestrator
  - content-repurposing
---

# In-App Best Practices — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Content

## Outcomes

30% or more overall engagement rate sustained across 500+ users spanning 5+ behavioral personas, with at least 5 percentage points retention lift per persona. The 10x multiplier comes from personalization: instead of showing the same tips to everyone, each persona gets tips that match their specific role, usage pattern, and product maturity. The card library expands from 5-8 cards to 15+ cards covering all personas and maturity tiers.

## Leading Indicators

- New personas activating without requiring manual content creation (the personalization pipeline handles variant generation)
- Per-persona engagement rates clustering above 25% (no single persona dragging the average down)
- A/B test velocity: at least 2 experiments completed per month with documented outcomes
- Card library growing by 2-3 new cards per month from ongoing session recording analysis
- Content repurposing producing email digest and web versions of top-performing cards without additional effort
- Persona migration tracking shows users moving from Casual to Builder/Power (tips are driving deeper usage)

## Instructions

### 1. Deploy persona-based personalization

Run the `best-practices-personalization` drill to transform the generic card library into a per-persona system:

1. **Define behavioral personas from PostHog data.** Create 5 cohorts based on actual usage patterns:
   - **Builders:** Create 5+ items/week, spend 70%+ of time in the editor
   - **Reviewers:** View 10+ items/week, primarily use commenting and viewing features
   - **Admins:** Visit settings 2+ times/week, manage team permissions and integrations
   - **Power users:** Use 8+ distinct features/week, active 5+ days/week
   - **Casual users:** Log in 1-2 times/week, use 2-3 features

2. **Map existing cards to personas.** Each card gets a primary persona and up to 2 secondary personas based on which behavior pattern the card teaches. Workflow tips map to Builders, collaboration tips to Reviewers, configuration tips to Admins.

3. **Generate persona-specific copy variants.** For each card-persona pair, use the Anthropic API to rewrite the hook and opening sentence to resonate with the persona's priorities. The steps stay identical; only the framing changes.

4. **Layer product maturity tiers.** Segment users into Novice (weeks 1-2), Intermediate (weeks 3-8), and Advanced (week 9+). Combine with persona to create the delivery matrix: a Week-1 Builder sees foundational workflow tips, not advanced automation tips.

5. **Update the n8n delivery workflow.** When selecting which card to show a user, filter by persona match and maturity tier, then select the persona-specific copy variant.

Sync persona assignments to Intercom as custom user properties for targeted message delivery.

### 2. Run systematic A/B experiments

Run the `ab-test-orchestrator` drill to test variations across the content system:

**Month 1 experiments:**
- **Hook framing test:** Benefit-led hooks ("Save 2 minutes per task") vs. curiosity-led hooks ("Most users miss this shortcut") — run across all personas, measure click-through rate
- **Delivery timing test:** Show tips immediately on login vs. show tips after the user completes a related action — run in the Builder persona, measure completion rate

**Month 2 experiments:**
- **Format test:** Text-only cards vs. cards with animated GIF showing the practice — run across all personas, measure completion rate
- **Frequency test:** 1 tip per day vs. 1 tip every 3 days — run in the Casual persona, measure engagement rate and dismissal rate

For each experiment:
1. Form the hypothesis with expected impact
2. Calculate required sample size (minimum 200 per variant)
3. Set up the PostHog feature flag split
4. Run for the calculated duration without early peeking
5. Evaluate: adopt the winner, document the learning, move to the next experiment

### 3. Expand the card library through content repurposing

Run the `content-repurposing` drill adapted for best-practices content:

1. **Mine new patterns:** Re-run session recording analysis monthly. As the product evolves, new power-user behaviors emerge. Target adding 2-3 new cards per month.
2. **Repurpose top-performing cards.** Cards with >30% completion rate become:
   - Short video tutorials (60-second screen recordings demonstrating the practice)
   - Email digest content for the weekly best-practices email
   - Blog posts on the web knowledge base with SEO-optimized titles
   - Intercom Help Center featured articles
3. **Retire underperforming cards.** Cards with <10% completion rate after 30 days of delivery get reviewed. If a rewrite does not improve performance, retire the card and replace it.

Target: library of 15+ active cards covering all 5 personas and 3 maturity tiers by the end of Month 2.

### 4. Monitor per-persona performance

Review weekly using the PostHog personalization matrix dashboard:

| Signal | Action Threshold |
|--------|-----------------|
| Persona engagement rate <20% for 2 weeks | Pause that persona's delivery, test new card-persona mappings |
| Persona dismissal rate >40% | Reduce frequency for that persona, test subtler formats |
| Persona exhaustion >60% of eligible users already shown all cards | Prioritize new card creation for that persona |
| Overall engagement rate declining | Check if a new persona is dragging the average — isolate and fix |
| Experiment win rate <25% | Hypotheses are too incremental — test bigger changes |
| Retention lift for any persona <3pp | The tips may not be actionable enough for that persona — rewrite with more specific steps |

### 5. Evaluate against threshold

At the end of 2 months, calculate:
- Overall engagement rate across all personas (target: >=30%)
- Total users reached across all personas (target: 500+)
- Number of active personas with >=25% engagement (target: 5)
- Retention lift per persona (target: >=5pp for each)

- **Pass:** Personalized best-practices delivery scales across personas without proportional effort. Each new persona launches via the established pipeline. Proceed to Durable for autonomous optimization.
- **Fail:** Identify which personas are underperforming. If most personas work but 1-2 fail, retire those and test alternative segmentation. If most fail, the personalization may be too granular — try 3 broader segments instead of 5 narrow ones.

## Time Estimate

- 15 hours: Persona definition, PostHog cohort creation, Intercom property sync, card-persona mapping
- 10 hours: Copy variant generation, maturity tier layering, delivery workflow updates
- 15 hours: A/B test design, execution, and analysis (4 experiments over 2 months)
- 10 hours: Content library expansion (monthly session recording analysis, new card creation, repurposing)
- 10 hours: Weekly performance reviews, persona optimization, documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Cohorts, feature flags, experiments, funnels, dashboards, session recordings | Free up to 1M events/mo; Growth from $0.00045/event — https://posthog.com/pricing |
| Intercom | Persona-targeted in-app messages, Help Center | ~$75-300/mo depending on MAU — https://www.intercom.com/pricing |
| Loops | Persona-specific email sequences and digests | Starter $49/mo for 5,000 contacts — https://loops.so/pricing |
| n8n | Persona-aware orchestration workflow | Free self-hosted; Cloud from $24/mo — https://n8n.io/pricing |
| Anthropic API | Copy variant generation, new card content | ~$10-20/mo — https://www.anthropic.com/pricing |

**Play-specific cost:** ~$100-400/mo (Intercom and Loops scale with user count)

## Drills Referenced

- `best-practices-personalization` — segment users into behavioral personas, generate persona-specific copy variants, layer product maturity tiers
- `ab-test-orchestrator` — run systematic experiments on hooks, timing, format, and frequency
- `content-repurposing` — expand the card library and repurpose top performers into video, email, and web formats
