# Next Generation Wealth Pro

A Django-based wealth management platform offering financial services, appointment scheduling, and resource access.

## Features

- **Home Page**: Information sections with slider images
- **Team Profile**: Display financial advisors' details
- **Services**: Financial service offerings
- **Appointment Scheduling**: Client appointment booking system with integration to email notification
- **Contact Form**: Client inquiry submission system
- **Video Resources**: Financial education videos (both embedded and directly hosted)

## Technology Stack

- **Backend**: Django 5.1.4
- **Database**: SQLite (default)
- **Frontend**: HTML, CSS, Bootstrap 4.5.2
- **Icons**: Font Awesome
- **Media Handling**: Django built-in media handling for images and videos
- **Deployment**: Azure Web App

## Project Structure

- `main/`: Core application with models, views, and templates
- `wealthpro/`: Django project configurations
- `media/`: Uploaded files (images, videos)
- `productionfiles/`: Static files for production
- `manage.py`: Django management script

## Models

The application includes several models:
- `Team`: Financial advisor profiles
- `ServicesSection`: Financial service offerings
- `HomeInfoSection` & `HomeSliderImage`: Home page content
- `Videos` & `VideoDirect`: Educational resources
- `Appointment`: Client appointment scheduling
- `Contactus`: Client inquiries
- `BusinessContact`: Company contact information

## Setup and Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser (for admin access):
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000`

## Production Deployment

The application is configured to run on Azure with the following settings:
- Production URL: nextgenerationwealthpro.com
- Static files served with WhiteNoise

## Administration

Access the admin panel at `/admin` to manage:
- Team members
- Service offerings
- Appointment requests
- Client inquiries
- Videos and resources
- Home page content

## License

All rights reserved. This codebase is proprietary and confidential.

## Contact

For more information, contact the development team at krishna.dhakal03@gmail.com. 