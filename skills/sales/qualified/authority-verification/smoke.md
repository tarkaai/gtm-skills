---
name: authority-verification-smoke
description: >
  Authority Verification Process — Smoke Test. Confirm you're speaking with actual decision-makers to prevent wasted cycles on non-buyers and accelerate deals through the right stakeholders.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Smoke Test"
time: "4 hours over 1 week"
outcome: "≥3 opportunities with verified authority in 1 week"
kpis: ["Authority verification rate", "Decision maker connection rate", "Time to authority confirmation"]
slug: "authority-verification"
install: "npx gtm-skills add sales/qualified/authority-verification"
---
# Authority Verification Process — Smoke Test

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Confirm you're speaking with actual decision-makers to prevent wasted cycles on non-buyers and accelerate deals through the right stakeholders.

**Time commitment:** 4 hours over 1 week
**Pass threshold:** ≥3 opportunities with verified authority in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **LinkedIn** (Channel)

---

## Instructions

1. Before any sales call, research the prospect's org chart on LinkedIn to identify who reports to whom and where budget authority likely sits.

2. In first 5 minutes of initial call, ask: 'Who else will be involved in evaluating and approving this purchase?' to map decision structure.

3. Use RACI framework: identify who is Responsible, Accountable, Consulted, and Informed for this buying decision.

4. Ask explicitly: 'Do you have budget authority for this purchase, or will someone else need to approve?' to confirm authority level.

5. If speaking with non-authority, ask: 'Can you introduce me to [decision maker name]?' or 'What's the best way to involve [budget holder] in our next conversation?'.

6. Log authority level in Attio custom field: 'Decision Maker', 'Influencer', 'Champion', or 'End User'.

7. Track PostHog events: authority_verified, decision_maker_identified, multi_threading_needed.

8. Set pass threshold: ≥3 deals in 1 week where you've confirmed authority and connected with actual decision maker.

9. Measure time saved: compare deal velocity for authority-verified vs. non-verified opportunities.

10. Document learnings: what questions work best, what signals indicate authority, what org structures to watch for; proceed to Baseline if threshold met.

---

## KPIs to track
- Authority verification rate
- Decision maker connection rate
- Time to authority confirmation

---

## Pass threshold
**≥3 opportunities with verified authority in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/authority-verification`_
