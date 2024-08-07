# Student Grade Service

This is a web service built with FastAPI for managing student grades. The service provides functionality for adding grades for students and obtaining statistical data about grades.

## Features

The application provides several routes:

1. `POST /grades/` - for submitting a new grade for a student
2. `GET /grades/subject/{subject_id}/` - for obtaining the statistics of a particular subject
3. `GET /grades/student/{student_id}` - for obtaining the grades of a particular student

## API Documentation

The API documentation generated with Swagger can be found at `/docs` when the service is running. Simply navigate to `{your-service-url}:{service-port}/docs` in your browser to access it.


## Installation and Running the Service

1. Make sure Docker and Docker Compose are installed on your machine.
2. Run the following command to start the service: docker compose up -d

## Environment Variables

The service requires the following environment variables to be set:

- `DB_USER`: Specifies the username used to connect to the database.
- `DB_PASSWORD`: Specifies the password used to connect to the database.
- `DB_PORT`: Specifies  the port on which your Postgres database is running.
- `DB_NAME`: Specifies the name of the Postgres database to be used.
- `APP_PORT`: Specifies the port on which the FastAPI application will be running.
- `SERVICE_WORKERS`: Specifies the number of workers you want the Gunicorn server to use and to linearly scale up/down the application.