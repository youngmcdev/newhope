from flask import render_template
from app import app
from app.routes import PageTemplate

@app.errorhandler(404)
def not_found_error(error):
    pageModel = PageTemplate()
    return render_template('404.html', model=pageModel), 404

@app.errorhandler(500)
def internal_error(error):
    pageModel = PageTemplate()
    return render_template('500.html', model=pageModel), 500