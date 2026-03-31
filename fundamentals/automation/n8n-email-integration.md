---
name: n8n-email-integration
description: Connect n8n to email tools for automated outreach workflows
tool: n8n
product: n8n
difficulty: Intermediate
---

# Integrate n8n with Email Tools

## Prerequisites
- n8n instance running
- Email tool account (Instantly, Smartlead, or Loops) with API access

## Steps

1. **Set up email tool credentials.** In n8n, create a new credential for your email tool. For Instantly: use API key from Settings > Integrations. For Loops: use the API key from Settings > API. Store credentials securely in n8n's credential manager.

2. **Automate lead-to-campaign flow.** Build a workflow: Trigger (new enriched lead from Clay or CRM) > IF node (filter by lead score > 60) > HTTP Request node (add lead to Instantly campaign via API). This automatically enrolls qualified leads in your outbound sequence.

3. **Route replies to CRM.** Build a workflow: Trigger (Instantly webhook on reply received) > Code node (classify reply as positive/negative using keywords or AI) > IF node (branch on classification) > Attio node (create deal for positive replies). This ensures no interested reply falls through the cracks.

4. **Trigger lifecycle emails from events.** Build a workflow: Trigger (product event webhook) > Set node (map user data to Loops contact properties) > HTTP Request (update Loops contact or trigger transactional email). Use this for onboarding events, feature adoption signals, and usage milestones.

5. **Sync unsubscribes across tools.** Build a workflow: Trigger (unsubscribe event from any email tool) > HTTP Request (add to suppression list in all other email tools) > Attio node (update contact property "email_opt_out" = true). This keeps you compliant across all platforms.

6. **Monitor email health.** Build a scheduled workflow that runs daily, pulls campaign metrics from your email tool via API, and posts a summary to Slack: emails sent, replies received, bounces, and any accounts with deliverability issues.
