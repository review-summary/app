from flask import Flask, jsonify, request, render_template, redirect, url_for
import scipy

from models.arbitrary import predict, run_model, review_2_topic
from models.lda import *
from models.train import *
from models.bert import *
from models.clusterer import * 

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def form():
    products = [
        "Disney Mickey Mouse Deluxe Boys' Costume",
        "Levi's Men's 501 Original Fit Jeans, Polished Black, 44W x 30L",
        "Levi's Men's 501 Original-Fit Jeans, Trashed, 33W x 32L",
        "Hanes Absolutely Ultra Sheer Sheer Control Top SF (Single) Size:E Color:Jet",
        "Merrell Women's Jungle Moc Taupe Slip-On Shoe - 8.5 B(M) US",
        # "sofsy Soft-Touch Rayon Blend Tie Front Nursing & Maternity Fashion Top Charcoal Small",
        # "The Last Life: A Novel"
    ]
    if request.method == 'POST':
        selected = request.form.get("products")
        print(selected)
        # documents_rating_1, documents_rating_5, bow_corpus_1, bow_corpus_5, model_1, model_5 = run_model(selected)
        # sorted_topic_review_df_1_t0, sorted_topic_review_df_1_t1 = review_2_topic(documents_rating_1, model_1, bow_corpus_1)
        # sorted_topic_review_df_5_t0, sorted_topic_review_df_5_t1 = review_2_topic(documents_rating_5, model_5, bow_corpus_5)
        # print(sorted_topic_review_df_5_t0)
        number_of_sentences_display = m
        final_display = {}
        data = load_data("app/sample_reviews.json", product_name)
        corpus_embeddings = bert_model(product_name)
        cluster_assignment, centers = clustering(corpus_embeddings, num_clusters = 5)
        for k in range(num_clusters):
            cluster_indices = np.where(cluster_assignment == k)[0]
            cluster_embeddings = [corpus_embeddings[i] for i in cluster_indices]
            distance_from_centroids = scipy.spatial.distance.cdist(centers, cluster_embeddings, "cosine")
            closest_sentence_indices = distance_from_centroids[4].argsort()[-m:][::-1]
            display_sentences = [corpus[j] for j in closest_sentence_indices]
            final_display[k] = display_sentences
        p1 = final_display[0][0]
        p2 = final_display[0][1]
        p3 = final_display[0][2]
        n1 = final_display[0][1]
        n2 = final_display[0][1]
        n3 = final_display[0][1]
        print(p1, p2, n1, n2)
    else:
        selected = ""
        p1 = p2 = n1 = n2 = ""
    return render_template('form.html', products=products, selected=selected, 
    pos1=p1, 
    pos2=p2, 
    # pos3=p3, 
    neg1=n1,
    neg2=n2)
    # neg3=n3)


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
