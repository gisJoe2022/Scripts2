


#------Unvafified AI Generated Content


#-----What this script does
#Updates system and installs required packages.
#Configures MariaDB securely and creates a Nextcloud database/user.
#Downloads and sets up Nextcloud in /var/www/nextcloud.
#Configures Nginx for Nextcloud.
#Secures the site with Let’s Encrypt SSL.
#Sets proper permissions for Nextcloud.

#----Next Steps
#Replace yourdomain.com and StrongPassword123! with your actual domain and strong password.
#After running the script, complete Nextcloud setup via the web interface.
#Enable public link sharing in Nextcloud settings (with expiration and password options).
#######################################################################################################
#!/bin/bash
# Secure File Server Setup with Nextcloud + Nginx + SSL
# Tested on Ubuntu 22.04
#######################################################################################################

# Exit on error
set -e

# Update system
echo "Updating system..."
apt update && apt upgrade -y

# Install dependencies
echo "Installing dependencies..."
apt install -y nginx mariadb-server php-fpm php-mysql php-xml php-zip php-curl php-gd php-mbstring unzip certbot python3-certbot-nginx

# Configure MariaDB
echo "Configuring MariaDB..."
mysql_secure_installation <<EOF
n
Y
Y
Y
Y
EOF

# Create Nextcloud DB and user
DB_NAME="nextcloud"
DB_USER="nextclouduser"
DB_PASS="StrongPassword123!"
mysql -u root -p <<MYSQL_SCRIPT
CREATE DATABASE $DB_NAME;
CREATE USER '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

# Download Nextcloud
echo "Downloading Nextcloud..."
cd /var/www/
wget https://download.nextcloud.com/server/releases/nextcloud-28.0.1.zip
unzip nextcloud-28.0.1.zip
chown -R www-data:www-data nextcloud

# Configure Nginx
echo "Configuring Nginx..."
cat > /etc/nginx/sites-available/nextcloud <<EOL
server {
    listen 80;
    server_name yourdomain.com;

    root /var/www/nextcloud;
    index index.php index.html;

    location / {
        try_files \$uri \$uri/ /index.php\$is_args\$args;
    }

    location ~ \.php\$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    }

    location ~ /\.ht {
        deny all;
    }
}
EOL

ln -s /etc/nginx/sites-available/nextcloud /etc/nginx/sites-enabled/
nginx -t && systemctl restart nginx

# SSL with Let's Encrypt
echo "Setting up SSL..."
certbot --nginx -d yourdomain.com --non-interactive --agree-tos -m admin@yourdomain.com

echo "Nextcloud setup complete!"
echo "Access your server at: https://yourdomain.com"