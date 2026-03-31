---
name: loops-transactional
description: Send transactional emails through Loops API for consistent branding
tool: Loops
product: Loops
difficulty: Beginner
---

# Send Transactional Emails with Loops

## Prerequisites
- Loops account with verified sending domain
- Application backend with ability to make API calls

## Steps

1. **Understand transactional vs marketing.** Transactional emails are triggered by user actions and expected by the recipient: password resets, receipts, usage alerts, invitation confirmations. They do not require unsubscribe links and have higher deliverability than marketing emails.

2. **Create transactional templates.** Build templates in Loops for your core transactional emails: Welcome Email, Password Reset, Invoice/Receipt, Team Invitation, Usage Limit Warning, Account Cancellation Confirmation. Note each template's `transactionalId` for API calls.

3. **Use template variables.** Add dynamic content with Loops variables: `{{firstName}}`, `{{resetLink}}`, `{{planName}}`, `{{usagePercent}}`. Design templates to degrade gracefully if a variable is missing -- use default values where possible.

4. **Trigger emails via API.** Use the Loops Transactional API endpoint:
   ```
   POST /api/v1/transactional
   {
     "transactionalId": "tmpl_welcome_email",
     "email": "jane@acme.com",
     "dataVariables": {
       "firstName": "Jane",
       "planName": "Pro",
       "loginUrl": "https://app.acme.com/login"
     }
   }
   ```
   Response includes a success/fail status and message ID for tracking.

5. **Set up error handling.** Wrap your Loops API calls in try/catch. If Loops returns an error, log it and queue a retry. For critical emails (password reset, payment confirmation), implement a fallback sender (e.g., direct SMTP) in case Loops is unreachable.

6. **Monitor delivery via API.** Check transactional email delivery metrics weekly. Target 99%+ delivery rate. If delivery drops, check your sending domain's DNS records and review bounce reasons. Use n8n to automate daily delivery health checks.
