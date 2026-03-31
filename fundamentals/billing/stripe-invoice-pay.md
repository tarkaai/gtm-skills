---
name: stripe-invoice-pay
description: Programmatically attempt payment on an open invoice or void/forgive a failed invoice
tool: Stripe
difficulty: Config
---

# Stripe Invoice Pay

## Prerequisites

- Stripe account with API access (secret key)
- An open (unpaid) invoice to act on

## Attempt Payment on an Open Invoice

Trigger an immediate payment attempt on an open invoice (useful after a customer updates their payment method):

```bash
curl https://api.stripe.com/v1/invoices/in_XXXXX/pay \
  -u sk_live_YOUR_KEY: \
  -X POST
```

Optional: specify a different payment method than the one on file:

```bash
curl https://api.stripe.com/v1/invoices/in_XXXXX/pay \
  -u sk_live_YOUR_KEY: \
  -d payment_method="pm_XXXXX"
```

Response on success:
```json
{
  "id": "in_XXXXX",
  "status": "paid",
  "amount_paid": 4900,
  "paid": true
}
```

Response on failure:
```json
{
  "error": {
    "code": "card_declined",
    "message": "Your card was declined.",
    "type": "card_error"
  }
}
```

## Void an Invoice (cancel without collecting)

Use when you decide to forgive the charge (e.g., goodwill gesture for a long-time customer):

```bash
curl https://api.stripe.com/v1/invoices/in_XXXXX/void \
  -u sk_live_YOUR_KEY: \
  -X POST
```

Voiding removes the payment obligation. The subscription continues without interruption. Use sparingly -- it reduces revenue.

## Mark Invoice Uncollectible

Use when all recovery attempts have failed and you want to write off the amount:

```bash
curl https://api.stripe.com/v1/invoices/in_XXXXX/mark_uncollectible \
  -u sk_live_YOUR_KEY: \
  -X POST
```

This moves the invoice to `uncollectible` status. The subscription may be canceled depending on your Stripe settings.

## List All Open Invoices (recovery targets)

```bash
curl "https://api.stripe.com/v1/invoices?status=open&limit=100" \
  -u sk_live_YOUR_KEY:
```

Each open invoice is a potential recovery target. Sort by `amount_due` descending to prioritize high-value recoveries.

## Error Handling

- `invoice_not_open`: the invoice was already paid, voided, or uncollectible
- `card_declined`: the payment method still does not work -- route to payment method update flow
- `authentication_required`: the card requires 3D Secure; send the customer to the hosted invoice page instead
- Rate limit: payment attempts are rate-limited; do not retry more than once per hour per invoice

## Alternative Tools

| Tool | Pay/Void Mechanism | Documentation |
|------|-------------------|---------------|
| Stripe | `POST /v1/invoices/:id/pay` | [stripe.com/docs/api/invoices/pay](https://stripe.com/docs/api/invoices/pay) |
| Paddle | Transaction retry via API | [developer.paddle.com](https://developer.paddle.com) |
| Chargebee | `POST /invoices/:id/collect_payment` | [apidocs.chargebee.com](https://apidocs.chargebee.com) |
| Recurly | `PUT /invoices/:id/collect` | [docs.recurly.com](https://docs.recurly.com) |
| Braintree | Transaction retry | [developer.paypal.com/braintree](https://developer.paypal.com/braintree/docs) |
