from django.urls import path

from . import views

urlpatterns = [
    path('', views.note_lists, name='note_lists'),
]
