from flask import Flask, request, render_template
import scipy
import numpy as np
import logging

from models.bert import bert_model
from models.clusterer import clustering, closest_points_to_cluster_centroid

log = logging.getLogger(__name__)
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
    
    selected = None
    pos = []
    neg = []
    
    if request.method == 'POST':
        selected = request.form.get("products")
        log.info("Making predictions for: %s", selected)

        m = 3 # Num closest reviews to cluster centroid
        num_clusters = 3
        final_display_1 = {} # Negative reviews
        
        final_display_5 = {} # Positive reviews

        corpus_embeddings_1, corpus_embeddings_5, corpus_1, corpus_5 = bert_model(selected)
        cluster_assignment_1_star, centers_1 = clustering(corpus_embeddings_1, num_clusters)
        cluster_assignment_5_star, centers_5 = clustering(corpus_embeddings_5, num_clusters)

        close_reviews_to_centroid_1 = closest_points_to_cluster_centroid(cluster_assignment_1_star, corpus_1, centers_1, corpus_embeddings_1, m)
        close_reviews_to_centroid_5 = closest_points_to_cluster_centroid(cluster_assignment_5_star, corpus_5, centers_5, corpus_embeddings_5, m)

        def display(num_clusters, cluster_assignment, corpus_embeddings, cluster_centers, corpus, final_display):
            for k in range(num_clusters):
                review_indices_cluster_k = np.where(cluster_assignment == k)[0]
                cluster_embeddings = [corpus_embeddings[i] for i in review_indices_cluster_k]
                # Find embeddings for each cluster
                centroid = cluster_centers[k]
                distance_from_centroids = scipy.spatial.distance.cdist(cluster_centers, cluster_embeddings, "cosine")
                closest_sentence_indices = distance_from_centroids[k].argsort()[-m:][::-1]
                display_sentences = [corpus[j] for j in closest_sentence_indices]
                final_display[k] = display_sentences

            return final_display
        
        final_display_1 = display(num_clusters, cluster_assignment_1_star, corpus_embeddings_1, centers_1, corpus_1, final_display_1)
        final_display_5 = display(num_clusters, cluster_assignment_5_star, corpus_embeddings_5, centers_5, corpus_5, final_display_5)
        log.info("Predicted: %s", final_display_1)
        # First index is the cluster, second index is the review index for that cluster (0 is closest to cluster centroid)
        # Play around with below to make them work with final UI design!
        
        num_clusters = len(final_display_5)
        
        for i in range(num_clusters):
            for j in range(len(final_display_5[i])):
                pos.append(final_display_5[i][j])
            for k in range(len(final_display_1[i])):
                neg.append(final_display_1[i][k])
    else:
        close_reviews_to_centroid_5 = close_reviews_to_centroid_1 = {}
    return render_template('form.html', products=products, selected=selected, positive=close_reviews_to_centroid_5.values(), negative=close_reviews_to_centroid_1.values())


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
