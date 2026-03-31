---
name: alumni-campus-pro-orgs-scalable
description: >
  Alumni & Campus Outreach — Scalable Automation. Expand to 15-25 communities, automate content
  repurposing across platforms, run A/B tests on engagement approaches, and build the 10x multiplier
  through cross-community content amplification and systematic experimentation.
stage: "Marketing > Unaware"
motion: "Communities & Forums"
channels: "Communities, Other"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: "≥ 8 meetings booked over 2 months with cost per meeting < $50"
kpis: ["Meetings booked by community (monthly)", "Cost per meeting by community", "Referral sessions per hour invested", "Content repurposing ratio (derivatives per original)", "A/B test win rate", "Community portfolio coverage (active communities / total addressable)"]
slug: "alumni-campus-pro-orgs"
install: "npx gtm-skills add marketing/unaware/alumni-campus-pro-orgs"
drills:
  - ab-test-orchestrator
  - content-repurposing
  - community-monitoring-automation
---

# Alumni & Campus Outreach — Scalable Automation

> **Stage:** Marketing → Unaware | **Motion:** Communities & Forums | **Channels:** Communities, Other

## Outcomes

Find the 10x multiplier for community engagement. Scale from 3-5 communities to 15-25 without proportional effort increase by automating content repurposing, systematically testing engagement approaches, and upgrading monitoring to near-real-time. Agent handles monitoring, content adaptation, experiment design, and metric tracking. Human posts in gated communities and takes meetings.

## Leading Indicators

- 15-25 active communities with engagement activity in the last 7 days
- Content repurposing ratio ≥ 5:1 (5 derivative pieces per original)
- At least 2 A/B tests completed with statistically significant results
- Referral sessions per hour invested improving month-over-month
- Cost per meeting trending downward
- At least 1 meeting per week from community sources

## Instructions

### 1. Expand community portfolio to 15-25 targets

Re-run the `community-reconnaissance` drill with broader scope:

**Expand alumni networks:** Target universities beyond your own team's alma maters. Search for alumni groups at top-25 universities in your ICP's industry. Use Clay with the `community-directory-search` fundamental to find: `"{university} {industry} alumni"` across LinkedIn, Facebook, and standalone platforms (e.g., Alumnifire, GradConnection, PeopleGrove).

**Expand professional organizations:** Add national and regional chapters of professional associations. Search for: industry councils, standards bodies, certification communities, and trade associations. Target groups with 200-5,000 members (large enough for reach, small enough that your contributions are visible).

**Add adjacent communities:** Based on Baseline data, identify which community types produced the most meetings. If professional Slack communities outperformed alumni LinkedIn groups, weight the expansion toward more professional Slack communities.

Sort all communities into tiers:
- **Tier 1 (5-8 communities):** Proven meeting producers from Baseline. Daily engagement.
- **Tier 2 (8-12 communities):** High-potential communities matching Tier 1 profile. 2-3x/week engagement.
- **Tier 3 (5-8 communities):** Experimental communities testing new segments. 1x/week engagement.

### 2. Build cross-community content repurposing pipeline

Run the `content-repurposing` drill to create a system that turns 1 piece of content into 5-10 community-adapted versions:

**Step 1: Create the source content weekly.**
Write one substantial piece per week (800-1,200 words): a framework, case study, data analysis, or lessons-learned post. This is your "anchor content."

**Step 2: Adapt for each platform and community.**
Build an n8n workflow that takes the anchor content and generates adapted versions:

```
Manual Trigger (input: anchor content URL or text)
  → Function Node: Extract atomic units from the anchor:
      - 3-4 key insights (each → standalone social post)
      - 1-2 frameworks/lists (each → Slack thread or LinkedIn discussion)
      - 5-6 quotable lines (each → comment or reply)
      - 1 core argument (→ short-form post for smaller communities)
  → Function Node: For each target community, select the best atomic unit and adapt:
      - Match format to platform (LinkedIn post format vs Slack message vs Discord post)
      - Match tone to community culture (formal for professional orgs, casual for alumni Slack)
      - Adjust length (LinkedIn: 150-300 words, Slack: 50-150 words, Discord: 50-200 words)
      - Add community-specific context ("As a fellow {university} alum..." or "In our industry...")
  → Set Node: Attach UTM parameters unique to each community and platform
  → Airtable/Attio Node: Store all adapted versions with scheduled publish dates
```

**Step 3: Stagger publication.**
Spread derivatives across 2 weeks. Never post the same content to multiple communities on the same day. Adapt the hook and framing for each community even when the core insight is the same.

Target: 1 anchor piece → 5-10 adapted posts per week across 15-25 communities.

### 3. Upgrade monitoring to near-real-time

Run the `community-monitoring-automation` drill with Scalable-level upgrades:

**Upgrade from polling to webhooks/streaming where possible:**
- Slack: Use Slack Events API (real-time) instead of polling
- Discord: Use Discord Gateway (WebSocket, real-time) instead of REST polling
- Syften: Upgrade to Pro plan ($99.95/mo) for 100 filters, webhooks, and AI post-processing

**Add intelligent routing:**
Expand the n8n alert workflow with an AI classification step:

```
Webhook/Event Trigger (real-time from Slack/Discord/Syften)
  → Function Node: Normalize fields
  → HTTP Request Node (Claude API): Classify the thread:
      - "buying_intent": Someone asking for recommendations or comparing solutions → HIGH priority
      - "pain_point": Someone describing a problem you solve → MEDIUM priority
      - "thought_leadership": Active discussion where your expertise adds value → MEDIUM priority
      - "competitor_mention": Someone discussing a competitor → LOW priority
      - "noise": Off-topic or already well-answered → SKIP
  → Switch Node: Route by classification
  → Slack Alert Node: Post to #community-engagement with priority, suggested response type, and draft talking points
```

Target: Response time < 2 hours for HIGH priority, < 6 hours for MEDIUM.

### 4. Run A/B tests on engagement approaches

Run the `ab-test-orchestrator` drill to test and optimize community engagement:

**Test 1 — Content format (weeks 1-3):**
- Control: Standard text posts (insight + discussion question)
- Variant: Structured posts (numbered list + specific example + explicit ask)
- Metric: Replies per post
- Split: Alternate formats across comparable communities
- Minimum sample: 20 posts per variant

**Test 2 — CTA approach (weeks 3-5):**
- Control: Soft CTA ("Happy to chat more about this")
- Variant: Specific CTA ("I put together a more detailed breakdown — DM me and I will send it")
- Metric: DMs received per post
- Split: Alternate CTAs within the same communities
- Minimum sample: 20 posts per variant

**Test 3 — Engagement timing (weeks 5-7):**
- Control: Post during standard business hours (9am-5pm)
- Variant: Post during off-peak hours (7-9am, 5-8pm) when competition for attention is lower
- Metric: Engagement rate (reactions + replies / impressions)
- Split: Alternate timing within the same communities
- Minimum sample: 20 posts per variant

**Test 4 — Community introduction approach (weeks 7-9):**
- Control: Jump straight into value content
- Variant: Post a brief introduction first ("I am an {affiliation} alum working on {topic}"), then follow up with value content 2-3 days later
- Metric: Meeting conversion rate
- Split: Use for new Tier 3 communities
- Minimum sample: 10 communities per variant

For each test: document hypothesis, run for planned duration, evaluate with statistical rigor, implement winner permanently.

### 5. Track efficiency metrics

Create a PostHog dashboard: "Alumni & Campus — Scalable Performance"

Panels:
- Meetings booked by community (bar chart, last 30 days)
- Cost per meeting by community (table: community name, hours invested, tool cost, total cost, meetings, cost per meeting)
- Referral sessions per hour invested (line chart, weekly trend)
- Content repurposing ratio (metric: adapted pieces / anchor pieces this month)
- Community tier performance (table: tier, communities count, meetings, avg engagement rate)

Set alerts:
- Any Tier 1 community drops below 2 referral sessions/week → investigate
- Cost per meeting exceeds $50 for any community → review efficiency
- Overall meeting rate drops below 1/week → diagnose

### 6. Evaluate against threshold

After 2 months, measure against: **≥ 8 meetings booked over 2 months with cost per meeting < $50**.

Calculate cost per meeting: (tool costs + estimated hourly cost of time invested) / meetings booked.

**PASS:** Proceed to Durable. Document the community portfolio, winning content formats, optimal engagement cadence, and cost per meeting by community.
**FAIL:** If meetings ≥ 8 but cost > $50: optimize efficiency — drop low-performing communities, improve content repurposing. If meetings < 8: expand to more communities or increase posting frequency in high-performers. Re-run Scalable for another 4-week cycle.

## Time Estimate

- Community expansion and profiling: 4 hours
- Content repurposing pipeline build: 6 hours
- Monitoring upgrade: 4 hours
- Weekly content creation and engagement (8 weeks): 20 hours
- A/B test design and analysis: 4 hours
- Dashboard and evaluation: 2 hours
- **Total: 40 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Attribution, funnels, A/B test analysis, dashboards | Free tier: 1M events/mo (https://posthog.com/pricing) |
| n8n | Monitoring automation, content repurposing pipeline, alert routing | €24/mo Starter or €60/mo Pro cloud; free self-hosted (https://n8n.io/pricing) |
| Syften | Near-real-time keyword monitoring across platforms | $99.95/mo Pro plan for 100 filters + webhooks (https://syften.com/) |
| Clay | Community discovery and enrichment for portfolio expansion | $185/mo Launch plan (https://clay.com/pricing) |
| Attio | Community portfolio management, contact attribution | Free tier available (https://attio.com/pricing) |

**Estimated play-specific cost at Scalable level:** $100-350/mo (Syften Pro + n8n cloud + Clay if expanding actively)

## Drills Referenced

- `ab-test-orchestrator` — design, run, and evaluate A/B tests on content formats, CTAs, timing, and introduction approaches
- `content-repurposing` — build the pipeline that turns 1 anchor piece into 5-10 community-adapted versions per week
- `community-monitoring-automation` — upgrade to near-real-time monitoring with AI classification and intelligent routing
