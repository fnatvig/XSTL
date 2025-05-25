@echo off
call venv\Scripts\activate.bat
python -B src\run_experiment.py --test H3

pause