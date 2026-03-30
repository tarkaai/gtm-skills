---
name: account-research-playbook-smoke
description: >
  Account Research & Intelligence — Smoke Test. Systematically research target accounts before outreach to personalize messaging and improve relevance, from manual LinkedIn research to AI-driven account intelligence that auto-generates comprehensive account profiles with buying signals and talk tracks.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=8 accounts researched and >=30% reply rate from personalized outreach within 1 week"
kpis: ["Reply rate (researched vs non-researched)", "Research time per account", "Personalization hook effectiveness"]
slug: "account-research-playbook"
install: "npx gtm-skills add sales/qualified/account-research-playbook"
---
# Account Research & Intelligence — Smoke Test

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Systematically research target accounts before outreach to personalize messaging and improve relevance, from manual LinkedIn research to AI-driven account intelligence that auto-generates comprehensive account profiles with buying signals and talk tracks.

**Time commitment:** 8 hours over 1 week
**Pass threshold:** >=8 accounts researched and >=30% reply rate from personalized outreach within 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **LinkedIn Sales Navigator** (Channel)

---

## Instructions

1. Create an account research template in a spreadsheet with sections: Company Overview (what they do, size, stage), Recent News (funding, launches, executive hires), Tech Stack (tools they use), Pain Indicators (signals they have your problem), Key Contacts (names, titles, LinkedIn URLs), Personalization Hooks (specific reference points for outreach).

2. Select 10 target accounts from your ICP; spend 15-20 minutes researching each using LinkedIn, company website, Crunchbase, news search, G2 reviews, job postings.

3. Set pass threshold: complete research for >=8 accounts, and personalized outreach to researched accounts yields >=30% reply rate vs <=15% for non-researched accounts within 1 week.

4. For each account, identify 2-3 personalization hooks: recent funding round ("Congrats on Series B"), new executive hire ("Saw you brought on new CRO"), product launch ("Noticed you launched X"), pain indicator from job posting ("Hiring for Y role suggests you're scaling Z").

5. Use research to craft personalized first lines in outreach emails: "Saw [Company] just raised $X to expand into [market]—as you scale, [pain point] becomes critical. We help companies like [similar company] solve this by [value prop]."

6. Log research data in Attio with custom fields for recent_news, tech_stack, pain_indicators, personalization_hooks; track which hooks generate replies.

7. In PostHog, create events for account_researched and personalized_outreach_sent with properties for research depth and hooks used.

8. After outreach, track reply rates by research quality (deep research vs surface-level vs no research); measure whether personalization improves engagement.

9. After 1 week, compare reply rates: do researched accounts respond >=2x more than non-researched? If yes, research delivers ROI.

10. If >=8 accounts researched and reply rate >=30%, account research is valuable; document research process and proceed to Baseline; otherwise refine research sources or personalization approach.

---

## KPIs to track
- Reply rate (researched vs non-researched)
- Research time per account
- Personalization hook effectiveness

---

## Pass threshold
**>=8 accounts researched and >=30% reply rate from personalized outreach within 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/account-research-playbook`_
