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
from app.models import VideoMessage, Speaker
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
        self.is_published = False
        self.speaker_id = 0
        self.speaker = ''
        self.speaker_is_guest = False
        self.speaker_icon_file_name = ''
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
    app.logger.info('index.html')
    return render_template('index.html', model = pageModel)

@app.route('/give')
def give():
    return render_template('give.html', model = pageModel)

@app.route('/events')
def events():
    app.logger.info('events.html')
    return render_template('events.html', model = pageModel)

@app.route('/introduction')
def introduction():
    app.logger.info('introduction.html')
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
    app.logger.info('messages.html')
    pageModel.messages = GetMessages(3, True)
    return render_template('messages.html', model = pageModel)

@app.route('/guests')
def guests():
    app.logger.info('guests.html')
    return render_template('guests.html', model = pageModel)

@app.route('/live')
def live():
    app.logger.info('live.html')
    return render_template('live.html', model = pageModel)

@app.route('/services')
def services():
    app.logger.info('services.html')
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
    app.logger.info('donateco.html')
    return render_template('donateco.html', model = pageModel)

@app.route("/donateco-config")
def get_publishable_key():
    stripeConfig = {"publicKey": stripeKeys["publishableKey"]}
    # MCY - fix this bug - seem to be referencing publicKey incorrectly
    # app.logger.info(f'Getting the publishable key {stripeConfig.publicKey}')
    app.logger.info('donateco-config')
    return jsonify(stripeConfig)

@app.route('/donatecu', methods = ['GET', 'POST'])
def donatecu():
    app.logger.info('donatecu.html')
    form = DonateForm
    return render_template('donatecu.html', form = form, model = pageModel)

@app.route('/donate', methods = ['GET', 'POST'])
def donate():
    # this route does not actually 'checkout'
    app.logger.info('donate.html')
    form = DonateForm
    return render_template('donate.html', form = form, model = pageModel)

@app.route('/create-checkout-session', methods = ['POST'])
def create_checkout_session():
    baseMessage = 'create-checkout-session:'
    try:
        dollarAmount = math.floor(float(request.form['amount']))
        amount = dollarAmount * 100
        app.logger.info(f'{baseMessage} AmountPosted:' + str(amount))
        stripe.api_key = stripeKeys["secretKey"]
        # This is set in the Stripe dashboard. However, we can override that here
        stripe.api_version = '2020-08-27'
        successUrl = url_for('checkout_success', _external = True) + "?session_id={CHECKOUT_SESSION_ID}"
        cancelUrl = url_for('checkout_cancel', _external = True)
        app.logger.info(f'{baseMessage} SuccessUrl:{successUrl}')
        app.logger.info(f'{baseMessage} CancelUrl:{cancelUrl}')
        app.logger.error('This is NOT an error. A checkout session has been requested for donation.')

        session = stripe.checkout.Session.create(
            #payment_method_types = ['card'],
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
            customer_creation = 'if_required',
            success_url = successUrl,
            cancel_url = cancelUrl
        )
        app.logger.info(f'{baseMessage} Session Object: {session}')

        sessionId = ''
        if(session):
            app.logger.info(f'{baseMessage} session ID {session.id}')
            sessionId = session.id
        return jsonify(id = sessionId)
    except Exception as e:
        app.logger.error(f'{baseMessage} An exception was thrown creating a stripe checkout sesson. ' + str(e))
        return jsonify(error=str(e)), 403

@app.route('/checkout-success')
def checkout_success():
    baseMessage = 'checkout-success:'
    successModel = PageTemplate('Thank you!')
    sessionIdFromStripeSession = request.args.get('session_id')
    app.logger.info(f'{baseMessage} Session ID from URL: "{sessionIdFromStripeSession}"')
    if(sessionIdFromStripeSession and sessionIdFromStripeSession.strip()):
        app.logger.info(f'{baseMessage} Attempt to get a session from Stripe for the session ID.')
        try:
            session = stripe.checkout.Session.retrieve(sessionIdFromStripeSession)
            app.logger.info(f'{baseMessage} Session object: {session}')
            app.logger.info(f'{baseMessage} Attempt to get a customer object from Stripe for CustomerId:"{session.customer}"')
            customer = stripe.Customer.retrieve(session.customer)
            app.logger.info(f'{baseMessage} Customer object: {customer}')
        except:
            app.logger.info(f'{baseMessage} An error occured with the Stripe API. We could not retrieve the customer information after the successful payment processing. Returning default data to the view.')
            session = MockStripeSession()
            customer = session.customer
        
        if(customer):
            successModel.customerEmail = customer.email or ''
            successModel.customerName = customer.name or customer.email or ''

        successModel.donationAmount = int(session.amount_total/100)
        app.logger.error('This is NOT an error. A checkout session has been completed for donation.')

    return render_template('success.html', model = successModel)

@app.route('/checkout-cancel')
def checkout_cancel():
    app.logger.info('checkout-cancel: A checkout was cancelled.')
    app.logger.error('This is NOT an error. A checkout session has been canceled for donation.')
    return render_template('cancel.html', model = pageModel)

@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    baseMessage = 'create-payment-intent:'
    app.logger.error('This is NOT an error. A payment intent has been requested for donation.')
    try:
        app.logger.info(f'{baseMessage} Begin creating payment intent')
        app.logger.info(request.data)
        data = json.loads(request.data)
        app.logger.info(data)
        # A PaymentIntent tracks the customer's payment lifecycle, keeping track of any failed payment attempts and ensuring the customer is only charged once.
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='usd'
        )
        app.logger.info(f'{baseMessage} End creating payment intent')
        # Return the PaymentIntent's client secret in the response to finish the payment on the client.
        return jsonify({
            'clientSecret': intent['client_secret']
        })
        
    except Exception as e:
        app.logger.error(f'{baseMessage} An exception was thrown creating a stripe payment intent. ' + str(e))
        return jsonify(error=str(e)), 403

@app.route('/update-message', methods=['GET','POST'])
def update_message():
    baseMessage = 'update-message:'
    form = AddMessageForm(request.form)
    form.speaker.choices = GetSpeakerList()

    if form.validate_on_submit() and AuthorizedToUpdate(form.password.data):
        messageId = int(form.id.data)
        app.logger.info(f'{baseMessage} Form validated. Message ID: {messageId}')
        message = VideoMessage.query.filter_by(id = messageId).first()
        if bool(message):
            app.logger.info(f'{baseMessage} Update message: {message}')
            dateToStore = GetDateToStore(form.date.data, form.is_am_service.data == 'am')
            app.logger.info(f'{baseMessage} Message date: {dateToStore}')
            message.title = form.title.data
            message.description = form.description.data
            message.timestamp = dateToStore
            message.youtube_id = form.youtube_id.data
            message.is_published = True if form.is_published.data == '1' else False
            message.speaker_id = int(form.speaker.data)
            db.session.commit()
        else:
            app.logger.info(f'{baseMessage} Could not find the message to update.')

        return redirect(url_for('list_messages'))
    else:
        app.logger.info(f'{baseMessage} The form did not validate. FormMethod:{request.method}')

    if request.method == 'GET':
        messageId = int(request.args['id'])
        app.logger.info(f'{baseMessage} Message ID: {messageId}')
        message = VideoMessage.query.filter_by(id = messageId).first()
        app.logger.info(f'{baseMessage} Display message: {message}')
        if bool(message):
            form.id.data = messageId
            form.is_am_service.data = 'am' if message.timestamp.hour == 14 or message.timestamp.hour == 15 else 'pm'
            form.title.data = message.title
            form.description.data = message.description
            form.date.data = message.timestamp
            form.youtube_id.data = message.youtube_id
            form.is_published.data = '1' if message.is_published else '0'
            form.speaker.data = str(message.speaker_id)

    return render_template(
        'update_message.html',
        model = pageModel,
        form = form
    )

@app.route('/add-message', methods=['GET', 'POST'])
def add_message():
    baseMessage = 'add-message:'
    if request.method != 'POST':
        app.logger.info(f'{baseMessage} This is not a POST: {request.method}')

    #app.logger.info(request.form)
    form = AddMessageForm(request.form)
    form.speaker.choices = GetSpeakerList()
    #app.logger.info(f'value passed in {form.password.data}')
    if form.validate_on_submit() and AuthorizedToUpdate(form.password.data):
        # Add message
        app.logger.info(f'{baseMessage} This is a POST and the form was validated.')
        dateToStore = GetDateToStore(form.date.data, form.is_am_service.data == 'am')
        isPublished = True if form.is_published.data == '1' else False
        app.logger.info(f'{baseMessage} Message date: {dateToStore}')
        messageToStore = VideoMessage(title=form.title.data, description=form.description.data, youtube_id=form.youtube_id.data, timestamp=dateToStore, speaker_id=int(form.speaker.data), is_published=isPublished)
        app.logger.info(messageToStore)
        db.session.add(messageToStore)
        db.session.commit()
        return redirect(url_for('list_messages'))
    else:
        app.logger.info(f'{baseMessage} The form did not validate. FormMethod:{request.method}')
        
    # Get message data and return it
    # return render_template('login.html', title='Sign In', form=form, model = pageModel)
    
    app.logger.info(f'{baseMessage} Go to Add Message page.')
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
    baseMessage = 'delete-message:'
    password = request.args['confNum']
    if not AuthorizedToUpdate(password):
        app.logger.info(f'{baseMessage} Not authorized to delete the message.')
    else:
        youtubeId = request.args["id"]
        app.logger.info(f'{baseMessage} Delete message: {youtubeId}')
        message = VideoMessage.query.filter_by(youtube_id = youtubeId).first()
        if bool(message):
            app.logger.info(f'{baseMessage} Deleting message')
            db.session.delete(message)
            db.session.commit()
        else:
            app.logger.info(f'{baseMessage} Could not find the message to delete.')
    return redirect(url_for('list_messages'))

@app.route('/list-messages', methods=['GET'])
def list_messages():
    pageModel.messages = GetMessages()
    return render_template('list_messages.html', model = pageModel)

@app.route('/message-archive', methods=['GET'])
def message_archive():
    app.logger.info('message_archive.html')
    pageModel.messages = GetMessages()
    return render_template('message_archive.html', model = pageModel)

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
    result.speaker_id = message.speaker_id
    result.speaker = f'{message.speaker.first_name} {message.speaker.last_name}'
    result.speaker_is_guest = message.speaker.is_guest
    result.speaker_icon_file_name = message.speaker.icon_file_name
    result.is_published = message.is_published
    result.sequence = sequence
    
    if bool(image):
        result.image_file = image.filename
        result.image_description = image.description
        
    return result

def GetImages():
    return [Image('storm.jpg', 'Storm'), Image('man-walking-with-bag.jpg', 'Walking Man'), Image('bible-on-rock.jpg', 'Bible')]

def GetSpeakerList():
    speakers = Speaker.query.order_by(Speaker.last_name.asc()).all()
    speakerList = [(s.id, f'{s.first_name} {s.last_name}') for s in speakers]
    return speakerList

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
