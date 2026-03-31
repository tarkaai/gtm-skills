---
name: referral-network-mapping
description: Systematically map your existing network (customers, advisors, investors, peers) to identify intro paths to specific target accounts
category: Partnerships
tools:
  - Clay
  - Attio
  - LinkedIn
fundamentals:
  - clay-enrichment-waterfall
  - clay-people-search
  - attio-lists
  - attio-contacts
  - linkedin-organic-feed-search
---

# Referral Network Mapping

This drill builds a structured map of who in your existing network can introduce you to which target accounts. It replaces ad-hoc "who do I know?" guessing with a systematic enrichment pipeline that scores every connector-target pair by relationship strength and intro likelihood.

## Input

- Target account list in Attio (10-50 companies you want introductions to)
- Your existing network exported from Attio (customers, advisors, investors, partners, former colleagues)
- LinkedIn connection data (exported or scraped via Clay)

## Steps

### 1. Export your network from Attio

Query Attio for all contacts with a relationship tag: "Customer," "Advisor," "Investor," "Partner," "Former Colleague," or "Peer." Using the `attio-contacts` fundamental, pull: name, email, company, title, LinkedIn URL, and relationship type. Export to a Clay table called "Referral Network — {date}."

### 2. Export your target accounts

Query Attio for target accounts. For each account, pull: company name, domain, target contact name, target contact title, target contact LinkedIn URL. If you do not have specific target contacts yet, use the `clay-people-search` fundamental to find the right buyer persona at each target company (e.g., VP Engineering, Head of Product, CTO).

### 3. Build the connection matrix in Clay

Create a Clay table with one row per (connector, target) pair. For each connector in your network, check which target accounts they could potentially introduce you to:

1. **Company overlap**: Use the `clay-enrichment-waterfall` fundamental to check if the connector currently works at, previously worked at, or has invested in any target company. Check employment history, board seats, and advisory roles.
2. **LinkedIn mutual connections**: Use Clay's LinkedIn enrichment to check if the connector and the target contact share mutual connections. High mutual connection count (10+) suggests they likely know each other.
3. **Industry proximity**: Check if the connector operates in the same industry vertical as the target. Same-industry connectors have higher intro credibility.
4. **Event co-attendance**: If available, check conference speaker lists, podcast guest appearances, or community memberships for co-occurrence between connector and target.

### 4. Score each intro path

For each connector-target pair, compute an Intro Likelihood Score (1-10):

- **Direct relationship confirmed** (worked together, invested in them, on their board): 9-10
- **Strong indirect** (10+ mutual connections, same industry, recent LinkedIn interaction): 7-8
- **Moderate indirect** (5-9 mutual connections, adjacent industry): 4-6
- **Weak indirect** (1-4 mutual connections, different industry): 1-3

Also score Connector Willingness (1-5) based on your relationship with the connector:
- **5**: They have made intros for you before, or explicitly offered
- **4**: Strong relationship, they would likely say yes if asked
- **3**: Good relationship but you have never asked for an intro
- **2**: Acquaintance — asking is possible but not guaranteed
- **1**: Weak connection — high risk of being ignored or refused

Composite score = Intro Likelihood * Connector Willingness (max 50).

### 5. Rank and filter intro paths

Sort all connector-target pairs by composite score descending. Filter to keep only pairs scoring 20+ (strong intro paths). For targets with multiple possible connectors, pick the highest-scoring path. For targets with no viable intro paths (all pairs below 10), flag them for cold outreach instead.

### 6. Write the referral map to Attio

Using the `attio-lists` fundamental, create a list called "Referral Map — {date}" with fields:
- Target company
- Target contact (name, title)
- Best connector (name, relationship type)
- Intro likelihood score
- Connector willingness score
- Composite score
- Intro path notes (how they know each other)
- Status: "Ready to Ask" / "Need More Info" / "No Path Found"

### 7. Update the map monthly

Re-run this drill monthly at Baseline+. Networks change — people change jobs, new connections form, relationships deepen. Each re-run should:
- Add new targets from your pipeline
- Remove targets where intros were already made or deals closed
- Update connector willingness based on recent interactions (did they respond to your last ask? did they decline?)
- Check for new connectors added to your CRM

## Output

- Scored referral map in Attio showing the best intro path for each target account
- Prioritized list of connectors to ask, sorted by composite score
- Targets flagged as "no intro path" for alternative outreach strategies
- Monthly refresh cadence to keep the map current

## Triggers

Run once manually at Smoke level. Run monthly via n8n at Baseline+. At Scalable, the n8n workflow auto-triggers when new target accounts are added to Attio.
