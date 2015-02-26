-- Create tables for Lab2 D2D
-- Usage: sqlite3 d2d < db.sql

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
CREATE TABLE shipment
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	driver INTEGER, -- Foreign key
	delivery_price REAL,
	assigned_at DATETIME,
	pickup_at DATETIME,
	dropoff_at DATETIME,
	confirmed_at DATETIME,

	FOREIGN KEY (driver) REFERENCES drivers(id)
);

-- Contract table
CREATE TABLE contracts
(
	id INTEGER PRIMARY KEY,
	seller TEXT, -- Seller foreign key
	buyer TEXT, -- Buyer foreign key
	shipment INTEGER, -- Shipment foreign key
	pickup_addr TEXT,
	brn TEXT, -- Seller bank routing number
	ban TEXT, -- Seller bank account number
	delivery_addr TEXT,
	signed_at DATETIME,
	settled_at DATETIME,

	FOREIGN KEY (seller) REFERENCES users(email),
	FOREIGN KEY (buyer) REFERENCES users(email),
	FOREIGN KEY (shipment) REFERENCES shipment(id)
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
