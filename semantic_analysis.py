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

    for i in range(len(subreddit_objects)):
        for comment in subreddit_objects[i].comment_list:
            comment_list.append(comment)

    print("Total number of comments: %d \n" % len(comment_list))

    return comment_list

def run_count_vectorizer(num_comments, comments):

    vectorizer = CountVectorizer(stop_words=None)
    frequency_matrix = vectorizer.fit_transform(comments)
    feature_names = vectorizer.get_feature_names()
    frequency_df = pd.DataFrame(frequency_matrix.toarray(), columns=feature_names)

    frequency_df = get_rownames(num_comments, frequency_df)

    print("Frequency matrix shape: %d by %d \n" % (frequency_df.shape[0], frequency_df.shape[1]))

    print("Frequency matrix: \n")
    pprint(frequency_df)

    return frequency_df, feature_names

def run_tfidf_vectorizer(num_comments, feature_names, frequency_df):

    transformer = TfidfTransformer()
    tfidf_matrix = transformer.fit_transform(frequency_df)
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)

    tfidf_df = get_rownames(num_comments, tfidf_df)

    print("Tfidf matrix shape: %d by %d \n" % (tfidf_df.shape[0], tfidf_df.shape[1]))

    print("Tfidf matrix: \n")
    pprint(tfidf_df)

    return tfidf_df

def run_dimensionality_reduction(tfidf_df, dimension):

    svd = TruncatedSVD(dimension)
    lsa = make_pipeline(svd, Normalizer(copy=False))

    reduced_matrix = lsa.fit_transform(tfidf_df)

    return reduced_matrix

def get_rownames(num_comments, dataframe):

    index = []

    for i in range(num_comments):
        index.append("Comment %s" % str(i+1))

    dataframe.index = index

    return dataframe

def run_lsa(num_comments, comments):

    print("Building frequency matrix...")
    frequency_df, feature_names = run_count_vectorizer(num_comments, comments)

    print("Building tf-idf matrix...")
    tfidf_df = run_tfidf_vectorizer(num_comments, feature_names, frequency_df)

    print("Reducing dimension of data...")
    dimension = int(input("Input desired dimension: "))
    reduced_matrix = run_dimensionality_reduction(tfidf_df, dimension)

    pprint(reduced_matrix)

    return reduced_matrix
