from flask import Flask, render_template, request, flash,\
    redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import UserForm, FileForm, DocumentationForm, LanguageForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://mqdhozgzgkfpff:fed657b27227a549947a8e4aac54b166fbe01b11457732533727885cd7f844de@ec2-54-225-113-7.compute-1.amazonaws.com:5432/d13tkjgp6f6and"
app.config['SECRET_KEY'] = "8che9fj49fjsofjd93jfi59dje8b0e"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):

    __tablename__ = 'orm_user'

    user_email = db.Column(db.String(45), primary_key=True, nullable=False)
    user_name = db.Column(db.String(45))

    files = db.relationship('File')


class File(db.Model):

    __tablename__ = 'orm_file'

    file_name = db.Column(db.String(45), primary_key=True, nullable=False)
    file_link = db.Column(db.String(100))

    user_name_fk = db.Column(db.String(45), db.ForeignKey('orm_user.user_email'))
    language_name_fk = db.Column(db.String(45), db.ForeignKey('orm_language.language_name'))

    soft_name_fk = db.relationship('Soft', secondary='file_has_soft')


class FileHasSoft(db.Model):

    __tablename__ = 'file_has_soft'

    file_name_fk = db.Column(db.String(45), db.ForeignKey('orm_file.file_name'), primary_key=True)
    soft_name_fk = db.Column(db.String(45), db.ForeignKey('orm_soft.soft_name'), primary_key=True)


class Soft(db.Model):

    __tablename__ = 'orm_soft'

    soft_name = db.Column(db.String(45), primary_key=True, nullable=False)
    soft_price = db.Column(db.Integer)
    soft_vendor = db.Column(db.Integer)
    soft_version = db.Column(db.String(45))

    file_name_fk = db.relationship('File', secondary='file_has_soft')


class Language(db.Model):

    __tablename__ = 'orm_language'

    language_name = db.Column(db.String(45), primary_key=True)
    language_version = db.Column(db.String(20))

    documentation_name_fk = db.Column(db.String(100), db.ForeignKey('orm_documentation.documentation_link'))


class Documentation(db.Model):
    __tablename__ = 'orm_documentation'

    documentation_link = db.Column(db.String(100), primary_key=True, nullable=False)
    documentation_actor = db.Column(db.String(45))


db.create_all()
