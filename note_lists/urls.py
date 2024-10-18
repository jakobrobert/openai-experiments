from django.urls import path

from . import views

urlpatterns = [
    # TODO Maybe rename urls & names for consistency, e.g. get_note_lists, also note_list_id instead of pk to be explicit
    path('', views.get_note_lists, name='get_note_lists'),
    path('add/', views.add_note_list, name='add_note_list'),
    path('<int:note_list_id>/', views.get_note_list, name='get_note_list'),
    path('<int:note_list_id>/add/', views.add_note, name='add_note'),
    path('notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),
]
