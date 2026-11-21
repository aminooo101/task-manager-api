# Task Manager API

Django REST Framework API for managing tasks and users.

## Features

- User authentication and registration
- Task creation, listing, and management
- Django REST Framework
- SQLite database (development)

## Project Structure

```
task-manager-api/
├── core/          # Project settings and configuration
├── tasks/         # Task app (models, views, serializers)
├── users/         # User app
├── manage.py
├── requirements.txt
└── README.md
```

## Installation & Run

```bash
git clone https://github.com/aminooo101/task-manager-api
cd task-manager-api
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate      # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Notes

This is a learning project demonstrating Django REST Framework basics (models, serializers, views, authentication).

## Author

Amin Hadian · [github.com/aminooo101](https://github.com/aminooo101)
