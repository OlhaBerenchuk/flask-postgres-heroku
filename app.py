from flask import Flask, render_template, request, flash,\
    redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import UserForm, FileForm, DocumentationForm
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


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


@app.route('/', methods=['GET'])
def home():
    return render_template('header.html')


@app.route('/user', methods=['GET'])
def users():
    result = []
    form = UserForm()
    users = User.query.all()
    for user in users:
        result.append([user.id, user.name, user.email])
    return render_template('users.html', rows=result, form=form)


@app.route('/insert_user', methods=['post'])
def insert_user():
    form = UserForm()
    name = form.name.data
    email = form.email.data
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return redirect('/user')


@app.route('/update_user', methods=['post'])
def update_user():
    id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    user = User.query.filter_by(id=id).first()
    user.name = name
    user.email = email
    db.session.add(user)
    db.session.commit()
    return redirect('/user')


@app.route('/delete_user/<string:id>', methods=['get'])
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect('/user')


@app.route('/file', methods=['GET'])
def files():
    result = []
    form = FileForm()
    files = File.query.all()
    for file in files:
        result.append([file.id, file.name, file.link])
    return render_template('files.html', rows=result, form=form)


@app.route('/insert_file', methods=['post'])
def insert_file():
    form = FileForm()
    name = form.name.data
    link = form.link.data
    file = File(name=name, link=link)
    db.session.add(file)
    db.session.commit()
    return redirect('/file')


@app.route('/update_file', methods=['post'])
def update_file():
    id = request.form['id']
    name = request.form['name']
    link = request.form['link']
    file = User.query.filter_by(id=id).first()
    file.name = name
    file.link = link
    db.session.add(file)
    db.session.commit()
    return redirect('/file')


@app.route('/delete_file/<string:id>', methods=['get'])
def delete_file(id):
    file = File.query.filter_by(id=id).first()
    db.session.delete(file)
    db.session.commit()
    return redirect('/file')


@app.route('/doc', methods=['GET'])
def doc():
    result = []
    form = DocumentationForm()
    docs = Documentation.query.all()
    for doc in docs:
        result.append([doc.id, doc.actor, doc.link])
    return render_template('doc.html', rows=result, form=form)


@app.route('/insert_doc', methods=['post'])
def insert_doc():
    form = DocumentationForm()
    actor = form.actor.data
    link = form.link.data
    doc = Documentation(actor=actor, link=link)
    db.session.add(doc)
    db.session.commit()
    return redirect('/doc')


@app.route('/update_doc', methods=['post'])
def update_doc():
    id = request.form['id']
    actor = request.form['actor']
    link = request.form['link']
    doc = Documentation.query.filter_by(id=id).first()
    doc.actor = actor
    doc.link = link
    db.session.add(doc)
    db.session.commit()
    return redirect('/doc')


@app.route('/delete_doc/<string:id>', methods=['get'])
def delete_doc(id):
    doc = Documentation.query.filter_by(id=id).first()
    db.session.delete(doc)
    db.session.commit()
    return redirect('/doc')


@app.route('/dashboard', methods=['get'])
def dashboard():
    labels = ['Users', 'Files', 'Documentation']
    count = [
        len(User.query.all()),
        len(File.query.all()),
        len(Documentation.query.all())
    ]

    fig, ax = plt.subplots()
    ax.pie(count, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    ax.set_title('Count rows')
    pie = "pie"+str(datetime.now())+".png"
    plt.savefig(f'./static/images/{pie}')

    plt.clf()

    objects = ('Admin', 'Not admin')
    y_pos = np.arange(len(objects))
    admin_count = (Documentation.query.filter_by(actor='Admin').count())
    performance = [admin_count, len(Documentation.query.all()) - admin_count]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Usage')
    plt.title('Actors documentations')
    bar = "bar" + str(datetime.now()) + ".png"
    plt.savefig(f'./static/images/{bar}')

    return render_template('dash.html', bar=bar, pie=pie)


if __name__ == '__main__':
    app.run(debug=False)
