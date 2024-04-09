@echo off

set ENV_NAME=venv

REM Check if the virtual environment directory exists
if not exist "%ENV_NAME%" (
    REM Create the virtual environment
    echo Creating virtual environment...
    python -m venv %ENV_NAME%
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Activate the virtual environment
echo Activating the virtual environment...
call %ENV_NAME%\Scripts\activate

REM Check if requirements.txt exists and install packages
if exist requirements.txt (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    echo Dependencies installed.
) else (
    echo requirements.txt not found. If you have dependencies, please ensure the file is present.
)

echo Virtual environment activated. You can now run Python scripts within this environment.
cmd /k
