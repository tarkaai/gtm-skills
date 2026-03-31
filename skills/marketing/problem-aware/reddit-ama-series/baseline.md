---
name: reddit-ama-series-baseline
description: >
  Reddit AMA Series — Baseline Run. Host 3 AMAs across 2-3 subreddits over 6 weeks
  with full PostHog event tracking, UTM attribution, and structured performance
  comparison to prove the format produces repeatable referral traffic and leads.
stage: "Marketing > ProblemAware"
motion: "CommunitiesForums"
channels: "Social, Communities"
level: "Baseline Run"
time: "25 hours over 6 weeks"
outcome: "≥ 200 total referral sessions and ≥ 15 signups across 3 AMAs in 6 weeks"
kpis: ["Referral sessions from reddit.com (per AMA and cumulative)", "Signups attributed to reddit.com", "Average upvotes per AMA", "Average questions per AMA", "Content repurposing assets produced"]
slug: "reddit-ama-series"
install: "npx gtm-skills add marketing/problem-aware/reddit-ama-series"
drills:
  - community-monitoring-automation
  - content-repurposing
  - threshold-engine
---

# Reddit AMA Series — Baseline Run

> **Stage:** Marketing → ProblemAware | **Motion:** CommunitiesForums | **Channels:** Social, Communities

## Outcomes

Prove that a recurring AMA series produces repeatable referral traffic and signups — not just a one-time spike. Host 3 AMAs across 2-3 subreddits, implement full tracking, and repurpose the best content. Baseline proves the play works when sustained, not just when novel.

**Pass threshold:** ≥ 200 total referral sessions from reddit.com AND ≥ 15 signups attributed to reddit.com across 3 AMA sessions in 6 weeks.

## Leading Indicators

- Each successive AMA maintains or improves on the previous session's engagement (no declining trend)
- Referral traffic persists between AMAs (long-tail traffic from older AMA threads)
- Repurposed AMA content generates additional referral sessions beyond the live session
- Community members start recognizing the host by name in threads
- Inbound DMs or emails mentioning the AMA series

## Instructions

### 1. Implement AMA-specific event tracking

Set up PostHog custom events for the AMA series:

```javascript
posthog.capture('ama_session_posted', {
    subreddit: 'r/TARGET',
    topic: 'topic-slug',
    host: 'host-name',
    session_number: 1,
    scheduled_duration_hours: 2
});

posthog.capture('ama_referral_visit', {
    subreddit: 'r/TARGET',
    session_number: 1,
    source_url: 'https://reddit.com/r/TARGET/comments/...'
});

posthog.capture('ama_signup', {
    subreddit: 'r/TARGET',
    session_number: 1,
    attribution_url: 'https://reddit.com/r/TARGET/comments/...'
});
```

Create PostHog saved insights:
1. **AMA referral trend:** daily `ama_referral_visit` events broken down by `session_number`, last 6 weeks
2. **AMA signup attribution:** `ama_signup` events grouped by `subreddit` and `session_number`
3. **AMA conversion funnel:** `ama_referral_visit` → pricing/docs page viewed → `signup_started` → `signup_completed`, filtered by `utm_campaign=reddit-ama-series`

All links in AMA answers must include UTM parameters:
```
?utm_source=reddit&utm_medium=community&utm_campaign=reddit-ama-series&utm_content=r_SUBREDDIT_ama_SESSION_NUMBER_TOPIC
```

**Time estimate:** 1.5 hours

### 2. Plan and schedule the 3-AMA series

Run the the ama session planning workflow (see instructions below) drill three times, once per session, spaced 2 weeks apart:

**Session 1 (Week 1):** Return to the subreddit from the Smoke test (proven ground). Choose a new topic building on what worked — if the Smoke AMA's top questions were about [X], go deeper on [X].

**Session 2 (Week 3):** Try a second subreddit from your reconnaissance list. Choose a topic tailored to that community's specific interests. This tests whether the format transfers across subreddits.

**Session 3 (Week 5):** Host in whichever subreddit performed better (Session 1 or 2). Use a topic informed by the most-upvoted questions from previous sessions — the community is telling you what they want to hear about.

For each session, the agent produces:
- AMA topic recommendation with scoring rationale
- Drafted AMA post (title + body)
- Pre-seeded Q&A bank (15-20 entries)
- Moderator outreach message (if needed for new subreddit)

**Human action required:** Approve topics and post drafts. Handle moderator communication. Host all 3 live sessions.

**Time estimate:** 3 hours agent prep per session + 30 minutes human review per session = ~10.5 hours total

### 3. Set up monitoring between AMAs

Run the `community-monitoring-automation` drill to catch engagement between AMA sessions:

Build an n8n polling workflow (free) that checks target subreddits every 4 hours for:
- New questions referencing your previous AMA ("I saw [host]'s AMA about [topic] and wanted to ask...")
- Threads where your AMA answers are being cited or linked by other users
- New threads on topics you covered in the AMA (opportunity to comment with deeper context)

Route alerts to Slack. Between AMAs, respond to any threads that reference your sessions — this extends the AMA's reach and builds ongoing community presence.

**Time estimate:** 2 hours setup

### 4. Host each live AMA session

For each of the 3 sessions, follow the live execution protocol from the ama session planning workflow (see instructions below):

1. Post the AMA at the optimal time (based on subreddit peak activity hours from your engagement profile)
2. Agent monitors incoming questions in real-time (polling every 2 minutes)
3. Agent surfaces pre-seeded answers for matching questions, drafts outlines for new questions
4. Host answers live for 2-3 hours, returns 6-12 hours later for stragglers
5. Target ≥ 90% response rate on on-topic questions
6. Within 24 hours, run post-AMA follow-up: metrics collection, unanswered question cleanup, content flagging

**Time estimate:** 3 hours per session (live + follow-up) = 9 hours total

### 5. Repurpose top AMA content

After each AMA, run the `content-repurposing` drill on the top 3-5 Q&A pairs:

- **Blog post:** Combine the best answers into a "Lessons from our AMA on [topic]" post. Expand each answer with additional context. Link back to the AMA thread.
- **Social posts:** Pull 3-5 standalone insights from your answers. Reformat as LinkedIn or Twitter posts with the hook-insight-takeaway structure.
- **Newsletter section:** Include a "Community Q&A" section in your next newsletter featuring the most interesting exchange.

Each repurposed piece should link back to the original AMA (drives long-tail Reddit traffic) and include UTM parameters for attribution.

**Time estimate:** 2 hours per AMA = 6 hours total

### 6. Compare session performance

After all 3 AMAs, build a comparison table:

| Metric | Session 1 | Session 2 | Session 3 | Trend |
|--------|-----------|-----------|-----------|-------|
| Subreddit | | | | |
| Topic | | | | |
| Upvotes | | | | |
| Questions asked | | | | |
| Response rate | | | | |
| Referral sessions (7-day) | | | | |
| Signups (7-day) | | | | |
| Repurposed assets created | | | | |
| Referral sessions from repurposed content | | | | |

Analyze:
- Is engagement improving, stable, or declining across sessions?
- Which subreddit produces more referral traffic per AMA?
- Which topics generated the most questions and the highest-quality answers?
- Does repurposed content contribute measurable additional referral traffic?

### 7. Evaluate against threshold

Run the `threshold-engine` drill at the end of 6 weeks:

**Metrics to check:**
- Total referral sessions from reddit.com over 6 weeks (from both AMAs and repurposed content): ≥ 200?
- Total signups attributed to reddit.com over 6 weeks: ≥ 15?
- Engagement trend across 3 sessions: stable or improving?

**PASS (both session and signup thresholds met, trend not declining):** Document the winning subreddits, topic categories, and repurposing pipeline. Proceed to Scalable.

**MARGINAL PASS (one threshold met, the other within 80%):** Run 1-2 more AMA sessions focusing on the highest-performing subreddit. Re-evaluate.

**FAIL:** Analyze whether the issue is subreddit selection (wrong audience), topic selection (low relevance), host credibility (insufficient karma/history), or timing. If 2 of 3 sessions underperformed significantly, the AMA format may not fit your ICP's Reddit behavior. Consider pivoting to the `reddit-niche-communities` play (comment-based engagement) instead.

## Time Estimate

| Activity | Time |
|----------|------|
| PostHog event tracking setup | 1.5 hours |
| AMA planning (3 sessions x 3.5h) | 10.5 hours |
| Monitoring setup between AMAs | 2 hours |
| Live AMA sessions (3 x 3h) | 9 hours |
| Content repurposing (3 x 2h) | 6 hours |
| Performance comparison and evaluation | 1 hour |
| **Total** | **~30 hours** |

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Reddit | Platform for AMA hosting | Free (personal account with existing karma) |
| PostHog | Event tracking, funnels, AMA attribution | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Between-AMA monitoring workflow | Self-hosted: Free / Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated monthly cost:** $0-24/mo (n8n Cloud optional)

## Drills Referenced

- the ama session planning workflow (see instructions below) — end-to-end AMA preparation, live support, and follow-up for each session
- `community-monitoring-automation` — catch engagement and references between AMA sessions
- `content-repurposing` — transform top AMA Q&A pairs into blog, social, and newsletter content
- `threshold-engine` — pass/fail evaluation across the 3-session series
