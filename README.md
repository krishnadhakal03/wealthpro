# WealthPro

A comprehensive wealth management and financial services web application built with Django.

## Features

- Dynamic team member profiles
- Financial services catalog
- Insurance calculator
- Video resources library
- Appointment scheduling system
- Contact and inquiry management
- Admin-configurable site settings
- Database backup functionality
- Amazon SES email integration

## Tech Stack

- Django 5.1.4
- Bootstrap 5
- SQLite (development) / MySQL (production)
- jQuery
- Font Awesome
- Gunicorn (WSGI server)
- Nginx (production)

## Installation

1. Clone the repository
```bash
git clone https://github.com/krishnadhakal03/wealthpro.git
cd wealthpro
```

2. Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create environment file
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations
```bash
python manage.py migrate
```

6. Create superuser
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

## Production Deployment

See [Production Deployment Guide](docs/production_deployment.md) for detailed instructions on deploying to production environments.

## Email Configuration

The application supports Amazon SES for reliable email delivery. See [Amazon SES Setup Guide](docs/amazon_ses_setup.md) for configuration details.

## Database Backups

WealthPro includes a built-in database backup system accessible from the admin panel. See [Database Backup Guide](docs/database_backups.md) for usage instructions.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Krishna Dhakal - krishnadhakal03@gmail.com 