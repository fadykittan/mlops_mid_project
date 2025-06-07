-- Create the database if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'mlops_db') THEN
        CREATE DATABASE mlops_db;
    END IF;
END
$$;

-- Create the user if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_user WHERE usename = 'mlops') THEN
        CREATE USER mlops WITH PASSWORD 'mlops';
        ALTER USER mlops WITH SUPERUSER;
    END IF;
END
$$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE mlops_db TO mlops;

