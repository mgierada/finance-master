SELECT 'CREATE DATABASE finance_master'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'finance_master')\gexec
