-- 1. Buyer agrees to buy something from Seller for a price.
-- 2. Seller sets up contract
-- SELLER
INSERT OR IGNORE INTO users VALUES ('seller1@mail.com');
-- BUYER
INSERT OR IGNORE INTO users VALUES ('buyer1@gmail.com');

-- Insert contract with randomly generated id 555
INSERT INTO contracts(id, seller, buyer, pickup_addr, brn, ban, delivery_addr)
	VALUES (555, 'seller1@gmail.com', 'buyer1@gmail.com', 'Addr1',
		'112-123', '191999191', 'Addr2');

-- Seller adds packages to the contract
INSERT INTO packages VALUES (NULL, 555, 12.0, 'Box 1', 10.0, 10.0, 10.0, 5.5);
INSERT INTO packages VALUES (NULL, 555, 12.0, 'Box 2', 10.0, 10.0, 10.0, 5.5);
INSERT INTO packages VALUES (NULL, 555, 12.0, 'Box 3', 10.0, 10.0, 10.0, 5.5);

-- A shipment order is generated
-- And a delivery price is display to the seller
INSERT INTO shipments (contract, delivery_price)
	VALUES (555, (SELECT SUM(width*height*length/1000000)*1000 FROM packages WHERE contract = 555));

-- Seller accepts the delivery price and signs the contract
UPDATE contracts SET signed_at = datetime() WHERE id = 555;

-- 3. Buyer completes the contract with id=555
-- Buyer logs in and is shown the price to pay
SELECT SUM(price) FROM packages WHERE contract = 555;

-- Buyer provides credit card information and pays the specified amount
UPDATE contracts SET paid_at = datetime() WHERE id = 555;

-- 4. Driver delivers package
-- Create a random driver with BRN=123-123 and BAN=12838...
INSERT INTO drivers VALUES (NULL, '123-123', '128389129898');

-- Driver takes on contract 555
UPDATE shipments SET driver = last_insert_rowid(), -- last_insert_rowid() is the ID of the driver
	assigned_at = datetime() WHERE contract = 555;

-- Driver picks up the delivery
UPDATE shipments SET pickup_at = datetime() WHERE contract = 555;

-- Driver drives package to buyer
-- Driver drops off package
UPDATE shipments SET dropoff_at = datetime() WHERE contract = 555;

-- Buyer confirms delivery and satisfaction
UPDATE shipments SET confirmed_at = datetime() WHERE contract = 555;

-- 5. Contract is settled with seller and money is sent to the seller's bank.
UPDATE contracts SET settled_at = datetime() WHERE id = 555;
