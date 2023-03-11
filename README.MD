# Django User Management and Machine Learning Example with Docker and UnitTest
This is a RESTful API project built with Django and Django REST framework. The API provides various endpoints for user authentication, user management, and a machine learning model predictor.


# API Endpoints
The following endpoints are available:

# User Authentication
- POST /api/v1/register: Creates a new user account.
- POST /api/v1/login: Logs in a user and returns an access token and refresh token.
- POST /api/v1/logout: Logs out a user.


# User Management
- GET /api/v1/user: Returns the details of the authenticated user.
- PUT /api/v1/profile-update/<str:email>: Updates the authenticated user's profile.
- DELETE /api/v1/delete-user/<str:email>: Deletes the specified user.
- GET /api/v1/users-list: Returns a list of all users.
- POST /api/v1/add-user: Adds a new user.


# Machine Learning Model Predictor
- POST /api/v1/predictor: Makes a prediction using a machine learning model.

# Getting Started
### Prerequisites
- Python 3.x
- Django
- Django REST framework


# Installation
- Clone the repository:

``git clone https://github.com/projectslist/DjangoUserManagement.git
cd project
``

- Install the dependencies
- ``pip install -r requirements.txt
``
- Run the Docker
- ``docker-compose build``
- ``docker-compose up``


# Usage
To use the API, send requests to the desired endpoint using a RESTful client. See the API endpoints section above for details on each endpoint and its expected parameters.

# License
This project is licensed under the MIT License. See the LICENSE file for details.