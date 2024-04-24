CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 10000
);

CREATE TABLE historic (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INT NOT NULL,
    stock_name TEXT NOT NULL,
    price NUMERIC NOT NULL,
    quantity INT UNSIGNED,
    transaction_type TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INT NOT NULL,
    stock_name TEXT NOT NULL,
    stock_symbol TEXT NOT NULL,
    quantity INT NOT NULL,
    price NUMERIC NOT NULL,
    total FLOAT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Prueba --

CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, cash NUMERIC NOT NULL DEFAULT 10000.00);
CREATE TABLE portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INT NOT NULL,
    stock_name TEXT NOT NULL,
    stock_symbol TEXT NOT NULL,
    quantity INT NOT NULL,
    price NUMERIC NOT NULL, total FLOAT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE historic (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INT NOT NULL,
    stock_name TEXT NOT NULL,
    price NUMERIC NOT NULL,
    quantity INT UNSIGNED,
    transaction_type TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE UNIQUE INDEX username ON users (username);