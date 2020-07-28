from flask import Flask, request, jsonify
# from .. import models
# import sys
# sys.path.append('../models')
from tfidf_model.tfidf import tfidf_sum

app = Flask(__name__)

model = tfidf_sum()

@app.route('/', methods = ['GET', 'POST'])
def echo():
    if request.method == 'GET':
        data = request.args
    else:
        data = request.get_json()
    return jsonify(data)

@app.route('/show')
def show():
    reviews, raw_reviews = model.process_reviews(model.path, model.asin)
    tfidf_ratings = model.tfidf(reviews)
    summary, original_review = model.summarize_reviews(reviews, tfidf_ratings, raw_reviews)
    result = {}
    for i, sum in enumerate(summary):
        result[sum] = original_review[i]
    return jsonify(result)
    # return "Summarized Review is {} '\n' Original Review is {}".format(summary, original_review)

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
