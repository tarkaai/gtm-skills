---
name: guest-posting-scale-smoke
description: >
  Guest Posting at Scale — Smoke Test. Manually discover 15 target blogs, pitch 10 editors, and
  publish 2+ guest articles to validate that guest posting drives referral traffic to your site.
stage: "Marketing > Solution Aware"
motion: "PR & Earned Mentions"
channels: "Content, Email"
level: "Smoke Test"
time: "8 hours over 2 weeks"
outcome: "≥2 accepted pitches and ≥50 referral visits from published guest posts"
kpis: ["Pitch acceptance rate", "Articles published", "Referral traffic from guest posts", "Backlinks acquired (dofollow)"]
slug: "guest-posting-scale"
install: "npx gtm-skills add marketing/solution-aware/guest-posting-scale"
drills:
  - guest-post-blog-discovery
  - guest-post-pitch-outreach
  - guest-post-article-pipeline
  - threshold-engine
---

# Guest Posting at Scale — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** PR & Earned Mentions | **Channels:** Content, Email

## Outcomes

Validate that guest posting can generate referral traffic and backlinks for your site. Prove that your expertise and content can earn placement on relevant industry blogs before investing in automation.

## Leading Indicators

- Editor reply rate ≥20% (your pitches resonate)
- At least 1 pitch accepted within the first week (topic-market fit)
- Published articles generate measurable referral sessions within 7 days of publication

## Instructions

### 1. Discover target blogs

Run the `guest-post-blog-discovery` drill at Smoke scale (target: 15 blogs). Focus on:
- Blogs with Domain Authority 30+ that your ICP reads
- Blogs with explicit "write for us" or "contribute" pages
- Blogs where competitors have published guest posts

At Smoke level, execute this manually: search Ahrefs Content Explorer for 5-10 niche keywords combined with guest post signals ("write for us", "guest post", "contribute"). Score and tier the results by hand. Store in Attio.

### 2. Pitch 10 target blogs

Run the `guest-post-pitch-outreach` drill at Smoke scale. For each of the top 10 blogs from your discovery list:

1. Read 2-3 recent articles on the blog to understand their editorial voice and audience
2. Generate 2 pitch angles per blog using the Anthropic API pitch generation prompt from `ai-guest-post-drafting`
3. Select the strongest angle and write a fully personalized pitch email referencing a specific recent article
4. Send from the founder's personal email account
5. Log every pitch in Attio with: blog name, editor, topic pitched, date sent, status

**Human action required:** Send all pitches manually from the founder's email. This is a Smoke test — no automation. Hand-personalize every pitch. Follow up once after 7 days if no response.

### 3. Write and submit accepted articles

For each accepted pitch, run the `guest-post-article-pipeline` drill:

1. Analyze the target blog's style (tone, structure, formatting, typical length)
2. Generate a draft via Anthropic API with 1-2 strategic backlinks to high-value pages on your site
3. Run the AI editorial review check for style match, backlink naturalness, and content quality
4. **Human action required:** Author reviews and edits the draft, adding personal insights and verifying accuracy
5. Submit the article to the editor and handle any revision requests
6. Set up PostHog referrer-based tracking for the publishing blog's domain once the article goes live

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure:
- ≥2 pitches accepted (out of 10 sent)
- ≥50 referral visits from published guest posts within 2 weeks of publication

Pull acceptance data from Attio pitch pipeline. Pull referral traffic from PostHog filtered by guest post source blogs.

If PASS: Document which pitch angles and blog types worked. Save your pitch templates, blog target list, and editorial style notes. Proceed to Baseline.

If FAIL: Diagnose — was it low reply rates (pitch quality issue), low acceptance after reply (topic mismatch), or low traffic from published posts (blog audience mismatch)? Adjust and re-run.

## Time Estimate

- Blog discovery and scoring: 2 hours
- Pitch writing and sending (10 pitches): 3 hours
- Article writing and submission (2 articles): 2.5 hours
- Tracking setup and evaluation: 0.5 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Ahrefs | Blog discovery, DA scoring, backlink tracking | Standard $199/mo (https://ahrefs.com/pricing) |
| PostHog | Referral traffic tracking | Free up to 1M events/mo (https://posthog.com/pricing) |
| Attio | Pitch pipeline tracking | Free for small teams (https://attio.com/pricing) |
| Anthropic API | Pitch angle + article draft generation | ~$0.05/article (https://anthropic.com/pricing) |

## Drills Referenced

- `guest-post-blog-discovery` — find and score 15 blogs that accept guest posts in your niche
- `guest-post-pitch-outreach` — craft and send 10 personalized guest post pitches
- `guest-post-article-pipeline` — write, review, and submit guest articles for accepted pitches
- `threshold-engine` — evaluate pitch acceptance rate and referral traffic against pass threshold
