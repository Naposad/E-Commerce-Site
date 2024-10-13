"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from mobile.urls import router as mobile_router



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('siteweb.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/', include('mobile.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),  # login, logout, password reset, etc.
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
