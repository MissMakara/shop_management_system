create database purplepearl;
use purplepearl;
CREATE TABLE users(
    user_id BINARY(16) PRIMARY KEY NOT NULL,
    user_name VARCHAR(40) UNIQUE NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30),
    user_role VARCHAR(30) NOT NULL
);

create table customers (
    customer_id BINARY(16) PRIMARY KEY NOT NULL,
    contact VARCHAR(20) NOT NULL,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);

create table categories (
    category_id BINARY(16) PRIMARY KEY NOT NULL,
    category_name VARCHAR(30) UNIQUE NOT NULL,
    description VARCHAR(200),
    parent_id BINARY(16),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create table prices(
    price_id BINARY(16) PRIMARY KEY NOT NULL,
    buying_price DECIMAL(10,2) NOT NULL,
    selling_price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create table products (
    product_id BINARY(16) PRIMARY KEY NOT NULL,
    product_name VARCHAR(30) UNIQUE NOT NULL,
    description VARCHAR(200),
    price_id BINARY(16) NOT NULL,
    category_id BINARY(16) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create table product_colours(
    product_colour_id BINARY(16) PRIMARY KEY NOT NULL,
    product_id BINARY(16) NOT NULL,
    primary_colour ENUM('GOLD','SILVER','WHITE','BLACK','RED','GREEN','BLUE','PINK'),
    secondary_colour ENUM('GOLD','SILVER','WHITE','BLACK','RED','GREEN','BLUE','PINK'),
    quantity INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create table orders(
    order_id BINARY(16) PRIMARY KEY NOT NULL,
    customer_id BINARY(16) NOT NULL,
    total_amount DECIMAL(10,2),
    discount DECIMAL(10,2) DEFAULT 0,
    final_amount DECIMAL(10,2),
    customer_destination_id BINARY(16),
    additional_details VARCHAR(255),
    order_status ENUM ('PENDING PAYMENT ONLY','PENDING PAYMENT AND DELIVERY', 'PAID PENDING DELIVERY','PAID AND DELIVERED','PAID AND CLOSED AT SHOP','ERROR') NOT NULL,
    payment_reference VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create table order_product(
    order_product_id BINARY(16) PRIMARY KEY NOT NULL,
    order_id BINARY(16) NOT NULL,
    product_id BINARY(16) NOT NULL,
    product_quantity INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create table destinations(
    destination_id BINARY(16) PRIMARY KEY NOT NULL,
    destination_name VARCHAR(30) NOT NULL,
    delivery_charge DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE customer_destinations(
    customer_destination_id BINARY(16) PRIMARY KEY NOT NULL,
    customer_id BINARY(16) NOT NULL,
    destination_id BINARY(16) NOT NULL,
    destination_details VARCHAR(250),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO customers(customer_id,contact,first_name,last_name) 
VALUES (UUID_TO_BIN(UUID()),'0721657435','Esther','Mwangi'),
(UUID_TO_BIN(UUID()),'0734215432','Ann','Njeru'),
(UUID_TO_BIN(UUID()),'0755323453','Karim',NULL),
(UUID_TO_BIN(UUID()),'0700123425','shop',NULL),
(UUID_TO_BIN(UUID()),'0755323453','Getrude','Karimi'),
(UUID_TO_BIN(UUID()),'0712785329','Alicia','Mwangi');

INSERT INTO destinations(destination_id, destination_name, delivery_charge) VALUES
(UUID_TO_BIN(UUID()),'CBD',100.00),(UUID_TO_BIN(UUID()),'MOMBASA',300.00),
(UUID_TO_BIN(UUID()),'KASARANI',300.00),(UUID_TO_BIN(UUID()),'TRM',300),
(UUID_TO_BIN(UUID()),'KISUMU',250.00),(UUID_TO_BIN(UUID()),'NAKURU',250.00);

INSERT INTO categories(category_id ,category_name,parent_id,colour,description) VALUES 
(UUID_TO_BIN(UUID()),'earrings',NULL,NULL,NULL),(UUID_TO_BIN(UUID()),'belts',NULL,NULL,NULL),
(UUID_TO_BIN(UUID()),'jewellery_sets',NULL, NULL,NULL),
(UUID_TO_BIN(UUID()),'brooches',NULL,NULL,NULL),
(UUID_TO_BIN(UUID()),'cover_ups',NULL,NULL,NULL);

INSERT INTO categories(category_id ,category_name,parent_id,description) VALUES 
(UUID_TO_BIN(UUID()),'studs',UUID_TO_BIN('8996da5f-0106-11ed-aff4-6c8814a20f80'),NULL),
(UUID_TO_BIN(UUID()),'pearls',UUID_TO_BIN('8996da5f-0106-11ed-aff4-6c8814a20f80'),NULL),
(UUID_TO_BIN(UUID()),'crystals',UUID_TO_BIN('8996e338-0106-11ed-aff4-6c8814a20f80'),NULL),
(UUID_TO_BIN(UUID()),'hanging',UUID_TO_BIN('8996da5f-0106-11ed-aff4-6c8814a20f80'), NULL);

INSERT INTO users(user_id, user_name, first_name,last_name,user_role) VALUES 
(UUID_TO_BIN(UUID()),'ann_b','Ann','Mugure','admin'),
(UUID_TO_BIN(UUID()),'Mralex','Alex','Kariuki','teller');

INSERT INTO destinations (destination_id, destination_name, delivery_charge)
VALUES
(UUID_TO_BIN(UUID()), 'CBD',100),
(UUID_TO_BIN(UUID()), 'DONHOLM', 300),
(UUID_TO_BIN(UUID()), 'UPPERHILL', 250),
(UUID_TO_BIN(UUID()), 'KIAMBU', 400),
(UUID_TO_BIN(UUID()), 'THINDIGUA', 350),
(UUID_TO_BIN(UUID()), 'KAREN', 500),
(UUID_TO_BIN(UUID()), 'KABETE', 300);

INSERT INTO customer_destinations (customer_destination_id, customer_id, destination_id, destination_details)
VALUES
(UUID_TO_BIN(UUID()), UUID_TO_BIN('b1829037-0103-11ed-aff4-6c8814a20f80'), UUID_TO_BIN('98d5d078-02bb-11ed-9bff-6c8814a20f80'),'High  Flats Apartments, House 406');

INSERT INTO prices(price_id, buying_price,selling_price) VALUES 
(UUID_TO_BIN(UUID()),'100.00','350.00'),(UUID_TO_BIN(UUID()),'120.00','400.00'),
(UUID_TO_BIN(UUID()),'200.00','400.00'),(UUID_TO_BIN(UUID()),'250.00','400.00'),
(UUID_TO_BIN(UUID()),'250.00','500.00'),(UUID_TO_BIN(UUID()),600.00,1200.00),
(UUID_TO_BIN(UUID()),600.00,1000.00);

INSERT INTO products(product_id, product_name, description, category_id) VALUES
(UUID_TO_BIN(UUID()),'classy_earrings',NULL, UUID_TO_BIN('fa5c8cf1-012b-11ed-aff4-6c8814a20f8')),
(UUID_TO_BIN(UUID()),'chain_belts', NULL,UUID_TO_BIN('8996e338-0106-11ed-aff4-6c8814a20f80')),
(UUID_TO_BIN(UUID()),'leather_chain_belts', NULL,UUID_TO_BIN('8996e338-0106-11ed-aff4-6c8814a20f80')),
(UUID_TO_BIN(UUID()),'pearl_earrings', NULL, UUID_TO_BIN('fa5c8cf1-012b-11ed-aff4-6c8814a20f80'));

INSERT INTO products(product_name,description,price_id, category_id,primary_colour,secondary_colour) VALUES 
(UUID_TO_BIN(UUID()),'stud_earrings',NULL,10,2,1),
(UUID_TO_BIN(UUID()),'gold_belts',NULL,5,6,2),
(UUID_TO_BIN(UUID()),'drop_earrings',NULL,20,4,1),
(UUID_TO_BIN(UUID()),'crystal_hanging_earrings',NULL,15,5,1),
(UUID_TO_BIN(UUID()),'pearl_earrings',NULL,18,4,5),
(UUID_TO_BIN(UUID()),'kimonos_black',NULL,10,7,2);

INSERT INTO product_colours(product_colour_id, product_id, primary_colour, secondary_colour, quantity) VALUES 
(UUID_TO_BIN(UUID()), UUID_TO_BIN('87dfd888-029a-11ed-8d9e-6c8814a20f80'),'GOLD', 'RED', 30),
(UUID_TO_BIN(UUID()), UUID_TO_BIN('b6b1293e-029a-11ed-8d9e-6c8814a20f80'),'GOLD', 'GOLD', 10),
(UUID_TO_BIN(UUID()), UUID_TO_BIN('b6b13247-029a-11ed-8d9e-6c8814a20f80'),'BLACK', 'GOLD', 5),
(UUID_TO_BIN(UUID()), UUID_TO_BIN('b6b13523-029a-11ed-8d9e-6c8814a20f80'),'WHITE', 'WHITE', 12);

INSERT INTO orders(order_id, customer_id,total_amount,discount,final_amount,additional_details,order_status,payment_reference) 
VALUES 
(UUID_TO_BIN(UUID()), UUID_TO_BIN('b1829037-0103-11ed-aff4-6c8814a20f80'));

UPDATE orders SET total_amount = 1500,discount=100,final_amount=1400,
customer_destination_id=UUID_TO_BIN('8e3df316-02bc-11ed-9bff-6c8814a20f80'),order_status= 'PAID AND DELIVERED',
payment_reference='TH123WFTHPKW'
WHERE order_id = UUID_TO_BIN('4f23bf37-02a8-11ed-9bff-6c8814a20f80');

INSERT INTO orders (order_id, customer_id)
VALUES (UUID_TO_BIN(UUID()), UUID_TO_BIN('b1828959-0103-11ed-aff4-6c8814a20f80'));

INSERT INTO customer_destinations (customer_destination_id, customer_id, destination_id, destination_details)
VALUES (UUID_TO_BIN(UUID()), UUID_TO_BIN('b1828959-0103-11ed-aff4-6c8814a20f80'), UUID_TO_BIN('98d5c863-02bb-11ed-9bff-6c8814a20f80'), 'Pioneer BUilding, Fifth floor, room 502');

INSERT INTO order_products (order_product_id, order_id, product_id, quantity)
VALUES (UUID_TO_BIN(UUID()), UUID_TO_BIN('d60973be-02c0-11ed-9bff-6c8814a20f80'), UUID_TO_BIN('b6b1293e-029a-11ed-8d9e-6c8814a20f80'), 3);

UPDATE orders SET 
total_amount = 4500.00,
final_amount = 4500.00,
order_status = "PAID PENDING DELIVERY",
payment_reference = "RY23SF4562"
WHERE
order_id = UUID_TO_BIN('d60973be-02c0-11ed-9bff-6c8814a20f80');


INSERT INTO order_product(order_product_id, order_id, product_id, product_quantity) VALUES
(UUID_TO_BIN(UUID()),UUID_TO_BIN('4f23bf37-02a8-11ed-9bff-6c8814a20f80'), UUID_TO_BIN('b6b13247-029a-11ed-8d9e-6c8814a20f80'),1),
(UUID_TO_BIN(UUID()),UUID_TO_BIN('4f23bf37-02a8-11ed-9bff-6c8814a20f80'), UUID_TO_BIN('87dfd888-029a-11ed-8d9e-6c8814a20f80'),2);


product_name,description,price_id, category_id,primary_colour,secondary_colour, quantity
classy_earrings,NULL, UUID_TO_BIN('ac4c847b-0108-11ed-aff4-6c8814a20f80'), UUID_TO_BIN('fa5c8cf1-012b-11ed-aff4-6c8814a20f8'), GOLD, RED, 30
chain_belts, NULL,UUID_TO_BIN('e7a46404-0292-11ed-8d9e-6c8814a20f80'),UUID_TO_BIN('8996e338-0106-11ed-aff4-6c8814a20f80'), GOLD, GOLD, 10
leather_chain_belts, NULL,UUID_TO_BIN('e7a46404-0292-11ed-8d9e-6c8814a20f80'),UUID_TO_BIN('8996e338-0106-11ed-aff4-6c8814a20f80'), BLACK, GOLD, 5
pearl_earrings, NULL, UUID_TO_BIN('ac4c847b-0108-11ed-aff4-6c8814a20f80'), UUID_TO_BIN('fa5c8cf1-012b-11ed-aff4-6c8814a20f80'), WHITE, WHITE, 12



-- #SOME EDITS AFTER THE USER JOURNEY MAPPING
-- CUSTOMERS TABLE 
-- removed the destination_id column
-- instead we created a customer_destination table to map the customers
-- to their different destination details 


-- add a parent_id column to the categories table
-- this is to bring about sub categories under the first categories
-- ie: the subcategories are under a specific category whose id will
-- be the parent_id to the rest of the columns

-- drop the category_product table and add a category_id column to products table
-- include a product_colours table to link the product_id to the different colours a product has

--orders table
--

-- edit the order_product table and add order_id for each entry

-- any order made will populate this table with the different products ordered
-- then use the products price id's to populate the total amounts due

