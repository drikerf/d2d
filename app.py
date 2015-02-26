from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def login():
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
