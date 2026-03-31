---
name: sitemap-generation
description: Programmatically generate and submit XML sitemaps for bulk page indexation
tool: Dev Tools
product: Runtime
difficulty: Setup
---

# Sitemap Generation

Generate XML sitemaps programmatically for hundreds or thousands of pages. Submit to Google Search Console to accelerate indexation of programmatic SEO pages.

## Sitemap XML Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/solutions/crm-for-startups</loc>
    <lastmod>2026-03-30</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <!-- Repeat for each page -->
</urlset>
```

Rules:
- Maximum 50,000 URLs per sitemap file
- Maximum 50MB uncompressed per file
- For >50,000 URLs, create a sitemap index file referencing multiple sitemaps

## Sitemap Index Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemaps/solutions-1.xml</loc>
    <lastmod>2026-03-30</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemaps/solutions-2.xml</loc>
    <lastmod>2026-03-30</lastmod>
  </sitemap>
</sitemapindex>
```

## Generating Sitemaps Programmatically

### Using Node.js

```javascript
const { SitemapStream, streamToPromise } = require('sitemap');
const { createWriteStream } = require('fs');

const links = pages.map(page => ({
  url: `/solutions/${page.slug}`,
  lastmod: page.updatedAt,
  changefreq: 'monthly',
  priority: 0.8
}));

const stream = new SitemapStream({ hostname: 'https://example.com' });
links.forEach(link => stream.write(link));
stream.end();
const data = await streamToPromise(stream);
fs.writeFileSync('public/sitemap-solutions.xml', data.toString());
```

Install: `npm install sitemap`

### Using Python

```python
from xml.etree.ElementTree import Element, SubElement, tostring

urlset = Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
for page in pages:
    url_el = SubElement(urlset, 'url')
    SubElement(url_el, 'loc').text = f'https://example.com/solutions/{page["slug"]}'
    SubElement(url_el, 'lastmod').text = page['updated_at']
    SubElement(url_el, 'changefreq').text = 'monthly'
    SubElement(url_el, 'priority').text = '0.8'

with open('public/sitemap-solutions.xml', 'wb') as f:
    f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write(tostring(urlset, encoding='unicode').encode())
```

## Submit to Google Search Console

Use the `google-search-console-api` fundamental:

```
PUT https://searchconsole.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps/https%3A%2F%2Fexample.com%2Fsitemap-solutions.xml
Authorization: Bearer {access_token}
```

Also add the sitemap reference to `robots.txt`:
```
Sitemap: https://example.com/sitemap-solutions.xml
```

## Webflow-Specific Sitemap Handling

Webflow auto-generates sitemaps for CMS collections. If using Webflow CMS for programmatic pages, the sitemap updates automatically when new CMS items are published. Verify at `https://your-domain.com/sitemap.xml`.

For custom sitemaps outside Webflow's auto-generation, host the sitemap file on your server or a CDN and reference it via DNS or a reverse proxy.

## Validation

Validate sitemaps before submitting:
- Google's Sitemap testing tool in Search Console
- `xmllint --schema https://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd sitemap.xml`
- Online: `https://www.xml-sitemaps.com/validate-xml-sitemap.html`

## Pricing

Free. Sitemaps are a web standard with no cost.
