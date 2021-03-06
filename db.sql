-- Create tables for Lab2 D2D
-- Usage: sqlite3 db/d2d.db < db.sql

-- Drop existing tables
DROP TABLE IF EXISTS shipments;
DROP TABLE IF EXISTS contracts;
DROP TABLE IF EXISTS packages;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS drivers;

-- SQLite enable foreign key support
-- In SQLite3 this is off by default and needs to be
-- enabled _every_ connection for foreign key constraints
-- to be working.
PRAGMA foreign_keys = ON;

-- User table
-- An user can be both a Seller and a Buyer
CREATE TABLE users
(
	email TEXT PRIMARY KEY
);

-- Driver table
CREATE TABLE drivers
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	brn TEXT, -- Bank routing number
	ban TEXT -- Bank account number
);

-- Shipment table
CREATE TABLE shipments
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	contract INTEGER UNIQUE, -- Foreign key to contracts
	driver INTEGER, -- Foreign key to driver
	delivery_price REAL,
	assigned_at DATETIME,
	pickup_at DATETIME,
	dropoff_at DATETIME,
	confirmed_at DATETIME,

	FOREIGN KEY (contract) REFERENCES contracts(id),
	FOREIGN KEY (driver) REFERENCES drivers(id)
);

-- Contract table
CREATE TABLE contracts
(
	id INTEGER PRIMARY KEY,
	seller TEXT, -- Seller foreign key
	buyer TEXT, -- Buyer foreign key
	pickup_addr TEXT,
	brn TEXT, -- Seller bank routing number
	ban TEXT, -- Seller bank account number
	delivery_addr TEXT,
	signed_at DATETIME,
	paid_at DATETIME,
	settled_at DATETIME,
	declined INTEGER,

	FOREIGN KEY (seller) REFERENCES users(email),
	FOREIGN KEY (buyer) REFERENCES users(email)
);

-- Package table
CREATE TABLE packages
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	contract INTEGER, -- Contact foreign key
	price REAL,
	desc TEXT,
	height REAL, -- CM
	width REAL, -- CM
	length REAL, -- CM
	weight REAL, -- Grams

	FOREIGN KEY (contract) REFERENCES contracts(id)
);
