from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Company, Employee, Device
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from .serializers import (
    CompanySerializer,
    EmployeeSerializer,
    DeviceSerializer,
)
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import (
    BasicAuthentication,
    TokenAuthentication,
)
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


# Handle the view for signup
# * POST /signup/ -> (POST){
#    "username": "test",
#   "email": "test@test",
#  "password": "test"
# }
@api_view(["POST"])
def signup(request):
    if request.method == "POST":
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Handle the view for login
# * POST /login/ ->  (POST){
#    "username": "test",
#   "email": "test@test",
#  "password": "test"
# }
@api_view(["POST"])
def login(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")

        user = None
        if "@" in username:
            try:
                user = Company.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "company": CompanySerializer(user).data},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


# Handle the view for the Company model
# * GET /company/ ->  company (GET)
# * GET /company/employees/ ->  company-employees (GET)
# * GET /company/devices/ ->  company-devices (GET)
# * POST /company/create-employee/ ->  company-create-employee (POST)
# * POST /company/create-device/ ->  company-create-device (POST)
# * POST /company/update-employee/ ->  company-update-employee (POST)
# * POST /company/delete-employee/ ->  company-delete-employee (POST)
# * POST /company/delete-device/ ->  company-delete-device (POST)


@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class CompanyViewSet(viewsets.ModelViewSet, APIView):
    serializer_class = CompanySerializer
    # authentication_classes = [BasicAuthentication, TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    """
    get the details of the company 
    * GET /company/ ->  company (GET)
    
    """

    @authentication_classes([TokenAuthentication, BasicAuthentication])
    def details(self, request):
        company = get_object_or_404(Company, email=request.user.email)
        company_serializer = CompanySerializer(company, many=False)
        employees = Employee.objects.filter(company=company)
        employee_serializer = EmployeeSerializer(employees, many=True)
        devices = Device.objects.filter(company=company)
        devices_serializer = DeviceSerializer(devices, many=True)
        return Response(
            {
                "company": company_serializer.data,
                "employees": employee_serializer.data,
                "devices": devices_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    """
    get the employees of the company
    * GET /company/employees ->  company (GET)
    
    """

    @authentication_classes([BasicAuthentication, TokenAuthentication])
    def retrieve_employees(self, request):
        company = get_object_or_404(Company, email=request.user.email)

        serializer = CompanySerializer(company, many=False)
        queryset = Employee.objects.all().filter(company=company)
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(
            {"company": CompanySerializer(company).data, "employees": serializer.data}
        )

    """
        get the devices of the company
        * GET /company/devices ->  company (GET)
        
    """

    @authentication_classes([BasicAuthentication, TokenAuthentication])
    def retrieve_devices(self, request):
        company = get_object_or_404(Company, email=request.user.email)

        serializer = CompanySerializer(company, many=False)
        queryset = Device.objects.all().filter(company=company)
        serializer = DeviceSerializer(queryset, many=True)
        return Response({"devices": serializer.data})

    """
    create an employee for the company
    * POST /company/create-employee/ ->  company-create-employee (POST)
        {
            "name": "John Doe", // required
            "email": "John@mail.com" // required
        }
    """

    @authentication_classes([BasicAuthentication, TokenAuthentication])
    def create_employee(self, request):
        if request.method == "POST":
            company = get_object_or_404(Company, email=request.user.email)
            name = request.data["name"]
            email = request.data["email"]
            if Employee.objects.filter(email=email).exists():
                return Response(
                    {"error": "Employee with this email already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = EmployeeSerializer(
                data={"name": name, "email": email, "company": company.id}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"data": serializer.data}, status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    create device for the company
    * POST /company/create-device/ ->  company-create-device (POST)
        {
            "name": "iphone",
            "description": "iphone 15", // optional
            "serial_number": 123,   // optional
            "checked_out": 0,   // optional
            "checked_out_to": ""   // optional
            "condition": "",   // optional
            "checked_out": false,   // optional
            "checked_out_date": null,   // optional
            "checked_in": false,   // optional
            "checked_in_date": null,   // optional
            "company": 8,   // optional
            "checked_out_to": null   // optional
        }

requirments
    """

    @authentication_classes([BasicAuthentication, TokenAuthentication])
    def create_device(self, request):
        if request.method == "POST":
            company = get_object_or_404(Company, email=request.user.email)
            if "name" not in request.data:
                return Response(
                    {"error": "Name is required"}, status=status.HTTP_400_BAD_REQUEST
                )
            name = request.data["name"]
            description = request.data.get("description", "")
            serial_number = request.data.get("serial_number", "")
            checked_out = request.data.get("checked_out", False)
            checked_out_to = request.data.get("employee_id", "")
            condition = request.data.get("condition", "")


            data = {
                "name": name,
                "description": description,
                "serial_number": serial_number,
                "checked_out": checked_out,
                "checked_out_to": checked_out_to,
                "company": company.id,
                "condition": condition,
            }
            serializer = DeviceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": "Device added",
                        "data": serializer.data,
                    },
                    status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    update employee of the company by primary key (id)
    * POST /company/update-employee/ ->  company-update-employee (POST)
        {
            "name": "Satoshi Nakamoto", // optional
            "email": "sat@mail.com", // optional
        }
    """

    @authentication_classes([BasicAuthentication, TokenAuthentication])
    def update_employee(self, request):
        employee = Employee.objects.get(pk=request.data["id"])
        name = request.data.get("name", employee.name)
        email = request.data.get("email", employee.email)
        serializer = EmployeeSerializer(employee, data={"name": name, "email": email})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "Updated", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    update device by primary key
    * POST /company/update-device/ ->  company-update-device (POST)
        {
            "id": 7,
            "name": "iphone 15",
            "description": "iphone 15",
            "serial": 123,
            "checked_out": 0,
            "checked_out_to": ""
        }
    """

    def update_device(self, request):
        company = get_object_or_404(Company, email=request.user.email)
        device = get_object_or_404(Device, pk=request.data["id"])
        name = request.data["name"]
        description = request.data.get("description", "")
        serial_number = request.data.get("serial_number", "")
        checked_out = request.data.get("checked_out", False)
        checked_out_to = request.data.get("employee_id", "")
        checked_in = request.data.get("checked_in", False)
        condition = request.data.get("condition", "")
        data = {
            "name": name,
            "description": description,
            "serial_number": serial_number,
            "checked_out": checked_out,
            "checked_out_to": checked_out_to,
            "company": company.id,
            "condition": condition,
            "checked_in": checked_in,
        }
        serializer = DeviceSerializer(device, data=data)
        request.data["company"] = company.id
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "Updated", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    delete employee by primary key
    * POST /company/delete-employee/ ->  company-delete-employee (POST)
        {
            "id": 1
        }
    """

    def delete_employee(self, request):
        employee = Employee.objects.get(pk=request.data["id"])
        emp = EmployeeSerializer(employee).data
        employee.delete()
        return Response(
            {"employee": emp, "status": "Deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )

    """
    delete device by primary key
    * POST /company/delete-device/ ->  company-delete-device (POST)
        {
            "id": 7
        }
    """

    def delete_device(self, request):
        device = Device.objects.get(pk=request.data["id"])
        # serializer = DeviceSerializer(device).delete()
        device.delete()
        return Response(
            {
                "status": "Deleted",
                "device": DeviceSerializer(device, many=False).data,
            },
            status=status.HTTP_204_NO_CONTENT,
        )
    

