---
name: infographic-creation-pipeline
description: End-to-end workflow for sourcing data, generating infographic content via LLM, rendering images, and exporting platform-ready assets
category: Content
tools:
  - Anthropic Claude API
  - Plotly
  - Sharp
  - Canva
  - Figma
fundamentals:
  - ai-infographic-generation
  - data-visualization-rendering
  - social-image-sizing
---

# Infographic Creation Pipeline

This drill takes a topic and data source as input and produces a set of platform-ready infographic images as output. It chains data extraction, LLM-driven narrative design, programmatic rendering, and multi-platform export into a single repeatable workflow.

## Input

- Topic aligned with an ICP pain point or industry trend
- Data source: public dataset URL, API endpoint, CSV file, or research report excerpt
- Brand style: hex colors, font family, logo file path
- Target platforms: list of platforms to export for (LinkedIn, Twitter/X, blog, etc.)

## Steps

### 1. Source and validate data

Identify a credible data source for the infographic topic. Acceptable sources:
- Government or industry reports (Bureau of Labor Statistics, Gartner, McKinsey)
- Your own product analytics (PostHog exports, CRM reports)
- Public APIs (Statista, World Bank Open Data, GitHub trending)
- Survey data you have collected

Validate the data is current (within 12 months unless historical trends), from a named source, and not behind a paywall that prevents attribution. Extract the raw data into structured JSON or CSV format.

### 2. Generate the infographic specification

Run the `ai-infographic-generation` fundamental. Send the raw data and topic to the LLM with instructions to produce a structured JSON specification. The spec defines:
- Title (max 8 words, attention-grabbing)
- Subtitle (context sentence)
- 3-5 data points with labels, values, and icon hints
- Callout sentence (the single most surprising or important insight)
- Source attribution line
- CTA (what the viewer should do)

Review the spec before rendering. Verify: all statistics match the source data, the narrative angle is relevant to your ICP, and the title creates curiosity.

### 3. Render the data visualization component

If the infographic includes charts or graphs, run the `data-visualization-rendering` fundamental to generate the chart image. Choose the chart type based on the data:
- **Comparisons** (this vs. that): horizontal bar chart
- **Trends over time**: line chart
- **Composition/share**: donut chart
- **Distribution**: histogram
- **Correlation**: scatter plot

Export the chart as a high-resolution PNG (2400px minimum on longest edge) for compositing into the final infographic.

### 4. Compose the full infographic

Combine the LLM-generated text elements with the data visualization into a single image. Using the `ai-infographic-generation` fundamental's rendering workflow (Satori, Matplotlib, or Canva/Figma API):

- Place the title and subtitle at top
- Arrange data points with visual hierarchy (largest/most important first)
- Embed the chart visualization in the center section
- Add the callout sentence as a highlighted pull-quote
- Place source attribution and CTA at bottom
- Include your logo/brand mark

### 5. Export for all target platforms

Run the `social-image-sizing` fundamental to produce platform-optimized versions:
- LinkedIn feed (1200x1200)
- Twitter/X (1200x675)
- Blog embed (1200x800)
- Pinterest (1000x1500) if applicable
- LinkedIn carousel (1080x1350 per slide) if the infographic has 4+ data points

Each export must meet the target platform's file size limits. Compress if needed.

### 6. Generate companion copy

For each platform export, generate a companion post or caption. The copy should:
- Hook with the most surprising data point from the infographic
- Reference that the full visualization is in the image (drives image clicks)
- Include a question or opinion to encourage comments
- Add 2-3 relevant hashtags for discoverability (LinkedIn only)

Use the `ai-content-ghostwriting` fundamental if a founder voice profile exists. Otherwise, generate directly via LLM with the infographic spec as context.

### 7. Quality check

Before publishing, verify:
- [ ] All statistics in the image match the source data exactly
- [ ] Source attribution is visible and accurate
- [ ] Text is readable at mobile screen size (test by viewing at 375px width)
- [ ] Brand colors and logo are correctly applied
- [ ] No typos or truncated text in any platform export
- [ ] File sizes are within platform limits

## Output

- 1 high-resolution master infographic (PNG, 2400px+)
- Platform-specific exports (LinkedIn, Twitter, blog, Pinterest as specified)
- Companion post copy for each platform
- Infographic spec JSON (for future repurposing or A/B testing variants)

## Triggers

Run this drill weekly (for a steady cadence) or on-demand when new data becomes available. At Smoke level: 1-2 infographics total. At Baseline: 1 per week. At Scalable: 2-3 per week via batched generation.
