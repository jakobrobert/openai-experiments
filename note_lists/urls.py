from django.urls import path

from . import views

urlpatterns = [
    path('', views.note_lists, name='note_lists'),
    path('add/', views.add_note_list, name='add_note_list'),
    path('<int:pk>/', views.note_list, name='note_list'),
    path('<int:pk>/add/', views.add_note, name='add_note'),
]
