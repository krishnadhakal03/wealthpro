# WealthPro Production Deployment Guide

This guide outlines the steps required to deploy the WealthPro application to a production environment.

## Prerequisites

- Python 3.9+ installed
- PostgreSQL database server
- Web server (Nginx or Apache)
- WSGI server (Gunicorn or uWSGI)
- SSL certificate for HTTPS

## Deployment Steps

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/wealthpro.git
cd wealthpro
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root with the following variables:

```
DEBUG=False
SECRET_KEY=your_secure_random_key
ALLOWED_HOSTS=yoursite.com,www.yoursite.com

# Database configuration
DATABASE_URL=postgres://user:password@localhost:5432/wealthpro

# Email settings - these will be overridden by SiteSettings once configured
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your_email@gmail.com
CONTACT_EMAIL=your_contact_email@gmail.com

# Security settings
CSRF_TRUSTED_ORIGINS=https://yoursite.com,https://www.yoursite.com
```

### 4. Set Up PostgreSQL Database

```bash
sudo -u postgres psql
CREATE DATABASE wealthpro;
CREATE USER wealthpro_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE wealthpro TO wealthpro_user;
\q
```

### 5. Run Migrations and Create Superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Collect Static Files

```bash
python manage.py collectstatic
```

### 7. Configure WSGI Server (Gunicorn Example)

Create a systemd service file: `/etc/systemd/system/wealthpro.service`

```ini
[Unit]
Description=WealthPro Gunicorn Service
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/wealthpro
ExecStart=/path/to/wealthpro/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 wealthpro.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Start and enable the service:

```bash
sudo systemctl start wealthpro
sudo systemctl enable wealthpro
```

### 8. Configure Web Server (Nginx Example)

Create a site configuration: `/etc/nginx/sites-available/wealthpro`

```nginx
server {
    listen 80;
    server_name yoursite.com www.yoursite.com;
    
    # Redirect to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yoursite.com www.yoursite.com;
    
    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    
    # Static files
    location /static/ {
        alias /path/to/wealthpro/productionfiles/;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }
    
    # Media files
    location /media/ {
        alias /path/to/wealthpro/media/;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/wealthpro /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## Configuring Database-Driven Settings

After deployment, you'll need to configure the application's settings through the admin interface:

1. Visit `https://yoursite.com/admin/` and log in with the superuser account
2. Navigate to "Site Settings"
3. Configure the following settings:
   - Website Identity (site name, tagline, logo)
   - Contact Information
   - Email Settings (SMTP configuration)
   - Social Media Links
   - Business Hours
   - Security Settings
   - SEO Settings

The settings will be automatically applied and cached for performance.

## Maintenance Tasks

### 1. Database Backups

Set up automatic daily backups:

```bash
# Example cron job for daily backups at 2 AM
0 2 * * * pg_dump -U wealthpro_user wealthpro > /path/to/backups/wealthpro_$(date +\%Y\%m\%d).sql
```

### 2. Log Rotation

Configure log rotation for application logs:

```bash
# /etc/logrotate.d/wealthpro
/path/to/wealthpro/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
}
```

### 3. SSL Certificate Renewal

If using Let's Encrypt, set up auto-renewal:

```bash
# Automatic renewal with certbot
sudo certbot renew --post-hook "systemctl reload nginx"
```

## Updating the Application

To update the application:

```bash
cd /path/to/wealthpro
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart wealthpro
```

## Troubleshooting

### Check Application Logs

```bash
sudo journalctl -u wealthpro.service
```

### Check Nginx Logs

```bash
sudo tail -f /var/log/nginx/error.log
```

### Verify Settings

If having issues with the database-driven settings:

1. Log into the admin panel
2. Navigate to Site Settings
3. Use the "Refresh settings cache" action
4. Restart the application if needed

### Common Issues

- **500 Internal Server Error**: Check application logs for Python errors
- **Static Files Not Found**: Verify the STATIC_ROOT and MEDIA_ROOT paths
- **Email Not Working**: Check the email settings in the admin panel
- **Database Connection Issues**: Verify the DATABASE_URL in .env file

## Security Considerations

- Keep the SECRET_KEY secure and unique
- Regularly update dependencies
- Enable security settings in the admin panel
- Configure firewall rules
- Set up regular backups
- Monitor server logs for suspicious activity 