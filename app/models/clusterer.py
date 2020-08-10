from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import numpy as np

def clustering(corpus_embeddings, num_clusters = 5):
    clustering_model = KMeans(n_clusters=num_clusters)
    clustering_model.fit(corpus_embeddings)
    cluster_assignment = clustering_model.labels_
    centers = clustering_model.cluster_centers_
    return cluster_assignment, centers

def closest_points_to_cluster_centroid(cluster_assignment, corpus, centers, corpus_embeddings, number_closest_points=3):
    m_clusters = cluster_assignment.tolist()
    centers = np.array(centers)

    closest_data = []
    for i in range(len(centers)):
        center_vec = centers[i]
        data_idx_within_i_cluster = [ idx for idx, clu_num in enumerate(m_clusters) if clu_num == i ]

        one_cluster_tf_matrix = np.zeros( (  len(data_idx_within_i_cluster) , centers.shape[1] ) )
        for row_num, data_idx in enumerate(data_idx_within_i_cluster):
            one_row = corpus_embeddings[data_idx]
            one_cluster_tf_matrix[row_num] = one_row

        closest, _ = pairwise_distances_argmin_min(center_vec, one_cluster_tf_matrix)
        closest_idx_in_one_cluster_tf_matrix = closest[0]
        closest_data_row_num = data_idx_within_i_cluster[closest_idx_in_one_cluster_tf_matrix]
        data_id = all_data[closest_data_row_num]

        closest_data.append(data_id)

    closest_data = list(set(closest_data))
    # print(closest_data)
    return closest_data
