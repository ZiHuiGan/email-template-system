# Email Template System v1.0

**A reusable, modular HTML email template system with presets, components, and automatic validation.**

## Quick Start

### Installation

```bash
# Add to your project
pip install git+https://github.com/yourusername/email-template-system.git
```

### Usage

```python
from email_template_system import EmailPreset, EmailTemplate

# Load preset
preset = EmailPreset.load("evening-debrief")

# Create template
template = EmailTemplate(preset)

# Render email
html = template.render(
    content='<div class="section">...</div>',
    email_title="Evening Debrief 2026-04-11",
    header_meta="Friday, April 11"
)

# Validate
is_valid, issues = template.validate(html)
print(html)  # Send via SMTP
```

## Features

✅ **3 Professional Presets**
- Evening Debrief (scannable, news-focused)
- Weekly Report (strategic, analysis-heavy)
- Morning Brief (clean, fast-paced)

✅ **Responsive by Default**
- `clamp()` for all sizes (no media queries needed)
- Scales perfectly from mobile (320px) to desktop (1280px)

✅ **Dark Mode Support**
- Automatic dark mode with preset-specific colors
- Respects `prefers-color-scheme: dark`

✅ **Accessibility**
- WCAG 2.1 AA compliant
- Color contrast validation
- Alt text requirements

✅ **Reusable Components**
- Article cards
- Impact badges
- 3-column grids (Tier 1 → Tier 2 → Tier 3)
- Code snippets
- Blockquotes

✅ **Automatic Validation**
- HTML structure checking
- Accessibility verification
- Content limit enforcement
- Responsive sizing validation

✅ **Zero Dependencies**
- Pure HTML/CSS/Python
- No npm, no build tools
- Single 50KB template file

## Presets at a Glance

| Preset | Best For | Max Content | Colors |
|--------|----------|-------------|--------|
| **Evening Debrief** | Daily news summaries | 5 sections, 2 imgs | Blue + Red |
| **Weekly Report** | Strategic analysis | 6 sections, 3 imgs | Brown + Gold |
| **Morning Brief** | Quick updates | 4 sections, 1 img | Blue + Green |

## File Structure

```
email-template-system/
├── presets/                 # Email style presets (JSON)
│   ├── evening-debrief.json
│   ├── weekly-report.json
│   ├── morning-brief.json
│   └── _schema.json
├── templates/               # HTML templates & components
│   ├── base.html
│   └── components/
│       ├── article-card.html
│       ├── impact-badge.html
│       ├── grid-3col.html
│       ├── code-snippet.html
│       └── quote-section.html
├── validators/              # Quality checkers
│   ├── html_validator.py
│   ├── wcag_checker.py
│   └── constraints_checker.py
├── tests/                   # Automated tests
│   ├── test_presets.py
│   ├── test_html_validity.py
│   └── test_constraints.py
├── email_template_system.py # Main module
├── SKILL.md                 # Claude skill definition
├── README.md                # This file
├── setup.py
└── requirements.txt
```

## Key Concepts

### 1. Presets

Presets bundle colors, fonts, and constraints:

```json
{
  "name": "Evening Debrief",
  "colors": {
    "bg_primary": "#f8f9fa",
    "text_primary": "#1a1a1a",
    "accent": "#2c5aa0"
  },
  "constraints": {
    "max_sections": 5,
    "max_images": 2,
    "max_cta_buttons": 1
  }
}
```

### 2. CSS Variables

All styling uses CSS variables:

```css
:root {
    --accent: #2c5aa0;
    --text-primary: #1a1a1a;
    --headline-size: clamp(24px, 5vw, 28px);
}

h1 { color: var(--accent); font-size: var(--headline-size); }
```

### 3. Responsive Sizing

No breakpoints needed. Everything uses `clamp()`:

```css
/* Font scales from 24px to 28px based on viewport */
--headline-size: clamp(24px, 5vw, 28px);

/* Padding scales from 20px to 32px */
--section-padding: clamp(20px, 4vw, 32px);
```

### 4. Components

Reusable HTML snippets for common email elements:

- Article cards with impact badges
- 3-column grids showing data flow
- Code snippets with syntax highlighting
- Blockquotes with attribution

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_presets.py -v

# Check validation
python -c "
from email_template_system import EmailTemplate, EmailPreset
preset = EmailPreset.load('evening-debrief')
template = EmailTemplate(preset)
html = template.render('<div>test</div>')
is_valid, issues = template.validate(html)
print('Valid!' if is_valid else f'Issues: {issues}')
"
```

## Integration with news-intelligence

In `news-intelligence/emailer.py`:

```python
from email_template_system import EmailPreset, EmailTemplate

def generate_email(articles, preset_name, date):
    # Load preset
    preset = EmailPreset.load(preset_name)
    
    # Create template
    template = EmailTemplate(preset)
    
    # Claude generates content
    content = claude.generate(f"""
        Generate email HTML sections using preset: {preset_name}
        
        Constraints:
        - Max sections: {preset.constraints['max_sections']}
        - Max images: {preset.constraints['max_images']}
        - Max CTA buttons: {preset.constraints['max_cta_buttons']}
        
        Available components: [list]
        
        Articles: {articles}
    """)
    
    # Render final HTML
    html = template.render(
        content=content,
        email_title=f"{preset_name} {date}",
        header_meta=date
    )
    
    # Validate
    is_valid, issues = template.validate(html, verbose=True)
    
    return html
```

## Requirements

- Python 3.7+
- No external dependencies (validators are pure Python)

## Contributing

To add a new preset:

1. Create `presets/my-preset.json` with required fields
2. Update `SKILL.md` with preset description
3. Add test in `tests/test_presets.py`
4. Run tests: `pytest tests/test_presets.py`

## Version History

- **v1.0.0** (Apr 2026) — Initial release with 3 presets
- **v1.1.0** (Jun 2026) — Add font and color libraries
- **v2.0.0** (Jan 2027) — API for custom presets

## FAQ

**Q: Do I need to learn a new language?**  
A: No. The system generates standard HTML. You can edit templates with any HTML editor.

**Q: Can I add my own preset?**  
A: Yes! Create a JSON file in `presets/` following `_schema.json`.

**Q: How does dark mode work?**  
A: Automatically! Each preset defines dark mode colors. Email clients that support `prefers-color-scheme: dark` will use them.

**Q: What email clients does this support?**  
A: All modern clients (Gmail, Outlook, Apple Mail, etc.). Uses only widely-supported HTML/CSS.

**Q: Can I customize the colors?**  
A: Yes! Either modify the preset JSON, or create a new preset.

## License

MIT License — see LICENSE file for details

## Support

- 📖 Read `SKILL.md` for Claude integration
- 🧪 Check `tests/` for examples
- 📝 See `presets/` for preset structure
- 🤖 Use `email_template_system.py` for API reference

---

**Made with ❤️ for clean, accessible HTML emails**
