---
name: documentation-as-marketing-scalable
description: >
  Documentation as Marketing — Scalable Automation. Automate the docs content
  pipeline: keyword discovery, page generation, publishing, and performance
  tracking run continuously with minimal human intervention, scaling docs
  traffic and leads 10x.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Scalable Automation"
time: "50 hours over 3 months"
outcome: ">=5,000 organic visits/month to docs, >=50 leads/month from docs, and content pipeline producing >=5 new pages/week with automated quality gates"
kpis: ["Monthly organic docs traffic", "Monthly docs-sourced leads", "Docs-to-signup conversion rate", "Pages published per week", "Content pipeline automation rate", "Keyword coverage vs competitors"]
slug: "documentation-as-marketing"
install: "npx gtm-skills add marketing/solution-aware/documentation-as-marketing"
drills:
  - docs-content-scaling-pipeline
  - content-refresh-pipeline
  - cluster-gap-analysis
  - threshold-engine
---

# Documentation as Marketing — Scalable Automation

> **Stage:** Marketing > Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Outcomes

The automated docs content pipeline discovers keyword opportunities, generates pages, quality-checks them, and publishes with minimal human oversight. Organic traffic reaches >= 5,000 visits/month. Docs consistently produce >= 50 leads/month. The pipeline publishes >= 5 new pages per week. Keyword coverage vs top competitors reaches >= 60%.

## Leading Indicators

- Keyword discovery workflow surfaces >= 15 new opportunities per week
- Quality gate pass rate for auto-generated pages >= 80% (reducing regeneration cycles)
- Content refresh pipeline catches and fixes ranking decay within 14 days
- New pages reach Google top-50 within 21 days of publication at a rate of >= 60%
- Docs lead quality score (from Attio) correlates with actual pipeline conversion at >= 15% MQL-to-SQL rate
- Competitor keyword gap shrinks by >= 5% per month

## Instructions

### 1. Deploy the automated content scaling pipeline

Run the `docs-content-scaling-pipeline` drill to build the automated content engine:

**Keyword discovery (runs weekly via n8n):**
- Source 1: GSC query mining — find queries with impressions > 10 but clicks < 3 (content-intent mismatch)
- Source 2: Competitor keyword monitoring — detect new keywords competitor docs rank for that you do not
- Source 3: Docs search analytics — surface zero-result internal search queries (users asking for content you lack)

**Priority scoring:** Each discovered keyword is scored by `(search_volume * intent_score * gap_urgency) / keyword_difficulty`. Top opportunities enter the production queue automatically.

**Page generation (triggered when queue >= 5 items):**
- Auto-classify page type from keyword pattern
- Pull top 3 competitor pages for structure analysis
- Generate page content via Anthropic API with keyword targeting, real code examples, and proper docs template
- Run automated quality gate: keyword inclusion, length, code syntax, internal links, CTA, duplicate check

**Rate limit:** Maximum 10 pages generated per week. Quality over volume.

**Human action required:** Initially, review and approve all generated pages before publishing. As quality gate accuracy improves (track false positive rate), shift to spot-checking every 5th page. Full human review remains required for:
- Pages covering new product capabilities not yet documented
- Pages in competitive keyword spaces (top 3 results are strong)
- Integration guides for partners (accuracy is critical for relationship)

### 2. Activate the content refresh pipeline

Run the `content-refresh-pipeline` drill to automatically detect and fix declining pages:

**Weekly scan identifies pages needing refresh:**
- Priority 1: Pages where ranking position dropped > 5 spots in 30 days (had traction, losing it)
- Priority 2: Pages stuck at positions 11-30 for > 60 days (close to page 1 but not breaking through)
- Priority 3: Pages not indexed after 30 days (structural or content issue)
- Priority 4: Pages ranking on page 1 but engagement rate < 20% (content-intent mismatch)

**For each flagged page:**
- Diagnose the issue (competitor content improved, outdated content, thin content, wrong intent)
- Generate refreshed content addressing the specific diagnosis
- Rewrite meta title and description for better CTR
- Publish the refresh and track recovery over 28 days

**Automation:** The weekly scan, diagnosis, and refresh generation run automatically via n8n. Publishing refreshed content requires human approval (initially).

### 3. Run keyword gap analysis

Run the `cluster-gap-analysis` drill at month 2 to audit the full docs content portfolio:

- Map all docs pages against keyword coverage: which topic areas are well-covered vs thin
- Identify keyword cannibalization: multiple docs pages competing for the same query
- Audit internal linking completeness: are any pages orphaned (no internal links pointing to them)?
- Benchmark keyword coverage vs top 3 competitor docs sites

Act on findings:
- For thin topic areas: queue 5-10 new pages targeting those keywords
- For cannibalization: merge thin competing pages or differentiate their target keywords
- For orphaned pages: add internal links from related pages
- For competitor gaps: prioritize high-traffic keywords where competitors rank and you do not

### 4. Scale lead capture based on performance data

Using 8+ weeks of lead capture data from Baseline, optimize:

- **CTA A/B testing:** For high-traffic pages, test 2 CTA variants using PostHog feature flags. Test variables: CTA copy, CTA placement (after first section vs sidebar vs end of page), CTA type (signup vs email capture vs chat). Run each test for >= 200 CTA impressions per variant.
- **Lead scoring refinement:** Compare docs-sourced leads that converted to customers vs those that did not. Adjust scoring weights: which page types and engagement patterns actually predict conversion?
- **Nurture sequence optimization:** Analyze Loops sequence performance (open rates, click rates, conversion to signup). Test subject lines and content variations on the 3-email sequence.

### 5. Evaluate against threshold

Run the `threshold-engine` drill at month 3. Measure:
- Monthly organic visits to docs: target >= 5,000
- Monthly leads from docs: target >= 50
- Pages published per week (automated pipeline): target >= 5
- Content pipeline automation rate (pages published without manual intervention): target >= 60%

If PASS, proceed to Durable. If FAIL, diagnose the bottleneck: if traffic is low, the keyword discovery is not finding good targets — review priority scoring formula. If traffic is high but leads are low, conversion optimization needs more investment — run more CTA tests. If the pipeline is slow, reduce the quality gate strictness or invest in better generation prompts.

## Time Estimate

- Content scaling pipeline setup: 8 hours (n8n workflows + quality gate configuration)
- Content refresh pipeline setup: 4 hours (scan + diagnosis + refresh generation)
- Gap analysis and remediation: 6 hours (audit + fixes)
- Lead capture optimization: 5 hours (A/B tests + scoring refinement)
- Ongoing monitoring and pipeline management: 20 hours (spread over 3 months)
- Evaluation: 2 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Ahrefs | Keyword discovery, competitor monitoring, rank tracking, gap analysis | Lite $129/mo or Standard $249/mo — https://ahrefs.com/pricing |
| Mintlify | Docs platform (if used) | Free (Hobby) or $250/mo (Pro) — https://mintlify.com/pricing |
| PostHog | Analytics, funnels, feature flags for A/B tests | Free up to 1M events/mo, then usage-based — https://posthog.com/pricing |
| Google Search Console | Search analytics, indexation monitoring | Free — https://search.google.com/search-console |
| Anthropic Claude API | Content generation at scale (~40+ pages/month) | ~$15-40/mo (Sonnet 4: $3/$15 per M tokens) — https://anthropic.com/pricing |
| n8n | Orchestration for discovery, generation, publishing, monitoring | Free (self-hosted) or Pro EUR 60/mo — https://n8n.io/pricing |
| Attio | CRM for lead scoring and pipeline tracking | Free up to 3 users — https://attio.com/pricing |
| Loops | Nurture sequences for captured leads | Free up to 1,000 contacts — https://loops.so/pricing |

## Drills Referenced

- `docs-content-scaling-pipeline` — automated keyword discovery, page generation, quality gate, and publishing
- `content-refresh-pipeline` — detect declining pages and auto-generate refreshed content
- `cluster-gap-analysis` — audit keyword coverage, cannibalization, and internal linking
- `threshold-engine` — evaluate 3-month results against pass threshold
