from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class Company(AbstractUser):
    email = models.EmailField(max_length=55, unique=True)

    def __str__(self):
        return f"{self.username} - {self.email}"

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"


class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return f"{self.name} -> {self.company}"


class Device(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    checked_out = models.BooleanField(default=False)
    checked_out_date = models.DateTimeField(null=True, blank=True)
    checked_in = models.BooleanField(default=False)
    checked_in_date = models.DateTimeField(null=True, blank=True)
    checked_out_to = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True, blank=True
    )
    condition = models.TextField(null=True, blank=True)

    def save(self):
        if self.checked_out:
            self.checked_out_date = datetime.now()
        else:
            self.checked_out_date = None
        if self.checked_in:
            self.checked_in_date = datetime.now()
        else:
            self.checked_in_date = None

        return super().save()

    def __str__(self):
        return f"{self.name} -> {self.company} -> {self.checked_out_to} -> {self.checked_out}-{self.checked_out_date} -> {self.checked_in}-{self.checked_in_date}"

    def get_checked_out_to(self):
        if self.checked_out_to:
            return self.checked_out_to.name
        return None

    def get_checked_out_date(self):
        if self.checked_out_date:
            return self.checked_out_date.strftime("%Y-%m-%d %H:%M:%S")
        return None

    def get_checked_in_date(self):
        if self.checked_in_date:
            return self.checked_in_date.strftime("%Y-%m-%d %H:%M:%S")
        return None
