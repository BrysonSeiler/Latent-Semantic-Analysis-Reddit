from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score

import numpy as np
from scipy.stats import mode


def run_kmeans(num_clusters, matrix):

    print("Running k-means...\n")

    k_means = KMeans(n_clusters=num_clusters, init='k-means++')
    clusters = k_means.fit_predict(matrix)

    print("Successfully found %d clusters in %d dimensions \n" % k_means.cluster_centers_.shape)

    return clusters

def cluster(num_clusters, matrix, true_labels):

    clusters = run_kmeans(num_clusters, matrix)

    true_labels = np.asarray(true_labels)

    '''
    The following code was influenced by Jake VanderPlas's 
    in depth k-Means clustering tutorial outlined in his 
    Python Data Science Handbook.
    '''
    predicted_labels = np.zeros_like(clusters)

    for i in range(num_clusters):
        mask = (clusters == i)
        predicted_labels[mask] = mode(true_labels[mask])[0]

    print("Chosen clusters successfully grouped %0.3f submissions" % accuracy_score(true_labels, predicted_labels))