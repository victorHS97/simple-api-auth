from flask import Flask, request, jsonify
from database import db
from models.user import User
from flask_login import LoginManager

# LIBS
login_manager = LoginManager
app = Flask(__name__)

# CONFIG FLASK
app.config['SECRET_KEY'] = "your secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
login_manager.init_app(app)


@app.route('/login', methods=['POST'])
def login():
    data = request.json()
    username = data.get('username')
    password = data.get('password')
    if username and password:
        # login
    return jsonify({"Message": "Credenciais invalidas"}), 400


@app.route('/hello-world', methods=['GET'])
def hello_world():
    return "Hello World"


if __name__ == '__main__':
    app.run(debug=True)
