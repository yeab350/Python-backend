# Reusable Django Backend API (No Frontend)

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

## API URLs

- Health: `GET http://127.0.0.1:8000/api/health/`
- Auth token: `POST http://127.0.0.1:8000/api/auth/token/` (body: `{"username": "...", "password": "..."}`)
- Current user: `GET http://127.0.0.1:8000/api/auth/me/` (header: `Authorization: Token <token>`)
- Logout (delete token): `POST http://127.0.0.1:8000/api/auth/logout/`

### Resources

- Products: `GET /api/products/`, `GET /api/products/<slug>/`
   - Write operations require a staff user token.
- Orders: `POST /api/orders/` (public)
   - List/retrieve require a staff user token.
- Tickets: `POST /api/tickets/` (public)
   - List/retrieve require a staff user token.
   - Add message: `POST /api/tickets/<id>/messages/`
      - Staff: `Authorization: Token ...`
      - Anonymous: include `customer_email` matching the ticket.

## CORS (use from any website)

By default CORS is open in development (`DJANGO_DEBUG=1`).

For production, set one of:

- `CORS_ALLOW_ALL_ORIGINS=1` (allow any frontend)
- or `CORS_ALLOWED_ORIGINS=https://your-frontend.com,https://another.com`

## Admin

- Django admin: `http://127.0.0.1:8000/admin/`

## Database

Settings are env-driven. PostgreSQL is the primary target.

- By default, if `DB_ENGINE`/`DB_NAME` are not set, the app uses SQLite so you can run immediately.
- To use PostgreSQL: follow [docs/postgres-windows.md](docs/postgres-windows.md) then set `DB_ENGINE=postgres` and provide credentials.
- To use MySQL instead: set `DB_ENGINE=mysql` and install a MySQL driver (e.g. `mysqlclient`).

If no DB env vars are set, the project falls back to SQLite for local development.
