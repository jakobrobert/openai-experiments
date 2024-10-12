from django.urls import path

from . import views

urlpatterns = [
    path('', views.note_lists, name='note_lists'),
    path('add/', views.add_note_list, name='add_note_list'),
    path('note-list/<int:pk>/', views.note_list, name='note_list'),
    path('<int:note_list_id>/add/', views.add_note, name='add_note'),
]
