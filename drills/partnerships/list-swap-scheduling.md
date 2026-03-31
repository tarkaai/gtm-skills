---
name: list-swap-scheduling
description: Automate the coordination, timing, and cadence of list swaps across a portfolio of 10+ partners
category: Partnerships
tools:
  - n8n
  - Attio
  - PostHog
  - Loops
fundamentals:
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
  - n8n-crm-integration
  - attio-automation
  - attio-deals
  - loops-broadcasts
---

# List Swap Scheduling

This drill builds the automation layer that coordinates list swaps across a portfolio of 10+ partners. Without it, managing swap timing, reciprocal sends, email approval, and follow-up across many partners becomes a manual bottleneck. The drill ensures no swap falls through the cracks — every partner gets their email sent on time, every reciprocal commitment is honored, and performance data flows back automatically.

## Input

- Active partner list in Attio (from `partner-prospect-research` drill, status: "Active")
- n8n instance configured with Attio, PostHog, and Loops integrations
- Swap email templates from previous `list-swap-email-copy` runs
- Partner swap cadence agreements (monthly, bimonthly, quarterly per partner)

## Steps

### 1. Build the swap calendar workflow

Using the `n8n-scheduling` fundamental, create a recurring workflow that manages swap timing:

- **Trigger**: Weekly cron (Monday 9am)
- **Action 1**: Query Attio for active partners where "Next Swap Date" is within the next 14 days
- **Action 2**: For each upcoming swap, check status fields in Attio:
  - "Our Email Status": draft / approved / sent-to-partner / confirmed-sent
  - "Partner Email Status": received / reviewed / scheduled / sent
- **Action 3**: For swaps missing our email copy, trigger alert: "Swap email needed for {partner} by {date}"
- **Action 4**: For swaps where we received the partner's email but haven't scheduled it, trigger alert: "Schedule {partner}'s email to our list by {date}"
- **Action 5**: For swaps where both emails are ready, confirm the send date with both parties via automated reminder email
- **Action 6**: Update Attio with current status after each check

### 2. Build the reciprocal send automation

Using the `loops-broadcasts` fundamental and `n8n-triggers`, automate sending the partner's email to your list:

- **Trigger**: Attio webhook fires when a partner record's "Partner Email Status" changes to "reviewed" (meaning you approved it)
- **Action 1**: Create a Loops broadcast with the partner's email content, targeting the agreed segment of your list
- **Action 2**: Schedule the broadcast for the agreed swap date and time
- **Action 3**: After send, update Attio: "Partner Email Status" = "sent", log send timestamp
- **Action 4**: Fire PostHog event `list_swap_reciprocal_sent` with partner_slug property

### 3. Build the confirmation workflow

Using the `n8n-triggers` fundamental, create a workflow that confirms both sides sent:

- **Trigger**: Daily cron at 6pm on swap days
- **Action 1**: Check Attio for swaps scheduled today
- **Action 2**: For each swap, verify:
  - Did the partner confirm they sent our email? (Check for "confirmed-sent" status or partner reply)
  - Did we send the partner's email? (Check Loops broadcast status)
- **Action 3**: If both confirmed: mark swap as "Completed" in Attio, set "Next Swap Date" based on agreed cadence
- **Action 4**: If one side didn't send: alert in Slack, send a polite follow-up to the delinquent party
- **Action 5**: If a partner misses 2 consecutive swap dates: flag partner as "Unreliable" in Attio

### 4. Build the cadence management workflow

Using the `n8n-scheduling` and `attio-automation` fundamentals, manage per-partner swap frequency:

- **Monthly partners** (high-performers from Baseline): schedule 12 swaps/year, staggered across weeks
- **Bimonthly partners** (solid performers): schedule 6 swaps/year
- **Quarterly partners** (new or lower-volume partners): schedule 4 swaps/year
- **Never swap the same partner more than once per month** to avoid audience fatigue
- **Never schedule more than 3 inbound swaps to your list in the same week** to protect your own list engagement

After each completed swap, the workflow automatically sets the next swap date based on the partner's cadence tier.

### 5. Build the performance-triggered cadence adjustment

Using the `n8n-triggers` and `attio-deals` fundamentals, create workflows that auto-adjust cadence:

- **Upgrade trigger**: If a partner's last 2 swaps both exceeded 50 clicks and 2 meetings, propose upgrading cadence (quarterly → bimonthly, bimonthly → monthly). Log the recommendation in Attio for human approval.
- **Downgrade trigger**: If a partner's last 2 swaps both produced <10 clicks, propose downgrading or pausing. Log the recommendation in Attio.
- **Pause trigger**: If your list's engagement (open rate, click rate) drops >20% in weeks with 3+ inbound swaps, automatically reduce inbound swap frequency for the next month.

### 6. Build the swap pipeline dashboard

Using Attio and PostHog, maintain a live view of the swap portfolio:

**Attio fields per partner (updated by n8n after each swap):**
- Total swaps completed
- Total clicks received (outbound)
- Total meetings generated (outbound)
- Total clicks given (inbound — how your list responded to their content)
- Net swap value (received clicks minus given clicks)
- Swap cadence tier
- Next swap date
- Partner reliability score (% of scheduled swaps completed on time)

## Output

- Automated swap calendar with 14-day lookahead alerts
- Reciprocal send automation via Loops
- Confirmation workflow ensuring both sides honor commitments
- Per-partner cadence management with performance-based adjustments
- Swap pipeline dashboard with live status and performance data

## Triggers

Build these workflows once at the start of Scalable level. They run continuously. Review cadence tiers monthly based on swap performance data.
