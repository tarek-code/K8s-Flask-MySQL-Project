-- Database initialization script for Flask application
-- Note: Replace 'yourpassword' with a secure password in production
CREATE DATABASE IF NOT EXISTS flaskdb;
CREATE USER IF NOT EXISTS 'flaskuser'@'%' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON flaskdb.* TO 'flaskuser'@'%';
FLUSH PRIVILEGES;
USE flaskdb;
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);