---
name: ai-infographic-generation
description: Use an LLM to generate structured infographic content and render it as a shareable image via code
tool: Anthropic
product: Claude API
difficulty: Config
---

# AI Infographic Generation

Generate data-driven infographics programmatically by combining LLM-generated content structure with code-based rendering. The agent produces the data narrative, layout specification, and final image without manual design tools.

## Prerequisites

- Anthropic API key (or OpenAI API key)
- Node.js environment with `@vercel/og` or `satori` + `resvg-js` for image rendering (or Python with `matplotlib` / `plotly` for chart-based infographics)
- Data source: CSV, API response, or structured dataset to visualize
- Brand style guide: hex colors, font family, logo SVG

## Core Workflow

### 1. Extract the data story via LLM

Send your raw data to Claude and request a structured infographic specification:

```
POST https://api.anthropic.com/v1/messages
x-api-key: {ANTHROPIC_API_KEY}
anthropic-version: 2023-06-01
Content-Type: application/json

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2048,
  "system": "You are a data storytelling expert. Given raw data, you produce a structured JSON specification for an infographic. The spec must include: title, subtitle, 3-5 data points with labels and values, a narrative callout sentence, and a CTA. Every element must be factual and derived from the provided data. Do not fabricate statistics.",
  "messages": [
    {
      "role": "user",
      "content": "Create an infographic specification from this data:\n\n{RAW_DATA}\n\nTarget audience: {ICP_DESCRIPTION}\nTopic angle: {TOPIC_ANGLE}\nBrand colors: {HEX_COLORS}\n\nReturn JSON with this structure:\n{\n  \"title\": \"string (max 8 words)\",\n  \"subtitle\": \"string (max 15 words)\",\n  \"data_points\": [{\"label\": \"string\", \"value\": \"string\", \"icon_hint\": \"string\"}],\n  \"callout\": \"string (one punchy sentence summarizing the key insight)\",\n  \"source_attribution\": \"string (where the data came from)\",\n  \"cta\": \"string (what the viewer should do next)\"\n}"
    }
  ]
}
```

### 2. Render the infographic as an image

**Option A: Satori + resvg (Node.js, serverless-compatible)**

```javascript
const satori = require('satori');
const { Resvg } = require('@resvg/resvg-js');
const fs = require('fs');

async function renderInfographic(spec, brandColors, fontData) {
  const svg = await satori(
    {
      type: 'div',
      props: {
        style: {
          display: 'flex', flexDirection: 'column', width: '100%', height: '100%',
          background: `linear-gradient(180deg, ${brandColors.primary} 0%, ${brandColors.secondary} 100%)`,
          padding: '60px', fontFamily: 'Inter', color: '#ffffff',
        },
        children: [
          { type: 'div', props: { style: { fontSize: 48, fontWeight: 800 }, children: spec.title } },
          { type: 'div', props: { style: { fontSize: 24, opacity: 0.8, marginTop: 8 }, children: spec.subtitle } },
          ...spec.data_points.map(dp => ({
            type: 'div', props: {
              style: { display: 'flex', alignItems: 'baseline', gap: 16, marginTop: 24 },
              children: [
                { type: 'div', props: { style: { fontSize: 56, fontWeight: 800 }, children: dp.value } },
                { type: 'div', props: { style: { fontSize: 22 }, children: dp.label } },
              ]
            }
          })),
          { type: 'div', props: { style: { marginTop: 'auto', fontSize: 18, opacity: 0.6 }, children: spec.source_attribution } },
        ]
      }
    },
    { width: 1200, height: 1200, fonts: [{ name: 'Inter', data: fontData, weight: 400 }] }
  );
  const resvg = new Resvg(svg);
  const pngBuffer = resvg.render().asPng();
  fs.writeFileSync('infographic.png', pngBuffer);
  return 'infographic.png';
}
```

**Option B: Matplotlib (Python, chart-heavy infographics)**

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def render_chart_infographic(spec, output_path='infographic.png'):
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    labels = [dp['label'] for dp in spec['data_points']]
    values = [float(dp['value'].replace('%','').replace('$','').replace(',','')) for dp in spec['data_points']]
    bars = ax.barh(labels, values, color='#4ecdc4', height=0.5)
    ax.set_title(spec['title'], fontsize=28, color='white', fontweight='bold', pad=20)
    ax.tick_params(colors='white', labelsize=14)
    ax.spines[:].set_visible(False)
    fig.text(0.5, 0.02, spec['source_attribution'], ha='center', fontsize=10, color='#888888')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    return output_path
```

**Option C: Plotly (interactive + static export)**

```python
import plotly.graph_objects as go

def render_plotly_infographic(spec, output_path='infographic.png'):
    labels = [dp['label'] for dp in spec['data_points']]
    values = [float(dp['value'].replace('%','').replace('$','').replace(',','')) for dp in spec['data_points']]
    fig = go.Figure(data=[go.Bar(x=values, y=labels, orientation='h', marker_color='#4ecdc4')])
    fig.update_layout(
        title=dict(text=spec['title'], font=dict(size=28, color='white')),
        paper_bgcolor='#1a1a2e', plot_bgcolor='#1a1a2e',
        font=dict(color='white', size=14),
        margin=dict(l=20, r=20, t=80, b=40),
        width=1200, height=1200
    )
    fig.write_image(output_path, scale=2)
    return output_path
```

### 3. Generate via Canva API (alternative for template-based design)

```
POST https://api.canva.com/rest/v1/designs
Authorization: Bearer {CANVA_API_TOKEN}
Content-Type: application/json

{
  "design_type": { "type": "preset", "name": "InstagramPost" },
  "title": "{spec.title}",
  "asset_upload": false
}
```

Then update text elements and export:
```
POST https://api.canva.com/rest/v1/exports
Authorization: Bearer {CANVA_API_TOKEN}

{
  "design_id": "{design_id}",
  "format": { "type": "png", "quality": "high", "size": "medium" }
}
```

Canva API pricing: Canva for Teams ($10/user/mo) includes API access.

### 4. Generate via Figma API (alternative)

```
GET https://api.figma.com/v1/images/{file_key}?ids={node_id}&format=png&scale=2
X-Figma-Token: {FIGMA_TOKEN}
```

Requires a pre-built Figma template with named text layers. Use the Figma REST API to update text node content, then export as PNG. Figma Professional plan ($15/editor/mo) required for API access.

## Image Dimensions by Platform

| Platform | Format | Dimensions |
|----------|--------|------------|
| LinkedIn feed | Single image | 1200 x 1200 px |
| LinkedIn carousel | Multi-page PDF | 1080 x 1350 px per slide |
| Twitter/X | Single image | 1200 x 675 px |
| Instagram | Square | 1080 x 1080 px |
| Blog embed | Landscape | 1200 x 800 px |
| Pinterest | Tall | 1000 x 1500 px |

## Error Handling

- **LLM returns non-JSON**: Retry with explicit instruction "Return ONLY valid JSON, no markdown fencing."
- **Rendering fails on special characters**: Sanitize `spec.title` and all text fields before passing to renderer.
- **Font not found**: Bundle font files locally; do not rely on system fonts in serverless environments.
- **Image too large for upload**: Compress with `sharp` (Node.js) or `Pillow` (Python) to keep under 5MB for social platform limits.

## Cost Estimates

- Claude Sonnet for spec generation: ~$0.01 per infographic
- Satori rendering: free (open source)
- Matplotlib/Plotly rendering: free (open source)
- Canva API: $10/user/mo (Canva for Teams)
- Figma API: $15/editor/mo (Professional)

## Alternatives

- **Piktochart API**: Template-based infographic generation ($14/mo+)
- **Venngage API**: Business infographic templates ($19/mo+)
- **Visme API**: Data visualization + infographic ($29/mo+)
- **Infogram API**: Interactive infographic embed ($19/mo+)
- **Remove.bg API + custom compositing**: Layer product screenshots into branded templates
