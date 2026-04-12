"""
Email Template System — reusable HTML email presets, templates, and validation.

Usage:
    from email_template_system import EmailPreset, EmailTemplate

    preset = EmailPreset.load("evening-debrief")
    template = EmailTemplate(preset)
    html = template.render(content="<div>...</div>")
"""

from email_template_system.core import EmailPreset, EmailTemplate, render_email

__version__ = "1.0.0"
__all__ = ["EmailPreset", "EmailTemplate", "render_email"]
