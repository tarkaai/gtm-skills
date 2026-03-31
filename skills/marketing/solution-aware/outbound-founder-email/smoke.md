---
name: outbound-founder-email-smoke
description: >
  Outbound founder-led email — Smoke Test. Founder-sent cold email sequences to solution-aware prospects, from a small smoke test through scaled automation to agent-driven durable optimization that keeps or improves meeting rate over time.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email"
level: "Smoke Test"
time: "4 hours over 1 week"
outcome: "≥ 2 meetings in 1 week"
kpis: ["Reply rate", "Time to first reply", "Emails sent"]
slug: "outbound-founder-email"
install: "npx gtm-skills add marketing/solution-aware/outbound-founder-email"
drills:
  - icp-definition
  - threshold-engine
---
# Outbound founder-led email — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email

## Overview
Founder-sent cold email sequences to solution-aware prospects, from a small smoke test through scaled automation to agent-driven durable optimization that keeps or improves meeting rate over time.

**Time commitment:** 4 hours over 1 week
**Pass threshold:** ≥ 2 meetings in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **Clay** (Enrichment)
- **Instantly** (Email)

---

## Instructions

1. Define your ICP (industry, role, company size) and document it in a short brief.

2. Find 10 on-target prospects by manually searching LinkedIn, Apollo, or Clay; add each to a spreadsheet with email, name, role, and company.

3. In the spreadsheet, add a column for outcome (no reply, positive reply, meeting booked) and a column for date sent.

4. Write a 3-step email sequence: intro email (personalized first line, clear value, soft CTA); one follow-up 3–4 days later; final follow-up with Calendly link 4–5 days after that. Send from the founder's primary email; cap at 100 contacts total.

5. Before sending, set your pass threshold (e.g. ≥ 3% positive replies or ≥ 2 meetings in 7–10 days) and choose where you will log outcomes (PostHog or CRM such as Attio).

6. Configure PostHog or your CRM with properties for reply rate, meetings booked, and time to first reply so you can compare to threshold.

7. Send the intro email to all 10 contacts; schedule follow-ups in your calendar or a simple tool so you send on time.

8. As replies arrive, log each outcome in PostHog or the CRM and respond to positive replies within 24 hours.

9. After 7–10 days from the first send, stop the sequence and count: total emails sent, positive replies, meetings booked. Compute reply rate and meeting rate.

10. Compare results to your pass threshold. If you met or exceeded it, document the ICP and sequence and proceed to Baseline; if not, revisit ICP definition, list source, or offer and iterate before retesting.

---

## KPIs to track
- Reply rate
- Time to first reply
- Emails sent

---

## Pass threshold
**≥ 2 meetings in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/outbound-founder-email`_
