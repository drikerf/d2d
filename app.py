from flask import Flask, render_template, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecret'

@app.route('/', methods=['POST', 'GET'])
def login():
  if request.method == 'POST':
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
