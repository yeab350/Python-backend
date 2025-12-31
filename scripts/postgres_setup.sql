-- Run this as a PostgreSQL superuser (e.g. "postgres")
-- Creates a dedicated app user + database.

DO
$$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_user') THEN
    CREATE ROLE app_user LOGIN PASSWORD 'app_password';
  END IF;
END
$$;

-- Create DB if it doesn't exist (simple approach)
-- If your environment blocks CREATE DATABASE inside DO blocks,
-- run the CREATE DATABASE statement manually.

-- CREATE DATABASE app_db OWNER app_user;
