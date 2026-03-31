---
name: attio-reporting
description: Build pipeline reports and dashboards in Attio for forecasting and performance tracking
tool: Attio
product: Attio
difficulty: Intermediate
---

# Build Reports in Attio

## Prerequisites
- Attio pipeline with historical deal data
- Attio MCP server connected

## Steps

1. **Pipeline velocity report.** Create a view showing average days in each stage. Use the Attio MCP to query deals closed in the last 90 days, calculate the time spent in each stage, and identify bottlenecks. If deals stall in "Proposal Sent" for 10+ days on average, that's your biggest lever.

2. **Win rate dashboard.** Query all deals that reached "Qualified" stage in the last quarter. Calculate: total deals, won deals, lost deals, and win rate percentage. Break down by source (Outbound vs Inbound vs Referral) to see which channels convert best.

3. **Pipeline value report.** Sum the deal values by stage to see your weighted pipeline. Apply stage-specific probabilities: Qualified = 20%, Meeting Booked = 40%, Proposal Sent = 60%, Negotiation = 80%. This gives your weighted forecast.

4. **Activity report.** Count notes and activities per deal per week. Deals with fewer than 2 activities per week are at risk. Flag them automatically using the stale deal automation.

5. **Source attribution.** Query deals grouped by Source field. For each source, calculate: number of deals, total value, average deal size, and win rate. This tells you where to invest more budget.

6. **Export to PostHog.** For advanced analytics, push key deal events (stage changes, wins, losses) to PostHog via n8n. This lets you correlate pipeline data with product usage and marketing touchpoints in a single dashboard.
