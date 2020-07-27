from typing import Collection
from flask import Flask, request, jsonify

app = Flask(__name__)


def preprocess(documents: Collection[dict]) -> Collection[dict]:
    return documents


def predict(documents: Collection[dict]) -> Collection[dict]:
    return documents


@app.route('/', methods = ['POST'])
def main():
    data = request.get_json()
    data = preprocess(data)
    pred = predict(data)
    return jsonify(pred)


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
