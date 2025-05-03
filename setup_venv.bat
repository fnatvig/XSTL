@echo off
echo Creating virtual environment in "venv"...
python -m venv venv

if exist venv\Scripts\activate.bat (
    echo Virtual environment created successfully.
    echo Activating environment...
    call venv\Scripts\activate.bat

    if exist requirements.txt (
        echo Installing dependencies from requirements.txt...
        pip install -r requirements.txt
    ) else (
        echo No requirements.txt found. Skipping package installation.
    )
) else (
    echo Failed to create virtual environment. Please make sure Python is installed and added to PATH.
)

pause
