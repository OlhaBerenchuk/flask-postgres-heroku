from flask import Flask, render_template, request, flash,\
    redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from forms import UserForm, FileForm, DocumentationForm, LanguageForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://ndwwwbpuuiwdli:087f70d386426f46deacd7da8a68df6454e345a1a9cb078b57bb586bf244e00a@ec2-107-21-200-103.compute-1.amazonaws.com:5432/d4bd6o61l2b9h7"
app.config['SECRET_KEY'] = "8che9fj49fjsofjd93jfi59dje8b0e"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    # by default tablename is 'user' (lower classname), but we change it
    __tablename__ = 'users'
    # id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(45), unique=True, nullable=False)
    created_at = db.Column(db.String(20))
    name = db.Column(db.String(45))
    files = db.relationship('File', backref='user')

    def __repr__(self):
        return '<User %r>' % self.name


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45))
    link = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))

    def __repr__(self):
        return '<FIle %r>' % self.id


class Language(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45))
    version = db.Column(db.String(20))
    documentation_id = db.Column(db.Integer, db.ForeignKey('documentations.id'))

    def __repr__(self):
        return '<Language %r>' % self.name


class Documentation(db.Model):
    __tablename__ = 'documentations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.String(100))
    actor = db.Column(db.String(45))

    def __repr__(self):
        return '<Documentation %r>' % self.link


db.create_all()
