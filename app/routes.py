import json
import os
import stripe
from flask import Flask, url_for, render_template, jsonify, request, flash, redirect
from app import app
from app.forms import LoginForm, DonateForm
from datetime import datetime, date, time
import logging
from logging.handlers import RotatingFileHandler

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
# 4) Set any environment variables needed by the application.
# 5) Execute "flask run"

# Activate environment one server
# source /home/nhbcalle/virtualenv/proj/newhopebeta/3.8/bin/activate && cd /home/nhbcalle/proj/newhopebeta

# stripe help: https://testdriven.io/blog/flask-stripe-tutorial/
stripeKeys = {
    "secretKey": os.environ["STRIPE_SECRET_KEY"] or "oops",
    "publishableKey": os.environ["STRIPE_PUBLISHABLE_KEY"] or "sorry",
}

class PageTemplate:
    def __init__(self, title):
        self.title = title

pageModel = PageTemplate('New Hope Baptist Church')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', model = pageModel)

@app.route('/give')
def give():
    return render_template('give.html', model = pageModel)

@app.route('/events')
def events():
    return render_template('events.html', model = pageModel)

@app.route('/introduction')
def introduction():
    return render_template('introduction.html', model = pageModel)

@app.route('/messages')
def messages():
    return render_template('messages.html', model = pageModel)

@app.route('/live')
def live():
    return render_template('live.html', model = pageModel)

@app.route('/services')
def services():
    return render_template('services.html', model = pageModel)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.login.data, form.remember_me.data))
        return redirect(url_for('index'))
    flash('did nod validate')
    return render_template('login.html', title='Sign In', form=form, model = pageModel)

@app.route('/donateco', methods = ['GET'])
def donateco():
    return render_template('donateco.html', model = pageModel)

@app.route("/donateco-config")
def get_publishable_key():
    stripeConfig = {"publicKey": stripeKeys["publishableKey"]}
    return jsonify(stripeConfig)

@app.route('/donate', methods = ['GET', 'POST'])
def donate():
    form = DonateForm
    return render_template('donate.html', form = form, model = pageModel)

@app.route('/create-checkout-session', methods = ['POST'])
def create_checkout_session():
    try:
        dollarAmount = int(request.form['amount'])
        amount = dollarAmount * 100
        app.logger.info('create-checkout-session posted ' + str(amount))
        # domain_url = "http://localhost:5000/"
        stripe.api_key = stripeKeys["secretKey"]

        session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            submit_type = 'donate',
            line_items = [{
                'price_data': {
                    'currency': 'usd',
                    #'type': 'one_time',
                    'product_data': {
                        'name': 'One Time Donation'
                    },
                    'unit_amount': amount
                },

                # This, 'price', is configured in the Stripe dashboard. It allows for a one time pament of $10.
                # 'price': 'price_1ImSLiKkHVDoGTuCUY3oxfKm',
                'quantity': 1
            }],
            mode = 'payment',
            success_url = url_for('checkout_success', session_id="{CHECKOUT_SESSION_ID}", _external = True),
            cancel_url = url_for('checkout_cancel', _external = True)
        )
        # return jsonify({"sessionId": session["id"]})
        app.logger.info('session ID ' + session.id)
        return jsonify(id = session.id)
    except Exception as e:
        app.logger.error('An exception was thrown creating a stripe checkout sesson. ' + str(e))
        return jsonify(error=str(e)), 403

@app.route('/checkout-success')
def checkout_success():
    return render_template('success.html', model = PageTemplate('Thank you!') )

@app.route('/checkout-cancel')
def checkout_cancel():
    return render_template('cancel.html', model = pageModel)

@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        app.logger.info('In create-payment-intent')
        app.logger.info(request.data)
        data = json.loads(request.data)
        app.logger.info(data)
        # A PaymentIntent tracks the customer's payment lifecycle, keeping track of any failed payment attempts and ensuring the customer is only charged once.
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='usd'
        )
        # Return the PaymentIntent's client secret in the response to finish the payment on the client.
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        app.logger.error('An exception was thrown creating a stripe payment intent. ' + str(e))
        return jsonify(error=str(e)), 403

def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1986