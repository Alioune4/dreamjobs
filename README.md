# Dream Jobs

This is a simple API to manage job offers.

# Usage

## Dependencies
- Docker
- Docker Compose

## How to run

Run the following command to start the api

```bash
$ docker-compose up -d
```

## Environment variables
The following environment variables are needed to run the application:
- `DATABASE_URL`: The database URL. Default is `sqlite:///dreamjobs.db`
- `SECRET_KEY`: The secret key used to sign the JWT tokens
- `ADMIN_EMAIL`: The email of the admin user
- `ADMIN_PASSWORD`: The password of the admin user

## Admin user
The admin user is created when the application starts. The email and password are defined by the `ADMIN_EMAIL` and `ADMIN_PASSWORD` environment variables.
The admin username is `admin`.

# Documentation
The API documentation is available at http://localhost:5000/swagger/

# Tests

To run the tests, execute the following command in a virtual environment

```bash
$ pip install -r requirements.txt

$ pytest
```