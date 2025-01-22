#!/usr/bin/env bash
# Sets up web servers for web_static deployment by installing nginx and creating required directories

# Exit on error
set -e

# Function to create ubuntu user if it doesn't exist
create_ubuntu_user() {
    if ! id "ubuntu" &>/dev/null; then
        useradd -m -s /bin/bash ubuntu
    fi
    if ! getent group "ubuntu" &>/dev/null; then
        groupadd ubuntu
    fi
}

# Function to handle nginx restart
handle_nginx() {
    # Stop any process using port 80
    if lsof -Pi :80 -sTCP:LISTEN -t >/dev/null ; then
        fuser -k 80/tcp
    fi
    
    # Stop nginx if it's running
    systemctl stop nginx
    
    # Small delay to ensure port is released
    sleep 2
    
    # Start nginx
    systemctl start nginx
}

# Install nginx if not already installed
if ! command -v nginx &> /dev/null; then
    apt-get update
    apt-get -y install nginx
fi

# Create required directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create test HTML file
cat > /data/web_static/releases/test/index.html << EOF
<html>
  <head>
  </head>
  <body>
    ALX
  </body>
</html>
EOF

# Create/recreate symbolic link
rm -f /data/web_static/current
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Create ubuntu user and group if they don't exist
create_ubuntu_user

# Set ownership to ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# Configure nginx
nginx_config="/etc/nginx/sites-available/default"
if ! grep -q "location /hbnb_static" $nginx_config; then
    # Backup original config
    cp $nginx_config "${nginx_config}.bak"
    
    # Add location block for /hbnb_static
    sed -i '/server_name _;/a \    location /hbnb_static/ {\n        alias /data/web_static/current/;\n    }' $nginx_config
fi

# Test nginx configuration
nginx -t

# Handle nginx restart with proper port management
handle_nginx

echo "Setup completed successfully!"
exit 0
