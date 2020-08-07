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

        m = 5 # Num closest reviews to cluster centroid
        num_clusters = 5
        final_display_1 = {} # Negative reviews
        final_display_5 = {} # Positive reviews

        corpus_embeddings_1, corpus_embeddings_5, corpus = bert_model(selected)
        cluster_assignment_1, centers_1 = clustering(corpus_embeddings_1, num_clusters = 5)
        cluster_assignment_5, centers_5 = clustering(corpus_embeddings_5, num_clusters = 5)
        # print(corpus)
        def display(num_clusters, cluster_assignment, corpus_embeddings, cluster_centers, corpus, final_display):
            for k in range(num_clusters):
                cluster_indices = np.where(cluster_assignment == k)[0]
                cluster_embeddings = [corpus_embeddings[i] for i in cluster_indices]
                distance_from_centroids = scipy.spatial.distance.cdist(cluster_centers, cluster_embeddings, "cosine")
                closest_sentence_indices = distance_from_centroids[4].argsort()[-m:][::-1]
                display_sentences = [corpus[j] for j in closest_sentence_indices]
                final_display[k] = display_sentences
            return final_display
        final_display_1 = display(num_clusters, cluster_assignment_1, corpus_embeddings_1, centers_1, corpus, final_display_1)
        final_display_5 = display(num_clusters, cluster_assignment_5, corpus_embeddings_5, centers_5, corpus, final_display_5)
        print(final_display_1)
        # First index is the cluster, second index is the review index for that cluster (0 is closest to cluster centroid)
        # Play around with below to make them work with final UI design!
        p1 = final_display_5[0][0]
        p2 = final_display_5[0][1]
        p3 = final_display_5[0][1]
        n1 = final_display_1[2][0]
        n2 = final_display_1[3][0]
        n3 = final_display_1[4][0]
        print(p1, p2, p3, n1, n2, n3)
    else:
        selected = ""
        p1 = p2 = p3 = n1 = n2 = n3 = ""
    return render_template('form.html', products=products, selected=selected, 
    pos1=p1, 
    pos2=p2, 
    pos3=p3, 
    neg1=n1,
    neg2=n2,
    neg3=n3)


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
