from typing import Collection
from flask import Flask, request, jsonify

app = Flask(__name__)


def predict(documents: Collection[dict]) -> Collection[dict]:
    """Mock of the predict method, to be replaced with the code that we will use for making predictions.
    
    Currently it is just an identity function, but later we want to put the inference function in here.
    """
    return documents


@app.route('/', methods = ['POST'])
def main():
    data = request.get_json()
    preds = predict(data)
    return jsonify(preds)


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
