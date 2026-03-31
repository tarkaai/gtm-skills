---
name: lob-template-create
description: Create a reusable HTML postcard template in Lob with merge variable placeholders
tool: Lob
difficulty: Config
---

# Lob Template Create

Create a reusable HTML template for postcard fronts and backs in Lob. Templates support merge variables so you can personalize each postcard with recipient-specific data (name, company, pain point).

## Authentication

HTTP Basic Auth with your Lob API key as username, empty password.

## API Endpoint

```
POST https://api.lob.com/v1/templates
```

## Request Format

```bash
curl https://api.lob.com/v1/templates \
  -u "$LOB_API_KEY:" \
  -d "description=Postcard Front - Pain Point Variant A" \
  -d "html=<html>
<head>
<style>
  body { margin: 0; padding: 0; font-family: Arial, sans-serif; }
  .front { width: 6.25in; height: 4.25in; padding: 0.25in; box-sizing: border-box; background: #ffffff; }
  h1 { font-size: 24px; color: #1a1a1a; margin-bottom: 8px; }
  p { font-size: 14px; color: #333; line-height: 1.4; }
  .cta { background: #2563eb; color: white; padding: 10px 20px; display: inline-block; border-radius: 4px; margin-top: 12px; font-weight: bold; }
</style>
</head>
<body>
<div class=\"front\">
  <h1>{{first_name}}, {{pain_point_headline}}</h1>
  <p>{{body_copy}}</p>
  <div class=\"cta\">{{cta_text}}</div>
  <p style=\"font-size:11px; margin-top:16px;\">{{qr_or_url}}</p>
</div>
</body>
</html>"
```

## Merge Variables

Use `{{variable_name}}` syntax in your HTML. Common variables for direct mail postcards:

- `{{first_name}}` — Recipient first name
- `{{company}}` — Recipient company name
- `{{pain_point_headline}}` — Personalized headline addressing their specific pain
- `{{body_copy}}` — Main message body
- `{{cta_text}}` — Call-to-action text (e.g., "Book a 15-min call")
- `{{qr_or_url}}` — Personalized URL or QR code reference for tracking

## Response

```json
{
  "id": "tmpl_abc123",
  "description": "Postcard Front - Pain Point Variant A",
  "versions": [
    {
      "id": "vrsn_xyz789",
      "html": "...",
      "date_created": "2026-03-30T12:00:00.000Z"
    }
  ],
  "date_created": "2026-03-30T12:00:00.000Z"
}
```

Store the `id` (starts with `tmpl_`) — this is what you pass to `lob-postcard-send` as `front` or `back`.

## Template Design Rules for Postcards

### 4x6 Postcard
- Front: 6.25" x 4.25" (includes 0.125" bleed on each side)
- Back: 6.25" x 4.25" — right half is reserved for address and postage (do not place content there)

### 6x9 Postcard
- Front: 9.25" x 6.25"
- Back: 9.25" x 6.25" — right third reserved for address block

### Safe Zone
- Keep all text and important images at least 0.25" from the edges

## Updating Templates

```
POST https://api.lob.com/v1/templates/tmpl_abc123/versions
```

Creates a new version of an existing template. The latest version is always used when sending.

## Error Handling

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 200 | Template created | Store `id` for use in postcard sends |
| 401 | Invalid API key | Check credentials |
| 422 | Invalid HTML | Check for unclosed tags, invalid CSS, or template syntax errors |

## Pricing

- Template creation and storage are free on all Lob plans
- You only pay when postcards are printed and mailed

## Notes

- Create separate templates for front and back — each postcard send requires both
- Create multiple variants (A/B) with different headlines or CTAs for testing
- Include a personalized tracking URL or QR code so you can attribute responses to the specific postcard
- Test templates in Lob's test mode — the response includes a PDF preview URL so you can visually inspect before going live
- Keep HTML simple — Lob's rendering engine handles basic CSS but avoid complex layouts, JavaScript, or external font imports
