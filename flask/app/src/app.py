from flask import Flask
import time

app = Flask(__name__)

@app.route('/')
def hello():
    name = "Hello World"
    return name

@app.route('/good')
def good():
    name = "Good"
    return name


@app.route('/sleep1sec')
def sleep1sec():
    time.sleep(1)
    name = "sleep1sec_succes"
    return name


## おまじない
if __name__ == "__main__":
    app.run(debug=True, port=5901, host='0.0.0.0')