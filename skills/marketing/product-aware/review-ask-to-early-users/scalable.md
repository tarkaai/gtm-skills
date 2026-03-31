---
name: review-ask-to-early-users-scalable
description: >
    Review Ask to Early Users — Scalable Automation. Request reviews from a handful of early users
  to build social proof and see if new reviews correlate with at least one inbound lead.
stage: "Marketing > Product Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 20 new reviews and ≥ 15 inbound leads over 2 months"
kpis: ["3 new reviews", "1 inbound"]
slug: "review-ask-to-early-users"
install: "npx gtm-skills add marketing/product-aware/review-ask-to-early-users"
drills:
  - ab-test-orchestrator
  - tool-sync-workflow
---
# Review Ask to Early Users — Scalable Automation

> **Stage:** Marketing → Product Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Overview
Review Ask to Early Users — Scalable Automation. Request reviews from a handful of early users to build social proof and see if new reviews correlate with at least one inbound lead.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** ≥ 20 new reviews and ≥ 15 inbound leads over 2 months

---

## Budget

**Play-specific tools & costs**
- **Tool and automation costs:** ~$100-500/mo at scale

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Test listing variations
Run the `ab-test-orchestrator` drill to test: listing headlines, feature ordering, screenshot selection, pricing presentation, and CTA copy across directories. Rotate variations monthly.

### 2. Automate review and listing management
Run the `tool-sync-workflow` drill to build n8n workflows: auto-detect new reviews and alert team, auto-respond to reviews, sync directory-sourced leads to Attio, and auto-update listings when product features change.

### 3. Expand to more directories
List on 10+ directories. Focus effort on the top 3-5 that drive real pipeline. Maintain presence on others with minimal ongoing effort.

### 4. Evaluate against threshold
Measure against: ≥ 20 new reviews and ≥ 15 inbound leads over 2 months. If PASS, proceed to Durable. If FAIL, consolidate to highest-ROI directories.

---

## KPIs to track
- 3 new reviews
- 1 inbound

---

## Pass threshold
**≥ 20 new reviews and ≥ 15 inbound leads over 2 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/product-aware/review-ask-to-early-users`_
