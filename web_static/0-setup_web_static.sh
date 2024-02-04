#!/usr/bin/env bash
# Script: 0-setup_web_static.sh
# Description: Sets up web servers for the deployment of web_static
# Author: Udeme Harrison

# Update package lists and install nginx
sudo apt-get update
sudo apt-get -y install nginx

# Allow HTTP traffic through UFW furewall
sudo ufw allow 'Nginx HTTP'

# Create directory structure for web_static
sudo mkdir -p /data/
sudo mkdir -p /data/web_static
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

# Create a simple HTML file for testing
sudo tough /data/web_static/releases/test/index.html
sudo echo "<html>
	<head>
	</head>
	<body>
		Holberton School
	</body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link to current release
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

# Change ownership of /data/ directory to user 'ubuntu' and group 'ubuntu'
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve web_static content
# Add an alias to serve /hbnb_static URL
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

# Restart nginx to apply changes
sudo service nginx restart
