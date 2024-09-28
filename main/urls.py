from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate-quote/', views.generate_quote, name='generate_quote'),
]
