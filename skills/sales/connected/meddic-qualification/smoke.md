---
name: meddic-qualification-smoke
description: >
  MEDDIC Qualification System — Smoke Test. Apply MEDDIC (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion) to complex enterprise deals, from manual tracking to AI-driven continuous qualification that surfaces deal risks and accelerates cycles.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=2 deals with >=80% MEDDIC completeness in 1 week"
kpis: ["MEDDIC completeness score", "Elements per call", "Time to complete MEDDIC"]
slug: "meddic-qualification"
install: "npx gtm-skills add sales/connected/meddic-qualification"
---
# MEDDIC Qualification System — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Apply MEDDIC (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion) to complex enterprise deals, from manual tracking to AI-driven continuous qualification that surfaces deal risks and accelerates cycles.

**Time commitment:** 8 hours over 1 week
**Pass threshold:** >=2 deals with >=80% MEDDIC completeness in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **Cal.com** (Scheduling)

---

## Instructions

1. Create a MEDDIC scorecard in a spreadsheet with sections for Metrics (quantifiable goals), Economic Buyer (name/title), Decision Criteria (must-haves), Decision Process (steps/timeline), Pain (business impact), Champion (internal advocate).

2. Select 3-5 active opportunities from your pipeline; for each, fill out the MEDDIC scorecard based on current knowledge.

3. Identify gaps: which MEDDIC elements are you missing for each deal? Write 2-3 discovery questions to uncover each missing element.

4. Set pass threshold: complete >=80% of MEDDIC elements for at least 2 deals within 1 week to validate the framework is practical.

5. Schedule follow-up calls with prospects to fill MEDDIC gaps; use your questions to uncover Economic Buyer, Decision Process, and Champion.

6. After each call, update the MEDDIC scorecard in the spreadsheet and assign a completeness score (0-100%) based on how many elements are known.

7. Log MEDDIC completion scores in Attio as a custom field; track which elements are hardest to uncover (typically Champion and Decision Process).

8. In PostHog, create events for meddic_element_discovered with properties for element type (Metrics, Economic Buyer, etc.) and deal stage.

9. After 1 week, calculate average MEDDIC completeness across your deals; if >=2 deals reach >=80% completeness, the framework is working.

10. If threshold met, document which questions best uncovered each MEDDIC element and proceed to Baseline; otherwise refine discovery approach and retest.

---

## KPIs to track
- MEDDIC completeness score
- Elements per call
- Time to complete MEDDIC

---

## Pass threshold
**>=2 deals with >=80% MEDDIC completeness in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/meddic-qualification`_
