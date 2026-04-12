"""
Setup script for email-template-system
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="email-template-system",
    version="1.0.0",
    author="news-intelligence",
    author_email="your-email@example.com",
    description="Reusable HTML email template system with presets, components, and validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZiHuiGan/email-template-system",
    project_urls={
        "Bug Tracker": "https://github.com/ZiHuiGan/email-template-system/issues",
        "Documentation": "https://github.com/ZiHuiGan/email-template-system/blob/main/SKILL.md",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Email",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.7",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "email_template_system": [
            "presets/*.json",
            "templates/*.html",
            "templates/components/*.html",
        ],
    },
    install_requires=[],  # No dependencies!
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            # Future CLI tools can go here
        ],
    },
    keywords=[
        "email",
        "templates",
        "html",
        "presets",
        "responsive",
        "accessibility",
        "wcag",
    ],
)
