---
name: guest-posting-scale-smoke
description: >
  Guest Posting at Scale — Smoke Test. Publish guest posts on relevant industry blogs to build backlinks and awareness, from manual pitching to automated outreach and AI-driven content placement optimization.
stage: "Marketing > Solution Aware"
motion: "PR & Earned Mentions"
channels: "Content, Email"
level: "Smoke Test"
time: "8 hours over 2 weeks"
outcome: "≥2 accepted pitches and ≥50 referral visits"
kpis: ["Pitch acceptance rate", "Articles published", "Referral traffic", "Backlinks acquired"]
slug: "guest-posting-scale"
install: "npx gtm-skills add marketing/solution-aware/guest-posting-scale"
drills:
  - social-content-pipeline
  - threshold-engine
---
# Guest Posting at Scale — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** PR & Earned Mentions | **Channels:** Content, Email

## Overview
Publish guest posts on relevant industry blogs to build backlinks and awareness, from manual pitching to automated outreach and AI-driven content placement optimization.

**Time commitment:** 8 hours over 2 weeks
**Pass threshold:** ≥2 accepted pitches and ≥50 referral visits

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (Analytics)
- **Ahrefs** (Analytics)

---

## Instructions

1. Research 10-15 industry blogs that accept guest posts; prioritize sites with Domain Authority 30+ and your ICP as readers (use Ahrefs or Moz).

2. For each blog, identify content guidelines, preferred topics, and editor contact information; save in a spreadsheet with columns for site, DA, contact, status.

3. Create 3 unique article pitches (title, outline, key takeaways) aligned with each blog's content themes and your expertise.

4. Draft personalized pitch emails referencing specific articles from their blog; explain why your post would provide value to their readers.

5. Send pitches to 10 blogs manually via email; track responses in your spreadsheet (accepted, rejected, no response).

6. Set pass threshold: ≥2 pitches accepted within 2 weeks.

7. For accepted pitches, write high-quality 1,200-1,500 word articles with actionable insights; include 1-2 contextual backlinks to your site (to valuable content, not just homepage).

8. Submit articles for editorial review; incorporate feedback and get posts published.

9. Set up PostHog to track referral traffic from guest post backlinks; monitor conversions from guest post readers.

10. If you get ≥2 acceptances and published posts drive ≥50 referral visits total, document your pitch templates and target blog list and proceed to Baseline; if not, refine pitch approach or target different blogs.

---

## KPIs to track
- Pitch acceptance rate
- Articles published
- Referral traffic
- Backlinks acquired

---

## Pass threshold
**≥2 accepted pitches and ≥50 referral visits**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/guest-posting-scale`_
