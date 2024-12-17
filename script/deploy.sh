#!/bin/bash

# Navigate to the project directory
cd /var/www/my-github-2024 || { echo "Directory not found"; exit 1; }

# Find and kill the existing process
PID=$(pgrep -f my-github-2024.py)
if [ -n "$PID" ]; then
  kill "$PID" || { echo "Failed to kill process $PID"; exit 1; }
fi

# Remove old log files
rm -f app.log nohup.out

# Update the codebase
git fetch origin || { echo "Failed to fetch updates"; exit 1; }
git reset --hard origin/main || { echo "Failed to reset codebase"; exit 1; }

# Activate the virtual environment and install dependencies
source venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }
pip install -r requirements.txt || { echo "Failed to install dependencies"; exit 1; }

# Start the application
nohup python3 my-github-2024.py &
echo "Deployment completed successfully"