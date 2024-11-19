from flask import Flask, request, jsonify
from database import db
from models.user import User
from flask_login import LoginManager, login_user, current_user

# LIBS
login_manager = LoginManager()
app = Flask(__name__)

# CONFIG FLASK
app.config['SECRET_KEY'] = "your secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
login_manager.init_app(app)
# informa qual rota é a de login para o gerenciador Login Manager
login_manager.login_view = 'login'


@login_manager.user_loader  # carrega uma sessão com informações do usuario
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    # abaixo é feita uma busca no banco o usuario pelo username
    user = User.query.filter_by(username=username).first()
    if user and password == user.password:
        login_user(user)
        return jsonify({"Message": "Autenticação feita com sucesso"})

    return jsonify({"Message": "Credenciais invalidas"}), 400


@app.route('/hello-world', methods=['GET'])
def hello_world():
    return "Hello World"


if __name__ == '__main__':
    app.run(debug=True)
