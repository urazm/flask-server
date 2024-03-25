from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

#заглушка
users = {
    'user1': 'password1'
}

@app.route('register', methods=['POST'])
def register():
    username = request.json.get('login', None)
    password = request.json.get('password', None)

    if username is None or password is None:
        return jsonify({"msg": "Необходимо указать имя пользователя и пароль"}), 400

    if username in users:
        return jsonify({"msg": "Пользователь с таким именем уже существует"}), 400

    users[username] = password
    return jsonify({"msg": "Пользователь успешно зарегистрирован"}), 201


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if username not in users or users[username] != password:
        return jsonify({"msg": "Неверные учетные данные"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


# Пример защищенного маршрута
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/test', methods=['GET'])
def test():
    return "test", 200



if __name__ == "__main__":
    app.run(debug=True)
