---
name: gong-deal-intelligence
description: Use Gong's API to analyze deal health, identify risks, and forecast outcomes from conversation data
tool: Gong
product: Gong
difficulty: Advanced
---

# Use Gong Deal Intelligence

## Prerequisites
- Gong account with recorded calls
- Gong API access configured

## Steps

1. **Query deal data via API.** Use the Gong REST API to retrieve pipeline data with AI-generated deal scores:
   ```
   GET /v2/deals?filter={"status": "open"}
   ```
   Each deal includes engagement metrics, risk signals, and an AI-generated health score.

2. **Review deal engagement.** Parse the API response for engagement data: number of calls, emails, and stakeholders involved in each deal. More engagement usually means healthier deals. Multi-threaded deals (3+ contacts) close at higher rates.

3. **Check risk signals.** Gong flags deals where competitors were mentioned, pricing objections were raised, or next steps were not set. Use the API to filter for at-risk deals:
   ```
   GET /v2/deals?filter={"riskLevel": "high"}
   ```

4. **Analyze call recordings for at-risk deals.** Use the Gong API to retrieve call transcripts and summaries for the last 2-3 calls on at-risk deals:
   ```
   GET /v2/calls?dealId=<deal-id>&limit=3
   ```
   Identify where the deal may be stalling.

5. **Sync deal intelligence to CRM.** Build an n8n workflow that pulls Gong deal data daily and updates Attio deal records with: deal score, risk level, last call summary, and next steps. This keeps your CRM enriched with conversation intelligence.

6. **Track win/loss patterns via API.** Query closed deals to analyze conversation patterns that correlate with wins vs losses. Use this data to build coaching playbooks and improve discovery call frameworks.
