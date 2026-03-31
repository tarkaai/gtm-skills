---
name: personalized-onboarding-path-scalable
description: >
  Adaptive Onboarding Paths — Scalable Automation. Expand from 2 to 5+
  persona paths with automated classification, multi-channel delivery
  (tours + email + in-app messages), and systematic A/B testing per
  persona to find the optimal path for each segment.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "Activation rate >= 55% across 500+ users with 5+ persona paths, each persona within 10pp of the best-performing persona"
kpis: ["Activation rate by persona", "Tour completion rate by persona", "Email click-to-activation rate by persona", "Persona classification accuracy", "A/B test win rate", "Time to activation by persona"]
slug: "personalized-onboarding-path"
install: "npx gtm-skills add product/onboard/personalized-onboarding-path"
drills:
  - onboarding-persona-scaling
  - ab-test-orchestrator
---

# Adaptive Onboarding Paths — Scalable Automation

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Scale personalized onboarding from 2 personas to 5+ with automated classification, multi-channel delivery, and systematic per-persona optimization. Every persona path spans product tours, email sequences, and contextual in-app messages simultaneously. Automated persona detection replaces manual signup-form tagging. Systematic A/B testing brings the weakest personas up to parity with the strongest. Pass threshold: activation rate >= 55% across 500+ users with 5+ active persona paths, no single persona more than 10pp below the best-performing persona.

## Leading Indicators

- Automated persona classification assigns a `persona_type` to >= 95% of signups without relying on a signup-form dropdown (inferred classification working)
- 3rd and 4th persona tours achieve >= 50% tour completion rate within their first 2 weeks (new personas are not significantly worse than originals)
- Per-persona email sequences achieve open rate >= 40% and click rate >= 8% (persona-specific subject lines and CTAs outperform generic)
- At least 1 completed A/B test per persona within the first month (testing velocity)
- Comparative PostHog dashboard shows all 5+ personas with populated funnel data (no data gaps)

## Instructions

### 1. Discover new persona segments and build automated classification

Run the `onboarding-persona-scaling` drill. This is the core drill for this level. It produces:

**New persona discovery:**
- Analyze PostHog cohort data from Baseline to find 2-3 additional persona segments where the generic fallback tour underperforms. Each new persona must have >= 50 historical users and a measurably different activation path from existing personas.
- Example: Baseline had "Solo Creator" and "Team Lead." Scalable adds "Technical Builder" (API-first users), "Marketer" (campaign-focused), and "Sales User" (pipeline-focused). Each has a different fastest path to activation.

**Automated classification:**
- Build an n8n classification workflow triggered by `signup_completed`. The workflow collects signals (role field, email domain enrichment, company size, signup source UTMs, referral path) and applies if/else classification rules to assign `persona_type`.
- Write `persona_type` and `persona_confidence` ("explicit", "inferred", or "default") to both PostHog and Intercom.
- Target: >= 95% of signups classified within 60 seconds, <= 5% falling to the "default" generic path.

**Per-persona multi-channel paths:**
- Build 3 new Intercom product tours (one per new persona), each 3-5 steps focused on that persona's activation action. Use `intercom-product-tours`.
- Build 3 new Loops email sequences (5 emails each) with persona-specific subject lines, CTAs, and use case examples. Use `loops-sequences` and `loops-audience`.
- Add contextual in-app messages for each new persona's top stall point. Use `intercom-in-app-messages`.
- Set up PostHog feature flag `onboarding-persona-v2` with one variant per persona (5+ variants). Route based on `persona_type`.

**Per-persona funnels and dashboards:**
- Build one PostHog funnel per persona: `signup → classified → tour_started → tour_completed → activated`
- Build a comparative dashboard showing all personas side by side: activation rate, time to activation, tour completion, email open rate, email click rate.

### 2. Run systematic A/B tests per persona

Run the `ab-test-orchestrator` drill to test variations for each persona path, starting with the worst-performing persona.

**Testing priority order:**
1. The persona with the lowest activation rate gets tested first
2. For each persona, test the element with the biggest drop-off in its funnel

**Test types (run one per persona at a time):**

| Test | Hypothesis | Variants | Minimum sample |
|------|-----------|----------|---------------|
| Tour length | Shorter tours reduce drop-off | 3-step vs 5-step tour | 100 per variant |
| First action | Simpler initial milestone increases completion | Easy action vs current action | 100 per variant |
| Channel priority | Some personas respond better to email-first vs tour-first | Tour triggers immediately vs email triggers first (tour delayed 24h) | 100 per variant |
| Email CTA | More specific CTAs increase click rate | Generic CTA ("Get started") vs persona-specific CTA ("Import your first data set") | 200 per variant |
| Stall nudge timing | Earlier nudges prevent drop-off | 12h stall nudge vs 24h stall nudge | 100 per variant |

For each test:
1. Form a hypothesis with predicted outcome and reasoning
2. Calculate required sample size using PostHog's experiment calculator
3. Create the PostHog experiment with feature flag variants
4. Run for the calculated duration (minimum 7 days)
5. Evaluate with `experiment-evaluation` criteria: statistical significance at 95%, practical significance (>= 3pp improvement to be worth the complexity)
6. Implement winners, document losers with learnings

**Target:** Complete at least 1 test per persona in the first month. 2 tests per persona by end of month 2.

### 3. Monitor and converge persona performance

Using the comparative PostHog dashboard from Step 1, track the gap between the best-performing and worst-performing persona each week.

**Weekly review checklist (15 minutes):**
1. Which persona has the lowest activation rate this week?
2. What is the gap between best and worst persona?
3. Are any personas below the 55% overall threshold?
4. Are A/B tests running on schedule? Any stalled tests?
5. Has the persona distribution shifted? (If a new persona suddenly dominates signups, its path needs more investment.)

**Convergence target:** All personas within 10pp of each other. If persona A activates at 65% and persona C at 48%, persona C's path needs 2-3 more rounds of testing.

### 4. Evaluate against threshold

After 2 months of scaled operation with 500+ users onboarded through the system:

- **Overall activation rate >= 55%** across all persona paths combined
- **500+ users processed** through the personalized system (sufficient volume for statistical confidence per persona)
- **5+ active persona paths** (not counting the "default" fallback)
- **Persona parity:** No single persona more than 10pp below the best-performing persona
- **Classification accuracy:** >= 90% match between automated classification and actual behavior (check by comparing assigned persona with which activation metric the user actually completed)

Decision tree:
- **Pass:** Proceed to Durable. The multi-persona system works at scale. Focus shifts from building paths to autonomous optimization.
- **Marginal (overall >= 55% but one persona is 12+pp behind):** Extend by 2 weeks. Run 1 more A/B test on the lagging persona. If it improves to within 10pp, proceed.
- **Fail (overall < 55% or < 5 personas active):** Diagnose. If overall rate is low, the persona segments may be wrong — re-cluster from scratch. If < 5 personas, some segments may be too small — merge the smallest segment with its closest neighbor.

## Time Estimate

- 10 hours: Persona discovery and segment definition (PostHog cohort analysis, historical data mining)
- 8 hours: Automated classification workflow in n8n (rules, enrichment, testing)
- 15 hours: Building 3 new persona tours in Intercom (5 hours each including content, targeting, and testing)
- 10 hours: Building 3 new persona email sequences in Loops (15 emails total)
- 8 hours: A/B test design, setup, and analysis (2 tests per persona minimum)
- 5 hours: Dashboard and funnel setup in PostHog
- 4 hours: Weekly monitoring and review (30 min/week x 8 weeks)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Per-persona funnels, experiments, feature flags, dashboards, session recordings | Free tier likely sufficient; paid at $0.00005/event above 1M — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | 5+ persona-specific product tours + contextual in-app messages | Essential: $29/seat/mo + Proactive Support Plus: $99/mo (500 messages; overage charges above 500) — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | 5+ persona-specific email sequences | $49/mo for up to 5K contacts; scales with contact count — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Classification workflow + event routing (enrollment, sync, exit) | Pro: €60/mo (10K executions); self-hosted: free — [n8n.io/pricing](https://n8n.io/pricing/) |

**Estimated monthly cost at this level:** $200-450/mo (PostHog may push past free tier with 500+ users' events; Intercom $128-200 with message overage; Loops $49; n8n $60)

## Drills Referenced

- `onboarding-persona-scaling` — discovers new persona segments, builds automated classification, creates multi-channel per-persona paths (tours + emails + messages), and sets up comparative dashboards
- `ab-test-orchestrator` — designs, runs, and evaluates A/B tests per persona to systematically improve the weakest onboarding paths
