# PostgreSQL (Windows) setup (Option A)

## 1) Install PostgreSQL

### Option A1: Official installer (recommended)
- Download the Windows installer from https://www.postgresql.org/download/windows/
- Install **PostgreSQL Server** + **pgAdmin** + **Command Line Tools**.

During install:
- Remember the password you set for the `postgres` superuser.
- Keep the default port `5432`.

### Option A2: winget (if available)
If you have winget installed:
- `winget search postgresql`
- `winget install PostgreSQL.PostgreSQL`

(Exact package id can vary; the search output will show the correct id.)

## 2) Ensure psql is available
After install, open a new PowerShell and run:
- `psql --version`

If it’s not found, add PostgreSQL’s `bin` folder to your PATH.

## 3) Create database + user

### Using pgAdmin (GUI)
- Create login role `app_user` with password `app_password`
- Create database `app_db` owned by `app_user`

### Using psql (CLI)
Open PowerShell:
- `psql -U postgres -h 127.0.0.1 -p 5432`

Then run:
- `CREATE USER app_user WITH PASSWORD 'app_password';`
- `CREATE DATABASE app_db OWNER app_user;`

## 4) Configure Django
Edit `.env`:
- `DB_ENGINE=postgres`
- `DB_NAME=app_db`
- `DB_USER=app_user`
- `DB_PASSWORD=app_password`
- `DB_HOST=127.0.0.1`
- `DB_PORT=5432`

## 5) Migrate + run
- `\.venv\Scripts\python manage.py migrate`
- `\.venv\Scripts\python manage.py runserver`

## Troubleshooting
- If you see authentication errors, confirm the username/password and that the user has access to the DB.
- If you see connection refused, confirm the PostgreSQL service is running and listening on port 5432.
