"""
app_config.py — Application Configuration & Updates
Store the app's version, basic details, and release notes here.
You can import these variables anywhere in the project (e.g., to display the version in the UI).
"""

APP_NAME = "MuRuZ Character Build Helper"
VERSION = "1.0.0"

DESCRIPTION = """
Smart MU Online character build calculator with AI-driven stat recommendations (Farm / PvE / PvP).
"""

# You can add the latest news or changelog here to easily keep track of updates.
# Later, you could display this list in your UI for users to see "What's New".
UPDATES_LOG = [
    {
        "version": "1.0.0",
        "date": "2026-03-21",
        "title": "Release",
        "changes": [
            "Added AI-driven stat recommendations.",
            "Included Farm, PvE, and PvP build archetypes.",
            "Multi-language support added (EN, RU, AZ).",
            "Refactored project to a clean, modular structure."
        ]
    }
]
