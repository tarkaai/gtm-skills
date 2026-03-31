---
name: affiliate-payout-processing
description: Process, approve, and execute affiliate commission payouts
tool: Rewardful / FirstPromoter / PartnerStack / PayPal / Wise
difficulty: Config
---

# Affiliate Payout Processing

## Prerequisites

- Affiliate program with earned commissions (see `affiliate-commission-configuration`)
- Payout method configured (PayPal, Wise, Stripe Connect, or manual bank transfer)
- Accounting system or spreadsheet for tracking payouts

## Steps

### 1. Review pending commissions

Pull all commissions that have cleared the payout delay and are ready for payment:

```
GET https://api.rewardful.com/v1/commissions?status=approved&payout_eligible=true
Authorization: Bearer {REWARDFUL_API_KEY}
```

Response includes per-affiliate totals:

```json
{
  "data": [
    {
      "affiliate_id": "aff_abc123",
      "affiliate_email": "partner@example.com",
      "pending_amount": 340.00,
      "currency": "USD",
      "commission_count": 7,
      "oldest_commission_date": "2026-02-15"
    }
  ]
}
```

### 2. Check for chargebacks and refunds

Before processing payouts, verify no pending refunds would claw back commissions:

```
GET https://api.rewardful.com/v1/commissions?status=pending_refund&affiliate_id={affiliate_id}
Authorization: Bearer {REWARDFUL_API_KEY}
```

Deduct any refunded commissions from the payout amount before processing.

### 3. Process payouts

**Automatic payouts (Rewardful + PayPal):**

```
POST https://api.rewardful.com/v1/payouts/batch
Authorization: Bearer {REWARDFUL_API_KEY}

{
  "payout_method": "paypal",
  "affiliate_ids": ["aff_abc123", "aff_def456"],
  "note": "March 2026 commissions"
}
```

**Manual payout via Wise (for international partners):**

```
POST https://api.transferwise.com/v1/transfers
Authorization: Bearer {WISE_API_KEY}

{
  "targetAccount": "{wise_recipient_id}",
  "quoteUuid": "{quote_id}",
  "customerTransactionId": "payout-{affiliate_id}-2026-03",
  "details": {
    "reference": "Affiliate commission - March 2026"
  }
}
```

**FirstPromoter auto-payouts:**

```
POST https://firstpromoter.com/api/v1/payouts/process
Authorization: Bearer {FIRSTPROMOTER_API_KEY}

{
  "campaign_id": "{campaign_id}",
  "payout_method": "paypal_mass_pay"
}
```

### 4. Mark commissions as paid

After processing, update the commission status:

```
PUT https://api.rewardful.com/v1/commissions/batch_update
Authorization: Bearer {REWARDFUL_API_KEY}

{
  "commission_ids": ["comm_1", "comm_2", "comm_3"],
  "status": "paid",
  "paid_at": "2026-03-30T00:00:00Z",
  "payment_reference": "paypal-batch-12345"
}
```

### 5. Sync payout to CRM

Log the payout in Attio for relationship tracking:

```
POST https://api.attio.com/v2/notes
Authorization: Bearer {ATTIO_API_KEY}

{
  "parent_object": "people",
  "parent_record_id": "{attio_partner_record_id}",
  "title": "Commission Payout - March 2026",
  "content": "Paid $340.00 for 7 referrals. Lifetime earnings: $1,240.00."
}
```

## Error Handling

- If PayPal payout fails: check affiliate's PayPal email is verified and can receive mass payments
- If commission amount is negative (refund exceeded earned): carry the negative balance to the next payout period rather than requesting repayment
- If duplicate payout detected: check `payment_reference` field before processing; never process the same batch twice

## Output

- Processed commission payouts to all eligible affiliates
- Updated commission statuses in the affiliate platform
- Payout records synced to CRM for relationship tracking
- Accounting trail with payment references
