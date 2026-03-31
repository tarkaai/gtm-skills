---
name: linkedin-ads-measurement
description: Track and measure LinkedIn ad campaign performance and ROI
tool: LinkedIn Ads
difficulty: Intermediate
---

# Measure LinkedIn Ad Performance

## Prerequisites
- Active LinkedIn campaigns with at least 1 week of data
- Conversion tracking set up (LinkedIn Insight Tag or offline conversions)

## Steps

1. **Install the LinkedIn Insight Tag.** Add LinkedIn's JavaScript pixel to every page of your website. This enables conversion tracking, website retargeting, and audience demographics. Place the base tag in your site header. Add event-specific conversions for key actions (form submission, signup, demo request).

2. **Define your conversion events.** In Campaign Manager, go to Analyze > Conversion Tracking. Create conversions for each funnel stage: "Landing Page Visit" (page view), "Lead Form Submitted" (form event), "Demo Requested" (specific URL or event), "Signed Up" (signup confirmation page). Set the attribution window to 30 days click-through, 7 days view-through.

3. **Build your measurement framework.** Track three metric tiers. Tier 1 (weekly): Spend, Impressions, Clicks, CTR, CPC. Tier 2 (weekly): Leads, CPL, Conversion Rate. Tier 3 (monthly): Pipeline generated, Revenue influenced, ROAS. Tier 1 tells you if ads are working. Tier 3 tells you if they are profitable.

4. **Use Demographics reporting.** Campaign Manager shows which job titles, companies, industries, and seniorities are clicking your ads. Review this weekly. If non-ICP segments are consuming budget (e.g., students or job seekers clicking), add them as exclusions immediately.

5. **Connect to your CRM.** Export lead data from LinkedIn (from Lead Gen Forms or Insight Tag conversions) and import to your CRM (see `fundamentals/crm/attio-contacts`). Tag the source as "LinkedIn Ads" with the campaign name. This lets you track leads through the full pipeline to revenue.

6. **Calculate true ROI monthly.** Pull pipeline and revenue data from your CRM filtered to LinkedIn Ads source. Calculate: Total LinkedIn Ads spend / Pipeline generated = Cost per pipeline dollar. Target <$0.20 per pipeline dollar for B2B SaaS. If ROI is negative after 60 days, restructure targeting or offer before investing more.
