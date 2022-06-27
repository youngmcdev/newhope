import json
from operator import and_
import os
import math
import time
from re import template
from config import Config
import stripe
from flask import Flask, url_for, render_template, jsonify, request, flash, redirect
from app import app, db
from app.forms import LoginForm, DonateForm, AddMessageForm
from app.models import VideoMessage
from datetime import datetime, date, timezone
import logging
from logging.handlers import RotatingFileHandler

# If you've just cloned the repo
# 1) Execute "python -m venv venv" to set up the virtual environment
# 2) Activate the environment by executing "venv\Scripts\activate"
# 3) Install Flask via "pip install flask"
# 4) Install Stripe via "pip install --upgrade stripe"
# 5) If the files .env or .flaskenv are being used, then execute "pip install python-dotenv"
# 5.1) pip intall flask-wtf
# 5.2) pip install flask-sqlalchemy
# 5.3) pip install flask-migrate NOTE: We're not usingt this yet. It's safe to ignore
# 6) Execute "flask run"

# To start the application (assuming the environment has been setup after cloning the repo):
# 1) Open a command console and change directory to the root of the application/repository
# 2) Activate the environment by executing "venv\Scripts\activate"
# 3) Set the FLASK_APP environment variable "set FLASK_APP=<name_of_python_file>" example "set FLASK_APP=newhope.py"
#        Note: This is being done via the .flaskenv file
# 4) Set any environment variables needed by the application.
#        Note: There should be a batch file to do this, but that will not be in the repo.
# 4.1) The database may need to be initialized. From the python interpreter...
# 4.1.1) from app import db
# 4.1.2) db.create_all()
# 5) Execute "flask run"

# Generate requirements file: pip freeze > requirements.txt
# Install requirementns: pip install -r requirements.txt

# Example: Activate environment on server
# source /home/nhbcalle/virtualenv/proj/newhopebeta/3.8/bin/activate && cd /home/nhbcalle/proj/newhopebeta

# stripe help: https://testdriven.io/blog/flask-stripe-tutorial/
stripeKeys = {
    "secretKey": os.environ.get('STRIPE_SECRET_KEY') or 'oops',
    "publishableKey": os.environ.get('STRIPE_PUBLISHABLE_KEY') or 'sorry',
}

googleApiKey = os.environ.get('GOOGLE_API_KEY') or 'my-google-api-key'

class PageTemplate:
    def __init__(self, title):
        self.title = title
        self.customerName = ''
        self.customerEmail = ''
        self.donationAmount = 0
        self.googleApiKey = googleApiKey
        self.messages = []

class Message:
    def __init__(self, id = 0):
        self.id = id
        self.sequence = 0
        self.title = ''
        self.description = ''
        self.youtube_id = ''
        self.timestamp = datetime.now(timezone.utc)
        self.image_file = ''
        self.image_description = ''

class Image:
    def __init__(self, filename = '', description = ''):
        self.filename = filename
        self.description = description

class MockStripeSession:
    def __init__(self):
        self.customer = MockStripeCustomer()
        self.amount_total = 0

class MockStripeCustomer:
    def __init__(self):
        self.email = ''
        self.name = ''

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
    # messageList = VideoMessage.query.order_by(VideoMessage.timestamp.desc()).limit(3).all()
    # imageList = GetImages()
    # index = 0
    # app.logger.info(f'{len(messageList)} video message were retrieved to display.')

    # pageModel.messages.clear()
    # for message in messageList:
    #     pageModel.messages.append(MapMessage(index, message, imageList[index]))
    #     index = index + 1
    pageModel.messages = GetMessages(3, True)
    return render_template('messages.html', model = pageModel)

@app.route('/guests')
def guests():
    return render_template('guests.html', model = pageModel)

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
    # MCY - fix this bug - seem to be referencing publicKey incorrectly
    # app.logger.info(f'Getting the publishable key {stripeConfig.publicKey}')
    return jsonify(stripeConfig)

@app.route('/donatecu', methods = ['GET', 'POST'])
def donatecu():
    form = DonateForm
    return render_template('donatecu.html', form = form, model = pageModel)

@app.route('/donate', methods = ['GET', 'POST'])
def donate():
    # this route does not actually 'checkout'
    form = DonateForm
    return render_template('donate.html', form = form, model = pageModel)

@app.route('/create-checkout-session', methods = ['POST'])
def create_checkout_session():
    try:
        dollarAmount = math.floor(float(request.form['amount']))
        amount = dollarAmount * 100
        app.logger.info('create-checkout-session AmountPosted:' + str(amount))
        stripe.api_key = stripeKeys["secretKey"]
        # This is set in the Stripe dashboard. However, we can override that here
        stripe.api_version = '2020-08-27'
        successUrl = url_for('checkout_success', _external = True) + "?session_id={CHECKOUT_SESSION_ID}"
        cancelUrl = url_for('checkout_cancel', _external = True)
        app.logger.info(f'SuccessUrl:{successUrl}')
        app.logger.info(f'CancelUrl:{cancelUrl}')

        session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            submit_type = 'donate',
            line_items = [{
                'price_data': {
                    'currency': 'usd',
                    #'type': 'one_time',
                    'product_data': {
                        'name': 'One Time Donation',
                        'description': 'Thank you for your contribution!', # long form description of the product
                        'images': ['https://www.nhbcallegan.com/static/logo-white-sq.png'] # upto 8 URLs to images
                    },
                    'unit_amount': amount
                },

                # This, 'price', is configured in the Stripe dashboard. It allows for a one time pament of $10.
                # 'price': 'price_1ImSLiKkHVDoGTuCUY3oxfKm',
                'quantity': 1
            }],
            mode = 'payment',
            success_url = successUrl,
            cancel_url = cancelUrl
        )
        app.logger.info(f'Session Object: {session}')

        sessionId = ''
        if(session):
            app.logger.info(f'session ID {session.id}')
            sessionId = session.id
        return jsonify(id = sessionId)
    except Exception as e:
        app.logger.error('An exception was thrown creating a stripe checkout sesson. ' + str(e))
        return jsonify(error=str(e)), 403

@app.route('/checkout-success')
def checkout_success():
    successModel = PageTemplate('Thank you!')
    sessionIdFromStripeSession = request.args.get('session_id')
    app.logger.info(f'Session ID from URL: "{sessionIdFromStripeSession}"')
    if(sessionIdFromStripeSession and sessionIdFromStripeSession.strip()):
        app.logger.info(f'Attempt to get a session from Stripe for the session ID.')
        try:
            session = stripe.checkout.Session.retrieve(sessionIdFromStripeSession)
            app.logger.info(f'Session object: {session}')
            app.logger.info(f'Attempt to get a customer object from Stripe for CustomerId:"{session.customer}"')
            customer = stripe.Customer.retrieve(session.customer)
            app.logger.info(f'Customer object: {customer}')
        except:
            app.logger.info('An error occured with the Stripe API. We could not retrieve the customer information after the successful payment processing. Returning default data to the view.')
            session = MockStripeSession()
            customer = session.customer
        
        if(customer):
            successModel.customerEmail = customer.email or ''
            successModel.customerName = customer.name or customer.email or ''

        successModel.donationAmount = int(session.amount_total/100)

    return render_template('success.html', model = successModel)

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

@app.route('/update-message', methods=['GET','POST'])
def update_message():
    form = AddMessageForm(request.form)

    if form.validate_on_submit() and AuthorizedToUpdate(form.password.data):
        messageId = int(form.id.data)
        app.logger.info(f'Form validated. Message ID: {messageId}')
        message = VideoMessage.query.filter_by(id = messageId).first()
        if bool(message):
            app.logger.info(f'Update message: {message}')
            dateToStore = GetDateToStore(form.date.data, form.is_am_service.data == 'am')
            app.logger.info(f'Message date: {dateToStore}')
            message.title = form.title.data
            message.description = form.description.data
            message.timestamp = dateToStore
            message.youtube_id = form.youtube_id.data
            db.session.commit()
        else:
            app.logger.info('Could not find the message to update.')

        return redirect(url_for('list_messages'))
    else:
        app.logger.info(f'The form did not validate. FormMethod:{request.method}')

    if request.method == 'GET':
        messageId = int(request.args['id'])
        app.logger.info(f'Message ID: {messageId}')
        message = VideoMessage.query.filter_by(id = messageId).first()
        app.logger.info(f'Display message: {message}')
        if bool(message):
            form.id.data = messageId
            form.title.data = message.title
            form.description.data = message.description
            form.date.data = message.timestamp
            form.youtube_id.data = message.youtube_id

    return render_template(
        'update_message.html',
        model = pageModel,
        form = form
    )

@app.route('/add-message', methods=['GET', 'POST'])
def add_message():
    if request.method != 'POST':
        app.logger.info(f'This is not a POST: {request.method}')

    #app.logger.info(request.form)
    form = AddMessageForm(request.form)
    #app.logger.info(f'value passed in {form.password.data}')
    if form.validate_on_submit() and AuthorizedToUpdate(form.password.data):
        # Add message
        app.logger.info('This is a POST and the form was validated.')
        dateToStore = GetDateToStore(form.date.data, form.is_am_service.data == 'am')
        app.logger.info(f'Message date: {dateToStore}')
        messageToStore = VideoMessage(title=form.title.data, description=form.description.data, youtube_id=form.youtube_id.data, timestamp=dateToStore)
        app.logger.info(messageToStore)
        db.session.add(messageToStore)
        db.session.commit()
        return redirect(url_for('list_messages'))
    else:
        app.logger.info(f'The form did not validate. FormMethod:{request.method}')
        
    # Get message data and return it
    # return render_template('login.html', title='Sign In', form=form, model = pageModel)
    app.logger.info('Go to Add Message page.')
    return render_template(
        'add_message.html',
        model = pageModel,
        form = form
    )

def GetDateToStore(date: date, isAmService: bool) -> datetime:
    if not bool(date):
        return datetime.utcnow()
        
    offsetHours = math.floor(abs(time.localtime().tm_gmtoff / (60*60)))
    hour = (10 if isAmService else 18) + offsetHours # 10am or 6pm plus offset
    return datetime(date.year, date.month, date.day, hour, 45, 0)

def AuthorizedToUpdate(password: str) -> bool:
    return app.config['DATA_SECRET'] == password and app.config['DATA_SECRET'] != 'beriberi'

@app.route('/delete-message', methods=['GET'])
def delete_message():
    password = request.args['confNum']
    if not AuthorizedToUpdate(password):
        app.logger.info('Not authorized to delete the message.')
    else:
        youtubeId = request.args["id"]
        app.logger.info(f'Delete message: {youtubeId}')
        message = VideoMessage.query.filter_by(youtube_id = youtubeId).first()
        if bool(message):
            app.logger.info('Deleting message')
            db.session.delete(message)
            db.session.commit()
        else:
            app.logger.info('Could not find the message to delete.')
    return redirect(url_for('list_messages'))

@app.route('/list-messages', methods=['GET'])
def list_messages():
    pageModel.messages = GetMessages()
    return render_template('list_messages.html', model = pageModel)

def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1986

def MapMessage(sequence: int, message: VideoMessage, image: Image) -> Message:
    result = Message(message.id)
    result.title = message.title
    result.timestamp = message.timestamp
    result.description = message.description
    result.youtube_id = message.youtube_id
    result.sequence = sequence
    
    if bool(image):
        result.image_file = image.filename
        result.image_description = image.description
        
    return result

def GetImages():
    return [Image('storm.jpg', 'Storm'), Image('man-walking-with-bag.jpg', 'Walking Man'), Image('bible-on-rock.jpg', 'Bible')]

def GetMessages(count: int = 0, includeImages: bool = False):
    messages = []
    imageList = []

    if bool(count):
        messageList = VideoMessage.query.order_by(VideoMessage.timestamp.desc()).limit(count).all()
    else:
        messageList = VideoMessage.query.order_by(VideoMessage.timestamp.desc()).all()

    if includeImages:
        imageList = GetImages()
    
    index = 0
    numOfImages = len(imageList)
    app.logger.info(f'{len(messageList)} video message were retrieved to display.')
    
    for message in messageList:
        messages.append(MapMessage(
            index, 
            message, 
            None if index >= numOfImages else imageList[index])) # Add a default image?
        index = index + 1

    return messages