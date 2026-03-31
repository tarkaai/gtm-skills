---
name: alumni-campus-pro-orgs-baseline
description: >
    Alumni & Campus Outreach — Baseline Run. Post or email in alumni, campus, or professional org
  groups to reach warm communities and test whether 1–2 meetings come from low-friction
  participation.
stage: "Marketing > Unaware"
motion: "Communities & Forums"
channels: "Communities, Other"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 2 meetings over 2 weeks"
kpis: ["Post engagement", "Inbound inquiries"]
slug: "alumni-campus-pro-orgs"
install: "npx gtm-skills add marketing/unaware/alumni-campus-pro-orgs"
drills:
  - posthog-gtm-events
  - content-repurposing
---
# Alumni & Campus Outreach — Baseline Run

> **Stage:** Marketing → Unaware | **Motion:** Communities & Forums | **Channels:** Communities, Other

## Overview
Alumni & Campus Outreach — Baseline Run. Post or email in alumni, campus, or professional org groups to reach warm communities and test whether 1–2 meetings come from low-friction participation.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 2 meetings over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Set up analytics
Run the `posthog-gtm-events` drill to track community-driven traffic and conversions: `alumni-campus-pro-orgs_community_post`, `alumni-campus-pro-orgs_referral_visit`, `alumni-campus-pro-orgs_signup_from_community`. Use UTM parameters on all shared links to attribute traffic to specific communities.

### 2. Build a content repurposing system
Run the `content-repurposing` drill to adapt your best-performing community content across multiple communities and formats. One detailed answer can become a Reddit post, a Slack thread, a blog post, and a Twitter thread.

### 3. Execute a 2-week community engagement plan
Post 2-3 times per week across your top communities. Track everything in PostHog. Focus on communities that showed traction in Smoke.

### 4. Evaluate against threshold
Measure against: ≥ 2 meetings over 2 weeks. If PASS, proceed to Scalable. If FAIL, narrow focus to fewer communities or try different content types.

---

## KPIs to track
- Post engagement
- Inbound inquiries

---

## Pass threshold
**≥ 2 meetings over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/unaware/alumni-campus-pro-orgs`_
