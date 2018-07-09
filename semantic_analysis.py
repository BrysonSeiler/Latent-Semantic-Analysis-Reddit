import numpy as np
import pandas as pd
from pprint import pprint

from sklearn.feature_extraction.text import (CountVectorizer, TfidfTransformer,
                                             TfidfVectorizer)

from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer


class Subreddit_LSA:

    def __init__(self, frequency_df, tfidf_df, lsa_df, svd):
        self.frequency_df = frequency_df
        self.tfidf_df = tfidf_df
        self.lsa_df = lsa_df
        self.svd = svd


def run_count_vectorizer(num_strings, text):

    count_vectorizer = CountVectorizer(max_df=0.25, max_features=500)
    frequency_matrix = count_vectorizer.fit_transform(text)
    feature_names = count_vectorizer.get_feature_names()
    frequency_df = pd.DataFrame(frequency_matrix.toarray(), columns=feature_names)

    frequency_df = get_rownames(num_strings, frequency_df)

    print("Frequency matrix shape: %d by %d \n" % frequency_df.shape)

    return frequency_df, feature_names

def run_tfidf_vectorizer(num_strings, feature_names, frequency_df):

    tfidf_transformer = TfidfTransformer(use_idf=True, smooth_idf=True)
    tfidf_matrix = tfidf_transformer.fit_transform(frequency_df)
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)

    tfidf_df = get_rownames(num_strings, tfidf_df)

    print("Tfidf matrix shape: %d by %d \n" % (tfidf_df.shape[0], tfidf_df.shape[1]))

    return tfidf_df

def run_dimensionality_reduction(tfidf_df, subreddit_tags, numeric_tags, num_strings):

    '''
    This method was influenced by sklearn's 
    "Clustering text documents using k-means"
    '''

    svd = TruncatedSVD(n_components=300, n_iter=10, algorithm="randomized")
    reduced_matrix = svd.fit_transform(tfidf_df)
    reduced_matrix = Normalizer(copy=False).fit_transform(reduced_matrix)

    print("Successfully reduced data to %d submissions explained by %d features" % (reduced_matrix.shape))
    print("Reduced matrix shape: %d by %d \n" % reduced_matrix.shape)

    print("#-------------------------------------------------------------------------------#\n")

    print("Explained variance of first 5 components: %s \n" % str(svd.explained_variance_ratio_[:5]).strip("[]"))
    print("Singular values: %s \n" % str(svd.singular_values_[:5]).strip("[]"))
    print("Percent variance explained by all components: %.3f\n" % svd.explained_variance_ratio_.sum())

    print("#-------------------------------------------------------------------------------#\n")

    reduced_df = pd.DataFrame(reduced_matrix)

    reduced_df = get_rownames(num_strings, reduced_df)

    reduced_df.insert(loc=0, column='Subreddit', value=subreddit_tags)
    reduced_df.insert(loc=0, column='Numeric', value=numeric_tags)

    return reduced_matrix, reduced_df

def get_rownames(num_strings, dataframe):

    index = []

    for i in range(num_strings):
        index.append("Submission %s" % str(i+1))

    dataframe.index = index

    return dataframe

def run_lsa(num_strings, text, subreddit_tags, numeric_tags):

    print("#-------------------------------------------------------------------------------#")
    print("Learning vocabulary...\n")

    print("Building frequency matrix...")
    frequency_df, feature_names = run_count_vectorizer(num_strings, text)

    print("Building tf-idf matrix...")
    tfidf_df = run_tfidf_vectorizer(num_strings, feature_names, frequency_df)

    print("Reducing dimension of data...")
    reduced_matrix, reduced_df = run_dimensionality_reduction(tfidf_df, subreddit_tags, numeric_tags, num_strings)

    reduced_matrix = pd.DataFrame(reduced_matrix)

    return reduced_matrix, reduced_df
