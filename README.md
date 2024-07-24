# Dream Jobs

## Dependencies
- Docker
- Docker Compose

## How to run

Run the following command to start the api

```bash
$ docker-compose up -d
```

## DataBase

### Create a Migration
After modifying the models, run the following command to create a new migration.
The migrations are applied automatically when the backend container is started.

```bash
$  python3 -m flask --app api db migrate -m "migration message"
```