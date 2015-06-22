from flask.ext.wtf import Form
from wtforms import StringField, TextField
from wtforms.validators import DataRequired, Length, Optional


class LoginForm(Form):
    query = StringField('query')
    opQuery = StringField('opQuery')

class RandomForm(Form):
	query = TextField('one')
	opQuery = TextField('two')
