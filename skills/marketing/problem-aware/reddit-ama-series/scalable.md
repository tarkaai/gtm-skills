---
name: reddit-ama-series-scalable
description: >
  Reddit AMA Series — Scalable Automation. Scale to bi-weekly AMAs across 4-6 subreddits
  with agent-driven topic selection, automated Q&A preparation, A/B testing of AMA
  formats, and a content repurposing pipeline that multiplies each session's reach.
stage: "Marketing > ProblemAware"
motion: "CommunitiesForums"
channels: "Social, Communities"
level: "Scalable Automation"
time: "80 hours over 3 months"
outcome: "≥ 1,000 total referral sessions and ≥ 80 signups from AMAs and repurposed content over 3 months"
kpis: ["Referral sessions per AMA (avg)", "Signups per AMA (avg)", "Questions per AMA (avg)", "Referral sessions from repurposed AMA content", "Referral sessions per hour of engagement"]
slug: "reddit-ama-series"
install: "npx gtm-skills add marketing/problem-aware/reddit-ama-series"
drills:
  - community-monitoring-automation
  - community-health-scoring
  - content-repurposing
---

# Reddit AMA Series — Scalable Automation

> **Stage:** Marketing → ProblemAware | **Motion:** CommunitiesForums | **Channels:** Social, Communities

## Outcomes

Find the 10x multiplier for the AMA series. Scale from 3 sessions over 6 weeks to 6 sessions per month across 4-6 subreddits. Automate topic selection, Q&A preparation, and content repurposing so each AMA requires less human prep time while producing more downstream traffic. The agent does 80% of the work; the human hosts the live session and reviews drafts.

**Pass threshold:** ≥ 1,000 total referral sessions from reddit.com AND ≥ 80 signups attributed to reddit.com from both AMAs and repurposed AMA content over 3 months.

## Leading Indicators

- Agent-generated topic recommendations consistently match what the community engages with (≥ 70% of topics score above the series average in engagement)
- Pre-seeded Q&A bank accuracy improving: ≥ 85% of actual questions covered by prepared answers
- Time per AMA decreasing: human prep time drops from 3+ hours to under 1 hour per session
- Repurposed content producing ≥ 30% of total AMA-attributed referral sessions
- Community members proactively requesting specific AMA topics
- Cross-subreddit recognition: host is mentioned or tagged in threads outside the AMA

## Instructions

### 1. Expand to 4-6 target subreddits

Using data from the Baseline series and the `community-health-scoring` drill:

1. Rank your tested subreddits by referral sessions per AMA and signups per AMA
2. Keep the top 2 performers as anchor subreddits (host AMAs here every 4-6 weeks)
3. Add 2-4 new subreddits from your reconnaissance list, prioritizing:
   - Subreddits with 20,000-300,000 subscribers (engagement sweet spot for AMAs)
   - Active AMA history (other hosts getting 30+ upvotes on AMAs)
   - Different audience segments within your ICP (test which segments respond best)
4. Build engagement profiles for each new subreddit before the first AMA there

**Time estimate:** 3 hours

### 2. Automate the AMA preparation pipeline

Build an n8n workflow that automates the majority of the ama session planning workflow (see instructions below) prep work:

```
Schedule Trigger (14 days before next AMA)
  -> Reddit API Node: Pull top 50 posts from target subreddit (last 30 days)
  -> Reddit API Node: Search for recent questions matching ICP keywords
  -> Reddit API Node: Pull past AMAs in the subreddit (top engagement data)
  -> AI Agent Node (Claude):
     Input: Top posts, recent questions, past AMA data, host expertise areas,
            previous AMA performance data
     Prompt: "Generate 3 AMA topic recommendations for r/[SUBREDDIT].
       For each topic:
       1. Title (following the subreddit's AMA format)
       2. Why this topic (based on community interest signals)
       3. Expected engagement score (1-10, based on similar past content)
       4. 15 likely questions with draft answers
       Rank by expected engagement."
  -> Attio Node: Store recommendations as AMA planning notes
  -> Slack Node: Post top recommendation to #ama-series for human review
```

```
Trigger: Human approves topic (Slack reaction or webhook)
  -> AI Agent Node (Claude):
     Input: Approved topic, subreddit engagement profile, host bio
     Prompt: "Draft the full AMA post (title + body) and expand the Q&A bank
       to 20 entries. Follow these rules: [insert ama-session-planning format rules]"
  -> Slack Node: Post draft for human final review
  -> Google Sheets / Attio: Log AMA in the series calendar
```

This reduces human prep time from 3+ hours to 30-45 minutes of review per AMA.

**Time estimate:** 4 hours to build the automation

### 3. Scale to bi-weekly AMA cadence

With 4-6 subreddits and automated preparation, host AMAs on a bi-weekly schedule:

**Month 1 (4 AMAs):**
- Week 1: Anchor subreddit A (proven topic category)
- Week 2: New subreddit C (test)
- Week 3: Anchor subreddit B (proven topic category)
- Week 4: New subreddit D (test)

**Month 2 (4 AMAs):**
- Rotate through subreddits. Drop any new subreddit that underperformed (< 50% of anchor subreddit engagement). Replace with another candidate.

**Month 3 (4 AMAs):**
- Optimal rotation based on 2 months of data. Focus on the top 3-4 subreddits.

For each AMA:
1. Agent generates the prep package 14 days out (automated)
2. Human reviews and approves topic and draft (30 min, 7 days out)
3. Agent finalizes Q&A bank and schedules moderator outreach (automated)
4. Human hosts live session (2-3 hours)
5. Agent runs post-AMA analysis (automated)

**Human action required per AMA:** 30 min review + 2.5 hours live session = ~3 hours total.

### 4. A/B test AMA formats

Systematically test variations across sessions to maximize engagement:

**Test 1: AMA length (Month 1)**
- Sessions 1-2: Host for 2 hours
- Sessions 3-4: Host for 3 hours with a "round 2" announcement at the 2-hour mark
- Metric: questions asked, late-session upvotes, referral sessions

**Test 2: Post format (Month 2)**
- Sessions 5-6: Standard AMA format (bio + topic areas)
- Sessions 7-8: "Proof-first" format (lead with a specific data point or result, then offer the AMA)
- Metric: initial upvote velocity (first 30 minutes), total questions

**Test 3: Answer depth (Month 3)**
- Sessions 9-10: Concise answers (under 150 words each, answer more questions)
- Sessions 11-12: Deep answers (300-500 words, answer fewer questions with more substance)
- Metric: referral sessions per answer, average upvotes per answer

Track all test results in PostHog. Adopt winning variants for subsequent sessions.

### 5. Build the content repurposing pipeline

Automate content extraction from each AMA using `content-repurposing`:

```
Trigger: 48 hours after AMA post
  -> Reddit API Node: Fetch all Q&A pairs from the AMA
  -> Function Node: Rank Q&A pairs by upvotes, extract top 5
  -> AI Agent Node (Claude):
     Input: Top 5 Q&A pairs, host bio, product context
     Prompt: "Transform these AMA Q&A pairs into:
       1. A blog post: 'X Lessons from Our AMA on [Topic]' (800-1200 words)
       2. 5 standalone LinkedIn posts (one per Q&A pair, hook-insight-takeaway format)
       3. A newsletter section: 'Community Q&A Highlight' (300 words)
       Each piece must link back to the original AMA thread with UTM:
       ?utm_source=[channel]&utm_medium=content&utm_campaign=reddit-ama-series&utm_content=repurpose_session_[N]"
  -> Ghost API / CMS Node: Create draft blog post
  -> Slack Node: Queue social posts for human review and scheduling
  -> Loops API Node: Queue newsletter section for next broadcast
```

This ensures every AMA produces 7+ derivative content pieces without additional human writing time.

**Time estimate:** 3 hours to build the pipeline

### 6. Track cross-session performance with community health scoring

Run the `community-health-scoring` drill weekly to monitor the health of each AMA subreddit:

- Which subreddits are producing increasing vs. declining AMA engagement?
- Are any subreddits showing signs of AMA fatigue (declining questions session over session)?
- Which subreddits produce the highest referral-to-signup conversion rate?
- Is the repurposed content driving additional referral traffic between AMA sessions?

Use the weekly health scores to make subreddit rotation decisions: deprioritize declining subreddits, test replacements, and double down on high-converters.

### 7. Evaluate against threshold

At the end of 3 months, measure:

- Total referral sessions from reddit.com attributed to AMAs and repurposed AMA content: ≥ 1,000?
- Total signups attributed to reddit.com from AMA-related traffic: ≥ 80?
- Average referral sessions per AMA (should be improving over the 12 sessions)
- Referral sessions per hour of human engagement time (efficiency metric)
- What percentage of total referral sessions came from repurposed content vs. live AMAs?

**PASS (both thresholds met, efficiency improving):** Document the automation pipeline, winning AMA formats, optimal subreddit rotation, and repurposing workflow. Proceed to Durable.

**MARGINAL PASS (1,000+ sessions but <80 signups, or vice versa):** If sessions are high but signups are low, the issue is downstream conversion — review where AMA traffic lands and the signup flow. If signups are high but sessions are low, the existing traffic is high-quality; focus on scaling volume. Run 1 more month.

**FAIL:** Analyze whether the bottleneck is engagement (low upvotes/questions), traffic conversion (high engagement but low referral sessions), or signup conversion (high traffic but low signups). Each bottleneck has a different fix. If AMA engagement is declining across subreddits despite topic variation, the format may be saturated for your ICP.

## Time Estimate

| Activity | Time |
|----------|------|
| Subreddit expansion and profiling | 3 hours |
| AMA preparation pipeline (n8n build) | 4 hours |
| AMA review and approval (12 sessions x 30 min) | 6 hours |
| Live AMA sessions (12 sessions x 2.5h) | 30 hours |
| Post-AMA follow-up (12 sessions x 30 min) | 6 hours |
| Content repurposing pipeline (n8n build) | 3 hours |
| A/B test setup and analysis | 3 hours |
| Community health scoring review (weekly) | 6 hours |
| Final evaluation | 1 hour |
| **Total** | **~62 hours human time** |

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Reddit | Platform for AMA hosting | Free (personal account with existing karma) |
| PostHog | Event tracking, funnels, attribution, experiments | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | AMA prep pipeline, repurposing pipeline, monitoring | Self-hosted: Free / Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Claude API | Topic generation, Q&A drafting, content repurposing | ~$20-40/mo at 12 AMAs/mo ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Syften (optional) | Real-time monitoring between AMAs | Standard: $39.95/mo ([syften.com](https://syften.com)) |

**Estimated monthly cost:** $45-105/mo (n8n Cloud + Claude API + optional Syften)

## Drills Referenced

- the ama session planning workflow (see instructions below) — automated AMA preparation pipeline (topic selection, post drafting, Q&A bank)
- `community-monitoring-automation` — catch AMA-related engagement between sessions
- `community-health-scoring` — weekly subreddit health tracking to drive rotation decisions
- `content-repurposing` — automated pipeline transforming AMA Q&A into blog, social, and newsletter content
