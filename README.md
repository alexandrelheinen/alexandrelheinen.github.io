# Alexandre Loeblein Heinen - Personal Website

This is a minimalist personal website built with Jekyll and GitHub Pages, serving as a landing page for professional work, technical articles, and CV distribution. The architecture leverages Jekyll's templating system to maintain consistent design across pages while allowing flexible content creation through Markdown and HTML.

> But do not overlook it too much! It is obviously very vibe coded.

## Directory Structure

```
alexandrelheinen.github.io/
├── _layouts/              # Page templates
│   └── default.html       # Main layout (HTML structure)
├── _includes/             # Reusable components
│   ├── navigation.html    # Social links navigation
│   ├── figure.html        # Figure embedding
│   ├── youtube.html       # YouTube video embedding
│   └── youtube_short.html # YouTube shorts embedding
├── assets/
│   └── css/
│       └── style.css      # Global styles (shared across all pages)
├── pages/                 # Additional pages
│   └── cv.md             # CV page
├── articles/              # Technical articles
│   └── 3d_dubins.md      # Example article
├── files/                 # Downloadable files
│   ├── cven.pdf          # CV in English
│   ├── cvfr.pdf          # CV in French
│   └── images/           # Article images
├── index.md               # Home page
└── _config.yml            # Jekyll configuration
```

The structure separates concerns: layouts define HTML structure, includes provide reusable components, assets handle styling, and content lives in dedicated directories. This separation allows easy content updates without touching the design system.

## Template System

The site uses Jekyll's layout and include system. Pages are written in Markdown with YAML front matter specifying the layout:

```yaml
---
layout: default
title: Your Page Title
description: Optional description
---
```

The `default` layout wraps content with consistent HTML structure, navigation, and styling. Reusable components in `_includes/` can be embedded using Liquid syntax:

```liquid
{% include navigation.html %}
{% include figure.html src="path/to/image.png" caption="Figure caption" %}
{% include youtube.html id="VIDEO_ID" %}
```

This approach keeps content clean while maintaining design consistency across all pages.

## Local Development

To test the site locally on Linux:

1. **Install Jekyll**:
   ```bash
   sudo apt install jekyll
   ```

2. **Install required plugins**:
   ```bash
   sudo gem install jekyll-feed jekyll-relative-links
   ```

3. **Start the development server**:
   ```bash
   jekyll serve
   ```

4. **Access the site** at `http://localhost:4000`

The server watches for file changes and automatically rebuilds.

## Known Issues

### Math Rendering with MathJax

When writing mathematical equations in articles:

- **Inline math**: Use `$$...$$` on the same line as surrounding text
  - ✅ Correct: `This is $$x^2 + y^2 = r^2$$ inline math.`

- **Display math**: Use `$$...$$` on separate lines for block equations
  ```
  Text before.
  
  $$
  x^2 + y^2 = r^2
  $$
  
  Text after.
  ```

With Kramdown's `math_engine: mathjax` setting, both inline and display math use `$$` delimiters - the positioning (same line vs separate lines) determines the rendering mode.

## License

MIT License - See [LICENSE](LICENSE) file for details.
