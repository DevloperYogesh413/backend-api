# Shopline Auth API

Django REST Framework-based authentication API for Shopline backend.

Features:
- Signup
- Login
- Logout
- Password reset
- Simple HTML UI for auth flows

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
5. Run the dev server:
   ```bash
   python manage.py runserver
   ```

## Deploy to Render

- Add `render.yaml` or connect to a Git repo.
- Set `SECRET_KEY`, `DEBUG`, and database settings in Render environment variables.
- Use `gunicorn shopline_auth.wsgi` as the start command.
