"""
Tests for email presets

Validates that all presets are properly formatted and complete
"""

import json
import os
from pathlib import Path


def test_preset_files_exist():
    """Test that all required preset files exist"""
    presets_dir = Path(__file__).parent.parent / "email_template_system" / "presets"
    required_presets = [
        "evening-debrief.json",
        "weekly-report.json",
        "morning-brief.json",
    ]

    for preset_file in required_presets:
        preset_path = presets_dir / preset_file
        assert preset_path.exists(), f"Missing preset: {preset_file}"


def test_preset_schema_valid():
    """Test that all presets follow the schema"""
    presets_dir = Path(__file__).parent.parent / "email_template_system" / "presets"

    # Load schema
    with open(presets_dir / "_schema.json") as f:
        schema = json.load(f)

    # Test each preset
    preset_files = [
        "evening-debrief.json",
        "weekly-report.json",
        "morning-brief.json",
    ]

    for preset_file in preset_files:
        with open(presets_dir / preset_file) as f:
            preset = json.load(f)

        # Check required fields
        for required_field in schema["required"]:
            assert (
                required_field in preset
            ), f"{preset_file} missing required field: {required_field}"

        # Check colors have valid hex values
        colors = preset.get("colors", {})
        for color_name, color_value in colors.items():
            assert isinstance(
                color_value, str
            ), f"{preset_file} color {color_name} is not a string"
            if "#" in color_value:
                assert color_value.startswith(
                    "#"
                ), f"{preset_file} color {color_name} should start with #"


def test_evening_debrief_constraints():
    """Test Evening Debrief specific constraints"""
    presets_dir = Path(__file__).parent.parent / "email_template_system" / "presets"

    with open(presets_dir / "evening-debrief.json") as f:
        preset = json.load(f)

    assert preset["constraints"]["max_sections"] == 5
    assert preset["constraints"]["max_images"] == 2
    assert preset["constraints"]["max_cta_buttons"] == 1


def test_weekly_report_constraints():
    """Test Weekly Report specific constraints"""
    presets_dir = Path(__file__).parent.parent / "email_template_system" / "presets"

    with open(presets_dir / "weekly-report.json") as f:
        preset = json.load(f)

    assert preset["constraints"]["max_sections"] == 6
    assert preset["constraints"]["max_images"] == 3
    assert preset["constraints"]["max_cta_buttons"] == 2


def test_morning_brief_constraints():
    """Test Morning Brief specific constraints"""
    presets_dir = Path(__file__).parent.parent / "email_template_system" / "presets"

    with open(presets_dir / "morning-brief.json") as f:
        preset = json.load(f)

    assert preset["constraints"]["max_sections"] == 4
    assert preset["constraints"]["max_images"] == 1
    assert preset["constraints"]["max_cta_buttons"] == 1


def test_preset_color_scheme():
    """Test that preset colors are properly defined"""
    presets_dir = Path(__file__).parent.parent / "email_template_system" / "presets"

    preset_files = [
        "evening-debrief.json",
        "weekly-report.json",
        "morning-brief.json",
    ]

    for preset_file in preset_files:
        with open(presets_dir / preset_file) as f:
            preset = json.load(f)

        colors = preset.get("colors", {})

        # Check required colors
        required_colors = [
            "bg_primary",
            "text_primary",
            "accent",
        ]

        for color in required_colors:
            assert (
                color in colors
            ), f"{preset_file} missing required color: {color}"

        # Check dark mode colors
        dark_colors = preset.get("dark_mode", {})
        assert (
            len(dark_colors) > 0
        ), f"{preset_file} should have dark_mode colors"


def test_preset_fonts():
    """Test that preset fonts are properly defined"""
    presets_dir = Path(__file__).parent.parent / "email_template_system" / "presets"

    preset_files = [
        "evening-debrief.json",
        "weekly-report.json",
        "morning-brief.json",
    ]

    for preset_file in preset_files:
        with open(presets_dir / preset_file) as f:
            preset = json.load(f)

        fonts = preset.get("fonts", {})

        # Check required fonts
        required_fonts = ["headings", "body"]

        for font in required_fonts:
            assert (
                font in fonts
            ), f"{preset_file} missing required font: {font}"

        # Check Google Fonts URL if present
        if "google_fonts_url" in fonts:
            assert fonts["google_fonts_url"].startswith(
                "https://fonts.googleapis.com"
            ), f"{preset_file} has invalid Google Fonts URL"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
