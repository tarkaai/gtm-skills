---
name: template-tool-marketplaces-smoke
description: >
  Template or Tool Marketplace — Smoke Test. Create and publish one free template to 2-3
  template marketplaces (Notion, Figma, Gumroad, Airtable) with embedded CTAs. Measure whether
  template distribution generates any downloads and at least one lead.
stage: "Marketing > SolutionAware"
motion: "DirectoriesMarketplaces"
channels: "Other"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: ">= 50 downloads and >= 1 lead in 2 weeks"
kpis: ["Total downloads across marketplaces", "Site visits from template CTAs", "Leads captured from template-sourced sessions"]
slug: "template-tool-marketplaces"
install: "npx gtm-skills add marketing/solution-aware/template-tool-marketplaces"
drills:
  - icp-definition
  - marketplace-template-creation
  - threshold-engine
---

# Template or Tool Marketplace — Smoke Test

> **Stage:** Marketing > SolutionAware | **Motion:** DirectoriesMarketplaces | **Channels:** Other

## Outcomes

Run once, locally, with agent assistance. The goal is to prove that publishing a free template on marketplaces generates any downloads and drives at least one person to your product. No budget required. No always-on automation. Just one template, a few marketplaces, and proof of signal.

**Pass threshold:** >= 50 downloads and >= 1 lead in 2 weeks.

## Leading Indicators

- Template approved and live on 2-3 marketplaces within 3-5 business days of submission
- Downloads appearing within the first 48 hours of going live
- UTM-tagged traffic from marketplaces appearing in PostHog within 1 week
- At least one CTA click from a template user (proves users are engaging with the CTA, not just downloading)
- Template appearing in marketplace search results for target keyword

## Instructions

### 1. Identify template topic and target marketplaces

Run the `icp-definition` drill to understand what workflows your ICP cares about and what tools they use day-to-day. Specifically: which template platforms does your ICP use? If they are product managers, Notion is likely primary. If they are designers, Figma. If they work with structured data, Airtable.

Select 1 template topic that:
- Solves a real workflow problem your ICP faces
- Naturally connects to the problem your product solves
- Can be built as a standalone, useful template without requiring your product

Select 2-3 marketplaces. Recommended starting set:
- **Notion Marketplace** -- largest B2B template marketplace; strong for ops, PM, startup workflows
- **Gumroad** -- universal; accepts any file type; automatically captures downloader email
- **Figma Community** -- strong for design, UI, and visual workflow templates
- **Airtable Universe** -- good for data-heavy, structured workflow templates

### 2. Create and publish the template

Run the `marketplace-template-creation` drill. This drill covers:

1. Researching high-demand, low-competition template topics using Clay
2. Building the template with sample data, embedded CTAs, and UTM-tracked links
3. Publishing to the primary marketplace using the appropriate fundamental (`notion-template-publish`, `gumroad-product-publish`, `figma-community-publish`, or `airtable-universe-publish`)
4. Cross-publishing to 1-2 secondary marketplaces
5. Logging all listings in Attio CRM
6. Promoting the template on social channels and communities

**CTA link format for all CTAs inside the template:**
```
{your-product-url}?utm_source={marketplace}&utm_medium=marketplace&utm_campaign=template-{slug}
```

**Human action required:** Create the actual template content. The agent can research topics, draft descriptions, prepare metadata, and configure tracking, but the template itself requires human craft to be useful and authentic.

### 3. Monitor and measure

Check marketplace dashboards daily for the 2-week measurement period:
- Log downloads from each marketplace's creator analytics
- Check PostHog for `utm_source` traffic matching marketplace names
- Track any form submissions, trial starts, or demo requests from marketplace-sourced sessions

For Gumroad: check the sales dashboard for download count and captured emails.
For Notion/Figma/Airtable: check the creator dashboard for duplication/copy counts.

### 4. Evaluate against threshold

Run the `threshold-engine` drill to assess results after 2 weeks:

- **PASS (>= 50 downloads, >= 1 lead):** Template distribution drives real signal. Proceed to Baseline.
- **MARGINAL (>= 50 downloads, 0 leads):** Downloads prove discoverability but the CTA is not converting. Improve CTA placement and copy inside the template. Ensure the landing page matches what template users expect. Re-run for 1 more week.
- **FAIL (< 50 downloads):** Template topic may be wrong, marketplace selection may be off, or listing optimization is needed. Check: (a) does the template appear in marketplace search? (b) is the title keyword-optimized? (c) is the cover image compelling? Fix and re-submit.

## Time Estimate

- 0.5 hours: ICP research and template topic selection
- 1.5 hours: Template creation (agent-assisted research + human template building)
- 0.5 hours: Marketplace listing setup and submission
- 0.5 hours: Initial promotion and monitoring setup

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Notion Marketplace | Template distribution (B2B/ops/startup) | Free listing; 10% + $0.40 on paid sales ([notion.com/marketplace](https://www.notion.com/help/selling-on-marketplace)) |
| Gumroad | Template distribution (any file type) + email capture | Free; 10% + $0.50 per sale ([gumroad.com/pricing](https://gumroad.com/pricing)) |
| Figma Community | Template distribution (design/UI) | Free ([figma.com/community](https://www.figma.com/community)) |
| Airtable Universe | Template distribution (data/workflows) | Free ([airtable.com/universe](https://www.airtable.com/universe)) |
| PostHog | UTM traffic tracking | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | CRM for listing tracking | Free for small teams ([attio.com/pricing](https://attio.com/pricing)) |
| Clay | Template topic research | Explorer $149/mo ([clay.com/pricing](https://clay.com/pricing)) |

**Estimated monthly cost at this level:** $0 (free marketplace listings + free PostHog/Attio tiers). Clay is optional for research.

## Drills Referenced

- `icp-definition` -- identifies which template platforms your ICP uses and what workflow topics resonate
- `marketplace-template-creation` -- end-to-end template research, creation, publishing, and promotion across marketplaces
- `threshold-engine` -- evaluates pass/fail against the 50-download, 1-lead threshold
