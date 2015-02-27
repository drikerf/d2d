from flask import g
import random

# query helper function
def query_db(query, args=(), one=False):
  cur = g.db.execute(query, args)
  rv = cur.fetchall()
  cur.close()
  return (rv[0] if rv else None) if one else rv

# returns all contracts where email is buyer or seller
def contracts(email):
  return query_db('SELECT * FROM contracts WHERE buyer = ? OR seller = ?',
      [email, email])

def all_undelivered_contracts():
    return query_db('SELECT * FROM contracts WHERE paid_at NOTNULL AND settled_at ISNULL AND declined ISNULL')

# pending contracts for buyer with email
# a pending contract is a contract where paid_at is null
def pending_contracts(email):
  return query_db('SELECT * FROM contracts WHERE buyer = ? AND paid_at ISNULL AND declined ISNULL',
      [email])

# creates a contract
# returns the id of the new contract
def create_contract(seller, buyer, pickup_addr, brn, ban, delivery_addr):
  # TODO: Check for unqiueness
  gen_id = random.randrange(1000000, 9999999)
  g.db.execute('INSERT OR IGNORE INTO users VALUES (?)', [seller])
  g.db.execute('INSERT OR IGNORE INTO users VALUES (?)', [buyer])
  g.db.execute('INSERT INTO contracts(id, seller, buyer, pickup_addr, brn, ban, delivery_addr)' + \
      ' VALUES (?, ?, ?, ?, ?, ?, ?)', [gen_id, seller, buyer, pickup_addr, brn, ban, delivery_addr])
  g.db.commit()
  return gen_id

# returns all packages for contract id
def packages_for_contract(contractId):
  return query_db('SELECT * FROM packages WHERE contract = ?', [contractId])

# adds a package to a contract
# returns nothing 
def add_package_to_contract(contractId, price, desc, height, width, length, weight):
  g.db.execute('INSERT INTO packages (contract, price, desc, height, width, length, weight)' + \
      ' VALUES (?, ?, ?, ?, ?, ?, ?)', [contractId, price, desc, height, width, length, weight])
  g.db.commit()
  return 

# sign a contract - this marks the contract
# as signed by the seller and creates a 
# new shipment with delivery price derived from 
# packages included in the shipment
# returns nothing
def sign_contract(contractId):
  g.db.execute('UPDATE contracts SET signed_at = datetime() WHERE id = ?', [contractId])
  g.db.execute('INSERT INTO shipments (contract, delivery_price) VALUES ' + \
      '(?, (SELECT SUM(width*height*length/1000000)*1000 FROM packages WHERE contract = ?))', [contractId, contractId])
  g.db.commit()
  return

# marks a contract as paid
# TODO: create an entry in a payments table
# returns nothing
def pay_contract(contractId):
  # set paid_at column to datetime() for contractId=id
  g.db.execute('UPDATE contracts SET paid_at = datetime() WHERE id = ?', [contractId])
  g.db.commit()
  return

# return shipment details for contract id
def shipment(contractId):
  return query_db('SELECT * FROM shipments JOIN contracts ON shipments.contract = contracts.id WHERE contracts.id = ?', [contractId], True)

# assigns a driver to the shipment for
# contractId. brn and ban are the drivers
# bank routing och bank account numbers.
# returns driver id
def assign_driver_to_delivery(contractId, brn, ban):
  cur = g.db.cursor()
  cur.execute('INSERT INTO drivers VALUES (NULL, ?, ?)', [brn, ban])
  driverId = cur.lastrowid
  cur.execute('UPDATE shipments SET driver = ?, assigned_at = datetime() ' + \
      'WHERE contract = ?', [driverId, contractId])
  g.db.commit()
  return driverId

# Driver picks up delivery with contractId
# and marks the time in the shipments table
def pickup_delivery(contractId, driverId):
  g.db.execute('UPDATE shipments SET pickup_at = datetime() WHERE contract = ?', [contractId])
  g.db.commit()
  return

# Driver drops off package at the buyer
# and marks the time in the shipments table
def dropoff_delivery(contractId, driverId):
  g.db.execute('UPDATE shipments SET dropoff_at = datetime() WHERE contract = ?', [contractId])
  g.db.commit()
  return

# Buyer confirms and verifies the delivery
# and marks the time in the shipments table
def confirm_delivery(contractId):
  g.db.execute('UPDATE shipments SET confirmed_at = datetime() WHERE contract = ?', [contractId])
  g.db.commit()
  return

# Contract is settled with the seller and
# money is transfered to the seller's bank
def settle_contract(contractId):
  g.db.execute('UPDATE contracts SET settled_at = datetime() WHERE id = ?', [contractId])
  g.db.commit()
  return

# Decline contract
def decline_contract(contractId):
    g.db.execute('UPDATE contracts SET declined = 1 WHERE id = ?', [contractId])
    g.db.commit()
    return
