from django.urls import path
from . import views
from .views import DashboardView

urlpatterns = [
    path('generate/', views.generate, name='generate'),
    path('', views.index, name='index'),
    path('questions/', views.questions, name="questions"),
    path('signin/', views.signin, name='signin'),
    path('answer/<int:question_id>/', views.answer, name='answer'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('terms/', views.TandC, name='TandC'),
    path('policy/', views.policy, name='policy'),
    path('signout/', views.signout, name='signout'),
]

