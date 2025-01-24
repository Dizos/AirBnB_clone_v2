#!/usr/bin/env bash
# Sets up web servers for web_static deployment

# Install Nginx
apt-get update
apt-get -y install nginx

# Create directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create test HTML file
cat << EOF > /data/web_static/releases/test/index.html
<html>
  <head>
  </head>
  <body>
    ALX
  </body>
</html>
EOF

# Create/recreate symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
sed -i '/server_name _;/a \    location /hbnb_static/ {\n        alias /data/web_static/current/;\n    }' "$config_file"

# Restart Nginx
service nginx restart

exit 0
