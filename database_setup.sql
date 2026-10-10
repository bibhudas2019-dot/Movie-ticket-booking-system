CREATE DATABASE IF NOT EXISTS movie_booking_db;
USE movie_booking_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
);

INSERT IGNORE INTO users (username, password) VALUES ('admin', 'admin123');

CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    movie_name VARCHAR(100) NOT NULL,
    show_time VARCHAR(50) NOT NULL,
    seats INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL
);
