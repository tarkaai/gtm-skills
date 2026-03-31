---
name: template-tool-marketplaces-scalable
description: >
  Template or Tool Marketplace — Scalable Automation. Scale from 1-2 templates to a portfolio of
  5-10+ templates across multiple marketplaces. Automate cross-promotion, lead nurture, and A/B
  testing of listings. Find the 10x multiplier through volume and compounding discovery.
stage: "Marketing > SolutionAware"
motion: "DirectoriesMarketplaces"
channels: "Other"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">= 500 downloads and >= 15 leads over 2 months"
kpis: ["Total downloads across portfolio", "Number of active templates", "Cross-promotion click-through rate", "Portfolio-wide download-to-lead conversion rate", "Leads captured per template"]
slug: "template-tool-marketplaces"
install: "npx gtm-skills add marketing/solution-aware/template-tool-marketplaces"
drills:
  - ab-test-orchestrator
  - tool-sync-workflow
---

# Template or Tool Marketplace — Scalable Automation

> **Stage:** Marketing > SolutionAware | **Motion:** DirectoriesMarketplaces | **Channels:** Other

## Outcomes

Find the 10x multiplier. The Scalable level transforms a single proven template into a portfolio of 5-10+ templates across multiple marketplaces, with automated cross-promotion creating a compounding discovery network. Each new template is a new surface for your ICP to find you. Cross-promotion between templates multiplies the reach of every addition.

**Pass threshold:** >= 500 downloads and >= 15 leads over 2 months.

## Leading Indicators

- 5+ templates published and live across 2+ marketplaces within the first month
- Cross-promotion links installed in all templates (each template links to 2-3 others)
- Cross-promotion click-through rate > 3% (proves the network effect is working)
- Weekly template creation cadence established (1 new template per week)
- Email nurture sequence active for Gumroad downloaders (4-email sequence)
- A/B tests running on listing titles and descriptions (at least 1 active test)
- Downloads trending up month-over-month as portfolio grows

## Instructions

### 1. Scale the template portfolio

Run the the marketplace portfolio scaling workflow (see instructions below) drill. This is the core Scalable-level work:

1. **Identify 5-10 template topics** using Clay to research high-demand, low-competition opportunities across marketplaces. Prioritize templates that:
   - Cover different stages of the same workflow (planning -> execution -> review)
   - Target different roles in the buying org (IC, manager, executive)
   - Serve adjacent use cases that all connect to your product

2. **Build a creation pipeline** with a weekly cadence: 1 new template every 1-2 weeks, each published to 2-3 marketplaces.

3. **Implement cross-promotion** between all templates: each template includes a "More Templates" section linking to 2-3 related templates with UTM-tracked links (`utm_medium=cross-promo`).

4. **Automate lead nurture** using Loops: a 4-email sequence for template downloaders that educates, cross-promotes the portfolio, and soft-pitches the product.

5. **Track portfolio performance** in PostHog with per-template cohorts and a portfolio-level dashboard.

**Human action required:** Creating each template requires human craft. The agent handles: topic research, competitive analysis, listing metadata optimization, cross-promotion link setup, email sequence configuration, and analytics tracking. A human (or human-supervised agent) builds the actual template content.

### 2. A/B test listing variations

Run the `ab-test-orchestrator` drill to systematically test listing elements:

**Test priority (highest impact first):**

1. **Listing title:** Test keyword variations. Example: "OKR Tracker for Startups" vs "Quarterly Goal Setting Template for Teams." Run for 4 weeks, measure downloads.

2. **Cover image:** Test different visual styles. Example: screenshot with sample data vs. clean graphic with text overlay. Since most marketplaces do not support native A/B testing, run sequential tests: use version A for 2 weeks, version B for 2 weeks, compare downloads (normalize for weekday/weekend patterns).

3. **Description opening line:** Test outcome-focused vs. feature-focused. Example: "Track your team's quarterly goals in one place" vs "Includes 5 views, automated rollups, and weekly check-in templates."

4. **In-template CTA:** Test different CTA positions and copy. Example: CTA at top of template vs. at the workflow's natural "what's next" moment.

**Experiment logging:** For each test, log in Attio: hypothesis, variants, start date, end date, metric (downloads or CTA clicks), result, decision (adopt/revert).

### 3. Automate marketplace-to-CRM sync

Run the `tool-sync-workflow` drill to build n8n workflows that keep your marketplaces and CRM in sync:

**Workflow 1: Gumroad download -> Attio lead**
- Trigger: Gumroad webhook fires on new download
- Action: Create Person record in Attio (email, company if captured, source = "gumroad", template_slug)
- Action: Create Deal at "Template Downloader" stage
- Action: Add to Loops audience with tags: `source_marketplace=gumroad`, `source_template={slug}`

**Workflow 2: PostHog marketplace lead -> Attio update**
- Trigger: PostHog webhook on `marketplace_lead_captured` event
- Action: Find or create Person in Attio
- Action: Update Deal stage to "Lead Captured"
- Action: Add note: "Converted from template {template_slug} via {marketplace}"

**Workflow 3: Weekly performance sync**
- Trigger: n8n cron (Monday 8am)
- Action: Aggregate PostHog marketplace metrics
- Action: Update all template campaign records in Attio with latest download/lead counts
- Action: Post portfolio summary to Slack

### 4. Evaluate against threshold

After 2 months, measure against: >= 500 downloads and >= 15 leads.

**Per-template analysis:**
- Which templates drive the most downloads?
- Which templates have the highest download-to-lead conversion rate?
- Which marketplaces perform best for which template types?
- Is cross-promotion driving meaningful traffic between templates?

**Portfolio-level analysis:**
- Is the total download trajectory accelerating (compounding) or linear?
- What is the marginal cost of each new template vs. the marginal leads generated?
- Are there templates that should be retired (low downloads, zero leads)?

**PASS:** Proceed to Durable. Document the portfolio strategy and which templates/marketplaces form the core.
**FAIL:** Analyze per-template data. If 1-2 templates drive all the results, focus there and cut underperformers. If no templates convert, revisit the template-to-product bridge: is the CTA compelling? Does the landing page answer "why upgrade from the template?"

## Time Estimate

- 20 hours: Template portfolio creation (10 templates x 2 hours each, agent-assisted)
- 15 hours: Marketplace listing optimization and A/B testing
- 10 hours: Cross-promotion setup, email nurture sequence, CRM sync workflows
- 10 hours: Monitoring, analysis, and ongoing optimization
- 5 hours: Portfolio management and underperformer triage

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Notion Marketplace | Template distribution | Free listings ([notion.com/marketplace](https://www.notion.com/help/selling-on-marketplace)) |
| Gumroad | Template distribution + email capture | 10% + $0.50 per sale; free for $0 products ([gumroad.com/pricing](https://gumroad.com/pricing)) |
| Figma Community | Template distribution | Free ([figma.com/community](https://www.figma.com/community)) |
| Airtable Universe | Template distribution | Free ([airtable.com/universe](https://www.airtable.com/universe)) |
| PostHog | Funnel tracking, experiments, cohorts | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Workflow automation (sync, reporting) | Cloud Pro EUR 60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Clay | Template topic research, competitive analysis | Explorer $149/mo ([clay.com/pricing](https://clay.com/pricing)) |
| Attio | CRM for lead and template tracking | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Loops | Email nurture for template downloaders | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated monthly cost at this level:** $300-500 (n8n + Clay + Attio + Loops; marketplace listings and PostHog remain free at typical volumes)

## Drills Referenced

- the marketplace portfolio scaling workflow (see instructions below) -- systematic expansion from 1 template to a portfolio with cross-promotion, email nurture, and portfolio analytics
- `ab-test-orchestrator` -- designs and runs A/B tests on listing titles, descriptions, cover images, and CTAs
- `tool-sync-workflow` -- builds n8n workflows to sync marketplace downloads to Attio CRM and Loops nurture sequences
