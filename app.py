from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = "thisissecret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todo.sqlite')

db = SQLAlchemy(app)


# Database Tables

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)


# Routes

@app.route('/user', methods=['GET'])
def getAllUsers():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({ 'users': output })


@app.route('/user/<user_id>', methods=['GET'])
def getOneUser(user_id):
    return ''


@app.route('/user', methods=['POST'])
def createUser():
    data = request.get_json()
    hashedPassword = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], email=data['email'], password=hashedPassword, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
                     'status': 'ok',
                     'message': 'new user created successfully'
                   })


@app.route('/user/<user_id>', methods=['PUT'])
def promoteUser():
    return ''


@app.route('/user/<user_id>', methods=['DELETE'])
def deleteUser():
    return ''


if __name__ == '__main__':
    app.run(debug=True)
