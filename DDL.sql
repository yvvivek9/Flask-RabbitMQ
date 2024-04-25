DROP DATABASE IF EXISTS inventory;

CREATE DATABASE IF NOT EXISTS inventory;

USE inventory;

CREATE TABLE items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE stock (
    stock_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    -- order_date DATE NOT NULL DEFAULT CURRENT_DATE(),
    total_amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    price_per_item DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
);

CREATE TABLE stock_shipment( 
    stock_shipment_id INT AUTO_INCREMENT PRIMARY KEY, 
    stock_id INT NOT NULL, 
    shipment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    item_id INT NOT NULL, 
    quantity INT NOT NULL, 
    FOREIGN KEY (stock_id) REFERENCES stock(stock_id) ON DELETE CASCADE, 
    FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE  
);


-- Inserting data into the 'items' table
INSERT INTO items (name, price) VALUES
('Item1', 999.99),
('Item2', 499.99),
('Item3', 299.99),
('Item4', 79.99),
('Item5', 49.99);

-- Inserting data into the 'stock' table
INSERT INTO stock (item_id, quantity) VALUES
(1, 10),
(2, 20),
(3, 15),
(4, 30),
(5, 25);

-- Inserting data into the 'orders' table
INSERT INTO orders (total_amount) VALUES
(199.98),
(749.97),
(299.99),
(159.98);
