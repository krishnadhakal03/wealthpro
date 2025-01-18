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

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)