@echo off
echo Starting VASP DOS Plotter GUI...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Launch the GUI application
python dos_plotter_gui.py

pause
