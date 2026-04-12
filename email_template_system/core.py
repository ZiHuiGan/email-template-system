"""
Email Template System

A reusable, modular system for generating professional HTML emails with
visual style presets, email-client-compatible templates, and validation.

Usage:
    from email_template_system import EmailPreset, EmailTemplate

    preset = EmailPreset.load("corporate-blue")
    template = EmailTemplate(preset)
    html = template.render(content="<div>Email content</div>")
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from email_template_system.validators.html_validator import HTMLValidator
from email_template_system.validators.wcag_checker import WCAGChecker
from email_template_system.validators.constraints_checker import ConstraintsChecker


class EmailPreset:
    """
    Represents a visual style preset with colors, fonts, and design tokens.
    Presets define design language, not content type.
    """

    def __init__(self, preset_dict: Dict[str, Any]):
        """Initialize preset from dictionary."""
        self.data = preset_dict
        self.name = preset_dict.get("name", "Unnamed Preset")
        self.colors = preset_dict.get("colors", {})
        self.fonts = preset_dict.get("fonts", {})
        self.category = preset_dict.get("category", "professional")

    @classmethod
    def load(cls, preset_name: str) -> "EmailPreset":
        """Load preset from JSON file by name (e.g., 'corporate-blue')."""
        presets_dir = Path(__file__).parent / "presets"
        preset_path = presets_dir / f"{preset_name}.json"

        if not preset_path.exists():
            available = [f.stem for f in presets_dir.glob("*.json") if f.stem != "_schema"]
            raise FileNotFoundError(
                f"Preset not found: {preset_name}. "
                f"Available: {', '.join(sorted(available))}"
            )

        with open(preset_path) as f:
            preset_dict = json.load(f)

        return cls(preset_dict)

    @classmethod
    def list_presets(cls) -> List[str]:
        """Return names of all available presets."""
        presets_dir = Path(__file__).parent / "presets"
        return sorted(f.stem for f in presets_dir.glob("*.json") if f.stem != "_schema")

    def to_dict(self) -> Dict[str, Any]:
        """Return preset as dictionary."""
        return self.data

    def validate_colors(self) -> tuple:
        """Validate color contrast in preset."""
        checker = WCAGChecker()
        return checker.validate_color_contrast(self.colors)


class EmailTemplate:
    """
    Renders email HTML from a visual style preset.
    Produces email-client-compatible HTML with inline fallbacks.
    """

    def __init__(self, preset: EmailPreset):
        """Initialize template with preset."""
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
        preheader_text: Optional[str] = None,
        unsubscribe_url: Optional[str] = "https://example.com/unsubscribe",
    ) -> str:
        """
        Render email HTML with preset styling.

        Args:
            content: HTML content for the email body
            email_title: Title for <title> tag
            header_meta: Metadata string for header (e.g., date, article count)
            preheader_text: Hidden inbox preview text (40-130 chars recommended)
            unsubscribe_url: URL for unsubscribe link

        Returns:
            Rendered HTML string compatible with major email clients
        """
        colors = self.preset.colors
        fonts = self.preset.fonts
        dark_colors = self.preset.data.get("dark_mode", colors)
        design = self.preset.data.get("design", {})

        # Build font stack link
        font_stack = ""
        if fonts.get("google_fonts_url"):
            font_stack = f'<link rel="stylesheet" href="{fonts["google_fonts_url"]}" />'

        # Build preheader (default to email_title if not provided)
        preheader = preheader_text or email_title or self.preset.name

        # Prepare substitution dictionary
        template_vars = {
            "email_title": email_title or self.preset.name,
            "font_stack": font_stack,
            # Colors
            "bg_primary": colors.get("bg_primary", "#ffffff"),
            "bg_section": colors.get("bg_section", "#f5f5f5"),
            "text_primary": colors.get("text_primary", "#000000"),
            "text_secondary": colors.get("text_secondary", "#666666"),
            "accent": colors.get("accent", "#0066cc"),
            "highlight": colors.get("highlight", "#ff6600"),
            "border": colors.get("border", "#e0e0e0"),
            # Fonts
            "font_headings": fonts.get("headings", "Arial, sans-serif"),
            "font_body": fonts.get("body", "Arial, sans-serif"),
            "font_mono": fonts.get("mono", "monospace"),
            # Typography
            "headline_size": self.preset.data.get("typography", {}).get(
                "headline_size", "clamp(24px, 5vw, 28px)"
            ),
            "body_size": self.preset.data.get("typography", {}).get(
                "body_size", "clamp(14px, 1.5vw, 16px)"
            ),
            "mono_size": self.preset.data.get("typography", {}).get(
                "mono_size", "clamp(12px, 1vw, 13px)"
            ),
            # Layout
            "section_padding": self.preset.data.get("layout", {}).get(
                "section_padding", "24px"
            ),
            "line_height": self.preset.data.get("layout", {}).get(
                "line_height", "1.6"
            ),
            # Design
            "border_radius": design.get("border_radius", "8px"),
            # Dark mode
            "dark_bg_primary": dark_colors.get("bg_primary", colors.get("bg_primary")),
            "dark_bg_section": dark_colors.get("bg_section", colors.get("bg_section")),
            "dark_text_primary": dark_colors.get(
                "text_primary", colors.get("text_primary")
            ),
            "dark_text_secondary": dark_colors.get(
                "text_secondary", colors.get("text_secondary")
            ),
            # Content
            "preset_header": email_title or self.preset.name,
            "header_meta": header_meta or "",
            "preheader_text": preheader,
            "email_content": content,
            "unsubscribe_url": unsubscribe_url,
        }

        # Simple template substitution
        html = self.base_html
        for key, value in template_vars.items():
            placeholder = "{{ " + key + " }}"
            html = html.replace(placeholder, str(value))

        return html

    def validate(self, html: str, verbose: bool = False) -> tuple:
        """Validate rendered HTML for structure and accessibility."""
        html_valid, html_issues = self.validator.validate(html)

        all_issues = html_issues

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
    preheader_text: Optional[str] = None,
    validate: bool = True,
) -> str:
    """
    Convenience function to render email in one call.

    Args:
        preset_name: Style preset name (e.g., 'corporate-blue')
        content: Email content HTML
        email_title: Email title
        preheader_text: Hidden inbox preview text
        validate: Whether to validate output

    Returns:
        Rendered HTML email
    """
    preset = EmailPreset.load(preset_name)
    template = EmailTemplate(preset)
    html = template.render(content, email_title, preheader_text=preheader_text)

    if validate:
        is_valid, issues = template.validate(html, verbose=True)
        if not is_valid:
            print(f"Warning: Email has {len(issues)} validation issues")

    return html


__version__ = "2.0.0"
__all__ = [
    "EmailPreset",
    "EmailTemplate",
    "render_email",
]
