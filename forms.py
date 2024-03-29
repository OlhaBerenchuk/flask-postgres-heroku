from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import Email, InputRequired, URL


class UserForm(Form):
    name = StringField('name', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Email(message="It\'s not an email!")])


class SoftForm(Form):
    name = StringField('name', validators=[InputRequired()])
    price = IntegerField('price')
    vendor = IntegerField('vendor')
    version = StringField('version')


class FileForm(Form):
    name = StringField('name', validators=[InputRequired()])
    link = StringField('link', validators=[InputRequired(), URL(message="It\'s not an url")])


class DocumentationForm(Form):
    link = StringField('link', validators=[InputRequired(), URL(message="It\'s not an url")])
    actor = StringField('actor', validators=[InputRequired()])


class LanguageForm(Form):
    name = StringField('name', validators=[InputRequired()])
    version = StringField('version', validators=[InputRequired()])
