---
name: infographic-distribution
description: Distribute infographics across social platforms and conduct backlink outreach to industry sites and bloggers
category: Content
tools:
  - LinkedIn
  - Ahrefs
  - Instantly
  - n8n
  - Clay
fundamentals:
  - linkedin-organic-posting
  - linkedin-organic-engagement
  - ahrefs-backlink-analysis
  - instantly-campaign
  - clay-people-search
  - og-meta-generation
---

# Infographic Distribution

This drill takes a finished infographic (images + companion copy from the `infographic-creation-pipeline` drill) and distributes it across social channels while running targeted backlink outreach to earn links from industry blogs, resource pages, and newsletters.

## Input

- Completed infographic: platform-specific image exports and companion post copy
- Blog post URL where the infographic is hosted (for backlink outreach)
- ICP definition: who should see this content
- Outreach target list: bloggers, newsletter authors, resource page owners in your niche

## Steps

### 1. Publish the infographic on your blog

Host the infographic on your own domain as the canonical source. Create a blog post that:
- Embeds the full-resolution infographic
- Provides context and analysis around the data (500-1000 words)
- Includes an embed code snippet so others can embed it with attribution
- Has proper OG meta tags (use `og-meta-generation` fundamental) so the infographic displays as the share preview

The embed code snippet to include on the page:
```html
<p><a href="{YOUR_POST_URL}"><img src="{INFOGRAPHIC_IMAGE_URL}" alt="{INFOGRAPHIC_TITLE}" width="800" /></a><br />
Source: <a href="{YOUR_POST_URL}">{YOUR_SITE_NAME}</a></p>
```

### 2. Distribute on social platforms

**LinkedIn (primary for B2B):**
Using the `linkedin-organic-posting` fundamental, publish the LinkedIn-sized image with the companion copy. Post timing: Tuesday-Thursday, 8-10am in ICP timezone. Using the `linkedin-organic-engagement` fundamental, engage with 5-10 ICP-relevant accounts 30 minutes before posting to warm the algorithm.

**Twitter/X:**
Post the Twitter-sized image with a shorter version of the companion copy (max 280 characters + image). Quote-tweet it from the company account if separate from founder account. Pin if it is your best-performing infographic this month.

**Reddit (if relevant subreddits exist):**
Post to 1-2 relevant subreddits with a text post that provides value first, with the infographic as supporting evidence. Do not post just the image with no context. Follow subreddit rules on self-promotion.

**Pinterest (for long-tail discovery):**
Upload the Pinterest-sized tall image with keyword-rich description. Pin to a board titled with your content pillar topic. Pinterest drives traffic for months after posting.

### 3. Build the backlink outreach list

Using the `clay-people-search` fundamental, find potential link partners:

**Target profiles:**
- Bloggers who have written about the same topic (search for articles mentioning your infographic's topic)
- Newsletter authors covering your industry
- Resource page curators ("best [topic] resources" pages)
- Journalists who cover your data's subject area

Using the `ahrefs-backlink-analysis` fundamental, find sites that have linked to competitors' infographics or visual content. These sites are pre-qualified as willing to link to infographic content.

Build a list of 20-50 outreach targets with: name, email, site URL, relevance reason (why they would care about this data).

### 4. Send backlink outreach emails

Using the `instantly-campaign` fundamental, create a personalized outreach sequence:

**Email 1 (Day 0):**
```
Subject: Data on {TOPIC} your readers might find useful

Hi {FIRST_NAME},

I noticed your piece on {THEIR_ARTICLE_TOPIC} — particularly the section about {SPECIFIC_DETAIL}.

We just published an infographic with new data on {YOUR_TOPIC}: {ONE_KEY_STATISTIC}.

Here is the full piece: {BLOG_POST_URL}

If it is useful for your readers, feel free to embed it — there is a ready-made embed code on the page.

Either way, great work on {THEIR_SITE_NAME}.

{YOUR_NAME}
```

**Email 2 (Day 4, if no reply):**
```
Subject: Re: Data on {TOPIC}

Quick follow-up — wanted to make sure this did not get buried. The infographic has been getting traction on LinkedIn ({SHARE_COUNT} shares so far).

Happy to provide any additional data points or a custom version if it would be a better fit for your audience.

{YOUR_NAME}
```

Set guardrails: max 50 outreach emails per day, personalization required for every email (no bulk blasts), unsubscribe link included.

### 5. Track backlink acquisition

Using the `ahrefs-backlink-analysis` fundamental, run weekly checks for new backlinks to your infographic blog post URL:

```
GET https://api.ahrefs.com/v3/site-explorer/new-backlinks
target={BLOG_POST_URL}&mode=exact&date_from={LAST_CHECK_DATE}
```

Log each acquired backlink in Attio with: referring domain, domain rating, anchor text, dofollow status, and attribution (outreach email vs organic discovery).

### 6. Amplify high-performing content

If an infographic gets 2x average engagement on social:
- Boost it with LinkedIn Thought Leader Ads ($) if budget allows
- Repurpose into a LinkedIn carousel (split the infographic into 5-7 slides)
- Create a 60-second video walkthrough of the data using the infographic as visual
- Send it to your email list via Loops broadcast

## Output

- Infographic published on blog with embed code and OG tags
- Social posts live on LinkedIn, Twitter/X, and optionally Reddit/Pinterest
- 20-50 personalized backlink outreach emails sent
- Weekly backlink tracking report
- Amplification plan for high performers

## Triggers

Run distribution within 24 hours of infographic creation. Backlink outreach runs the same week. Backlink tracking runs weekly for 8 weeks after each infographic launch.
