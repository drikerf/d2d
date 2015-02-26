from flask import g

def query_db(query, args=(), one=False):
  cur = g.db.execute(query, args)
  rv = cur.fetchall()
  cur.close()
  return (rv[0] if rv else None) if one else rv

# returns an list of dictionaries
def contracts(email):
  return [{}] # all contracts where email = buyer or seller

# creates a contract
# returns the id of the new contract
def create_contract(seller, buyer, pickup_addr, brn, ban, delivery_addr):
  return 0

# returns all packages for contract id
def packages_for_contract(id):
  return [{}]

# adds a package to a contract
# returns id of the new package
def add_package_to_contract(contractId, price, desc, height, width, length, weight):
  return 0

# sign a contract - this marks the contract
# as signed by the seller and creates a 
# new shipment with delivery price derived from 
# packages included in the shipment
# returns nothing
def sign_contract(contractId):
  return

# marks a contract as paid
# TODO: create an entry in a payments table
# returns nothing
def pay_contract(contractId):
  # set paid_at column to datetime() for contractId=id
  return

# assigns a driver to the shipment for
# contractId. brn and ban are the drivers
# bank routing och bank account numbers.
# returns driver id
def assign_driver_to_delivery(contractId, brn, ban):
  return 0

# Driver picks up delivery with contractId
# and marks the time in the shipments table
def pickup_delivery(contractId, driverId):
  return

# Driver drops off package at the buyer
# and marks the time in the shipments table
def dropoff_delivery(contractId, driverId):
  return

# Buyer confirms and verifies the delivery
# and marks the time in the shipments table
def confirm_delivery(contractId):
  return

# Contract is settled with the seller and
# money is transfered to the seller's bank
def settle_contract(contractId):
  return
