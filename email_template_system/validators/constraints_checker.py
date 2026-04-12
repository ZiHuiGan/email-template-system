"""
Constraints Checker for email templates

Validates that emails follow preset constraints
"""

from typing import List, Tuple
import re
import json


class ConstraintsChecker:
    """Validates emails against preset constraints"""

    @staticmethod
    def validate_against_preset(html: str, preset_dict: dict) -> Tuple[bool, List[str]]:
        """
        Validate HTML against preset constraints

        Args:
            html: HTML string to validate
            preset_dict: Preset dictionary with 'constraints' key

        Returns:
            Tuple of (is_valid, violations_list)
        """
        violations = []
        constraints = preset_dict.get("constraints", {})

        # Check max sections
        max_sections = constraints.get("max_sections", 5)
        num_sections = html.count('class="section"')
        if num_sections > max_sections:
            violations.append(
                f"Too many sections: {num_sections} (max: {max_sections})"
            )

        # Check max images
        max_images = constraints.get("max_images", 2)
        num_images = len(re.findall(r"<img[^>]*>", html))
        if num_images > max_images:
            violations.append(f"Too many images: {num_images} (max: {max_images})")

        # Check max CTA buttons
        max_ctas = constraints.get("max_cta_buttons", 1)
        num_ctas = html.count('class="cta-button"')
        if num_ctas > max_ctas:
            violations.append(
                f"Too many CTA buttons: {num_ctas} (max: {max_ctas})"
            )

        # Check for proper CSS variable usage
        if "var(--" not in html:
            violations.append("Should use CSS variables (var(--...)) instead of hardcoded colors")

        return (len(violations) == 0, violations)

    @staticmethod
    def check_responsive_sizing(html: str) -> Tuple[bool, List[str]]:
        """Check if email uses responsive sizing (clamp)"""
        issues = []

        # Check for hardcoded pixel sizes
        hardcoded_px = re.findall(r"(?:width|height|padding|margin):\s*\d+px", html)
        if hardcoded_px:
            issues.append(
                f"Found {len(hardcoded_px)} hardcoded pixel sizes (use clamp() instead)"
            )

        # Check for clamp() usage
        if "clamp(" not in html:
            issues.append(
                "No clamp() found - consider using clamp() for responsive font sizes"
            )

        return (len(issues) == 0, issues)

    @staticmethod
    def check_content_density(html: str, preset_dict: dict) -> dict:
        """
        Analyze content density of email

        Returns dictionary with density metrics
        """
        # Count content elements
        headings = len(re.findall(r"<h[1-6]>", html))
        paragraphs = len(re.findall(r"<p>", html))
        lists = len(re.findall(r"<li>", html))
        images = len(re.findall(r"<img[^>]*>", html))
        buttons = html.count('class="cta-button"')

        total_content = headings + paragraphs + lists + images + buttons

        # Get constraints from preset
        constraints = preset_dict.get("constraints", {})
        max_sections = constraints.get("max_sections", 5)

        return {
            "total_elements": total_content,
            "headings": headings,
            "paragraphs": paragraphs,
            "lists": lists,
            "images": images,
            "buttons": buttons,
            "avg_per_section": total_content / max(max_sections, 1),
        }


def validate_constraints(html: str, preset: dict, verbose: bool = False) -> bool:
    """
    Quick constraints validation function

    Returns True if email meets all constraints, False otherwise
    """
    checker = ConstraintsChecker()
    is_valid, violations = checker.validate_against_preset(html, preset)

    if verbose and violations:
        print(f"Constraint Violations ({len(violations)}):")
        for violation in violations:
            print(f"  - {violation}")

    return is_valid
