from sklearn.cluster import KMeans

def clustering(corpus_embeddings, num_clusters = 5):
    clustering_model = KMeans(n_clusters=num_clusters)
    clustering_model.fit(corpus_embeddings)
    cluster_assignment = clustering_model.labels_
    centers = clustering_model.cluster_centers_
    return cluster_assignment, centers

