import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, render_template, session, request, redirect, url_for, g

app = Flask(__name__)
app.secret_key = 'supersecret'

def connect_db():
  rv = sqlite3.connect(os.path.join(app.root_path, 'db/d2d.db'))
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
  return render_template('dashboard.html')

@app.route('/new')
def new_contract():
  return render_template('new_contract.html')

@app.route('/complete')
def complete_contract():
  return render_template('complete_contract.html')

@app.route('/shipment/<int:id>')
def shipment(id):
  return render_template('shipment.html', id=id)

if __name__ == '__main__':
  app.run(debug=True)
