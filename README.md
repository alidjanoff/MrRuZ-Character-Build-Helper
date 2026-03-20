# MuRuZ Character Build Helper

An intelligent stat optimizer and formula-driven recommendation engine for MU Online builds.
The application helps players distribute their level-up and reset points optimally across different stats based on actual game formulas rather than guesswork.

## Features

- **Formula-Driven**: Uses exact game logic formulas for all 10 character classes
- **Multilingual Support**: English, Russian, and Azerbaijani
- **Build Archetypes**: Generates tailored advice for Farm, PvE (Bosses), and PvP
- **Bonus Point Detection**: Warns if your current points differ from standard progressions
- **Vitality Toggle**: Skip standard VIT allocations if your gear provides high HP
- **Modern UI**: Clean, responsive interface with easy-to-read reports

## How to Run

1. Ensure you have Python installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## How to Build .exe

To create a standalone executable that you can share without needing Python installed:

1. Double-click the `build_exe.bat` file.
2. Wait for PyInstaller to finish processing.
3. The generated executable will be found in the `dist` folder.
