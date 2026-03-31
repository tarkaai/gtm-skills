---
name: brand-refresh-redesign-smoke
description: >
  Brand Refresh & Redesign — Smoke Test. Run a structured brand audit on your
  current website, analyze messaging consistency and conversion paths, benchmark
  against 3 competitors, and produce 3 positioning concepts for testing.
stage: "Marketing > Unaware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "Complete brand audit report with 3 positioning concepts and prioritized action list"
kpis: ["Pages audited", "Messaging consistency score (1-5)", "Conversion path gaps identified", "Competitive positioning gaps found", "Positioning concepts produced"]
slug: "brand-refresh-redesign"
install: "npx gtm-skills add marketing/unaware/brand-refresh-redesign"
drills:
  - brand-audit-analysis
  - threshold-engine
---

# Brand Refresh & Redesign — Smoke Test

> **Stage:** Marketing > Unaware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Outcomes

Produce a structured brand audit that identifies what is broken in your current website's messaging, conversion paths, and competitive positioning. Generate 3 concrete positioning concepts that can be A/B tested in the Baseline level. This is research and analysis — no changes are made to the live site.

## Leading Indicators

- Website crawl completes successfully and extracts data from all marketing pages
- PostHog data shows at least 4 weeks of baseline web analytics (enough to measure against)
- Competitor crawl reveals at least 2 positioning gaps (opportunities for differentiation)
- Claude analysis identifies at least 3 specific, rewritable messaging issues

## Instructions

### 1. Define the audit scope

Before running the audit, document:
- **ICP**: Who should this brand resonate with? Describe the persona: role, pain points, goals, current awareness level (Unaware stage means they don't yet know your solution category exists).
- **Audit perimeter**: List all marketing pages to audit. Typically: homepage, pricing, features/product, about, 3-5 top landing pages, 3-5 top blog posts.
- **Competitor set**: Choose 3-5 direct competitors whose websites will be benchmarked.
- **Success criteria for the brand refresh**: What does "better" look like? Examples: "Higher homepage-to-pricing click rate," "Lower bounce rate on features page," "Clearer differentiation from Competitor X."

### 2. Run the brand audit

Run the `brand-audit-analysis` drill with your scope inputs. The drill executes:

**Website crawl:** Programmatically crawls all marketing pages and extracts every headline (H1, H2), CTA (text + destination), meta description, above-fold screenshot, and color/font usage. Also crawls 3-5 competitor sites.

**Messaging analysis:** Passes all extracted copy to Claude for analysis. Evaluates:
- Messaging consistency across pages (does every page reinforce the same value prop?)
- Clarity for a first-time visitor (can they understand the product in 5 seconds?)
- Differentiation (do your headlines also describe competitors?)
- CTA hierarchy (is there one clear primary action?)
- ICP alignment (does the messaging address Unaware-stage pain points?)

**Conversion path analysis:** Pulls PostHog data to identify:
- Bounce rate by entry page (which pages lose visitors?)
- Session duration by source (is traffic quality consistent?)
- Top exit pages (where do visitors leave?)
- Conversion funnel: any page > CTA click > form submit > lead captured

**Competitive positioning:** Compares your messaging against competitors. Identifies:
- Commodity claims (everyone says the same thing)
- Unique claims (only you say this)
- Competitor claims you're missing
- Open positioning territory no one owns

**Human action required:** Watch 10-20 PostHog session recordings of homepage visitors who bounced. Note what they looked at, where they scrolled, and where they left. Add these qualitative observations to the audit report.

### 3. Generate positioning concepts

Using the audit findings, produce 3 positioning concepts:

**Concept A (Evolutionary):** Refine the existing positioning. Keep the core value prop but sharpen the language, fix consistency issues, and improve clarity. Low risk, moderate impact.

**Concept B (Differentiation):** Reposition around an unoccupied territory identified in the competitive analysis. New headline, new messaging hierarchy, new proof points. Medium risk, high impact.

**Concept C (Audience-shift):** Rewrite all messaging for a specific ICP segment that the current site underserves. Different pain points, different language, different outcomes. Higher risk, potentially highest impact.

For each concept, produce:
- A new homepage H1 headline
- A supporting H2 subheadline
- The primary CTA text
- The key proof point (stat, testimonial, or case study reference)
- Rationale: why this concept based on the audit data

### 4. Evaluate against threshold

Run the `threshold-engine` drill:
- **Brand audit report complete?** Must contain: messaging audit, conversion path analysis, competitive positioning map, and prioritized action list.
- **3 positioning concepts produced?** Each with headline, subheadline, CTA, proof point, and rationale.

Decision tree:
- **PASS**: Audit is thorough and concepts are concrete enough to A/B test. Proceed to Baseline.
- **FAIL**: Audit missed key pages or competitors, or concepts are too vague to implement. Re-run with expanded scope.

## Time Estimate

- 1 hour: Define audit scope, ICP, competitor set
- 2 hours: Run brand audit analysis (crawl + analytics pull + Claude analysis)
- 1 hour: Watch session recordings and add qualitative notes
- 1.5 hours: Generate and refine 3 positioning concepts
- 30 minutes: Final evaluation and documentation

**Total: ~6 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Playwright | Website crawling and screenshot capture | Free (open source) |
| PostHog | Web analytics, session recordings, funnel analysis | Free tier (1M events/mo, 5K recordings/mo) |
| Anthropic API | Messaging analysis and positioning concept generation | ~$5-10 for audit volume |
| Clay | Competitor company enrichment | Free tier or ~$50/mo |

## Drills Referenced

- `brand-audit-analysis` — Runs the full audit: website crawl, messaging analysis, conversion path analysis, competitive positioning, and produces the structured audit report
- `threshold-engine` — Evaluates completeness of the audit report and positioning concepts against pass criteria
