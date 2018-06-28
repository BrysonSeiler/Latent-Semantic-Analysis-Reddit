import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import (CountVectorizer, TfidfTransformer,
                                             TfidfVectorizer)

def run_count_vectorizer(num_comments, comments):

    vectorizer = CountVectorizer(stop_words=None)
    frequency_matrix = vectorizer.fit_transform(comments)
    feature_names = vectorizer.get_feature_names()
    frequency_df = pd.DataFrame(frequency_matrix.toarray(), columns=feature_names)

    index = []

    for i in range(num_comments):
        index.append("Comment %d" % i)

    frequency_df.index = index

    return frequency_df