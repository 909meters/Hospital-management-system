-- Initialization script for Hospital Management System Database
-- This script sets up the initial database configuration

-- Create database if it doesn't exist (PostgreSQL will handle this through environment variables)

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE hospital_db TO hospital_user;

-- This file will be executed when the PostgreSQL container starts for the first time
