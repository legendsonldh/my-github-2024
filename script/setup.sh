#!/bin/bash

# Display warning and prompt user for confirmation
echo "Warning: This script may overwrite some existing configurations. Do you want to continue? (y/n)"
read -r response
if [[ "$response" != "y" && "$response" != "Y" ]]; then
    echo "Setup aborted by user."
    exit 1
fi

# Update package list and install necessary packages
apt update && apt install -y python3.12 python3-pip nginx certbot python3-certbot-nginx python3-gunicorn python3-virtualenv || { echo "Failed to install packages"; exit 1; }

# Create and navigate to the web directory
mkdir -p /var/www || { echo "Failed to create directory"; exit 1; }
cd /var/www

# Clone the repository
git clone https://github.com/WCY-dt/my-github-2024.git || { echo "Failed to clone repository"; exit 1; }
cd my-github-2024

# Set environment variables
echo "CLIENT_ID=YOUR_CLIENT_ID" > .env
echo "CLIENT_SECRET=YOUR_CLIENT_SECRET" >> .env

# Replace placeholder URL with actual URL
sed -i 's/2024.ch3nyang.top/YOUR_URL/g' my-github-2024

# Set up virtual environment and install dependencies
virtualenv venv --python=python3.12 || { echo "Failed to create virtual environment"; exit 1; }
source venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }
pip3 install -r requirements.txt || { echo "Failed to install dependencies"; exit 1; }
pip3 install gunicorn || { echo "Failed to install Gunicorn"; exit 1; }

# Copy service file and start the service
cp my-github-2024.service /etc/systemd/system
systemctl daemon-reload || { echo "Failed to reload daemon"; exit 1; }
systemctl start my-github-2024 || { echo "Failed to start service"; exit 1; }
systemctl enable my-github-2024 || { echo "Failed to enable service"; exit 1; }

# Obtain SSL certificate
certbot --nginx -d YOUR_URL || { echo "Failed to obtain SSL certificate"; exit 1; }
certbot renew --dry-run || { echo "Failed to renew SSL certificate"; exit 1; }

# Configure nginx
cp my-github-2024 /etc/nginx/sites-available
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/my-github-2024 /etc/nginx/sites-enabled
nginx -t || { echo "Failed to test nginx configuration"; exit 1; }
systemctl restart nginx || { echo "Failed to restart nginx"; exit 1; }
nginx -s reload || { echo "Failed to reload nginx"; exit 1; }

echo "Setup completed successfully."