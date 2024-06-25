from .views import about_site
from django.urls import path

app_name = 'about'
urlpatterns = [
    path('about_site/', about_site, name='about_site'),
]