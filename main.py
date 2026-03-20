"""
MuRuZ Character Build Helper — Entry point
Run this file to launch the application.

To build as .exe (with icon and bundled resources):
    pip install pyinstaller
    pyinstaller --onefile --windowed --name MuRuZ_Build_Helper --icon=assets/icon.ico --add-data "assets;assets" main.py
"""

from ui.app_ui import run_app

if __name__ == "__main__":
    run_app()
