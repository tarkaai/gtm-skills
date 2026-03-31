---
name: certification-program-scalable
description: >
  Product Certification Program — Scalable Automation. Expand to multi-tier certification
  with persona-based paths, cohort delivery, and A/B-tested tier transitions.
  Target ≥100 certifications per month with automated content refresh.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email, Content"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥100 certifications/month, ≥40% tier transition rate from Tier 1 to Tier 2"
kpis: ["Certifications per month", "Completion rate by persona", "Tier transition rate", "Cohort-over-cohort improvement", "Certified retention lift"]
slug: "certification-program"
install: "npx gtm-skills add product/onboard/certification-program"
drills:
  - ab-test-orchestrator
  - feature-adoption-monitor
---

# Product Certification Program — Scalable Automation

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Content

## Outcomes

The certification program serves multiple user personas across multiple tiers. Cohort-based delivery creates social proof and accountability. A/B testing optimizes every stage of the funnel. The program produces ≥100 certified users per month with improving cohort-over-cohort metrics.

## Leading Indicators

- Persona-based enrollment rates outperform the generic rate by ≥15% (personalization works)
- Cohort 2+ completion rates are higher than Cohort 1 (iteration is improving the program)
- Tier 1 → Tier 2 transition rate ≥40% (users want deeper mastery)
- Module content refresh identifies ≥1 improvement per month that improves pass rates

## Instructions

### 1. Expand the curriculum to all tiers

Using the curriculum spec from `certification-curriculum-design`, build Tiers 2-4:
- **Tier 2 (Practitioner):** 4-5 modules covering intermediate features — automations, integrations, team collaboration
- **Tier 3 (Expert):** 4-5 modules covering advanced features — custom configurations, API usage, advanced reporting
- **Tier 4 (Power User):** 3-4 modules covering cross-feature orchestration, performance tuning, and workflow optimization

Build Intercom Product Tours for each new module. Create assessments for each. Instrument PostHog events using the same taxonomy from Baseline.

**Human action required:** Review Tiers 3-4 curriculum. Expert and Power User content must reflect genuinely advanced skills — not intermediate features relabeled. Test each assessment yourself to confirm it requires real mastery.

### 2. Launch persona-based certification paths

Run the the certification scaling pipeline workflow (see instructions below) drill to:
- Analyze PostHog data from Baseline to identify 3-5 certification personas (by role, use case, plan type)
- Build PostHog feature flags that route users to persona-specific module orders and content variants
- Create persona-variant Intercom Product Tours for each module (same skill, different use-case framing)
- Personalize the enrollment prompt copy and email subjects by persona

### 3. Switch to cohort-based delivery

From the the certification scaling pipeline workflow (see instructions below) drill, activate the cohort system:
- n8n workflow runs bi-weekly, batching eligible users into a cohort with a shared start date
- Enrollment emails reference the cohort: "Join {N} users starting this Monday"
- In-app messages show cohort progress: "Your cohort is {X}% through Tier 1"
- Track cohort-level metrics in PostHog: completion rate, time-to-complete, stall rate

### 4. A/B test the funnel at every stage

Run the `ab-test-orchestrator` drill to test:

**Enrollment stage:**
- Test enrollment prompt copy: feature-focused ("Master advanced features") vs outcome-focused ("Users who certify retain 2x longer") vs social-proof ("47 users certified this month")
- Test email timing: 14-day delay vs 7-day delay vs immediate on activation

**Completion stage:**
- Test module ordering: recommended order vs user-choice order
- Test stall nudge channel: in-app only vs email only vs both
- Test stall nudge timing: 7-day threshold vs 5-day threshold

**Transition stage:**
- Test Tier 1 → Tier 2 bridge: immediate enrollment vs 7-day rest period vs teaser content
- Test celebration email CTA: "Start Tier 2" vs "Share your badge" vs "Invite a colleague"

Run one experiment at a time per funnel stage. Each test needs ≥200 users per variant. At Scalable volume (100+ certs/month), most tests can conclude within 4-6 weeks.

### 5. Monitor feature adoption impact

Run the `feature-adoption-monitor` drill configured for certification:
- Track whether certified users adopt features at higher rates than non-certified users
- Measure: do Tier 2 graduates use intermediate features more? Do Tier 3 graduates use advanced features?
- If certification does not drive feature adoption, the curriculum is teaching theory, not practice — redesign the assessments to require real feature usage

### 6. Build the scaling dashboard

Extend the Baseline dashboard with:

| Panel | Type | Purpose |
|-------|------|---------|
| Certifications per month (all tiers) | Trend line | Are we hitting 100/month? |
| Completion rate by persona | Bar chart | Which personas need path adjustments |
| Cohort-over-cohort completion | Cohort chart | Is each cohort improving |
| Tier transition funnel | Funnel | Tier 1 → 2 → 3 → 4 drop-off |
| Experiment results log | Table | Running and completed A/B tests with outcomes |
| Feature adoption: certified vs non-certified | Bar chart | Business justification |
| Content health: module difficulty | Heatmap | First-attempt pass rate by module by tier |

Set alerts:
- Monthly certification volume drops below 100
- Any persona completion rate drops below 50%
- Tier transition rate drops below 30%
- A/B test guardrail metric spikes

### 7. Evaluate against threshold after 2 months

Measure:
- **Certifications per month:** ≥100
- **Tier 1 → Tier 2 transition rate:** ≥40%
- **Certified retention lift:** Certified users retain at ≥1.3x rate of non-certified
- **Cohort improvement:** Cohort 3+ completes at higher rate than Cohort 1

If PASS: The certification scales. Document the persona paths, cohort model, experiment learnings, and proceed to Durable.
If FAIL: Focus on the bottleneck. Low volume → enrollment funnel needs work (test more aggressive prompts or wider targeting). Low transition → bridge sequence is weak (test different CTAs). Low retention lift → curriculum redesign needed.

## Time Estimate

- 12 hours: Expand curriculum to 4 tiers, build Product Tours and assessments
- 10 hours: Build persona segmentation, feature flags, and persona-variant content
- 8 hours: Set up cohort delivery automation
- 15 hours: Design and run 3-4 A/B tests across the funnel
- 8 hours: Feature adoption analysis and dashboard build
- 7 hours: Monitoring, weekly reviews, and final analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Events, funnels, experiments, feature flags, cohorts, dashboards | Free-$45/mo for most (usage-based) — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | Product Tours (all tiers), persona-variant tours, contextual messages | Advanced: $85/seat/mo + Proactive Support: $349/mo — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Enrollment, stall, celebration, and tier-bridge sequences | Starter: $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Cohort batching, stall detection, badge issuance, content refresh | Self-hosted: Free; Cloud: from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Typeform | In-module quizzes (if quiz-based assessments used) | Basic: $29/mo — [typeform.com/pricing](https://www.typeform.com/pricing) |

**Estimated play-specific cost:** Intercom Advanced + Proactive ~$434/mo + Loops ~$49/mo + Typeform ~$29/mo = ~$512/mo

## Drills Referenced

- the certification scaling pipeline workflow (see instructions below) — persona segmentation, cohort delivery, tier transitions, and content refresh automation
- `ab-test-orchestrator` — design and run A/B tests on enrollment, completion, and transition stages
- `feature-adoption-monitor` — track whether certification drives actual feature usage
