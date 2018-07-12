import pandas as pd

def get_word_frequency(frequency_df, subreddit_names, num_terms):

    word_frequency_df = pd.DataFrame(columns=subreddit_names)

    for subreddit in subreddit_names:

        #Grab all rows of frequency data frame that belong to the subreddit
        subreddit_block = pd.DataFrame(frequency_df.loc[frequency_df['Subreddit'] == subreddit])
        
        #Sort word frequencies in decending order
        sorted_frequencies = subreddit_block.drop('Subreddit', axis=1).sum(axis=0).sort_values(ascending=False)

        word_frequency_df[subreddit] = list(zip(sorted_frequencies[:num_terms], sorted_frequencies[:num_terms].index))

    print("Top %d most frequently occuring terms in each subreddit (frequency, word): \n " % num_terms)

    print(word_frequency_df, "\n")


def get_tfidf_score(tfidf_df, subreddit_names, num_terms):

    tfidf_score_df = pd.DataFrame(columns=subreddit_names)

    for subreddit in subreddit_names:

        #Grab all rows of frequency data frame that belong to the subreddit
        subreddit_block = pd.DataFrame(tfidf_df.loc[tfidf_df['Subreddit'] == subreddit])
        
        #Sort word frequencies in decending order
        sorted_scores = subreddit_block.drop('Subreddit', axis=1).sum(axis=0).sort_values(ascending=False)

        tfidf_score_df[subreddit] = list(zip(sorted_scores[:num_terms], sorted_scores[:num_terms].index))

    print("Top %d highest tfidf scoring terms in each subreddit (score, word): \n " % num_terms)

    print(tfidf_score_df, "\n")



