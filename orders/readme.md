# ShopSphere Backend

A Django-based e-commerce backend system with products, orders, and user management.

## Setup

1. Created and activated virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Installed dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Started development server:
```bash
python manage.py runserver
```

## Features

- User authentication and authorization
- Product management
- Order processing
- RESTful API endpoints

## Tech Stack

- Django 4.2.7
- Django REST Framework
- Celery
- PostgreSQL (configured for development with SQLite)