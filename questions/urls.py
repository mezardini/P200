from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate, name='generate'),
    path('generate/', views.index, name='index'),
    path('questions/', views.questions, name="questions"),
]
