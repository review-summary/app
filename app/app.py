from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def echo():
    if request.method == 'GET':
        data = request.args
    else:
        data = request.get_json()
    return jsonify(data)


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
