---
name: guest-post-pitch-outreach
description: Craft and send personalized guest post pitches to blog editors with topic proposals and author credentials
category: GuestPosting
tools:
  - Instantly
  - Attio
  - Clay
  - Anthropic
fundamentals:
  - media-pitch-email
  - instantly-campaign
  - attio-contacts
  - attio-notes
  - ai-guest-post-drafting
---

# Guest Post Pitch Outreach

This drill takes a qualified blog target list and executes personalized guest post pitch campaigns. It handles pitch angle generation, email personalization, sending, follow-up, and reply management. Pitches propose specific article topics and demonstrate why the author is qualified to write them.

## Input

- Scored blog target list from `guest-post-blog-discovery` drill (in Attio)
- Author credentials: name, role, company, expertise areas, previous publications
- 3-5 content pillars the author can write about
- 2-3 strategic landing page URLs for backlinks
- Company press kit or author bio page URL

## Steps

### 1. Generate pitch angles per blog

For each target blog, use `ai-guest-post-drafting` (pitch angle generation mode) to create 2-3 tailored pitch ideas. Feed the prompt:
- The blog's recent popular articles (from Clay enrichment data)
- The blog's audience description
- Content gaps: topics the blog hasn't covered recently but their audience would value
- The author's unique expertise or data that maps to those gaps

Select the strongest pitch per blog based on: (a) uniqueness of angle, (b) match to the blog's content themes, (c) natural fit for backlink placement.

### 2. Prepare pitch emails

**Guest Post Pitch Email (Day 0):**

```
Subject: Article idea for {{blog_name}}: {{article_title_short}}

Hi {{editor_first_name}},

I follow {{blog_name}} -- your recent piece on {{recent_article_topic}} {{specific_observation}}.

I'd like to contribute an article: "{{article_title}}."

This piece would cover:
- {{key_point_1}}
- {{key_point_2}}
- {{key_point_3}}

Why this fits your readers: {{relevance_explanation}}

About me: {{author_credentials_2_sentences}}. I've written for {{previous_publication_1}} and {{previous_publication_2}}.

I can send a full draft ({{target_word_count}} words) or just the outline for your review.

{{author_name}}
{{author_title}}, {{company}}
```

Rules:
- Under 150 words
- Reference a specific recent article on their blog
- Propose a concrete article topic with 3 clear takeaways
- Demonstrate author credibility with past publications
- Do NOT pitch your product. Pitch a useful article.

**Follow-up (Day 7):**

```
Subject: Re: Article idea for {{blog_name}}: {{article_title_short}}

Hi {{editor_first_name}},

Following up on my article pitch. I noticed {{recent_industry_trend_or_news}} -- I could incorporate this angle into the piece for extra timeliness.

Happy to adjust the topic if you have different editorial priorities right now.

{{author_name}}
```

Rules:
- One follow-up maximum per editor
- Tie to a timely event or offer flexibility
- If no response after follow-up, mark as "no response" and re-pitch in 3 months with a different topic

### 3. Personalize merge fields

For every target blog, populate from Clay data:

**Required fields:**
- `editor_first_name`
- `blog_name`
- `recent_article_topic` (from a specific article on their blog)
- `specific_observation` (genuine comment about that article)
- `article_title` (from pitch angle generation)
- `key_point_1`, `key_point_2`, `key_point_3`

**At Smoke level:** Write each personalization by hand after reading 2-3 recent articles on the blog.
**At Baseline+:** Use Clay columns for merge fields, with human review of Tier 1 pitches.

### 4. Send pitches

**Smoke (10-15 pitches):**
Send manually from the founder's personal email. Full hand-personalization. Track in a spreadsheet or Attio.

**Baseline (30-40 pitches):**
Use Instantly with the `instantly-campaign` fundamental:
1. Create campaign: `guest-post-pitch-{date}`
2. Upload contacts from Clay with merge fields mapped
3. Sending schedule: Tue-Thu, 9am-11am editor timezone (editors process submissions mid-morning)
4. Daily send limit: 10 per sending account
5. Set 1 follow-up at Day 7
6. Enable reply detection

**Scalable (100+ pitches):**
Use Instantly with inbox rotation across 2-3 sending accounts. Tier-based personalization: Tier 1 gets full hand-personalization, Tier 2 gets template + 4 merge fields, Tier 3 gets template + 2 merge fields.

### 5. Handle replies

Monitor Instantly and inbox. Classify and act:

- **"Send the full article"** or **"Send a draft"**: Run the `guest-post-article-pipeline` drill. Update Attio: status = "accepted." This is the win.
- **"Send an outline first"**: Generate a detailed 300-word outline with section headings, key points per section, and proposed word count. Update Attio: status = "outline_requested."
- **"We already have something on this"**: Propose an alternative angle on the same topic or a new topic. Update Attio: status = "redirected."
- **"Not accepting guest posts right now"**: Ask when they might reopen. Set a follow-up reminder. Update Attio: status = "paused."
- **"Not a fit"**: Thank them. Update Attio: status = "declined." Re-approach in 6 months only if your content offering changes significantly.
- **No reply after full sequence**: Update Attio: status = "no_response." Re-pitch in 3 months with an entirely different topic.

### 6. Track the pitch pipeline

Log every outreach attempt and outcome in Attio:

Pipeline stages: `pitched` -> `replied` -> `outline_requested` -> `accepted` -> `draft_submitted` -> `published`

Track conversion metrics:
- Pitch-to-reply rate (target: 15-25%)
- Reply-to-acceptance rate (target: 30-50% of positive replies)
- Overall pitch-to-publication rate (target: 8-15%)
- Average days from pitch to publication

## Output

- Personalized pitches sent to all blogs on the target list
- Attio pipeline updated with pitch status for every blog
- Accepted pitches queued for article writing via `guest-post-article-pipeline`
- Conversion metrics for optimizing future pitch batches

## Triggers

- Run once per batch of new blog targets from `guest-post-blog-discovery`
- Run weekly at Scalable level with new batches of 15-25 pitches
- Re-run quarterly for "no_response" contacts with fresh topics
