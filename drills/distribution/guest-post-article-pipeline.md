---
name: guest-post-article-pipeline
description: Write, review, and submit guest articles with strategic backlink placement for accepted pitches
category: GuestPosting
tools:
  - Anthropic
  - Attio
  - PostHog
fundamentals:
  - ai-guest-post-drafting
  - attio-notes
  - attio-contacts
  - posthog-custom-events
---

# Guest Post Article Pipeline

This drill converts accepted guest post pitches into published articles. It covers article drafting via AI, editorial review, backlink placement strategy, submission to blog editors, and post-publication tracking setup.

## Input

- Accepted pitch details from `guest-post-pitch-outreach` (blog name, editor contact, approved topic, editorial guidelines)
- 3-5 recent articles from the target blog (for style matching)
- Strategic backlink URLs: 2-3 pages on your site to link to (prioritize high-value content, not homepage)
- Author bio, headshot, and credentials
- Target word count (typically from editor or blog guidelines; default 1,200-1,800 words)

## Steps

### 1. Research the target blog's style

Before generating any draft, analyze 3-5 recent articles from the target blog:
- **Tone**: Formal/academic vs. conversational vs. punchy?
- **Structure**: Long-form narrative vs. listicle vs. how-to with numbered steps?
- **Heading style**: H2 only? H2+H3? Questions as headings?
- **Formatting**: Do they use bullet points, code blocks, pull quotes, images?
- **Length**: Average word count of recent posts
- **Backlink conventions**: Do existing articles include external links? How many per article? Dofollow or nofollow?

Document these observations. They feed into the AI drafting prompt.

### 2. Plan backlink placement

For each article, identify 2-3 strategic backlink opportunities:

**Rules for natural backlink placement:**
- The linked page must be directly relevant to the sentence where it appears
- The link must provide additional value the reader would actually want to click
- Place backlinks in the body of the article, not the intro or conclusion (editors delete those first)
- Use descriptive anchor text that describes the destination content, not "click here" or your brand name
- If the blog has a nofollow policy, the backlinks still drive referral traffic and brand awareness

**Priority order for link targets:**
1. High-value content pages (guides, tools, research) that provide genuine extra value
2. Product pages that directly solve a problem discussed in the article
3. Author bio link to company homepage (this one is almost always allowed)

### 3. Generate the article draft

Use `ai-guest-post-drafting` with:
- Target blog's style analysis from step 1
- 3 example articles as style reference
- Editorial guidelines from the blog
- Approved topic and key points from the accepted pitch
- Backlink URLs and their placement context
- Author voice notes

The AI generates a full draft matching the blog's editorial standards.

### 4. Review and refine the draft

Run the editorial review prompt from `ai-guest-post-drafting` to check:
- Style match against the target blog (PASS/FAIL)
- Backlink naturalness (PASS/FAIL)
- Content quality: actionable, original, not promotional (PASS/FAIL)
- Word count within ±10% of target (PASS/FAIL)

If any check fails, regenerate with adjusted parameters.

**Human action required:** The author must read the final draft and:
1. Add personal anecdotes, specific data, or proprietary insights the AI cannot fabricate
2. Verify all claims and statistics are accurate
3. Ensure the article represents their genuine expertise and opinion
4. Confirm backlinks feel natural and add value
5. Approve for submission

### 5. Submit to the editor

Send the final article to the editor via email reply to the original pitch thread:

```
Hi {{editor_first_name}},

Here's the completed article: "{{article_title}}"

Word count: {{word_count}}
Author bio: {{author_bio_2_sentences}}
Author headshot: {{headshot_url}}

I've included {{backlink_count}} references to related resources where they add context for your readers. Let me know if you'd like any revisions.

{{author_name}}
```

Attach the article as both:
- Inline in the email body (for quick reading)
- Google Doc or Markdown file link (for editor markup)

Update Attio: status = "draft_submitted"

### 6. Handle editorial feedback

- **"Accepted as-is"**: Confirm publication date. Update Attio: status = "scheduled."
- **"Minor edits needed"**: Make requested changes within 24 hours. Respond promptly — editors work on tight schedules.
- **"Remove a backlink"**: Comply immediately. One backlink is better than zero published articles. Keep the author bio link.
- **"Major rewrite needed"**: Regenerate the affected sections using AI with the editor's specific feedback. Re-submit within 48 hours.
- **"Rejected after acceptance"**: Rare but happens. Thank the editor, ask what would work better, and offer a new topic. Repurpose the article for your own blog.

### 7. Configure post-publication tracking

When the article goes live, use `posthog-custom-events` to set up tracking:

- Create UTM-tagged URLs for all backlinks in the article: `?utm_source={{blog_domain}}&utm_medium=guest_post&utm_campaign={{article_slug}}`
- **If the editor accepts UTM parameters**: provide UTM-tagged URLs before publication
- **If UTM parameters are stripped**: track via PostHog referrer matching (`referrer contains {{blog_domain}}`)

Track these events per guest post:
- `guest_post_referral_visit`: pageview where referrer matches the publishing blog's domain
- `guest_post_signup`: conversion event (signup, demo request) from a guest post referral visitor
- `guest_post_engagement`: scroll depth >50% or time on page >30s from guest post referral visitor

Log in Attio: publication URL, publication date, backlink URLs, initial referral traffic after 7 days.

## Output

- Published guest article on the target blog
- Strategic backlinks pointing to your site
- PostHog tracking configured for referral traffic attribution
- Attio pipeline updated: status = "published" with publication URL and date

## Triggers

- Run for each accepted pitch from `guest-post-pitch-outreach`
- Target turnaround: 48-72 hours from pitch acceptance to draft submission
- At Scalable level, batch 3-5 articles per week
