---
name: competitive-intelligence-automation
description: Automated pipeline for monitoring competitor changes, delivering real-time battlecards to reps, and triggering competitive positioning when competitors are tagged in deals
category: Sales
tools:
  - n8n
  - Attio
  - Clay
  - PostHog
  - Anthropic
fundamentals:
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - n8n-crm-integration
  - attio-deals
  - attio-notes
  - attio-automation
  - clay-claygent
  - clay-company-search
  - competitor-changelog-monitoring
  - competitive-positioning-generation
  - posthog-custom-events
  - posthog-dashboards
---

# Competitive Intelligence Automation

This drill builds the always-on automation layer for competitive intelligence. It connects three loops: (1) monitor competitor changes in the market, (2) deliver battlecards when a competitor is tagged in a deal, and (3) surface competitive insights from product usage and web behavior. Together these loops ensure every rep has current competitive intelligence at the moment they need it.

## Input

- Attio CRM with Competitors object populated (from `competitive-battlecard-assembly`)
- At least 5 tracked competitors with battlecards
- Clay account for web scraping and enrichment
- n8n instance for orchestration
- PostHog tracking on website and product

## Steps

### 1. Build the competitor change monitoring workflow (n8n)

Create an n8n workflow triggered by weekly cron (Monday 6 AM):

1. **Fetch competitor list** from Attio — query the Competitors object for all active competitors
2. **Run changelog monitoring** for each competitor using `competitor-changelog-monitoring`:
   - Scrape changelog URLs via Clay Claygent
   - Scrape pricing pages via Clay Claygent
   - Compare content hashes against last-known values stored in Attio
3. **Classify changes** using Claude API:
   - Input: previous content, current content, competitor name
   - Output: `change_type`, `change_summary`, `competitive_impact` (1-5), `positioning_affected` (boolean)
4. **Route by impact level:**
   - Impact 1-2: Log to Attio Competitor record, no alert
   - Impact 3-4: Log to Attio + send Slack alert to sales channel + update battlecard notes
   - Impact 5: Log to Attio + Slack alert + create urgent task for competitive strategy review
5. **Fire PostHog event:** `competitor_change_detected` with properties: competitor_name, change_type, competitive_impact

### 2. Build the battlecard delivery workflow (n8n)

Create an n8n workflow triggered by Attio webhook — fires when `competitors_evaluated` field is updated on a deal:

1. **Parse the competitor names** from the deal's `competitors_evaluated` field
2. **Fetch battlecards** from Attio Competitors object for each named competitor
3. **Generate tailored positioning** using `competitive-positioning-generation`:
   - Pull deal context: company, industry, deal value, top pains, champion, decision criteria
   - Pull competitor battlecard: strengths, weaknesses, win rate, common objections
   - Generate: verbal response, trap questions, comparison talking points, follow-up email, champion ammunition
4. **Deliver the package** to the deal owner:
   - Slack DM with summary: "Competitive alert: {prospect} is evaluating {competitors}. Win rate against {primary_competitor}: {rate}%. Battlecard and positioning attached."
   - Attach: full positioning response, relevant case studies (query Attio for won deals against this competitor in the same industry)
5. **Fire PostHog event:** `battlecard_delivered` with properties: deal_id, competitor_name, deal_value

### 3. Build the web behavior competitive trigger (n8n)

Create an n8n workflow triggered by PostHog webhook — fires when a known prospect visits a competitor comparison page or pricing page:

1. **Identify the prospect** from PostHog person properties (email or company match to Attio contact)
2. **Identify the page context** — which competitor comparison page? Which pricing tier page?
3. **Generate contextual positioning content** using Claude:
   - "This prospect is comparing us to {competitor} based on their page visit pattern. Their deal has these pains: {pains}. Generate a 3-sentence email that addresses their likely evaluation questions without mentioning we know they visited this page."
4. **Route the action:**
   - If deal exists in Attio and has an owner: send Slack alert to owner with context + suggested response
   - If no deal exists: create a warm outreach task — this person is actively evaluating solutions
5. **Fire PostHog event:** `competitive_page_trigger` with properties: prospect_email, page_visited, competitor_inferred

### 4. Build the competitive intelligence dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

| Panel | Query | Purpose |
|-------|-------|---------|
| Competitor frequency (30d) | Count `competitor_named` grouped by `competitor_name` | Which competitors appear most |
| Win rate by competitor | `deal_won` / (`deal_won` + `deal_lost`) where `competitor_name` = X | Where we win and lose |
| Competitive risk distribution | Count deals grouped by `competitive_risk` | Pipeline risk assessment |
| Battlecard delivery rate | `battlecard_delivered` / `competitive_situation_identified` | Are reps getting intel |
| Competitor change velocity | Count `competitor_change_detected` by week | Market movement speed |
| Discovery quality trend | Average `seller_discovery_quality` by week | Are reps improving |
| Time-to-battlecard | Average time between `competitive_situation_identified` and `battlecard_delivered` | Delivery speed |

### 5. Set up guardrail alerts

Configure n8n alert workflows:
- **New competitor spike:** If a competitor is mentioned in 3+ deals in one week but has no battlecard, alert the team to prioritize building one
- **Win rate drop:** If win rate against any tracked competitor drops below 35% over a 4-week window, alert for competitive strategy review
- **Discovery gap:** If `competitive_situation_identified` events drop below 60% of qualified deals in any 2-week period, alert that discovery process is degrading
- **Stale battlecard:** If a Competitor record's `Last Updated` is older than 30 days and mention count > 5, flag for refresh

## Output

- Weekly competitor change monitoring with impact-based alerting
- Real-time battlecard delivery when competitors are tagged in deals
- Web behavior triggers that surface competitive intent from prospects
- Competitive intelligence dashboard with trend tracking
- Guardrail alerts for competitive health degradation

## Triggers

- **Competitor monitoring:** Weekly cron (Monday 6 AM)
- **Battlecard delivery:** Attio webhook on `competitors_evaluated` field update
- **Web behavior trigger:** PostHog webhook on competitor comparison page visits
- **Guardrail checks:** Daily cron (8 AM) for win rate, discovery rate, and staleness checks
