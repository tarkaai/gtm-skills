---
name: sms-phone-number-provisioning
description: Provision a phone number and register for A2P 10DLC compliance
tool: Twilio
difficulty: Setup
---

# SMS Phone Number Provisioning

Provision a local or toll-free phone number for SMS outreach and complete A2P 10DLC registration required for business-to-person messaging in the US.

## Why A2P 10DLC Matters

US carriers (AT&T, T-Mobile, Verizon) require A2P 10DLC registration for all business SMS sent via local (10-digit) numbers. Without registration, messages are throttled or blocked. Registration involves:
1. Brand registration (your company)
2. Campaign registration (your use case)
3. Number assignment to the campaign

## Twilio (Default)

### Step 1: Buy a phone number

```bash
curl -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/IncomingPhoneNumbers.json" \
  --data-urlencode "AreaCode=415" \
  --data-urlencode "SmsEnabled=true" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
```

Cost: $1.15/month for a local US number.

### Step 2: Register your brand

Via Twilio Console > Messaging > Trust Hub > A2P Brand Registration. Provide:
- Company legal name, EIN, address
- Company type (private, public, nonprofit)
- Stock exchange and ticker (if public)

Or via API:
```bash
curl -X POST "https://messaging.twilio.com/v1/a2p/BrandRegistrations" \
  -d "CustomerProfileBundleSid=BUxxxxxxxx" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
```

Brand registration fee: $4 one-time. Vetting fee: $40 one-time (optional but improves throughput).

### Step 3: Register your campaign

```bash
curl -X POST "https://messaging.twilio.com/v1/Services/$TWILIO_MESSAGING_SERVICE_SID/UsAppToPerson" \
  -d "BrandRegistrationSid=BNxxxxxxxx" \
  -d "Description=Sales outreach to solution-aware B2B prospects" \
  -d "MessageFlow=Prospects opt in via website form or respond to initial outreach. They can reply STOP at any time." \
  -d "MessageSamples=[\"Hi {{first_name}}, saw {{company}} is scaling {{pain_area}}. We help teams like yours cut that timeline in half. Worth a 10-min chat? Reply YES or STOP to opt out.\"]" \
  -d "UseCase=MIXED" \
  -d "HasEmbeddedLinks=true" \
  -d "HasEmbeddedPhone=false" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
```

Campaign registration fee: $15/campaign one-time.

### Step 4: Add number to Messaging Service

```bash
curl -X POST "https://messaging.twilio.com/v1/Services/$TWILIO_MESSAGING_SERVICE_SID/PhoneNumbers" \
  -d "PhoneNumberSid=PNxxxxxxxx" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
```

### Throughput after registration

- Standard brand: 15-75 SMS/second (varies by carrier trust score)
- Sole proprietor: 1 SMS/second (very limited)
- High-volume brands with secondary vetting: up to 225 SMS/second

## Salesmsg

Number provisioning and A2P 10DLC registration handled through Salesmsg dashboard: Settings > Phone Numbers > Add Number. Salesmsg manages the carrier registration process. Registration fee: included in plan. Processing time: 1-5 business days.

## OpenPhone (Quo)

Each Quo user gets one local or toll-free number included. A2P 10DLC registration: Settings > Business Texting Registration. One-time fee: $19.50 + $1.50-3.00/month ongoing. Processing time: 2-7 business days.

## Error Handling

- Registration rejected: Review company information for accuracy. Common issues: EIN mismatch, unregistered business name, insufficient campaign description.
- Number not SMS-capable: Verify `SmsEnabled=true` on the number resource. Some numbers are voice-only.
- Low throughput: Apply for secondary brand vetting ($40 via Twilio) to increase per-second sending rate.

## Timeline

Allow 3-7 business days for full A2P 10DLC registration. Start this BEFORE writing message copy. Do NOT send any outbound SMS until registration is confirmed and active.
