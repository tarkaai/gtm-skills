---
name: intent-signal-tracking-scalable
description: >
  Intent Signal Tracking — Scalable Automation. Monitor and act on buyer intent signals like website behavior, content consumption, and G2 research to reach prospects at peak buying moment, from manual tracking in spreadsheets to AI-driven real-time intent orchestration that triggers personalized outreach automatically.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=200 high-intent accounts/month and >=3x conversion rate vs cold outreach over 2 months"
kpis: ["Intent accounts per month", "Signal-to-outreach time", "Conversion rate by intent tier", "Intent decay impact"]
slug: "intent-signal-tracking"
install: "npx gtm-skills add sales/qualified/intent-signal-tracking"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Intent Signal Tracking — Scalable Automation

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Overview
Monitor and act on buyer intent signals like website behavior, content consumption, and G2 research to reach prospects at peak buying moment, from manual tracking in spreadsheets to AI-driven real-time intent orchestration that triggers personalized outreach automatically.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** >=200 high-intent accounts/month and >=3x conversion rate vs cold outreach over 2 months

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing, scaled):** ~$100–200/mo
- **Clay (enrichment + AI personalization):** ~$150–400/mo
- **LinkedIn Sales Navigator (prospecting, optional):** ~$100/mo

_Total play-specific: ~$100–400/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **Attio** (CRM)
- **n8n** (Automation)
- **Clay** (Enrichment)
- **Instantly** (Email)

---

## Instructions

1. Scale to 200+ high-intent accounts per month; integrate PostHog with n8n to trigger automated workflows when accounts cross intent thresholds.

2. Build an n8n workflow triggered by PostHog's high_intent_threshold event: pull account from PostHog, enrich via Clay, identify stakeholders, find verified emails, create personalized email draft, add to Attio, notify rep.

3. Expand intent model to include third-party signals: G2 profile views (via G2 API), LinkedIn company page visits (via LinkedIn Ads), tech stack changes (via BuiltWith), job postings (via Otta or LinkedIn).

4. Set up real-time intent alerts in Slack: when a Fortune 500 account triggers >=2 high-value signals in 24 hours, n8n sends alert to sales channel with account details and recommended action.

5. In Attio, create intent-based lead routing: accounts with >=50 intent points go to senior AEs, 30-49 to mid-level, <30 to SDRs; route within 1 hour of threshold crossing.

6. Build a PostHog dashboard showing daily intent signal volume, intent tier distribution, outreach velocity (time from signal to contact), and conversion by intent tier.

7. Implement intent decay: if no new signals for 7 days, reduce intent score by 30%; prevents stale leads from staying in high-intent queue.

8. Each week, analyze which signal combinations (e.g., pricing + demo + case study) most strongly predict closed deals; adjust scoring weights in n8n.

9. Test automated outreach: for low-touch segments, have n8n send first email automatically within 30 minutes of high-intent signal; monitor reply rates vs manual outreach.

10. After 2 months, if high-intent accounts convert at >=3x rate of cold outreach and signal-to-outreach time <2 hours, move to Durable; otherwise refine routing or signal sources.

---

## KPIs to track
- Intent accounts per month
- Signal-to-outreach time
- Conversion rate by intent tier
- Intent decay impact

---

## Pass threshold
**>=200 high-intent accounts/month and >=3x conversion rate vs cold outreach over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/intent-signal-tracking`_
