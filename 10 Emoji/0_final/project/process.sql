CREATE TABLE
  users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    email TEXT,
    hash TEXT NOT NULL
  );

CREATE TABLE
  stores (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    img TEXT
  );

CREATE TABLE
  products (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    store_id INT NOT NULL,
    product TEXT,
    cents INT,
    FOREIGN KEY (store_id) REFERENCES stores (id)
  );

CREATE TABLE
  orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INT NOT NULL,
    store_id INT NOT NULL,
    DATE DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
  );

CREATE TABLE
  order_line (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    qty INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (id),
    FOREIGN KEY (order_id) REFERENCES orders (id)
  );

SELECT
  product_id,
  qty,
  p.product,
  p.cents
FROM
  order_line
  JOIN products AS p ON p.id = product_id
WHERE
  order_id = 1
ORDER BY
  p.id ASC;

SELECT
  store_id,
  DATE,
  s.name
FROM
  orders
  JOIN stores AS s ON s.id = store_id
WHERE
  store_id = 1;

SELECT
  o.id,
  o.date,
  s.name
FROM
  orders AS o
  JOIN stores AS s ON s.id = o.store_id
WHERE
  user_id = 1;

CREATE TABLE
  users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    email TEXT
  );

CREATE TABLE
  stores (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    img TEXT
  );

CREATE TABLE
  products (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    store_id INT NOT NULL,
    product TEXT,
    cents INT,
    FOREIGN KEY (store_id) REFERENCES stores (id)
  );

CREATE TABLE
  order_line (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    qty NOT NULL DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products (id),
    FOREIGN KEY (order_id) REFERENCES orders (id)
  );

CREATE TABLE
  orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INT NOT NULL,
    store_id INT NOT NULL,
    DATE DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
  );