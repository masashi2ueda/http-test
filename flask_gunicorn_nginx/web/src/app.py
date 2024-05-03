from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# @app.route('/')
# def hello():
#     name = "Hello World"
#     return name

# @app.route('/good')
# def good():
#     name = "Good"
#     return name


# @app.route('/sleep1sec')
# def sleep1sec():
#     time.sleep(1)
#     name = "sleep1sec_succes"
#     return name

# ディクショナリ
users = [
    {"user_id": "1", "name": "tujimura", "age": 11},
    {"user_id": "2", "name": "mori", "age": 20},
    {"user_id": "3", "name": "shimada", "age": 50},
    {"user_id": "4", "name": "kyogoku", "age": 70}]

@app.route('/good')
def good():
    name = "Good"
    return name

@app.route('/', methods=['GET'])
def get_users():
    # GETリクエストを処理
    age = request.args.get('age')
    if age:
        return jsonify(list(filter(lambda user: user['age'] == int(age), users)))
    return jsonify(users)

@app.route('/', methods=['POST'])
def post_user():
    # POSTリクエストを処理
    data = request.get_json()
    users.append(data)
    return jsonify(users), 201

@app.route('/<user_id>', methods=['PUT'])
def put_user(user_id):
    # PUTリクエストを処理
    data = request.get_json()
    res_users = list(map(lambda user: user.update(data) or user if user['user_id'] == user_id else user, users))
    return jsonify(res_users)

@app.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    # DELETEリクエストを処理
    res_users = list(filter(lambda user: user['user_id'] != user_id, users))
    return jsonify(res_users)


## おまじない
if __name__ == "__main__":
    app.run(debug=True, port=5901, host='0.0.0.0')