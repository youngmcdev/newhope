from flask import render_template
from app import app
from app.routes import PageTemplate

pageModel = PageTemplate('New Hope Baptist Church')

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html', model=pageModel), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', model=pageModel), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', model=pageModel), 500