import numpy as np
import pandas as pd
from pprint import pprint

from sklearn.feature_extraction.text import (CountVectorizer, TfidfTransformer,
                                             TfidfVectorizer)

from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import Pipeline, make_pipeline


class Subreddit_LSA:

    def __init__(self, frequency_df, tfidf_df, lsa_df, svd):
        self.frequency_df = frequency_df
        self.tfidf_df = tfidf_df
        self.lsa_df = lsa_df
        self.svd = svd


def get_comments(subreddit_objects):

    comment_list = []
    tag_list = []
    numeric_tag_list = []

    for i in range(len(subreddit_objects)):
        for comment in subreddit_objects[i].comment_list:
            comment_list.append(comment)
            tag_list.append(subreddit_objects[i].name)
            numeric_tag_list.append(i)

    print("Total number of comments: %d \n" % len(comment_list))

    return comment_list, tag_list, numeric_tag_list

def run_count_vectorizer(num_comments, comments):

    vectorizer = CountVectorizer(stop_words=None)
    frequency_matrix = vectorizer.fit_transform(comments)
    feature_names = vectorizer.get_feature_names()
    frequency_df = pd.DataFrame(frequency_matrix.toarray(), columns=feature_names)

    frequency_df = get_rownames(num_comments, frequency_df)

    print("Frequency matrix shape: %d by %d \n" % (frequency_df.shape[0], frequency_df.shape[1]))

    return frequency_df, feature_names

def run_tfidf_vectorizer(num_comments, feature_names, frequency_df):

    transformer = TfidfTransformer()
    tfidf_matrix = transformer.fit_transform(frequency_df)
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)

    tfidf_df = get_rownames(num_comments, tfidf_df)

    print("Tfidf matrix shape: %d by %d \n" % (tfidf_df.shape[0], tfidf_df.shape[1]))

    return tfidf_df

def run_dimensionality_reduction(tfidf_df, tags, numeric):

    '''
    This method was influenced by sklearn's 
    "Clustering text documents using k-means"
    '''

    svd = TruncatedSVD(n_components=100, n_iter=10, random_state=13)
    normalizer = Normalizer(copy=False)
    lsa = make_pipeline(svd, normalizer)

    reduced_matrix = lsa.fit_transform(tfidf_df)

    print("Reduced matrix shape: %d by %d \n" % (reduced_matrix.shape[0], reduced_matrix.shape[1]))
    print("Explained variance: %s \n" % str(svd.explained_variance_[:10]).strip("[]"))
    print("Singular values: %s \n" % str(svd.singular_values_[:10]).strip("[]"))

    reduced_df = pd.DataFrame(reduced_matrix)

    reduced_df.insert(loc=0, column='subreddit', value=tags)
    reduced_df.insert(loc=0, column='numeric', value=numeric)

    return reduced_df

def get_rownames(num_comments, dataframe):

    index = []

    for i in range(num_comments):
        index.append("Comment %s" % str(i+1))

    dataframe.index = index

    return dataframe

def run_lsa(num_comments, comments, tags, numeric):

    print("Building frequency matrix...")
    frequency_df, feature_names = run_count_vectorizer(num_comments, comments)

    print("Building tf-idf matrix...")
    tfidf_df = run_tfidf_vectorizer(num_comments, feature_names, frequency_df)

    print("Reducing dimension of data...")
    reduced_df = run_dimensionality_reduction(tfidf_df, tags, numeric)

    return reduced_df
