import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, render_template, session, request, redirect, url_for, g, get_flashed_messages, flash
import d2d

app = Flask(__name__)
app.secret_key = 'supersecret'

def connect_db():
  rv = sqlite3.connect(os.path.join(app.root_path, 'db/d2d.db'))
  rv.row_factory = sqlite3.Row
  return rv

@app.before_request
def before_request():
  g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

@app.route('/', methods=['POST', 'GET'])
def login():
  if session.get('user'):
    return redirect(url_for('dashboard'))
  if request.method == 'POST':
    try:
      g.db.execute('insert into users (email) values (?)', [request.form['email']])
      g.db.commit()
    except sqlite3.IntegrityError:
      # User in db.
      pass
    session['user'] = request.form['email']
    return redirect(url_for('dashboard'))
  return render_template('login.html')

@app.route('/dashboard')
def dashboard():
  contracts = d2d.contracts(session['user'])
  pending = d2d.pending_contracts(session['user'])
  return render_template('dashboard.html', contracts=contracts, pending=pending)

@app.route('/new', methods=['POST', 'GET'])
def new_contract():
  if request.method == 'POST':
    f = request.form
    print f
    id = d2d.create_contract(f['sellerEmail'], f['buyerEmail'], f['pickupAddress'],
      f['routingNr'], f['accountNr'], f['deliveryAddress'])
    i = 1
    while True:
      pc = str(i)
      try:
        d2d.add_package_to_contract(id, f['price_'+pc], f['description_'+pc], f['height_'+pc], f['width_'+pc],
          f['length_'+pc], f['weight_'+pc])
      except KeyError:
        break
      i += 1
    d2d.sign_contract(id)
    flash('Contract added!')
    return redirect(url_for('dashboard'))
  return render_template('new_contract.html')

@app.route('/complete/<int:id>', methods=['POST', 'GET'])
def complete_contract(id):
  if request.method == 'POST':
    d2d.pay_contract(id)
    flash('Contract paid!')
    return redirect(url_for('dashboard'))
  return render_template('complete_contract.html', id=id)

@app.route('/shipment/<int:id>')
def shipment(id):
  shipment = d2d.shipment(id)
  return render_template('shipment.html', shipment=shipment)

@app.route('/logout')
def logout():
  session.pop('user', None)
  return redirect(url_for('login'))

if __name__ == '__main__':
  app.run(debug=True)
