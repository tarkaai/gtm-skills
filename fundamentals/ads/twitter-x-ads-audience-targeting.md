---
name: twitter-x-ads-audience-targeting
description: Build and refine X Ads audiences using keywords, interests, follower lookalikes, and custom audiences
tool: X Ads
difficulty: Config
---

# Twitter/X Ads Audience Targeting

Build precise audiences on X Ads for B2B SaaS campaigns. X's strength is real-time interest signals — keywords people tweet about, handles they follow, and topics they engage with.

## Custom Audiences (Tailored Audiences)

Upload your own lists for targeting or exclusion.

### Create a list-based custom audience

```
POST /12/accounts/{account_id}/custom_audiences

{
  "name": "Existing Customers - Exclude",
  "list_type": "EMAIL"
}
```

List types: `EMAIL`, `DEVICE_ID`, `TWITTER_ID`, `PHONE_NUMBER`.

### Upload users to the audience

```
POST /12/accounts/{account_id}/custom_audiences/{audience_id}/users

{
  "operation_type": "Update",
  "users": [
    {"hashed_email": ["{SHA256_HASH_1}", "{SHA256_HASH_2}"]}
  ]
}
```

Emails must be lowercase and SHA-256 hashed before upload. Minimum audience size: 100 matched users.

### Website activity audience

```
POST /12/accounts/{account_id}/tailored_audience_memberships

{
  "account_id": "{ACCOUNT_ID}",
  "audience_names": ["Website Visitors 30d"],
  "js_event": "pageview"
}
```

Requires the X pixel installed on your site. Collects visitors automatically.

## Keyword Targeting

Target users based on what they recently tweeted, searched, or engaged with.

```
POST /12/accounts/{account_id}/targeting_criteria

{
  "line_item_id": "{LINE_ITEM_ID}",
  "targeting_type": "KEYWORD",
  "targeting_value": "devops automation"
}
```

Keyword strategies for solution-aware B2B:
- **Problem keywords**: Terms your ICP uses when describing their pain. "slow deployments", "manual QA", "onboarding bottleneck"
- **Solution-category keywords**: The category your product belongs to. "deployment automation", "testing platform", "onboarding software"
- **Competitor brand keywords**: Target people discussing competitors. Use with care — check X's policies.
- **Event/conference keywords**: Hashtags and names of relevant industry events.

Keywords match on exact phrase and close variants. Add 25-50 keywords per ad group. Use negative keywords via `NEGATIVE_KEYWORD` targeting type to exclude irrelevant matches.

## Follower Lookalikes

Target users who behave like followers of specific handles. This is X's most powerful B2B signal.

```
POST /12/accounts/{account_id}/targeting_criteria

{
  "line_item_id": "{LINE_ITEM_ID}",
  "targeting_type": "FOLLOWER_LOOKALIKES",
  "targeting_value": "{HANDLE_WITHOUT_@}"
}
```

Build a list of 10-20 handles:
- Direct competitors
- Industry thought leaders your ICP follows
- Media outlets / podcasts your ICP consumes
- SaaS review platforms (G2, TrustRadius handles)

Use `GET /12/targeting_criteria/locations`, `GET /12/targeting_criteria/interests`, etc. to discover valid targeting values.

## Interest Targeting

```
POST /12/accounts/{account_id}/targeting_criteria

{
  "line_item_id": "{LINE_ITEM_ID}",
  "targeting_type": "INTEREST",
  "targeting_value": "technology"
}
```

Fetch all interest categories:
```
GET /12/targeting_criteria/interests
```

For B2B SaaS: Technology, Business, Startups, Computer Programming, Enterprise Software, Cloud Computing, Data Science.

## Conversation Topics

```
POST /12/accounts/{account_id}/targeting_criteria

{
  "line_item_id": "{LINE_ITEM_ID}",
  "targeting_type": "CONVERSATION_TOPIC",
  "targeting_value": "{TOPIC_ID}"
}
```

10,000+ topics available. Fetch with:
```
GET /12/targeting_criteria/conversations
```

More granular than interests. Targets users who actively participate in conversations about specific topics.

## Audience Sizing

After adding targeting criteria to a line item, estimate reach:

```
GET /12/accounts/{account_id}/reach_estimate?line_item_id={LINE_ITEM_ID}
```

Response includes `count` (estimated audience size). Target 50,000-500,000 for B2B campaigns. Below 50,000 limits delivery. Above 500,000 may be too broad.

## Exclusions

Always exclude:
1. Existing customers (upload custom audience from CRM, set as `NEGATIVE`)
2. Recent converters (website custom audience filtered to conversion events)
3. Internal team members

```
POST /12/accounts/{account_id}/targeting_criteria

{
  "line_item_id": "{LINE_ITEM_ID}",
  "targeting_type": "TAILORED_AUDIENCE",
  "targeting_value": "{CUSTOM_AUDIENCE_ID}",
  "operator_type": "NE"
}
```

## Error Handling

- `AUDIENCE_TOO_SMALL`: Custom audience has fewer than 100 matched users. Upload more records.
- `INVALID_TARGETING_VALUE`: The keyword, interest, or handle does not exist. Verify via the lookup endpoints.
- `TOO_MANY_TARGETING_CRITERIA`: Maximum 200 criteria per line item. Consolidate or split into separate line items.
