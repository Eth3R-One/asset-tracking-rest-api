from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from asset_management import views
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="API Documentation")
# router = DefaultRouter()
# router.register(r"company", views.CompanyViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("asset_management.urls")),
    # path("api-documentation/", schema_view, name="api-documentation"),
    re_path(r"^$", schema_view),
]
