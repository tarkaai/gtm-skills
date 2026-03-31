---
name: pr-campaign-launch-scalable
description: >
    PR Campaign Launch — Scalable Automation. Coordinated press outreach for product launches or
  milestones to generate media coverage and awareness with problem-aware audiences.
stage: "Marketing > Problem Aware"
motion: "PR & Earned Mentions"
channels: "Other, Social"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥40 press mentions and ≥60 qualified leads from quarterly PR campaigns over 6 months"
kpis: ["Weekly volume", "Conversion rate", "Cost per result", "Automation efficiency", "Quality score"]
slug: "pr-campaign-launch"
install: "npx gtm-skills add marketing/problem-aware/pr-campaign-launch"
drills:
  - content-repurposing
  - ab-test-orchestrator
---
# PR Campaign Launch — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** PR & Earned Mentions | **Channels:** Other, Social

## Overview
PR Campaign Launch — Scalable Automation. Coordinated press outreach for product launches or milestones to generate media coverage and awareness with problem-aware audiences.

**Time commitment:** 75 hours over 3 months
**Pass threshold:** ≥40 press mentions and ≥60 qualified leads from quarterly PR campaigns over 6 months

---

## Budget

**Play-specific tools & costs**
- **Tool and automation costs:** ~$100-500/mo at scale

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Repurpose PR content
Run the `content-repurposing` drill to turn every media mention into multiple assets: social posts, email newsletter content, website social proof, and sales enablement materials.

### 2. Test PR approaches
Run the `ab-test-orchestrator` drill to test: pitch angles (data-driven vs story-driven), outreach timing, follow-up cadence, and content types (guest post vs quote vs exclusive data). Track which approaches yield the highest coverage rates.

### 3. Scale media relationships
Move from one-off pitches to ongoing relationships. Offer journalists regular access to data, experts, and customer stories. Build a media list in Attio and nurture it.

### 4. Evaluate against threshold
Measure against: ≥40 press mentions and ≥60 qualified leads from quarterly PR campaigns over 6 months. If PASS, proceed to Durable. If FAIL, focus on the media relationships that are generating the most value.

---

## KPIs to track
- Weekly volume
- Conversion rate
- Cost per result
- Automation efficiency
- Quality score

---

## Pass threshold
**≥40 press mentions and ≥60 qualified leads from quarterly PR campaigns over 6 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/pr-campaign-launch`_
