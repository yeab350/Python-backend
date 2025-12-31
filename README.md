# Simple Django Admin + Public Site (Backend-focused)

## Setup

1. Create a virtualenv and install deps:

   - `python -m venv .venv`
   - `\.venv\Scripts\pip install -r requirements.txt`

2. Create `.env` (copy from `.env.example`).

3. Run migrations:

   - `\.venv\Scripts\python manage.py migrate`

4. Create an admin user:

   - `\.venv\Scripts\python manage.py createsuperuser`

5. Run the server:

   - `\.venv\Scripts\python manage.py runserver`

## URLs

- Public catalog: `http://127.0.0.1:8000/`
- Public support form: `http://127.0.0.1:8000/support/`
- Staff dashboard: `http://127.0.0.1:8000/staff/`
- Django admin: `http://127.0.0.1:8000/admin/`

## Database

Settings are env-driven. PostgreSQL is the primary target.

- By default, if `DB_ENGINE`/`DB_NAME` are not set, the app uses SQLite so you can run immediately.
- To use PostgreSQL: follow [docs/postgres-windows.md](docs/postgres-windows.md) then set `DB_ENGINE=postgres` and provide credentials.
- To use MySQL instead: set `DB_ENGINE=mysql` and install a MySQL driver (e.g. `mysqlclient`).

If no DB env vars are set, the project falls back to SQLite for local development.
