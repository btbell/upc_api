from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'upc_api.db')
app.config['JWT_SECRET_KEY'] = 'super-secret' # string simplicity is just for testing

db = SQLAlchemy(app)
jwt = JWTManager(app)


# ######  CLI DATABASE COMMANDS  ######
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    test_user = User(name='Odie',
                     email='odie@test.com',
                     password='p^assword')

    db.session.add(test_user)
    db.session.commit()
    print('Database seeded!')


@app.route('/')
def home():
    return jsonify(message='hello pgh!')


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
    else:
        email = request.form['email']

    test = User.query.filter_by(email=email).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login success!", access_token=access_token)
    else:
        return jsonify(message="Bad email!"), 401


# ######  MODELS  ######
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


if __name__ == '__main__':
    app.run()
