import json
import os
import stripe
from flask import Flask, url_for, render_template, jsonify, request, flash, redirect
from app import app
from app.forms import LoginForm
from datetime import datetime, date, time

# If you've just cloned the repo
# 1) Execute "python -m venv venv" to set up the virtual environment
# 2) Activate the environment by executing "venv\Scripts\activate"
# 3) Install Flask via "pip install flask"
# 4) Install Stripe via "pip install --upgrade stripe"
# 5) If the files .env or .flaskenv are being used, then execute "pip install python-dotenv"
# 6) Execute "flask run"

# To start the application (assuming the environment has been setup after cloning the repo):
# 1) Open a command console and change directory to the root of the application/repository
# 2) Activate the environment by executing "venv\Scripts\activate"
# 3) Set the FLASK_APP environment variable "set FLASK_APP=<name_of_python_file>" example "set FLASK_APP=newhope.py"
#        Note: This is being done via the .flaskenv file
# 4) Execute "flask run"

# Activate environment one server
# source /home/nhbcalle/virtualenv/proj/newhopebeta/3.8/bin/activate && cd /home/nhbcalle/proj/newhopebeta

stripe.api_key = ""

class PageTemplate:
    def __init__(self):
        self.title = 'New Hope Baptist Church'


@app.route('/')
@app.route('/index')
def index():
    # user = {'username': 'Mark'}
    # currentDate = datetime.now()
    # today = datetime.date(currentDate).strftime("%d-%b-%Y")
    # now = datetime.time(currentDate).strftime("%H:%M:%S")
    # sermonList = [
    #     {'title':'Title One', 'image':'', 'url':'', 'description':'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Neque gravida in fermentum et sollicitudin. Mollis nunc sed id semper risus. Luctus venenatis lectus magna fringilla urna porttitor rhoncus dolor purus.'},
    #     {'title':'Title Two', 'image':'', 'url':'', 'description':'Congue nisi vitae suscipit tellus mauris a diam maecenas. Orci sagittis eu volutpat odio facilisis mauris. Suscipit tellus mauris a diam maecenas sed enim ut. Nec dui nunc mattis enim ut tellus elementum sagittis.'},
    #     {'title':'Title Three', 'image':'', 'url':'', 'description':'Diam sollicitudin tempor id eu nisl nunc mi ipsum faucibus. Orci nulla pellentesque dignissim enim sit amet venenatis urna cursus. Cum sociis natoque penatibus et magnis dis parturient. Eget magna fermentum iaculis eu non diam.'}
    #     ]
    pageModel = PageTemplate()
    return render_template('index.html', model = pageModel)

@app.route('/donate')
def donate():
    pageModel = PageTemplate()
    return render_template('donate.html', model = pageModel)

@app.route('/events')
def events():
    pageModel = PageTemplate()
    return render_template('events.html', model = pageModel)

@app.route('/introduction')
def introduction():
    pageModel = PageTemplate()
    return render_template('introduction.html', model = pageModel)

@app.route('/messages')
def messages():
    pageModel = PageTemplate()
    return render_template('messages.html', model = pageModel)

@app.route('/live')
def live():
    pageModel = PageTemplate()
    z = 1/0
    return render_template('live.html', model = pageModel)

@app.route('/services')
def services():
    pageModel = PageTemplate()
    return render_template('services.html', model = pageModel)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    pageModel = PageTemplate()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.login.data, form.remember_me.data))
        return redirect(url_for('index'))
    flash('did nod validate')
    return render_template('login.html', title='Sign In', form=form, model = pageModel)

@app.route('/create-checkout-session', methods = ['POST'])
def create_checkout_session():
    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items = [{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Donation'
                },
                'unit_amount': 50.00
            },
            'quantity': 1
        }],
        mode = 'payment',
        success_url = url_for('checkout_success', _external = True),
        cancel_url = url_for('checkout_cancel', _external = True)
    )

    return jsonify(id = session.id)

@app.route('/checkout-success')
def checkout_success():
    pageModel = PageTemplate()
    return render_template('success.html', model = pageModel)

@app.route('/checkout-cancel')
def checkout_cancel():
    pageModel = PageTemplate()
    return render_template('cancel.html', model = pageModel)

@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='usd'
        )

        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403

def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 21.12