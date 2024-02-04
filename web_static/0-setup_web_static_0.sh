#!/usr/bin/env bash
# Bash script to set up web servers for deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    apt-get update
    apt-get install -y nginx
fi

# Create necessary directories if they don't exist
mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file
echo -e "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>" > /data/web_static/releases/test/index.html

# Create symbolic link
rm -rf /data/web_static/current
ln -sf /data/web_static/releases/test /data/web_static/current

# Set ownership recursively
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
sed -i '/^\s*location \/hbnb_static/ {s/^/#/}' /etc/nginx/sites-available/default
echo -e "\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n" >> /etc/nginx/sites-available/default

# Restart Nginx
service nginx restart
