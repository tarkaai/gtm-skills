---
name: competitive-intel-aggregation
description: Aggregate competitor mentions from win/loss data into a structured competitive intelligence database
tool: Attio
product: Attio
difficulty: Config
---

# Aggregate Competitive Intelligence from Win/Loss Data

Build a structured competitive intelligence database from win/loss interview data. Every interview that mentions a competitor is a data point. Aggregate enough data points and patterns emerge.

## Prerequisites

- Attio CRM with deal records tagged with win/loss outcomes
- At least 10 completed win/loss interviews with extracted insights (see `transcript-insight-extraction`)
- n8n instance for automation

## Steps

1. **Create a Competitors object in Attio.** Using the Attio MCP, create a custom object called "Competitors" with these attributes:
   - Name (text) — competitor company name
   - Mentions (number) — count of times mentioned in interviews
   - Win Rate Against (number) — percentage of deals won when this competitor was in the deal
   - Loss Rate Against (number) — percentage of deals lost to this competitor
   - Common Objections (text, multi-line) — recurring objections buyers raise about us vs them
   - Their Strengths (text, multi-line) — what buyers say they do better
   - Their Weaknesses (text, multi-line) — what buyers say they do worse
   - Last Updated (date) — when this record was last refreshed

2. **Query win/loss insights from deal notes.** Using the Attio MCP, query all deal notes tagged "win-loss-insight" from the last 90 days. Parse the COMPETITORS_MENTIONED field from each. Build a frequency table: which competitors appear most often?

3. **Calculate win/loss rates per competitor.** For each competitor mentioned in 3+ deals:
   - Count deals where we won AND this competitor was mentioned
   - Count deals where we lost AND this competitor was mentioned
   - Calculate: Win Rate Against = wins / (wins + losses) * 100
   Update the Competitors object in Attio with these numbers.

4. **Extract competitive themes.** For each competitor, pull all PRODUCT_FEEDBACK and SALES_PROCESS_FEEDBACK entries from deals where they were mentioned. Use Claude API to summarize into 3 categories:
   - What buyers say they do better than us (Their Strengths)
   - What buyers say we do better than them (Their Weaknesses from their perspective)
   - Common objections that come up in competitive deals

5. **Build a competitive battlecard.** For each competitor with 5+ mentions, generate a battlecard note in Attio:
   ```
   ## {Competitor Name} Battlecard
   **Win rate against them:** {X}%
   **They win when:** {summary of their strengths from buyer quotes}
   **We win when:** {summary of our strengths from buyer quotes}
   **Handle this objection:** "{most common objection}" → {recommended response}
   **Key quotes from buyers:** {2-3 verbatim quotes}
   **Last updated:** {date}
   ```

6. **Set up refresh automation.** Create an n8n workflow that runs weekly:
   - Trigger: Cron schedule (every Monday 9am)
   - Query new win/loss insights from the past 7 days
   - Update competitor mention counts, win/loss rates, and themes
   - If any competitor's win rate against drops below 40%, send a Slack alert to the sales team

7. **Track trends over time.** Each time the weekly refresh runs, log the current win rate against each competitor as a PostHog event: `competitive_win_rate_updated` with properties `competitor_name` and `win_rate`. This creates a time series so you can see if competitive positioning is improving or degrading.
