# Task Manager API

![CI](https://github.com/aminooo101/task-manager-api/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Django](https://img.shields.io/badge/django-6.0-green)

REST API for task management with projects, built with Django REST Framework.
JWT authentication, role-based filtering, and pagination.

## Features
- JWT authentication with djangorestframework-simplejwt
- Projects and tasks with priority and status
- Filtering by status, priority, date range
- Pagination (10 items per page)
- Project statistics endpoint
- Django admin panel
- Dockerized with docker-compose
- CI with GitHub Actions

## Quick start
```bash
git clone https://github.com/aminooo101/task-manager-api
cd task-manager-api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

## Run with Docker
```bash
docker-compose up
```

## Tests
```bash
pytest tasks/tests.py -v
```

## Stack
Django · DRF · PostgreSQL · JWT · Docker · GitHub Actions · Render