---
name: timing-qualification-smoke
description: >
  Timing Qualification Process — Smoke Test. Determine prospect's urgency and buying timeline to prioritize opportunities ready to close now and avoid pipeline bloat from future deals.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Smoke Test"
time: "4 hours over 1 week"
outcome: "Timeline identified for ≥8 opportunities in 1 week"
kpis: ["Timeline identification rate", "Urgent opportunity percentage", "Timeline validation success"]
slug: "timing-qualification"
install: "npx gtm-skills add sales/qualified/timing-qualification"
drills:
  - icp-definition
  - threshold-engine
---
# Timing Qualification Process — Smoke Test

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Determine prospect's urgency and buying timeline to prioritize opportunities ready to close now and avoid pipeline bloat from future deals.

**Time commitment:** 4 hours over 1 week
**Pass threshold:** Timeline identified for ≥8 opportunities in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. On first 10 discovery calls, ask explicitly 'What's driving you to solve this now?' and 'When do you need this in place?' to understand urgency.

2. Identify timing triggers: upcoming deadline, seasonal need, executive mandate, budget expiration, competitive pressure.

3. Use timeline categorization: Immediate (0-30 days), Near-term (1-3 months), Medium-term (3-6 months), Long-term (6+ months).

4. Ask follow-up 'What happens if you don't solve this by [timeline]?' to validate urgency.

5. Log timeline in Attio with specific target date and urgency rating (High/Medium/Low).

6. Track PostHog events: timeline_identified, urgent_opportunity, timeline_validated.

7. Prioritize Immediate and Near-term opportunities for fast follow-up; place Long-term in nurture.

8. Set pass threshold: Timeline identified for ≥8 opportunities in 1 week with ≥50% Immediate or Near-term.

9. Compare close rates by timeline category to validate that urgency predicts deal velocity.

10. Document which timing questions work best; proceed to Baseline if threshold met.

---

## KPIs to track
- Timeline identification rate
- Urgent opportunity percentage
- Timeline validation success

---

## Pass threshold
**Timeline identified for ≥8 opportunities in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/timing-qualification`_
