---
name: social-image-sizing
description: Resize and optimize images for each social platform's dimensions and file size limits
tool: Sharp
difficulty: Setup
---

# Social Image Sizing

Programmatically resize, crop, and optimize infographic or visual content images to meet each social platform's required dimensions, aspect ratios, and file size limits. Produces platform-ready exports from a single source image.

## Prerequisites

- Node.js with `sharp` package, or Python with `Pillow`
- Source image at high resolution (minimum 2400px on longest edge recommended)
- Target platform list (LinkedIn, Twitter/X, Instagram, Pinterest, blog)

## Platform Specifications

| Platform | Use Case | Dimensions (px) | Aspect Ratio | Max File Size | Format |
|----------|----------|-----------------|--------------|---------------|--------|
| LinkedIn | Feed image | 1200 x 1200 | 1:1 | 10 MB | PNG/JPEG |
| LinkedIn | Carousel slide | 1080 x 1350 | 4:5 | 100 MB (PDF) | PDF |
| LinkedIn | Link preview | 1200 x 627 | 1.91:1 | 5 MB | PNG/JPEG |
| Twitter/X | In-stream | 1200 x 675 | 16:9 | 5 MB | PNG/JPEG |
| Twitter/X | Card image | 800 x 418 | 1.91:1 | 3 MB | PNG/JPEG |
| Instagram | Feed square | 1080 x 1080 | 1:1 | 8 MB | JPEG |
| Instagram | Feed portrait | 1080 x 1350 | 4:5 | 8 MB | JPEG |
| Pinterest | Standard pin | 1000 x 1500 | 2:3 | 20 MB | PNG/JPEG |
| Blog/embed | Content width | 1200 x 800 | 3:2 | - | PNG/WebP |
| Email | Inline | 600 x 400 | 3:2 | 1 MB | JPEG |

## Implementation (Node.js with Sharp)

```javascript
const sharp = require('sharp');
const path = require('path');

const PLATFORMS = {
  linkedin_feed: { width: 1200, height: 1200, format: 'png' },
  linkedin_carousel: { width: 1080, height: 1350, format: 'png' },
  twitter: { width: 1200, height: 675, format: 'png' },
  instagram_square: { width: 1080, height: 1080, format: 'jpeg', quality: 90 },
  pinterest: { width: 1000, height: 1500, format: 'png' },
  blog: { width: 1200, height: 800, format: 'webp', quality: 85 },
  email: { width: 600, height: 400, format: 'jpeg', quality: 80 },
};

async function resizeForPlatforms(sourcePath, outputDir, platforms = Object.keys(PLATFORMS)) {
  const results = {};
  for (const platform of platforms) {
    const spec = PLATFORMS[platform];
    const outputPath = path.join(outputDir, `${path.basename(sourcePath, path.extname(sourcePath))}_${platform}.${spec.format}`);
    await sharp(sourcePath)
      .resize(spec.width, spec.height, { fit: 'cover', position: 'center' })
      .toFormat(spec.format, { quality: spec.quality || 100 })
      .toFile(outputPath);
    results[platform] = outputPath;
  }
  return results;
}
```

## Implementation (Python with Pillow)

```python
from PIL import Image
import os

PLATFORMS = {
    'linkedin_feed': {'width': 1200, 'height': 1200, 'format': 'PNG'},
    'linkedin_carousel': {'width': 1080, 'height': 1350, 'format': 'PNG'},
    'twitter': {'width': 1200, 'height': 675, 'format': 'PNG'},
    'instagram_square': {'width': 1080, 'height': 1080, 'format': 'JPEG', 'quality': 90},
    'pinterest': {'width': 1000, 'height': 1500, 'format': 'PNG'},
    'blog': {'width': 1200, 'height': 800, 'format': 'WEBP', 'quality': 85},
    'email': {'width': 600, 'height': 400, 'format': 'JPEG', 'quality': 80},
}

def resize_for_platforms(source_path, output_dir, platforms=None):
    platforms = platforms or list(PLATFORMS.keys())
    img = Image.open(source_path)
    results = {}
    for platform in platforms:
        spec = PLATFORMS[platform]
        resized = img.resize((spec['width'], spec['height']), Image.LANCZOS)
        ext = spec['format'].lower()
        if ext == 'jpeg': ext = 'jpg'
        output_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(source_path))[0]}_{platform}.{ext}")
        save_kwargs = {}
        if 'quality' in spec:
            save_kwargs['quality'] = spec['quality']
        resized.save(output_path, spec['format'], **save_kwargs)
        results[platform] = output_path
    return results
```

## LinkedIn Carousel PDF Generation

For multi-slide infographics (carousels), combine individual slide PNGs into a single PDF:

```javascript
const PDFDocument = require('pdfkit');
const fs = require('fs');

function createCarouselPdf(slidePaths, outputPath) {
  const doc = new PDFDocument({ size: [1080, 1350], margin: 0 });
  doc.pipe(fs.createWriteStream(outputPath));
  slidePaths.forEach((slidePath, i) => {
    if (i > 0) doc.addPage({ size: [1080, 1350], margin: 0 });
    doc.image(slidePath, 0, 0, { width: 1080, height: 1350 });
  });
  doc.end();
  return outputPath;
}
```

## File Size Optimization

If the exported image exceeds platform limits:

```javascript
// Progressively reduce quality until under target size
async function optimizeFileSize(inputPath, maxBytes, format = 'png') {
  let quality = 100;
  let buffer;
  do {
    buffer = await sharp(inputPath).toFormat(format, { quality }).toBuffer();
    quality -= 5;
  } while (buffer.length > maxBytes && quality > 20);
  return buffer;
}
```

## Error Handling

- **Source image too small**: Warn if source is smaller than target dimensions. Upscaling produces blurry results. Regenerate at higher resolution.
- **Transparent backgrounds**: Some platforms (Instagram, email) do not support transparency. Flatten transparent PNGs onto a white or branded background before converting to JPEG.
- **Color profile issues**: Strip ICC profiles for web use: `sharp(input).toColorspace('srgb')`.

## Cost

- Sharp: free (open source, MIT license)
- Pillow: free (open source)
- No API costs; runs locally or in CI/CD
