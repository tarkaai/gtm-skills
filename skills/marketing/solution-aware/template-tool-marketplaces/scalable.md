---
name: template-tool-marketplaces-scalable
description: >
    Template or Tool Marketplace — Scalable Automation. Publish a free template (Notion, Airtable,
  Figma, etc.
stage: "Marketing > Solution Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 500 downloads and ≥ 15 leads over 2 months"
kpis: ["Download rate", "Landing page visits"]
slug: "template-tool-marketplaces"
install: "npx gtm-skills add marketing/solution-aware/template-tool-marketplaces"
drills:
  - ab-test-orchestrator
  - tool-sync-workflow
---
# Template or Tool Marketplace — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Overview
Template or Tool Marketplace — Scalable Automation. Publish a free template (Notion, Airtable, Figma, etc.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** ≥ 500 downloads and ≥ 15 leads over 2 months

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
Measure against: ≥ 500 downloads and ≥ 15 leads over 2 months. If PASS, proceed to Durable. If FAIL, consolidate to highest-ROI directories.

---

## KPIs to track
- Download rate
- Landing page visits

---

## Pass threshold
**≥ 500 downloads and ≥ 15 leads over 2 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/template-tool-marketplaces`_
