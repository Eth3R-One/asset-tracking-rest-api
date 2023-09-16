from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from asset_management import views

# router = DefaultRouter()
# router.register(r"company", views.CompanyViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("asset_management.urls")),
]
