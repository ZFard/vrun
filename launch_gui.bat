@echo off
echo Starting VASP DOS Plotter GUI...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Launch the GUI application
python run_gui.py

pause
