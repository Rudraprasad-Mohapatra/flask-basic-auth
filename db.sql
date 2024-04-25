CREATE DATABASE flask_login_db;

USE flask_login_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES ('demo_user', '$2b$12$v6aXtMNcNxgcbCRm/YRk4O21Gb3Y9tJy62kR39PS6Q6l/Q4vF8g7C');