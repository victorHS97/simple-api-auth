from flask import Flask, request, jsonify
from database import db
from models.user import User
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

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


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"Message": "Logout realizado com sucesso"})


@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"Message": "Cadastro realizado com sucesso"})
    return jsonify({"message": "Dados invalidos"})


@app.route('/user/<int:id_user>', methods=['GET'])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)
    if user:
        return jsonify({"message": f'Usuario encontrado: {user.username}'})
    return jsonify({"message": "usuario não econtrado"})


@app.route('/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    user = User.query.get(id_user)
    data = request.json
    if user:
        user.password = data.get('password')
        db.session.commit()
        return jsonify({"message": f" usuario {user.username} atualizado com sucesso"})
    return jsonify({"message": "Usuario não econtrado"})


@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
    if id_user == current_user.id:
        return jsonify({"message": "Deletação não permitida"})
    user = User.query.get(id_user)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f'usuario {user.username} foi excluido com sucesso'})
    return jsonify({"message": "usuario não encontrado"})


@app.route('/hello-world', methods=['GET'])
def hello_world():
    return "Hello World"


if __name__ == '__main__':
    app.run(debug=True)
