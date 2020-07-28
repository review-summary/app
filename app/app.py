from flask import Flask, jsonify, request
from models.tfidf import predict

app = Flask(__name__)


@app.route('/', methods = ['POST'])
def main():
    data = request.get_json()
    return jsonify(predict(data))


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
