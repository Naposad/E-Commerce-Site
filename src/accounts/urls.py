from django.urls import path, include
from .views import CustomPasswordChangeView

urlpatterns = [
    path('', include('allauth.urls')),  # Allauth URL patterns
    path('password/change/', CustomPasswordChangeView.as_view(), name='password_change'),
]
