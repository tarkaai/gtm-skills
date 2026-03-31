---
name: reddit-ama-series-smoke
description: >
  Reddit AMA Series — Smoke Test. Host one AMA in a target subreddit where your
  ICP is active. Prove that a structured Ask Me Anything session generates referral
  traffic and inbound interest from problem-aware audiences.
stage: "Marketing > ProblemAware"
motion: "CommunitiesForums"
channels: "Social, Communities"
level: "Smoke Test"
time: "8 hours over 2 weeks"
outcome: "≥ 50 upvotes and ≥ 20 questions on first AMA, with ≥ 10 referral sessions to your site"
kpis: ["AMA post upvotes", "Questions asked (top-level comments)", "Referral sessions from reddit.com", "Response rate (questions answered / questions asked)"]
slug: "reddit-ama-series"
install: "npx gtm-skills add marketing/problem-aware/reddit-ama-series"
drills:
  - community-reconnaissance
  - community-content-posting
---

# Reddit AMA Series — Smoke Test

> **Stage:** Marketing → ProblemAware | **Motion:** CommunitiesForums | **Channels:** Social, Communities

## Outcomes

Prove that hosting a structured AMA session on Reddit generates meaningful engagement and referral traffic from problem-aware audiences. This is a single-session test: one AMA, one subreddit, no automation. The agent handles research and preparation; the human hosts the live session.

**Pass threshold:** ≥ 50 upvotes on the AMA post AND ≥ 20 questions asked AND ≥ 10 referral sessions to your site within 7 days of the AMA.

## Leading Indicators

- Moderator approval received within 5 days of outreach (if required)
- Pre-seeded Q&A bank covers ≥ 80% of actual questions asked
- Upvotes accumulating during the live session (not just after)
- Follow-up DMs from community members after the AMA
- PostHog shows referral traffic from reddit.com within 24 hours of the AMA

## Instructions

### 1. Discover and select the target subreddit

Run the `community-reconnaissance` drill to identify 5-10 subreddits where your ICP participates. From the ranked list, select ONE subreddit for the first AMA based on these additional AMA-specific criteria:

- Has hosted successful AMAs before (search for "AMA" in the subreddit and check engagement levels)
- Subscriber count between 10,000 and 500,000 (large enough for engagement, small enough to not get buried)
- Active moderation that responds to messages (check mod activity in recent threads)
- No rule explicitly banning AMAs or self-promotion posts

Using the `reddit-api-read` fundamental:
```
GET https://oauth.reddit.com/r/SUBREDDIT/search?q=AMA&restrict_sr=true&sort=top&t=year&limit=25
```

If top AMAs in the subreddit get 50+ upvotes and 20+ questions, it is a viable AMA subreddit. If past AMAs get single-digit engagement, choose a different subreddit.

**Time estimate:** 2 hours

### 2. Plan the AMA session

Run the the ama session planning workflow (see instructions below) drill. This produces:

1. **Topic and angle:** A specific, value-first AMA topic based on what the community is discussing and what the host can uniquely contribute. Frame around expertise and experience, not company promotion.

2. **Moderator outreach:** If the subreddit requires mod approval, draft and send a message to the mod team. Allow 5-7 days for response.

3. **AMA post draft:** Title and body following the subreddit's established AMA format. The title must lead with credentials/experience, not company name. The body establishes context and lists 3-5 specific topic areas to seed questions.

4. **Pre-seeded Q&A bank:** 15-20 prepared answers to the most likely questions, based on analysis of recent subreddit threads and past AMAs on similar topics. Each answer follows the `community-response-crafting` format: direct answer first, specific numbers, under 300 words.

**Human action required:** Send the moderator message from the host's personal Reddit account (must have existing karma and history). Review and approve the AMA post draft and Q&A bank.

**Time estimate:** 3 hours (agent prep) + 30 minutes (human review)

### 3. Set up basic tracking

Ensure PostHog is tracking website visits. Verify that visits from `reddit.com` appear in PostHog under the `$referrer` or `$initial_referring_domain` property.

Create a PostHog insight: pageviews where `$initial_referring_domain` contains `reddit.com`, broken down by day, for the next 14 days.

Any links included in AMA answers must include UTM parameters:
```
?utm_source=reddit&utm_medium=community&utm_campaign=reddit-ama-series&utm_content=r_SUBREDDIT_ama_TOPIC
```

**Time estimate:** 15 minutes

### 4. Execute the live AMA

**Human action required:** The host posts the AMA and answers questions live for 2-3 hours.

Agent support during the live session:
1. Monitor incoming questions by polling the AMA post every 2 minutes
2. Match new questions against the pre-seeded Q&A bank
3. For matching questions, surface the prepared answer for the host to customize and post
4. For new questions, generate a draft response outline
5. Flag high-upvoted unanswered questions so the host prioritizes them
6. Track which questions have been answered vs. pending

Rules for the live session:
- Answer every question that is on-topic (target ≥ 90% response rate)
- Prioritize questions by upvote count (highest first)
- Keep answers specific: use numbers, timelines, examples
- If someone asks about your product directly, answer honestly but briefly — do not turn it into a pitch
- Stay active for at least 2 hours. Return 6-12 hours later to answer late arrivals.

**Time estimate:** 2-3 hours live + 30 minutes follow-up

### 5. Post-AMA follow-up

Within 24 hours, run the post-AMA follow-up from the the ama session planning workflow (see instructions below) drill:

1. Fetch all questions and answers from the AMA post
2. Calculate metrics: total questions, response rate, total upvotes, average upvotes per answer
3. Answer any remaining unanswered questions
4. Identify the top 5 most-upvoted Q&A pairs — flag these for content repurposing (blog posts, social content)
5. Log all metrics in the activity log

**Time estimate:** 30 minutes

### 6. Evaluate against threshold

After 7 days, check PostHog and the AMA post:

- AMA post upvotes: ≥ 50?
- Total questions asked (top-level comments that are questions): ≥ 20?
- Referral sessions from reddit.com in the 7 days after the AMA: ≥ 10?

**PASS (all three thresholds met):** Document which subreddit, topic, and answer styles worked best. Identify the 5 strongest Q&A pairs for repurposing. Proceed to Baseline.

**PARTIAL PASS (2 of 3 met):** Analyze which threshold was missed. If upvotes were low but questions were high, the topic resonated but the post didn't get enough initial visibility (timing issue). If referral sessions were low, review whether answers included enough relevant links. Try one more AMA in the same or a different subreddit.

**FAIL (fewer than 2 thresholds met):** Review: Was this the right subreddit? Was the topic relevant to the community? Did the host's credentials establish authority? Consider running a second attempt with a different subreddit/topic combination before abandoning the play.

## Time Estimate

| Activity | Time |
|----------|------|
| Community reconnaissance and subreddit selection | 2 hours |
| AMA planning (topic, post draft, Q&A bank) | 3.5 hours |
| PostHog tracking setup | 15 minutes |
| Live AMA session | 2.5 hours |
| Post-AMA follow-up and late answers | 30 minutes |
| Evaluation | 15 minutes |
| **Total** | **~9 hours** |

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Reddit | Platform for hosting the AMA | Free (personal account with existing karma) |
| PostHog | Track referral traffic and signups from the AMA | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |

## Drills Referenced

- `community-reconnaissance` — discover and rank target subreddits for AMA hosting
- the ama session planning workflow (see instructions below) — end-to-end AMA preparation: topic selection, post drafting, Q&A bank, live support
- `community-content-posting` — format guidelines for Reddit-native content
