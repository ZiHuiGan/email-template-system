"""
HTML Validator for email templates

Validates HTML email structure and integrity
"""

from typing import List, Tuple


class HTMLValidator:
    """Validates email HTML for correctness and email client compatibility"""

    @staticmethod
    def validate(html: str) -> Tuple[bool, List[str]]:
        """
        Validate HTML email for common issues

        Args:
            html: HTML string to validate

        Returns:
            Tuple of (is_valid, errors_list)
        """
        errors = []

        # Check for DOCTYPE
        if not html.strip().startswith("<!DOCTYPE"):
            errors.append("Missing DOCTYPE declaration")

        # Check for unclosed tags
        required_tags = ["<html>", "<body>", "<head>"]
        for tag in required_tags:
            if f"{tag}" in html and f"</{tag[1:]}" not in html:
                errors.append(f"Unclosed tag: {tag}")

        # Check for proper meta tags
        if "<meta charset" not in html:
            errors.append("Missing charset meta tag")

        if "viewport" not in html:
            errors.append("Missing viewport meta tag")

        # Check for proper email container
        if 'class="email-container"' not in html:
            errors.append("Missing email-container div")

        # Check for CSS variables usage
        if "var(--" not in html and "<style>" in html:
            errors.append("Should use CSS variables instead of hardcoded values")

        # Check for clamp() usage for responsive sizing
        if "px" in html and "clamp(" not in html:
            # This is a warning, not a critical error
            pass

        # Check for proper closing tags
        divs_open = html.count("<div")
        divs_close = html.count("</div>")
        if divs_open != divs_close:
            errors.append(f"Mismatched div tags: {divs_open} open, {divs_close} close")

        # Check for deprecated attributes
        deprecated_attrs = ["border=", "cellpadding=", "cellspacing="]
        for attr in deprecated_attrs:
            if attr in html:
                errors.append(f"Uses deprecated HTML attribute: {attr}")

        return (len(errors) == 0, errors)

    @staticmethod
    def validate_structure(html: str) -> Tuple[bool, List[str]]:
        """Validate email structure against email-template-system standards"""
        errors = []

        required_elements = {
            'class="header"': "Header section",
            'class="email-content"': "Email content area",
            'class="footer"': "Footer section",
        }

        for selector, name in required_elements.items():
            if selector not in html:
                errors.append(f"Missing required element: {name} ({selector})")

        return (len(errors) == 0, errors)

    @staticmethod
    def get_stats(html: str) -> dict:
        """Get statistics about the HTML"""
        return {
            "total_lines": len(html.split("\n")),
            "total_size_bytes": len(html.encode("utf-8")),
            "num_sections": html.count('class="section"'),
            "num_images": html.count("<img"),
            "num_links": html.count("<a href"),
            "num_buttons": html.count('class="cta-button"'),
        }


def validate_email_html(html: str, verbose: bool = False) -> bool:
    """
    Quick validation function

    Returns True if HTML is valid, False otherwise
    """
    validator = HTMLValidator()
    is_valid, errors = validator.validate(html)

    if verbose and errors:
        print(f"HTML Validation Errors ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")

    return is_valid
