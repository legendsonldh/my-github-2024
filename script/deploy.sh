#!/bin/bash

# Navigate to the project directory
cd /var/www/my-github-2024 || { echo "Directory not found"; exit 1; }

# Find and kill the existing process
PID=$(ps -ef | grep my-github-2024.py | grep -v grep | awk '{print $2}')
if [ -n "$PID" ]; then
    kill -9 $PID || { echo "Failed to kill existing process"; exit 1; }
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
nohup python3 my-github-2024.py > ./app.log 2>&1 &
echo "Deployment completed successfully"