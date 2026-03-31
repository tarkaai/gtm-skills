---
name: og-meta-generation
description: Programmatically generate Open Graph meta tags and social share preview cards for product pages and shared content
tool: Vercel OG
difficulty: Setup
---

# OG Meta Generation

Generate dynamic Open Graph images and meta tags so that when users share product URLs on social platforms (LinkedIn, Twitter/X, Slack, Discord), the preview card displays a rich, branded visual with contextual data.

## Approach

Use a serverless OG image generation endpoint (Vercel OG, Cloudflare Workers, or a custom Node.js service) to produce dynamic images based on URL parameters. The meta tags are injected server-side or via middleware so crawlers and link unfurlers see them.

## Tools (pick one)

| Tool | Method | Strengths |
|------|--------|-----------|
| **@vercel/og** (Vercel OG) | Serverless Edge function using Satori + Resvg | Sub-100ms generation, JSX templates, native Vercel deploy |
| **Cloudflare Workers OG** | Workers + HTMLRewriter + Satori | Edge-generated, global CDN, no Vercel dependency |
| **Puppeteer / Playwright** | Headless browser screenshot | Full CSS support, slower (~2s), higher compute cost |
| **imgproxy** | URL-based image transformation | Fast, but limited to image manipulation, not text rendering |
| **Social Share Preview (npm)** | Node library for OG image generation | Self-hosted, customizable templates |

## Implementation (Vercel OG — default stack)

### 1. Create the OG image endpoint

Deploy an API route at `/api/og` that accepts query parameters and returns a PNG:

```typescript
// app/api/og/route.tsx (Next.js App Router)
import { ImageResponse } from '@vercel/og';

export const runtime = 'edge';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const title = searchParams.get('title') ?? 'Check this out';
  const metric = searchParams.get('metric') ?? '';
  const metricValue = searchParams.get('value') ?? '';
  const userName = searchParams.get('user') ?? '';
  const productName = 'YourProduct';

  return new ImageResponse(
    (
      <div style={{
        display: 'flex', flexDirection: 'column', width: '100%', height: '100%',
        background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
        padding: '60px', fontFamily: 'Inter, sans-serif', color: '#ffffff',
      }}>
        <div style={{ fontSize: 28, opacity: 0.7 }}>{productName}</div>
        <div style={{ fontSize: 48, fontWeight: 700, marginTop: 20 }}>{title}</div>
        {metric && (
          <div style={{ display: 'flex', marginTop: 30, gap: 20 }}>
            <div style={{ fontSize: 64, fontWeight: 800 }}>{metricValue}</div>
            <div style={{ fontSize: 24, opacity: 0.8, alignSelf: 'flex-end' }}>{metric}</div>
          </div>
        )}
        {userName && (
          <div style={{ marginTop: 'auto', fontSize: 22, opacity: 0.6 }}>
            Shared by {userName}
          </div>
        )}
      </div>
    ),
    { width: 1200, height: 630 }
  );
}
```

### 2. Inject meta tags on shareable pages

For each shareable page or resource, set the `<meta>` tags server-side:

```html
<meta property="og:title" content="{dynamic title}" />
<meta property="og:description" content="{dynamic description}" />
<meta property="og:image" content="https://yourapp.com/api/og?title={encoded_title}&metric={metric}&value={value}&user={user}" />
<meta property="og:url" content="https://yourapp.com/shared/{resource_id}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://yourapp.com/api/og?title={encoded_title}&metric={metric}&value={value}&user={user}" />
```

### 3. Cache generated images

Set `Cache-Control: public, max-age=86400, s-maxage=604800` on the OG endpoint response. Invalidate by appending a version query parameter (`?v=2`) when the underlying data changes.

## Authentication

No auth required for the OG endpoint itself (crawlers cannot authenticate). Protect against abuse with rate limiting (Vercel Edge Middleware or Cloudflare rate limits). The shareable page behind the OG image may require auth — handle this with a public landing page that shows a preview and prompts sign-in for full access.

## Error Handling

- Missing parameters: return a generic branded OG image (logo + tagline) rather than an error
- Invalid resource ID: return generic image, do not expose 404 details in the image
- Generation timeout (>5s): return a pre-cached fallback image

## Verification

Test OG tags with:
- Twitter Card Validator: `https://cards-dev.twitter.com/validator`
- LinkedIn Post Inspector: `https://www.linkedin.com/post-inspector/`
- Facebook Sharing Debugger: `https://developers.facebook.com/tools/debug/`
- `curl -I` to verify `og:image` URL returns 200 with `content-type: image/png`
