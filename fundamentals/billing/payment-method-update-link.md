---
name: payment-method-update-link
description: Generate a secure one-click link for customers to update their payment method without logging in
tool: Stripe
difficulty: Config
---

# Payment Method Update Link

## Prerequisites

- Stripe account with Customer Portal enabled
- API access with secret key

## Generate a Billing Portal Session

Create a Stripe Customer Portal session that drops the user directly into payment method update:

```bash
curl https://api.stripe.com/v1/billing_portal/sessions \
  -u sk_live_YOUR_KEY: \
  -d customer="cus_XXXXX" \
  -d return_url="https://app.yourproduct.com/billing"
```

Response:
```json
{
  "id": "bps_XXXXX",
  "url": "https://billing.stripe.com/p/session/XXXXX",
  "return_url": "https://app.yourproduct.com/billing",
  "created": 1234567890
}
```

The `url` field is a secure, single-use link that takes the customer directly to the Stripe-hosted portal where they can update their card, switch payment methods, or view invoices. No login required -- the session is authenticated via the URL token.

## Configure the Billing Portal

Before generating links, configure what customers can do in the portal:

```bash
curl https://api.stripe.com/v1/billing_portal/configurations \
  -u sk_live_YOUR_KEY: \
  -d "features[payment_method_update][enabled]"=true \
  -d "features[invoice_history][enabled]"=true \
  -d "features[subscription_cancel][enabled]"=false \
  -d "business_profile[headline]"="Update your payment method"
```

Key settings:
- Enable `payment_method_update` so customers can add/change cards
- Enable `invoice_history` so they can see/pay outstanding invoices
- Optionally disable `subscription_cancel` to prevent churn from the update flow
- Customize `business_profile.headline` to set expectations

## Link Behavior

- Links expire after 24 hours or first use, whichever comes first
- Each link is single-customer, single-use -- cannot be shared or reused
- After updating, the customer is redirected to your `return_url`
- Stripe automatically retries the failed invoice after a successful payment method update

## Generate Links in Bulk (for dunning campaigns)

For each customer with a failed payment, generate a unique link:

```javascript
const failedCustomers = await stripe.invoices.list({
  status: 'open',
  limit: 100
});

const links = await Promise.all(
  failedCustomers.data.map(async (invoice) => {
    const session = await stripe.billingPortal.sessions.create({
      customer: invoice.customer,
      return_url: 'https://app.yourproduct.com/billing?recovered=true'
    });
    return {
      customer_id: invoice.customer,
      invoice_id: invoice.id,
      update_url: session.url,
      amount_due: invoice.amount_due
    };
  })
);
```

Pass these links to your email tool (Loops, Intercom) for personalized recovery emails.

## Error Handling

- If the customer ID is invalid, Stripe returns `resource_missing` -- skip and log
- If the portal is not configured, Stripe returns `invalid_request_error` -- configure the portal first
- Links are time-limited (24h); if sending in batch emails, generate links at send time, not in advance
- Rate limit: Stripe allows ~100 portal session creations per second

## Alternative Tools

| Tool | Update Mechanism | Documentation |
|------|-----------------|---------------|
| Stripe | Billing Portal session URL | [stripe.com/docs/customer-management/portal-deep-links](https://stripe.com/docs/customer-management/portal-deep-links) |
| Paddle | Paddle.js update checkout | [developer.paddle.com](https://developer.paddle.com) |
| Chargebee | Hosted page for card update | [chargebee.com/docs](https://www.chargebee.com/docs) |
| Recurly | Hosted payment page | [docs.recurly.com](https://docs.recurly.com) |
| Braintree | Drop-in UI for payment update | [developer.paypal.com/braintree](https://developer.paypal.com/braintree/docs) |
