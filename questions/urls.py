from django.urls import path
from . import views
from .views import DashboardView

urlpatterns = [
    path('generate/', views.generate, name='generate'),
    path('', views.index, name='index'),
    path('questions/', views.questions, name="questions"),
    path('signin/', views.signin, name='signin'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('terms/', views.TandC, name='TandC'),
    path('policy/', views.policy, name='policy'),
]

