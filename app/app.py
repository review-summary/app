from flask import Flask, jsonify, request
from inference import preprocess, predict

app = Flask(__name__)


@app.route('/', methods = ['POST'])
def main():
    data = request.get_json()
    data = preprocess(data)
    pred = predict(data)
    return jsonify(pred)


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
