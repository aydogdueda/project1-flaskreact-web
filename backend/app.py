# app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from flask_cors import CORS
import os 

app = Flask(__name__)

# CORS ayarı: localhost:3000'den gelen isteklere izin veriyoruz.
# Eğer frontend'iniz farklı bir portta veya domainde çalışacaksa, burayı güncellemeyi unutmayın.
# Geliştirme aşamasında tüm kaynaklara (*) izin vermek de yaygındır:
# CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, origins="http://localhost:3000")


# Veritabanı bağlantı ayarları
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    'DATABASE_URL',
    'mysql+pymysql://root:@localhost/flaskreact?charset=utf8mb4' # Yerel geliştirme için varsayılan
)
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
    # Veritabanı bağlantısını test etmek için basit bir try-except bloğu ekleyebiliriz
    try:
        all_users = Users.query.all()
        results = users_schema.dump(all_users)
        return jsonify(results)
    except Exception as e:
        # Hata durumunda loglama veya hata mesajı döndürme
        print(f"Veritabanından kullanıcıları çekerken hata oluştu: {e}")
        return jsonify({"error": "Veritabanına bağlanılamadı veya veri çekilemedi", "details": str(e)}), 500

@app.route('/userdetails/<int:id>', methods=['GET'])
def userdetails(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
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
        try:
            db.create_all()
            print("Veritabanı tabloları oluşturuldu (eğer yoksa).")
        except Exception as e:
            print(f"Veritabanı tabloları oluşturulurken hata: {e}")
    
    # app.run() varsayılan olarak debug=True ile gelir.
    # Üretim ortamında debug=False olmalıdır, ancak yerel geliştirme için True olması faydalıdır.
    # Port belirtmezseniz varsayılan olarak 5000'i kullanır.
    app.run(debug=True, port=5000)
