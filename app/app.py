from flask import Flask, jsonify, request, render_template, redirect, url_for

from models.arbitrary import predict, run_model, review_2_topic
from models.lda import *
from models.train import *

app = Flask(__name__)


product_name = "Disney Mickey Mouse Deluxe Boys' Costume"


@app.route('/', methods=['POST'])
def main():
    data = request.get_json()
    return jsonify(predict(data))


@app.route('/form', methods=['GET', 'POST'])
def form():
    products = [
        "Disney Mickey Mouse Deluxe Boys' Costume",
        "Levi's Men's 501 Original Fit Jeans, Polished Black, 44W x 30L",
        "Levi's Men's 501 Original-Fit Jeans, Trashed, 33W x 32L",
        "Hanes Absolutely Ultra Sheer Sheer Control Top SF (Single) Size:E Color:Jet",
        "Merrell Women's Jungle Moc Taupe Slip-On Shoe - 8.5 B(M) US",
        "sofsy Soft-Touch Rayon Blend Tie Front Nursing & Maternity Fashion Top Charcoal Small",
        "The Last Life: A Novel"
    ]
    if request.method == 'POST':
        selected = request.form.get("products")
        print(selected)
    else:
        selected = ""
    documents_rating_1, documents_rating_5, bow_corpus_1, bow_corpus_5, model_1, model_5 = run_model(products[0])
    sorted_topic_review_df_1_t1, sorted_topic_review_df_1_t0 = review_2_topic(documents_rating_1, model_1, bow_corpus_1)
    return render_template('form.html', products=products, selected=sorted_topic_review_df_1_t1.iloc[0]['reviewText'])


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
