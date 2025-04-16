# Project Management API Documentation

## Docker Setup

Install Docker Desktop(on the docker desktop application) and run the following command to start the application:

```sh
docker-compose up --build
```

Or in detached mode( use this -f docker-compose.yml file name)

```sh
docker compose up -d
```

If not using Docker, use Python 3.13 and configure PostgreSQL correctly:

```add it to .env
POSTGRES_HOST=localhost
POSTGRES_PORT=5433

include postgres data in .env

do 
pipenv install

python manage.py migrate

python manage.py runserver

```

---

## Authentication Endpoints

### Register a new user
**POST** `/register/`

```json
{
    "username": "",
    "email": "",
    "password": "",
    "password_confirm": ""
}
```

Upon successful registration, an activation link is sent via email.

### Activate account
**GET** `/activate/<token>/`

### Request password reset
**POST** `accounts/password-reset/request/`

```json
{
    "email":""
}
```

```json
{
    "status": "success",
    "message": "OTP has been sent to your email.",
    "token": "......."
}```

Upon request, a token is returned, and an OTP is sent via email.

> **Issue:** This endpoint allows checking if an email is registered.

### Verify password reset
**POST** `accounts/password-reset/verify/`

```json
{
    "token": "",
    "otp": "",
    "new_password": "",
    "confirm_password": ""
}
```

> **Issue:** The old password can be reused.

---

## Authentication and Token Management

> CORS is not implemented. Use Django Rest Framework browser client for authentication.

### Obtain access token(login)
**POST** `/api/token/`

{
    "refresh": "",
    "access": ""
}

### Refresh access token
**POST** `/api/token/refresh/`

---

## Project Endpoints

### List all projects
**GET** `api/projects/`

### Create a new project
**POST** `api/projects/`

### Get project details with tasks
**GET** `api/projects/{id}/`

### Update a project
**PUT** `api/projects/{id}/`

### Partially update a project
**PATCH** `api/projects/{id}/`

### Delete a project
**DELETE** `api/projects/{id}/`

### List all tasks for a project
**GET** `api/projects/{id}/tasks/`

---

## Task Endpoints

### List all tasks
**GET** `api/tasks/`

### Create a standalone task
**POST** `api/tasks/`

### Get task details with comments
**GET** `api/tasks/{id}/`

### Update a task
**PUT** `api/tasks/{id}/`

### Delete a task
**DELETE** `api/tasks/{id}/`

### Partially update a task (e.g., change status)
**PATCH** `api/tasks/{id}/`

### List all comments for a task
**GET** `api/tasks/{id}/comments/`

### Add a comment to a task
**POST** `api/tasks/{id}/comment/`

---

## Status Management

### List all statuses
**GET** `api/statuses/`

### Create a new status
**POST** `api/statuses/`

---

## User Assignment

### Assign users to a task
**POST** `api/tasks/{task_id}/assign/`

```json
{
    "profile_ids": [id, id...]
}
```

### Unassign users from a task
**POST** `api/tasks/{task_id}/assign/`

```json
{
    "profile_ids": [id, id...]
}
```

### List all users assigned to a task
**GET** `/api/tasks/1/?profile_id={profile_id}`

