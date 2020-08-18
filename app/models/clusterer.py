from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min, pairwise_distances, pairwise_distances_argmin
import numpy as np

def clustering(corpus_embeddings, num_clusters = 5):
    # TODO: Should not hard code num_clusters, need a smart way to figure out optimal clusters
    clustering_model = KMeans(n_clusters=num_clusters)
    clustering_model.fit(corpus_embeddings)
    cluster_assignment = clustering_model.labels_
    centers = clustering_model.cluster_centers_
    return cluster_assignment, centers

def closest_points_to_cluster_centroid(cluster_assignment, corpus, centers, corpus_embeddings, number_closest_points=2):
    """
    Takes in rating specific cluster assignments for all text reviews in that rating. For the centroid in each of the cluster, 
    the function find the closes point to that centroid. It outputs a dictionary of centroid numbers and their respective 
    closest texts to the centroids. 
    """
    m_clusters = cluster_assignment.tolist()
    # print('m_clusters', m_clusters)
    centers = np.array(centers)
    # print(centers.shape)
    # print(centers)
    closest_data = {}
    for i in range(len(centers)):
        print("CLUSTER ", i)
        # Centroid for ith cluster, reshape for pairwise_distances function below
        center_vec = centers[i].reshape(1, -1)
        # For each of the cluster, find the indices in cluster_assignment
        data_idx_within_i_cluster = [idx for idx, clu_num in enumerate(m_clusters) if clu_num == i]
        # print("data_idx_within_i_cluster", data_idx_within_i_cluster)
        # Each row represent a review in the ith cluster, col represents the embedding size
        one_cluster_tf_matrix = np.zeros((len(data_idx_within_i_cluster), centers.shape[1]))
        # Populate each row with rating specific review embeddings
        for row_num, data_idx in enumerate(data_idx_within_i_cluster):
            one_row = corpus_embeddings[data_idx]
            one_cluster_tf_matrix[row_num] = one_row
        # print(center_vec.shape)
        # TODO find closes m points, given m <= len(points in cluster)
        # closest, _ = pairwise_distances_argmin_min(center_vec, one_cluster_tf_matrix, metric='cosine')
        # All cosine similarities of points (reviews) to centroid for ith cluster
        distances = pairwise_distances(center_vec, one_cluster_tf_matrix, metric='cosine')
        # distances=pairwise_distances_argmin(center_vec, one_cluster_tf_matrix, metric='cosine')
        # print("distances shape is ", distances.shape)
        # print(distances)
        closest_points_idx = distances.argsort()[0][::-1][:number_closest_points]
        # print('closest_points_idx', closest_points_idx)
        closest_idx_in_one_cluster_tf_matrix = closest_points_idx
        # print('closest_idx_in_one_cluster_tf_matrix', closest_idx_in_one_cluster_tf_matrix)
        closest_data_row_num = np.array(data_idx_within_i_cluster)[closest_idx_in_one_cluster_tf_matrix]
        # print('closest_data_row_num', closest_data_row_num)
        # print(type(corpus))
        data_id = np.array(corpus)[closest_data_row_num]
        # print(data_id) 
        # Use dictionary here will be helpful
        closest_data[i] = data_id

    # closest_data = list(set(closest_data))
    # print(closest_data)
    return closest_data
