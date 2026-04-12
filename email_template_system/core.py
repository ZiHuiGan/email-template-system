"""
Email Template System

A reusable, modular system for generating professional HTML emails with
preset styles, templates, and automatic validation.

Usage:
    from email_template_system import EmailPreset, EmailTemplate

    preset = EmailPreset.load("evening-debrief")
    template = EmailTemplate(preset)
    html = template.render(content="<div>Email content</div>")
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any
from email_template_system.validators.html_validator import HTMLValidator
from email_template_system.validators.wcag_checker import WCAGChecker
from email_template_system.validators.constraints_checker import ConstraintsChecker


class EmailPreset:
    """
    Represents an email template preset with colors, fonts, and constraints
    """

    def __init__(self, preset_dict: Dict[str, Any]):
        """
        Initialize preset from dictionary

        Args:
            preset_dict: Dictionary containing preset configuration
        """
        self.data = preset_dict
        self.name = preset_dict.get("name", "Unnamed Preset")
        self.colors = preset_dict.get("colors", {})
        self.fonts = preset_dict.get("fonts", {})
        self.constraints = preset_dict.get("constraints", {})

    @classmethod
    def load(cls, preset_name: str) -> "EmailPreset":
        """
        Load preset from JSON file

        Args:
            preset_name: Name of preset (e.g., 'evening-debrief')

        Returns:
            EmailPreset instance
        """
        presets_dir = Path(__file__).parent / "presets"
        preset_path = presets_dir / f"{preset_name}.json"

        if not preset_path.exists():
            raise FileNotFoundError(f"Preset not found: {preset_name}")

        with open(preset_path) as f:
            preset_dict = json.load(f)

        return cls(preset_dict)

    def to_dict(self) -> Dict[str, Any]:
        """Return preset as dictionary"""
        return self.data

    def validate_colors(self) -> tuple:
        """Validate color contrast in preset"""
        checker = WCAGChecker()
        return checker.validate_color_contrast(self.colors)


class EmailTemplate:
    """
    Renders email HTML from a preset template
    """

    def __init__(self, preset: EmailPreset):
        """
        Initialize template with preset

        Args:
            preset: EmailPreset instance
        """
        self.preset = preset
        self.validator = HTMLValidator()
        self.constraints_checker = ConstraintsChecker()

        # Load base template
        templates_dir = Path(__file__).parent / "templates"
        with open(templates_dir / "base.html") as f:
            self.base_html = f.read()

    def render(
        self,
        content: str,
        email_title: Optional[str] = None,
        header_meta: Optional[str] = None,
        unsubscribe_url: Optional[str] = "https://example.com/unsubscribe",
    ) -> str:
        """
        Render email HTML

        Args:
            content: HTML content for {{ email_content }}
            email_title: Title for <title> tag
            header_meta: Metadata for header (e.g., date)
            unsubscribe_url: URL for unsubscribe link

        Returns:
            Rendered HTML string
        """
        # Prepare template variables
        colors = self.preset.colors
        fonts = self.preset.fonts
        dark_colors = self.preset.data.get("dark_mode", colors)

        # Build font stack link
        font_stack = ""
        if fonts.get("google_fonts_url"):
            font_stack = f'<link rel="stylesheet" href="{fonts["google_fonts_url"]}" />'

        # Prepare substitution dictionary
        template_vars = {
            "email_title": email_title or self.preset.name,
            "font_stack": font_stack,
            "bg_primary": colors.get("bg_primary", "#ffffff"),
            "bg_section": colors.get("bg_section", "#f5f5f5"),
            "text_primary": colors.get("text_primary", "#000000"),
            "text_secondary": colors.get("text_secondary", "#666666"),
            "accent": colors.get("accent", "#0066cc"),
            "highlight": colors.get("highlight", "#ff6600"),
            "border": colors.get("border", "#e0e0e0"),
            "font_headings": fonts.get("headings", "Arial, sans-serif"),
            "font_body": fonts.get("body", "Arial, sans-serif"),
            "font_mono": fonts.get("mono", "monospace"),
            "headline_size": self.preset.data.get("typography", {}).get(
                "headline_size", "2rem"
            ),
            "body_size": self.preset.data.get("typography", {}).get(
                "body_size", "1rem"
            ),
            "mono_size": self.preset.data.get("typography", {}).get(
                "mono_size", "0.875rem"
            ),
            "section_padding": self.preset.data.get("layout", {}).get(
                "section_padding", "24px"
            ),
            "line_height": self.preset.data.get("layout", {}).get(
                "line_height", "1.6"
            ),
            "dark_bg_primary": dark_colors.get("bg_primary", colors.get("bg_primary")),
            "dark_bg_section": dark_colors.get("bg_section", colors.get("bg_section")),
            "dark_text_primary": dark_colors.get(
                "text_primary", colors.get("text_primary")
            ),
            "dark_text_secondary": dark_colors.get(
                "text_secondary", colors.get("text_secondary")
            ),
            "preset_header": self.preset.name,
            "header_meta": header_meta or "",
            "email_content": content,
            "unsubscribe_url": unsubscribe_url,
        }

        # Simple template substitution (not using Jinja2 to avoid dependencies)
        html = self.base_html
        for key, value in template_vars.items():
            placeholder = "{{ " + key + " }}"
            html = html.replace(placeholder, str(value))

        return html

    def validate(self, html: str, verbose: bool = False) -> tuple:
        """
        Validate rendered HTML

        Args:
            html: HTML to validate
            verbose: Print validation issues

        Returns:
            Tuple of (is_valid, issues_list)
        """
        # Run all validators
        html_valid, html_issues = self.validator.validate(html)
        constraints_valid, constraint_issues = self.constraints_checker.validate_against_preset(
            html, self.preset.data
        )

        all_issues = html_issues + constraint_issues

        if verbose and all_issues:
            print(f"Validation Issues ({len(all_issues)}):")
            for issue in all_issues:
                print(f"  - {issue}")

        return (len(all_issues) == 0, all_issues)


# Convenience functions

def render_email(
    preset_name: str,
    content: str,
    email_title: Optional[str] = None,
    validate: bool = True,
) -> str:
    """
    Convenience function to render email in one call

    Args:
        preset_name: Name of preset to use
        content: Email content HTML
        email_title: Email title
        validate: Whether to validate output

    Returns:
        Rendered HTML email
    """
    preset = EmailPreset.load(preset_name)
    template = EmailTemplate(preset)
    html = template.render(content, email_title)

    if validate:
        is_valid, issues = template.validate(html, verbose=True)
        if not is_valid:
            print(f"⚠️ Email has {len(issues)} validation issues")

    return html


__version__ = "1.0.0"
__all__ = [
    "EmailPreset",
    "EmailTemplate",
    "render_email",
]
