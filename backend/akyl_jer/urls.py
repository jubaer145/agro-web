"""
URL configuration for akyl_jer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from core.views import health, api_root, dashboard_summary, DistrictViewSet, FarmViewSet, EventViewSet

# Create router for DRF viewsets
router = DefaultRouter()
router.register(r'districts', DistrictViewSet, basename='district')
router.register(r'farms', FarmViewSet, basename='farm')
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path("", api_root, name="api-root"),
    path("admin/", admin.site.urls),
    path("api/health/", health, name="health"),
    path("api/dashboard/summary/", dashboard_summary, name="dashboard-summary"),
    path("api/", include(router.urls)),
]
