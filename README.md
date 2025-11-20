# SICEI API - Final project

Final project for distributed systems. API for managing students, courses, and grades.

## Create a virtual environment
You can follow the [FastAPI official doc](https://fastapi.tiangolo.com/virtual-environments/) for setting the environment

```
python -m venv .venv
```

## Activate the environment
For Linux
```
source .venv/bin/activate
```

For Windows
```
.venv\Scripts\Activate.ps1
```

## Upgrade pip
```
python -m pip install --upgrade pip
```

## Install  FastAPI from requirements.txt
```
pip install -r requirements.txt
```

## Set the ENV file
Create a .env file with the following attributes for the production database
```
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=
```

## Run the Sicei API using Dockerfile
Build the image for the container using the provided Dockerfile

```
docker build -t sicei-api .
```

Start a new container based on the image you just created

```
docker run -d -p 8000:8000 --name sicei-api-container sicei-api
```

## Run dev mode with Docker Compose
Use the following command to start the docker compose

```
docker compose up -d
```

Use the following command to turn off the container

```
docker compose down
```

## For Developers:

If you plan to contribute, test, or modify the code, install the development tools:
```
pip install -r requirements-dev.txt
```

Development Workflow
We use Ruff for linting/formatting and Pytest for testing. We also enforce code quality using Pre-commit hooks.

1. Setup Pre-commit
Once dependencies are installed, initialize the pre-commit hooks. This ensures code is checked automatically before every commit.

pre-commit install

2. Useful Commands

| Action | Command | Description |
| :--- | :--- | :--- |
| **Run Tests** | `pytest` | Runs all unit tests and generates a coverage report. |
| **Format Code** | `ruff format .` | Automatically formats code to match the project style. |
| **Lint & Fix** | `ruff check --fix .` | Checks for errors and fixes imports/variables automatically. |
| **Validate All** | `pre-commit run --all-files` | Runs all checks (lint, format, types) on all files manually. |
