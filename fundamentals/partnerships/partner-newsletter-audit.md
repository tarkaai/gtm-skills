---
name: partner-newsletter-audit
description: Research a partner's newsletter to assess audience size, frequency, engagement, and fit for co-marketing
tool: Clay
difficulty: Setup
---

# Partner Newsletter Audit

## Prerequisites
- Target partner identified (company name and domain)
- Clay account for enrichment (or manual research workflow)
- Web browser or web search API access

## Steps

1. **Find the newsletter.** Search for the partner's newsletter signup page. Check: their website footer, `/newsletter` or `/subscribe` path, their blog sidebar, their LinkedIn company page (often links to newsletter), and their Twitter/X bio. Record the signup URL.

2. **Assess audience size.** Look for public signals of subscriber count:
   - Check if they publish subscriber count on their signup page ("Join 10,000+ subscribers")
   - Search Substack leaderboards if they use Substack
   - Check SparkToro for estimated audience size: query their domain and look at the "Newsletter" or "Email" audience estimate
   - Use Clay's `claygent` to research: "How many subscribers does {company}'s newsletter have?" with sources

   ```
   Clay Claygent prompt:
   "Research {partner_domain}. Find their newsletter. Estimate subscriber count
   from public sources (landing page claims, press mentions, Substack rankings,
   social proof). Return: newsletter_name, estimated_subscribers, source_of_estimate,
   signup_url, publishing_platform (Substack/Beehiiv/Ghost/Loops/ConvertKit/other)."
   ```

3. **Analyze content and audience fit.** Read the last 3-5 issues of the newsletter. Assess:
   - **Topic alignment**: Do they cover topics your ICP cares about?
   - **Audience persona**: Is their reader your target buyer (title, industry, company size)?
   - **Tone and format**: Would your blurb feel native in their newsletter?
   - **Existing co-marketing**: Do they already feature partner content? If yes, what format (blurb, banner, dedicated section)?

4. **Check engagement signals.** Look for:
   - Social shares on newsletter issues (check Twitter/LinkedIn)
   - Comment threads on Substack/blog posts
   - Reply-to engagement (do they encourage replies?)
   - Frequency and consistency (weekly newsletters with no gaps signal healthy engagement)

5. **Score the partner newsletter.** Rate on a 1-5 scale across four dimensions:
   - **Audience overlap** (1-5): How well does their audience match your ICP?
   - **Audience size** (1-5): 1 = <500, 2 = 500-2K, 3 = 2K-10K, 4 = 10K-50K, 5 = 50K+
   - **Engagement quality** (1-5): Based on social shares, comments, and consistency
   - **Co-marketing friendliness** (1-5): Do they already feature partners? Is there a clear way to pitch?

   Total score out of 20. Prioritize partners scoring 14+.

6. **Record findings.** Store in your CRM (Attio) on the partner company record:
   - Newsletter name and URL
   - Estimated subscriber count
   - Publishing platform
   - Frequency
   - Audience overlap score
   - Overall partner newsletter score

## Alternative Tools
- **SparkToro**: Audience intelligence for newsletter research
- **Beehiiv Analytics** (if partner shares): Direct engagement metrics
- **SimilarWeb**: Traffic estimates to newsletter landing pages
- **Apollo**: Find the newsletter editor/partnerships contact at the partner company
- **Clearbit**: Enrich the partner company for firmographic context
