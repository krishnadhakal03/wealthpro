# Local Development Guide

This guide provides instructions for setting up and running the Next Generation Wealth Pro application locally for development and testing.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

## Initial Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd wealthpro
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file:
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit with your actual settings
   # On Windows
   notepad .env
   
   # On macOS/Linux
   nano .env
   ```

5. Update the `.env` file with your development settings, including:
   - Email credentials for testing email functionality
   - Secret key (for development only)
   - Debug mode (set to True)

6. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser to access the admin panel:
   ```bash
   python manage.py createsuperuser
   ```

8. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

## Running the Development Server

Start the Django development server:
```bash
python manage.py runserver
```

Access the site at http://127.0.0.1:8000/

Access the admin panel at http://127.0.0.1:8000/admin/

## Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes to the code

3. Test your changes locally with:
   ```bash
   python manage.py test
   ```

4. Run the development server to see your changes:
   ```bash
   python manage.py runserver
   ```

5. Add and commit your changes:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

6. Push your changes and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## Common Development Tasks

### Working with Models

1. Make changes to models in `main/models.py`
2. Create migrations:
   ```bash
   python manage.py makemigrations
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

### Static Files

If you add or modify static files (CSS, JavaScript, images):
```bash
python manage.py collectstatic
```

### Testing Email Functionality

For testing email functionality without sending real emails, you can use Django's console email backend by adding to your `.env` file:
```
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Database Reset

If you need to start with a fresh database:
```bash
# Delete the db.sqlite3 file
rm db.sqlite3

# Re-run migrations
python manage.py migrate

# Create a new superuser
python manage.py createsuperuser
```

## Troubleshooting

### Migration Issues

If you encounter migration errors:
```bash
python manage.py migrate --fake-initial
```

### Static Files Not Updating

Clear your browser cache or use incognito mode to view updated static files.

### Package Conflicts

If you encounter package conflicts, try updating your virtual environment:
```bash
pip install --upgrade -r requirements.txt
```

### Debug Mode

Ensure DEBUG=True is set in your .env file during local development to see detailed error messages. 