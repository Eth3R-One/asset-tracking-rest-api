# <h1 align="center">Corporate Asset Tracking API</h1>


## Overview

This Django application is designed to track corporate assets such as phones, tablets, laptops, and other equipment provided to employees. It supports multiple companies, allowing each company to manage its employees, devices, and asset assignments.

## Features

1. Company Management: Companies can register and manage their information.
2. Employee Management: Companies can add and manage their employees.
3. Device Management: Devices (e.g., phones, tablets) can be registered and tracked.
4. Asset Assignment: Assign devices to employees for a specified period.
5. Device Condition Logging: Log the condition of devices during assignment and return.

## Installation
Clone the repository:

```
git clone https://github.com/Eth3R-One/asset-tracking-rest-api.git
```


Create a virtual environment:
```
python3 -m venv env
```
Activate virtual environment:


```
source env/bin/activate
```

On Windows, use: 
```
env\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Apply database migrations:
```
python manage.py migrate
```


Create a superuser (to access the admin panel):

```
python manage.py createsuperuser
```


Run the development server:

```
python manage.py runserver
```




See the API documentation at <http://127.0.0.1:8000/>

> Note: The application is configured to use SQLite by default. To use a different database, update the DATABASES setting in settings.py.


### Default Credentials
Username:`admin`

Password:`admin`

## Usage
Access the admin panel at <http://127.0.0.1:8000/admin/> and log in with the superuser credentials to manage the application data.
Use the provided API endpoints (e.g., /api/companies/, /api/employees/) for programmatic access to the application.
API Documentation
API documentation can be found at /swagger/ when the application is running. Additionally, the provided API endpoints can be explored interactively through the Swagger UI.


## Screenshots
![Screenshot](./screenshots/1.png)
![Screenshot](./screenshots/2.png)
![Screenshot](./screenshots/3.png)
![Screenshot](./screenshots/4.png)
![Screenshot](./screenshots/5.png)

## Demo
![Demo](./screenshots/gifs/1.gif)
![Demo](./screenshots/gifs/2.gif)
![Demo](./screenshots/gifs/3.gif)

# Contributing
Contributions to this project are welcome. Feel free to open an issue or submit a pull request.

# License
This project is licensed under the MIT License.

