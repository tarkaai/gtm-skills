---
name: q-a-sites-stackoverflow-etc-baseline
description: >
    Q&A Site Authority — Baseline Run. Answer a few relevant questions on Q&A sites with a soft CTA
  to test if authority-building drives profile clicks and a lead.
stage: "Marketing > Problem Aware"
motion: "Communities & Forums"
channels: "Other"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 80 profile clicks and ≥ 3 leads over 2 weeks"
kpis: ["Profile views", "Profile click rate"]
slug: "q-a-sites-stackoverflow-etc"
install: "npx gtm-skills add marketing/problem-aware/q-a-sites-stackoverflow-etc"
drills:
  - posthog-gtm-events
  - content-repurposing
---
# Q&A Site Authority — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Communities & Forums | **Channels:** Other

## Overview
Q&A Site Authority — Baseline Run. Answer a few relevant questions on Q&A sites with a soft CTA to test if authority-building drives profile clicks and a lead.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 80 profile clicks and ≥ 3 leads over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Set up analytics
Run the `posthog-gtm-events` drill to track community-driven traffic and conversions: `q-a-sites-stackoverflow-etc_community_post`, `q-a-sites-stackoverflow-etc_referral_visit`, `q-a-sites-stackoverflow-etc_signup_from_community`. Use UTM parameters on all shared links to attribute traffic to specific communities.

### 2. Build a content repurposing system
Run the `content-repurposing` drill to adapt your best-performing community content across multiple communities and formats. One detailed answer can become a Reddit post, a Slack thread, a blog post, and a Twitter thread.

### 3. Execute a 2-week community engagement plan
Post 2-3 times per week across your top communities. Track everything in PostHog. Focus on communities that showed traction in Smoke.

### 4. Evaluate against threshold
Measure against: ≥ 80 profile clicks and ≥ 3 leads over 2 weeks. If PASS, proceed to Scalable. If FAIL, narrow focus to fewer communities or try different content types.

---

## KPIs to track
- Profile views
- Profile click rate

---

## Pass threshold
**≥ 80 profile clicks and ≥ 3 leads over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/q-a-sites-stackoverflow-etc`_
