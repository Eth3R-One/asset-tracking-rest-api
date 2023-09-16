from django.contrib import admin
from django.urls import re_path, path
from asset_management import views
from rest_framework import routers

urlpatterns = [
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path(
        "company/",
        views.CompanyViewSet.as_view({"get": "details"}),
        name="comapany",
    ),
    path(
        "company/employees/",
        views.CompanyViewSet.as_view({"get": "retrieve_employees"}),
        name="company-employees",
    ),
    path(
        "company/devices/",
        views.CompanyViewSet.as_view({"get": "retrieve_devices"}),
        name="company-devices",
    ),
    path(
        "company/create-employee/",
        views.CompanyViewSet.as_view({"post": "create_employee"}),
        name="company-create-employee",
    ),
    path(
        "company/create-device/",
        views.CompanyViewSet.as_view({"post": "create_device"}),
        name="company-create-device",
    ),
    path(
        "company/update-employee/",
        views.CompanyViewSet.as_view({"post": "update_employee"}),
        name="company-update-employee",
    ),
    path(
        "company/update-device/",
        views.CompanyViewSet.as_view({"post": "update_device"}),
        name="company-update-device",
    ),
    path(
        "company/delete-employee/",
        views.CompanyViewSet.as_view({"post": "delete_employee"}),
        name="company-delete-employee",
    ),
    path(
        "company/delete-device/",
        views.CompanyViewSet.as_view({"post": "delete_device"}),
        name="company-delete-device",
    ),
    # path(
    #     "company/checkout-device/",
    #     views.CompanyViewSet.as_view({"post": "checkout_device"}),
    #     name="company-checkout-device",
    # ),
    # path(
    #     "company/checkin-device/",
    #     views.CompanyViewSet.as_view({"post": "checkin_device"}),
    #     name="company-checkin-device",
    # ),
]
