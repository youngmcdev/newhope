from flask import render_template
from app import app
from datetime import datetime, date, time
# To start the application:
# 1) Open a command console and change directory to the root of the application/repository
# 2) Activate the environment by executing "venv\Scripts\activate"
# 3) Set the FLASK_APP environment variable "set FLASK_APP=<name_of_python_file>" example "set FLASK_APP=newhope.py"
#        Note: This is being done via the .flaskenv file
# 4) Execute "flask run"

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Mark'}
    currentDate = datetime.now()
    today = datetime.date(currentDate).strftime("%d-%b-%Y")
    now = datetime.time(currentDate).strftime("%H:%M:%S")
    sermonList = [
        {'title':'Title One', 'image':'', 'url':'', 'description':'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Neque gravida in fermentum et sollicitudin. Mollis nunc sed id semper risus. Luctus venenatis lectus magna fringilla urna porttitor rhoncus dolor purus.'},
        {'title':'Title Two', 'image':'', 'url':'', 'description':'Congue nisi vitae suscipit tellus mauris a diam maecenas. Orci sagittis eu volutpat odio facilisis mauris. Suscipit tellus mauris a diam maecenas sed enim ut. Nec dui nunc mattis enim ut tellus elementum sagittis.'},
        {'title':'Title Three', 'image':'', 'url':'', 'description':'Diam sollicitudin tempor id eu nisl nunc mi ipsum faucibus. Orci nulla pellentesque dignissim enim sit amet venenatis urna cursus. Cum sociis natoque penatibus et magnis dis parturient. Eget magna fermentum iaculis eu non diam.'}
        ]
    return render_template('index.html', title='New Hope Baptist Church', user=user, time=now, date=today, sermons=sermonList)