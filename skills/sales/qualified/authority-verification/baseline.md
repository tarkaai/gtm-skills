---
name: authority-verification-baseline
description: >
  Authority Verification Process — Baseline Run. Confirm you're speaking with actual decision-makers to prevent wasted cycles on non-buyers and accelerate deals through the right stakeholders.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "Authority verified in ≥80% of opportunities over 2 weeks"
kpis: ["Authority verification rate", "Economic buyer connection rate", "Deal velocity with verified authority", "Close rate with verified authority"]
slug: "authority-verification"
install: "npx gtm-skills add sales/qualified/authority-verification"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Authority Verification Process — Baseline Run

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Confirm you're speaking with actual decision-makers to prevent wasted cycles on non-buyers and accelerate deals through the right stakeholders.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** Authority verified in ≥80% of opportunities over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$40–100/mo
- **Clay or Apollo (list building + enrichment):** ~$50–150/mo

_Total play-specific: ~$40–150/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **LinkedIn Sales Navigator** (Channel)

---

## Instructions

1. Create authority verification checklist: org chart research, LinkedIn reporting structure, budget authority confirmation, RACI mapping, introduction to economic buyer.

2. Build question bank for different scenarios: inbound leads, outbound prospects, enterprise vs. SMB, technical vs. business buyers.

3. Research 50-100 target accounts over 2 weeks; map org structures in advance using LinkedIn Sales Navigator and company websites.

4. On every discovery call, use standardized authority questions within first 10 minutes; log responses in Attio custom fields immediately.

5. Create multi-threading strategy: when speaking with influencer, request introduction to decision maker before moving to demo or proposal.

6. Set up PostHog event tracking: authority_question_asked, authority_level_identified, decision_maker_intro_requested, economic_buyer_connected.

7. Track conversion metrics: what % of opportunities with verified authority convert to meeting vs. non-verified; measure deal velocity difference.

8. Set pass threshold: Authority verified in ≥80% of opportunities within 2 weeks, with ≥50% resulting in connection to economic buyer.

9. Analyze data: which authority verification approaches work best by buyer persona, deal size, and industry.

10. If threshold met, document authority verification playbook and proceed to Scalable; if not, refine questions or earlier qualification.

---

## KPIs to track
- Authority verification rate
- Economic buyer connection rate
- Deal velocity with verified authority
- Close rate with verified authority

---

## Pass threshold
**Authority verified in ≥80% of opportunities over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/authority-verification`_
