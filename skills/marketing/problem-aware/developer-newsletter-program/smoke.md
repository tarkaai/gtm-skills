---
name: developer-newsletter-program-smoke
description: >
  Developer Newsletter — Smoke Test. Ship 3 newsletter issues with code examples, tutorials,
  and industry insights to a small seed audience. Validate that the format produces subscribers
  and qualified developer leads before committing to always-on automation.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Email, Content"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=100 subscribers and >=3 qualified leads from first 3 issues"
kpis: ["Open rate", "Click rate", "Reply rate", "Subscriber count", "Qualified leads"]
slug: "developer-newsletter-program"
install: "npx gtm-skills add marketing/problem-aware/developer-newsletter-program"
drills:
  - icp-definition
  - newsletter-pipeline
  - threshold-engine
---

# Developer Newsletter — Smoke Test

> **Stage:** Marketing > Problem Aware | **Motion:** Founder Social Content | **Channels:** Email, Content

## Outcomes

Ship 3 issues of a developer-focused newsletter to a seed audience of >=100 subscribers. Demonstrate that the format produces engagement (>=30% open rate) and at least 3 qualified leads (developers or engineering leaders who reply, click a CTA, or express interest in the product).

## Leading Indicators

- Issue 1 achieves >=35% open rate (new list enthusiasm)
- At least 5 replies across the 3 issues (signals the content resonates enough to provoke conversation)
- At least 1 subscriber forwards the newsletter to a colleague (organic growth signal)
- Click rate on in-issue links >=5% (content is actionable, not just readable)

## Instructions

### 1. Define the newsletter ICP and content pillars

Run the `icp-definition` drill to define the developer audience. Document:
- Target reader job titles (e.g., senior backend engineer, engineering manager, DevOps lead)
- Pain points they encounter weekly that your product addresses
- Technical topics they search for or discuss in communities
- Competing newsletters they already read (research via Substack trending, dev.to, Hacker News popular topics)

From the ICP output, define 3-4 content pillars for the newsletter. Each pillar maps to a pain point:
- Pillar 1: Tactical tutorials (code examples solving a specific problem)
- Pillar 2: Industry analysis (trends, tool comparisons, architecture decisions)
- Pillar 3: Behind-the-scenes (engineering decisions at your company, lessons learned)
- Pillar 4: Curated links (5-7 best articles/repos from the week, with your commentary)

### 2. Build the seed subscriber list

Collect initial subscribers from these sources — no paid promotion at Smoke level:
- Export contacts from your CRM (Attio) where role contains "engineer", "developer", "CTO", "VP Engineering"
- Collect emails from existing LinkedIn connections who match the ICP (use LinkedIn export)
- Add any existing blog subscribers or product users who opted into marketing emails
- **Human action required:** Post on LinkedIn and Twitter announcing the newsletter with a signup link. Write the post using the `social-content-pipeline` drill's hook frameworks: lead with a specific pain point the newsletter will solve, not "I'm launching a newsletter."

Target: >=50 seed subscribers before sending Issue 1. If you have fewer than 50, delay launch by 3-5 days and promote more aggressively on social.

### 3. Set up the newsletter in Loops

Run the `newsletter-pipeline` drill to configure:
- Create a new newsletter in Loops with sender name = founder's name (not company name)
- Authenticate sending domain for deliverability
- Design a minimal template: plain-text style with a short intro, the main content section, one CTA, and footer. No heavy HTML — developer audiences respond better to text-forward emails.
- Create segments in Loops: "all-subscribers", "engaged" (opened last 2 issues), "at-risk" (did not open last 2 issues)

### 4. Write and send 3 issues

For each of the 3 issues (send weekly, Tuesday-Thursday, 9-10am in your primary audience timezone):

**Issue structure:**
- Subject line: specific and curiosity-driven, under 50 characters. Test different styles across the 3 issues: Issue 1 = question style ("Why does X break at scale?"), Issue 2 = data/number style ("3 patterns that cut deploy time by 40%"), Issue 3 = contrarian style ("Stop doing X — here's why")
- Opener (2-3 sentences): personal, conversational, references a real situation or problem
- Main content (400-800 words): one content pillar per issue, rotating through pillars. Include code snippets, architecture diagrams, or tool configurations where relevant. Be specific — "use Redis sorted sets with ZADD for leaderboard queries" not "consider a caching layer."
- CTA: one clear ask per issue. Rotate: Issue 1 = "reply and tell me what topic you want next", Issue 2 = "check out this tool/resource", Issue 3 = "book a 15-min chat if you're dealing with [problem]"
- Footer: unsubscribe link, forward-to-a-friend link

**Human action required:** The founder writes each issue. The agent prepares the structure, researches topics, drafts sections, and loads the email into Loops. The founder reviews, adds personal anecdotes, and approves the send.

### 5. Engage with every reply

After each send, monitor replies within 24 hours. Respond personally to every reply. Classify each reply in Attio:
- Positive engagement (compliment, question, discussion) — tag as "engaged-subscriber"
- Buying signal (asks about pricing, demo, trial, or references the problem your product solves) — tag as "qualified-lead" and create a deal record
- Feedback (content request, criticism) — log as a note for future issue planning

### 6. Evaluate against threshold

Run the `threshold-engine` drill after Issue 3 is sent and 48 hours have passed:
- Check: total subscriber count >= 100 (including organic signups from social promotion during the 3 weeks)
- Check: qualified leads >= 3 (replies or CTA clicks from people matching ICP who showed buying intent)
- Check: average open rate >= 30% across the 3 issues
- Check: unsubscribe rate < 2% per issue (if higher, content-audience mismatch)

**PASS:** All criteria met. Proceed to Baseline.
**FAIL:** Diagnose which criterion failed. If open rate low: test different subject lines. If no leads: strengthen CTAs or adjust content pillars toward more product-adjacent topics. If subscriber count low: invest more in social promotion. Re-run with 3 more issues.

## Time Estimate

- ICP definition and content pillar selection: 1 hour
- Seed list building and Loops setup: 1 hour
- Writing each issue (agent drafts, founder edits): 1 hour x 3 = 3 hours
- Reply management and evaluation: 1 hour
- **Total: 6 hours over 3 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loops | Newsletter sending and subscriber management | Free up to 1,000 contacts — https://loops.so/pricing |
| Attio | CRM for lead tracking and reply classification | Free tier available — https://attio.com/pricing |
| PostHog | Website analytics for signup tracking | Free up to 1M events/mo — https://posthog.com/pricing |

**Play-specific cost: Free** (all tools within free tier at Smoke volume)

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

## Drills Referenced

- `icp-definition` — define the developer audience, pain points, and content pillars
- `newsletter-pipeline` — set up Loops, design the template, configure sending
- `threshold-engine` — evaluate pass/fail against subscriber and lead thresholds
