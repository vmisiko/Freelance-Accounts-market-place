"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls

urlpatterns = [
    
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('', include('Home.urls' , namespace = "Home")),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('dashboard/', include('dashboard.urls')),
    path("mobile/", include("MpesaApp.urls")),
    path("unlocks/", include("UnlocksApp.urls")),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
