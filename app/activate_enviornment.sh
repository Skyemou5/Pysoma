#!/bin/bash

# Define the environment name and the alias for your application
ENV_NAME="venv"
ALIAS_NAME="pysoma"
MAIN_PY_PATH="./main.py"  # Relative path to your main.py

# Create the virtual environment if it doesn't exist
if [ ! -d "$ENV_NAME" ]; then
    echo "Creating virtual environment..."
    python -m venv "$ENV_NAME"
fi

# Activate the virtual environment if it's not already active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating the virtual environment..."
    source "$ENV_NAME/bin/activate"
else
    echo "Virtual environment is already active."
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "No requirements.txt found. If you have dependencies, ensure the file is present."
fi

# Start a new interactive shell with the environment activated
echo "Launching a subshell with the virtual environment activated..."
bash --rcfile <(cat << EOF
# Customize the prompt
export PS1="(pysoma) \$PS1"

# Activate the virtual environment
source "$ENV_NAME/bin/activate"

# Create an alias to run main.py
alias $ALIAS_NAME="python $MAIN_PY_PATH"
EOF
)

# This subshell will have a custom prompt and an alias set up.
