---
name: ama-session-planning
description: Plan, schedule, execute, and follow up on Reddit AMA sessions in target subreddits
category: Community
tools:
  - Reddit API
  - AI (Claude / GPT)
  - Attio
  - PostHog
fundamentals:
  - reddit-api-read
  - reddit-api-write
  - subreddit-research
  - community-engagement-tracking
  - attio-contacts
  - attio-notes
---

# AMA Session Planning

This drill covers the end-to-end workflow for hosting a Reddit AMA (Ask Me Anything): topic selection, subreddit outreach, scheduling, live execution, answer drafting, and post-session follow-up. Designed for an AI agent to prepare everything, with the human executing the live session.

## Input

- Target subreddit engagement profiles (from `community-reconnaissance` drill)
- The host's expertise areas, bio, and credentials
- Previous AMA performance data (if any)
- Product positioning and ICP definition

## Steps

### 1. Select AMA topic and angle

Using the `reddit-api-read` fundamental, pull the top 50 posts from each target subreddit over the past month:

```
GET https://oauth.reddit.com/r/SUBREDDIT/top?t=month&limit=50
```

Analyze:
- Which topics get the most engagement (upvotes + comments)?
- What questions keep recurring that the host can answer authoritatively?
- What recent industry events or trends are generating discussion?
- What content gaps exist (questions asked but not well answered)?

Score each candidate topic on:
| Factor | Weight |
|--------|--------|
| Relevance to host expertise | 30% |
| Community interest (based on engagement data) | 30% |
| Differentiation (not already covered by another AMA) | 20% |
| Connection to product problem-space (without being promotional) | 20% |

Select the highest-scoring topic. Frame it as a value-first angle: "I spent 3 years building [X] and learned [Y]" not "I'm the CEO of [Company], AMA."

### 2. Research subreddit AMA norms

Using `reddit-api-read`, search for previous AMAs in the target subreddit:

```
GET https://oauth.reddit.com/r/SUBREDDIT/search?q=AMA&restrict_sr=true&sort=top&t=year&limit=25
```

For each past AMA, record:
- Title format used
- Number of questions asked
- Host's response rate and depth
- How the host was introduced (credentials, not company)
- Whether the mods scheduled it or the host posted directly
- Flair requirements
- Day of week and time posted

Also check subreddit rules for AMA-specific policies:
```
GET https://oauth.reddit.com/r/SUBREDDIT/about/rules
```

Some subreddits require mod pre-approval. Others have designated AMA days. Note all requirements.

### 3. Contact moderators (if required)

If the subreddit requires mod approval for AMAs, draft a message to the mod team:

```
POST https://oauth.reddit.com/api/compose
to=/r/SUBREDDIT
subject=AMA Request: [Topic] — [Host Name]
text=Hi mods,

I'd like to host an AMA in r/SUBREDDIT about [TOPIC].

Background: [HOST_BIO — 2-3 sentences on credentials, NOT company pitch]

I've been active in this community [reference specific past contributions if any]. The AMA would focus on [SPECIFIC_VALUE_TOPICS] based on [X years/months] of experience.

Happy to work with your scheduling preferences. Let me know if you need any additional info.

Thanks,
[NAME]
```

**Human action required:** Send this message from the host's personal Reddit account. Log the outreach and mod response in Attio using `attio-notes`.

### 4. Prepare the AMA post

Draft the AMA announcement post following the subreddit's established format. Standard structure:

**Title:** `I'm [Name], [credential/experience that establishes authority]. AMA about [topic]!`

**Body:**
```markdown
Hi r/[SUBREDDIT],

I'm [Name]. [2-3 sentences establishing credibility through experience, NOT company promotion].

Over the past [time], I've [specific accomplishment or experience relevant to the topic]. I've [second relevant credential].

I'm here for the next [2-3] hours to answer questions about:
- [Specific topic area 1]
- [Specific topic area 2]
- [Specific topic area 3]

Ask me anything!

**Proof:** [link to verification if required by subreddit — Twitter post, LinkedIn, etc.]
```

Rules:
- Do NOT mention the company name in the title
- Do NOT link to product pages
- Credentials must be experience-based ("built 3 SaaS products" not "CEO of Acme Inc")
- Include 3-5 specific topic areas to seed good questions
- Prepare a verification method if the subreddit requires proof

### 5. Pre-seed question bank

Before the AMA goes live, the agent prepares answers to the 15-20 most likely questions. Generate these by:

1. Pulling the most common questions from the subreddit's recent threads (using `reddit-api-read`)
2. Identifying questions from past AMAs on similar topics
3. Anticipating pushback or skepticism the community might have

For each expected question, draft a response following `community-response-crafting` format rules:
- Lead with the direct answer
- Be specific with numbers and examples
- Keep under 300 words
- No self-promotion unless directly asked about your product
- Include dissenting views where honest

Store the Q&A bank as structured data for the host to reference during the live session.

### 6. Execute the live AMA

**Human action required:** The host posts the AMA and answers questions live for 2-3 hours.

Agent responsibilities during the AMA:
1. Monitor incoming questions in real-time using `reddit-api-read` (poll every 2 minutes):
   ```
   GET https://oauth.reddit.com/r/SUBREDDIT/comments/POST_ID?sort=new&limit=100
   ```
2. Categorize each new question: matches pre-seeded Q&A, requires fresh answer, off-topic, hostile
3. For questions matching the pre-seeded bank, surface the prepared answer for the host to customize
4. For new questions, draft a response outline the host can expand on
5. Track which questions are answered vs unanswered
6. Flag high-upvoted questions that haven't been answered yet

### 7. Post-AMA follow-up

Within 24 hours after the AMA:

1. Using `reddit-api-read`, pull all questions and the host's answers
2. Calculate engagement metrics:
   - Total questions asked
   - Questions answered (response rate)
   - Total upvotes on the AMA post
   - Average upvotes per answer
   - New followers/DMs received
3. Log all metrics using `community-engagement-tracking`
4. Update Attio with AMA results using `attio-notes`
5. Identify the top 5 most-upvoted questions and answers for content repurposing
6. Reply to any unanswered questions that accumulated after the live window closed

## Output

- AMA topic and angle recommendation (scored)
- Drafted AMA post (title + body)
- Pre-seeded Q&A bank (15-20 entries)
- Live session support (question triage + draft answers)
- Post-AMA engagement metrics report
- Top answers flagged for content repurposing

## Triggers

- Run once per AMA session (typically monthly at Baseline, bi-weekly at Scalable)
- Topic selection runs 2 weeks before the AMA date
- Post preparation runs 3-5 days before
- Follow-up runs within 24 hours after
