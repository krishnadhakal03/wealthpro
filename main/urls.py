from django.conf import settings
from django.conf.urls.static import static
from django.urls import  path
from . import views
urlpatterns = [
    path('', views.home, name='home'),

path('team/', views.team, name='team'),
path('services/', views.services, name='services'),

path('appointment/', views.appointment, name='appointment'),
path('contact/', views.contact, name='contact'),
path('videos/', views.videos, name='videos'),

# Insurance Calculator
path('insurance-calculator/', views.insurance_calculator, name='insurance_calculator'),

# Zoom API endpoints
path('api/zoom-slots/', views.get_zoom_slots, name='get_zoom_slots'),
path('api/book-zoom-slot/', views.book_zoom_slot, name='book_zoom_slot'),
]

# In development, Django can serve media files
# In production, these should be served by the web server
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Still allow Django to serve media in production until proper web server is configured
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
