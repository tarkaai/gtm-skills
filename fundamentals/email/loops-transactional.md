---
name: loops-transactional
description: Send transactional emails through Loops for consistent branding
tool: Loops
difficulty: Beginner
---

# Send Transactional Emails with Loops

## Prerequisites
- Loops account with verified sending domain
- Application backend with ability to make API calls

## Steps

1. **Understand transactional vs marketing.** Transactional emails are triggered by user actions and expected by the recipient: password resets, receipts, usage alerts, invitation confirmations. They do not require unsubscribe links and have higher deliverability than marketing emails.

2. **Create transactional templates.** In Loops, go to Transactional > New Template. Build templates for your core transactional emails: Welcome Email, Password Reset, Invoice/Receipt, Team Invitation, Usage Limit Warning, Account Cancellation Confirmation. Keep them clean and functional.

3. **Use template variables.** Add dynamic content with Loops variables: {{firstName}}, {{resetLink}}, {{planName}}, {{usagePercent}}. Design templates to degrade gracefully if a variable is missing -- use default values where possible.

4. **Integrate with your API.** Use Loops' Transactional API endpoint to trigger emails from your application. Pass the template ID, recipient email, and a data object containing the template variables. Response includes a success/fail status and message ID for tracking.

5. **Set up error handling.** Wrap your Loops API calls in try/catch. If Loops returns an error, log it and queue a retry. For critical emails (password reset, payment confirmation), implement a fallback sender (e.g., direct SMTP) in case Loops is unreachable.

6. **Monitor delivery.** Check Loops' transactional dashboard weekly. Target 99%+ delivery rate for transactional emails. If delivery drops, check your sending domain's DNS records and review any bounce reasons in the dashboard.
