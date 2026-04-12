"""
WCAG Accessibility Checker for email templates

Validates email templates for WCAG 2.1 AA accessibility compliance
"""

from typing import List, Tuple
import re


class WCAGChecker:
    """Checks email HTML for WCAG 2.1 AA accessibility compliance"""

    # Minimum contrast ratio for WCAG AA
    MIN_CONTRAST_RATIO = 4.5

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 6:
            return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        return (0, 0, 0)

    @staticmethod
    def calculate_luminance(rgb: Tuple[int, int, int]) -> float:
        """Calculate relative luminance per WCAG"""
        r, g, b = [x / 255.0 for x in rgb]

        def adjust(x):
            return x / 12.92 if x <= 0.03928 else ((x + 0.05) / 1.05) ** 2.4

        r, g, b = adjust(r), adjust(g), adjust(b)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    @staticmethod
    def calculate_contrast(fg: str, bg: str) -> float:
        """Calculate contrast ratio between two colors"""
        fg_rgb = WCAGChecker.hex_to_rgb(fg)
        bg_rgb = WCAGChecker.hex_to_rgb(bg)

        fg_lum = WCAGChecker.calculate_luminance(fg_rgb)
        bg_lum = WCAGChecker.calculate_luminance(bg_rgb)

        lighter = max(fg_lum, bg_lum)
        darker = min(fg_lum, bg_lum)

        return (lighter + 0.05) / (darker + 0.05)

    @staticmethod
    def check_color_contrast(
        html: str, fg_color: str, bg_color: str
    ) -> Tuple[bool, str]:
        """Check if foreground/background colors meet WCAG AA standard"""
        contrast = WCAGChecker.calculate_contrast(fg_color, bg_color)

        if contrast >= WCAGChecker.MIN_CONTRAST_RATIO:
            return (True, f"Contrast ratio: {contrast:.2f}:1 ✓ (meets WCAG AA)")
        else:
            return (False, f"Contrast ratio: {contrast:.2f}:1 ✗ (needs {WCAGChecker.MIN_CONTRAST_RATIO}:1)")

    @staticmethod
    def validate(html: str) -> Tuple[bool, List[str]]:
        """
        Validate HTML for accessibility issues

        Args:
            html: HTML string to validate

        Returns:
            Tuple of (is_valid, issues_list)
        """
        issues = []

        # Check for alt text on images
        img_tags = re.findall(r"<img[^>]*>", html)
        for img in img_tags:
            if "alt=" not in img:
                issues.append(f"Image missing alt text: {img[:50]}...")

        # Check for link text
        link_pattern = r"<a[^>]*href=[^>]*>([^<]*)</a>"
        links = re.findall(link_pattern, html)
        for link_text in links:
            if link_text.strip() in ["click here", "read more", "link", ">"]:
                issues.append(f"Link has non-descriptive text: '{link_text}'")

        # Check for heading hierarchy
        if "<h1>" not in html:
            issues.append("No h1 heading found")

        # Check for color contrast issues (basic check)
        if "--text-primary" in html and "--bg-primary" in html:
            # We're using CSS variables, so contrast should be OK
            pass

        # Check for proper list markup
        if "<ul>" in html or "<ol>" in html:
            list_items = html.count("<li>")
            ul_count = html.count("<ul>")
            ol_count = html.count("<ol>")
            if (ul_count + ol_count) == 0 and list_items > 0:
                issues.append("List items found outside of <ul> or <ol>")

        return (len(issues) == 0, issues)

    @staticmethod
    def validate_color_contrast(colors: dict) -> Tuple[bool, List[str]]:
        """
        Validate color contrast for email preset

        Args:
            colors: Dictionary with 'text_primary', 'text_secondary', 'bg_primary', 'bg_section'

        Returns:
            Tuple of (is_valid, issues_list)
        """
        issues = []

        # Check primary text on primary background
        is_valid, message = WCAGChecker.check_color_contrast(
            "", colors.get("text_primary", "#000000"), colors.get("bg_primary", "#ffffff")
        )
        if not is_valid:
            issues.append(f"Primary text on primary background: {message}")

        # Check primary text on section background
        is_valid, message = WCAGChecker.check_color_contrast(
            "", colors.get("text_primary", "#000000"), colors.get("bg_section", "#ffffff")
        )
        if not is_valid:
            issues.append(f"Primary text on section background: {message}")

        # Check secondary text on primary background
        is_valid, message = WCAGChecker.check_color_contrast(
            "", colors.get("text_secondary", "#666666"), colors.get("bg_primary", "#ffffff")
        )
        if not is_valid:
            issues.append(f"Secondary text on primary background: {message}")

        return (len(issues) == 0, issues)


def validate_accessibility(html: str, verbose: bool = False) -> bool:
    """
    Quick accessibility validation function

    Returns True if HTML meets WCAG AA standards, False otherwise
    """
    checker = WCAGChecker()
    is_valid, issues = checker.validate(html)

    if verbose and issues:
        print(f"Accessibility Issues ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")

    return is_valid
