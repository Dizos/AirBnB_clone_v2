-- Script to prepare MySQL server for the project
-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create user if it doesn't exist
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant privileges for hbnb_dev_db
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Grant SELECT privilege on performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Apply privileges
FLUSH PRIVILEGES;
