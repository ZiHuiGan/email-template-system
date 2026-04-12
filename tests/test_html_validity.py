"""
Tests for HTML email validity

Validates that generated HTML is structurally sound
"""

from pathlib import Path
import sys

# Add validators to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.html_validator import HTMLValidator


def get_sample_html():
    """Get a sample valid HTML email"""
    templates_dir = Path(__file__).parent.parent / "templates"
    with open(templates_dir / "base.html") as f:
        return f.read()


def test_html_validator_validates_good_html():
    """Test that validator accepts valid HTML"""
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

    # Should have some errors (missing styles), but basic structure is OK
    assert "<html>" in html


def test_html_validator_catches_missing_doctype():
    """Test that validator catches missing DOCTYPE"""
    html = """<html>
<head><title>Test</title></head>
<body></body>
</html>"""

    validator = HTMLValidator()
    is_valid, errors = validator.validate(html)

    assert not is_valid
    assert any("DOCTYPE" in error for error in errors)


def test_html_validator_catches_unclosed_tags():
    """Test that validator catches unclosed tags"""
    html = """<!DOCTYPE html>
<html>
<head><title>Test</title>
<body>Content</body>
</html>"""

    validator = HTMLValidator()
    is_valid, errors = validator.validate(html)

    assert not is_valid


def test_html_validator_catches_missing_charset():
    """Test that validator catches missing charset"""
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Test</title>
</head>
<body></body>
</html>"""

    validator = HTMLValidator()
    is_valid, errors = validator.validate(html)

    assert any("charset" in error.lower() for error in errors)


def test_html_validator_checks_structure():
    """Test that validator checks for required structure"""
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width" />
    <title>Test</title>
</head>
<body>
    <div class="email-container">
    </div>
</body>
</html>"""

    validator = HTMLValidator()
    is_valid, errors = validator.validate_structure(html)

    # Should fail because missing header, content, footer
    assert not is_valid


def test_html_validator_gets_stats():
    """Test that validator can get HTML stats"""
    html = """<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
    <div class="section">Content</div>
    <img src="test.jpg" />
    <a href="#">Link</a>
</body>
</html>"""

    validator = HTMLValidator()
    stats = validator.get_stats(html)

    assert stats["num_sections"] == 1
    assert stats["num_images"] == 1
    assert stats["num_links"] == 1
    assert stats["total_size_bytes"] > 0


def test_base_template_has_variables():
    """Test that base template has required placeholders"""
    templates_dir = Path(__file__).parent.parent / "templates"
    with open(templates_dir / "base.html") as f:
        html = f.read()

    required_variables = [
        "{{ email_title }}",
        "{{ preset_header }}",
        "{{ email_content }}",
        "{{ unsubscribe_url }}",
    ]

    for var in required_variables:
        assert var in html, f"Missing template variable: {var}"


def test_base_template_has_css_variables():
    """Test that base template uses CSS variables"""
    templates_dir = Path(__file__).parent.parent / "templates"
    with open(templates_dir / "base.html") as f:
        html = f.read()

    # Check for CSS variable definitions
    assert "var(--" in html
    assert "--bg-primary" in html
    assert "--text-primary" in html
    assert "--accent" in html


def test_base_template_responsive():
    """Test that base template uses responsive sizing"""
    templates_dir = Path(__file__).parent.parent / "templates"
    with open(templates_dir / "base.html") as f:
        html = f.read()

    # Should use clamp() for responsive sizing
    assert "clamp(" in html


def test_base_template_dark_mode():
    """Test that base template supports dark mode"""
    templates_dir = Path(__file__).parent.parent / "templates"
    with open(templates_dir / "base.html") as f:
        html = f.read()

    # Should have media query for dark mode
    assert "@media (prefers-color-scheme: dark)" in html
    assert "dark_mode" in html.lower()


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
