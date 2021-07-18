from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField
#from wtforms.fields.core import SelectField
from datetime import date
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    login = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class DonateForm(FlaskForm):
    submit = SubmitField('Donate')

class AddMessageForm(FlaskForm):
    style = {'class': 'form-control'}
    id = HiddenField('Id')
    title = StringField('Title', [DataRequired(message='Please enter a title for this message.'), Length(max=128, message='Max 128 characters.')], render_kw=style)
    description = StringField('Description', [Length(max=256, message='Max 256 characters.')], render_kw=style)
    date = DateField('Date of message', [DataRequired(message='Please enter the date this message was delivered.')], default=date.today, render_kw=style)
    is_am_service = SelectField('Morning or eventing service?', [DataRequired()], choices=[('am', 'AM'), ('pm', 'PM')], default='am', render_kw={'class': 'form-select'})
    youtube_id = StringField('YouTube Key', [DataRequired(message='Please supply the key for this video.')], render_kw=style)
    submit = SubmitField('OK', render_kw={'class': 'btn btn-primary'})
    password = PasswordField('Secret', [DataRequired(message='If you do not have this value please contact your system administrator.'), Length(min=1, max=100, message='This is not valid.')], render_kw=style)
