from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_note_lists, name='get_note_lists'),
    path('add/', views.add_note_list, name='add_note_list'),
    path('<int:note_list_id>/', views.get_note_list, name='get_note_list'),
    path('<int:note_list_id>/delete/', views.delete_note_list, name='delete_note_list'),
    path('<int:note_list_id>/notes/add/', views.add_note, name='add_note'),
    path('<int:note_list_id>/notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('<int:note_list_id>/generate-report/', views.generate_report, name='generate_report'),
]
