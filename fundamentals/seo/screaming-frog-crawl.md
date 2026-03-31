---
name: screaming-frog-crawl
description: Crawl a website to discover broken links, redirect chains, missing metadata, and indexation issues
tool: Screaming Frog SEO Spider
difficulty: Config
---

# Screaming Frog SEO Spider — CLI Crawl

Run a full site crawl programmatically to discover technical SEO issues: broken links (4xx/5xx), redirect chains, duplicate titles, missing meta descriptions, orphan pages, canonical errors, and more. Screaming Frog SEO Spider has a CLI mode for headless execution.

## Setup

1. Install Screaming Frog SEO Spider: https://www.screamingfrog.co.uk/seo-spider/
2. Activate a license ($259/year) for CLI mode and crawls over 500 URLs
3. The CLI executable location:
   - macOS: `/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher`
   - Linux: `/usr/bin/screamingfrogseospider`
   - Windows: `C:\Program Files (x86)\Screaming Frog SEO Spider\ScreamingFrogSEOSpiderCli.exe`

## Core Operations

### Run a full site crawl

```bash
"/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher" \
  --crawl "https://example.com" \
  --headless \
  --save-crawl \
  --output-folder "/tmp/seo-crawl-output" \
  --export-tabs "Internal:All,Response Codes:Client Error (4xx),Response Codes:Server Error (5xx),Page Titles:All,Meta Description:All,H1:All,Canonicals:All,Directives:All" \
  --bulk-export "All Inlinks,All Outlinks,Redirect Chains"
```

Key flags:
- `--headless`: Run without GUI (required for agent execution)
- `--save-crawl`: Save the full crawl database to the output folder
- `--output-folder`: Where to write CSV exports
- `--export-tabs`: Which data tabs to export as CSV
- `--bulk-export`: Additional reports to generate
- `--config "/path/to/config.seospiderconfig"`: Load a saved crawl configuration

### Crawl with custom configuration

```bash
# Create a config file that limits crawl scope and speed
"/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher" \
  --crawl "https://example.com" \
  --headless \
  --output-folder "/tmp/seo-crawl-output" \
  --config "/path/to/seo-audit.seospiderconfig" \
  --export-tabs "Internal:All"
```

Config file settings to tune (create via GUI, save, then use in CLI):
- Max crawl depth: 5-10 for most sites
- Crawl speed: 2-5 URLs/second to avoid overloading the server
- Respect robots.txt: enabled by default
- Follow internal nofollow: disabled (to match Googlebot behavior)
- Store HTML/rendered page: enabled (for content analysis)

### Parse the CSV output

After crawl completes, the output folder contains CSV files. Key files:

- `internal_all.csv`: Every internal URL with status code, title, description, word count, canonical, indexability
- `client_error_4xx.csv`: All 404 and other 4xx responses
- `server_error_5xx.csv`: All 500-class errors
- `redirect_chains.csv`: URLs with multiple redirects (301 → 301 → 200)
- `all_inlinks.csv`: Every internal link (source URL, destination URL, anchor text)

Key columns in `internal_all.csv`:
- `Address`: The URL
- `Status Code`: HTTP response code
- `Indexability`: "Indexable" or "Non-Indexable"
- `Indexability Status`: Reason for non-indexability (noindex, canonicalized, etc.)
- `Title 1`: Page title
- `Title 1 Length`: Character count
- `Meta Description 1`: Meta description text
- `Meta Description 1 Length`: Character count
- `H1-1`: First H1 tag
- `Canonical Link Element 1`: Canonical URL
- `Word Count`: Content word count

### Identify issues by category

Parse the CSV and flag:

1. **Broken internal links**: rows in `client_error_4xx.csv` that have inlinks from live pages
2. **Redirect chains**: entries in `redirect_chains.csv` with 2+ hops
3. **Missing titles**: rows in `internal_all.csv` where `Title 1` is empty and `Indexability` = "Indexable"
4. **Duplicate titles**: group by `Title 1`, flag groups with >1 URL
5. **Missing meta descriptions**: empty `Meta Description 1` on indexable pages
6. **Missing H1**: empty `H1-1` on indexable pages
7. **Canonical issues**: `Canonical Link Element 1` differs from `Address` unexpectedly
8. **Non-indexable pages that should be indexed**: `Indexability` = "Non-Indexable" on important pages
9. **Thin content**: `Word Count` < 300 on pages intended to rank

## Rate Limits

- Crawl speed is configurable (default: 5 URLs/second)
- Set to 1-2 URLs/second for smaller servers to avoid triggering WAF or rate limiting
- Large sites (10,000+ pages) may take 30-60 minutes to crawl

## Error Handling

- Crawl hangs: Set `--max-crawl-time 3600` (seconds) to auto-terminate
- Memory errors on large sites: Increase Java heap with `--max-heap-size 4g`
- Robot exclusion: If pages are blocked by robots.txt, the crawl will skip them. Check robots.txt first.
- Connection refused: The target server may be blocking the crawler User-Agent. Configure a custom UA in the config file.

## Pricing

- Free version: Crawl up to 500 URLs (no CLI mode)
- Paid license: $259/year — unlimited URLs, CLI mode, JavaScript rendering
- Pricing page: https://www.screamingfrog.co.uk/seo-spider/pricing/

## Alternatives

- **Sitebulb** ($13.50/mo+): Desktop crawler with automated hints — https://sitebulb.com/
- **Lumar (DeepCrawl) API** (custom pricing): Cloud-based crawling with API access — https://lumar.io/
- **Ahrefs Site Audit** (included in $99/mo+ plans): Cloud crawl with issue detection — https://ahrefs.com/site-audit
- **Semrush Site Audit** (included in $129.95/mo+ plans): Cloud crawl with scored issues — https://www.semrush.com/siteaudit/
- **Oncrawl API** ($69/mo+): Cloud crawling with log file analysis — https://www.oncrawl.com/
