create database purplepearl;
use purplepearl;

create table customers (customer_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
-> contact VARCHAR(20) NOT NULL,
-> first_name VARCHAR(30),
-> last_name VARCHAR(30),
-> destination_id INT,
-> created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
-> updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);

create table categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    category_name VARCHAR(30) UNIQUE NOT NULL,
    description VARCHAR(200),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create table products (
    product_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    product_name VARCHAR(30) UNIQUE NOT NULL,
    description VARCHAR(200),
    quantity INT NOT NULL,
    price_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create table prices(
    price_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    buying_price DECIMAL(10,2) NOT NULL,
    selling_price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create table orders(
    order_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    order_product INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    discount DECIMAL(10,2) NOT NULL DEFAULT 0,
    final_amount DECIMAL(10,2) NOT NULL,
    additional_details VARCHAR(255),
    order_status ENUM ('PENDING PAYMENT ONLY','PENDING PAYMENT AND DELIVERY', 'PAID-PENDING DELIVERY','PAID AND DELIVERED','ERROR') NOT NULL,
    payment_reference VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create table category_product(
    category_product_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    category_id INT NOT NULL,
    product_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    
);

create table destinations(
    destination_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    destination_name VARCHAR(30) NOT NULL,
    delivery_charge DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create table order_product(
    order_product_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    product_id INT NOT NULL,
    product_quantity INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO customers(contact,first_name,last_name,destination_id) 
VALUES ('0721657435','Esther','Mwangi',001),
('0734215432','Ann','Njeru',003),
('0755323453','Karim',NULL,001),('0700123425','shop',NULL,7);

INSERT INTO destinations(destination_name, delivery_charge) VALUES
('CBD',100.00),('MOMBASA',300.00),
('KASARANI',300.00),('TRM',300),
('KISUMU',250.00),('NAKURU',250.00);

INSERT INTO categories(category_name,description) VALUES 
('earrings',NULL),('belts',NULL),('jewellery_sets',NULL),
('brooches',NULL),('cover_ups',NULL);

INSERT INTO prices(buying_price,selling_price) VALUES 
('100.00','350.00'),('120.00','400.00'),
('200.00','400.00'),('250.00','400.00'),
('250.00','500.00'),(600.00,1200.00),(600.00,1000.00);

INSERT INTO products(product_name,description,quantity,price_id) VALUES 
('stud_earrings',NULL,10,2),
('gold_belts',NULL,5,6),
('drop_earrings',NULL,20,4),
('crystal_hanging_earrings',NULL,15,5),
('pearl_earrings',NULL,18,4),
('kimonos_black',NULL,10,7);

INSERT INTO orders(customer_id,order_product,total_amount,discount,final_amount,additional_details,order_status,payment_reference) 
VALUES (2,2,200,0.00,200,NULL,'PAID AND DELIVERED','FR27TH345A6'),
(3,1,1000, 0.00,1000,NULL,'PAID-PENDING DELIVERY','RY23SF4562');

INSERT INTO category_product(category_id,product_id) VALUES
(1,1),(1,3),(1,4),(1,5),(5,6),(2,2);

INSERT INTO order_product(product_id, product_quantity) VALUES(6,1);



