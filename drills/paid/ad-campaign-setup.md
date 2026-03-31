---
name: ad-campaign-setup
description: Set up paid ad campaigns on Google, LinkedIn, or Meta with proper tracking and budget allocation
category: Paid
tools:
  - Google Ads
  - LinkedIn Ads
  - Meta Ads
  - PostHog
fundamentals:
  - google-ads-campaign-setup
  - linkedin-ads-campaign-setup
  - meta-ads-campaign-setup
  - posthog-custom-events
---

# Ad Campaign Setup

This drill walks through setting up a paid advertising campaign from platform selection through launch and initial optimization. It covers Google, LinkedIn, and Meta with a focus on B2B SaaS targeting.

## Prerequisites

- Ad platform accounts created and billing configured
- Landing pages built (run `landing-page-pipeline` drill if needed)
- PostHog tracking installed on landing pages
- Budget allocated (minimum $1,000/month per platform for meaningful data)

## Steps

### 1. Choose the right platform

Match the platform to your goal and audience:

- **Google Ads**: Best for capturing existing demand. Use when people actively search for your solution category. Start with Search campaigns targeting bottom-of-funnel keywords.
- **LinkedIn Ads**: Best for targeting specific professional audiences. Use when your ICP is defined by job title, company size, or industry. Higher CPM but precise targeting.
- **Meta Ads**: Best for retargeting and lookalike audiences. Use when you have website traffic or a customer list to build audiences from. Lower CPM, good for awareness.

Start with one platform. Add others only after the first is profitable.

### 2. Define campaign structure

Using the platform-specific fundamental (`google-ads-campaign-setup`, `linkedin-ads-campaign-setup`, or `meta-ads-campaign-setup`), organize your campaign:

- **Campaign level**: One campaign per objective (lead generation, demo signups, content promotion)
- **Ad group/set level**: One per audience segment or keyword theme
- **Ad level**: 3-5 ad variations per group for testing

Keep the structure simple. Over-segmentation spreads budget too thin and slows learning.

### 3. Configure targeting

For Google: research keywords using your SEO data from `blog-seo-pipeline`. Start with exact match and phrase match on high-intent terms. Add negative keywords aggressively to prevent wasted spend.

For LinkedIn: target by job title + company size + industry. Layer additional filters (seniority, skills, groups) only if your audience is too broad. Audience size between 20,000-80,000 is ideal.

For Meta: start with retargeting your website visitors (install the pixel first). Build a lookalike audience from your best customers. Exclude existing customers.

### 4. Write ad creative

Lead with the outcome, not the product. Structure:

- **Headline**: Specific benefit or result. Numbers perform well. "Cut onboarding time by 60%."
- **Description**: How you deliver the result. One sentence.
- **CTA**: Match the funnel stage. "Learn More" for awareness, "Get Demo" for consideration, "Start Free Trial" for decision.

Create 3-5 variations with different hooks, benefits, and CTAs. Let the platform optimize toward the best performer.

### 5. Set up conversion tracking

Using `posthog-custom-events`, configure conversion events: page view, form submission, demo booked, trial started. Set up UTM parameters on every ad URL so you can track which campaign, ad group, and ad drove each conversion. Connect PostHog to your ad platform for conversion optimization.

### 6. Launch and optimize weekly

Start with a daily budget that allows at least 50 clicks per week per ad group (enough data to optimize). Review performance weekly: pause ads with CTR below 1% (Google) or 0.3% (LinkedIn/Meta). Shift budget from underperforming ad groups to winners. Optimize for cost per conversion, not just clicks. After 2 weeks of data, make your first major adjustments.
