---
name: docs-lead-capture-setup
description: Configure lead capture mechanisms across documentation pages — signup CTAs, gated content, email capture, and visitor identification
category: Docs
tools:
  - PostHog
  - Loops
  - Intercom
  - Attio
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - posthog-cohorts
  - loops-sequences
  - loops-audience
  - intercom-in-app-messages
  - attio-contacts
  - attio-lead-scoring
  - n8n-workflow-basics
  - n8n-triggers
---

# Docs Lead Capture Setup

This drill configures the conversion layer that turns documentation readers into identifiable leads. Documentation traffic without lead capture is a vanity metric. This drill makes it a pipeline source.

## Input

- Published docs site with PostHog tracking installed
- Product signup flow URL
- API key generation URL (if applicable)
- Attio CRM configured
- At least 4 weeks of docs traffic data (to know which pages get traffic)

## Steps

### 1. Classify pages by conversion intent

Pull the top 50 docs pages by organic traffic from PostHog. Classify each into a conversion tier:

**Tier 1 — High intent (convert now):**
- Getting started guides → CTA: "Start building — get your API key"
- Integration guides → CTA: "Connect {product} to {integration} now"
- Pricing/limits pages → CTA: "Start your free trial"

**Tier 2 — Medium intent (capture email):**
- How-to tutorials → CTA: "Get the complete {topic} guide (email gate)"
- Best practices → CTA: "Subscribe to our developer newsletter for tips like this"

**Tier 3 — Low intent (identify for later):**
- API reference pages → CTA: subtle "Star us on GitHub" or sidebar newsletter signup
- Troubleshooting pages → CTA: "Need help? Talk to our team"

### 2. Implement conversion CTAs per tier

For each page, add the appropriate CTA using your docs platform's component system or injected HTML:

**Tier 1 — Direct signup CTA:**
```html
<div class="docs-cta docs-cta-primary">
  <h3>Ready to build?</h3>
  <p>Get your API key and start integrating in minutes.</p>
  <a href="/signup?utm_source=docs&utm_medium=cta&utm_content={page_slug}">
    Get Started Free
  </a>
</div>
```

Place after the first major section (above the fold) and at the end of the page.

**Tier 2 — Email capture CTA:**
```html
<div class="docs-cta docs-cta-secondary">
  <h3>Get the full {topic} playbook</h3>
  <p>We compiled everything we know about {topic} into a downloadable guide.</p>
  <form action="/api/docs-lead-capture" method="POST">
    <input type="email" name="email" placeholder="your@email.com" required>
    <input type="hidden" name="source" value="docs">
    <input type="hidden" name="page" value="{page_slug}">
    <button type="submit">Send me the guide</button>
  </form>
</div>
```

**Tier 3 — Passive capture:**
- Sidebar newsletter signup form (always visible)
- "Was this helpful? Yes/No" feedback widget (captures engagement signal)

### 3. Track all conversion events

Using `posthog-custom-events`, configure events:

- `docs_signup_cta_clicked`: properties `page_url`, `page_type`, `cta_tier`, `cta_text`
- `docs_email_captured`: properties `page_url`, `page_type`, `email_hash` (do not store raw email in PostHog)
- `docs_feedback_submitted`: properties `page_url`, `feedback_value` (helpful/not_helpful)

Build a PostHog funnel using `posthog-funnels`:
```
docs_page_viewed → docs_signup_cta_clicked → account_created
docs_page_viewed → docs_email_captured → email_opened (from Loops)
```

### 4. Route captured leads to CRM

Using `n8n-workflow-basics` and `n8n-triggers`, create a workflow:

1. **Trigger:** Webhook fires when email is captured or signup occurs from docs
2. **Enrich:** Look up the email in Attio. If new, create a contact using `attio-contacts`
3. **Tag:** Set source = "docs", set `docs_entry_page` = the page URL, set `docs_entry_keyword` = the target keyword of that page
4. **Score:** Run `attio-lead-scoring` — docs leads from high-intent pages (Tier 1) get a higher initial score
5. **Sequence:** Add to a Loops nurture sequence using `loops-sequences` — send a 3-email sequence:
   - Email 1 (immediate): "Here's the resource you requested" + link to related docs
   - Email 2 (day 3): "Others who read {topic} also found {related_topic} useful"
   - Email 3 (day 7): "Ready to try {product}? Here's a quickstart" + signup link

### 5. Build the docs lead dashboard

Using `posthog-funnels` and `posthog-cohorts`:

- **Docs → Signup funnel:** docs_page_viewed → docs_signup_cta_clicked → account_created (segmented by page type and traffic source)
- **Docs → Email funnel:** docs_page_viewed → docs_email_captured → email_opened → account_created
- **Docs visitor cohort:** visitors who viewed >= 3 docs pages in 7 days (high-intent segment)
- **Dashboard panels:** total docs leads this week, conversion rate by page type, top converting pages, lead source breakdown (organic vs direct vs referral)

### 6. Set up lead quality scoring

Using `attio-lead-scoring`, define scoring rules for docs-sourced leads:

- Viewed getting started guide: +20 points
- Viewed integration guide: +15 points
- Viewed API reference: +10 points
- Captured via Tier 1 CTA: +25 points
- Captured via Tier 2 CTA: +15 points
- Viewed 5+ docs pages: +20 points
- Returned to docs within 7 days: +15 points

Leads scoring > 60 are flagged as MQLs in Attio for sales follow-up.

## Output

- CTAs deployed across all docs pages, matched to page intent
- Lead capture forms on medium-intent pages
- n8n workflow routing leads to Attio with enrichment and scoring
- Loops nurture sequence for docs-captured emails
- PostHog dashboard showing docs funnel performance
- Lead scoring rules specific to docs engagement

## Triggers

- Set up once at Baseline level
- Review CTA performance monthly: swap underperforming CTAs, test new placements
- Re-score leads quarterly based on actual conversion data
