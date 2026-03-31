---
name: partner-marketplace-listings-durable
description: >
    Partner Marketplace Listings — Durable Intelligence. Get listed in partner app marketplaces
  (Salesforce AppExchange, HubSpot, Shopify) to drive discovery and leads from solution-aware users
  of those platforms.
stage: "Marketing > Solution Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained marketplace performance and ≥50 leads/quarter over 12 months via AI-optimized listing content"
kpis: ["Sustained conversion rate", "AI experiment win rate", "Market adaptation speed", "Cost efficiency trend", "Lead quality score"]
slug: "partner-marketplace-listings"
install: "npx gtm-skills add marketing/solution-aware/partner-marketplace-listings"
drills:
  - dashboard-builder
---
# Partner Marketplace Listings — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Overview
Partner Marketplace Listings — Durable Intelligence. Get listed in partner app marketplaces (Salesforce AppExchange, HubSpot, Shopify) to drive discovery and leads from solution-aware users of those platforms.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained marketplace performance and ≥50 leads/quarter over 12 months via AI-optimized listing content

---

## Budget

**Play-specific tools & costs**
- **Ongoing tool costs:** ~$100-500/mo
- **Agent compute costs:** Variable based on monitoring frequency

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build directory dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: traffic per directory, conversion rate per directory, review score trends, pipeline attributed to directory traffic. Set alerts for review score drops or traffic declines.

### 2. Autonomous directory management
Configure the agent to: monitor competitor listings for changes, alert when new reviews come in, suggest listing updates based on new features or positioning changes, and track directory ranking positions.

### 3. Sustain and optimize
Monthly: review directory ROI, update listing copy, request new reviews, and respond to recent reviews. The agent generates a monthly directory performance report.

### 4. Evaluate sustainability
Measure against: Sustained marketplace performance and ≥50 leads/quarter over 12 months via AI-optimized listing content. This level runs continuously. If directories consistently drive qualified traffic, the play is durable.

---

## KPIs to track
- Sustained conversion rate
- AI experiment win rate
- Market adaptation speed
- Cost efficiency trend
- Lead quality score

---

## Pass threshold
**Sustained marketplace performance and ≥50 leads/quarter over 12 months via AI-optimized listing content**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/partner-marketplace-listings`_
