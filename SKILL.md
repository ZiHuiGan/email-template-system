---
name: email-template-system
description: Reusable HTML email template system with presets, components, and validation. Use this to generate professional HTML emails with consistent styling.
---

# Email Template System

A modular, reusable system for generating professional HTML emails with preset styles, templates, components, and automatic quality checks.

## Purpose

This skill provides:
- **3 Email Presets** (Evening Debrief, Weekly Report, Morning Brief)
- **Responsive HTML Templates** with CSS variable system
- **Reusable Components** (article cards, impact badges, grids, code blocks, quotes)
- **Automatic Validators** (HTML structure, WCAG accessibility, constraints)
- **Zero Dependencies** on npm/build tools (pure HTML/CSS/Python)

## Core Principles

1. **Preset-First**: Choose a preset name instead of describing colors/fonts
2. **Responsive by Default**: Uses `clamp()` for all sizing, no media queries needed
3. **Dark Mode Support**: Built-in for all presets
4. **Accessibility**: WCAG 2.1 AA compliant
5. **Constraint-Based**: Clear limits prevent overflow and ensure quality

## Using This Skill

### Option 1: Simple Rendering

For Claude to generate an email using a preset:

```
Generate a professional email using preset: evening-debrief

Articles to include:
- Title: "New AI Model Released"
  Source: TechCrunch
  Summary: OpenAI released GPT-5...
  Impact: High
```

### Option 2: With Specific Components

Reference available components in your generation:

```
Generate email using preset: weekly-report

Use components:
- Section with 3-column grid (chip→ai→app)
- Q&A section
- Watch list

Content: [articles]
```

### Option 3: Development Usage

```python
from email_template_system import EmailPreset, EmailTemplate

# Load preset
preset = EmailPreset.load("evening-debrief")

# Create template
template = EmailTemplate(preset)

# Render email
html = template.render(
    content="<div class='section'>...</div>",
    email_title="Evening Debrief 2026-04-11",
    header_meta="Friday, April 11"
)

# Validate
is_valid, issues = template.validate(html)
```

## Available Presets

### Evening Debrief
- **Vibe**: Professional, scannable, tech-focused
- **Max Content**: 5 sections, 2 images, 1 CTA button
- **Best For**: Daily news summaries
- **Colors**: News blue (#2c5aa0) + highlight red (#ff6b35)

### Weekly Report
- **Vibe**: Strategic, insightful, analysis-heavy
- **Max Content**: 6 sections, 3 images, 2 CTA buttons
- **Best For**: Weekly intelligence reports with analysis
- **Colors**: Editorial brown (#5c4033) + gold (#d4a574)

### Morning Brief
- **Vibe**: Clean, energetic, fast-paced
- **Max Content**: 4 sections, 1 image, 1 CTA button
- **Best For**: Quick morning updates
- **Colors**: Bright blue (#0d6efd) + green (#198754)

## Available Components

Located in `templates/components/`:

- **article-card.html** — Article with title, source, summary, impact badge, CTA
- **impact-badge.html** — Colored badge for impact/priority
- **grid-3col.html** — 3-column grid (Chip→AI Lab→App data flow)
- **code-snippet.html** — Code block with monospace font
- **quote-section.html** — Blockquote with attribution

## Key Features

### Responsive Sizing
All fonts, spacing, and sizes use `clamp()` to scale perfectly from mobile to desktop:
```css
--headline-size: clamp(24px, 5vw, 28px);  /* Scales 24px-28px */
--body-size: clamp(14px, 1.5vw, 16px);    /* Scales 14px-16px */
--section-padding: clamp(20px, 4vw, 32px);  /* Scales 20px-32px */
```

### CSS Variables
All colors, fonts, and spacing are CSS variables:
```css
:root {
    --accent: #2c5aa0;
    --text-primary: #1a1a1a;
    --bg-section: #ffffff;
}
```

### Dark Mode
Automatic dark mode support with preset-specific colors:
```css
@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #1a1a1a;
        --text-primary: #f0f0f0;
    }
}
```

## Constraints

Each preset enforces content limits to prevent overflow:

| Preset | Max Sections | Max Images | Max CTA |
|--------|---|---|---|
| Evening Debrief | 5 | 2 | 1 |
| Weekly Report | 6 | 3 | 2 |
| Morning Brief | 4 | 1 | 1 |

**Rule**: If content exceeds limits, split into multiple sections or emails.

## Validation

The system automatically validates:

1. **HTML Structure** — Proper tags, DOCTYPE, meta tags
2. **Accessibility** — WCAG 2.1 AA color contrast, alt text on images
3. **Constraints** — Max sections, images, and buttons per preset
4. **Responsive** — Uses `clamp()` instead of hardcoded pixels

```python
is_valid, issues = template.validate(html)
if not is_valid:
    print(f"Issues: {issues}")  # List of problems to fix
```

## Integration with news-intelligence

In `news-intelligence/emailer.py`:

```python
from email_template_system import EmailPreset, EmailTemplate

def generate_evening_debrief(articles, date):
    preset = EmailPreset.load("evening-debrief")
    template = EmailTemplate(preset)
    
    # Claude generates content using components
    content = claude.generate("""
        Generate email sections using available components.
        Presets and constraints defined above.
        Articles: {articles}
    """)
    
    html = template.render(content, email_title=f"Evening Debrief {date}")
    
    # Validate before sending
    is_valid, _ = template.validate(html)
    
    return html
```

## When to Use Each Preset

**Evening Debrief** when:
- Generating daily news summaries
- Need fast-scanning format (lists, bullets)
- Content is 3-5 article summaries
- Single CTA ("Read full story")

**Weekly Report** when:
- Generating strategic analysis emails
- Need to show Tier 1 (Chips) → Tier 2 (AI) → Tier 3 (App) flow
- Including Q&A section
- Need a "watch list" of emerging topics

**Morning Brief** when:
- Sending quick updates
- Minimal images and decorative elements
- Focus on action items
- Need clean, minimal aesthetic

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Colors don't look right" | Check that `var(--accent)` is being used, not `#2c5aa0` |
| "Email looks broken on mobile" | Verify `clamp()` is used for all sizes, not fixed `px` |
| "Dark mode not working" | Ensure `@media (prefers-color-scheme: dark)` is in CSS |
| "Validation fails" | Check that sections, images, buttons don't exceed preset limits |
| "Image is too big" | Set `max-height` on image or use smaller image file |

## File Structure

```
templates/
├── base.html                (Master template with {{ placeholders }})
└── components/
    ├── article-card.html
    ├── impact-badge.html
    ├── grid-3col.html
    ├── code-snippet.html
    └── quote-section.html

presets/
├── evening-debrief.json
├── weekly-report.json
├── morning-brief.json
└── _schema.json             (Preset validation schema)

validators/
├── html_validator.py        (HTML structure checks)
├── wcag_checker.py          (Accessibility checks)
└── constraints_checker.py   (Content limit checks)

tests/
├── test_presets.py
├── test_html_validity.py
└── test_constraints.py
```

## Version History

**v1.0.0** (Current)
- 3 presets (Evening Debrief, Weekly Report, Morning Brief)
- 5 reusable components
- 3 validators (HTML, WCAG, Constraints)
- 100% responsive with dark mode
- Zero dependencies

**v1.1.0** (Planned)
- Font pairing library (10+ serif+sans combinations)
- Color scheme library (10+ preset palettes)
- WCAG checker improvements

**v2.0.0** (Future)
- API for custom presets
- International support (multi-language dates)
- Dynamic color selection

---

**Last Updated**: April 2026
**License**: MIT
**Maintainer**: news-intelligence project
