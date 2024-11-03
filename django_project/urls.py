"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
import os
from dotenv import load_dotenv

load_dotenv()

URL_PREFIX = os.getenv('URL_PREFIX', '')

urlpatterns = [
    path(f'{URL_PREFIX}admin/', admin.site.urls),
    path(f'{URL_PREFIX}motivational-quotes/', include('motivational_quotes.urls')),
    path(f'{URL_PREFIX}note-lists/', include('note_lists.urls')),
    path(f'{URL_PREFIX}image-generator/', include('image_generator.urls')),
]
