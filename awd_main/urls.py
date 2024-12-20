"""
URL configuration for awd_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path("dataentry/", include('dataentry.urls')),
    path('emails/', include('emails.urls')),
    path("celery-test/", views.celery_test),
    path('image-comression/', include("image_compression.urls")),
    path('web-scraping/', include("stockanalysis.urls")),
    path('qr/', include("qrcode_app.urls")),


    # Registration and Login URLs.
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('accounts/', include('allauth.urls')),  # Add this line

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
