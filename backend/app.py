from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:@localhost/flaskreact'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, email):
        self.name = name
        self.email = email

# SCHEMA
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
    date = ma.auto_field(dump_only=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# ROUTES
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/listusers', methods=['GET'])
def listusers():
    all_users = Users.query.all()
    results = users_schema.dump(all_users)  # <-- DÜZELTME: dump
    return jsonify(results)

@app.route('/userdetails/<int:id>', methods=['GET'])
def userdetails(id):
    user= Users.query.get(id)
    return user_schema.jsonify(user)

@app.route('/userupdate/<int:id>', methods=['PUT'])
def userupdate(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    name = request.json.get('name', user.name)
    email = request.json.get('email', user.email)

    user.name = name
    user.email = email

    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/userdelete/<int:id>', methods=['DELETE'])
def userdelete(id): 
    user = Users.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/useradd', methods=['POST'])
def useradd():
    name = request.json['name']
    email = request.json['email']

    users = Users(name, email)
    db.session.add(users)
    db.session.commit()
    return user_schema.jsonify(users)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
