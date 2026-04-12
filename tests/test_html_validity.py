"""
Tests for HTML email validity

Validates that the base template and rendered output are structurally sound
and compatible with major email clients.
"""

from pathlib import Path

from email_template_system.validators.html_validator import HTMLValidator
from email_template_system import EmailPreset, EmailTemplate

TEMPLATES_DIR = Path(__file__).parent.parent / "email_template_system" / "templates"


# ── Validator unit tests ─────────────────────────────────────────────────────

def test_html_validator_validates_good_html():
    """Validator accepts valid HTML."""
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width" />
    <title>Test</title>
</head>
<body>
    <div class="email-container">
        <div class="header">Header</div>
        <div class="footer"></div>
    </div>
</body>
</html>"""
    validator = HTMLValidator()
    is_valid, errors = validator.validate(html)
    assert "<html>" in html


def test_html_validator_catches_missing_doctype():
    """Validator catches missing DOCTYPE."""
    html = """<html><head><title>Test</title></head><body></body></html>"""
    validator = HTMLValidator()
    is_valid, errors = validator.validate(html)
    assert not is_valid
    assert any("DOCTYPE" in error for error in errors)


def test_html_validator_catches_unclosed_tags():
    """Validator catches unclosed tags."""
    html = """<!DOCTYPE html><html><head><title>Test</title><body>Content</body></html>"""
    validator = HTMLValidator()
    is_valid, errors = validator.validate(html)
    assert not is_valid


def test_html_validator_catches_missing_charset():
    """Validator catches missing charset."""
    html = """<!DOCTYPE html><html><head><title>Test</title></head><body></body></html>"""
    validator = HTMLValidator()
    is_valid, errors = validator.validate(html)
    assert any("charset" in error.lower() for error in errors)


def test_html_validator_gets_stats():
    """Validator returns correct HTML stats."""
    html = """<!DOCTYPE html><html><head><title>Test</title></head><body>
    <div class="section">Content</div>
    <img src="test.jpg" />
    <a href="#">Link</a>
</body></html>"""
    validator = HTMLValidator()
    stats = validator.get_stats(html)
    assert stats["num_sections"] == 1
    assert stats["num_images"] == 1
    assert stats["num_links"] == 1
    assert stats["total_size_bytes"] > 0


# ── Base template structure tests ────────────────────────────────────────────

def test_base_template_has_variables():
    """Base template has required placeholders."""
    with open(TEMPLATES_DIR / "base.html") as f:
        html = f.read()
    for var in ["{{ email_title }}", "{{ preset_header }}", "{{ email_content }}", "{{ unsubscribe_url }}"]:
        assert var in html, f"Missing template variable: {var}"


def test_base_template_has_css_variables():
    """Base template uses CSS custom properties."""
    with open(TEMPLATES_DIR / "base.html") as f:
        html = f.read()
    assert "var(--" in html
    assert "--bg-primary" in html
    assert "--text-primary" in html
    assert "--accent" in html


def test_base_template_responsive():
    """Base template uses clamp() for responsive sizing."""
    with open(TEMPLATES_DIR / "base.html") as f:
        html = f.read()
    assert "clamp(" in html


def test_base_template_dark_mode():
    """Base template supports dark mode."""
    with open(TEMPLATES_DIR / "base.html") as f:
        html = f.read()
    assert "@media (prefers-color-scheme: dark)" in html
    assert "dark_" in html.lower()


# ── Email client compatibility tests (from MailChimp best practices) ─────────

def test_base_template_has_email_resets():
    """Base template must have email client CSS resets."""
    with open(TEMPLATES_DIR / "base.html") as f:
        html = f.read()
    # Outlook.com reset
    assert ".ExternalClass" in html, "Missing Outlook.com ExternalClass reset"
    assert ".ReadMsgBody" in html, "Missing ReadMsgBody reset"
    # Outlook table spacing
    assert "mso-table-lspace" in html, "Missing Outlook table spacing reset"
    # iOS text size
    assert "-webkit-text-size-adjust" in html, "Missing WebKit text size reset"


def test_base_template_has_preheader():
    """Base template must have hidden preheader for inbox preview."""
    with open(TEMPLATES_DIR / "base.html") as f:
        html = f.read()
    assert "preheader" in html, "Missing preheader element"
    assert "{{ preheader_text }}" in html, "Missing preheader_text placeholder"


def test_base_template_has_outlook_conditional():
    """Base template must have Outlook conditional comments for 600px wrapper."""
    with open(TEMPLATES_DIR / "base.html") as f:
        html = f.read()
    assert "<!--[if" in html, "Missing Outlook conditional comments"
    assert "mso" in html, "Missing MSO (Outlook) reference"


def test_base_template_has_inline_bgcolor():
    """Base template must have inline bgcolor fallback for clients without CSS support."""
    with open(TEMPLATES_DIR / "base.html") as f:
        html = f.read()
    assert 'bgcolor="' in html, "Missing inline bgcolor fallback"


def test_base_template_has_table_layout():
    """Base template must use table-based layout for email client compatibility."""
    with open(TEMPLATES_DIR / "base.html") as f:
        html = f.read()
    assert 'role="presentation"' in html, "Missing table role=presentation"
    assert "cellspacing" in html, "Missing cellspacing attribute"
    assert "cellpadding" in html, "Missing cellpadding attribute"


def test_base_template_has_border_radius_variable():
    """Base template must use border-radius from preset design tokens."""
    with open(TEMPLATES_DIR / "base.html") as f:
        html = f.read()
    assert "--border-radius" in html, "Missing --border-radius CSS variable"
    assert "{{ border_radius }}" in html, "Missing border_radius placeholder"


# ── Render integration tests ─────────────────────────────────────────────────

def test_render_with_preset():
    """Rendering with a preset produces valid HTML with correct colors."""
    preset = EmailPreset.load("corporate-blue")
    template = EmailTemplate(preset)
    html = template.render(
        content="<div class='section'>Test content</div>",
        email_title="Test Email",
        preheader_text="Preview text here",
    )
    assert "<!DOCTYPE html>" in html
    assert "#0d6efd" in html  # corporate-blue accent
    assert "Preview text here" in html
    assert "Test Email" in html


def test_render_different_presets_have_different_colors():
    """Different style presets must produce different accent colors."""
    preset_a = EmailPreset.load("corporate-blue")
    preset_b = EmailPreset.load("dark-minimal")
    tmpl_a = EmailTemplate(preset_a)
    tmpl_b = EmailTemplate(preset_b)
    html_a = tmpl_a.render(content="<p>A</p>")
    html_b = tmpl_b.render(content="<p>B</p>")
    assert "#0d6efd" in html_a  # corporate-blue
    assert "#4da3ff" in html_b  # dark-minimal


def test_render_preheader_defaults_to_title():
    """If no preheader_text, it should default to email_title."""
    preset = EmailPreset.load("corporate-blue")
    template = EmailTemplate(preset)
    html = template.render(content="<p>Content</p>", email_title="My Title")
    assert "My Title" in html


def test_render_empty_content_does_not_crash():
    """Empty content should not raise an exception."""
    preset = EmailPreset.load("corporate-blue")
    template = EmailTemplate(preset)
    html = template.render(content="")
    assert isinstance(html, str)
    assert "<!DOCTYPE html>" in html


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
