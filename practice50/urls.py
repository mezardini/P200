from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('dini/', admin.site.urls),
    path('', include('questions.urls')),
]
