# AWS EC2 Deployment Guide

This guide provides step-by-step instructions for deploying the Next Generation Wealth Pro application on AWS EC2.

## Prerequisites

- AWS Account
- SSH client (Terminal for Mac/Linux, PuTTY for Windows)
- Application code in a Git repository

## Step 1: Create an EC2 Instance

1. Sign in to the AWS Management Console
2. Navigate to EC2 Dashboard
3. Click "Launch Instance"
4. Choose Amazon Linux 2023 AMI
5. Select t2.micro (Free tier eligible) or larger as needed
6. Configure instance details (default settings are fine for basic setup)
7. Add storage (default 8GB is sufficient for basic setup)
8. Add tags (optional)
9. Configure Security Group:
   - Allow SSH (port 22) from your IP
   - Allow HTTP (port 80) from anywhere
   - Allow HTTPS (port 443) from anywhere
10. Review and launch
11. Create or select an existing key pair
12. Download the key pair (.pem file) and keep it secure

## Step 2: Connect to Your EC2 Instance

```bash
# For Mac/Linux
chmod 400 your-key-pair.pem
ssh -i your-key-pair.pem ec2-user@your-ec2-instance-public-dns

# For Windows, use PuTTY with the converted .ppk file
```

## Step 3: Install Required Software

```bash
# Update system packages
sudo yum update -y

# Install Python and development tools
sudo yum install python3 python3-pip python3-devel gcc nginx git -y

# Install PostgreSQL (optional - if you want to switch from SQLite)
sudo amazon-linux-extras install postgresql14 -y
sudo yum install postgresql-devel -y

# Create a virtual environment
python3 -m venv ~/venv
source ~/venv/bin/activate
```

## Step 4: Clone and Configure the Application

```bash
# Clone your repository
git clone [YOUR_REPOSITORY_URL]
cd wealthpro

# Install dependencies
pip install -r requirements.txt

# Add gunicorn to requirements
pip install gunicorn

# Create environment-specific settings
cat > wealthpro/.env << EOL
DEBUG=False
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
ALLOWED_HOSTS=your-ec2-public-dns,your-domain-name,localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EOL
```

## Step 5: Test the Application Locally on EC2

```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Test with gunicorn
gunicorn wealthpro.wsgi:application --bind 0.0.0.0:8000
```

Visit http://your-ec2-public-dns:8000 to verify the application is running.

## Step 6: Configure Gunicorn Service

```bash
# Create a systemd service file
sudo nano /etc/systemd/system/gunicorn.service
```

Add the following content:

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/wealthpro
ExecStart=/home/ec2-user/venv/bin/gunicorn --workers 3 --bind unix:/home/ec2-user/wealthpro/wealthpro.sock wealthpro.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
# Start and enable the service
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

## Step 7: Configure Nginx as a Reverse Proxy

```bash
# Create Nginx configuration
sudo nano /etc/nginx/conf.d/wealthpro.conf
```

Add the following content:

```nginx
server {
    listen 80;
    server_name your-ec2-public-dns your-domain-name;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ec2-user/wealthpro;
    }
    
    location /media/ {
        root /home/ec2-user/wealthpro;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ec2-user/wealthpro/wealthpro.sock;
    }
}
```

```bash
# Test Nginx configuration
sudo nginx -t

# If successful, restart Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

## Step 8: Set Up HTTPS with Let's Encrypt (Optional)

```bash
# Install certbot
sudo yum install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d your-domain-name

# Auto-renewal
sudo systemctl status certbot-renew.timer
```

## Step 9: Database Migration (Optional)

If you want to use PostgreSQL instead of SQLite:

```bash
# Install PostgreSQL client
sudo yum install postgresql postgresql-devel python3-devel -y

# Create a database and user
sudo -u postgres psql

postgres=# CREATE DATABASE wealthpro;
postgres=# CREATE USER wealthproadmin WITH PASSWORD 'secure_password';
postgres=# ALTER ROLE wealthproadmin SET client_encoding TO 'utf8';
postgres=# ALTER ROLE wealthproadmin SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE wealthproadmin SET timezone TO 'UTC';
postgres=# GRANT ALL PRIVILEGES ON DATABASE wealthpro TO wealthproadmin;
postgres=# \q

# Update the .env file
sed -i 's|DATABASE_URL=sqlite:///db.sqlite3|DATABASE_URL=postgresql://wealthproadmin:secure_password@localhost:5432/wealthpro|g' wealthpro/.env

# Install psycopg2
pip install psycopg2-binary

# Migrate the database
python manage.py migrate
```

## Step 10: Continuous Deployment Setup

Create a deployment script:

```bash
nano ~/deploy.sh
```

Add the following content:

```bash
#!/bin/bash
cd ~/wealthpro
git pull
source ~/venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

Make it executable:

```bash
chmod +x ~/deploy.sh
```

## Monitoring and Maintenance

- **Logs**: Check logs with `sudo journalctl -u gunicorn` and `sudo tail -f /var/log/nginx/error.log`
- **Updates**: Regularly run `sudo yum update -y` to keep the system updated
- **Backups**: Set up regular database backups
- **Monitoring**: Consider setting up AWS CloudWatch for monitoring

## Troubleshooting

- If the application isn't accessible, check the status of gunicorn and nginx services
- Verify security group settings to ensure proper ports are open
- Check application logs for specific errors
- Ensure file permissions are correct for the application directory 