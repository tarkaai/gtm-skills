---
name: linkedin-automation-sequence
description: Automate LinkedIn connection requests and follow-up message sequences via LinkedIn automation tools
tool: Expandi
product: LinkedIn Automation
difficulty: Config
---

# LinkedIn Automation Sequence

Automate LinkedIn outreach at scale: connection requests, follow-up messages, profile visits, and skill endorsements. These tools operate via browser extension or cloud proxy to simulate human LinkedIn activity.

## Tool Options

| Tool | API/Integration | Best For |
|------|----------------|----------|
| Dripify | REST API + webhooks | Cloud-based, safe daily limits, CRM sync |
| Expandi | REST API + webhooks | Smart sequences with multi-channel, IP warmup |
| PhantomBuster | REST API | Scraping + automation combos, flexible triggers |
| Linked Helper | Local app + CSV export | Budget option, runs from desktop |
| Waalaxy | REST API + webhooks | Combined LinkedIn + email sequences |

## Authentication

**Dripify:**
```
Authorization: Bearer {DRIPIFY_API_KEY}
Base URL: https://api.dripify.io/v1
```

**Expandi:**
```
Authorization: Bearer {EXPANDI_API_KEY}
Base URL: https://api.expandi.io/api/v1
```

**PhantomBuster:**
```
X-Phantombuster-Key: {PHANTOMBUSTER_API_KEY}
Base URL: https://api.phantombuster.com/api/v2
```

## Operations

### 1. Create a campaign / sequence

**Dripify:**
```
POST https://api.dripify.io/v1/campaigns
{
  "name": "Mar24-Series-A-CTOs-LI-Outreach",
  "linkedin_account_id": "{ACCOUNT_ID}",
  "sequence": [
    {
      "action": "visit_profile",
      "delay_days": 0
    },
    {
      "action": "connect",
      "delay_days": 1,
      "message": "Hi {{firstName}}, saw your post about {{topic}}. We're working on something similar for {{companyName}} -- would love to connect."
    },
    {
      "action": "message",
      "delay_days": 3,
      "message": "Thanks for connecting, {{firstName}}. Quick question: how is your team currently handling {{pain_point}}? Curious if you've run into the same issues we hear from other {{title}}s.",
      "condition": "connected"
    },
    {
      "action": "message",
      "delay_days": 7,
      "message": "Last thought, {{firstName}} -- we helped {{similar_company}} cut {{metric}} by {{result}}. Worth a 15-min chat? Here's my calendar: {{booking_link}}",
      "condition": "no_reply"
    }
  ],
  "daily_limits": {
    "connections": 20,
    "messages": 40,
    "profile_visits": 50
  }
}
```

**Expandi:**
```
POST https://api.expandi.io/api/v1/campaigns
{
  "name": "Mar24-Series-A-CTOs-LI-Outreach",
  "type": "connector",
  "steps": [
    {"type": "view_profile", "delay": 0},
    {"type": "connect", "delay": 86400, "note": "Hi {{firstName}}..."},
    {"type": "message", "delay": 259200, "text": "Thanks for connecting..."},
    {"type": "message", "delay": 604800, "text": "Last thought..."}
  ],
  "schedule": {
    "timezone": "America/New_York",
    "days": ["mon", "tue", "wed", "thu", "fri"],
    "hours": {"start": 8, "end": 17}
  }
}
```

### 2. Import prospects to campaign

**Dripify:**
```
POST https://api.dripify.io/v1/campaigns/{CAMPAIGN_ID}/leads
{
  "leads": [
    {
      "linkedin_url": "https://www.linkedin.com/in/janesmith",
      "first_name": "Jane",
      "company_name": "Acme Corp",
      "custom_vars": {
        "topic": "pipeline automation",
        "pain_point": "manual CRM updates",
        "similar_company": "TechCo",
        "booking_link": "https://cal.com/founder/discovery"
      }
    }
  ]
}
```

**PhantomBuster (via Sales Navigator search):**
```
POST https://api.phantombuster.com/api/v2/agents/launch
{
  "id": "{SALES_NAV_SEARCH_EXPORT_AGENT_ID}",
  "argument": {
    "searchUrl": "https://www.linkedin.com/sales/search/people?query=...",
    "numberOfProfiles": 100
  }
}
```

### 3. Monitor campaign replies and connection accepts

**Dripify webhook:**
```
POST {YOUR_WEBHOOK_URL}
// Dripify sends events for:
// - connection_accepted
// - message_replied
// - message_sent
// Payload includes lead data, message content, and timestamp
```

**Expandi webhook:**
```
POST {YOUR_WEBHOOK_URL}
{
  "event": "reply_received",
  "lead": {"linkedin_url": "...", "first_name": "..."},
  "message": "Sure, I'd be happy to chat...",
  "campaign_id": "..."
}
```

Route these webhooks to n8n for CRM updates and cross-channel coordination.

### 4. Retrieve campaign analytics

**Dripify:**
```
GET https://api.dripify.io/v1/campaigns/{CAMPAIGN_ID}/stats
```
Returns: connection_requests_sent, connections_accepted, messages_sent, replies_received, acceptance_rate, reply_rate.

### 5. Pause or stop a campaign

```
PUT https://api.dripify.io/v1/campaigns/{CAMPAIGN_ID}
{
  "status": "paused"
}
```

Pause immediately if: acceptance rate drops below 15%, reply rate drops below 5%, or LinkedIn sends a warning.

## Safety Guardrails

- **Daily limits**: Never exceed 25 connection requests/day (LinkedIn's soft limit). Start at 15 and ramp over 2 weeks.
- **Warm up**: New or inactive accounts need 2 weeks of manual activity (posting, commenting, browsing) before automation.
- **Personalization**: Never send identical messages to more than 10 people. Vary templates using merge fields.
- **Business hours only**: Send during 8am-5pm in the prospect's timezone. Weekend sends look automated.
- **Withdraw stale requests**: Withdraw pending connection requests older than 3 weeks. Too many pending requests flags your account.
- **Stop on positive signal**: If a prospect replies positively, immediately stop the automation sequence and hand off to human follow-up.

## Error Handling

- **LinkedIn restriction warning**: Pause all automation for 48-72 hours. Reduce daily limits by 50% when resuming.
- **Account temporarily restricted**: Stop automation entirely. Do manual activity only for 1 week. Resume at half limits.
- **Prospect has open profile**: Skip connection request, send InMail directly (requires Sales Navigator).
- **Duplicate detection**: Check CRM before adding to campaign. Never run the same prospect through two LinkedIn campaigns simultaneously.
