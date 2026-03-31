---
name: trial-to-paid-conversion-baseline
description: >
  Trial-to-Paid Conversion — Baseline Run. Convert free trial users to paying customers by driving activation, demonstrating value, and creating urgency, from manual trial follow-ups to AI-driven trial orchestration that personalizes interventions and maximizes conversion rates.
stage: "Sales > Won"
motion: "Outbound Founder-Led"
channels: "Email, Product, Direct"
level: "Baseline Run"
time: "24 hours over 2 weeks"
outcome: ">=45% trial-to-paid conversion rate over 2 weeks"
kpis: ["Trial conversion rate by segment", "Activation milestone completion rate", "Trial health score distribution", "Time to activation"]
slug: "trial-to-paid-conversion"
install: "npx gtm-skills add sales/won/trial-to-paid-conversion"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Trial-to-Paid Conversion — Baseline Run

> **Stage:** Sales → Won | **Motion:** Outbound Founder-Led | **Channels:** Email, Product, Direct

## Overview
Convert free trial users to paying customers by driving activation, demonstrating value, and creating urgency, from manual trial follow-ups to AI-driven trial orchestration that personalizes interventions and maximizes conversion rates.

**Time commitment:** 24 hours over 2 weeks
**Pass threshold:** >=45% trial-to-paid conversion rate over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$40–100/mo
- **Clay or Apollo (list building + enrichment):** ~$50–150/mo

_Total play-specific: ~$40–150/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **Attio** (CRM)
- **Instantly** (Email)

---

## Instructions

1. Expand to 30-50 trial users over 2 weeks; build an automated email sequence in Instantly or similar: welcome email (day 0), setup guide (day 1), milestone coaching (days 3, 7, 10), upgrade offer (day 12), urgency reminder (day 13).

2. Create in-app messaging (using PostHog or Intercom) that triggers based on user behavior: if user hasn't completed setup after 24 hours, show "Need help getting started?" prompt with link to guide or call booking.

3. Set pass threshold: >=45% trial-to-paid conversion rate, and users who hit >=3 activation milestones convert at >=3x rate vs users who hit <2 milestones.

4. Sync trial user data from product (via PostHog) to Attio so sales/success teams can see trial activity, activation progress, and engagement score in real-time.

5. Implement activation-based outreach: when user hits milestone 2, trigger sales call booking email; when user hits milestone 3, trigger upgrade offer; when user stalls, trigger help offer.

6. Build a trial health score in PostHog: combine activation milestones (40%), feature usage frequency (30%), team size (20%), and engagement with emails/content (10%); score 0-100.

7. Create trial user segments in PostHog: Hot (score >=70, call immediately), Warm (score 40-69, automated nurture), Cold (score <40, re-engagement campaign or let expire).

8. Track trial outcomes in PostHog: trial_converted (paid), trial_expired (didn't convert), trial_extended (needed more time); analyze why users don't convert (didn't see value, budget issue, not decision-maker).

9. After 2 weeks, measure conversion rate by segment and activation milestone; if Hot trial users convert >=60% and overall conversion >=45%, trial motion is working.

10. If threshold met, document trial playbook and activation benchmarks, then move to Scalable; otherwise improve onboarding, reduce friction, or adjust trial length.

---

## KPIs to track
- Trial conversion rate by segment
- Activation milestone completion rate
- Trial health score distribution
- Time to activation

---

## Pass threshold
**>=45% trial-to-paid conversion rate over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/won/trial-to-paid-conversion`_
