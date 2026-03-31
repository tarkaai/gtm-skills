---
name: brand-audit-scrape
description: Programmatically crawl and analyze a website's brand presentation including messaging, visual consistency, and conversion paths
tool: Microsoft
product: Playwright
difficulty: Setup
---

# Brand Audit Scrape

Crawl a target website to extract and catalog all brand-facing elements: headlines, CTAs, value propositions, navigation structure, color palette, font usage, and conversion paths. This fundamental produces the raw data that brand audit drills consume.

## Option A: Playwright (headless browser)

### Crawl top-level pages

```javascript
const { chromium } = require('playwright');

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

// Crawl the sitemap or top-level nav
await page.goto('https://target-site.com/sitemap.xml');
const sitemapXml = await page.content();
// Parse sitemap for URLs, filter to marketing pages (exclude /docs, /blog, /api)

for (const url of marketingUrls) {
  await page.goto(url);

  const audit = {
    url,
    title: await page.title(),
    metaDescription: await page.$eval('meta[name="description"]', el => el.content).catch(() => null),
    h1: await page.$$eval('h1', els => els.map(e => e.textContent.trim())),
    h2s: await page.$$eval('h2', els => els.map(e => e.textContent.trim())),
    ctas: await page.$$eval('a[href], button', els => els.map(e => ({
      text: e.textContent.trim(),
      href: e.href || null,
      tag: e.tagName
    }))),
    images: await page.$$eval('img', els => els.map(e => ({
      src: e.src,
      alt: e.alt
    }))),
    bodyText: await page.$eval('body', el => el.innerText.substring(0, 5000)),
    computedStyles: await page.evaluate(() => {
      const body = document.body;
      const styles = getComputedStyle(body);
      return {
        fontFamily: styles.fontFamily,
        color: styles.color,
        backgroundColor: styles.backgroundColor
      };
    })
  };

  // Store audit per page
}

await browser.close();
```

### Extract color palette

```javascript
await page.evaluate(() => {
  const allElements = document.querySelectorAll('*');
  const colors = new Set();
  allElements.forEach(el => {
    const style = getComputedStyle(el);
    colors.add(style.color);
    colors.add(style.backgroundColor);
  });
  return [...colors].filter(c => c !== 'rgba(0, 0, 0, 0)');
});
```

### Screenshot key pages

```javascript
await page.screenshot({ path: `audit/${slug}-full.png`, fullPage: true });
await page.screenshot({ path: `audit/${slug}-above-fold.png`, clip: { x: 0, y: 0, width: 1440, height: 900 } });
```

## Option B: Screaming Frog SEO Spider (CLI)

```bash
# Crawl up to 500 pages and export
/Applications/Screaming\ Frog\ SEO\ Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher \
  --crawl https://target-site.com \
  --headless \
  --output-folder ./audit-export \
  --export-tabs "Internal:All,Page Titles:All,H1:All,H2:All,Meta Description:All,Images:All"
```

Exports CSVs with all on-page elements.

## Option C: Clay Website Scraper

Use Clay's built-in website scraper for quick extraction:

1. Create a Clay table with target URLs
2. Add "Scrape Website" enrichment
3. Extract: page title, H1, meta description, body text
4. Export results as CSV or push to Attio via Clay-Attio integration

## Output

The audit scrape produces a structured JSON or CSV per page containing:
- All headlines (H1, H2, H3)
- All CTAs with destination URLs
- Meta descriptions and page titles
- Body text (first 5000 chars)
- Image sources and alt text
- Color values used
- Full-page screenshots

This data feeds into the `brand-audit-analysis` drill for competitive positioning, messaging consistency, and conversion path analysis.

## Error Handling

- `Navigation timeout`: Page took >30s to load. Increase timeout or skip.
- `Element not found`: Selector returned null. Use `.catch(() => null)` for optional elements.
- `Blocked by WAF`: Site blocks headless browsers. Add realistic user-agent header and consider using a residential proxy.
