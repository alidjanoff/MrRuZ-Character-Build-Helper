@echo off
echo ============================================
echo   MuRuZ Character Build Helper - Setup
echo ============================================
echo.
echo Installing PyInstaller for .exe compilation...
pip install pyinstaller
echo.
echo ============================================
echo   Setup complete!
echo.
echo   To run the application:
echo     python main.py
echo.
echo   To build .exe:
echo     pyinstaller --onefile --windowed --name MuRuZ_Build_Helper main.py
echo ============================================
pause
