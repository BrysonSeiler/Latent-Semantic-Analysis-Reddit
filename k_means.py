import numpy as np
from nltk.cluster import KMeansClusterer, cosine_distance
from scipy.stats import mode
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score


def euclidean_cluster(num_clusters, matrix):

    print("Running k-means using euclidean distance...\n")

    k_means = KMeans(n_clusters=num_clusters, init='k-means++', n_init=100)
    clusters = k_means.fit_predict(matrix)

    print("Successfully found %d clusters in %d dimensions \n" % k_means.cluster_centers_.shape)

    return clusters

def cosine_cluster(num_clusters, matrix):

    print("Running k-means using cosine distance...\n")

    matrix = np.asanyarray(matrix)
    
    k_means = KMeansClusterer(num_clusters, cosine_distance, avoid_empty_clusters=True)
    clusters = k_means.cluster(matrix, assign_clusters=True, trace=False)

    print("Successfully found %d clusters in %d dimensions \n" % (num_clusters, matrix.shape[1]))

    return clusters
    

def get_statistics(num_clusters, clusters, true_labels):

    true_labels = np.asarray(true_labels)
    clusters = np.asarray(clusters)

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

    return predicted_labels


def run_kmeans(num_clusters, matrix, true_labels):

    print('''Distance metric:

            1. Euclidean
            2. Cosine (Slow on large batches)
    ''')

    user_input = int(input('Choose metric: '))

    if user_input == 1:
        clusters = euclidean_cluster(num_clusters, matrix)
        predicted_labels = get_statistics(num_clusters, clusters, true_labels)

        return predicted_labels

    if user_input == 2:
        clusters = cosine_cluster(num_clusters,matrix)
        predicted_labels = get_statistics(num_clusters, clusters, true_labels)

        return predicted_labels
