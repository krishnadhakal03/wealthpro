# Database Backup Guide

WealthPro includes a built-in database backup feature that allows administrators to create and download database backups directly from the Django admin interface. This guide explains how to use this functionality.

## Overview

The database backup feature allows you to:

1. Create a complete SQLite database backup with a single click
2. Download the backup file to your local system
3. Store backups in your preferred location for safekeeping

This is especially useful when running in cloud environments like AWS EC2, where you may want to periodically create backups without direct server access.

## Using the Database Backup Feature

### Prerequisites

- You must have superuser (admin) access to the Django admin interface
- Your system should have sufficient memory to process the database file

### Creating and Downloading a Backup

1. Log in to the Django admin interface at `https://your-site.com/admin/`
2. Navigate to **Main** > **Site Settings**
3. Select the site settings entry by checking the box to the left of it
4. From the **Action** dropdown at the top, select "Download database backup"
5. Click the "Go" button to execute the action
6. Your browser will automatically download the database file
7. The file will be named `wealthpro_db_backup_YYYYMMDD_HHMMSS.sqlite` with the current timestamp

![Database Backup Process](../documentation/images/db_backup_process.png)

### Security Considerations

- The database file contains all your application data, including sensitive information
- Store downloaded backups securely
- Consider encrypting backups if they contain highly sensitive information
- Never share database backups with unauthorized users

## Restoring from Backup

To restore your site from a backup:

1. Stop the Django application
2. Replace the SQLite database file with your backup file
3. Restart the application

For SQLite databases in production, you can restore as follows:

```bash
# SSH into your EC2 instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Stop the application service
sudo systemctl stop wealthpro

# Navigate to the database directory
cd /path/to/wealthpro

# Backup the current database just in case
cp db.sqlite3 db.sqlite3.before_restore

# Copy your backup file to replace the current database
cp /path/to/your/wealthpro_db_backup_YYYYMMDD_HHMMSS.sqlite db.sqlite3

# Restart the application
sudo systemctl start wealthpro
```

## Automated Backups

For production environments, it's recommended to set up automated backups in addition to the manual backup feature.

Here's an example of a cron job that creates daily backups:

```bash
# Create a backup script
cat > /path/to/backup-script.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
DB_PATH="/path/to/wealthpro/db.sqlite3"
BACKUP_DIR="/path/to/backups"
cp $DB_PATH $BACKUP_DIR/wealthpro_db_$DATE.sqlite
# Keep only the last 7 backups
ls -tp $BACKUP_DIR/wealthpro_db_*.sqlite | grep -v '/$' | tail -n +8 | xargs -I {} rm -- {}
EOF

# Make it executable
chmod +x /path/to/backup-script.sh

# Add to crontab to run daily at 2 AM
(crontab -l 2>/dev/null; echo "0 2 * * * /path/to/backup-script.sh") | crontab -
```

## Best Practices

1. **Regular Backups**: Create backups before making significant changes to your site
2. **Backup Rotation**: Don't keep all backups forever - implement a rotation policy
3. **Test Restores**: Periodically test the restore process to ensure backups are valid
4. **Offsite Storage**: Copy important backups to a different location or cloud storage
5. **Documentation**: Keep a log of when backups were made and what changes were occurring

## Limitations

- For very large databases, the browser download may time out
- This feature is optimized for SQLite databases
- In high-traffic sites, consider performing backups during low-usage periods

## Troubleshooting

If you encounter issues with the backup process:

1. Check that your user has superuser privileges
2. Verify that the database file is accessible to the Django application
3. For large databases, you may need to increase your server timeout settings
4. If download fails, use the server-side backup script approach instead 