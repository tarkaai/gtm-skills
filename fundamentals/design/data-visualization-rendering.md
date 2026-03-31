---
name: data-visualization-rendering
description: Render data charts, graphs, and statistical visualizations as static images suitable for infographic embedding
tool: Plotly
product: Charts
difficulty: Config
---

# Data Visualization Rendering

Programmatically generate publication-quality data visualizations (bar charts, line charts, pie charts, area charts, scatter plots, treemaps) as static PNG/SVG images. These visualizations become components within infographics or standalone social content.

## Prerequisites

- Data source in structured format (JSON, CSV, or API response)
- Python with `plotly` and `kaleido` (for static export), OR Node.js with `chart.js` and `chartjs-node-canvas`
- Brand color palette (hex values)

## Implementation (Python with Plotly — recommended)

### Bar chart (horizontal, for comparisons)

```python
import plotly.graph_objects as go

def render_bar_chart(labels, values, title, output_path, colors=None):
    """Render a horizontal bar chart as PNG."""
    default_colors = ['#4ecdc4', '#ff6b6b', '#45b7d1', '#96ceb4', '#ffeaa7']
    bar_colors = colors or default_colors[:len(labels)]
    fig = go.Figure(data=[go.Bar(
        x=values, y=labels, orientation='h',
        marker_color=bar_colors,
        text=[f'{v}' for v in values], textposition='outside',
        textfont=dict(size=16, color='white')
    )])
    fig.update_layout(
        title=dict(text=title, font=dict(size=28, color='white'), x=0.5),
        paper_bgcolor='#1a1a2e', plot_bgcolor='#1a1a2e',
        font=dict(color='white', size=14),
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, autorange='reversed'),
        margin=dict(l=20, r=80, t=80, b=40),
        width=1200, height=800
    )
    fig.write_image(output_path, scale=2, engine='kaleido')
    return output_path
```

### Line chart (for trends over time)

```python
def render_line_chart(x_values, y_series, series_names, title, output_path, colors=None):
    """Render a multi-series line chart as PNG."""
    default_colors = ['#4ecdc4', '#ff6b6b', '#45b7d1', '#96ceb4']
    fig = go.Figure()
    for i, (y_vals, name) in enumerate(zip(y_series, series_names)):
        color = (colors or default_colors)[i % len(colors or default_colors)]
        fig.add_trace(go.Scatter(
            x=x_values, y=y_vals, name=name, mode='lines+markers',
            line=dict(color=color, width=3),
            marker=dict(size=8, color=color)
        ))
    fig.update_layout(
        title=dict(text=title, font=dict(size=28, color='white'), x=0.5),
        paper_bgcolor='#1a1a2e', plot_bgcolor='#1a1a2e',
        font=dict(color='white', size=14),
        xaxis=dict(showgrid=True, gridcolor='#2a2a4e'),
        yaxis=dict(showgrid=True, gridcolor='#2a2a4e'),
        legend=dict(font=dict(size=14)),
        margin=dict(l=20, r=20, t=80, b=40),
        width=1200, height=800
    )
    fig.write_image(output_path, scale=2, engine='kaleido')
    return output_path
```

### Donut chart (for composition/share data)

```python
def render_donut_chart(labels, values, title, output_path, colors=None):
    """Render a donut chart as PNG."""
    default_colors = ['#4ecdc4', '#ff6b6b', '#45b7d1', '#96ceb4', '#ffeaa7', '#dfe6e9']
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.55,
        marker=dict(colors=(colors or default_colors)[:len(labels)]),
        textinfo='label+percent', textfont=dict(size=14, color='white'),
        hoverinfo='label+value+percent'
    )])
    fig.update_layout(
        title=dict(text=title, font=dict(size=28, color='white'), x=0.5),
        paper_bgcolor='#1a1a2e', plot_bgcolor='#1a1a2e',
        font=dict(color='white', size=14),
        showlegend=True, legend=dict(font=dict(size=14, color='white')),
        margin=dict(l=20, r=20, t=80, b=40),
        width=1200, height=1200
    )
    fig.write_image(output_path, scale=2, engine='kaleido')
    return output_path
```

## Implementation (Node.js with Chart.js)

```javascript
const { ChartJSNodeCanvas } = require('chartjs-node-canvas');

async function renderBarChart(labels, values, title, outputPath) {
  const chartCanvas = new ChartJSNodeCanvas({ width: 1200, height: 800, backgroundColour: '#1a1a2e' });
  const config = {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: ['#4ecdc4', '#ff6b6b', '#45b7d1', '#96ceb4', '#ffeaa7'],
        borderWidth: 0,
      }],
    },
    options: {
      indexAxis: 'y',
      plugins: {
        title: { display: true, text: title, color: '#ffffff', font: { size: 24, weight: 'bold' } },
        legend: { display: false },
      },
      scales: {
        x: { ticks: { color: '#ffffff' }, grid: { display: false } },
        y: { ticks: { color: '#ffffff', font: { size: 14 } }, grid: { display: false } },
      },
    },
  };
  const buffer = await chartCanvas.renderToBuffer(config);
  require('fs').writeFileSync(outputPath, buffer);
  return outputPath;
}
```

## Implementation (QuickChart.io — no-code API)

For agents that cannot run local rendering, use the QuickChart API:

```
GET https://quickchart.io/chart?c={URL_ENCODED_CHART_CONFIG}&width=1200&height=800&backgroundColor=%231a1a2e&format=png
```

Example chart config (URL-encode this):
```json
{
  "type": "bar",
  "data": {
    "labels": ["Category A", "Category B", "Category C"],
    "datasets": [{"data": [42, 67, 33], "backgroundColor": ["#4ecdc4","#ff6b6b","#45b7d1"]}]
  },
  "options": {
    "indexAxis": "y",
    "plugins": {"legend": {"display": false}}
  }
}
```

QuickChart free tier: 500 charts/month, 250 requests/day. Paid: $40/mo for 100K charts.

## Alternatives

| Tool | Method | Pricing |
|------|--------|---------|
| **Plotly + Kaleido** | Python, static export | Free (open source) |
| **Chart.js + chartjs-node-canvas** | Node.js, server-side | Free (open source) |
| **QuickChart.io** | REST API, no local code | Free (500/mo), $40/mo paid |
| **Datawrapper API** | Hosted chart creation | Free (10K views/mo), $599/mo teams |
| **Flourish API** | Interactive + static | Free (public), $149/mo private |
| **Google Charts Image API** | Deprecated but functional for basic charts | Free |
| **Apache ECharts + node-canvas** | Node.js, rich chart types | Free (open source) |

## Error Handling

- **Kaleido fails to install**: Use `pip install kaleido==0.2.1` (specific version). On ARM Macs, build from source or use QuickChart as fallback.
- **Font rendering issues**: Install system fonts or bundle font files. Plotly uses system fonts by default.
- **Values contain non-numeric strings**: Strip currency symbols, commas, and percent signs before plotting. Store original formatted strings for display labels.
- **Too many data points**: For >20 categories, aggregate into top 10 + "Other" to keep the chart readable.

## Cost

- Plotly + Kaleido: free (open source)
- Chart.js: free (open source)
- QuickChart: free tier for up to 500/month
