---
name: instantly-account-setup
description: Set up Instantly accounts and sending domains for cold outreach
tool: Instantly
difficulty: Setup
---

# Set Up Instantly for Cold Email

## Prerequisites
- Instantly account (Growth plan or higher for API access)
- Secondary domain purchased for cold outreach (never use your primary domain)

## Steps

1. **Purchase sending domains.** Buy 2-3 secondary domains that are similar to your primary domain. Example: if your company is acme.com, buy acmehq.com, getacme.com, tryacme.com. Use a registrar like Namecheap or Cloudflare. Cost is roughly $10-15 per domain per year.

2. **Set up DNS records.** For each domain, configure: SPF record (v=spf1 include:instantly.ai ~all), DKIM (Instantly generates this in account settings), and DMARC (v=DMARC1; p=none). These records tell email providers your sending is legitimate.

3. **Create sending accounts.** Set up Google Workspace or Microsoft 365 accounts on each domain. Create 2-3 mailboxes per domain (e.g., dan@acmehq.com, daniel@acmehq.com). This gives you 4-9 sending accounts across your domains.

4. **Connect accounts to Instantly.** In Instantly, go to Accounts > Add Account and connect each mailbox via SMTP/IMAP or OAuth. Verify each connection sends and receives successfully.

5. **Set sending limits.** Configure each account to send a maximum of 30 emails per day initially. After 2 weeks of warmup, increase to 50 per day. Never exceed 75 per account per day.

6. **Add a professional signature.** Set up a simple signature: Name, Title, Company, and a link to your website. Avoid images, HTML, or tracking pixels in the signature -- these hurt deliverability.
