from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Company, Device, Employee
from datetime import datetime


class CompanySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Company
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = Company(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Employee
        fields = "__all__"

    def create(self, validated_data):
        employee = Employee(**validated_data)
        employee.save()
        return employee

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance

    # def delete(self, instance):
    #     return super().delete(instance)


class DeviceSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Device
        fields = "__all__"

    def create(self, validated_data):
        device = Device(**validated_data)
        if device.checked_out:
            device.checked_out_date = datetime.now()
        if device.checked_in:
            device.checked_in_date = datetime.now()

        device.save()
        return device

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.serial_number = validated_data.get(
            "serial_number", instance.serial_number
        )
        instance.checked_out = validated_data.get("checked_out", instance.checked_out)
        instance.checked_out_to = validated_data.get(
            "checked_out_to", instance.checked_out_to
        )
        instance.checked_in = validated_data.get("checked_in", instance.checked_in)
        instance.condition = validated_data.get("condition", instance.condition)
        if instance.checked_out:
            instance.checked_out_date = datetime.now()
        if instance.checked_in:
            instance.checked_in_date = datetime.now()
        instance.save()
        return instance

    def delete(self, instance):
        return super().delete(instance)

    def get_checked_out_to(self, instance):
        if instance.checked_out_to:
            return instance.checked_out_to.name
        return None

    def get_checked_out_date(self, instance):
        if instance.checked_out_date:
            return instance.checked_out_date.strftime("%Y-%m-%d %H:%M:%S")
        return None
