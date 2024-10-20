from django.urls import path

from . import views

urlpatterns = [
    path('', views.motivational_quotes, name='motivational_quotes'),
    path('generate-quote/', views.generate_quote, name='generate_quote'),
]
