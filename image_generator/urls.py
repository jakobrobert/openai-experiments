from django.urls import path

from . import views

urlpatterns = [
    path('', views.image_generator, name='image_generator'),
    path('generate-image/', views.generate_image, name='generate_image')
]
