from app import app
from datetime import datetime, date, time

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Mark'}
    currentDate = datetime.now()
    today = datetime.date(currentDate).strftime("%d-%b-%Y")
    currentTime = datetime.time(currentDate).strftime("%H:%M:%S")
    return '''
<html>
<head>
<title>Home Page - Microblog</title>
</head>
<body>
<h1>''' + today + '''</h1>
<h2>Hello, ''' + user['username'] + '''! The time is ''' + currentTime + '''</h2>
</body>
</html>'''