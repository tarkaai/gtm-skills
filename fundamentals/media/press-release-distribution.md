---
name: press-release-distribution
description: Distribute press releases via wire services to reach journalists and publications at scale
tool: PR Newswire
product: Wire Service
difficulty: Config
---

# Press Release Distribution

Distribute press releases through wire services that push your announcement to journalist inboxes, news aggregators, and publication feeds. Wire distribution amplifies reach beyond your own media list.

## Tool Options

| Tool | API/Method | Best For |
|------|-----------|----------|
| PR Newswire | Web portal + API | Largest network, premium outlets (AP, Reuters), geographic targeting |
| Business Wire | Web portal | Berkshire-owned, strong finance/enterprise coverage |
| GlobeNewsWire | Web portal + API | Good mid-tier option, international distribution |
| EIN Presswire | Web portal | Budget-friendly, fast turnaround |
| Newswire.com | Web portal | Small business focused, affordable |
| PRLog | Web submission | Free basic distribution |

## When to Use Wire Distribution

Wire distribution is NOT for every press release. Use it for:
- Product launches (major features, not minor updates)
- Funding announcements
- Major partnerships or integrations
- Original research with data/findings
- Award wins or industry recognition
- Executive hires (C-level)

Do NOT use wire distribution for:
- Minor product updates (pitch directly instead)
- Company blog posts (publish and promote organically)
- Thought leadership pieces (pitch as guest articles instead)

## PR Newswire (Primary)

### Submit via web portal
1. Log in to `https://portal.prnewswire.com`
2. Create new release: headline, subheadline, body, boilerplate, contact info
3. Select distribution: US National (~$800), Regional (~$400), State (~$300)
4. Add targeting: industry verticals, subject codes (technology, business, etc.)
5. Add multimedia: images, video links (increases pickup rate by 2-3x)
6. Schedule: immediate or future date/time
7. Review and submit (editorial review takes 1-2 hours)

### API submission (for automated workflows)

```http
POST https://api.prnewswire.com/v2/releases
Content-Type: application/json
Authorization: Bearer {PRNEWSWIRE_API_KEY}

{
  "headline": "Company X Launches AI-Powered Feature Y",
  "subheadline": "New capability reduces Z by 50%",
  "body": "<p>Full press release HTML body...</p>",
  "boilerplate": "About Company X: ...",
  "contact": {
    "name": "Founder Name",
    "email": "press@company.com",
    "phone": "+1-555-0123"
  },
  "distribution": {
    "circuit": "US-NATIONAL",
    "industry_codes": ["TEK"],
    "subject_codes": ["NEW"]
  },
  "multimedia": [
    {"type": "image", "url": "https://...", "caption": "Product screenshot"}
  ],
  "release_date": "2026-04-01T09:00:00-04:00"
}
```

### Track pickup

After distribution, PR Newswire provides:
- Distribution report: which outlets received it
- Pickup report: which outlets published it (available 24-72 hours later)
- Engagement metrics: views, clicks on links in the release
- Backlink report: which sites link to your website from the release

## EIN Presswire (Budget Option)

### Submit via web portal
1. Go to `https://www.einpresswire.com`
2. Create release: headline, body, contact info
3. Select distribution tier: Basic ($99.95), Standard ($199.95), Premium ($399.95)
4. Add industry targeting
5. Submit (review takes 1-4 hours)

### Tracking
EIN provides: views, outlet pickups, and geographic distribution data.

## Press Release Writing Framework

### Structure
```
HEADLINE: [Action verb] + [Company] + [What happened] + [Why it matters]
  Example: "Tarka Launches AI-Powered GTM Playbook, Enabling Startups to Run Enterprise-Grade Go-to-Market with Zero Budget"

SUBHEADLINE: [Supporting detail or key stat]
  Example: "Open-source playbook covers 150+ plays across marketing, sales, and product"

DATELINE: [City, State, Date] --

LEAD PARAGRAPH: Who, what, when, where, why in 2-3 sentences. The journalist should be able to write their article from this paragraph alone.

BODY:
  - Quote from founder/CEO (make it substantive, not "we're excited")
  - Key details: features, availability, pricing
  - Supporting data or customer validation
  - Quote from customer or partner (if available)

BOILERPLATE: 2-3 sentence company description. Include: what you do, who you serve, key differentiator, website URL.

CONTACT: Name, title, email, phone
```

### Rules for agent-generated press releases
- Keep under 500 words (journalists scan, not read)
- Lead with the newsworthy element, not background
- Quotes should contain insight, not platitudes ("We're excited" = delete)
- Include at least one specific number or data point
- Link to a landing page where journalists can get more info, assets, and images
- Do NOT use superlatives ("best", "revolutionary", "groundbreaking") -- journalists ignore these

## Error Handling

- **Editorial rejection**: Wire services review releases for newsworthiness. If rejected, rewrite the headline to emphasize the news angle (what changed, not what exists).
- **Low pickup**: If fewer than 5 outlets pick up the release, the headline or topic lacks news value. Supplement with direct pitches to your media list.
- **Link issues**: Verify all URLs in the release before submission. Broken links in a press release damage credibility.

## Pricing

| Service | Cost per Release | Best Value Tier |
|---------|-----------------|-----------------|
| PR Newswire | $400-1,500+ | US Regional at ~$400 for startups |
| Business Wire | $400-1,000+ | Similar to PR Newswire |
| GlobeNewsWire | $350-800 | Mid-tier option |
| EIN Presswire | $100-400 | Best budget option at $99.95 basic |
| Newswire.com | $99-549 | Startup Plan at $99/release |
| PRLog | Free-$49 | Free tier for basic distribution |
