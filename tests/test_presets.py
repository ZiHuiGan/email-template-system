"""
Tests for visual style presets

Validates that all presets are properly formatted and follow the schema.
"""

import json
from pathlib import Path

PRESETS_DIR = Path(__file__).parent.parent / "email_template_system" / "presets"

EXPECTED_PRESETS = [
    "corporate-blue.json",
    "dark-minimal.json",
    "swiss-modern.json",
    "warm-editorial.json",
    "clean-pastel.json",
    "neon-tech.json",
]


def test_preset_files_exist():
    """All required style preset files must exist."""
    for preset_file in EXPECTED_PRESETS:
        assert (PRESETS_DIR / preset_file).exists(), f"Missing preset: {preset_file}"


def test_no_old_content_type_presets():
    """Old content-type presets (morning-brief, evening-debrief, weekly-report) must be deleted."""
    old_presets = ["morning-brief.json", "evening-debrief.json", "weekly-report.json"]
    for old in old_presets:
        assert not (PRESETS_DIR / old).exists(), f"Old preset should be deleted: {old}"


def test_preset_schema_valid():
    """All presets must follow the schema: required fields present, colors valid."""
    with open(PRESETS_DIR / "_schema.json") as f:
        schema = json.load(f)

    for preset_file in EXPECTED_PRESETS:
        with open(PRESETS_DIR / preset_file) as f:
            preset = json.load(f)

        for required_field in schema["required"]:
            assert required_field in preset, \
                f"{preset_file} missing required field: {required_field}"

        # Check colors have valid hex values
        for color_name, color_value in preset.get("colors", {}).items():
            assert isinstance(color_value, str), \
                f"{preset_file} color {color_name} is not a string"
            assert color_value.startswith("#"), \
                f"{preset_file} color {color_name} should start with #"


def test_preset_has_category():
    """Each preset must declare a category for discovery."""
    valid_categories = {"professional", "dark", "editorial", "creative"}
    for preset_file in EXPECTED_PRESETS:
        with open(PRESETS_DIR / preset_file) as f:
            preset = json.load(f)
        assert preset.get("category") in valid_categories, \
            f"{preset_file} has invalid category: {preset.get('category')}"


def test_preset_color_scheme():
    """Each preset must have required colors and dark mode overrides."""
    required_colors = ["bg_primary", "text_primary", "accent"]
    for preset_file in EXPECTED_PRESETS:
        with open(PRESETS_DIR / preset_file) as f:
            preset = json.load(f)

        for color in required_colors:
            assert color in preset.get("colors", {}), \
                f"{preset_file} missing required color: {color}"

        dark_colors = preset.get("dark_mode", {})
        assert len(dark_colors) > 0, \
            f"{preset_file} should have dark_mode colors"


def test_preset_fonts():
    """Each preset must define headings and body fonts."""
    for preset_file in EXPECTED_PRESETS:
        with open(PRESETS_DIR / preset_file) as f:
            preset = json.load(f)

        fonts = preset.get("fonts", {})
        assert "headings" in fonts, f"{preset_file} missing headings font"
        assert "body" in fonts, f"{preset_file} missing body font"

        if "google_fonts_url" in fonts:
            assert fonts["google_fonts_url"].startswith(
                "https://fonts.googleapis.com"
            ), f"{preset_file} has invalid Google Fonts URL"


def test_preset_has_typography():
    """Each preset must define responsive typography with clamp()."""
    for preset_file in EXPECTED_PRESETS:
        with open(PRESETS_DIR / preset_file) as f:
            preset = json.load(f)

        typo = preset.get("typography", {})
        assert "headline_size" in typo, f"{preset_file} missing headline_size"
        assert "clamp(" in typo["headline_size"], \
            f"{preset_file} headline_size should use clamp()"


def test_preset_has_design_tokens():
    """Each preset must have design tokens (border_radius, shadow, header_style)."""
    for preset_file in EXPECTED_PRESETS:
        with open(PRESETS_DIR / preset_file) as f:
            preset = json.load(f)

        design = preset.get("design", {})
        assert "border_radius" in design, f"{preset_file} missing border_radius"
        assert "header_style" in design, f"{preset_file} missing header_style"


def test_presets_have_unique_accents():
    """Each preset should have a unique accent color."""
    accents = []
    for preset_file in EXPECTED_PRESETS:
        with open(PRESETS_DIR / preset_file) as f:
            preset = json.load(f)
        accents.append(preset["colors"]["accent"])
    assert len(set(accents)) == len(accents), \
        f"Preset accent colors should be unique, got: {accents}"


def test_list_presets_api():
    """EmailPreset.list_presets() should return all available preset names."""
    from email_template_system import EmailPreset
    presets = EmailPreset.list_presets()
    for expected in ["corporate-blue", "dark-minimal", "swiss-modern"]:
        assert expected in presets, f"list_presets() missing: {expected}"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
