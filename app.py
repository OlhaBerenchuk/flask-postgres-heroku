import uuid
import json
import plotly
import plotly.graph_objs as go

from math import fabs

from sqlalchemy.sql import func
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from forms import UserForm, FileForm, DocumentationForm, SoftForm


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


@app.route('/', methods=['GET'])
def home():
    return render_template('header.html')


@app.route('/get', methods=['GET'])
def get():
    soft1 = Soft(soft_name=uuid.uuid4(), soft_price=1, soft_vendor=5, soft_version='soft_version1')
    soft2 = Soft(soft_name=uuid.uuid4(), soft_price=2, soft_vendor=6, soft_version='soft_version2')
    soft3 = Soft(soft_name=uuid.uuid4(), soft_price=3, soft_vendor=7, soft_version='soft_version3')
    for soft in (soft1, soft2, soft3):
        db.session.add(soft)
        db.session.commit()
    return redirect('/pup')


@app.route('/pup', methods=['GET'])
def softs():
    result = []
    form = SoftForm()
    softs = Soft.query.all()
    for soft in softs:
        result.append([soft.soft_name, soft.soft_price, soft.soft_vendor, soft.soft_version])
    return render_template('softs.html', rows=result, form=form)


@app.route('/insert_soft', methods=['post'])
def insert_soft():
    form = SoftForm()
    name = form.name.data
    price = form.price.data
    try:
        price = int(price)
    except Exception:
        return render_template('validate.html', error='Price is not integer value.')
    else:
        if price < 0:
            return render_template('validate.html', error='Price must be more than 0.')
    vendor = form.vendor.data
    try:
        vendor = int(vendor)
    except Exception:
        return render_template('validate.html', error='Vendor is not integer value.')
    else:
        if fabs(vendor) > 10:
            return render_template('validate.html', error='Vendor is not between -10 an 10.')
    version = form.version.data
    soft = Soft(soft_name=name, soft_price=price, soft_vendor=vendor, soft_version=version)
    db.session.add(soft)
    db.session.commit()
    return redirect('/pup')


@app.route('/update_soft', methods=['post'])
def update_soft():
    id = request.form['id']
    name = request.form['name']
    price = request.form['price']
    try:
        price = int(price)
    except Exception:
        return render_template('validate.html', error='Price is not integer value.')
    else:
        if price < 0:
            return render_template('validate.html', error='Price must be more than 0.')
    vendor = request.form['vendor']
    try:
        vendor = int(vendor)
    except Exception:
        return render_template('validate.html', error='Vendor is not integer value.')
    else:
        if fabs(vendor) > 10:
            return render_template('validate.html', error='Vendor is not between -10 and 10.')
    version = request.form['version']
    soft = Soft.query.filter_by(soft_name=id).first()
    soft.soft_name = name
    soft.soft_price = price
    soft.soft_vendor = vendor
    soft.soft_version = version
    db.session.add(soft)
    db.session.commit()
    return redirect('/pup')


@app.route('/delete_soft/<string:id>', methods=['get'])
def delete_soft(id):
    soft = Soft.query.filter_by(soft_name=id).first()
    db.session.delete(soft)
    db.session.commit()
    return redirect('/pup')


@app.route('/user', methods=['GET'])
def users():
    result = []
    form = UserForm()
    users = User.query.all()
    for user in users:
        result.append([user.user_email, user.user_name])
    return render_template('users.html', rows=result, form=form)


@app.route('/insert_user', methods=['post'])
def insert_user():
    form = UserForm()
    name = form.name.data
    email = form.email.data
    user = User(user_name=name, user_email=email)
    db.session.add(user)
    db.session.commit()
    return redirect('/user')


@app.route('/update_user', methods=['post'])
def update_user():
    id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    user = User.query.filter_by(user_email=id).first()
    user.user_name = name
    user.user_email = email
    db.session.add(user)
    db.session.commit()
    return redirect('/user')


@app.route('/delete_user/<string:id>', methods=['get'])
def delete_user(id):
    user = User.query.filter_by(user_email=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect('/user')


@app.route('/file', methods=['GET'])
def files():
    result = []
    form = FileForm()
    files = File.query.all()
    for file in files:
        result.append([file.file_name, file.file_link])
    return render_template('files.html', rows=result, form=form)


@app.route('/insert_file', methods=['post'])
def insert_file():
    form = FileForm()
    name = form.name.data
    link = form.link.data
    file = File(file_name=name, file_link=link)
    db.session.add(file)
    db.session.commit()
    return redirect('/file')


@app.route('/update_file', methods=['post'])
def update_file():
    id = request.form['id']
    name = request.form['name']
    link = request.form['link']
    file = File.query.filter_by(file_name=id).first()
    file.file_name = name
    file.file_link = link
    db.session.add(file)
    db.session.commit()
    return redirect('/file')


@app.route('/delete_file/<string:id>', methods=['get'])
def delete_file(id):
    file = File.query.filter_by(file_name=id).first()
    db.session.delete(file)
    db.session.commit()
    return redirect('/file')


@app.route('/doc', methods=['GET'])
def doc():
    result = []
    form = DocumentationForm()
    docs = Documentation.query.all()
    for doc in docs:
        result.append([doc.documentation_link, doc.documentation_actor])
    return render_template('doc.html', rows=result, form=form)


@app.route('/insert_doc', methods=['post'])
def insert_doc():
    form = DocumentationForm()
    actor = form.actor.data
    link = form.link.data
    doc = Documentation(documentation_actor=actor, documentation_link=link)
    db.session.add(doc)
    db.session.commit()
    return redirect('/doc')


@app.route('/update_doc', methods=['post'])
def update_doc():
    id = request.form['id']
    actor = request.form['actor']
    link = request.form['link']
    doc = Documentation.query.filter_by(documentation_link=id).first()
    doc.documentation_actor = actor
    doc.documentation_link = link
    db.session.add(doc)
    db.session.commit()
    return redirect('/doc')


@app.route('/delete_doc/<string:id>', methods=['get'])
def delete_doc(id):
    doc = Documentation.query.filter_by(documentation_link=id).first()
    db.session.delete(doc)
    db.session.commit()
    return redirect('/doc')


@app.route('/dashboard', methods=['get'])
def dashboard():
    query1 = (
        db.session.query(
            User.user_name,
            func.count(File.file_name).label('file_name')
        ).join(File, User.user_email == File.user_name_fk).
            group_by(User.user_name)
    ).all()

    query2 = (
        db.session.query(
            Language.language_name,
            func.count(File.file_name).label('file_name')
        ).join(File, Language.language_name == File.language_name_fk).
            group_by(Language.language_name)
    ).all()

    user_name, file_count = zip(*query1)
    print(user_name, file_count)
    bar = go.Bar(
        x=user_name,
        y=file_count
    )

    vacancy_name, criterion_count = zip(*query2)
    print(vacancy_name, criterion_count)
    pie = go.Pie(
        labels=vacancy_name,
        values=criterion_count
    )

    data = {
        "bar": [bar],
        "pie": [pie]
    }
    graphs_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dash.html', graphsJSON=graphs_json)


@app.route('/plot', methods=['GET'])
def plot():
    softs = Soft.query.all()
    names = []
    prices = []
    for soft in softs:
        names.append(soft.soft_name)
        prices.append(soft.soft_price)

    print(names, prices)
    pie = go.Pie(
        labels=tuple(names),
        values=tuple(prices)
    )

    data = {
        "pie": [pie]
    }
    graphs_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dash.html', graphsJSON=graphs_json)


if __name__ == '__main__':
    app.run(debug=False)
